from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import jwt
import datetime
import joblib
import pandas as pd
import os
import traceback

app = Flask(__name__)
# Enable CORS for Next.js client
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'api-super-secret-key-change-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///api_site.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load ML Model
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
daily_model_path = os.path.join(MODEL_DIR, 'daily_stress_model.joblib')
daily_model = None
if os.path.exists(daily_model_path):
    daily_model = joblib.load(daily_model_path)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_completed = db.Column(db.Boolean, default=False)
    
    # Profile attributes
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

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow().date)
    sleep_hours = db.Column(db.Float, nullable=False)
    study_hours = db.Column(db.Float, nullable=False)
    mood = db.Column(db.Integer, nullable=False)
    physical_activity = db.Column(db.Float, nullable=False)
    social_interaction = db.Column(db.Float, nullable=False)
    stress_score = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# Token Authentication Decorator
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# === AUTH SERVICES ===
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing data'}), 400
        
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409
        
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'profile_completed': user.profile_completed
        }
    }), 200

# === USER DATA SERVICES ===
@app.route('/api/user/profile', methods=['GET', 'POST'])
@token_required
def profile(current_user):
    if request.method == 'GET':
        return jsonify({
            'username': current_user.username,
            'profile_completed': current_user.profile_completed,
            'gender': current_user.gender,
            'dep': current_user.dep
        }), 200
        
    if request.method == 'POST':
        data = request.get_json()
        
        current_user.gender = data.get('gender')
        current_user.dep = data.get('dep')
        current_user.financial = data.get('financial')
        current_user.profile_completed = True
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200

# === PREDICTION / CHECK-IN SERVICE ===
@app.route('/api/predict', methods=['POST'])
@token_required
def predict(current_user):
    try:
        data = request.get_json()
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
        
        # Save Log Daily
        today = datetime.datetime.utcnow().date()
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
        
        feedback = []
        if stress_score > 70:
            if sleep_hours < 6: feedback.append("Low sleep is driving your stress. Aim for 7+ hours.")
            if mood <= 2: feedback.append("Mood is running low. Take time to decompress.")
        elif stress_score < 40:
            feedback.append("Excellent metrics. Your habits are keeping stress low.")
        else:
            feedback.append("Moderate stress. Maintain your equilibrium.")

        return jsonify({
            "status": "success",
            "score": stress_score,
            "feedback": feedback
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'message': str(e)}), 400

# === REPORT GENERATION SERVICE ===
@app.route('/api/report', methods=['GET'])
@token_required
def report(current_user):
    last_7_days = datetime.datetime.utcnow().date() - datetime.timedelta(days=7)
    logs = DailyLog.query.filter(DailyLog.user_id == current_user.id, DailyLog.date >= last_7_days).order_by(DailyLog.date.asc()).all()
    
    data = []
    for log in logs:
        data.append({
            'date': log.date.strftime("%Y-%m-%d"),
            'display_date': log.date.strftime("%b %d"),
            'score': log.stress_score,
            'sleep': log.sleep_hours,
            'study': log.study_hours
        })
        
    avg_score = round(sum(l.stress_score for l in logs)/len(logs), 1) if logs else 0
    
    return jsonify({
        'logs': data,
        'avg_score': avg_score
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
