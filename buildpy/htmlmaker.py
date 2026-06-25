import buildpy.config as conf
with open("style.css", "r") as f:
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
    {{}}
</body>
</html>'''