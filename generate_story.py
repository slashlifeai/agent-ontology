import google.generativeai as genai
import os
import sys

# System prompt to set the context for the model
SYSTEM_PROMPT = """You are an expert in agile development and user story creation.
Your task is to take user requests and transform them into well-formatted user stories.
The standard format is: "As a [persona], I want [action], so that [benefit]."
If the user's request is ambiguous, ask clarifying questions to get the necessary details.
If the user just wants to chat, respond conversationally.
"""

def main():
    """
    Main function to run the interactive user story generator.
    """
    try:
        # Get API key from environment variable
        api_key = os.environ["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    except KeyError:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set the variable and try again.")
        sys.exit(1)

    # Initialize the model
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[
        {'role': 'user', 'parts': [SYSTEM_PROMPT]},
        {'role': 'model', 'parts': ["Understood. I am ready to help you craft excellent user stories. What feature or idea are we working on today?"]}
    ])

    print("--- User Story Generator ---")
    print("Enter your idea, and I'll help you turn it into a user story.")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            response = chat.send_message(user_input)
            print(f"\nGemini: {response.text}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
