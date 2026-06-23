# IMPORTS
import requests
from models.word import Word



# Creating the class DictionayClient
class DictionaryClient:

    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def __init__(self):
        pass


    # Get Word Function
    def get_data_word(self, word: str) -> Word:

        # Validation
        if not isinstance(word, str):
            raise TypeError(f"'{word}' must be a string.\n")
        
        if not word.strip():
            raise ValueError(f"word cannot be empty.\n")
        

        url = self.BASE_URL + word.strip()

        # Exception Handling to avoid error when internet is unavailable
        try:
            response = requests.get(url, timeout=10)

            # Checks if HTTP request is successful and raise an exception if error occurs.
            response.raise_for_status()

            data = response.json()

            if not data:
                raise ValueError(f"Word: '{word}' not found.\n")

            entry = data[0]

            word_text = entry['word']
            phonetics = entry.get("phonetics", "")
            meanings = entry.get("meanings", "")

            definition = ""
            example = ""
            synonyms = []
            antonyms = []

            if meanings:
                meaning = meanings[0]

                definitions = meaning.get("definitions", [])
            
                if definitions:
                    definition = definitions[0].get("definition", "")

                    example = definitions[0].get("example", "")
                
                synonyms = meaning.get("synonyms", [])

                antonyms = meaning.get("antonyms", [])
            

                        
            return Word(
                word=word_text, 
                definition=definition, 
                phonetics=phonetics, 
                synonyms=synonyms, 
                antonyms=antonyms,                  
                examples=[example] if example else []
            )        
        
        except requests.ConnectionError:
            raise ConnectionError(f"Unable to connect to dictionary's API.\n")
        
        except requests.Timeout:
            raise TimeoutError(f"Request timed out.\n")
        
        except requests.HTTPError:
            raise ValueError(f"Word: '{word}' not found.\n")
        

        except requests.RequestException as e:
            raise Exception(f"Request error: {e}.\n")
        


            
        

        
    

