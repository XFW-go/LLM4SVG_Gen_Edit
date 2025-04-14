import anthropic
from abc import ABC
import base64
import os

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
        
        
class Claude(ABC):
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=self.api_key,)
    
    def basic_request(self, system_prompt, prompt, **kwargs):
        message = self.client.messages.create(
            model=self.model, #"claude-3-7-sonnet-20250219",
            max_tokens=1024,
            system = system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        return message
    
    def vision_request(self, system_prompt, prompt, image_media_type, image_path, **kwargs):
        image_data = encode_image(image_path)
        message = self.client.messages.create(
            model=self.model, #"claude-3-7-sonnet-20250219",
            max_tokens=1024,
            system = system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        return message
    
    def score_2_imgs(self, system_prompt, prompt, image_media_type, image1_path, image2_path, **kwargs):
        image1_data = encode_image(image1_path)
        image2_data = encode_image(image2_path)
        message = self.client.messages.create(
            model=self.model, #"claude-3-7-sonnet-20250219",
            max_tokens=1024,
            system = system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Image 1:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_media_type,
                                "data": image1_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Image 2:"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_media_type,
                                "data": image2_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        return message
    
if __name__ == "__main__":
    Sonnet = Claude(model='claude-3-7-sonnet-20250219', api_key="Your Anthropic API key")
    system_prompt = 'You are an assistant.'
    prompt = 'Your prompt'
    answer = Claude.basic_request(system_prompt, prompt)
    ans = answer.content[0].text