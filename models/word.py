# CREATING THE CLASS 'WORD'.
class Word:
    # Initialization
    def __init__(
            self, 
            word: str, 
            definition: str = "", 
            phonetics: str = "", 
            examples: list[str] | None = None, 
            synonyms: list[str] | None = None, 
            antonyms: list[str] | None = None
    ):
        
        # Validation
        if not isinstance(word, str):
            raise TypeError(f"'{word}' must be a string.\n")
        
        if not word.strip():
            raise ValueError(f"word cannot be empty.\n")
        

        self.word = word.strip()
        self.definition = definition
        self.phonetics = phonetics
        self.examples = examples or []
        self.synonyms = synonyms or []
        self.antonyms = antonyms or []

    
    # Function to display information of word searched to Users.
    def display_info(self):
        # Displays the Info about Word Searched
        print(
            f"\n********** WORD INFO **********\n"
            f"---> WORD: {self.word}\n"
            f"---> DEFINITION: {self.definition}\n"
            f"---> PHONETICS: {self.phonetics}"            
        )

        # Printing Examples
        print(f"---> EXAMPLES: ")
        if self.examples:
            for example in self.examples:
                print(f"----->>> {example}")
        
        else:
            print(f"None.\n")
        
        # Printing Synonyms
        print(f"---> SYNONYMS: ")
        if self.synonyms:
            for syns in self.synonyms:
                print(f"----->>> '{syns}'")
        
        else:
            print(f"None.\n")

        # Printing Antonyms
        print(f"---> ANTONYMS: ")
        if self.antonyms:
            for antys in self.antonyms:
                print(f"----->>> '{antys}'")
        
        else:
            print(f"None.\n")
    

    # Converts WordObjects to Dictionary; 'to_dict()' Function
    def to_dict(self) -> dict:
        return {
            "word": self.word, 
            "definition": self.definition, 
            "phonetics": self.phonetics, 
            "examples": self.examples, 
            "synonyms": self.synonyms, 
            "antonyms": self.antonyms
        }
    

    # Converts Dictionary to Object; 'from_dict()' Function
    @classmethod
    def from_dict(cls, data: dict) -> Word:

        return cls(
            word=data["word"], 
            definition=data["definition"], 
            phonetics=data["phonetics"], 
            examples=data["examples"], 
            synonyms=data["synonyms"], 
            antonyms=data["antonyms"]
        )



