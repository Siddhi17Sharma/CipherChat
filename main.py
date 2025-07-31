# main.py

from cipherchat_app import CipherChatApp # Import the main application class
import os
from datetime import datetime # Required for timestamping in cipherchat_app

def main():
    """
    Main entry point for the CipherChat application.
    """
    app = CipherChatApp()
    print("\nWelcome to CipherChat! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting CipherChat. Goodbye!")
            break

        response = app.handle_user_message(user_input)
        print(response)

if __name__ == "__main__":
    main()