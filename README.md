# Vocabulary Builder App

A Python-based vocabulary learning application that helps users discover new words, understand their meanings, and improve retention using AI-generated explanations, flashcards, and quizzes.

## Features

* Search for words using a dictionary API.
* Generate explanations, example sentences, memory tricks, and quiz questions with Gemini AI.
* Save words as flashcards.
* Review saved flashcards.
* Take interactive quizzes.
* Store and view quiz scores.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

This project uses Gemini AI. Since API keys are private and are not tracked by Git, you must create your own `.env` file.

### Step 1: Obtain a Gemini API Key

Visit:

https://aistudio.google.com/

Create an API key.

### Step 2: Create a `.env` File

In the project root directory, create a file named:

```text
.env
```

Add the following:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with the API key you generated.

## Running the Application

### Console Version

```bash
python main.py
```

### Streamlit Version

Method 1:

```bash
streamlit run streamlit_app.py
```

Method 2 (Recommended):

```bash
python -m streamlit run streamlit_app.py
```

## Project Structure

```text
vocab_app/
│
├── data_folder/
│   ├── flashcards.json
│   └── quiz_scores.json
│
├── models/
│   ├── flashcard.py
│   └── word.py
│
├── services/
│   ├── dictionary_client.py
│   ├── gemini_client.py
│   ├── quiz_generator.py
│   └── spaced_repetition_manager.py
│
├── utils/
│   ├── file_manager.py
│   ├── flashcard_manager.py
│   ├── score_manager.py
│   └── text_cleaner.py
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
├── streamlit_app.py
└── README.md
```

## Technologies Used

* Python
* Streamlit
* Object-Oriented Programming (OOP)
* Gemini AI
* Dictionary API
* JSON

## Author

Developed as a vocabulary learning application for educational purposes.
