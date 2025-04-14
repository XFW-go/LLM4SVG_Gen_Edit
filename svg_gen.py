from openai import OpenAI
from PIL import Image
import pandas as pd
import base64
import requests
import os
import json
import re
from abc import ABC
import time
from utils import encode_image, svg_clean
from models.OpenAI import GPT


if __name__ == "__main__":
    gpt4o = GPT(model='gpt-4o', api_key="Your OpenAI API Key")
    # SVG Generation part 
    system_prompt = 'You are an expert SVG graphics generator. You generate clean, valid SVG code according to user instructions.'
    
    with open("data/sketchy_svgs/labels.json", "r") as f:
        labels = json.load(f)
    #comments = pd.read_csv('claude_eval_gpt4o_sketchy.csv')
    
    output = {}
    outdir = 'output-4o_with_reasoning'
    os.makedirs(outdir, exist_ok=True)
    
    begin = time.time()
    for i in range(125):
        label = labels[str(i)]
        print(label)
        
        # Original prompt
        #txt_prompt = 'Create a nice-looking SVG image which can be described by the following label: {%s}'%(label)
        
        # If comments are available for reference
        #comment = comments[comments['Label']==label]['Comment']
        #txt_prompt = 'Create a nice-looking SVG image of the following object: {%s}.\n Some comments to your previously generated SVG image:{%s}.\n Now please create the SVG image.'%(label, comment)
        
        # If score is above the threshold, no need to re-generate 
        #score = float(comments[comments['Label']==label]['Score'])
        #if score >= 7:
        #    continue
        
        # Reasoning prompt. (First reasoning about the object, then generate)
        txt_prompt = 'Think step by step of the feature about the object {%s}.\n Then create a nice-looking SVG image which can be described by the following label: {%s}.'%(label, label)
        
        answer = gpt4o.basic_request(system_prompt, txt_prompt)
        ans = answer['choices'][0]['message']['content']
        
        svg_output = svg_clean(ans)
        output[label] = svg_output
    end = time.time()
    # Calculate time for generation
    print(end-begin)
    
    #with open('output-4o_with_reasoning.json', 'w') as f:
    #    json.dump(output, f, indent=4)
    
    for key in output.keys():
        with open(outdir+'/'+key+'.svg', 'w') as fout:
            fout.write(output[key])

    '''
    # SVG Edit part
    system_prompt = 'You are an assistant for SVG edit task.'
    repo = 'SVGEditBench'
    tasks = [
        "1_ChangeColor",
        "2_SetContour",
        "3_Compression",
        "4_UpSideDown",
        "5_Transparency",
        "6_CropToHalf",
    ]
    output_prefix = 'gpt4o_svgedit'
    os.makedirs(output_prefix, exist_ok=True)
    
    for task in tasks:
        print(task)
        query_file = os.path.join(repo,task,'query')
        queries = os.listdir(query_file)
        output_dir = os.path.join(output_prefix, task)
        os.makedirs(output_dir, exist_ok=True)
        
        for query in queries:
            with open(os.path.join(query_file, query), 'r') as f:
                txt_prompt = f.read()
                answer = gpt4o.basic_request(system_prompt, txt_prompt)
                ans = answer['choices'][0]['message']['content']
                svg_output = svg_clean(ans)
                with open(output_dir+'/'+query.replace('.txt','.svg'),'w') as fout:
                    fout.write(svg_output)
    '''