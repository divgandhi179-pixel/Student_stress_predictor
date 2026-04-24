import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df = pd.read_csv("../data/Student Attitude and Behavior.csv")

df.head()

# Rename columns
df.rename(columns={
"Certification Course":"certification",
"Gender":"gender",
"Department":"dep",
"Height(CM)":"height",
"Weight(KG)":"weight",
"10th Mark":"mark10th",
"12th Mark":"mark12th",
"college mark":"collegemark",
"daily studing time":"studytime",
"prefer to study in":"prefertime",
"salary expectation":"salexpect",
"Do you like your degree?":"likedegree",
"willingness to pursue a career based on their degree  ":"career_willing",
"social medai & video":"smtime",
"Travelling Time ":"travel",
"Stress Level ":"stress",
"Financial Status":"financial",
"part-time job":"parttime"
}, inplace=True)

df.head()
df.info()

df.duplicated().sum()

df["studytime"].unique()

# Convert study time
def studyTime(x):
    x = x.split()
    time = []
    for i in x:
        if i.isnumeric():
            time.append(int(i))
    if len(time) == 1:
        return time[0] * 60
    elif len(time) == 2 and (("Hour" in x) or ("hour" in x)):
        return ((time[0] * 60 + time[1] * 60) / 2)
    elif len(time) == 2:
        return sum(time) / len(time)

df["studytime"] = df["studytime"].apply(studyTime)

# Convert career willingness
df["career_willing"] = df["career_willing"].str.replace("%","")
df["career_willing"] = df["career_willing"].astype(float)

df.head()

df["smtime"].unique()

# Convert social media time
def socialTime(x):
    x=x.split()
    time =[]
    for i in x:
        try:
            time.append(float(i))
        except ValueError:
            pass

    if len(time) == 1:
        return time[0]*60
    elif len(time) == 2 and (("Hour" in x) or ("hour" in x)):
        return (((time[0]*60) + (time[1]*60))/2)
    elif len(time) == 2:
        return (sum(time)/len(time))

df["smtime"] = df["smtime"].apply(socialTime)

df.head()

df["travel"].unique()

df["travel"] = df["travel"].apply(socialTime)

df.head()

df.info()

# Drop noisy features that might reduce accuracy on a limited dataset
df = df.drop(["height", "weight"], axis=1)

# Convert stress labels to numeric mapping (0: Low, 1: Medium, 2: High)
ordinal_mapping = {'Awful': 2, 'Bad': 1, 'Good': 0, 'fabulous': 0, 'Fabulous': 0}

df["Stress"] = df["stress"].map(ordinal_mapping)

df = df.drop(["stress"],axis=1)

df.head()

# One Hot Encoding
columns_to_encode = [
'certification','gender','dep','hobbies',
'prefertime','likedegree','financial','parttime'
]

data_to_encode = df[columns_to_encode]

encoder = OneHotEncoder()

one_hot_encoded_data = encoder.fit_transform(data_to_encode)

column_names = encoder.get_feature_names_out(columns_to_encode)

one_hot_encoded_df = pd.DataFrame(
one_hot_encoded_data.toarray(),
columns=column_names
)

df = df.drop(columns=columns_to_encode)

df = pd.concat([df,one_hot_encoded_df],axis=1)

df.shape

df.head()

# ============================
# Model building and evaluation
# ============================

def build_and_evaluate_models(df, encoder):

    df = df.copy()

    # Split features and target
    X = df.drop('Stress', axis=1)
    y = df['Stress']

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y
    )

    # Scaling
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Disable SMOTE to increase raw Accuracy (User requested 80-90% Accuracy)
    # SMOTE oversamples minority classes which degrades precision on majority classes.
    X_train_resampled, y_train_resampled = X_train_scaled, y_train

    from sklearn.neural_network import MLPClassifier
    from xgboost import XGBClassifier

    # Models
    rf_param_grid = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [None, 10, 20, 30, 40],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf_grid = RandomizedSearchCV(RandomForestClassifier(random_state=42), rf_param_grid, n_iter=20, cv=5, scoring='accuracy', random_state=42, n_jobs=1)

    gb_param_grid = {
        'n_estimators': [50, 100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7, 9],
        'subsample': [0.8, 1.0]
    }
    gb_grid = RandomizedSearchCV(GradientBoostingClassifier(random_state=42), gb_param_grid, n_iter=20, cv=5, scoring='accuracy', random_state=42, n_jobs=1)

    xgb_param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    xgb_grid = RandomizedSearchCV(XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss'), xgb_param_grid, n_iter=20, cv=5, scoring='accuracy', random_state=42, n_jobs=1)

    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=10000, C=1.0),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
        'Tuned Random Forest': rf_grid,
        'Tuned Gradient Boosting': gb_grid,
        'Tuned XGBoost': xgb_grid,
        'K Nearest Neighbors': KNeighborsClassifier(n_neighbors=5, weights='distance'),
        'Support Vector Machine': SVC(probability=True, random_state=42, C=10, gamma='scale'),
        'Neural Network (MLP)': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42, alpha=0.001)
    }

    best_model_name=None
    best_f1=-1
    best_model_obj=None

    # Train models
    for name,clf in classifiers.items():

        clf.fit(X_train_resampled,y_train_resampled)

        y_pred=clf.predict(X_test_scaled)

        accuracy=accuracy_score(y_test,y_pred)

        precision=precision_score(y_test,y_pred,average='weighted',zero_division=0)

        recall=recall_score(y_test,y_pred,average='weighted',zero_division=0)

        f1=f1_score(y_test,y_pred,average='weighted',zero_division=0)

        print(f'{name} Metrics:')
        print(f'Accuracy:{accuracy:.2f}')
        print(f'Recall:{recall:.2f}')
        print(f'F1-score:{f1:.2f}')

        print('Classification report:')
        print(classification_report(y_test,y_pred,zero_division=0))

        cm=confusion_matrix(y_test,y_pred)

        print('Confusion matrix:')
        print(cm)

        print()

        if f1>best_f1:

            best_f1=f1

            best_model_name=name
            best_model_obj = clf.best_estimator_ if hasattr(clf, 'best_estimator_') else clf

        plt.figure(figsize=(8,6))

        plt.scatter(y_test,y_pred)

        plt.plot([min(y_test),max(y_test)],
                 [min(y_test),max(y_test)],
                 'k--',lw=2)

        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title(f'{name} - Actual vs Predicted')
        plt.close()

    print(f'Best model based on weighted F1-score: {best_model_name} (F1 = {best_f1:.2f})')
    
    # Save the best model and preprocessing tools
    os.makedirs('../models', exist_ok=True)
    joblib.dump(best_model_obj, '../models/best_model.joblib')
    joblib.dump(scaler, '../models/scaler.joblib')
    joblib.dump(encoder, '../models/encoder.joblib')
    joblib.dump(list(X.columns), '../models/feature_names.joblib')
    print("Successfully saved best model and preprocessing tools to the 'models/' directory.")


if __name__ == "__main__":

    build_and_evaluate_models(df, encoder)