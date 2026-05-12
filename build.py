import buildpy.markdown as md
import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
from pathlib import Path
from datetime import datetime
import json

def build(post):
    content = ''
    with open(f"posts-md/{post["slug"]}.md",'r') as f:
        content = f.read()
    # 這下面我自己來

with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

for post in posts:
    with open(f"posts/{post["slug"]}.html",'w',encoding="utf-8") as f:
        f.write(build(post))