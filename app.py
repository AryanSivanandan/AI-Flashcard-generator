import openai
import os

# Retrieve the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_flashcards_with_openai(text):
    prompt = f"""
    Generate flashcards based on the following text:
    {text}

    The flashcards should be in the following format:
    Q: [Question]
    A: [Answer]
    """

    # OpenAI API call to generate flashcards
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can adjust the model as needed
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    flashcards = []
    content = response.choices[0].message["content"]

    # Parsing the response content to extract questions and answers
    for line in content.strip().split("\n"):
        if line.startswith("Q:"):
            question = line[3:].strip()
        elif line.startswith("A:"):
            answer = line[3:].strip()
            flashcards.append({"question": question, "answer": answer})

    return flashcards
