from datetime import datetime
from email.utils import format_datetime
from html import escape

def rss_time(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return format_datetime(dt)

def buildrss(posts):
    rss = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Niugnep 的部落格</title>
    <link>https://stupidestjack.github.io/</link>
    <description>一個國二生幹話的地方</description>
    <language>zh-TW</language>
    <atom:link
        href="https://stupidestjack.github.io/rss.xml"
        rel="self"
        type="application/rss+xml"/>
    '''
    for i in posts:
        rss += f'''
    <item>
        <title>{escape(i["title"])}</title>
        <link>https://stupidestjack.github.io/posts/{i["slug"]}.html</link>
        <guid>https://stupidestjack.github.io/posts/{i["slug"]}.html</guid>
        <description>{escape(i["description"])}</description>
        <pubDate>{rss_time(i["time"])}</pubDate>
        <author>Niugnep Hsueh | niugnep87@proton.me</author>
    </item>'''
    rss += '</channel></rss>'
    return rss 

def buildsm(posts):
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    for i in posts:
        sitemap += f'''
    <url>
        <loc>https://stupidestjack.github.io/posts/{i["slug"]}.html</loc>
        <lastmod>{i["time"]}</lastmod>
    </url>'''

    sitemap += f'''
    <url>
        <loc>https://stupidestjack.github.io/</loc>
        <lastmod>2026-05-12</lastmod>
    </url>'''

    sitemap += f'''
    <url>
        <loc>https://stupidestjack.github.io/all.html</loc>
        <lastmod>2026-05-12</lastmod>
    </url>'''
    sitemap += '</urlset>'
    return sitemap 