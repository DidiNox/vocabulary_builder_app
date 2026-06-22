# IMPORTS

# Services Imports
from services.dictionary_client import DictionaryClient
from services.gemini_client import GeminiClient
from services.quiz_generator import QuizGenerator
from services.spaced_repitiion_manager import SpacedRepetitionManager

# Utilities Imports
from utils.flashcard_manager import FlashcardManager
from utils.score_manager import ScoreManager
from utils.text_cleaner import TextCleaner

# Models Imports
from models.flashcard import Flashcard



class VocabularyApp:

    def __init__(self):

        self.dictionary_client = DictionaryClient()
        self.gemini_client = GeminiClient()
        self.quiz_generator = QuizGenerator()
        self.flashcard_manager = FlashcardManager()
        self.score_manager = ScoreManager()
        self.spaced_repitition = SpacedRepetitionManager()

   
    
    def search_word(self, word: str) -> None:
            
        # Validation
        if not isinstance(word, str):
            raise TypeError(f"Word: '{word}' must be a string.\n")
            
        if not word.strip():
            raise ValueError(f"Word cannot be empty.\n")
            
        if not TextCleaner.valid_word(word):
            print(f"Invalid word inserted!\n")
            return
            

        # Dictionary Search
        try:

            word_object = (
                self.dictionary_client.get_data_word(word)
            )

            # Displays Word Info.
            word_object.display_info()

                
            # GENERATE AI DATA
            ai_data = (
                self.gemini_client.generate_word(word)
            )

            print()
                
            for key, value in ai_data.items():
                print(
                    f"{key.replace('_', ' ').title()}:\n"
                    f"{value}\n"
                )

                
            # Create Flashcards
            flashcard = Flashcard(
                word = word, 
                explanation = ai_data["simple_explanation"], 
                memory_trick = ai_data["memory_trick"], 
                quiz_question = ai_data["quiz_question"]
            )


            # Saves Flashcards
            self.flashcard_manager.save_flashcards(flashcard)


        except Exception as e:
            print(f"Error: {e}.\n")

    

    # Function to Review Flashcards
    def review_flashcards(self) -> None:
        
        try:
            flashcards = self.flashcard_manager.load_flashcards()

            if not flashcards:
                print(f"No flashcard available.\n")
                return
            
            print()

            print(f"********** SAVED FLASHCARDS **********\n")
            for card in flashcards:
                card.display_flashcards()
        
        except Exception as e:
            print(f"Unexpected error: {e}.\n")
    

    # Function to Start Quiz
    def start_quiz(self) -> None:

        try:
            flashcards = self.flashcard_manager.load_flashcards()

            if not flashcards:
                print(f"No flashcard available.\n")
                return
            
            try:
                no_of_quests = int(input("How many questions would you like?: "))

            except ValueError:
                print(f"Please give a valid number!.\n")
                return
            
            score = self.quiz_generator.start_quiz(flashcards, no_of_quests)

            self.score_manager.save_scores(score, self.quiz_generator.total_questions)

            print(f"Quiz score saved successfully!\n")

        
        except Exception as e:
            print(f"An unexpected error occured: {e}.\n")
    

    # Function to Display User's Scores
    def display_scores(self) -> None:

        try:
            scores = self.score_manager.load_scores()

            if not scores:
                print(f"No quiz score found.\n")
                return
            
            print(f"\n********** QUIZ SCORES **********")
            for score in scores:
                print(
                    f"Score: {score["score"]}.\n"
                    f"Total Questions: {score["total_questions"]}.\n"
                    f"Date: {score["date"]}.\n"
                    f"\n"
                )
        except Exception as e:
            print(f"Unexpected error: {e}.\n")
    


    # Function to Display Menu
    def menu(self) -> None:

        run = True
        while run:
            print(f"\n************ VOCABULARY BUILDER ************")
            print(
                f"1. Search Word\n"
                f"2. Review Flashcards\n"
                f"3. Take Quiz\n"
                f"4. View Scores\n"
                f"5. Exit\n"
            )

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                word = input("Enter word to search: ").strip()

                self.search_word(word)
            
            elif choice == "2":

                self.review_flashcards()
            
            elif choice == "3":

                self.start_quiz()
            
            elif choice == "4":

                self.display_scores()
            
            elif choice == "5":
                print(f"See you later! Bye for now!\n")
                run = False
            
            else:
                print(f"Invalid Option.\n")
                




if __name__ == "__main__":
    
    app = VocabularyApp()

    app.menu()


