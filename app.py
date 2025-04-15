import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file (for local development)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API key from environment
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure the environment variable is set.")

# Configure the Gemini API
genai.configure(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    print(f"Incoming request: {request.data}")
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    message = data.get('message')

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            message,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=["."],
                max_output_tokens=100,
                temperature=1.0,
            )
        )

        return jsonify({"response": response.candidates[0].content.parts[0].text}), 200

    except Exception as e:
        print(f"Error while processing the request: {e}")
        return jsonify({"error": "Error while processing the request", "details": str(e)}), 500
