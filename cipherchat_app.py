# cipherchat_app.py

from .encryption_handler import EncryptionHandler  # Note the '.'
from .steganography_handler import SteganographyHandler # Note the '.'
from .content_analyzer import ContentAnalyzer     # Note the '.'
import os
from datetime import datetime # Make sure this is present for timestamping
PROFANITY_LIST = [
    "badword1", "swearword", "curse", "profane", "damn", "hell", "fuck", "shit"
]

# --- Core Functions ---

def detect_profanity(text):
    """
    Detects if the given text contains any words from the PROFANITY_LIST.
    This is a basic, case-insensitive check.
    """
    text_lower = text.lower()
    for word in PROFANITY_LIST:
        if word in text_lower:
            return True
    return False

def get_masked_response():
    """
    Generates the standard masked response for hidden messages.
    """
    return "[Message Hidden: Inappropriate Content Detected]"

def handle_user_message(message):
    """
    Handles a user's incoming message, applies profanity check,
    and determines the next action (normal reply or masked response).
    """
    print(f"\nUser says: {message}")

    if detect_profanity(message):
        print("Profanity detected!")
        # In a later step, this is where encryption and steganography would happen.
        return get_masked_response()
    else:
        # Placeholder for normal chatbot response logic
        return f"Chatbot: You said '{message}'. (Normal reply)"

def main():
    """
    Main loop for the CipherChat application.
    """
    print("Welcome to CipherChat! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting CipherChat. Goodbye!")
            break

        response = handle_user_message(user_input)
        print(response)

if __name__ == "__main__":
    main()