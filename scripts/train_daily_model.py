import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def generate_synthetic_data(num_samples=2000):
    np.random.seed(42)
    
    sleep_hours = np.random.uniform(3, 10, num_samples)
    study_hours = np.random.uniform(0, 10, num_samples)
    mood = np.random.randint(1, 6, num_samples) # 1 to 5
    physical_activity = np.random.uniform(0, 3, num_samples)
    social_interaction = np.random.uniform(0, 6, num_samples)
    
    stress_scores = []
    for i in range(num_samples):
        # Base logic for stress score (0-100)
        # Less sleep -> higher stress
        sleep_factor = (7 - sleep_hours[i]) * 8 # If sleep is 4, +24 stress. If 9, -16.
        
        # More study -> slight increase in academic stress, but too little might also cause exam stress (U-shape)
        if study_hours[i] < 2:
            study_factor = 10
        else:
            study_factor = study_hours[i] * 2
            
        # Low mood -> huge stress
        mood_factor = (3 - mood[i]) * 15 # If mood 1, +30 stress. If 5, -30.
        
        # Physical activity -> reduces stress
        physical_factor = physical_activity[i] * -7
        
        # Social interaction -> normal is good, too much could be distracting
        if social_interaction[i] < 1:
            social_factor = 5
        elif social_interaction[i] > 4:
            social_factor = (social_interaction[i] - 4) * 4 # Too much screen/social
        else:
            social_factor = -5
            
        base = 50 + sleep_factor + study_factor + mood_factor + physical_factor + social_factor
        
        # Add noise
        noise = np.random.normal(0, 5)
        
        # Clip to 0-100
        score = np.clip(int(base + noise), 0, 100)
        stress_scores.append(score)
        
    df = pd.DataFrame({
        'sleep_hours': sleep_hours,
        'study_hours': study_hours,
        'mood': mood,
        'physical_activity': physical_activity,
        'social_interaction': social_interaction,
        'stress_score': stress_scores
    })
    
    return df

def train_daily_model():
    print("Generating synthetic data for Option C ML Model...")
    df = generate_synthetic_data()
    
    X = df.drop('stress_score', axis=1)
    y = df['stress_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print(f"Model trained! MAE: {mae:.2f}, R2 Score: {r2:.2f}")
    
    os.makedirs('../models', exist_ok=True)
    joblib.dump(model, '../models/daily_stress_model.joblib')
    print("Model saved to ../models/daily_stress_model.joblib")

if __name__ == "__main__":
    train_daily_model()
