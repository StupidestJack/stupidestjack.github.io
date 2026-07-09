import buildpy.markdown as md
import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
import buildpy.xmlbuild as xmlb
import config as conf
from pathlib import Path
from datetime import datetime
import json
import subprocess
import shutil

now = datetime.now()

def buildspec(pages):
    for page in pages:
        slug = page["slug"]
        title = page["title"]
        desc = page.get("desc") or page.get("description") or ""
        
        # 處理動態時間 TODAY
        time_str = page.get("time", "2026-01-01")
        if time_str.upper() == "TODAY":
            time_str = now.strftime("%Y-%m-%d")

        # 讀取 Markdown 內容
        page_path = Path(f"posts-md/spec/{slug}.md")
        if not page_path.exists():
            content = f"# {title}\n這裡目前沒有內容，請建立 `posts-md/spec/{slug}.md`！"
        else:
            with open(page_path, 'r', encoding="utf-8") as f:
                file_content = f.read()
            
            # 聰明防呆：如果 Markdown 內容開頭沒有大標題 (#)，自動幫忙補上，省去手寫麻煩
            if not file_content.strip().startswith("#"):
                content = f"# {title}\n\n{file_content}"
            else:
                content = file_content

        # 轉譯 HTML
        html = htmlmk.html_template.format(
            f'{title} | {conf.site_title}',
            f'''
            {meta.desc.format(desc)} 
            {meta.og_title.format(f'{title} | {conf.site_title}')}
            {meta.og_desc.format(desc)}
            {meta.author}
            <link rel="canonical" href="{conf.url}/{slug}.html">
            {meta.pub_date.format(time_str)}
            ''',
            f'''
            {ht.get_header(pages)}
            <div id="blog">
                <div id="content">
                    {md.markdown_to_html(content)}
                    <br>
                </div>
            </div>
            {ht.get_footer()}
            '''
        )
        
        # 寫入目標檔案
        with open(f'docs/spec/{slug}.html', 'w', encoding="utf-8") as f:
            f.write(html)
        print(f"  └─ 特殊頁面 {slug}.html 建置成功！ >v<")


def build(post, pages):
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
        {ht.get_header(pages)}
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

def build_home(posts, pages):
    desc_html = "<br>".join(conf.site_desc)
    
    if conf.index_is_spec:
        with open("posts-md/spec/index.md", "r", encoding="utf-8") as f:
            page = f.read()

    html = htmlmk.html_template.format(
        f"首頁 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的首頁")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的首頁")}
        {meta.author}
        {meta.pub_date.format(now.strftime("%Y-%m-%d"))}
        <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss.xml">
        ''',
        f'''
        {ht.get_header(pages)}
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
    ) if not conf.index_is_spec else htmlmk.html_template.format(
        f"首頁 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的首頁")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的首頁")}
        {meta.author}
        {meta.pub_date.format(now.strftime("%Y-%m-%d"))}
        <link rel="alternate" type="application/rss+xml" title="RSS" href="/rss.xml">
        ''',
        f'''
        {ht.get_header(pages)}
        <div id="home-post">
            {md.markdown_to_html(page)}
        </div>
        {ht.get_footer()}
        '''
    )
    return html

def build_all(posts, pages):
    html = htmlmk.html_template.format(
        f"所有文章 | {conf.site_title}",
        f'''
        {meta.desc.format(f"{conf.site_title}的所有文章畫面")} 
        {meta.og_title.format(conf.site_title)}
        {meta.og_desc.format(f"{conf.site_title}的所有文章畫面")}
        {meta.author}
        {meta.pub_date.format(now.strftime("%Y-%m-%d"))}
        ''',
        f'''
        {ht.get_header(pages)}
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

