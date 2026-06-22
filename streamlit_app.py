import streamlit as st
import random
from services.dictionary_client import DictionaryClient
from services.gemini_client import GeminiClient
from services.quiz_generator import QuizGenerator
from utils.flashcard_manager import FlashcardManager
from utils.score_manager import ScoreManager
from models.flashcard import Flashcard

st.title("Vocabulary Builder App")
st.write(
    "Learn new words using AI-generated explanations, "
    "memory tricks, and quizzes."
)

# Objects of Each Classes
dictionary_client = DictionaryClient()
gemini_client = GeminiClient()
quiz_generator = QuizGenerator()
flashcard_manager = FlashcardManager()
score_manager = ScoreManager()



# Initialize Session Variables
if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "score_saved" not in st.session_state:
    st.session_state.score_saved = False

if "answer_checked" not in st.session_state:
    st.session_state.answer_checked = False

if "answer_result" not in st.session_state:
    st.session_state.answer_result = None





# Creating A Sidebar
st.sidebar.title("Navigation")

# Sidebar Menu Options
menu = st.sidebar.radio(
    "Choose an option", 
    [
        "Search Word", 
        "Review Flashcards", 
        "Take Quiz", 
        "View Scores"
    ]
)


# Search Word Menu Option
if menu == "Search Word":

    word = st.text_input("Enter a word")

    if st.button("Search Word"):

        # Validation
        if not word.strip():
            st.error("Please enter a word!")

        else:

            try:

                word_obj = (
                    dictionary_client.get_data_word(word)
                )

                st.subheader("Word Information")

                st.write(
                    f"-----------------------------------------\n"
                    f"**Word:** {word_obj.word}\n\n"
                    f"**Definition:** {word_obj.definition}\n\n"
                    f"**Phonetics:** {word_obj.phonetics}\n\n"
                )

                st.write("**Examples:**")

                for example in word_obj.examples:
                    st.write(f"-- {example}")

                st.write("\n**Synonyms:**")
                st.write(
                    ", ".join(word_obj.synonyms)
                )

                st.write("\n**Antonyms:**")
                st.write(
                    ", ".join(word_obj.antonyms)
                )

                st.write(
                    "-----------------------------------------"
                )


                # Generate AI Content
                ai_data = (
                    gemini_client.generate_word(word)
                )

                st.subheader(
                    "AI Learning Assistant"
                )

                st.write(
                    "-----------------------------------------"
                )

                st.write(
                    "##### Simple Explanation:"
                )

                st.write(
                    f"*{ai_data['simple_explanation']}*"
                )

                st.write(
                    "##### Example Sentence:"
                )

                st.write(
                    f"*{ai_data['example_sentence']}*"
                )

                st.write(
                    "##### Memory Trick:"
                )

                st.info(
                    ai_data["memory_trick"]
                )

                st.write(
                    "##### Quiz Question:"
                )

                st.warning(
                    ai_data["quiz_question"]
                )

                st.write(
                    "-----------------------------------------"
                )


                # Create Flashcard Object
                flashcard = Flashcard(
                    word=word,
                    explanation=ai_data[
                        "simple_explanation"
                    ],
                    example=ai_data[
                        "example_sentence"
                    ],
                    memory_trick=ai_data[
                        "memory_trick"
                    ],
                    quiz_question=ai_data[
                        "quiz_question"
                    ]
                )


                # Check whether flashcard already exists
                existing_cards = (
                    flashcard_manager
                    .load_flashcards()
                )

                already_exists = False

                for card in existing_cards:

                    if (
                        card.word.lower()
                        ==
                        flashcard.word.lower()
                    ):

                        already_exists = True
                        break


                # Save if not existing
                if already_exists:

                    st.success(
                        "Flashcard already exists and is saved!"
                    )

                else:

                    flashcard_manager.save_flashcards(
                        flashcard
                    )

                    st.success(
                        "Flashcard saved successfully!"
                    )


            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )




# Review Flashcards Menu Option
elif menu == "Review Flashcards":

    st.subheader("📚 Saved Flashcards")

    flashcards = flashcard_manager.load_flashcards()

    if not flashcards:

        st.warning(
            "No flashcards found!"
        )

    else:

        st.success(
            f"{len(flashcards)} flashcard(s) found."
        )

        # Search box
        search_word = st.text_input(
            "Search flashcards"
        ).strip().lower()


        filtered_cards = []

        for card in flashcards:

            if (
                not search_word
                or
                search_word in card.word.lower()
            ):

                filtered_cards.append(card)


        if not filtered_cards:

            st.warning(
                "No matching flashcards found."
            )


        else:

            for index, card in enumerate(
                filtered_cards,
                start=1
            ):

                with st.expander(
                    f"{index}. {card.word.title()}"
                ):

                    st.markdown(
                        "### 📖 Explanation"
                    )

                    st.write(
                        card.explanation
                    )


                    st.markdown(
                        "### ✏ Example"
                    )

                    st.write(
                        card.example
                    )


                    st.markdown(
                        "### 🧠 Memory Trick"
                    )

                    st.info(
                        card.memory_trick
                    )


                    st.markdown(
                        "### ❓ Quiz Question"
                    )

                    st.warning(
                        card.quiz_question
                    )



