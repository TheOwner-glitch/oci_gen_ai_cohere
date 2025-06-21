import oci
from dotenv import load_dotenv
import os

# Load environment variables from .env file explicitly
dotenv_path = './.env'  # Relative path to .env file
load_dotenv(dotenv_path=dotenv_path)

# OCI Setup
CONFIG_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
config_path = os.path.expanduser(os.getenv("OCI_CONFIG_PATH", "~/.oci/config"))  # Ensure this path is correct
config_path = os.path.expanduser(config_path)

compartment_id = os.getenv("OCI_COMPARTMENT_ID")
model_id = os.getenv("OCI_MODEL_ID")
private_key_path = os.getenv("OCI_PRIVATE_KEY_PATH")
fingerprint = os.getenv("OCI_FINGERPRINT")
tenant_id = os.getenv("OCI_TENANCY_ID")
region = os.getenv("OCI_REGION")

# Ensure all required environment variables are present
if None in [region, compartment_id, model_id, private_key_path]:
    raise ValueError("Error: One or more required environment variables are missing.")

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

def generate_response(input_message, max_tokens=600, temperature=1, frequency_penalty=0, top_p=0.75, top_k=0):
    """
    Function to generate a response from Oracle's Generative AI model.

    Parameters:
        input_message (str): The input message to be processed by the model.
        max_tokens (int): Maximum tokens for the response.
        temperature (float): Temperature setting for the model (affects randomness).
        frequency_penalty (float): Frequency penalty for the model's output.
        top_p (float): Top P (nucleus sampling).
        top_k (int): Top K tokens to consider for each response.

    Returns:
        str: The AI-generated response.
    """
    try:
        # Set up the request for the AI service
        chat_detail = oci.generative_ai_inference.models.ChatDetails()

        chat_request = oci.generative_ai_inference.models.CohereChatRequest()
        chat_request.message = input_message
        chat_request.max_tokens = max_tokens
        chat_request.temperature = temperature
        chat_request.frequency_penalty = frequency_penalty
        chat_request.top_p = top_p
        chat_request.top_k = top_k

        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id)
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = compartment_id

        # Call the AI service
        chat_response = generative_ai_inference_client.chat(chat_detail)

        # Extract the chat response using correct attribute access
        response_text = chat_response.data.chat_response.text

        # Return the response
        return response_text

    except Exception as e:
        return f"Error: {str(e)}"