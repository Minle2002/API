from flask import Flask, jsonify, request
from predict import DiseaseDetector
from symptoms import gui_symptoms, model_symptoms
import pickle
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

model_path = "v2/decision_tree-v2.pkl"

def load_model(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

def parse_symptoms(symptoms):
    sym = []
    for s in model_symptoms:
        if s in symptoms:
            sym.append(1)
        else:
            sym.append(0)
    return sym

def load_disease_advice():
    try:
        with open('advice.json') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load disease advice data: {e}")
        return {}

model = load_model(model_path)

@app.route('/chatbot', methods=['POST'])
def detect_disease():
    data = request.json
    symptoms = data.get('symptoms', [])
    
    if len(symptoms) < 3:
        return jsonify({'error': 'Please enter at least 3 symptoms.'}), 400
    
    symps = parse_symptoms(symptoms)
    disease = model.predict([symps])[0]
    disease_info = load_disease_advice().get(disease, {})
    advice = disease_info.get('advice', 'Please consult a healthcare provider for more information.')
    medications = ', '.join(disease_info.get('medications', ['Consult a healthcare provider for medication options.']))
    full_message = f"The disease detected was {disease}. Advice: {advice} OTC Medications: {medications}"

    return jsonify({"message": full_message}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)