# Take Quiz Menu Option
elif menu == "Take Quiz":

    st.subheader("🧠 Quiz")

    flashcards = flashcard_manager.load_flashcards()

    if not flashcards:

        st.warning("No flashcards available!")

    else:

        # Show setup only before quiz starts
        if not st.session_state.quiz_started:

            no_of_quests = st.number_input(
                "How many questions?",
                min_value=1,
                max_value=len(flashcards),
                value=1
            )

            if st.button("Start Quiz"):

                st.session_state.selected_cards = random.sample(
                    flashcards,
                    min(no_of_quests, len(flashcards))
                )

                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_started = True
                st.session_state.score_saved = False
                st.session_state.answer_checked = False
                st.session_state.answer_result = None

                st.rerun()

        # Quiz has started
        else:

            current_index = st.session_state.current_question

            # Quiz completed
            if current_index >= len(st.session_state.selected_cards):

                percent = (
                    st.session_state.score
                    /
                    len(st.session_state.selected_cards)
                ) * 100

                st.success("🎉 Quiz Completed!")

                st.write(
                    f"Score: "
                    f"{st.session_state.score}/"
                    f"{len(st.session_state.selected_cards)}"
                )

                st.write(
                    f"Percentage: {percent:.1f}%"
                )

                # Save score once
                if not st.session_state.score_saved:

                    score_manager.save_scores(
                        st.session_state.score,
                        len(st.session_state.selected_cards)
                    )

                    st.session_state.score_saved = True

                st.info(
                    "Use the sidebar to view score history."
                )

                if st.button("🆕 New Quiz"):

                    st.session_state.quiz_started = False
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.score_saved = False
                    st.session_state.selected_cards = []
                    st.session_state.answer_checked = False
                    st.session_state.answer_result = None

                    st.rerun()

            # Continue quiz
            else:

                try:

                    current_card = (
                        st.session_state.selected_cards[
                            current_index
                        ]
                    )

                    question = (
                        quiz_generator.generate_question(
                            current_card
                        )
                    )

                    st.write(
                        f"Question "
                        f"{current_index + 1} "
                        f"of "
                        f"{len(st.session_state.selected_cards)}"
                    )

                    st.subheader(
                        question["title"]
                    )

                    st.write(
                        question["question"]
                    )

                    answer = st.text_input(
                        "Your answer",
                        key=f"answer_{current_index}"
                    )

                    # User has not checked answer yet
                    if not st.session_state.answer_checked:

                        if st.button("Submit Answer"):

                            if not answer.strip():

                                st.warning(
                                    "Answer cannot be empty!"
                                )

                            else:

                                if quiz_generator.is_correct_answer(
                                    answer,
                                    question["answer"]
                                ):

                                    st.session_state.score += 1

                                    st.session_state.answer_result = {
                                        "correct": True,
                                        "answer": question["answer"]
                                    }

                                else:

                                    st.session_state.answer_result = {
                                        "correct": False,
                                        "answer": question["answer"]
                                    }

                                st.session_state.answer_checked = True

                                st.rerun()

                    # Answer already checked
                    else:

                        if (
                            st.session_state.answer_result[
                                "correct"
                            ]
                        ):

                            st.success("✅ Correct!")

                        else:

                            st.error("❌ Wrong!")

                        st.write(
                            "Correct Answer: "
                            +
                            st.session_state.answer_result[
                                "answer"
                            ]
                        )

                        # Not last question
                        if current_index < (
                            len(
                                st.session_state.selected_cards
                            ) - 1
                        ):

                            if st.button(
                                "Next Question ➡️"
                            ):

                                st.session_state.current_question += 1
                                st.session_state.answer_checked = False
                                st.session_state.answer_result = None

                                st.rerun()

                        # Last question
                        else:

                            if st.button(
                                "Finish Quiz 🏁"
                            ):

                                st.session_state.current_question += 1
                                st.session_state.answer_checked = False
                                st.session_state.answer_result = None

                                st.rerun()

                except Exception as e:

                    st.error(
                        f"Quiz error: {e}"
                    )




# View Scores Menu Option
elif menu == "View Scores":

    st.subheader("🏆 Quiz History")

    scores = score_manager.load_scores()

    if not scores:

        st.warning(
            "No scores found!"
        )

    else:

        st.success(
            f"{len(scores)} score(s) found."
        )


        # Statistics
        total_quizzes = len(scores)

        average_score = (
            sum(
                score["score"]
                for score in scores
            )
            /
            total_quizzes
        )

        best_score = max(
            score["score"]
            for score in scores
        )


        st.metric(
            "Total Quizzes Taken",
            total_quizzes
        )

        st.metric(
            "Average Score",
            f"{average_score:.1f}"
        )

        st.metric(
            "Best Score",
            best_score
        )


        st.divider()


        # Latest first
        for index, score in enumerate(
            reversed(scores),
            start=1
        ):

            percent = (
                score["score"]
                /
                score["total_questions"]
            ) * 100


            with st.expander(
                f"Quiz #{index}"
            ):

                st.write(
                    f"Score: "
                    f"{score['score']}/"
                    f"{score['total_questions']}"
                )

                st.write(
                    f"Percentage: "
                    f"{percent:.1f}%"
                )

                st.write(
                    f"Date: "
                    f"{score['date']}"
                )
    

