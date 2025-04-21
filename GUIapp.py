import streamlit as st
import json
import re

# ✅ Lightweight Flashcard Generator (no spaCy)
def generate_flashcards_lightweight(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    flashcards = []
    seen = set()

    for sent in sentences:
        # Basic proper noun / key term detection (capitalized words)
        match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', sent)
        if match:
            answer = match.group(1)
            question = sent.replace(answer, "______")
            if len(answer.split()) <= 5 and len(question.split()) > 3:
                question_key = question.lower().strip()
                if question_key not in seen:
                    flashcards.append({"question": question.strip(), "answer": answer.strip()})
                    seen.add(question_key)

    return flashcards

# Streamlit UI
st.title("📚 Flashcard Generator (Lightweight)")
st.write("Generate flashcards without large NLP models")

text_input = st.text_area("Paste your text here:", height=200)

if st.button("Generate Flashcards"):
    if not text_input.strip():
        st.warning("Please enter some text")
    else:
        flashcards = generate_flashcards_lightweight(text_input)

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
