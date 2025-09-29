from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
# import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Load the pre-trained models and data
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("course_classifier.pkl", "rb") as f:
    clf = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le_course = pickle.load(f)

with open("feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

with open("dataset.pkl", "rb") as f:
    df = pickle.load(f)

def recommend_courses(user_profile, top_n=5):
    """
    Recommend courses based on user profile
    """
    try:
        # Ensure user_profile is a numpy array
        user_profile = np.array(user_profile, dtype=float).reshape(1, -1)
        
        # Scale input
        user_scaled = scaler.transform(user_profile)
        
        # Calculate similarity with dataset
        sims = cosine_similarity(user_scaled, scaler.transform(df[feature_columns]))[0]
        df["similarity"] = sims
        
        # Aggregate similarity per course
        course_scores = df.groupby("Course")["similarity"].mean().reset_index()
        top_courses = course_scores.sort_values("similarity", ascending=False).head(top_n)
        
        # Collect career options + top skills
        recommendations = []
        for _, row in top_courses.iterrows():
            course = row["Course"]
            sim = row["similarity"]
            
            # Get career options, handle potential missing column
            if "Career Options" in df.columns:
                career_data = df[df["Course"] == course]["Career Options"]
                if not career_data.empty:
                    careers = career_data.dropna().unique()
                    career_str = ", ".join(careers) if len(careers) > 0 else "Various career options available"
                else:
                    career_str = "Various career options available"
            else:
                career_str = "Career information not available"
            
            # Find top supporting skills
            if all(f in df.columns for f in feature_columns):
                course_data = df[df["Course"] == course][feature_columns]
                if not course_data.empty:
                    course_avg = course_data.mean().values
                    diffs = user_profile.flatten() - course_avg
                    top_features_idx = diffs.argsort()[::-1][:3]  # top 3 strengths
                    top_features = [feature_columns[i] for i in top_features_idx if i < len(feature_columns)]
                    top_skills = ", ".join(top_features) if top_features else "Various skills"
                else:
                    top_skills = "Various skills"
            else:
                top_skills = "Skill information not available"
            
            recommendations.append({
                "Course": str(course),
                "Similarity": float(round(sim, 3)),
                "Career Options": career_str,
                "Top Supporting Skills": top_skills
            })
        
        return recommendations
        
    except Exception as e:
        import traceback
        print(f"Error in recommend_courses: {str(e)}")
        print(traceback.format_exc())
        return []

@app.route('/')
def home():
    """Serve the main HTML page"""
    return app.send_static_file('arts_course_recommendation.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint for getting recommendations"""
    try:
        data = request.get_json()
        user_profile_dict = data.get('user_profile', {})
        
        # Convert dictionary to list in the correct feature order
        user_profile = [user_profile_dict.get(feature, 50) for feature in feature_columns]
        
        if len(user_profile) != len(feature_columns):
            return jsonify({
                'error': f'Expected {len(feature_columns)} features, got {len(user_profile)}',
                'features': feature_columns
            }), 400
            
        recommendations = recommend_courses(user_profile)
        return jsonify(recommendations)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/api/features', methods=['GET'])
def get_features():
    """Get the list of feature columns"""
    return jsonify({
        'features': feature_columns,
        'description': 'These are the features used for recommendations',
        'count': len(feature_columns)
    })

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Move the HTML file to static directory if it exists
    if os.path.exists('arts_course_recommendation.html'):
        import shutil
        shutil.move('arts_course_recommendation.html', 'static/arts_course_recommendation.html')
    
    # Run the app
    app.run(debug=True, port=5000)
