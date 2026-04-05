from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import numpy as np
import os
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key-change-in-prod')

# Use Supabase/Remote DB if available, otherwise fallback to local SQLite
db_url = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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

# Database Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Static Variables
    gender = db.Column(db.String(20))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    financial = db.Column(db.String(20))
    dep = db.Column(db.String(50))
    mark10th = db.Column(db.Float)
    mark12th = db.Column(db.Float)
    collegemark = db.Column(db.Float)
    certification = db.Column(db.String(10))
    likedegree = db.Column(db.String(10))
    salexpect = db.Column(db.Float)
    career_willing = db.Column(db.Float)
    prefertime = db.Column(db.String(50))
    hobbies = db.Column(db.String(50))
    travel = db.Column(db.Float)
    parttime = db.Column(db.String(10))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if current_user.is_authenticated:
        if not current_user.profile_completed:
            return redirect(url_for('profile'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check username and password", "error")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Username already exists. Please login.", "error")
            return redirect(url_for('signup'))
            
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.gender = request.form.get('gender')
        current_user.height = float(request.form.get('height', 0))
        current_user.weight = float(request.form.get('weight', 0))
        current_user.financial = request.form.get('financial')
        current_user.dep = request.form.get('dep')
        current_user.mark10th = float(request.form.get('mark10th', 0))
        current_user.mark12th = float(request.form.get('mark12th', 0))
        current_user.collegemark = float(request.form.get('collegemark', 0))
        current_user.certification = request.form.get('certification')
        current_user.likedegree = request.form.get('likedegree')
        current_user.salexpect = float(request.form.get('salexpect', 0))
        current_user.career_willing = float(request.form.get('career_willing', 0))
        current_user.prefertime = request.form.get('prefertime')
        current_user.hobbies = request.form.get('hobbies')
        current_user.travel = float(request.form.get('travel', 0))
        current_user.parttime = request.form.get('parttime')
        
        current_user.profile_completed = True
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=current_user)

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.profile_completed:
        return redirect(url_for('profile'))
    return render_template('dashboard.html', user=current_user)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        # Data from daily check-in
        data = request.json
        studytime = float(data.get('studytime', 0))
        smtime = float(data.get('smtime', 0))
        
        # Merge with User Profile (Static Data)
        combined_data = {
            'gender': current_user.gender,
            'height': current_user.height,
            'weight': current_user.weight,
            'financial': current_user.financial,
            'dep': current_user.dep,
            'mark10th': current_user.mark10th,
            'mark12th': current_user.mark12th,
            'collegemark': current_user.collegemark,
            'certification': current_user.certification,
            'likedegree': current_user.likedegree,
            'salexpect': current_user.salexpect,
            'career_willing': current_user.career_willing,
            'prefertime': current_user.prefertime,
            'hobbies': current_user.hobbies,
            'travel': current_user.travel,
            'parttime': current_user.parttime,
            # Merged Daily Variables
            'studytime': studytime,
            'smtime': smtime
        }
        
        df_in = pd.DataFrame([combined_data])
        
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
        travel_time = combined_data['travel']
        study_time = combined_data['studytime']
        sm_time = combined_data['smtime']
        part_time = str(combined_data['parttime']).lower()
        
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
