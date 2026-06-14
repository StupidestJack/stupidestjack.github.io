import re
import html
from typing import List, Tuple, Dict

# 【修正】：將所有佔位符改為純粹的英數組合 (使用 PLHZ 前綴與 Z 結尾)
# 徹底避免佔位符內的底線 (_) 被 Markdown 的斜體語法誤判破壞
ESCAPE_MAP: Dict[str, Tuple[str, str]] = {
    r'\*': ('PLHZESCAPEASTERISKZ', '*'),
    r'\_': ('PLHZESCAPEUNDERSCOREZ', '_'),
    r'\~': ('PLHZESCAPETILDEZ', '~'),
    r'\|': ('PLHZESCAPEPIPEZ', '|'),
    r'\\': ('PLHZESCAPEBACKSLASHZ', '\\'),
    r'\#': ('PLHZESCAPEHASHZ', '#'),
    r'\`': ('PLHZESCAPEBACKTICKZ', '`'),
    r'\[': ('PLHZESCAPELEFTBRACKETZ', '['),
    r'\]': ('PLHZESCAPERIGHTBRACKETZ', ']'),
    r'\(': ('PLHZESCAPELEFTPARENZ', '('),
    r'\)': ('PLHZESCAPERIGHTPARENZ', ')'),
    r'\+': ('PLHZESCAPEPLUSZ', '+'),
    r'\-': ('PLHZESCAPEMINUSZ', '-'),
    r'\.': ('PLHZESCAPEDOTZ', '.'),
    r'\!': ('PLHZESCAPEEXCLAMATIONZ', '!'),
}

def parse_inline_styles(s: str) -> str:
    """
    解析行內的 Basic Markdown 標記（粗體、斜體、刪除線、雷區/Spoiler）。
    此步驟在 HTML 轉義與純英數佔位符抽離之後安全執行。
    """
    # 雷區/Spoiler標記: ||text|| 轉換為 <span class="spoiler">text</span>
    s = re.sub(r'\|\|(.*?)\|\|', r'<span class="spoiler">\1</span>', s)
    
    # 粗體: **text** 與 __text__
    s = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'__(.*?)__', r'<strong>\1</strong>', s)
    
    # 斜體: *text* 與 _text_
    s = re.sub(r'\*(.*?)\*', r'<em>\1</em>', s)
    s = re.sub(r'_(.*?)_', r'<em>\1</em>', s)
    
    # 刪除線: ~~text~~
    s = re.sub(r'~~(.*?)~~', r'<del>\1</del>', s)
    
    return s

