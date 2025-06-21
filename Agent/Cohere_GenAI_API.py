from flask import Flask, request, jsonify
import oci
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file explicitly
dotenv_path = './.env'  # Relative path to .env file
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

# OCI Setup
CONFIG_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")

# Expanding user directory for config path
config_path = os.getenv("OCI_CONFIG_PATH", "~/.oci/config")  # Ensure this path is correct
config_path = os.path.expanduser(config_path)

# Debug: Print out the full path for the config file
print(f"OCI Config Path: {config_path}")

compartment_id = os.getenv("OCI_COMPARTMENT_ID")
model_id = os.getenv("OCI_MODEL_ID")
private_key_path = os.getenv("OCI_PRIVATE_KEY_PATH")
fingerprint = os.getenv("OCI_FINGERPRINT")
tenant_id = os.getenv("OCI_TENANCY_ID")
region = os.getenv("OCI_REGION")

# Ensure all required environment variables are present
if None in [region, compartment_id, model_id, private_key_path]:
    raise ValueError("Error: One or more required environment variables are missing.")

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Debug: Print out the configuration values
print(f"Loaded Config Data: {config_data}")

# Endpoint
endpoint = f"https://inference.generativeai.{region}.oci.oraclecloud.com"

# Load OCI config from environment variable
try:
    config = oci.config.from_file(config_path, CONFIG_PROFILE)
except Exception as e:
    print(f"Error loading OCI config: {str(e)}")
    exit(1)

# Create the Generative AI Inference Client
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint)

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Extract the message from the incoming request
        data = request.get_json()
        input_message = data.get('message')

        if not input_message:
            return jsonify({'error': 'No message provided'}), 400

        # Retrieve the temperature from the headers
        temperature = float(request.headers.get('Temperature', 1))  # Default to 1 if not provided

        # Set up the request for the AI service
        chat_detail = oci.generative_ai_inference.models.ChatDetails()

        chat_request = oci.generative_ai_inference.models.CohereChatRequest()
        chat_request.message = input_message
        chat_request.max_tokens = config_data.get('max_tokens', 600)
        chat_request.temperature = temperature
        chat_request.frequency_penalty = config_data.get('frequency_penalty', 0)
        chat_request.top_p = config_data.get('top_p', 0.75)
        chat_request.top_k = config_data.get('top_k', 0)

        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id)
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = compartment_id

        # Call the AI service
        chat_response = generative_ai_inference_client.chat(chat_detail)

        # Extract the chat response using correct attribute access
        response_text = chat_response.data.chat_response.text

        # Return the response in JSON format
        return jsonify({'response': response_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)