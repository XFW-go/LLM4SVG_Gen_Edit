import base64
import os
import re

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

        
def svg_clean(svg_str):
    svg_data = None
    match = re.search(r"<svg[^>]*>.*?</svg>", svg_str, re.DOTALL)
    if match:
        svg_data = match.group(0)
    return svg_data


def parse_score_comment(output):
    raw_score = output.split('<score>')[1].split('</score>')[0]
    comment = output.split('<comment>')[1].split('</comment>')[0]   
    score = int(raw_score.split('/')[0])
    return str(score), comment