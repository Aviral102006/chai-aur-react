from flask import Flask, request, jsonify
import joblib
from ast import literal_eval

severity_model = joblib.load("severity_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
department_model = joblib.load("department_model.pkl")
dept_classes = joblib.load("dept_classes.pkl")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🔥 AI Emergency Service Running"

@app.route("/severity", methods=["POST"])
def severity_api():
    text = request.json.get("text", "")
    vec = vectorizer.transform([text])
    sev = severity_model.predict(vec)[0]
    return jsonify({"severity": sev})

@app.route("/department", methods=["POST"])
def dept_api():
    text = request.json.get("text", "")
    vec = vectorizer.transform([text])
    pred = department_model.predict(vec)[0]
    depts = [dept_classes.classes_[i] for i,v in enumerate(pred) if v == 1]
    return jsonify({"departments": depts})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
