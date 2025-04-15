from datasets import load_dataset

import os
os.environ['WANDB_DISABLED']="true"


def push_data_1():
    dataset = load_dataset("starvector/text2svg-stack")
    def pre_proc(example):
        desc = example["caption_llava"]
        svg = example["Svg"]
        
        inst = "You are an expert SVG graphics generator. You generate clean, valid SVG code according to user instructions."
        inst += f"Create an SVG image with the following instruction: {desc}"
        output = str(svg)
        
        return {
            "instruction": inst,
            "input": "",
            "output": output,
            "messages": [
                {
                    "content": inst,
                    "role": "user",
                }, 
                {
                    "content": output,
                    "role": "assistant"
                }
            ]
        }

    train_set = dataset["train"].select(range(10000))
    train_set = train_set.map(pre_proc, remove_columns=train_set.column_names)
    train_set.push_to_hub("XXX/text2svg-stack-train-10k")
    
    
push_data_1()

# push_data()
