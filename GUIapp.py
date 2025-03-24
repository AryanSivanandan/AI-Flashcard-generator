import streamlit as st
import spacy
import re
import json
import ollama
from tqdm import tqdm

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Test Ollama Connection
def test_ollama_connection():
    """Ensure Ollama is running and directly use 'gemma2:2b'."""
    try:
        ollama.show("gemma2:2b")  # Directly check if the model exists
        st.success("✅ Successfully connected to Ollama. Using model: gemma2:2b")
        return "gemma2:2b"
    except Exception as e:
        st.error(f"❌ Could not connect to Ollama or find 'gemma2:2b'.\nDetails: {e}")
        st.stop()

# Flashcard Generator Class
class FlashcardGenerator:
    def __init__(self, model_name="gemma2:2b"):
        self.model_name = model_name

    def chunk_text(self, text, max_chunk_size=500):
        """Split text into manageable chunks."""
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]
        chunks, current_chunk, current_length = [], [], 0

        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk, current_length = [sentence], sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def generate_flashcards(self, text_chunk):
        """Generate flashcards from a text chunk."""
        prompt = f"""
Generate maximum flashcards from the following text.
Each flashcard should have a question that is a complete sentence and an answer that is exactly one word or a short phrase.
Format:
Q: [question sentence]
A: [one-word or short answer]
Text:
{text_chunk}
"""
        try:
            response = ollama.generate(
                model=self.model_name, 
                prompt=prompt, 
                options={"temperature": 0.7, "num_predict": 500}
            )

            response_text = response.get("response", "").strip()

            # Extract Q&A pairs using regex
            flashcard_pairs = []
            matches = re.findall(r"\*\*Q:\*\*\s*(.*?)\s*\n\*\*A:\*\*\s*(.*?)\s*(?=\n\*\*Q:\*\*|$)", response_text, re.DOTALL)

            for question, answer in matches:
                question, answer = question.strip(), answer.strip(".,;:!?")
                if len(question.split()) > 2 and len(answer.split()) <= 5:
                    flashcard_pairs.append({"question": question, "answer": answer})

            return flashcard_pairs

        except Exception as e:
            st.error(f"❌ Error generating flashcards: {e}")
            return []

    def process_text(self, text):
        """Process text to generate flashcards."""
        chunks = self.chunk_text(text)
        all_flashcards, seen_questions = [], set()

        for chunk in tqdm(chunks, desc="Generating Flashcards"):
            flashcards = self.generate_flashcards(chunk)
            for card in flashcards:
                norm_question = card["question"].lower()
                if norm_question not in seen_questions:
                    seen_questions.add(norm_question)
                    all_flashcards.append(card)

        return all_flashcards

# Streamlit UI
st.title("📚 AI Flashcard Generator")
st.write("Enter text and generate flashcards using Ollama-powered AI!")

# Test Ollama connection
model_name = test_ollama_connection()

# Text Input
text_input = st.text_area("📝 Paste your text here:", height=250)

# Flashcard Generation
if st.button("Generate Flashcards"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text before generating flashcards.")
    else:
        generator = FlashcardGenerator(model_name)
        flashcards = generator.process_text(text_input)

        if flashcards:
            st.success(f"✅ Generated {len(flashcards)} flashcards!")
            for i, card in enumerate(flashcards):
                st.write(f"**Q{i+1}:** {card['question']}")
                st.write(f"**A:** {card['answer']}")
                st.markdown("---")

            # Download Flashcards as JSON
            flashcards_json = json.dumps(flashcards, indent=2)
            st.download_button(
                label="📥 Download Flashcards as JSON",
                data=flashcards_json,
                file_name="flashcards.json",
                mime="application/json",
            )
        else:
            st.error("⚠️ No flashcards were generated. Try with different text.")

