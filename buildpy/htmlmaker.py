import config as conf
with open("style.css", "r", encoding="utf-8") as f:
    s = f.read().replace("{", "{{").replace("}", "}}")
html_template = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{}}</title>
    {{}}
    <link rel="icon" href="{conf.icon}" type="image/png">
    <style>{s}</style>
</head>
<body>
<div id="eos"><span>此頁面將停止更新，請轉移到<a href="https://niugnep87.codeberg.page">Codeberg 站點</a></span></div>
    {{}}
</body>
</html>'''
