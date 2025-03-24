# 📚 AI Flashcard Generator

This project is a **Streamlit-based Flashcard Generator** that uses **Ollama's AI models** to generate flashcards from any given text. It helps users quickly extract key information in a question-answer format for study and review purposes.

## 🚀 Features
- **Interactive UI**: Built with Streamlit for a user-friendly experience.
- **AI-Powered Flashcards**: Uses Ollama's `gemma2:2b` model to generate intelligent flashcards.
- **Text Chunking**: Splits large text into smaller chunks for better processing.
- **Flashcard Extraction**: Extracts structured Q&A pairs from text.
- **Download Option**: Save flashcards as a JSON file.

## 📦 Installation

### 1️⃣ Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install streamlit spacy ollama tqdm
```

### 2️⃣ Install spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### 3️⃣ Start Ollama (if not already running)
You need to have Ollama installed and running. To check:
```bash
ollama show gemma2:2b
```
If it's not installed, follow [Ollama's installation guide](https://ollama.com).

### 4️⃣ Run the Application
```bash
streamlit run flashcard_app.py
```

## 🛠 Usage
1. Paste or enter your text in the provided input box.
2. Click the **"Generate Flashcards"** button.
3. View AI-generated flashcards directly on the interface.
4. Download the flashcards as a JSON file for later use.

## 📌 Example Output
**Input Text:**
```
The mitochondrion is the powerhouse of the cell, producing ATP through cellular respiration.
```
**Generated Flashcard:**
```
Q1: What is the powerhouse of the cell?
A: Mitochondrion
```

## 🔗 Dependencies
- **Python 3.8+**
- **Streamlit** for UI
- **spaCy** for text processing
- **Ollama** for AI-generated responses
- **tqdm** for progress tracking

## 📝 License
This project is open-source and available under the MIT License.

