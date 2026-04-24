import sys
import os
import random
from datetime import datetime, timedelta
import pandas as pd
import joblib

# Add parent directory to path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, DailyLog
from werkzeug.security import generate_password_hash

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
daily_model_path = os.path.join(MODEL_DIR, 'daily_stress_model.joblib')
daily_model = None
if os.path.exists(daily_model_path):
    daily_model = joblib.load(daily_model_path)

TEST_ACCOUNTS = ['admin', 'shubham', 'div', 'dhruv', 'shanay']

def initialize_db():
    with app.app_context():
        # 1. Clean up old testing sessions
        print("Running routine database cleanup...")
        for username in TEST_ACCOUNTS:
            user = User.query.filter_by(username=username).first()
            if user:
                DailyLog.query.filter_by(user_id=user.id).delete()
                db.session.delete(user)
        db.session.commit()

        # 2. Create Admin Account
        print("Creating admin account...")
        admin_pass = generate_password_hash("admin123")
        student_pass = generate_password_hash("password123")
        admin = User(username='admin', password=admin_pass, profile_completed=True)
        db.session.add(admin)

        # 3. Setup Student Profiles
        print("Creating student accounts and profiles...")
        students = [
            {
                'username': 'shubham', 
                'profile': {'gender': 'Male', 'dep': 'BCA', 'financial': 'good', 'studytime': 3, 'smtime': 4, 'career_willing': 100}, 
                'pattern': 'high_stress'
            },
            {
                'username': 'div', 
                'profile': {'gender': 'Male', 'dep': 'Commerce', 'financial': 'Fabulous', 'studytime': 5, 'smtime': 1, 'career_willing': 100}, 
                'pattern': 'low_stress'
            },
            {
                'username': 'dhruv', 
                'profile': {'gender': 'Male', 'dep': 'B.com ISM', 'financial': 'Bad', 'studytime': 2, 'smtime': 6, 'career_willing': 0}, 
                'pattern': 'volatile'
            },
            {
                'username': 'shanay', 
                'profile': {'gender': 'Male', 'dep': 'B.com Accounting and Finance ', 'financial': 'good', 'studytime': 4, 'smtime': 2, 'career_willing': 100}, 
                'pattern': 'medium_stress'
            },
        ]

        today = datetime.utcnow().date()

        for s in students:
            # Create User
            user = User(
                username=s['username'],
                password=student_pass,
                profile_completed=True,
                gender=s['profile']['gender'],
                dep=s['profile']['dep'],
                financial=s['profile']['financial'],
                studytime=s['profile']['studytime'],
                smtime=s['profile']['smtime'],
                career_willing=s['profile']['career_willing'],
                # Fill required fallback fields
                height=175, weight=70, mark10th=80, mark12th=80, collegemark=80,
                certification='No', likedegree='Yes', salexpect=50000, prefertime='Morning',
                hobbies='Sports', travel=30, parttime='No'
            )
            db.session.add(user)
            db.session.commit()

            # 4. Generate 10 days of DailyLogs
            print(f"Generating 10 days of logs for {s['username']}...")
            for i in range(10):
                d = today - timedelta(days=9-i)
                
                # Varied habit patterns for realistic presentation graphs
                if s['pattern'] == 'high_stress':
                    sleep = random.uniform(3, 5.5)
                    study = random.uniform(4, 8)
                    mood = random.randint(1, 2)
                    physical = random.uniform(0, 1)
                    social = random.uniform(4, 7)
                elif s['pattern'] == 'low_stress':
                    sleep = random.uniform(7, 9)
                    study = random.uniform(3, 6)
                    mood = random.randint(4, 5)
                    physical = random.uniform(1.5, 2.5)
                    social = random.uniform(1, 3)
                elif s['pattern'] == 'medium_stress':
                    sleep = random.uniform(6, 7.5)
                    study = random.uniform(2, 5)
                    mood = random.randint(3, 4)
                    physical = random.uniform(0.5, 1.5)
                    social = random.uniform(2, 4)
                else: # volatile pattern
                    sleep = random.uniform(4, 8)
                    study = random.uniform(1, 7)
                    mood = random.randint(1, 5)
                    physical = random.uniform(0, 2)
                    social = random.uniform(1, 7)

                # Use model to predict realistic score, fallback to random if missing
                df_in = pd.DataFrame([{
                    'sleep_hours': sleep,
                    'study_hours': study,
                    'mood': mood,
                    'physical_activity': physical,
                    'social_interaction': social
                }])
                
                score = daily_model.predict(df_in)[0] if daily_model else random.randint(20, 90)
                score = round(float(score), 1)

                log = DailyLog(
                    user_id=user.id,
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

        print("\n✅ Database initialization sequence complete.")
        print("Accounts configured:")
        print("  - admin")
        for s in students:
            print(f"  - {s['username']}")

if __name__ == "__main__":
    initialize_db()
