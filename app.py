import openai
import json, re
from flask import Flask, render_template, request
import pandas as pd
from io import StringIO
import sys

app = Flask(__name__)

# get OpenAI API key from json file
with open('openaicreds.json') as f:
    openaicreds = json.load(f)
    openai.api_key = openaicreds['api_key']

# Define chatGPT completion function
def get_completion(systemMessage, prompt):
    messages=[
            {"role": "system", "content": systemMessage},
            {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

# render data upload page
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
    dataHead =  data.head()
    dataHead = pd.DataFrame.to_string(dataHead)

    # Get the prompt from the user
    userMessage = request.form['prompt']

    # Get system prompt
    systemMessage = open('system_prompt.txt','r').read()
    interpMessage = open('interp_system_prompt.txt','r').read()

    # Create prompt from user input
    with open('prompt.txt','r') as f:
        prompt = f.read()
        prompt = prompt.replace('dataFile', file.filename)
        prompt = prompt.replace('dataHead', dataHead)
        prompt = prompt.replace('userMessage', userMessage)
    
    print(prompt)

    """ # Generate response from ChatGPT
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemMessage},
            {"role": "user", "content": prompt}
        ], # can also add assistant role and message for one-shot prompting
        temperature = 0.2 # a measure of how deterministic the output is (between 0 and 2)
    ) """
    # Generate response from ChatGPT
    fullResponse = get_completion(systemMessage, prompt)

    # retrieve responce and print
    #fullResponse = completion.choices[0].message.content
    print(fullResponse)

    # Redirect stdout to a StringIO object to capture output
    old_stdout = sys.stdout
    sys.stdout = output_buffer = StringIO()

    # Find all code and run it.
    code_pattern = r'```python(.*?)```'
    code = re.findall(code_pattern, fullResponse, re.DOTALL)
    for match in code:
        exec(match)

    # Reset stdout and get captured output
    sys.stdout = old_stdout
    output = output_buffer.getvalue()

    with open('interp_prompt.txt','r') as f:
        interpPrompt = f.read()
        interpPrompt = interpPrompt.replace('dataFile', file.filename)
        interpPrompt = interpPrompt.replace('dataHead', dataHead)
        interpPrompt = interpPrompt.replace('pythonCode', fullResponse)
        interpPrompt = interpPrompt.replace('pythonOutput', output)

    """ # Interpret python output using ChatGPT
    interpretation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": interpMessage},
            {"role": "user", "content": interpPrompt}
        ],
        temperature = 0.2 
    ) """
    # Interpret python output using ChatGPT
    interpResponse = get_completion(interpMessage, interpPrompt)

    #interpResponse = interpretation.choices[0].message.content
    print(interpResponse)

    # Self-reflection (ask ChatGPT if user query is answered)

    # Render the template with the prompt and the head of the data
    return render_template('result.html', userMessage=userMessage, data=data.head(), fullResponse=fullResponse, output=output, interpretation=interpResponse)

if __name__ == '__main__':
    app.run(debug=True)
