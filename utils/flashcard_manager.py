# IMPORTS
from pathlib import Path
from models.flashcard import Flashcard
import json


# FlashcardManager Class
class FlashcardManager:

    DATA_FOLDER = Path("data_folder")
    FLASHCARD_FILE = DATA_FOLDER / "flashcards.json"


    def __init__(self):
        # Creates directory if it does not exists, else, it ignores and raises no error.
        self.DATA_FOLDER.mkdir(exist_ok=True)
    
    # Load Flashcards

    def load_flashcards(self) -> list[Flashcard]:
        '''
        returns: a list of the Object: Flashcard
        '''
        if not self.FLASHCARD_FILE.exists():
            return []
        
        try:
            with self.FLASHCARD_FILE.open("r", encoding="utf-8") as file:
                card_file = json.load(file)

            flashcards = []
            for item in card_file:
                flashcards.append(
                    Flashcard.from_dict(item)
                )
            
            return flashcards
        
        except json.JSONDecodeError:
            print(f"The Flashcard Json file is corrupted.\n")
            return []
        
        except OSError as e:
            print(f"File Error: {e}.\n")
            return []
        
        except Exception as e:
            print(f"Unexpected error: {e}.\n")
            return []
        
    

    def save_flashcards(self, new_card: Flashcard) -> None:

        # Validation
        if not isinstance(new_card, Flashcard):
            raise TypeError(f"New Flashcard must be a Flashcard Object.\n")


        flashcards = self.load_flashcards()

        for card in flashcards:
            if card.word.lower() == new_card.word.lower():
                print(f"New flashcard already exists.\n")
                return
        
        flashcards.append(new_card)

        
        # Converts Flashcard Object to List of Dictionaries/Dictionary
        flashcards_array = []
        for card in flashcards:
            flashcards_array.append(
                card.to_dict()
            )
        
        try:
            with open(self.FLASHCARD_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    flashcards_array, 
                    file, 
                    indent=4
                )
            
            print(f"Flashcard saved successfully!")
        
        except OSError as e:
            print(f"File Error: {e}.\n")
        
        except Exception as e:
            print(f"Unexpected error: {e}.\n")
        
        
