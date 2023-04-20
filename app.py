import openai
import os, json
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# get OpenAI API key from json file
with open('openaicreds.json') as f:
    openaicreds = json.load(f)
    openai.api_key = openaicreds['api_key']

@app.route("/")
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files['file']

    # Read in file using pandas
    if file.filename.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.filename.endswith('.txt'):
        data = pd.read_table(file)
    elif file.filename.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")

    # Display the first five rows of the data
    # return data.head().to_html()

    # Get the prompt from the user
    prompt = request.form['prompt']

    # Get system prompt and user prompt
    systemMessage = open('system_prompt.txt','r').read()
    userMessage = prompt
    
    # Generate response from ChatGPT
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemMessage},
        {"role": "user", "content": userMessage}
    ], # can also add assistant role and message for one-shot prompting
    temperature = 0.2 # a measure of how deterministic the output is (between 0 and 2)
    )

    # retrieve responce and print
    fullResponse = completion.choices[0].message.content

    # Render the template with the prompt and the head of the data
    return render_template('result.html', prompt=prompt, data=data.head(), fullResponse=fullResponse)

if __name__ == '__main__':
    app.run(debug=True)