def markdown_to_html(text: str) -> str:
    # 1. 統一換行符號
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 2. 處理反斜線轉義（換成無害的純字母佔位符）
    for esc, (placeholder, _) in ESCAPE_MAP.items():
        text = text.replace(esc, placeholder)
        
    # 3. 抽離並保護「圍欄程式碼區塊」
    code_blocks: List[Tuple[str, str, str]] = []
    def save_code_block(match: re.Match) -> str:
        lang = match.group(1).strip() if match.group(1) else ""
        code_content = match.group(2)
        escaped_code = html.escape(code_content)
        placeholder = f"PLHZBLOCKCODE{len(code_blocks)}Z"
        code_blocks.append((placeholder, lang, escaped_code))
        return placeholder
        
    text = re.sub(r'```([a-zA-Z0-9_\-\+]*)\n([\s\S]*?)\n```', save_code_block, text)
    
    # 4. 抽離並保護「行內程式碼」
    inline_codes: List[Tuple[str, str]] = []
    def save_inline_code(match: re.Match) -> str:
        code_content = match.group(1)
        escaped_code = html.escape(code_content)
        placeholder = f"PLHZINLINECODE{len(inline_codes)}Z"
        inline_codes.append((placeholder, escaped_code))
        return placeholder
        
    text = re.sub(r'`([^`\n]+)`', save_inline_code, text)
    
    # 5. 全域 HTML 轉義
    text = html.escape(text)
    
    # 6. 抽離並保護「圖片」與「超連結」
    images: List[Tuple[str, str]] = []
    def save_image(match: re.Match) -> str:
        alt = match.group(1)
        url = match.group(2)
        placeholder = f"PLHZIMG{len(images)}Z"
        images.append((placeholder, f'<img src="{url}" alt="{alt}" />'))
        return placeholder
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', save_image, text)
    
    links: List[Tuple[str, str]] = []
    def save_link(match: re.Match) -> str:
        link_text = match.group(1)
        url = match.group(2)
        placeholder = f"PLHZLINK{len(links)}Z"
        formatted_text = parse_inline_styles(link_text)
        links.append((placeholder, f'<a href="{url}">{formatted_text}</a>'))
        return placeholder
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', save_link, text)
    
    # 7. 區塊級語法解析
    lines = text.split('\n')
    output_blocks: List[str] = []
    
    current_block_type = None
    current_block_content: List[str] = []
    
    def close_current_block():
        nonlocal current_block_type, current_block_content
        if not current_block_type:
            return
            
        if current_block_type == 'p':
            processed_lines = []
            for item in current_block_content:
                parsed_line = parse_inline_styles(item)
                if item.endswith("  "):
                    processed_lines.append(parsed_line[:-2] + "<br/>")
                else:
                    processed_lines.append(parsed_line)
            content = " ".join(processed_lines)
            output_blocks.append(f"<p>{content}</p>")
            
        elif current_block_type == 'ul':
            list_items = []
            for item in current_block_content:
                list_items.append(f"  <li>{parse_inline_styles(item)}</li>")
            output_blocks.append("<ul>\n" + "\n".join(list_items) + "\n</ul>")
            
        elif current_block_type == 'ol':
            list_items = []
            for item in current_block_content:
                list_items.append(f"  <li>{parse_inline_styles(item)}</li>")
            output_blocks.append("<ol>\n" + "\n".join(list_items) + "\n</ol>")
            
        elif current_block_type == 'blockquote':
            processed_lines = [parse_inline_styles(item) for item in current_block_content]
            content = "<br/>\n  ".join(processed_lines)
            output_blocks.append(f"<blockquote>\n  {content}\n</blockquote>")
            
        current_block_content = []
        current_block_type = None

    for line in lines:
        stripped = line.strip()
        
        # 判斷是否為程式碼區塊的佔位符
        if stripped.startswith("PLHZBLOCKCODE"):
            close_current_block()
            output_blocks.append(stripped)
            continue
            
        if not stripped:
            close_current_block()
            continue
            
        if re.match(r'^ {0,3}(?:-{3,}|\*{3,}|_{3,})$', stripped):
            close_current_block()
            output_blocks.append("<hr />")
            continue
            
        header_match = re.match(r'^ {0,3}(#{1,6})\s+(.*)$', line)
        if header_match:
            close_current_block()
            level = len(header_match.group(1))
            output_blocks.append(f"<h{level}>{parse_inline_styles(header_match.group(2))}</h{level}>")
            continue
            
        if line.startswith('&gt;'):
            content = line[4:].strip()
            if current_block_type != 'blockquote':
                close_current_block()
                current_block_type = 'blockquote'
            current_block_content.append(content)
            continue
            
        ul_match = re.match(r'^ {0,3}[*\-+]\s+(.*)$', line)
        if ul_match:
            if current_block_type != 'ul':
                close_current_block()
                current_block_type = 'ul'
            current_block_content.append(ul_match.group(1))
            continue
            
        ol_match = re.match(r'^ {0,3}\d+\.\s+(.*)$', line)
        if ol_match:
            if current_block_type != 'ol':
                close_current_block()
                current_block_type = 'ol'
            current_block_content.append(ol_match.group(1))
            continue
            
        if current_block_type != 'p':
            close_current_block()
            current_block_type = 'p'
        current_block_content.append(line)
        
    close_current_block()
    result = "\n".join(output_blocks)
    
    # 8. 依序還原所有純英數佔位符
    for placeholder, link_html in links:
        result = result.replace(placeholder, link_html)
        
    for placeholder, img_html in images:
        result = result.replace(placeholder, img_html)
        
    for placeholder, code_html in inline_codes:
        result = result.replace(placeholder, f"<code>{code_html}</code>")
        
    for placeholder, lang, code_html in code_blocks:
        lang_class = f' class="language-{lang}"' if lang else ''
        result = result.replace(placeholder, f'<pre><code{lang_class}>{code_html}</code></pre>')
        
    for _, (placeholder, original) in ESCAPE_MAP.items():
        result = result.replace(placeholder, html.escape(original))
        
    return result

