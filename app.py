from ollama import chat
from flask import Flask, render_template, Response, request

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
            yield token  

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.form['prompt']

    def stream_tokens():
        for token in generate_response(prompt):
            yield token  # stream each token to the browser

    return Response(stream_tokens(), mimetype='text/plain')

app.run()