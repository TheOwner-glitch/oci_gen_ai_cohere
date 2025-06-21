import sys
from Cohere_GenAI_Function import generate_response

def main():
    if len(sys.argv) < 2:
        print("Usage: python call_cohere_genai.py <message>")
        sys.exit(1)

    # Get the input message from the command-line argument
    input_message = sys.argv[1]

    # Call the function to generate the response
    response = generate_response(input_message)

    # Print the AI-generated response
    print("AI Response:", response)

if __name__ == "__main__":
    main()