def build_404(pages):
    html = htmlmk.html_template.format(
        f"找不到此頁面 | {conf.site_title}",
        f'''
        ''',
        f'''
        {ht.get_header(pages)}
        <section class="hero">
            <h1>迷路的旅行者，您在找什麼呢？</h1>
        </section>
        <div id="err404" style="text-align: center;">
            <h2>Error 404，網頁不見了。</h2>
            <p>此處乃虛無之地，無任何可留戀之處。</p>
            <p>此地附近有數個傳送之門，或許您需要這個。</p>
            <div id="blog">
                <h2>傳送之門</h2>
                <a href="/index.html">首頁</a>
                <a href="/about.html">關於我</a>
                <a href="/all.html">所有文章</a>
                <a href="/timeline">時間軸</a><br>
                <a href="https://github.com/StupidestJack/stupidestjack.github.io/issues">質問此世之神(GitHub Issues)</a>
                <br><br>
            </div>
        </div>
        {ht.get_footer()}
        '''
    )
    return html

def build_random(posts, pages):
    slugs = [post["slug"] for post in posts]
    slugs_json = json.dumps(slugs)
    
    html = htmlmk.html_template.format(
        f'隨機文章 | {conf.site_title}',
        f'''
        {meta.desc.format(f'隨機挑選一篇 {conf.author} 的文章閱讀')} 
        {meta.og_title.format(f'隨機文章 | {conf.site_title}')}
        {meta.og_desc.format(f'隨機挑選一篇 {conf.author} 的文章閱讀')}
        {meta.author}
        <link rel="canonical" href="{conf.url}/random.html">
        {meta.pub_date.format(now.strftime("%Y-%m-%d"))}
        ''',
        f'''
        {ht.get_header(pages)}
        <div id="blog" style="text-align: center; padding: 100px 20px;">
            <div id="content">
                <h2 style="font-size: 1.8rem; margin-bottom: 15px;">正在挑選隨機文章...</h2>
                <p style="color: #666; font-size: 1rem;">
                    如果瀏覽器沒有自動跳轉，請點擊 <a id="redirect-link" href="/index.html" style="color: #007acc; text-decoration: underline;">這裡</a>回到首頁。
                </p>
            </div>
        </div>
        
        <script>
            const posts = {slugs_json};
            if (posts && posts.length > 0) {{
                const randomSlug = posts[Math.floor(Math.random() * posts.length)];
                const targetUrl = "/posts/" + randomSlug + ".html";
                document.getElementById("redirect-link").href = targetUrl;
                window.location.replace(targetUrl);
            }} else {{
                window.location.replace("/index.html");
            }}
        </script>
        {ht.get_footer()}
        '''
    )
    return html

