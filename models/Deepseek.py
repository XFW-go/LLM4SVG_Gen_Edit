from openai import OpenAI
from abc import ABC


class Deepseek(ABC):
    
    def __init__(self, model, api_key):
        self.model = model  # ["deepseek-chat", "deepseek-reasoner"]
        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key, 
            base_url="https://api.deepseek.com"
        )
        
        
    def basic_request(self, system_prompt, prompt, **kwargs):
        response = self.client.chat.completions.create(
            **kwargs,
            model=self.model,
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": prompt
                },
            ],
        )
        
        return response
    
    
    def vision_request(self, system_prompt, prompt, image_path, **kwargs):
        raise NotImplementedError("Deepseek only supports text inputs")
    

if __name__ == "__main__":
    model = "deepseek-chat"  # or "deepseek-reasoner"
    api_key = "XXXX"
    ds = Deepseek(model, api_key)
    
    sys_prompt = "you are a XXX system"
    prompt = "please provide ..."
    ans = ds.basic_request(sys_prompt, prompt)
    
    ans_str = ans.choices[0].message.content
