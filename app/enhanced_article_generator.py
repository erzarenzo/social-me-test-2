import requests
from connect_llm_to_generator import call_llm

def generate_article(topic):
    prompt = f"Write a detailed article about {topic}"
    return call_llm(prompt)

if __name__ == "__main__":
    print(generate_article("The Future of AI"))
