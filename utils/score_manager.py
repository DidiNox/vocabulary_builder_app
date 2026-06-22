# IMPORTS
from datetime import datetime
from pathlib import Path
import json



class ScoreManager:
    
    # CONSTANTS
    DATA_FOLDER = Path("data_folder")
    SCORES_FILE = DATA_FOLDER / "quiz_scores.json"

    def __init__(self):
        self.DATA_FOLDER.mkdir(exist_ok=True)

    
    # Function to Load Scores
    def load_scores(self) -> list[dict]:

        if not self.SCORES_FILE.exists():
            return []
        

        try:
            with open(self.SCORES_FILE, "r", encoding="utf-8") as file:
                scores = json.load(file)

                return scores
        
        except json.JSONDecodeError:
            print(f"The quiz scores JSON file is corrupted.\n")
            return []
        
        except OSError as e:
            print(f"File Error: {e}.\n")
            return []
        
        except Exception as e:
            print(f"Unexpected Error: {e}.\n")
            return []
        
    

    # Function to Save Quiz Scores
    def save_scores(self, score: int, total_quest: int) -> None:

        # Validation
        if not isinstance(score, int):
            raise TypeError(f"Score must be integer!\n")
        
        if not isinstance(total_quest, int):
            raise TypeError(f"Total questions must be integer.\n")
        
        if score > total_quest:
            raise ValueError(f"Scores cannot exceed total number of questions.\n")
        


        scores = self.load_scores()

        new_score = {
            "score": score, 
            "total_questions": total_quest, 
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        scores.append(new_score)


        try:
            with open(self.SCORES_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    scores, 
                    file, 
                    indent=4
                )
                
                print(f"Score saved successfully.\n")
        
        except OSError as e:
            print(f"Unable to save score: {e}.\n")
            
        
        except Exception as e:
            print(f"Unexpected error: {e}.\n")
            
        

