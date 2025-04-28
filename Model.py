import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
matrix_path = r"C:\Users\USER\Downloads\matrix.csv"  # Use raw string literals for paths
df = pd.read_csv(matrix_path)

# Drop non-feature columns
df = df.drop(columns=["Genome_Name"], errors='ignore')

# Handle missing values
df.fillna("Unknown", inplace=True)

# Encode all string columns (label encoding for simplicity)
for col in df.columns:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

# Separate features and target
X = df.drop(columns=["Final_Classification"])
y = df["Final_Classification"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:\n", classification_report(y_test, y_pred))
print("🧩 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Plot the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=np.unique(y), yticklabels=np.unique(y))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')

# Save the confusion matrix as a PNG
conf_matrix_path = r"C:\Users\USER\Downloads\april18\april18\confusion_matrix.png" # Use raw string literals
plt.savefig(conf_matrix_path)

# Close the plot
plt.close()

# Save the model
model_path = r"C:\Users\USER\Downloads\april18\april18\random_forest_model-MAIN.pkl"  # Use raw string literals
joblib.dump(model, model_path)
print(f"✅ Model saved to: {model_path}")
print(f"✅ Confusion Matrix saved to: {conf_matrix_path}")
