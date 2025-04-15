import os
import json
import re
from models import Deepseek


if __name__ == "__main__":
    
    client = Deepseek("deepseek-chat", "your_api_key")
    
    
    src_dir = "llama_gen_maxNewToken8192_png_claude_eval"
    dst_dir = "llama_gen_maxNewToken8192_ds_inst"

    sys_prompt = "You are an assistant for providing concise instructions given a long context. "
    sys_prompt += "The context are the comments of a VLM to SVG images generated from a small model."

    for model_id in os.listdir(src_dir):
        if not os.path.isdir(os.path.join(src_dir, model_id)):
            continue
        src_model_dir = os.path.join(src_dir, model_id)
        dst_model_dir = os.path.join(dst_dir, model_id)
        os.makedirs(dst_model_dir, exist_ok=True)
        for filename in os.listdir(src_model_dir):
            with open(os.path.join(src_model_dir, filename), "r") as f:
                d = json.load(f)
            score = d["score"]
            comment = d["comment"]
            
            prompt = f"context: score: {score}, comment: {comment}\n\n"
            prompt += "Generate brief instructions in 20 words to guide the small model to generate better SVG image."
            
            answer = client.basic_request(sys_prompt, prompt, stream=False, temperature=1.0)
            # ans = answer['choices'][0]['message']['content']
            ans = answer.choices[0].message.content
            
            res = res.replace("\"", "")
            res = re.sub(r"\(.*?\)", "", res)
            
            d1 = {"score": score, "comment": res}
            
            with open(os.path.join(dst_model_dir, filename), "w") as f:
                json.dump(d1, f, ensure_ascii=False, indent=4)
        