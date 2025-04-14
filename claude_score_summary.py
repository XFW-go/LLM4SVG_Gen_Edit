import os
import json
import pandas as pd
from abc import ABC
import anthropic
from models.Claude import Claude

def comment_summary(label, list_comments, claude):
    system_prompt = 'You are given several user comments about the same image regarding relevance to a given label. Please summarize from these comments into one single concise and coherent comment.\n \
                    The final comment must not exceed 50 words.\n \
                    Preserve important opinions or observations from the original comments.\n \
                    Keep the tone natural and unified.'
    
    ntry = len(list_comments)
    if ntry==1:
        return list_comments[0]
        
    prompts = ['Label: %s\n Comment %d:%s\n'%(label, j, list_comments[j]) for j in range(ntry)]
    prompt = ''.join(prompts)
    answer = claude.comments_summary(system_prompt, prompt)
    
    return answer

def score_calculate(paths):
    nsample = len(os.listdir(paths[0]))
    files = os.listdir(paths[0])
    scores = 0
    for fname in files:
        label = fname.split('__')[0]
        score = int(fname.split('__score')[1].split('__try')[0])
        #print(label, score)
        scores += score
    
    return scores/nsample

def score_comment_summary(paths, claude):
    nsample = len(os.listdir(paths[0]))
    ntry = len(paths)
    output = pd.DataFrame({
        'Label': [],
        'Score': [],
        'Comment': []
    })
    filelists = {}
    for j in range(ntry):
        filelists[paths[j]] = os.listdir(paths[j])
    
    for i in range(nsample):
        fnames = [filelists[paths[j]][i] for j in range(ntry)]
        label = fnames[0].split('__')[0]
        print(label)
        scores = [int(fnames[j].split('__score')[1].split('__try')[0]) for j in range(ntry)]
        score = round(sum(scores)/ntry, 2)
        comments = []
        for j in range(ntry):
            with open(paths[j]+'/'+fnames[j], 'r') as f:
                comment = f.read()
                comments.append(comment)
        final_comment = comment_summary(label, comments, claude)
        
        instance = {'Label':label, 'Score':score, 'Comment':final_comment}
        output.loc[len(output)] = instance
    
    return output
    
    
if __name__ == "__main__":
    sonnet = Claude(model='claude-3-7-sonnet-20250219', api_key="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")
    paths = ['claude_eval_gpt4o_reasoning_try%d'%(j) for j in range(3)]
    average_score = [score_calculate(paths[j]) for j in range(3)]
    print(sum(average_score)/3)
    df = score_comment_summary(paths, sonnet)
    df.to_csv('claude_eval_gpt4o_reasoning.csv', index=False)
    