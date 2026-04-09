from flask import Flask, request, jsonify
import joblib  # For loading your scikit-learn model

app = Flask(__name__)

# Load your trained model
model = joblib.load('path_to_your_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)