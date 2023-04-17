import os, json
import openai
with open('Python_App\openaicreds.json') as f:
    openaicreds = json.load(f)
    openai.api_key = openaicreds['api_key']


""" completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[s
    {"role": "user", "content": "Have you heard about updog?"}
  ]
)

print(completion.choices[0].message) """


""" text = openai.Completion.create(
  model="text-davinci-003",
  prompt="Say this is a test",
  max_tokens=7,
  temperature=0
)

print(text.choices[0].text) """

