import spacy
import re
import json
from tqdm import tqdm
from typing import List, Dict, Set

# Load spaCy model (using the small model for Vercel compatibility)
nlp = spacy.load("en_core_web_sm")

class FlashcardGenerator:
    def __init__(self):
        self.min_answer_length = 2  # Minimum words in answer
        self.max_answer_length = 7  # Maximum words in answer
        self.max_flashcards = 100   # Maximum flashcards to return
        print("📌 Flashcard Generator initialized (spaCy only)")

    def chunk_text(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """Split text into semantically coherent chunks using sentence boundaries."""
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sent in sentences:
            sent_length = len(sent.split())
            if current_length + sent_length > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sent]
                current_length = sent_length
            else:
                current_chunk.append(sent)
                current_length += sent_length
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

    def generate_flashcards(self, text_chunk: str) -> List[Dict[str, str]]:
        """Generate multiple question types using spaCy's analysis."""
        doc = nlp(text_chunk)
        flashcards = []
        
        # 1. Named Entity Recognition (NER) cards
        for ent in doc.ents:
            if (self.min_answer_length <= len(ent.text.split()) <= self.max_answer_length
               and ent.label_ in ["PERSON", "ORG", "GPE", "DATE", "EVENT"]):
                flashcards.append({
                    "question": f"Who/what is '{ent.text}' in this context?",
                    "answer": f"{ent.label_}: {ent.text} (from: {ent.sent.text[:100]}...)"
                })
        
        # 2. Noun chunk cards (concepts)
        for chunk in doc.noun_chunks:
            if (chunk.root.pos_ == "NOUN" 
                and len(chunk.text.split()) >= 2
                and not any(t.is_stop for t in chunk)):
                flashcards.append({
                    "question": f"Explain the concept: '{chunk.text}'",
                    "answer": f"Related to: {chunk.root.lemma_}. Context: {chunk.sent.text[:150]}"
                })
        
        # 3. Action/verb cards
        for token in doc:
            if (token.pos_ == "VERB" 
                and not token.is_stop
                and token.lemma_ not in ["be", "have", "do"]):
                flashcards.append({
                    "question": f"What does the action '{token.text}' mean here?",
                    "answer": f"Verb: {token.lemma_}. Context: {token.sent.text[:100]}..."
                })
                
        return flashcards

    def process_text(self, text: str) -> List[Dict[str, str]]:
        """Process full text with duplicate prevention."""
        chunks = self.chunk_text(text)
        all_flashcards: List[Dict[str, str]] = []
        seen_questions: Set[str] = set()
        
        print(f"🔄 Processing {len(chunks)} text chunks...")
        for chunk in tqdm(chunks, desc="Generating Flashcards"):
            for card in self.generate_flashcards(chunk):
                question_hash = hash(card["question"].lower().strip())
                if question_hash not in seen_questions:
                    seen_questions.add(question_hash)
                    all_flashcards.append(card)
                    
        return sorted(all_flashcards, key=lambda x: len(x["question"]))[:self.max_flashcards]

def main():
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

    generator = FlashcardGenerator()
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
            print()

if __name__ == "__main__":
    main()