import re
import json
from typing import List, Dict, Set

class FlashcardGenerator:
    def __init__(self):
        self.min_answer_length = 2
        self.max_answer_length = 7
        self.max_flashcards = 100
        print("📌 Flashcard Generator initialized (lightweight mode)")

    def chunk_text(self, text: str, max_chunk_size: int = 500) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
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
        flashcards = []
        seen = set()
        sentences = re.split(r'(?<=[.!?])\s+', text_chunk)

        for sent in sentences:
            match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', sent)
            if match:
                answer = match.group(1)
                question = sent.replace(answer, "______")
                if len(answer.split()) <= self.max_answer_length and len(question.split()) > 3:
                    question_key = question.lower().strip()
                    if question_key not in seen:
                        flashcards.append({"question": question.strip(), "answer": answer.strip()})
                        seen.add(question_key)

        return flashcards

    def process_text(self, text: str) -> List[Dict[str, str]]:
        chunks = self.chunk_text(text)
        all_flashcards: List[Dict[str, str]] = []
        seen_questions: Set[str] = set()

        print(f"🔄 Processing {len(chunks)} text chunks...")
        for chunk in chunks:
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
