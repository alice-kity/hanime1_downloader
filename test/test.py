
import os
import subprocess

def get_html(url:str):
    cmd = f'./lightpanda fetch --dump "{url}"'
    resp=subprocess.getoutput(cmd)
    lines = resp.split("\n")
    for idx, line in enumerate(lines):
        if line.startswith("info") or line.startswith("warning") or "(browser)" in line:
            continue
        else:
            _html = lines[idx:]
            break
    html = "\n".join(_html)
    return html


print(get_html('https://hanime1.me/previews/202505'))
