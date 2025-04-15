import os
import json
os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'
import cairosvg
from PIL import Image
import numpy as np


src_dir = "ds_svgedit"
gt_dir = "SVGEditBench"

def eval(gen, ref):
    g = np.array(gen)
    r = np.array(ref)
    return np.mean(((g - r) / 255) ** 2)


tasks = [
    "1_ChangeColor",
    "2_SetContour",
    "3_Compression",
    "4_UpSideDown",
    "5_Transparency",
    "6_CropToHalf",
]

results = {
    
}

for task in tasks:
    gen_task_dir = os.path.join(src_dir, task)
    gt_task_dir = os.path.join(gt_dir, task, "answer")
    
    gt_files = set(os.listdir(gt_task_dir))
    
    mse_sum0 = sum0 = 0
    mse_sum1 = sum1 = 0
    for filename in gt_files:
        
        with open(os.path.join(gt_task_dir, filename), "r") as f:
            gt_str = f.read()
        
        with open("tmp_gt.png", "bw") as f:
            cairosvg.svg2png(
                url=os.path.join(gt_task_dir, filename),
                # bytestring=gt_str.encode(),
                write_to=f,
                output_width=72,
                output_height=72,
                background_color="#FFFFFF",
            )
        _ref = Image.open("tmp_gt.png").convert('RGB')
            
        try:
            with open(os.path.join(gen_task_dir, filename), "br") as f:
                gen_str = f.read()
            
            with open("tmp_gen.png", "bw") as f:
                cairosvg.svg2png(
                    url=os.path.join(gen_task_dir, filename),
                    # bytestring=gen_str,
                    write_to=f,
                    output_width=72,
                    output_height=72,
                    background_color="#FFFFFF",
                )
                
            _gen = Image.open("tmp_gen.png").convert('RGB')
            res = eval(_gen, _ref)
            mse_sum0 += res
            mse_sum1 += res
            sum0 += 1
            sum1 += 1
            
        except Exception as e:
            if _ref.mode == "RGBA":
                _gen = Image.new('RGBA', _ref.size, (255, 255, 255, 255))
            else:
                _gen = Image.new('RGB', _ref.size, (255, 255, 255))
                
            res = eval(_gen, _ref)
            mse_sum1 += res
            sum1 += 1
    
    results[task] = {
        "sum": sum0,
        "sum_white": sum1,
        "mse": mse_sum0 / sum0,
        "mse_white": mse_sum1 / sum1,
    }
        
with open(os.path.join(src_dir, "ds_edit_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)