def run_build():
    """執行完整建置的進入點"""
    Path("docs/posts").mkdir(parents=True, exist_ok=True)
    Path("docs/spec").mkdir(parents=True, exist_ok=True)
    success = True

    if not Path("posts.json").exists():
        print("錯誤：找不到 posts.json，無法讀取文章列表！")
        return False

    if not Path("pages.json").exists():
        print("錯誤：找不到 pages.json，無法讀取獨立頁面列表！")
        return False

    with open("posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    with open("pages.json", "r", encoding="utf-8") as f:
        pages = json.load(f)

    posts = sorted(posts, key=lambda x: x["time"], reverse=True)

    # 1. 執行 spec 特殊頁面動態生成
    try:
        print("開始建置特殊獨立頁面...")
        buildspec(pages)
    except Exception as e:
        print(f"建置 spec 失敗... >皿< ({e})")
        success = False
    else:
        print("所有 spec 特殊頁面建置完成！ >v<")

    # 2. 各篇文章
    for post in posts:
        try:
            with open(f'docs/posts/{post["slug"]}.html', 'w', encoding="utf-8") as f:
                f.write(build(post, pages))
        except Exception as e:
            print(f"建置 {post['slug']} 失敗... >皿< ({e})")
            success = False
        else:
            print(f"建置 {post['slug']} 成功！ >v<")

    # 3. 首頁
    try:
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(build_home(posts, pages))
    except Exception as e:
        print(f"建置 index 失敗... >皿< ({e})")
        success = False
    else:
        print("建置 index 成功！ >v<")

    # 4. 所有文章
    try:
        with open("docs/all.html", "w", encoding="utf-8") as f:
            f.write(build_all(posts, pages))
    except Exception as e:
        print(f"建置 all 失敗... >皿< ({e})")
        success = False
    else:
        print("建置 all 成功！ >v<")
        
    # 5. Sitemap
    try:
        with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(xmlb.buildsm(posts))
    except Exception as e:
        print(f"建置 sitemap 失敗... >皿< ({e})")
        success = False
    else:
        print("建置 sitemap 成功！ >v<")

    # 6. RSS
    try:
        with open("docs/rss.xml", "w", encoding="utf-8") as f:
            f.write(xmlb.buildrss(posts))
    except Exception as e:
        print(f"建置 rss 失敗... >皿< ({e})")
        success = False
    else:
        print("建置 rss 成功！ >v<")

    # 7. 404 頁面
    try:
        with open("docs/404.html", "w", encoding="utf-8") as f:
            f.write(build_404(pages))
    except Exception as e:
        print(f"建置 404 失敗... >皿< ({e})")
        success = False
    else:
        print("建置 404 成功！ >v<")

    # 8. 隨機文章頁面
    try:
        with open("docs/random.html", "w", encoding="utf-8") as f:
            f.write(build_random(posts, pages))
    except Exception as e:
        print(f"建置 random 失敗... >皿< ({e})")
        success = False
    else:
        print("建置 random 成功！ >v<")
    
    return success

def popen(cmd, cwd=None):
    """執行終端機指令的輔助函式"""
    # ✨ 關鍵：移除 text=True，直接加上 encoding="utf-8"
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"執行失敗: {cmd}\n錯誤訊息: {result.stderr}")
        return False
    return True

if __name__ == "__main__":
    if conf.deploy_to_pages_branch and run_build():
        temp_dir = Path("../blog_temp_deploy")
        docs_dir = Path("docs")
        
        if not docs_dir.exists():
            print("找不到 docs/ 資料夾，請確認建置是否成功。")
            exit()
            
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        shutil.copytree(docs_dir, temp_dir)
            
        print("提交 main 內容...")
        popen("git add .")
        
        # 【優化 2】防呆機制：如果直接按 Enter 沒輸入訊息，自動補上預設時間訊息
        user_msg = input("請輸入 git 提交訊息: ").strip()
        if not user_msg:
            user_msg = f"Automated deploy via build.py at {now.strftime('%Y-%m-%d %H:%M')}"
            
        popen(f'git commit -m "{user_msg}"')
        popen("git push origin main")

        print("切換到 pages 分支...")
        if not popen("git checkout pages"):
            print("嘗試建立 pages 分支...")
            if not popen("git checkout -b pages"):
                exit()
        
        print("清除 pages 分支的文件...")
        for item in Path(".").iterdir():
            if item.name != ".git" and item.name != "node_modules": # 依需求排除
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        
        print("加入 pages 分支的文件...")
        for item in temp_dir.iterdir():
            shutil.move(str(item), ".")
            
        # 【優化 1】搬移完成後，順手把專案外層的暫存資料夾刪除，保持電腦乾淨
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        
        print("提交 pages 內容...")
        popen("git add .")
        
        # 【優化 2】防呆機制：如果直接按 Enter 沒輸入訊息，自動補上預設時間訊息
        user_msg = input("請輸入 git 提交訊息: ").strip()
        if not user_msg:
            user_msg = f"Automated deploy via build.py at {now.strftime('%Y-%m-%d %H:%M')}"
            
        popen(f'git commit -m "{user_msg}"')
        popen("git push origin pages")
        
        print("切換回 main 分支...")
        popen("git checkout main")
        print("🎉 部署成功！大功告成！ >v<")