# content_analyzer.py

class ContentAnalyzer:
    def __init__(self):
        # A very basic list of profanity words.
        # In a real application, this would be much more comprehensive,
        # potentially loaded from a file, a database, or replaced by ML models.
        self.profanity_list = [
            "badword1", "swearword", "curse", "profane", "damn", "hell", "fuck", "shit",
            "asshole", "bitch", "cunt", "douche", "motherfucker", "bastard"
        ]
        # Placeholder for more advanced models if we integrate them later
        self.loaded_ml_models = False
        # self._load_ml_models() # Uncomment this if you implement ML models

    def _load_ml_models(self):
        """
        Placeholder for loading offline ML models for toxicity, sentiment, etc.
        This would involve libraries like transformers (Hugging Face) or SpaCy.
        """
        print("INFO: Attempting to load offline ML models for content analysis...")
        # Example:
        # try:
        #     from transformers import pipeline
        #     self.sentiment_pipeline = pipeline("sentiment-analysis", model="local_sentiment_model_path")
        #     self.toxicity_pipeline = pipeline("text-classification", model="local_toxicity_model_path")
        #     self.loaded_ml_models = True
        #     print("INFO: Offline ML models loaded successfully.")
        # except ImportError:
        #     print("WARNING: Transformers or other ML libraries not installed. Advanced analysis disabled.")
        # except Exception as e:
        #     print(f"ERROR: Could not load ML models: {e}. Advanced analysis disabled.")

    def detect_profanity(self, text: str) -> bool:
        """
        Detects if the given text contains any words from the profanity list.
        This is a basic, case-insensitive check.
        """
        text_lower = text.lower()
        for word in self.profanity_list:
            if word in text_lower:
                return True
        return False

    def analyze_toxicity(self, text: str) -> dict:
        """
        Placeholder for more advanced toxicity analysis using ML models.
        Returns a dictionary with toxicity scores/flags.
        """
        # if self.loaded_ml_models and hasattr(self, 'toxicity_pipeline'):
        #     result = self.toxicity_pipeline(text)
        #     return {"is_toxic": result[0]['label'] == 'toxic' and result[0]['score'] > 0.7, "details": result}
        # else:
        print("INFO: Advanced toxicity analysis is not active (ML models not loaded/implemented).")
        return {"is_toxic": self.detect_profanity(text)} # Fallback to profanity for now

    def analyze_sentiment(self, text: str) -> dict:
        """
        Placeholder for sentiment analysis using ML models.
        Returns a dictionary with sentiment score/label.
        """
        # if self.loaded_ml_models and hasattr(self, 'sentiment_pipeline'):
        #     result = self.sentiment_pipeline(text)
        #     return {"sentiment": result[0]['label'], "score": result[0]['score'], "details": result}
        # else:
        print("INFO: Sentiment analysis is not active (ML models not loaded/implemented).")
        return {"sentiment": "neutral", "score": 0.5} # Default placeholder

    def full_content_check(self, text: str) -> bool:
        """
        Performs a comprehensive check for inappropriate content.
        Returns True if any inappropriate content is detected.
        """
        if self.detect_profanity(text):
            print("DEBUG: Profanity detected by basic check.")
            return True
        # You can add more checks here as you implement them
        # if self.analyze_toxicity(text)["is_toxic"]:
        #     print("DEBUG: Toxicity detected by advanced analysis.")
        #     return True
        return False

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    print("--- Testing ContentAnalyzer ---")
    analyzer = ContentAnalyzer()

    print("\nTest 1: Profane message")
    msg1 = "That's a damn good idea, but also a piece of shit."
    print(f"Message: '{msg1}' -> Inappropriate: {analyzer.full_content_check(msg1)}")
    assert analyzer.full_content_check(msg1) == True

    print("\nTest 2: Clean message")
    msg2 = "Hello, how are you doing today?"
    print(f"Message: '{msg2}' -> Inappropriate: {analyzer.full_content_check(msg2)}")
    assert analyzer.full_content_check(msg2) == False

    print("\nTest 3: Message with slight profanity")
    msg3 = "You are a total asshole sometimes."
    print(f"Message: '{msg3}' -> Inappropriate: {analyzer.full_content_check(msg3)}")
    assert analyzer.full_content_check(msg3) == True