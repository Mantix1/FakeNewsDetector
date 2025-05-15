from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

# For extension
app = Flask(__name__)
CORS(app)  


# Load vectorizer and model
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/fake_news_model.pkl")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')

    if not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    # Vectorize text
    vec = vectorizer.transform([text])
    
    # Predict class
    pred = model.predict(vec)[0]

    # Get probability
    proba = model.predict_proba(vec)[0]
    confidence = round(max(proba) * 100, 2)

    # Build response
    result = {
        'prediction': 'REAL' if pred == 1 else 'FAKE',
        'confidence': confidence
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)
