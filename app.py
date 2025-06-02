from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow only your GitHub Pages domain to access this API
CORS(app, origins=["https://thejapachipala.github.io"])

# Simulated SharePoint-approved email list
approved_emails = [
    "user1@example.com",
    "user2@example.com",
    "thejapachipala@yourdomain.com",  # Example entry
    # Add more approved emails as needed
]

# Microsoft Form URL to redirect on approval
MS_FORM_URL = "https://forms.office.com/r/Saurgpg1XQ"

@app.route("/")
def home():
    return "QR Access Check Flask App Running"

@app.route("/check_access", methods=["POST"])
def check_access():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        if email in approved_emails:
            return jsonify({
                "access": "granted",
                "redirect_url": MS_FORM_URL
            })
        else:
            return jsonify({
                "access": "denied",
                "message": f"{email} is not in the approved list"
            }), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
