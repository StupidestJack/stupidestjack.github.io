import buildpy.markdown as md
import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
from pathlib import Path
import json

def build(post):
    content = ''
    with open(f"posts-md/{post["slug"]}.md",'r') as f:
        content = f.read()
    html = htmlmk.html_template.format(
        f'{post["title"]} | Niugnep 的部落格', # 第一部份：title
        f'''
        {meta.desc.format(post["description"])} 
        {meta.og_title.format(post["title"])}
        {meta.og_desc.format(post["description"])}
        {meta.author}
        {meta.canonical.format(post["slug"])}
        {meta.pub_date.format(post["time"])}
        ''', # 第二部份：metadatas
        f'''
        {ht.header}
        <div id="blog">
            <div id="title-chunk">
                <h1 id="title" class="title">{post["title"]}</h1>
                <span id="time" class="title">{post["time"]}</span>
            </div>
            <div id="content">
                {md.markdown_to_html(content)}
            </div>
        </div>
        <div id="comment">
            <h4>測試版功能：Giscus留言區</h4>
            <script src="https://giscus.app/client.js"
                data-repo="StupidestJack/blog"
                data-repo-id="R_kgDORI815g"
                data-category="Announcements"
                data-category-id="DIC_kwDORI815s4C82_p"
                data-mapping="pathname"
                data-strict="0"
                data-reactions-enabled="1"
                data-emit-metadata="0"
                data-input-position="bottom"
                data-theme="preferred_color_scheme"
                data-lang="zh-TW"
                data-loading="lazy"
                crossorigin="anonymous"
                async></script>
            <br>
        </div>
        {ht.footer}
        ''' # 第三部份：正文
    )
    return html

def get_articles(posts, all):
    articles = ''
    count = len(posts) if all else min(len(posts), 6)

    for i in range(count):
        tags = ""
        
        for j in posts[i]["tags"]:
            tags += f'<span class="tag">{j}</span>'
        article = f'''
        <article class="post-card"><a href="posts/{posts[i]["slug"]}.html">
            <h3>{posts[i]["title"]}</h3>
            <p class="post-time">
                {posts[i]["time"]}
            </p>
            <p class="des">
                {posts[i]["description"]}
            </p>
            <div class="tags">
                {tags}
            </div>
        </a></article>
        '''
        articles += article
    # print(articles)
    return articles

def build_home(posts):
    html = htmlmk.html_template.format(
        "首頁 | Niugnep 的部落格", # 第一部份：title
        f'''
        {meta.desc.format("Niugnep 部落格的首頁")} 
        {meta.og_title.format("Niugnep 的部落格")}
        {meta.og_desc.format("Niugnep 部落格的首頁")}
        {meta.author}
        {meta.pub_date.format("2026-05-12")}
        ''', # 第二部份：metadatas
        f'''
        {ht.header}
        <section class="hero">
            <h1>Niugnep 的部落格</h1>
            <p>
                一個國二生幹話的地方。<br>
                會分享開源資訊、無聊的教學、網路內容跟日常等內容。
            </p>
        </section>

        <section id="posts-list">
            <h2>最新文章</h2>

            <div id="posts-container">
                {get_articles(posts, False)}
            </div>
        </section>
        {ht.footer}
        ''' # 第三部份：正文
    )
    return html

def build_all(posts):
    html = htmlmk.html_template.format(
        "所有文章 | Niugnep 的部落格", # 第一部份：title
        f'''
        {meta.desc.format("Niugnep 部落格的所有文章畫面")} 
        {meta.og_title.format("Niugnep 的部落格")}
        {meta.og_desc.format("Niugnep 部落格的所有文章畫面")}
        {meta.author}
        {meta.pub_date.format("2026-05-12")}
        ''', # 第二部份：metadatas
        f'''
        {ht.header}
        <section class="hero">
            <h1>所有文章</h1>
        </section>

        <section id="posts-list">
            <div id="posts-container">
                {get_articles(posts, True)}
            </div>
        </section>
        {ht.footer}
        ''' # 第三部份：正文
    )
    return html

with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

Path("posts").mkdir(exist_ok=True)
for post in posts:
    try:
        with open(f'posts/{post["slug"]}.html','w',encoding="utf-8") as f:
            f.write(build(post))
    except Exception as e:
        print(f"建置{post["slug"]}失敗...>皿< ({e})")
    else:
        print(f"建置{post["slug"]}成功！>v<")

try:
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(build_home(posts))
except Exception as e:
    print(f"建置index失敗...>皿< ({e})")
else:
    print(f"建置index成功！>v<")

try:
    with open("all.html", "w", encoding="utf-8") as f:
        f.write(build_all(posts))
except Exception as e:
    print(f"建置all失敗...>皿< ({e})")
else:
    print(f"建置all成功！>v<")
