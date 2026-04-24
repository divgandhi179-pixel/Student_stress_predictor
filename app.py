from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import numpy as np
import os
import traceback
from datetime import datetime, timedelta

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
daily_model_path = os.path.join(MODEL_DIR, 'daily_stress_model.joblib')
daily_model = None
if os.path.exists(daily_model_path):
    daily_model = joblib.load(daily_model_path)

best_model_path = os.path.join(MODEL_DIR, 'best_model.joblib')
scaler_path = os.path.join(MODEL_DIR, 'scaler.joblib')
encoder_path = os.path.join(MODEL_DIR, 'encoder.joblib')
feature_names_path = os.path.join(MODEL_DIR, 'feature_names.joblib')

baseline_model = None
scaler = None
encoder = None
feature_names = None

if os.path.exists(best_model_path):
    baseline_model = joblib.load(best_model_path)
    scaler = joblib.load(scaler_path)
    encoder = joblib.load(encoder_path)
    feature_names = joblib.load(feature_names_path)

# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Keeping old static vars for backwards compatibility
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
    studytime = db.Column(db.Float)
    smtime = db.Column(db.Float)

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    sleep_hours = db.Column(db.Float, nullable=False)
    study_hours = db.Column(db.Float, nullable=False)
    mood = db.Column(db.Integer, nullable=False)
    physical_activity = db.Column(db.Float, nullable=False)
    social_interaction = db.Column(db.Float, nullable=False)
    stress_score = db.Column(db.Float, nullable=False)

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
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/run_setup')
def run_setup():
    import subprocess
    result = subprocess.run(["python", "scripts/db_setup.py"], capture_output=True, text=True)
    return f"<pre>Database setup executed.\n\nOutput:\n{result.stdout}\n\nErrors:\n{result.stderr}</pre>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
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
        current_user.studytime = float(request.form.get('studytime', 0))
        current_user.smtime = float(request.form.get('smtime', 0))
        
        current_user.profile_completed = True
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=current_user)

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.username != 'admin':
        return redirect(url_for('dashboard'))
        
    users = User.query.filter(User.username != 'admin').all()
    user_data = []
    
    for u in users:
        last_10_days = datetime.utcnow().date() - timedelta(days=10)
        logs = DailyLog.query.filter(DailyLog.user_id == u.id, DailyLog.date >= last_10_days).all()
        scores = [l.stress_score for l in logs]
        avg_stress = round(sum(scores) / len(scores), 1) if scores else 0
        
        if avg_stress > 70: status = 'Critical'
        elif avg_stress > 40: status = 'Moderate'
        elif avg_stress > 0: status = 'Stable'
        else: status = 'No Data'
        
        user_data.append({
            'username': u.username,
            'dep': u.dep or 'N/A',
            'days_logged': len(logs),
            'avg_stress': avg_stress,
            'status': status
        })
        
    total_users = len(users)
    valid_scores = [u['avg_stress'] for u in user_data if u['avg_stress'] > 0]
    platform_avg = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else 0
    
    return render_template('admin.html', user=current_user, users=user_data, total_users=total_users, platform_avg=platform_avg)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.username == 'admin':
        return redirect(url_for('admin_panel'))
    if not current_user.profile_completed:
        return redirect(url_for('profile'))
        
    baseline_stress_level = "Unknown"
    
    if baseline_model and encoder and scaler and feature_names:
        try:
            df_in = pd.DataFrame([{
                'certification': current_user.certification,
                'gender': current_user.gender,
                'dep': current_user.dep,
                'mark10th': current_user.mark10th,
                'mark12th': current_user.mark12th,
                'collegemark': current_user.collegemark,
                'studytime': current_user.studytime,
                'prefertime': current_user.prefertime,
                'salexpect': current_user.salexpect,
                'likedegree': current_user.likedegree,
                'career_willing': current_user.career_willing,
                'smtime': current_user.smtime,
                'travel': current_user.travel,
                'financial': current_user.financial,
                'parttime': current_user.parttime,
                'hobbies': current_user.hobbies
            }])
            
            columns_to_encode = ['certification', 'gender', 'dep', 'hobbies', 'prefertime', 'likedegree', 'financial', 'parttime']
            data_to_encode = df_in[columns_to_encode]
            encoded_data = encoder.transform(data_to_encode)
            encoded_df = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out(columns_to_encode))
            
            df_in = df_in.drop(columns=columns_to_encode)
            df_final = pd.concat([df_in, encoded_df], axis=1)
            df_final = df_final[feature_names] 
            
            scaled_data = scaler.transform(df_final)
            pred = baseline_model.predict(scaled_data)[0]
            
            mapping = {0: 'Low Stress', 1: 'Medium Stress', 2: 'High Stress'}
            baseline_stress_level = mapping.get(pred, "Unknown")
            
        except Exception as e:
            print("Baseline Predict Error:", traceback.format_exc())
            
    return render_template('dashboard.html', user=current_user, baseline_stress=baseline_stress_level)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.json
        sleep_hours = float(data.get('sleep_hours', 7))
        study_hours = float(data.get('study_hours', 2))
        mood = int(data.get('mood', 3))
        physical_activity = float(data.get('physical_activity', 0))
        social_interaction = float(data.get('social_interaction', 2))
        
        # ML Inference
        df_in = pd.DataFrame([{
            'sleep_hours': sleep_hours,
            'study_hours': study_hours,
            'mood': mood,
            'physical_activity': physical_activity,
            'social_interaction': social_interaction
        }])
        
        stress_score = daily_model.predict(df_in)[0] if daily_model else 50
        stress_score = round(float(stress_score), 1)
        
        # Save to DB - Check if entry for today exists and overwrite, or create new
        today = datetime.utcnow().date()
        log = DailyLog.query.filter_by(user_id=current_user.id, date=today).first()
        if not log:
            log = DailyLog(user_id=current_user.id, date=today)
            db.session.add(log)
            
        log.sleep_hours = sleep_hours
        log.study_hours = study_hours
        log.mood = mood
        log.physical_activity = physical_activity
        log.social_interaction = social_interaction
        log.stress_score = stress_score
        
        db.session.commit()
        
        # Real-time feedback insights
        feedback = []
        if stress_score > 70:
            if sleep_hours < 6:
                 feedback.append("Low sleep is heavily driving your high stress today. Try to get at least 7 hours.")
            if mood <= 2:
                 feedback.append("Your mood is running low. Take some time to decompress or chat with a friend.")
            if social_interaction > 5:
                 feedback.append("High screen/social time might be overwhelming you.")
        elif stress_score < 40:
            feedback.append("Great day! Your habits are keeping stress at an excellent low level.")
        else:
            feedback.append("Moderate stress. Keep balancing your study time with adequate physical activity.")

        return jsonify({
            "status": "success",
            "score": stress_score,
            "feedback": feedback
        })
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/report')
@login_required
def report():
    # Fetch last 7 days of logs
    last_7_days = datetime.utcnow().date() - timedelta(days=7)
    logs = DailyLog.query.filter(DailyLog.user_id == current_user.id, DailyLog.date >= last_7_days).order_by(DailyLog.date.asc()).all()
    
    dates = [log.date.strftime("%b %d") for log in logs]
    scores = [log.stress_score for log in logs]
    
    avg_score = round(sum(scores)/len(scores), 1) if scores else 0
    
    # Generate insights Based on patterns
    insights = []
    if logs:
        highest_day = max(logs, key=lambda x: x.stress_score)
        lowest_day = min(logs, key=lambda x: x.stress_score)
        
        insights.append(f"Highest stress day: {highest_day.date.strftime('%A')} ({highest_day.stress_score})")
        insights.append(f"Lowest stress day: {lowest_day.date.strftime('%A')} ({lowest_day.stress_score})")
        
        high_stress_logs = [l for l in logs if l.stress_score >= 60]
        if high_stress_logs:
            avg_sleep_high = sum(l.sleep_hours for l in high_stress_logs) / len(high_stress_logs)
            if avg_sleep_high < 6:
                insights.append(f"Suggestion: On high stress days, your average sleep is only {avg_sleep_high:.1f} hours. Improving sleep is a clear priority.")
        
    return render_template('report.html', user=current_user, dates=dates, scores=scores, avg_score=avg_score, insights=insights, logs=logs)

@app.route('/seed')
@login_required
def seed():
    # Seed 7 days of demo data
    today = datetime.utcnow().date()
    db.session.query(DailyLog).filter_by(user_id=current_user.id).delete()
    
    import random
    for i in range(7):
        d = today - timedelta(days=6-i)
        
        # Add varied logic for demo
        sleep = random.uniform(4, 9)
        study = random.uniform(1, 8)
        mood = random.randint(1, 5)
        physical = random.uniform(0, 2)
        social = random.uniform(1, 5)
        
        # Inference
        df_in = pd.DataFrame([{
            'sleep_hours': sleep,
            'study_hours': study,
            'mood': mood,
            'physical_activity': physical,
            'social_interaction': social
        }])
        score = daily_model.predict(df_in)[0] if daily_model else random.randint(20, 90)
        
        log = DailyLog(
            user_id=current_user.id,
            date=d,
            sleep_hours=sleep,
            study_hours=study,
            mood=mood,
            physical_activity=physical,
            social_interaction=social,
            stress_score=score
        )
        db.session.add(log)
    db.session.commit()
    return redirect(url_for('report'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
