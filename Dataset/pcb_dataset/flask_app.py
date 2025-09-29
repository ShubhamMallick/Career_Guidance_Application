from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
from functools import wraps
import time

# Subject organization
SUBJECT_CATEGORIES = {
    'core': {
        'title': '📘 Core Subjects',
        'subjects': [
            'Physics', 'Chemistry', 'Biology', 
            'Mathematics', 'English', 'Hindi'
        ],
        'icon': 'atom',
        'description': 'Fundamental subjects that form the core of the PCB stream'
    },
    'elective': {
        'title': '📙 Elective Subjects',
        'subjects': [
            'Psychology', 'Computer Science', 'Research Skills'
        ],
        'icon': 'flask',
        'description': 'Complementary subjects that enhance your scientific knowledge'
    },
    'aptitude': {
        'title': '🎯 Aptitudes & Skills',
        'subjects': [
            'Logical Reasoning', 'Analytical Thinking', 'Critical Thinking',
            'Problem-Solving', 'Communication', 'Creativity',
            'Numerical Aptitude', 'Empathy', 'Attention to Detail'
        ],
        'icon': 'brain',
        'description': 'Essential skills for success in scientific careers'
    }
}

app = Flask(__name__)

# --- Load Pickle Files ---
print("Loading model files...")
try:
    with open("pcb_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    
    with open("pcb_course_classifier.pkl", "rb") as f:
        clf = pickle.load(f)
    
    with open("pcb_label_encoder.pkl", "rb") as f:
        le_course = pickle.load(f)
    
    with open("pcb_feature_columns.pkl", "rb") as f:
        feature_columns = pickle.load(f)
    
    with open("pcb_dataset.pkl", "rb") as f:
        df = pickle.load(f)
    
    print("All model files loaded successfully!")
    print(f"Feature columns: {feature_columns}")
    print(f"Dataset columns: {df.columns.tolist()}")
    print(f"Sample career options: {df['Career Option'].head().tolist()}")
    
except Exception as e:
    print(f"Error loading model files: {str(e)}")
    raise

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def recommend_courses(user_profile, top_n=5):
    try:
        # Convert user profile to list if it's a dictionary
        if isinstance(user_profile, dict):
            user_profile = [user_profile.get(feature, 50) for feature in feature_columns]
        
        # Ensure we have the right number of features
        if len(user_profile) != len(feature_columns):
            raise ValueError(f"Expected {len(feature_columns)} features, got {len(user_profile)}")
        
        # Scale the input
        user_scaled = scaler.transform([user_profile])
        
        # Calculate similarity with all courses
        sims = cosine_similarity(user_scaled, scaler.transform(df[feature_columns]))[0]
        df_temp = df.copy()
        df_temp["similarity"] = sims
        
        # Aggregate similarity per course
        course_scores = df_temp.groupby("Course")["similarity"].mean().reset_index()
        top_courses = course_scores.sort_values("similarity", ascending=False).head(top_n)
        
        recommendations = []
        for _, row in top_courses.iterrows():
            course = row["Course"]
            sim = row["similarity"]
            
            # Get career options (handle different column names)
            career_col = next((col for col in ['Career Option', 'Career_Options', 'CareerOptions', 'Career'] 
                             if col in df_temp.columns), None)
            
            if career_col is None:
                careers = ["Various careers in this field"]
            else:
                career_data = df_temp[df_temp["Course"] == course][career_col].iloc[0]
                if pd.isna(career_data):
                    careers = ["Various careers in this field"]
                elif isinstance(career_data, str):
                    careers = [c.strip() for c in career_data.split(',')]
                elif isinstance(career_data, (list, np.ndarray)):
                    careers = list(career_data)
                else:
                    careers = [str(career_data)]
            
            # Find top contributing skills (most aligned with user's strengths)
            course_avg = df_temp[df_temp["Course"] == course][feature_columns].mean().values
            diffs = np.array(user_profile) - course_avg
            top_features_idx = diffs.argsort()[::-1][:3]  # Top 3 strengths
            top_features = [feature_columns[i] for i in top_features_idx if i < len(feature_columns)]
            
            recommendations.append({
                "course": course,
                "similarity": round(float(sim), 3),
                "career_options": careers[:3],  # Limit to top 3 careers
                "top_skills": top_features
            })
        
        return recommendations
    except Exception as e:
        print(f"Error in recommend_courses: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

@app.route('/')
def home():
    """Render the main page with subject sliders"""
    # Check for any missing features in the dataset
    all_subjects = []
    for category in SUBJECT_CATEGORIES.values():
        all_subjects.extend(category['subjects'])
    
    missing_features = [subj for subj in all_subjects if subj not in feature_columns]
    if missing_features:
        print(f"Warning: The following subjects are not in the feature columns: {missing_features}")
    
    return render_template(
        'pcb_recommendation.html',
        categories=SUBJECT_CATEGORIES,
        all_subjects=all_subjects,
        missing_features=missing_features
    )

@app.route('/get_features', methods=['GET'])
def get_features():
    """Return the list of all features in order"""
    return jsonify({
        'features': feature_columns,
        'subjects': [subj for cat in SUBJECT_CATEGORIES.values() for subj in cat['subjects']]
    })

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """Handle recommendation requests"""
    try:
        data = request.get_json()
        if not data or 'scores' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No scores provided'
            }), 400
        
        # Convert scores to list in the correct order
        scores = data['scores']
        if isinstance(scores, dict):
            # Ensure all required features are present
            for feature in feature_columns:
                if feature not in scores:
                    scores[feature] = 50  # Default value
            # Convert to list in correct order
            scores = [scores[feature] for feature in feature_columns]
        
        print(f"Getting recommendations for scores: {scores}")
        
        # Get recommendations
        recommendations = recommend_courses(scores)
        
        print(f"Generated {len(recommendations)} recommendations")
        return jsonify({
            'status': 'success',
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        }), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"success": False, "error": "No input data provided"}), 400
        
        # Create a list of values in the same order as feature_columns
        user_input = []
        for feature in feature_columns:
            value = data.get(feature, 0)
            # Ensure the value is within 0-100 range
            value = max(0, min(100, int(value)))
            user_input.append(value)
        
        # Get recommendations
        recommendations = recommend_courses(user_input)
        
        if not recommendations:
            return jsonify({
                "success": False, 
                "error": "No recommendations could be generated"
            }), 400
            
        return jsonify({
            "success": True, 
            "recommendations": recommendations,
            "timestamp": time.time()
        })
        
    except Exception as e:
        print(f"Error in recommend endpoint: {str(e)}")
        return jsonify({
            "success": False, 
            "error": f"An error occurred: {str(e)}"
        }), 500

# Error handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error="Page not found"), 404

# Error handler for 500 errors
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Print server info
    print("\n" + "="*50)
    print("PCB Course & Career Recommendation System")
    print("="*50)
    print(f"Loaded {len(df)} courses with {len(feature_columns)} features")
    print(f"Available courses: {len(df['Course'].unique())}")
    print("\nStarting server... (Press Ctrl+C to stop)")
    print("="*50 + "\n")
    
    # Run the app
    app.run(debug=True, port=5002, threaded=True)