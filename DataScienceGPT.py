import os, json, re
import openai

# get OpenAI API key from json file
with open('openaicreds.json') as f:
    openaicreds = json.load(f)
    openai.api_key = openaicreds['api_key']

# get system prompt and user prompt
systemMessage = open('system_prompt.txt','r').read()
userMessage = open('prompt.txt','r').read()

# generate response from ChatGPT
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
print(fullResponse)

# Find all code and run it.
code_pattern = r'```python(.*?)```'
matches = re.findall(code_pattern, fullResponse, re.DOTALL)
for match in matches:
    exec(match)
