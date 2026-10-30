from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load ML assets right when the backend server launches
with open('models/churn_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # 1. Standardize UI text definitions into model-ready structural integers
        contract_mapping = {"Month-to-month": 0, "One year": 1, "Two year": 2}
        tech_mapping = {"Yes": 1, "No": 0}
        
        # 2. Extract and format incoming features
        input_data = pd.DataFrame([{
            'tenure': float(data['tenure']),
            'monthly_charges': float(data['monthly_charges']),
            'contract_type': contract_mapping[data['contract']],
            'tech_support': tech_mapping[data['tech_support']]
        }])
        
        # 3. Apply the exact same preprocessing scaler used during training
        input_scaled = scaler.transform(input_data)
        
        # 4. Extract explicit probability matrices
        prediction_proba = model.predict_proba(input_scaled)[0][1]
        
        return jsonify({
            'status': 'success',
            'churn_probability': float(round(prediction_proba, 3)),
            'risk_level': 'High' if prediction_proba > 0.6 else 'Medium' if prediction_proba > 0.3 else 'Low'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
