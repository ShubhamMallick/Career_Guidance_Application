from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Load models and data
with open("pcm_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("pcm_course_classifier.pkl", "rb") as f:
    clf = pickle.load(f)

with open("pcm_label_encoder.pkl", "rb") as f:
    le_course = pickle.load(f)

with open("pcm_feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

with open("pcm_dataset.pkl", "rb") as f:
    df = pickle.load(f)

def recommend_courses(user_profile, top_n=5):
    """Generate course recommendations based on user profile"""
    user_scaled = scaler.transform([user_profile])
    
    # Calculate similarity with dataset
    sims = cosine_similarity(user_scaled, scaler.transform(df[feature_columns]))[0]
    df_temp = df.copy()
    df_temp["similarity"] = sims
    
    # Aggregate similarity per course
    course_scores = df_temp.groupby("Suggested_Course")["similarity"].mean().reset_index()
    top_courses = course_scores.sort_values("similarity", ascending=False).head(top_n)
    
    # Collect career options
    recommendations = []
    for _, row in top_courses.iterrows():
        course = row["Suggested_Course"]
        sim = row["similarity"]
        careers = df_temp[df_temp["Suggested_Course"] == course]["Career Options"].unique()
        recommendations.append({
            "course": course,
            "similarity": round(float(sim), 3),
            "careers": list(careers)
        })
    
    return recommendations

def predict_course(user_profile):
    """Predict the best fit course for the user"""
    user_scaled = scaler.transform([user_profile])
    pred = clf.predict(user_scaled)
    course = le_course.inverse_transform(pred)[0]
    return course

@app.route('/')
def home():
    return render_template('pcm_recommendation.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        user_profile = [data[col] for col in feature_columns]
        
        # Get predictions and recommendations
        best_course = predict_course(user_profile)
        recommendations = recommend_courses(user_profile, top_n=5)
        
        # Get careers for the best course
        careers = df[df["Suggested_Course"] == best_course]["Career Options"].unique().tolist()
        
        return jsonify({
            'status': 'success',
            'best_course': best_course,
            'recommendations': recommendations,
            'careers': careers
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Move HTML file to templates directory if it's not already there
    if os.path.exists('pcm_recommendation.html') and not os.path.exists('templates/pcm_recommendation.html'):
        import shutil
        shutil.move('pcm_recommendation.html', 'templates/pcm_recommendation.html')
    
    app.run(debug=True, port=5003)
