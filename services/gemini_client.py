from dotenv import load_dotenv
import os
import json
import time
import random
from google import genai

load_dotenv()


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("Gemini API key not found.")

        api_key = api_key.strip()

        self.client = genai.Client(api_key=api_key)

        print("KEY LENGTH:", len(api_key))
        print("API KEY LOADED:", bool(api_key))
        print("Gemini client initialized successfully.")

        # fallback models (primary first)
        self.models = [
            "gemini-2.5-flash-lite",
            "gemini-1.5-flash",
        ]

    def _clean_json(self, text: str) -> str:
        """Remove markdown fences and clean response"""
        return (
            text.replace("```json", "")
                .replace("```", "")
                .strip()
        )

    def _call_gemini(self, prompt: str):
        """Try models one by one with retry logic"""
        max_retries = 4

        for model in self.models:
            for attempt in range(max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if not response or not getattr(response, "text", None):
                        raise ValueError("Empty response from Gemini")

                    return response.text.strip()

                except Exception as e:
                    print(f"[{model}] attempt {attempt + 1} failed: {e}")

                    # last attempt for this model → move to next model
                    if attempt == max_retries - 1:
                        break

                    # exponential backoff + jitter
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)

        raise RuntimeError("All Gemini models failed after retries.")

    def generate_word(self, word: str) -> dict:
        if not isinstance(word, str):
            raise TypeError("Word must be a string.")

        if not word.strip():
            raise ValueError("Word cannot be empty.")

        prompt = f"""
For the English vocabulary word "{word}", generate:

1. A simple explanation.
2. An example sentence.
3. A memory trick.
4. A quiz question.

Return ONLY valid JSON:

{{
    "simple_explanation": "",
    "example_sentence": "",
    "memory_trick": "",
    "quiz_question": ""
}}
"""

        try:
            raw_text = self._call_gemini(prompt)

            print("\n========== GEMINI RAW RESPONSE ==========\n")
            print(raw_text)
            print("\n=========================================\n")

            cleaned = self._clean_json(raw_text)

            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")

            return {
                "simple_explanation": "Failed to parse AI response.",
                "example_sentence": "",
                "memory_trick": "",
                "quiz_question": ""
            }

        except Exception as e:
            print(f"Gemini Fatal Error: {e}")

            return {
                "simple_explanation": "AI service temporarily unavailable.",
                "example_sentence": "Try again in a few seconds.",
                "memory_trick": "",
                "quiz_question": ""
            }
        

        