def markdown_to_full_html(text: str, title: str = "Markdown Preview") -> str:
    body_content = markdown_to_html(text)
    # 此處省略了長篇的 HTML 骨架與 CSS，沿用上一版的 <style> 與 <script> 即可
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 4px; }}
        pre {{ background-color: #f4f4f4; padding: 16px; border-radius: 8px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #dfe2e5; color: #6a737d; padding-left: 16px; }}
        .spoiler {{ background-color: #222; color: #222; padding: 2px 6px; border-radius: 4px; cursor: pointer; user-select: none; }}
        .spoiler.revealed {{ background-color: #f0f0f0; color: #d0021b; user-select: text; }}
    </style>
</head>
<body>

{body_content}

<script>
    document.querySelectorAll('.spoiler').forEach(function(el) {{
        el.addEventListener('click', function() {{ this.classList.toggle('revealed'); }});
    }});
</script>
</body>
</html>
"""
    return full_html

# 這下面是我讓AI寫的腦癱文章，可以透過把直接執行markdown.py的輸出結果放進html文件測試，看不下去就別看了
if __name__ == "__main__":
    test_markdown = """
# 奪回你的數位自主權！Linux Mint 21 實戰指南：擺脫微軟監視的極致流暢人生
嗨大家，我是那個每天都在跟編譯器吵架、熱愛開源技術的科技宅老王。
最近微軟的 Windows 11 動作頻頻，各種強推 AI、廣告與隱私搜集政策，簡直把使用者的電腦當成自家的後花園。身為一個對**數位自主權**有著異常執著的開源狂熱者，我今天真的忍不住要來跟大家推坑這款兼具顏值與效能的開源救星 —— **Linux Mint**！
||其實我只是不想被 Windows 11 的 Recall 監視器看光隱私，連半夜偷偷看迷因都被記錄真的太扯了||
如果你一直在考慮要跳槽到 Linux 陣營，卻又害怕指令介面像是駭客任務一樣難懂，那麼請放心，Linux Mint 將會是你的無痛首選。
## 為什麼是 Linux Mint？（對，我就是不推 Ubuntu）
在 Linux 的世界裡，發行版（Distros）百家爭鳴。很多人會推老大哥 Ubuntu，但我偏不。目前的 Ubuntu 強推 Snap 套件格式，啟動慢又佔空間，簡直像是某種__新型態的綑綁銷售__。
相較之下，Linux Mint 堅持保持_乾淨、穩定、不囉唆_的系統體驗。它不搞那些花裡胡哨的商業小動作，完全由社群驅動。
### 桌面環境任你選：三劍客解析
Linux Mint 提供三種官方桌面環境，你可以根據你的硬體老舊程度來選擇：
 * **Cinnamon**：預設推薦！特效華麗且最符合 Windows 使用者的習慣，過渡期幾乎為零。
 *    * **MATE**：走傳統經典路線，極其穩定，老電腦的續航神器。
 *    * **XFCE**：輕量化之王，連十年前的祖傳筆電裝上去都能~~直接升天~~飛速運行。
> 「軟體就像性，免費的更好。」
> —— 林納斯·托瓦茲（Linus Torvalds）
> 這位 Linux 之父的至理名言至今依然適用。數位自主權不只是免費，更是「免於被大科技公司掌控」的真正自由！
> 
## 裝機前的「保命」準備步驟
別急著把你的 Windows 磁區直接格式化，除非你非常有把握。請跟著以下步驟循序漸進：
 1. 備份你硬碟裡的珍貴資料（包括你私藏的迷因與程式碼原始檔）。
 2. 下載官方 ISO 映像檔並製作 USB 啟動碟。
在製作啟動碟時，只要下載好 ISO 檔，
然後用 Rufus 燒錄進隨身碟，重開機狂按 F12 進入 Boot 菜單就行了（這裡故意換行，看看我的 SSG 解析器有沒有正確換行）。
## 第一次開機：終端機不是妖魔鬼怪！
很多人一聽到 Linux 要用命令列就瑟瑟發抖。放輕鬆，Linux Mint 的軟體主管小工具超級好用，幾乎可以讓你一鍵安裝所有常用軟體（例如 Steam、Discord 和 Chrome）。
不過，如果你想裝逼，體驗一下科技宅的快樂，打開終端機輸入這行指令吧：
首先，我們用 neofetch 來看看炫酷的系統資訊（如果沒安裝，等等在代碼區塊教你怎麼裝）：
```bash
# 1. 更新系統的套件索引
sudo apt update && sudo apt upgrade -y

# 2. 安裝一些日常必備開源神器與系統資訊工具
sudo apt install -y curl git neofetch

# 3. 秀出你的 Linux Mint 標誌！
neofetch

```
看著終端機畫面啪啪啪地閃過一堆綠色文字，是不是覺得自己瞬間變成了好萊塢電影裡的頂尖駭客？
||**極度機密：其實我第一次用 Linux 時，連 Vim 怎麼退出都查了半個小時**||
||*這大概是每個 Linux 玩家都經歷過的社倒退歷史*||
## 自製 SSG 解析器語法大考驗（轉義符號測試）
既然這篇文章是要在我剛寫好的靜態網站產生器（SSG）上跑，我必須在內文中故意加入一些轉義符號，來測試我的 Markdown 解析器是不是真的足夠魯棒（Robust）。
在 Markdown 中，如果你想要顯示原樣的符號，就必須用反斜線來轉義：
 * 這是一個原樣的星號：*
 * 這是一個原樣的雷區符號：||
 * 這是一個原樣的反斜線本身：\
如果解析器把上面這些顯示成了奇怪的斜體或隱藏區塊，||**那我的代碼就真的寫得太爛了**||。
## 立即加入開源大家庭！
不要再猶豫了。點擊下方的連結，下載 Linux Mint，給你的老電腦第二次生命吧！
Linux Mint 官方下載頁面
希望這篇碎碎念文章對你有所幫助。我們下次見，願開源力量與你同在！

"""
    full_html_content = markdown_to_full_html(test_markdown)
    print(full_html_content)