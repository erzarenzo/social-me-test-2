from transformers import pipeline

# Load the Hugging Face GPT model
generator = pipeline("text-generation", model="gpt2")

def generate_command(command):
    return generator(command, max_length=50, num_return_sequences=1)[0]['generated_text']

if __name__ == "__main__":
    command = input("What do you want to do? ")
    response = generate_command(command)
    print(f"Generated command: {response}")
