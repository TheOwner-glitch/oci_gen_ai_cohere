# Cohere Generative AI Integration

This project demonstrates how to integrate with Oracle's Cohere Generative AI Service using a Flask API, Python functions, and configuration management via environment variables and JSON files.

## Project Structure

* **Cohere\_GenAI\_API.py**: A Flask API that processes requests and returns AI-generated responses.
* **Cohere\_GenAI\_Function.py**: Contains the core function for interacting with the Cohere Generative AI service, which can be imported into other Python apps.
* **Cohere\_GenAI\_Caller.py**: A script that calls `Cohere_GenAI_Function.py` from the command line and prints the response.
* **config.json**: Stores configurable values like `max_tokens`, `temperature`, etc., for controlling AI behavior.
* **.env**: Contains OCI credentials and paths, which should be set up locally (not included in the repository for security reasons).
* **env\_example.txt**: A template for creating your `.env` file with example values.

## Quick Start

1. **Set Up OCI Environment**: Set your OCI credentials in the `.env` file. (Refer to `env_example.txt` for a template).
2. **Install Dependencies**
3. **Run Flask API**:

   ```bash
   python Cohere_GenAI_API.py
   ```

   This will expose the API at `http://127.0.0.1:5000/generate`.
   
   OR
   
4. **Call Function Directly**: Use `Cohere_GenAI_Function.py` in your Python code or via the command line using `Cohere_GenAI_Caller.py`:

   ```bash
   python Cohere_GenAI_Caller.py "Are you there?"
   ```

## Full Instructions

For detailed setup and usage instructions, please refer to the Readme_Complete file under the Documentation folder.

For detailed steps on running a virtual python environment for development and testing purposes to host the Flask API, see Readme_Virtual_Environment under the documentation folder.