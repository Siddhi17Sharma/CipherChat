# encryption_handler.py

from cryptography.fernet import Fernet
import base64

class EncryptionHandler:
    def __init__(self, key=None):
        """
        Initializes the EncryptionHandler.
        If no key is provided, a new one is generated.
        IMPORTANT: In a real application, the key should be securely loaded and persisted.
        Generating a new key on every run is for demonstration purposes only.
        """
        if key is None:
            self._key = Fernet.generate_key()
            print(f"DEBUG: New encryption key generated: {self._key.decode()}")
        else:
            self._key = key
            print(f"DEBUG: Encryption handler initialized with provided key.")

        self._fernet = Fernet(self._key)

    def get_key(self):
        """Returns the current encryption key."""
        return self._key.decode() # Return as string for display/storage

    def encrypt_message(self, message: str) -> bytes:
        """
        Encrypts a string message using the initialized Fernet key.
        Returns bytes.
        """
        return self._fernet.encrypt(message.encode('utf-8'))

    def decrypt_message(self, encrypted_message: bytes) -> str:
        """
        Decrypts a bytes message using the initialized Fernet key.
        Returns the original string.
        """
        return self._fernet.decrypt(encrypted_message).decode('utf-8')

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    print("--- Testing EncryptionHandler ---")
    # Scenario 1: Generate a new key
    handler1 = EncryptionHandler()
    original_msg1 = "This is a secret message."
    encrypted_msg1 = handler1.encrypt_message(original_msg1)
    print(f"Original: '{original_msg1}'")
    print(f"Encrypted: {encrypted_msg1}")
    decrypted_msg1 = handler1.decrypt_message(encrypted_msg1)
    print(f"Decrypted: '{decrypted_msg1}'")
    assert original_msg1 == decrypted_msg1
    print("Test 1 Passed: New key generation and encryption/decryption works.\n")

    # Scenario 2: Use a pre-existing key (decode from string to bytes)
    # In a real app, you'd load this from a secure file/env variable.
    pre_existing_key_str = handler1.get_key() # Get the key generated above
    pre_existing_key_bytes = pre_existing_key_str.encode('utf-8')

    handler2 = EncryptionHandler(key=pre_existing_key_bytes)
    original_msg2 = "Another confidential piece of text."
    encrypted_msg2 = handler2.encrypt_message(original_msg2)
    print(f"Original: '{original_msg2}'")
    print(f"Encrypted: {encrypted_msg2}")
    decrypted_msg2 = handler2.decrypt_message(encrypted_msg2)
    print(f"Decrypted: '{decrypted_msg2}'")
    assert original_msg2 == decrypted_msg2
    print("Test 2 Passed: Using pre-existing key works.\n")