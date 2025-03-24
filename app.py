import spacy
import re
import json
from tqdm import tqdm
import ollama

# Load spaCy model for text processing
nlp = spacy.load("en_core_web_sm")
OLLAMA_API_URL = "http://127.0.0.1:11434"  # Change to your Ollama server URL

def test_ollama_connection():
    """Ensure Ollama is running and directly use 'gemma2:2b'."""
    try:
        ollama.show("gemma2:2b")  # Directly check if the model exists
        print("✅ Successfully connected to Ollama. Using model: gemma2:2b")
        return "gemma2:2b"
    except Exception as e:
        print(f"❌ Error: Could not connect to Ollama or find 'gemma2:2b'.\nDetails: {e}")
        exit(1)

class FlashcardGenerator:
    def __init__(self, model_name="gemma2:2b"):
        self.model_name = model_name
        print(f"📌 Using Ollama model: {self.model_name}")

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
Generate 5 flashcards from the following text.
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
            print("\n📄 Raw Ollama Response:\n", response_text)  # Debugging output

            # 🔹 Improved Regex for better extraction
            flashcard_pairs = []
            matches = re.findall(r"\*\*Q:\*\*\s*(.*?)\s*\n\*\*A:\*\*\s*(.*?)\s*(?=\n\*\*Q:\*\*|$)", response_text, re.DOTALL)

            
            for question, answer in matches:
                question, answer = question.strip(), answer.strip(".,;:!?")
                if len(question.split()) > 2 and len(answer.split()) <= 5:  # Ensuring valid flashcards
                    flashcard_pairs.append({"question": question, "answer": answer})

            return flashcard_pairs

        except Exception as e:
            print(f"❌ Error generating flashcards: {e}")
            return []

    def process_text(self, text):
        """Process text to generate flashcards."""
        chunks = self.chunk_text(text)
        all_flashcards, seen_questions = [], set()

        print(f"🔄 Processing {len(chunks)} text chunks...")
        for chunk in tqdm(chunks, desc="Generating Flashcards"):
            flashcards = self.generate_flashcards(chunk)
            for card in flashcards:
                norm_question = card["question"].lower()
                if norm_question not in seen_questions:
                    seen_questions.add(norm_question)
                    all_flashcards.append(card)

        return all_flashcards

def main():
    print("\n🔗 Connecting to Ollama...")
    model_name = test_ollama_connection()
    
    print("\n📝 Enter or paste your text below. Press Enter twice when done:")
    lines = []
    while True:
        try:
            line = input()
            if not line:
                break
            lines.append(line)
        except EOFError:
            break
            
    text = "\n".join(lines)
    if not text.strip():
        print("⚠️ Error: No text provided.")
        return
        
    generator = FlashcardGenerator(model_name)
    flashcards = generator.process_text(text)
    
    output_file = "flashcards.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(flashcards, f, indent=2)
        
    print(f"\n✅ Generated {len(flashcards)} unique flashcards and saved to {output_file}")
    
    if flashcards:
        print("\n📚 Sample flashcards:")
        for i, card in enumerate(flashcards[:5]):
            print(f"{i+1}. Q: {card['question']}")
            print(f"   A: {card['answer']}")

if __name__ == "__main__":
    main()
