from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Subject organization
SUBJECT_CATEGORIES = {
    'core': {
        'title': '📘 Core Subjects',
        'subjects': [
            'Accountancy', 'Business Studies', 'Economics', 
            'Mathematics', 'English', 'Hindi'
        ],
        'icon': 'book-open'
    },
    'elective': {
        'title': '📙 Elective Subjects',
        'subjects': [
            'Statistics', 'Computer Science', 'Psychology', 'Sociology'
        ],
        'icon': 'book'
    },
    'aptitude': {
        'title': '🎯 Aptitudes & Skills',
        'subjects': [
            'Logical Reasoning', 'Numerical Aptitude', 'Critical Thinking',
            'Empathy', 'Memory', 'Communication', 'Creativity'
        ],
        'icon': 'brain'
    }
}

app = Flask(__name__)

# --- Load Pickle Files ---
print("Loading model files...")
with open("commerce_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("commerce_course_classifier.pkl", "rb") as f:
    clf = pickle.load(f)

with open("commerce_label_encoder.pkl", "rb") as f:
    le_course = pickle.load(f)

with open("commerce_feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

with open("commerce_dataset.pkl", "rb") as f:
    df = pickle.load(f)

print("All model files loaded successfully!")

def recommend_courses(user_profile, top_n=5):
    try:
        # Ensure user_profile is in the correct order matching feature_columns
        if isinstance(user_profile, dict):
            # If user_profile is a dict, convert to list in correct order
            user_profile = [user_profile.get(feature, 50) for feature in feature_columns]
        
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
            
            # Get career options (handle both string and list types)
            career_data = df_temp[df_temp["Course"] == course]["Career Options"].iloc[0]
            if isinstance(career_data, str):
                careers = [c.strip() for c in career_data.split(',')]
            elif isinstance(career_data, (list, np.ndarray)):
                careers = list(career_data)
            else:
                careers = [str(career_data)]
            
            # Find top contributing skills
            course_avg = df_temp[df_temp["Course"] == course][feature_columns].mean().values
            diff = np.abs(np.array(user_profile) - course_avg)
            top_features_idx = diff.argsort()[:3]  # 3 most aligned skills
            top_features = [feature_columns[i] for i in top_features_idx if i < len(feature_columns)]
            
            recommendations.append({
                "course": course,
                "similarity": round(float(sim), 3),
                "career_options": careers,
                "top_skills": top_features
            })
        
        return {"status": "success", "recommendations": recommendations}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    # Get all features from the loaded model
    all_features = list(feature_columns) if 'feature_columns' in globals() else []
    
    # Organize features into categories
    categories = {}
    for cat_id, cat_data in SUBJECT_CATEGORIES.items():
        # Only include subjects that exist in our feature columns
        valid_subjects = [s for s in cat_data['subjects'] if s in all_features]
        if valid_subjects:  # Only include non-empty categories
            categories[cat_id] = {
                'title': cat_data['title'],
                'subjects': valid_subjects,
                'icon': cat_data['icon']
            }
    
    return render_template('commerce_course_recommendation_.html', categories=categories)

@app.route('/api/features', methods=['GET'])
def get_features():
    # Return features organized by category
    all_features = list(feature_columns) if 'feature_columns' in globals() else []
    
    categories = {}
    for cat_id, cat_data in SUBJECT_CATEGORIES.items():
        valid_subjects = [s for s in cat_data['subjects'] if s in all_features]
        if valid_subjects:
            categories[cat_id] = {
                'title': cat_data['title'],
                'subjects': valid_subjects,
                'icon': cat_data['icon']
            }
    
    return jsonify({
        "status": "success",
        "categories": categories
    })

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        user_profile = [data.get(feature, 50) for feature in feature_columns]
        result = recommend_courses(user_profile)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Move HTML file to templates directory if it exists in the root
    html_file = 'commerce_course_recommendation_.html'
    if os.path.exists(html_file) and not os.path.exists(f'templates/{html_file}'):
        import shutil
        shutil.move(html_file, 'templates/')
    
    print("Starting Flask server...")
    print("Available routes:")
    print(f"- http://127.0.0.1:5001/ (Main application)")
    print(f"- http://127.0.0.1:5001/api/features (API endpoint for features)")
    print(f"- http://127.0.0.1:5001/api/recommend (API endpoint for recommendations)")
    
    app.run(debug=True, port=5001)
