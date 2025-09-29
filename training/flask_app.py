from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle
import os
from mistralai import Mistral
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize Mistral client
MISTRAL_API_KEY = "kw73FMj4V7HsZQ91CHei3N6TNfEN8ARn"  # In production, use environment variables
client = Mistral(api_key=MISTRAL_API_KEY)

app = Flask(__name__)

# Load models and encoders
def load_models():
    with open("stream_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("stream_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("stream_label_encoder.pkl", "rb") as f:
        le = pickle.load(f)
    return model, scaler, le

model, scaler, le = load_models()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Prepare input data in the correct order
        input_data = [
            data['math'],
            data['science'],
            data['biology'],
            data['english'],
            data['social'],
            data['language'],
            data['logical'],
            data['analytical'],
            data['numerical'],
            data['creativity'],
            data['communication'],
            data['artistic'],
            data['practical']
        ]
        
        # Convert to DataFrame with correct column names
        columns = [
            'Math', 'Science', 'Biology', 'English', 'SocialStudies', 'Language',
            'LogicalReasoning', 'AnalyticalSkills', 'NumericalAbility',
            'Creativity', 'CommunicationSkills', 'ArtisticSkills', 'PracticalSkills'
        ]
        
        input_df = pd.DataFrame([input_data], columns=columns)
        
        # Scale the input
        scaled_input = scaler.transform(input_df)
        
        # Make prediction
        probabilities = model.predict_proba(scaled_input)[0]
        stream_names = le.classes_
        
        # Get top 3 streams
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_streams = [stream_names[i] for i in top_indices]
        top_probs = [float(probabilities[i] * 100) for i in top_indices]
        
        # Prepare response
        result = {
            'status': 'success',
            'predictions': [
                {'stream': stream, 'probability': prob} 
                for stream, prob in zip(top_streams, top_probs)
            ],
            'best_stream': top_streams[0],
            'scores': data  # Include original scores for AI analysis
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

def format_score_analysis(scores, categorized_scores):
    """Format the score analysis section of the prompt."""
    analysis = []
    
    # Group subjects by category
    high = [subj for subj, cat in categorized_scores.items() if cat == 'high']
    moderate = [subj for subj, cat in categorized_scores.items() if cat == 'moderate']
    low = [subj for subj, cat in categorized_scores.items() if cat == 'low']
    
    # Build analysis sections
    if high:
        analysis.append("⭐ Strongest Areas (80-100%):")
        for subj in high:
            analysis.append(f"   - {subj}: {scores[subj]}%")
    
    if moderate:
        analysis.append("\n📊 Areas with Good Potential (60-80%):")
        for subj in moderate:
            analysis.append(f"   - {subj}: {scores[subj]}%")
    
    if low:
        analysis.append("\n📝 Areas Needing Improvement (Below 60%):")
        for subj in low:
            analysis.append(f"   - {subj}: {scores[subj]}%")
    
    return "\n".join(analysis)

def generate_insights_prompt(stream, scores, question=None, conversation_history=None):
    """Generate a prompt for the AI based on the context and conversation history."""
    if question:
        # For follow-up questions
        prompt = f"""
        You are a helpful career advisor. The user is interested in the {stream} career stream.
        
        Previous conversation:
        {conversation_history if conversation_history else 'No previous conversation'}
        
        User's question: {question}
        
        Please provide a helpful and detailed response to the user's question. 
        Keep it professional, accurate, and encouraging.
        """
    else:
        # Initial insights
        categorized_scores = {subject: categorize_score(score) for subject, score in scores.items()}
        prompt = f"""As a career advisor, provide personalized guidance based on the student's academic performance in the {stream} stream.
        
        Performance Analysis:
        {format_score_analysis(scores, categorized_scores)}
        
        Please provide a detailed career guidance report including:
        
        1. Career Suitability Analysis:
           - How their performance in key subjects aligns with {stream} careers
           - Strengths to leverage based on high-scoring subjects
           - Areas for improvement and how they might impact career choices
           
        2. Career Pathway Recommendations:
           - 3-5 specific career options that match their profile
           - For each, explain why it's a good fit based on their scores
           - Required qualifications and skills for each path
           
        3. Development Plan:
           - Key skills to focus on improving
           - Recommended courses or certifications
           - Extracurricular activities that could strengthen their profile
           
        4. Next Steps:
           - Immediate actions they can take
           - Resources for exploring careers further
           - How to build on their strengths and address weaknesses
        
        Format your response with clear sections and bullet points for better readability.
        Keep the tone professional, friendly, and encouraging.
        """
    return prompt.strip()

@app.route('/get_insights', methods=['POST'])
def get_insights():
    try:
        data = request.get_json()
        stream = data.get('stream')
        scores = data.get('scores', {})
        question = data.get('question')
        conversation_history = data.get('conversation_history')
        
        # Generate appropriate prompt based on context
        prompt = generate_insights_prompt(stream, scores, question, conversation_history)
        
        # Call Mistral API with the working format from Mistral_Chatbot.py
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": "You are a helpful career advisor. Provide accurate, professional, and encouraging career guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return jsonify({
            'status': 'success',
            'insights': response.choices[0].message.content
        })
        
    except Exception as e:
        app.logger.error(f"Error in get_insights: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Sorry, I encountered an error while processing your request.'
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5006)
