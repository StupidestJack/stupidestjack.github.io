import buildpy.config as conf

html_template = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{}}</title>
    {{}}
    <link rel="icon" href="{conf.icon}" type="image/png">
    <link rel="stylesheet" href="/sty.css">
</head>
<body>
    {{}}
</body>
</html>"""