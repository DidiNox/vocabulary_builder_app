from dotenv import load_dotenv
from pathlib import Path
import os
import google.generativeai as genai
import json


load_dotenv()

class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        # Validation
        if not api_key:
            raise ValueError(f"Gemini API key not found.\n")
        
        
        genai.configure(api_key=api_key)


        # Choosing a model
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    
    # Function to Generate Word
    def generate_word(self, word: str) -> dict:
        
        # Validation
        if not isinstance(word, str):
            raise TypeError(f"Word must be a string.\n")
        
        if not word.strip():
            raise ValueError(f"Word cannot be empty.\n")
        

        prompt = f"""
        
        For the word '{word}', return ONLY JSON.
        
        Format:
        
        {{
            "simple_explanation": "",
            "example_sentence":"",
            "memory_trick":"",
            "quiz_question":""
        }}
        
        Do not include markdown.
        Do not include ```json.
        Do not explain anything.
        
        """

        try:
            response = self.model.generate_content(prompt)

            response_text = response.text.strip()

            # Converts the AI daata to JSON
            ai_data = json.loads(response_text)

            return ai_data
        
        except json.JSONDecodeError:
            print(f"Gemini returned an invalid JSON.\n")

            return {
                "simple_explanation": "", 

                "example_sentence": "", 

                "memory_trick": "", 

                "quiz_question": ""
            }
        
        except Exception as e:
            print(
                f"Gemini error: {e}.\n"
                f"Unable to generate AI content.\n"
            )
            
            return {
                "simple_explanation": f"\n", 

                "example_sentence": f"\n", 

                "memory_trick": f"\n", 
                
                "quiz_question": f"\n"
            }
        
    


