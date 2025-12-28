from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# Load models with error handling
try:
    severity_model = joblib.load("severity_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    department_model = joblib.load("department_model.pkl")
    dept_classes = joblib.load("dept_classes.pkl")
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")

@app.route("/", methods=["GET"])
def home():
    return "🔥 AI Emergency Service Running"

@app.route("/severity", methods=["POST"])
def severity_api():
    try:
        text = request.json.get("text", "")
        vec = vectorizer.transform([text])
        sev = severity_model.predict(vec)[0]
        return jsonify({"severity": sev})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/department", methods=["POST"])
def dept_api():
    try:
        text = request.json.get("text", "")
        vec = vectorizer.transform([text])
        pred = department_model.predict(vec)[0]
        depts = [dept_classes.classes_[i] for i,v in enumerate(pred) if v == 1]
        return jsonify({"departments": depts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
