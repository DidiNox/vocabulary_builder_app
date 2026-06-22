# IMPORTS
import random
from models.flashcard import Flashcard
from difflib import SequenceMatcher


# QuizGenerator Class
class QuizGenerator:

    def __init__(self):
        self.score = 0
        self.total_questions = 0

    # Function to compare user answer with correct answer
    def is_correct_answer(self, user_answer: str, correct_answer: str) -> bool:
        # Normalize both strings
        user_answer = user_answer.strip().lower()
        correct_answer = correct_answer.strip().lower()
        
        similarity = SequenceMatcher(None, user_answer, correct_answer).ratio()
        
        return similarity >= 0.8
    

    # Function to Generate Random Questions for Streamlit
    def generate_question(self, flashcard: Flashcard) -> dict:

        # Validation
        if not isinstance(flashcard, Flashcard):
            raise("flashcard must be a Flashcard object.\n")
        

        question_types: list[dict] = []

        if flashcard.explanation:
            question_types.append(
                {
                    "title": "What word means: ", 
                    "question": flashcard.explanation, 
                    "answer": flashcard.word
                }
            )
        
        if flashcard.example:
            question_types.append(
                {
                    "title": "Which word best fits this sentence?: ", 
                    "question": flashcard.example, 
                    "answer": flashcard.word
                }
            )

        if flashcard.memory_trick:
            question_types.append(
                {
                    "title": "Which word is described by this memory trick?: ", 
                    "question": flashcard.memory_trick, 
                    "answer": flashcard.word
                }
            )
        
        if not question_types:
            raise ValueError("No valid questions available.\n")
        
        return random.choice(question_types)


    
    # Function to Ask Users Questions
    def ask_questions(self, flashcard: Flashcard, quest_no: int) -> bool:

        # Validation
        if not isinstance(flashcard, Flashcard):
            raise TypeError(f"flashcard must be a Flashcard object.\n")
        
        # Build Up Varieties of Question Types to Ask User
        question_types: list[dict] = []

        if flashcard.explanation:
            question_types.append(
                {
                    "title": "What word means: ", 
                    "question": flashcard.explanation, 
                    "answer": flashcard.word
                }
            )
        
        if flashcard.example:
            question_types.append(
                {
                    "title": "Which word best fits this sentence?: ", 
                    "question": flashcard.example, 
                    "answer": flashcard.word
                }
            )

        if flashcard.memory_trick:
            question_types.append(
                {
                    "title": "Which word is described by this memory trick?: ", 
                    "question": flashcard.memory_trick, 
                    "answer": flashcard.word
                }
            )
        
        
        if not question_types:
            raise ValueError(f"No valid questions available.\n")
        
        
        # Randomly Choose a Type of Question for Display to User
        selected_question = random.choice(question_types)
        
        print()
        
        # Displays the Question
        print("-----------------------------\n")
        
        print(
            f"Question {quest_no} of {self.total_questions}\n\n"
            f"{selected_question["title"]}\n"
            f"{selected_question["question"]}\n"
        
        )
        print("-----------------------------\n")
        # Collects user's answer input
        while True:
            user_answer = input("Your answer: ").strip()

            if user_answer:
                break

            print(f"Answer cannot be empty!.\n")

        if self.is_correct_answer(user_answer, selected_question["answer"]):
            print(f"\✅✅ CORRRECT!\n")
            self.score += 1
            return True
        
        else:
            print(f"\n❌❌ WRONG!!\n")
            print(f"The correct answer is: {flashcard.word}\n")
            return False
    
       
    
    # Function to Start the Quiz
    def start_quiz(self, flashcards: list[Flashcard], no_of_quests: int = 7) -> int:

        self.score = 0
        self.total_questions = 0

        # Validation
        if not isinstance(no_of_quests, int):
            raise TypeError(f"Number_of_questions must be an integer.\n")
        
        if no_of_quests <= 0:
            raise ValueError(f"Number of questions must be positive!\n")

        if not flashcards:
            print(f"No flashcard available.\n")
            return 0
        
        # Flashcard Validation
        for card in flashcards:
            if not isinstance(card, Flashcard):
                raise TypeError(f"All card items must be a Flashcard object.\n")
        
        

        try:
            selected_cards = random.sample(
                flashcards, 
                min(
                    no_of_quests, 
                    len(flashcards)
                )
            
            )

            self.total_questions = len(selected_cards)
        
        except ValueError as e:
            print(f"Quiz error: {e}.\n")
            return 0
        
        # Iterate through the cards of questions and asks users via display.
        for num, card in enumerate(selected_cards, start=1):
            self.ask_questions(card, num)
        
        percent = (self.score / self.total_questions) * 100
        
        print()

        # Displays User's Final Score
        print("-----------------------------\n")

        print(
            f"Final Score: {self.score}/{self.total_questions}.\n"
            f"Percentage: {percent:.1f}%\n"
        )

        print("-----------------------------\n")

        
        

        return self.score
    

    
