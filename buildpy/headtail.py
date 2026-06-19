import buildpy.config as conf

def get_header(pages=None):
    """
    獲取頁首 HTML，支援傳入 pages 列表以動態生成導覽列連結
    """
    # 預設的基本固定連結
    links = [
        f'<a href="{conf.url}/index.html">首頁</a>',
        f'<a href="{conf.url}/all.html">所有文章</a>',
        f'<a href="{conf.url}/random.html">隨機</a>',
        f'<a href="{conf.url}/timeline">時間軸</a>'
    ]
    
    # 如果有傳入自訂獨立頁面，且設定要在導覽列顯示，就動態加進去
    if pages:
        for page in pages:
            # 同時支援 "on_nvabar" (JSON 裡的拼法) 與標準的 "on_navbar"
            if page.get("on_nvabar") or page.get("on_navbar"):
                slug = page["slug"]
                title = page["title"]
                links.append(f'<a href="/spec/{slug}.html">{title}</a>')
                
    # 將所有連結用換行與縮排組合起來
    links_html = "\n            ".join(links)

    return f"""
<header>
    <div class="logo"><a href="/index.html">{conf.site_title}</a></div>
    <nav class="navbar">
        <input type="checkbox" id="menu-toggle">
        <label for="menu-toggle" class="hamburger">☰</label>
        <div class="nav-links">
            {links_html}
        </div>
    </nav>
</header>
"""

def get_footer():
    return f"""
<footer>
    <p>&copy; {conf.year} {conf.author} | 文章基於 {conf.posts_license} 授權 | <a href="/rss.xml">RSS</a></p>
    <p>Powered by Niugnep's Blog Template</p>
</footer>
"""