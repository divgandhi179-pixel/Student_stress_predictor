# ============================================================
# 📊 EXPLORATORY DATA ANALYSIS (EDA)
# PROJECT: AI-Based Student Stress Level Predictor
# ============================================================

# ==============================
# 1️⃣ Import Required Libraries
# ==============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")
sns.set_theme(style="whitegrid")

# ==============================
# 2️⃣ Load Dataset
# ==============================
df = pd.read_csv("Student Attitude and Behavior.csv")

# Rename columns for easier use
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
    "willingness to pursue a career based on their degree  ":"carrer_willing",
    "social medai & video":"smtime",
    "Travelling Time ":"travel",
    "Stress Level ":"stress",
    "Financial Status":"financial",
    "part-time job":"parttime"
}, inplace=True)

# ==============================
# 3️⃣ Basic Dataset Overview
# ==============================
print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:\n", df.isnull().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

# ============================================================
# 4️⃣ Certification & Gender Analysis
# ============================================================

df["certification"].value_counts().plot(kind="bar", title="Certification Course Distribution")
plt.show()

df["gender"].value_counts().plot(kind="bar", title="Gender Distribution")
plt.show()

df.groupby("gender")["certification"].value_counts().plot(kind="bar", title="Certification Course Distribution by Gender")
plt.show()

# ============================================================
# 5️⃣ Department Analysis
# ============================================================

df["dep"].value_counts().plot(kind="bar", title="Department Distribution")
plt.show()

df.groupby('dep')["gender"].value_counts().sort_values(ascending=False).plot(
    kind="bar", title="Department vs Gender Distribution"
)
plt.show()

# ============================================================
# 6️⃣ Height vs Weight Relationship
# ============================================================

plt.figure(figsize=(10,6))
sns.regplot(x=df["height"], y=df["weight"])
plt.title("Height vs Weight Relationship")
plt.show()

df.groupby("gender")["weight"].mean().plot(kind="bar", title="Average Weight by Gender")
plt.show()

# ============================================================
# 7️⃣ Academic Performance Analysis
# ============================================================

# 10th marks
print(df["mark10th"].describe())
df["mark10th"].plot(kind="box", title="10th Mark Distribution")
plt.show()

# 12th marks
print(df["mark12th"].describe())
df["mark12th"].plot(kind="kde", title="12th Mark Distribution")
plt.show()

# College marks
print(df["collegemark"].describe())
df["collegemark"].plot(kind="kde", title="College Mark Distribution")
plt.show()

# ============================================================
# 8️⃣ Hobbies Analysis
# ============================================================

df["hobbies"].value_counts().plot(
    kind="pie", autopct='%1.1f%%', ylabel="", title="Hobbies Distribution"
)
plt.show()

hobbies_percentage = df.groupby('gender')["hobbies"].value_counts()
hobbies_percentage.plot(
    kind="pie", autopct='%1.1f%%', ylabel="", title="Hobbies Distribution by Gender"
)
plt.show()

# ============================================================
# 9️⃣ Study Time Analysis
# ============================================================

print(df["studytime"].describe())

df["studytime"].plot(kind="box", title="Study Time Distribution")
plt.show()

df.groupby('dep')["studytime"].mean().plot(
    kind="bar", title="Average Study Time by Department"
)
plt.show()

# ============================================================
# 🔟 Preferred Study Time
# ============================================================

df.groupby('dep')["prefertime"].value_counts().plot(
    kind="bar", title="Preferred Time to Study by Department"
)
plt.show()

# ============================================================
# 1️⃣1️⃣ Salary Expectation
# ============================================================

print(df["salexpect"].describe())

df.groupby('salexpect')["salexpect"].mean().plot(
    kind="bar", title="Salary Expectation Distribution"
)
plt.show()

# ============================================================
# 1️⃣2️⃣ Social Media Usage
# ============================================================

df.groupby('dep')["smtime"].mean().sort_values(ascending=False).plot(
    kind="bar", title="Average Social Media Time by Department"
)
plt.show()

# ============================================================
# 1️⃣3️⃣ Travel Time Analysis
# ============================================================

print(df["travel"].describe())

df["travel"].plot(kind="kde", title="Travel Time Distribution")
plt.show()

# ============================================================
# 1️⃣4️⃣ Stress Level Analysis
# ============================================================

df["stress"].value_counts().plot(kind="bar", title="Stress Level Distribution")
plt.show()

# Stress vs gender
df.groupby("stress")["gender"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", ylabel="", title="Stress vs Gender"
)
plt.show()

# Stress vs department
stress_dep = df.groupby("dep")["stress"].value_counts().reset_index(name="count")

sns.barplot(data=stress_dep, x="dep", y="count", hue="stress")
plt.title("Stress Level Distribution by Department")
plt.xticks(rotation=45)
plt.show()

# ============================================================
# 1️⃣5️⃣ Financial Status vs Stress
# ============================================================

df.groupby("financial")["stress"].value_counts().plot(
    kind="bar", title="Financial Status vs Stress"
)
plt.show()

# ============================================================
# 1️⃣6️⃣ Part-time Job vs Stress
# ============================================================

df.groupby("parttime")["stress"].value_counts().plot(
    kind="bar", title="Part-time Job vs Stress"
)
plt.show()

print("\nEDA Completed Successfully ✅")