import os
import google.generativeai as genai
from flask import Flask, request, jsonify

chat_app = Flask(__name__)

# Set the API key from the environment variable
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure the environment variable is set.")
genai.configure(api_key=api_key)

@chat_app.route('/chat', methods=['POST'])
def chat():
    # Log the incoming request for debugging
    print(f"Incoming request: {request.data}")
    
    data = request.get_json()

    # Check if data and message are present
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    message = data.get('message')

    try:
        # Use the Gemini model to generate content with configuration
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            message,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,        # One response candidate
                stop_sequences=["."],     # Stop after a period
                max_output_tokens=100,    # Limit to 100 tokens
                temperature=1.0,          # Control response randomness
            )
        )

        # Return the generated content in the response
        return jsonify({"response": response.candidates[0].content.parts[0].text}), 200

    except Exception as e:
        # General exception logging
        print(f"Error while processing the request: {e}")
        return jsonify({"error": "Error while processing the request", "details": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app, accessible on all interfaces at port 5001
    chat_app.run(debug=True, host='0.0.0.0', port=5001)

