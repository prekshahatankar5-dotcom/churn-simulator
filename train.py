import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

print("⏳ Generating synthetic Telco Churn dataset...")
np.random.seed(42)
n_samples = 5000

# Generate realistic feature spaces
tenure = np.random.randint(1, 72, n_samples)
monthly_charges = np.random.uniform(18, 120, n_samples)
contract_type = np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.25, 0.25]) 
tech_support = np.random.choice([0, 1], n_samples, p=[0.7, 0.3]) 

# Algorithmic log odds relationship to simulate realistic churn rules
log_odds = (0.05 * monthly_charges) - (0.06 * tenure) - (1.5 * contract_type) - (0.8 * tech_support) - 0.5
probability = 1 / (1 + np.exp(-log_odds))
churn = np.random.binomial(1, probability)

# Structure into Dataframe
df = pd.DataFrame({
    'tenure': tenure,
    'monthly_charges': monthly_charges,
    'contract_type': contract_type,
    'tech_support': tech_support,
    'churn': churn
})

# Split data features
X = df.drop('churn', axis=1)
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numeric values to prevent gradient skewing
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train Classifier Model
print("🤖 Training Machine Learning model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save artifacts to folder assets
with open('models/churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Model assets successfully trained and exported into /models/ directory!")
s