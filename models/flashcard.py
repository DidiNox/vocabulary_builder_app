# Creating the 'Flashcard' class
class Flashcard:
    # Initialization
    def __init__(
            self, 
            word: str, 
            explanation: str = "", 
            example: str = "", 
            memory_trick: str = "", 
            quiz_question: str = ""
    ):
        
        # Validation
        if not isinstance(word, str):
            raise TypeError(f"'{word}' must be a string.\n")
        
        if not word.strip():
            raise ValueError(f"word cannot be empty.\n")
        

        self.word = word.strip()
        self.explanation = explanation.strip()
        self.example = example.strip()
        self.memory_trick = memory_trick.strip()
        self.quiz_question = quiz_question.strip()

    
    # Function to display flashcards to Users.
    def display_flashcards(self):
        print(f"\n********** FLASHCARD **********")
        print(
            f"---> Word: {self.word}\n"
            f"---> Explanation: {self.explanation}\n"
            f"---> Example: {self.example}\n" 
            f"---> Memory Trick: {self.memory_trick}\n" 
            f"---> Quiz Question: {self.quiz_question}\n"
        )
    

    # 'to_dict()' Function to Convert Object to Dictionary
    def to_dict(self) -> dict:
        return {
            "word": self.word, 
            "explanation": self.explanation, 
            "example": self.example, 
            "memory_trick": self.memory_trick, 
            "quiz_question": self.quiz_question
        }
    
    # 'from_dict()' Function to Convert Dictionary to Object
    @classmethod
    def from_dict(cls, data: dict) -> 'Flashcard':

        # Validation
        if not isinstance(data, dict):
            raise TypeError(f"data must be of dictionary data type.\n")


        return cls(
            word=data["word"], 
            explanation=data["explanation"], 
            example=data["example"], 
            memory_trick=data["memory_trick"], 
            quiz_question=data["quiz_question"]
        )



        
