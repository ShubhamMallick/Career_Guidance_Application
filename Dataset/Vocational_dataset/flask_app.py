from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
import pandas as pd
import numpy as np
import pickle
import json
import os
import traceback
from sklearn.metrics.pairwise import cosine_similarity
from functools import wraps
from flask_cors import CORS

# Get the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app with template folder path
app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Load models and data
with open("vocational_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("vocational_course_classifier.pkl", "rb") as f:
    clf = pickle.load(f)

with open("vocational_label_encoder.pkl", "rb") as f:
    le_course = pickle.load(f)

# Define the feature columns based on the provided subjects
feature_columns = [
    'Fine Arts', 'Creativity', 'Communication', 'Empathy', 'English', 
    'Sociology', 'Memory', 'Computer Science', 'Mathematics', 'Statistics', 
    'Accountancy', 'Business Studies', 'Economics', 'Psychology', 'Hindi', 
    'Geography', 'Biology', 'Chemistry', 'Logical Reasoning', 'Critical Thinking', 
    'Numerical Aptitude'
]

# Load the dataset
with open("vocational_dataset.pkl", "rb") as f:
    df = pickle.load(f)
    
    # Ensure the dataset has all required columns
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0  # Initialize missing columns with 0

# Recommendation function
def recommend_courses(user_profile, top_n=5):
    try:
        # Ensure user_profile is a list with the correct number of features
        if len(user_profile) != len(feature_columns):
            raise ValueError(f"Expected {len(feature_columns)} features, got {len(user_profile)}")
            
        # Create a DataFrame with proper feature names for scaling
        user_df = pd.DataFrame([user_profile], columns=feature_columns)
        
        # Convert all values to numeric, handling any potential non-numeric values
        for col in feature_columns:
            user_df[col] = pd.to_numeric(user_df[col], errors='coerce').fillna(0)
        
        # Scale user input
        user_scaled = scaler.transform(user_df[feature_columns])
        
        # Scale the dataset for comparison
        X = df[feature_columns].copy()
        for col in X.columns:
            X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)
        X_scaled = scaler.transform(X)
        
        # Calculate similarity with all courses
        sims = cosine_similarity(user_scaled, X_scaled)[0]
        
        # Add similarity scores to dataframe
        df_temp = df.copy()
        df_temp["similarity"] = sims
        
        # Group by course and get mean similarity
        course_scores = df_temp.groupby("Course")["similarity"].mean().reset_index()
        
        # Get top N courses
        top_courses = course_scores.sort_values("similarity", ascending=False).head(top_n)
        
        # Add career options for each course
        recommendations = []
        for _, row in top_courses.iterrows():
            course = row["Course"]
            sim = row["similarity"]
            
            # Get all career options for this course
            careers = df_temp[df_temp["Course"] == course]["Career Options"].unique()
            
            recommendations.append({
                "Course": course,
                "Similarity": round(sim, 3),
                "Career Options": ", ".join(careers)
            })
        
        return pd.DataFrame(recommendations)
    except Exception as e:
        print(f"Error in recommend_courses: {str(e)}")
        # Return empty dataframe with expected columns
        empty_df = pd.DataFrame(columns=["Course", "Similarity", "Career Options"])
        print("Returning empty recommendations due to error")
        return empty_df

# Predict course function
def predict_course(user_profile):
    try:
        # Create a DataFrame with proper feature names for prediction
        user_df = pd.DataFrame([user_profile], columns=feature_columns)
        user_scaled = scaler.transform(user_df)
        pred = clf.predict(user_scaled)
        course = le_course.inverse_transform(pred)[0]
        return course
    except Exception as e:
        print(f"Error in predict_course: {str(e)}")
        return "Unknown"

# Routes
@app.route('/')
def index():
    return render_template('vocational_recommendation.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # Handle preflight
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200

    try:
        # Get JSON data from request
        if not request.is_json:
            print("Error: Request is not JSON")
            return jsonify({'success': False, 'error': 'Missing JSON in request'}), 400
            
        data = request.get_json()
        if not data:
            print("Error: No data in request")
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        print(f"Received data: {json.dumps(data, indent=2)}")
        
        # Ensure all required features are present, use default of 50 if missing
        user_profile = []
        missing_features = []
        
        for feature in feature_columns:
            if feature in data:
                try:
                    # Convert to float and ensure it's between 0-100
                    value = float(data[feature])
                    value = max(0, min(100, value))  # Clamp between 0-100
                    user_profile.append(value)
                except (ValueError, TypeError) as e:
                    app.logger.warning(f"Invalid value for {feature}: {data[feature]}, using default 50")
                    user_profile.append(50.0)
            else:
                app.logger.warning(f"Missing feature: {feature}, using default 50")
                missing_features.append(feature)
                user_profile.append(50.0)
        
        if missing_features:
            app.logger.warning(f"Missing features, using default values for: {', '.join(missing_features)}")
        
        # Verify we have the correct number of features
        if len(user_profile) != len(feature_columns):
            error_msg = f'Expected {len(feature_columns)} features, got {len(user_profile)}'
            app.logger.error(error_msg)
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Get recommendations
        try:
            app.logger.info("Generating recommendations...")
            recommendations_df = recommend_courses(user_profile)
            predicted_course = predict_course(user_profile)
            
            # Convert recommendations to list of dicts
            recommendations = []
            for _, row in recommendations_df.iterrows():
                recommendations.append({
                    'Course': str(row.get('Course', 'Unknown')),
                    'Similarity': float(row.get('Similarity', 0)),
                    'Career_Options': str(row.get('Career Options', 'Not specified'))
                })
            
            response_data = {
                'success': True,
                'predicted_course': str(predicted_course),
                'recommendations': recommendations
            }
            
            app.logger.info("Successfully generated recommendations")
            return jsonify(response_data)
            
        except Exception as e:
            error_msg = f'Error generating recommendations: {str(e)}'
            app.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({'success': False, 'error': error_msg}), 500
            
    except Exception as e:
        error_msg = f'An unexpected error occurred: {str(e)}'
        app.logger.error(f"{error_msg}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': error_msg}), 500

# Run the app
# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Starting Flask server...")
    print(f"Templates directory: {os.path.join(basedir, 'templates')}")
    print(f"Static directory: {os.path.join(basedir, 'static')}")
    
    app.run(host='0.0.0.0', port=5005, debug=True)
