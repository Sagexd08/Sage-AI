import os
import requests
import json
from config import apikey

# OpenRouter API endpoint
url = "https://openrouter.ai/api/v1/chat/completions"

# Headers for OpenRouter API
headers = {
    "Authorization": f"Bearer {apikey}",
    "Content-Type": "application/json"
}

# Request payload for Mistral model
data = {
    "model": "mistralai/devstral-small:free",
    "messages": [
        {
            "role": "user",
            "content": "Write an email to my boss for resignation?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 256,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

# Make the API request
response = requests.post(url, headers=headers, json=data)

# Parse and print the response
if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
    print("\n" + "="*50)
    print("Generated text:")
    print(result['choices'][0]['message']['content'])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
'''
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "\n\nSubject: Resignation\n\nDear [Name],\n\nI am writing to inform you of my intention to resign from my current position at [Company]. My last day of work will be [date].\n\nI have enjoyed my time at [Company], and I am grateful for the opportunity to work here. I have learned a great deal during my time in this position, and I am grateful for the experience.\n\nIf I can be of any assistance during this transition, please do not hesitate to ask.\n\nThank you for your understanding.\n\nSincerely,\n[Your Name]"
    }
  ],
  "created": 1683815400,
  "id": "cmpl-7F1aqg7BkzIY8vBnCxYQh8Xp4wO85",
  "model": "text-davinci-003",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 125,
    "prompt_tokens": 9,
    "total_tokens": 134
  }
}
'''
