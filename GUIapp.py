import openai
import streamlit as st
import json
import os
from .app import generate_flashcards_with_openai  # Import the flashcard generation logic from app.py

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv(api_key = st.secrets["OPENAI_API_KEY"])

# Streamlit UI for Flashcard Generator
st.title("📚 Flashcard Generator")
st.write("Generate flashcards based on your text")

text_input = st.text_area("Paste your text here:", height=200)

if st.button("Generate Flashcards"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        flashcards = generate_flashcards_with_openai(text_input)

        if flashcards:
            st.success(f"Generated {len(flashcards)} flashcards")
            st.markdown("---")

            for i, card in enumerate(flashcards):
                st.write(f"**Q{i+1}:** {card['question']}")
                st.write(f"**A:** {card['answer']}")
                st.markdown("---")

            st.download_button(
                "Download as JSON",
                json.dumps(flashcards, indent=2),
                "flashcards.json",
                "application/json"
            )
        else:
            st.error("No flashcards generated. Try different or longer text.")
