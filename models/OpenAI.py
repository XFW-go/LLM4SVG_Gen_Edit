from openai import OpenAI
import base64
import requests
from abc import ABC

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
        
        
class GPT(ABC):
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
        self.provider = "openai"

        self.history = []
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def basic_request(self, system_prompt, prompt, **kwargs):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            **kwargs,
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                    ]
                }
            ],
        }
            
        response = requests.post(self.base_url, headers=headers, json=data)
        try:
            response = response.json()
        except:
            response = ''

        return response
        
    def vision_request(self, system_prompt, prompt, image_path, **kwargs):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        base64_images = encode_image(image_path)
        
        data = {
            **kwargs,
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_images}"
                            }
                        }
                    ]
                }
            ],
            # "max_tokens": 300
        }
            
        response = requests.post(self.base_url, headers=headers, json=data)
        try:
            response = response.json()
        except:
            response = ''

        return response


if __name__ == "__main__":
    gpt4o = GPT(model='gpt-4o', api_key="Your OpenAI API key")
    system_prompt = 'You are an assitant.'
    txt_prompt = 'Your request'
    answer = gpt4o.basic_request(system_prompt, txt_prompt)
    ans = answer['choices'][0]['message']['content']