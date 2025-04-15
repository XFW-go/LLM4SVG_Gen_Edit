from datasets import (
    DatasetInfo, 
    GeneratorBasedBuilder, 
    SplitGenerator, 
    Split, 
    Value
)
from datasets import Dataset
import os
import random


def push_data_obj():
    source_dir = "SVGEdit-20k"
    nums_each_task = 5000
    ds_name = "SVGEdit-30k"
    tasks = [
        "1_ChangeColor",
        "2_SetContour",
        "3_Compression",
        "4_UpSideDown",
        "5_Transparency",
        "6_CropToHalf",
    ]
    data_items = []
    
    inst = "You are an expert SVG graphics generator. You generate clean, valid SVG code according to user instructions."
    max_len = 0
    for task in tasks:
        task_dir = os.path.join(source_dir, task)
        queries = os.listdir(os.path.join(task_dir, "query"))
        queries.sort()
        queries = queries[:nums_each_task]
        for qname in queries:
            name = os.path.splitext(qname)[0]
            with open(os.path.join(task_dir, "query", qname), "r") as f:
                q_txt = f.read()
            
            with open(os.path.join(task_dir, "answer", name + ".svg"), "r") as f:
                a_txt = f.read()
            item = {
                "instruction": inst,
                "input": q_txt,
                "output": a_txt,
                "messages": [
                    {
                        "content": inst + q_txt,
                        "role": "user",
                    }, 
                    {
                        "content": a_txt,
                        "role": "assistant"
                    }
                ]
            }
            data_items.append(item)
            max_len = max(max_len, len(q_txt) + len(inst) + len(a_txt))
            
    print("max_len", max_len)
    random.shuffle(data_items)
    dataset = Dataset.from_list(data_items)
    
    dataset.push_to_hub("XXX/" + ds_name)
    

push_data_obj()