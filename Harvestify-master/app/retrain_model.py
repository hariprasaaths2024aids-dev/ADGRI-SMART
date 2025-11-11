import pickle
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Read the training data
data_path = os.path.join(os.path.dirname(__file__), '..', 'Data-processed', 'crop_recommendation.csv')
df = pd.read_csv(data_path)

# Prepare features and target
X = df.drop('label', axis=1)
y = df['label']

# Train a new model
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the new model
model_path = os.path.join(os.path.dirname(__file__), 'models', 'RandomForest.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model retrained and saved successfully to {model_path}")
print(f"   Accuracy on training data: {model.score(X, y):.2%}")
