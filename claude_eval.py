import anthropic
from abc import ABC
import base64
import os
from utils import parse_score_comment
from models.Claude import Claude

    
if __name__ == "__main__":
    sonnet = Claude(model='claude-3-7-sonnet-20250219', api_key="Your Anthropic API key")
    system_prompt = 'You are an assistant to evaluate the quality of a SVG image regarding the relevance to the given label.'
    
    png_path = 'gpt4_5_with_reasoning_png/'
    gpt4o = os.listdir(png_path)

    for i in range(3):
        dest = 'claude_eval_gpt4_5_reasoning_try%d/'%(i)
        os.makedirs(dest, exist_ok=True)
        for fname in gpt4o:
            img = png_path + fname
            label = fname.split('.p')[0]
            prompt = 'Label: %s. Please give a score of 1-10 and the comment of the image with <score> and <comment> in your answer.'%(label)
            answer = sonnet.vision_request(system_prompt, prompt, "image/png", img)
            score, comment = parse_score_comment(answer.content[0].text)
            newfile = label + '__score' + score + '__try%d.txt'%(i)
            
            with open(dest + newfile,'w') as f:
                f.write(comment)
        