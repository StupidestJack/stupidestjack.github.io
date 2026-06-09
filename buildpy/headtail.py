import buildpy.config as conf

def get_header():
    return f"""
<header>
    <div class="logo"><a href="/index.html">{conf.site_title}</a></div>
    <nav class="navbar">
        <input type="checkbox" id="menu-toggle">
        <label for="menu-toggle" class="hamburger">☰</label>
        <div class="nav-links">
            <a href="/index.html">首頁</a>
            <a href="/about.html">關於我</a>
            <a href="/all.html">所有文章</a>
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