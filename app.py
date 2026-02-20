from ollama import chat
from flask import Flask

app = Flask(__name__)

def generate_response(prompt, model="llama3"):
    fullResponse = ""
    stream = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        token = chunk['message']['content']
        if token:
            fullResponse += token
            yield token, fullResponse  

@app.route('/')
def home():
    pass