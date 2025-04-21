import streamlit as st
import spacy
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class FlashcardGenerator:
    def __init__(self):
        pass

    def generate_flashcards(self, text):
        """Generate basic flashcards using NER"""
        doc = nlp(text)
        flashcards = []
        seen = set()

        for ent in doc.ents:
            question = f"What is {ent.label_} in the context?"
            answer = ent.text.strip()

            if question.lower() not in seen:
                flashcards.append({"question": question, "answer": answer})
                seen.add(question.lower())

        return flashcards

# Basic Streamlit UI
st.title("📚 Flashcard Generator")
st.write("Generate simple flashcards from your text")

text_input = st.text_area("Paste your text here:", height=200)

if st.button("Generate Flashcards"):
    if not text_input.strip():
        st.warning("Please enter some text")
    else:
        generator = FlashcardGenerator()
        flashcards = generator.generate_flashcards(text_input)

        if flashcards:
            st.success(f"Generated {len(flashcards)} flashcards")
            st.markdown("---")
            
            for i, card in enumerate(flashcards):
                st.write(f"**Q{i+1}:** {card['question']}")
                st.write(f"**A:** {card['answer']}")
                st.markdown("---")

            # JSON Download
            st.download_button(
                "Download as JSON",
                json.dumps(flashcards, indent=2),
                "flashcards.json",
                "application/json"
            )
        else:
            st.error("No flashcards generated. Try different text.")