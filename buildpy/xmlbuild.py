from datetime import datetime
from email.utils import format_datetime
from html import escape
import buildpy.config as conf

def rss_time(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return format_datetime(dt)

def buildrss(posts):
    # 防止 site_desc 為空陣列時噴錯
    description = conf.site_desc[0] if conf.site_desc else conf.site_title
    
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>{escape(conf.site_title)}</title>
    <link>{conf.url}</link>
    <description>{escape(description)}</description>
    <language>zh-TW</language>
    <atom:link href="{conf.url}/rss.xml" rel="self" type="application/rss+xml"/>
    '''
    for i in posts:
        rss += f'''
    <item>
        <title>{escape(i["title"])}</title>
        <link>{conf.url}/posts/{i["slug"]}.html</link>
        <guid>{conf.url}/posts/{i["slug"]}.html</guid>
        <description>{escape(i["description"])}</description>
        <pubDate>{rss_time(i["time"])}</pubDate>
        <author>{escape(conf.author_email)} ({escape(conf.author)})</author>
    </item>'''
    rss += '</channel></rss>'
    return rss 

def buildsm(posts):
    today = datetime.now().strftime("%Y-%m-%d")
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    for i in posts:
        sitemap += f'''
    <url>
        <loc>{conf.url}/posts/{i["slug"]}.html</loc>
        <lastmod>{i["time"]}</lastmod>
    </url>'''

    sitemap += f'''
    <url>
        <loc>{conf.url}/</loc>
        <lastmod>{today}</lastmod>
    </url>
    <url>
        <loc>{conf.url}/all.html</loc>
        <lastmod>{today}</lastmod>
    </url>
</urlset>'''
    return sitemap