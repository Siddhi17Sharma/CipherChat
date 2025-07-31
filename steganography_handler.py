# steganography_handler.py

from PIL import Image
import os

class SteganographyHandler:
    def __init__(self):
        pass

    def _text_to_binary(self, text):
        """Converts a string into a binary string."""
        return ''.join([format(ord(i), "08b") for i in text])

    def _binary_to_text(self, binary_string):
        """Converts a binary string back to a text string."""
        # Ensure the binary string length is a multiple of 8
        if len(binary_string) % 8 != 0:
            raise ValueError("Binary string length must be a multiple of 8 for conversion to text.")

        chars = []
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            chars.append(chr(int(byte, 2)))
        return ''.join(chars)

    def encode_text_in_image(self, image_path: str, secret_message: str, output_path: str = "output_stego_image.png"):
        """
        Encodes a secret message into an image using LSB steganography.
        The message is terminated by a special sequence ('#####').
        """
        try:
            img = Image.open(image_path).convert("RGB") # Ensure RGB mode
        except FileNotFoundError:
            print(f"ERROR: Image not found at {image_path}")
            return False
        except Exception as e:
            print(f"ERROR: Could not open image: {e}")
            return False

        # Add a termination sequence to the message
        message_with_terminator = secret_message + '#####'
        binary_message = self._text_to_binary(message_with_terminator)
        message_length = len(binary_message)

        if message_length > img.width * img.height * 3: # 3 color channels (R,G,B) per pixel
            print("ERROR: Message is too long to hide in this image.")
            return False

        data_index = 0
        pixels = img.getdata() # Get pixel data as a sequence of (R,G,B) tuples
        new_pixels = []

        for pixel in pixels:
            r, g, b = list(pixel) # Convert tuple to list to modify
            if data_index < message_length:
                # Modify the least significant bit of R channel
                r = (r & 0xFE) | int(binary_message[data_index])
                data_index += 1
            if data_index < message_length:
                # Modify the least significant bit of G channel
                g = (g & 0xFE) | int(binary_message[data_index])
                data_index += 1
            if data_index < message_length:
                # Modify the least significant bit of B channel
                b = (b & 0xFE) | int(binary_message[data_index])
                data_index += 1

            new_pixels.append(tuple([r, g, b]))

        img.putdata(new_pixels)
        try:
            img.save(output_path)
            print(f"Steganographic image saved to {output_path}")
            return True
        except Exception as e:
            print(f"ERROR: Could not save image: {e}")
            return False

    def decode_text_from_image(self, image_path: str) -> str | None:
        """
        Decodes a secret message from an image using LSB steganography.
        Looks for the termination sequence ('#####').
        """
        try:
            img = Image.open(image_path).convert("RGB")
        except FileNotFoundError:
            print(f"ERROR: Image not found at {image_path}")
            return None
        except Exception as e:
            print(f"ERROR: Could not open image: {e}")
            return None

        binary_message = []
        pixels = img.getdata()

        for pixel in pixels:
            r, g, b = pixel
            # Extract the least significant bit from each color channel
            binary_message.append(str(r & 1))
            binary_message.append(str(g & 1))
            binary_message.append(str(b & 1))

        full_binary_string = "".join(binary_message)

        # Look for the termination sequence in binary form
        terminator_binary = self._text_to_binary('#####')
        try:
            # Find the index where the terminator starts
            end_index = full_binary_string.find(terminator_binary)
            if end_index == -1:
                print("WARNING: Termination sequence not found in the image. Message might be incomplete or not present.")
                # Attempt to decode what's there anyway, up to a reasonable limit
                # Or just return None if strict termination is required
                return None # Or self._binary_to_text(full_binary_string) for partial data

            # Extract the message part before the terminator
            message_binary_part = full_binary_string[:end_index]
            decoded_message = self._binary_to_text(message_binary_part)
            return decoded_message
        except ValueError as e:
            print(f"ERROR during decoding: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during decoding: {e}")
            return None


# Example Usage (for testing this module independently)
if __name__ == "__main__":
    print("--- Testing SteganographyHandler ---")
    stego_handler = SteganographyHandler()
    input_image_path = "sample_image.png" # Make sure this image exists in your project root!
    output_image_path = "hidden_message_image.png"
    secret_text = "This is my super secret hidden message for CipherChat!"
    long_secret_text = "a" * 100000 # Test for too long message

    # Test encoding
    print(f"Attempting to encode '{secret_text}' into {input_image_path}")
    success = stego_handler.encode_text_in_image(input_image_path, secret_text, output_image_path)
    if success:
        print(f"Encoding successful! Check '{output_image_path}'")
        # Test decoding
        print(f"Attempting to decode from '{output_image_path}'")
        decoded_text = stego_handler.decode_text_from_image(output_image_path)
        if decoded_text:
            print(f"Decoded: '{decoded_text}'")
            assert secret_text == decoded_text
            print("Steganography Test Passed: Encoding and decoding match.")
        else:
            print("Steganography Test Failed: Decoding returned None.")
    else:
        print("Steganography Test Failed: Encoding was not successful.")

    # Test with a message that's too long
    print(f"\nAttempting to encode a very long message into {input_image_path}")
    stego_handler.encode_text_in_image(input_image_path, long_secret_text, "too_long_image.png")

    # Clean up generated image if desired
    # if os.path.exists(output_image_path):
    #     os.remove(output_image_path)