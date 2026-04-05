from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
import traceback

app = Flask(__name__)

# Load Models
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
best_model = joblib.load(os.path.join(MODEL_DIR, 'best_model.joblib'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.joblib'))
encoder = joblib.load(os.path.join(MODEL_DIR, 'encoder.joblib'))
feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.joblib'))

# Mapping for output
mapping = {0: 'Awful', 1: 'Bad', 2: 'Good', 3: 'Fabulous'}

columns_to_encode = ['certification','gender','dep','hobbies','prefertime','likedegree','financial','parttime']
numerical_columns = ['height', 'weight', 'mark10th', 'mark12th', 'collegemark', 'studytime', 'salexpect', 'career_willing', 'smtime', 'travel']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        df_in = pd.DataFrame([data])
        
        # Ensure numerical columns are actually float/int
        for col in numerical_columns:
            df_in[col] = pd.to_numeric(df_in[col], errors='coerce').fillna(0)
        
        # Ensure string categorical columns
        for col in columns_to_encode:
            df_in[col] = df_in[col].astype(str)

        # Encoding categorical variables
        data_to_encode = df_in[columns_to_encode]
        encoded_arr = encoder.transform(data_to_encode)
        
        col_names = encoder.get_feature_names_out(columns_to_encode)
        encoded_df = pd.DataFrame(encoded_arr.toarray(), columns=col_names)
        
        # Drop and concatenate
        df_in = df_in.drop(columns=columns_to_encode)
        df_final = pd.concat([df_in.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
        
        # Reorder columns to match training EXACTLY
        # Handle any missing one-hot columns by filling 0
        for col in feature_names:
            if col not in df_final.columns:
                df_final[col] = 0.0
                
        df_final = df_final[feature_names]
        
        # Scale
        X_scaled = scaler.transform(df_final)
        
        # Predict
        pred = best_model.predict(X_scaled)[0]
        stress_level = mapping.get(pred, "Unknown")
        
        # Setup Standout Features / Explainable AI Insights
        insights = []
        travel_time = df_in['travel'].values[0]
        study_time = df_in['studytime'].values[0]
        sm_time = df_in['smtime'].values[0]
        part_time = str(data.get('parttime')).lower()
        
        if travel_time > 120:
             insights.append(f"Your heavy commute ({int(travel_time/60)} hrs) is a major contributor to exhaustion. Consider utilizing this time for light reading or audiobooks to distress.")
        
        if sm_time > 180:
             insights.append(f"High social media usage ({int(sm_time/60)} hrs) is negatively correlating with your well-being. Try a digital detox before bedtime.")
             
        if study_time < 60:
             insights.append("Low daily study time might be causing compounding academic pressure during exams.")
             
        if part_time == 'yes':
             insights.append("Balancing a part-time job with your coursework requires excellent time management. Don't forget to schedule rest days!")
             
        if not insights:
             insights.append("Your lifestyle metrics look well-balanced! Keep maintaining this healthy routine.")

        return jsonify({
            "status": "success",
            "prediction": stress_level,
            "insights": insights
        })
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
