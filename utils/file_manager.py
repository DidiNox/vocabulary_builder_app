# FILE MANAGER FOR VOCAB_APP
# IMPORTS
from pathlib import Path
import json
from models.word import Word

# Creating the FileManager class
class FileManager:

    # Constants Variables
    DATA_FOLDER = Path("data_folder")
    WORDS_FILE = DATA_FOLDER / "saved_words_file.json"

    def __init__(self):
        self.DATA_FOLDER.mkdir(exist_ok=True)
    

    # Function to Load/Read
    def load_words(self) -> list[Word]:

        if not self.WORDS_FILE.exists():
            return []
        
        try:
            # Open JSON File
            with open(self.WORDS_FILE, "r", encoding="utf-8") as file:
                file_doc = json.load(file)
            

            # words = []
            
            # for item in file_doc:
            #     words.append(
            #         Word.from_dict(item)
            #     )

            # List Comprehension
            # Iterates through file_doc and appends it to the empty list created.
            words = [
                Word.from_dict(item)
                for item in file_doc
            ]            
            
            return words
        

        except json.JSONDecodeError:
            print(f"The Json file is corrupted.\n")
            return []
        
        except OSError as e:
            print(f"File error: {e}\n")
            return []
        
        except Exception as e:
            print(f"Unexpected error: {e}\n")
            return []
    

    # Function to save words that was searched: save_words()
    def save_words(self, new_word: Word) -> None:

        # Validation
        if not isinstance(new_word, Word):
            raise TypeError(f"'New word' must be a Word object.\n")


        words = self.load_words()

        for word in words:
            if word.word.lower() == new_word.word.lower():
                print(f"New word already exists.\n")
                return
            
        words.append(new_word)

        # Converts Word Object to Dictionary/List of Dictionaries
        words_array = []
        for word in words:
            words_array.append(
                word.to_dict()
            )
        
        try:
            with open(self.WORDS_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    words_array, 
                    file, 
                    indent=4
                )

                print(f"New word: {new_word} saved successfully.\n")
        
        except OSError as e:
            print(f"Could not save the word: {e}.\n")
            return []
        
        except Exception as e:
            print(f"Unexpected error: {e}. \n")
            return []



