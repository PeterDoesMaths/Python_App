import os, json
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

print(completion.choices[0].message.content)

fullResponse = completion.choices[0].message.content
start_index = fullResponse.find("```python") + 10
end_index = fullResponse.find("```", start_index)
code = fullResponse[start_index:end_index]

exec(code)
