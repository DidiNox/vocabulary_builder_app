# IMPORTS
import re


class TextCleaner:

    # The class does not need 'self'

    # Function to Validate Word Texts.
    @staticmethod
    def valid_word(word: str) -> bool:

        # Validation
        if not isinstance(word, str):
            raise TypeError(f"word must be a string.\n")
        
        if not word.strip():
            raise ValueError(f"word cannot be empty.\n")
        
        
        pattern_regex = r"^[a-zA-Z-]+$"


        return bool(
            re.fullmatch(
                pattern_regex, 
                word
            )
        )
    

    # Function to Remove Punctuations
    @staticmethod
    def remove_puncts(sentence: str) -> str:

        # Validation
        if not isinstance(sentence, str):
            raise TypeError(f"Sentence must be a string.\n")
        


        return re.sub(
            r"[^\w\s]", 
            "", 
            sentence
        )

    

    # Function to Clean Sentence
    @staticmethod
    def clean_sentence(sentence: str) -> str:

        # Validation
        if not isinstance(sentence, str):
            raise TypeError(f"Sentence must be a string.\n")
        
        sentence = TextCleaner.remove_puncts(sentence)

        # To remove extra spaces
        sentence = re.sub(
            r"\s+", 
            " ", 
            sentence
        )

        
        return sentence.strip()
