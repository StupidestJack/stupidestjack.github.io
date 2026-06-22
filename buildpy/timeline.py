import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
import json
from datetime import datetime
import buildpy.config as conf

today = datetime.now().strftime("%Y-%m-%d")

def make_timeline(timeline_chunk):
    """
    僅渲染傳入的該分頁時間軸資料
    """
    articles = ''
    for i in timeline_chunk:
        article = f'''
        <article class="tl-card">
            <h3>{i["time"]}</h3>
            <p class="tl-des">
                {i["note"]}
            </p>
        </article>
        '''
        articles += article
    return articles

def make_pagination(current_page, total_pages):
    """
    產生分頁導覽的 HTML 與基礎 CSS 樣式
    """
    if total_pages <= 1:
        return ""
    
    links = []
    
    # 1. 上一頁按鈕
    if current_page > 1:
        prev_file = "index.html" if current_page - 2 == 0 else f"page{current_page - 1}.html"
        links.append(f'<a href="{prev_file}" class="tl-page-btn">&laquo; 上一頁</a>')
    else:
        links.append('<span class="tl-page-btn disabled">&laquo; 上一頁</span>')
    
    # 2. 頁碼按鈕
    for p in range(1, total_pages + 1):
        p_file = "index.html" if p == 1 else f"page{p}.html"
        if p == current_page:
            links.append(f'<span class="tl-page-num active">{p}</span>')
        else:
            links.append(f'<a href="{p_file}" class="tl-page-num">{p}</a>')
            
    # 3. 下一頁按鈕
    if current_page < total_pages:
        next_file = f"page{current_page + 1}.html"
        links.append(f'<a href="{next_file}" class="tl-page-btn">下一頁 &raquo;</a>')
    else:
        links.append('<span class="tl-page-btn disabled">下一頁 &raquo;</span>')
        
    pagination_html = f'''
    <div class="tl-pagination">
        {" ".join(links)}
    </div>
    '''
    return pagination_html

def build_timeline_pages(timeline, headpages):
    """
    核心：每 30 篇切成一個分頁，並打包成字典回傳 { "檔名.html": "完整HTML代碼" }
    """
    items_per_page = 30
    total_pages = (len(timeline) + items_per_page - 1) // items_per_page
    if total_pages == 0:
        total_pages = 1
        
    pages = {}
    for page_num in range(1, total_pages + 1):
        # 切片選取這頁的 30 筆資料
        start_idx = (page_num - 1) * items_per_page
        chunk = timeline[start_idx : start_idx + items_per_page]
        
        # 決定檔名與 Canonical 連結路徑
        filename = "index.html" if page_num == 1 else f"page{page_num}.html"
        canonical_suffix = "/timeline/" if page_num == 1 else f"/timeline/page{page_num}.html"
        
        # 如果是分頁，標題後面加上頁數提示
        title_suffix = f" (第 {page_num} 頁)" if page_num > 1 else ""
        
        html = htmlmk.html_template.format(
            f'時間軸{title_suffix} | {conf.site_title}', # 第一部份：title
            f'''
            {meta.desc.format(f'由 {conf.author} 撰寫的時間軸{title_suffix}')} 
            {meta.og_title.format(f'時間軸{title_suffix} | {conf.site_title}')}
            {meta.og_desc.format(f'由 {conf.author} 撰寫的時間軸{title_suffix}')}
            {meta.author}
            <link rel="canonical" href="{conf.url}{canonical_suffix}">
            {meta.pub_date.format(today)}
            ''', # 第二部份：metadatas
            f'''
            {ht.get_header(headpages)}
            <div id="timeline">
                <h1>時間軸</h1>
                <p>這是個比一般文章還要瘋狂的短部落格，</p>
                <p>偶有出言不遜請見諒。</p>
                {make_timeline(chunk)}
                {make_pagination(page_num, total_pages)}
            </div>
            {ht.get_footer()}
            ''' # 第三部份：正文
        )
        pages[filename] = html
        
    return pages

def build_timeline(timeline):
    """
    向下相容方法：若其他程式或舊邏輯呼叫，則直接回傳第一頁 (index.html) 的內容
    """
    pages = build_timeline_pages(timeline)
    return pages.get("index.html", "")