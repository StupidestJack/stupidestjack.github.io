import buildpy.markdown as md
import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
import buildpy.xmlbuild as xmlb
import buildpy.config as conf
from pathlib import Path
import json

def build_about():
    content = ''
    about_path = Path("posts-md/about.md")
    if not about_path.exists():
        content = "# 關於我\n這裡目前沒有內容，請建立 `posts-md/about.md`！"
    else:
        with open(about_path, 'r', encoding="utf-8") as f:
            content = f.read()
        
    html = htmlmk.html_template.format(
        f'關於我 | {conf.site_title}',
        f'''
        {meta.desc.format(f'關於 {conf.author} 和 {conf.site_title}')} 
        {meta.og_title.format(f'關於我 | {conf.site_title}')}
        {meta.og_desc.format(f'關於 {conf.author} 和 {conf.site_title}')}
        {meta.author}
        <link rel="canonical" href="{conf.url}/about.html">
        {meta.pub_date.format('2026-05-24')}
        ''',
        f'''
        {ht.get_header()}
        <div id="blog">
            <div id="content">
                {md.markdown_to_html(content)}
            </div>
        </div>
        {ht.get_footer()}
        '''
    )
    return html


def build(post):
    content = ''
    with open(f"posts-md/{post['slug']}.md", 'r', encoding="utf-8") as f:
        content = f.read()
        
    giscus_tips_html = conf.giscus_tips.replace("\n", "<br>")
        
    html = htmlmk.html_template.format(
        f'{post["title"]} | {conf.site_title}',
        f'''
        {meta.desc.format(post["description"])} 
        {meta.og_title.format(post["title"])}
        {meta.og_desc.format(post["description"])}
        {meta.author}
        {meta.canonical.format(post['slug'])}
        {meta.pub_date.format(post["time"])}
        ''',
        f'''
        {ht.get_header()}
        <div id="blog">
            <div id="title-chunk">
                <h1 id="title" class="title">{post["title"]}</h1>
                <span id="time" class="title">{post["time"]}</span>
            </div>
            <div id="content">
                {md.markdown_to_html(content)}
                <br>
            </div>
        </div>
        <div id="comment">
            <h4>Giscus留言區</h4>
            <span>{giscus_tips_html}</span>
            <script src="https://giscus.app/client.js"
                    data-repo="{conf.giscus['repo']}"
                    data-repo-id="{conf.giscus['repo_id']}"
                    data-category="{conf.giscus['category']}"
                    data-category-id="{conf.giscus['category_id']}"
                    data-mapping="pathname"
                    data-strict="0"
                    data-reactions-enabled="1"
                    data-emit-metadata="0"
                    data-input-position="bottom"
                    data-theme="{conf.giscus['theme']}"
                    data-lang="zh-TW"
                    crossorigin="anonymous"
                    async>
            </script>
            <br>
        </div>
        {ht.get_footer()}
        '''
    )
    return html

def get_articles(posts, all_posts):
    articles = ''
    count = len(posts) if all_posts else min(len(posts), 6)

    for i in range(count):
        tags = ""
        for j in posts[i]["tags"]:
            tags += f'<span class="tag">{j}</span> '
        article = f'''
        <article class="post-card"><a href="posts/{posts[i]['slug']}.html">
            <h3>{posts[i]["title"]}</h3>
            <p class="post-time">{posts[i]["time"]}</p>
            <p class="des">{posts[i]["description"]}</p>
            <div class="tags">{tags}</div>
        </a></article>
        '''
        articles += article
    return articles

def build_home(posts):
    desc_html = "<br>".join(conf.site_desc)
    
    html = htmlmk.html_template.format(
        f"首頁 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的首頁")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的首頁")}
        {meta.author}
        {meta.pub_date.format("2026-05-12")}
        <meta name="google-site-verification" content="-BsyQE4UmvmmmNQqDf_hvjxk3V9AFHN1nPSElMM7Vs0" />
        <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss.xml">
        ''',
        f'''
        {ht.get_header()}
        <section class="hero">
            <h1>{conf.site_title}</h1>
            <p>{desc_html}</p>
        </section>

        <section id="posts-list">
            <h2>最新文章</h2>
            <div id="posts-container">
                {get_articles(posts, False)}
            </div>
        </section>
        {ht.get_footer()}
        '''
    )
    return html

def build_all(posts):
    html = htmlmk.html_template.format(
        f"所有文章 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的所有文章畫面")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的所有文章畫面")}
        {meta.author}
        {meta.pub_date.format("2026-05-12")}
        ''',
        f'''
        {ht.get_header()}
        <section class="hero">
            <h1>所有文章</h1>
        </section>

        <section id="posts-list">
            <div id="posts-container">
                {get_articles(posts, True)}
            </div>
        </section>
        {ht.get_footer()}
        '''
    )
    return html

def run_build():
    """執行完整建置的進入點"""
    Path("docs/posts").mkdir(parents=True, exist_ok=True)

    if not Path("posts.json").exists():
        print("❌ 錯誤：找不到 posts.json，無法讀取文章列表！")
        return

    with open("posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    posts = sorted(posts, key=lambda x: x["time"], reverse=True)

    # 1. 關於我
    try:
        with open('docs/about.html', 'w', encoding="utf-8") as f:
            f.write(build_about())
    except Exception as e:
        print(f"建置 about 失敗... >皿< ({e})")
    else:
        print("建置 about 成功！ >v<")

    # 2. 各篇文章
    for post in posts:
        try:
            with open(f'docs/posts/{post["slug"]}.html', 'w', encoding="utf-8") as f:
                f.write(build(post))
        except Exception as e:
            print(f"建置 {post['slug']} 失敗... >皿< ({e})")
        else:
            print(f"建置 {post['slug']} 成功！ >v<")

    # 3. 首頁
    try:
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(build_home(posts))
    except Exception as e:
        print(f"建置 index 失敗... >皿< ({e})")
    else:
        print("建置 index 成功！ >v<")

    # 4. 所有文章
    try:
        with open("docs/all.html", "w", encoding="utf-8") as f:
            f.write(build_all(posts))
    except Exception as e:
        print(f"建置 all 失敗... >皿< ({e})")
    else:
        print("建置 all 成功！ >v<")
        
    # 5. Sitemap
    try:
        with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(xmlb.buildsm(posts))
    except Exception as e:
        print(f"建置 sitemap 失敗... >皿< ({e})")
    else:
        print("建置 sitemap 成功！ >v<")

    # 6. RSS
    try:
        with open("docs/rss.xml", "w", encoding="utf-8") as f:
            f.write(xmlb.buildrss(posts))
    except Exception as e:
        print(f"建置 rss 失敗... >皿< ({e})")
    else:
        print("建置 rss 成功！ >v<")

if __name__ == "__main__":
    run_build()

"""
{
    "slug":"install-mint",
    "title":"《成為Linux使用者並在一年內挑戰Arch Linux》02 - 連我媽都能看懂的Linux Mint安裝教學",
    "time":"2026-06-02",
    "description": "Linux Mint的完整安裝教學，但是老嫗能解（未完工）",
    "tags":["Linux","教學","新手"]
}
"""