import openai
import streamlit as st
import json
import os
# from .app import generate_flashcards_with_openai  # Import the flashcard generation logic from app.py

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv(api_key = st.secrets["OPENAI_API_KEY"])

def generate_flashcards_with_openai(text: str) -> list[dict]:
    """
    Generate flashcards using OpenAI's latest API
    Returns: List of {"question": str, "answer": str}
    """
    prompt = f"""Generate 5 concise flashcards from this text. Follow exactly:
    
Text: {text}

Format each flashcard as:
Q: [Clear question about key concept]
A: [Succinct answer, max 15 words]

Focus on:
- Key terms and definitions
- Cause-effect relationships
- Important dates/figures (if applicable)"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=500  # Limit response length
        )
        
        content = response.choices[0].message.content
        return _parse_flashcards(content)
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []

def _parse_flashcards(content: str) -> list[dict]:
    """Parse Q/A pairs from formatted text"""
    flashcards = []
    current_q, current_a = None, None
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('Q:'):
            if current_q and current_a:  # Save previous pair
                flashcards.append({"question": current_q, "answer": current_a})
            current_q = line[2:].strip()
            current_a = None
        elif line.startswith('A:'):
            current_a = line[2:].strip()
    
    # Add the last pair if exists
    if current_q and current_a:
        flashcards.append({"question": current_q, "answer": current_a})
        
    return flashcards[:5]  # Ensure max 5 cards


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
