import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df = pd.read_csv("Student Attitude and Behavior.csv")

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

# Convert stress labels to numeric
ordinal_mapping = {'Awful':0,'Bad':1,'Good':2,'fabulous':3,'Fabulous':3}

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

    # SMOTE
    class_counts = y_train.value_counts()

    min_class_count = class_counts.min()

    if min_class_count > 1:

        k_neighbors = min(5,min_class_count-1)

        smote = SMOTE(random_state=42,k_neighbors=k_neighbors)

        X_train_resampled,y_train_resampled = smote.fit_resample(
        X_train_scaled,y_train
        )

    else:

        print("Not enough samples for SMOTE")

        X_train_resampled,y_train_resampled = X_train_scaled,y_train

    # Models
    classifiers = {

    'Logistic Regression':LogisticRegression(max_iter=10000),
    'Decision Tree':DecisionTreeClassifier(),
    'Random Forest':RandomForestClassifier(),
    'K Nearest Neighbors':KNeighborsClassifier(),
    'Support Vector Machine':SVC()

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
            best_model_obj=clf

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
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model_obj, 'models/best_model.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    joblib.dump(encoder, 'models/encoder.joblib')
    joblib.dump(list(X.columns), 'models/feature_names.joblib')
    print("Successfully saved best model and preprocessing tools to the 'models/' directory.")


if __name__ == "__main__":

    build_and_evaluate_models(df, encoder)