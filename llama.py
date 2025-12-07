import ollama

def generate_response(prompt: str) -> str:
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response['message']['content']

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        answer = generate_response(user_input)
        print("Assistant:", answer)