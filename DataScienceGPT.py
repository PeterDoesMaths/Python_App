import os, json, re
import openai
with open('openaicreds.json') as f:
    openaicreds = json.load(f)
    openai.api_key = openaicreds['api_key']

systemMessage = open('system_prompt.txt','r').read()
userMessage = open('prompt.txt','r').read()

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": systemMessage},
    {"role": "user", "content": userMessage}
  ]
)

fullResponse = completion.choices[0].message.content

print(fullResponse)

# Find all code and run it.
code_pattern = r'```python(.*?)```'
matches = re.findall(code_pattern, fullResponse, re.DOTALL)
for match in matches:
    exec(match)
