# 哥們冷靜，AI寫的
import re
import html
from typing import List, Tuple, Dict

# 將所有佔位符改為純粹的英數組合 (使用 PLHZ 前綴與 Z 結尾)
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

def is_delimiter_row(l: str) -> bool:
    """
    檢查此行是否為 Markdown 表格的分隔對齊線 (例如 |:---:|:---|)
    """
    stripped = l.strip()
    if not stripped:
        return False
    # 只允許含有 | : - 還有空格的組合
    cleaned = re.sub(r'[|:\-\s]', '', stripped)
    if cleaned != '':
        return False
    # 分隔線中必須至少包含一個破折號 '-'
    if '-' not in stripped:
        return False
    return True

def parse_table_row(row_str: str, tag: str, alignments: List[str]) -> str:
    """
    解析表格的單行 (Header 或 Body cell)，並根據 alignment 套用文字對齊樣式
    """
    stripped = row_str.strip()
    if stripped.startswith('|'):
        stripped = stripped[1:]
    if stripped.endswith('|'):
        stripped = stripped[:-1]
        
    cells = stripped.split('|')
    
    row_html = ["  <tr>"]
    for idx, cell in enumerate(cells):
        cell_content = parse_inline_styles(cell.strip())
        align_attr = ""
        if idx < len(alignments) and alignments[idx]:
            align_attr = f' style="text-align: {alignments[idx]};"'
            
        row_html.append(f'    <{tag}{align_attr}>{cell_content}</{tag}>')
    row_html.append("  </tr>")
    return "\n".join(row_html)

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
    
    # 4.5. 抽離並保護原始 HTML 的換行標記 <br> 或 <br/> 
    # 避免其被後續的 html.escape 轉義成純文字 &lt;br&gt;
    text = re.sub(r'<br\s*/?>', 'PLHZBRTAGZ', text, flags=re.IGNORECASE)
    
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
                # 同時支援「雙空格」或「單反斜線 \」作為 Markdown 的換行機制
                if item.endswith("  "):
                    processed_lines.append(parsed_line[:-2] + "<br/>")
                elif item.endswith("\\"):
                    # 如果原行結尾是反斜線，需要將其去掉並補上換行符
                    if parsed_line.endswith("\\"):
                        processed_lines.append(parsed_line[:-1] + "<br/>")
                    else:
                        processed_lines.append(parsed_line + "<br/>")
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
            # 【修正】：移除尾部多餘的空白行，避免結尾出現多餘的換行/br標記
            while current_block_content and not current_block_content[-1].strip():
                current_block_content.pop()
                
            # 【修正】：將內容依照空引言行拆分為多個段落 (Paragraphs)
            paragraphs = []
            current_para = []
            for item in current_block_content:
                if not item.strip():
                    if current_para:
                        paragraphs.append(current_para)
                        current_para = []
                else:
                    current_para.append(item)
            if current_para:
                paragraphs.append(current_para)
                
            # 解析並轉譯各段落
            rendered_paras = []
            for para in paragraphs:
                processed_lines = []
                for item in para:
                    parsed_line = parse_inline_styles(item)
                    if item.endswith("  "):
                        processed_lines.append(parsed_line[:-2] + "<br/>")
                    elif item.endswith("\\"):
                        if parsed_line.endswith("\\"):
                            processed_lines.append(parsed_line[:-1] + "<br/>")
                        else:
                            processed_lines.append(parsed_line + "<br/>")
                    else:
                        processed_lines.append(parsed_line)
                rendered_paras.append("<br/>\n  ".join(processed_lines))
                
            # 套用語意化 HTML，多段落包裹為 <p>，單段落則乾淨呈現
            if len(rendered_paras) > 1:
                content = "\n  ".join([f"<p>{p}</p>" for p in rendered_paras])
            elif len(rendered_paras) == 1:
                content = f"<p>{rendered_paras[0]}</p>"
            else:
                content = ""
                
            output_blocks.append(f"<blockquote>\n  {content}\n</blockquote>")
            
        current_block_content = []
        current_block_type = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 判斷是否為程式碼區塊的佔位符
        if stripped.startswith("PLHZBLOCKCODE"):
            close_current_block()
            output_blocks.append(stripped)
            i += 1
            continue
            
        if not stripped:
            close_current_block()
            i += 1
            continue
            
        if re.match(r'^ {0,3}(?:-{3,}|\*{3,}|_{3,})$', stripped):
            close_current_block()
            output_blocks.append("<hr />")
            i += 1
            continue
            
        header_match = re.match(r'^ {0,3}(#{1,6})\s+(.*)$', line)
        if header_match:
            close_current_block()
            level = len(header_match.group(1))
            output_blocks.append(f"<h{level}>{parse_inline_styles(header_match.group(2))}</h{level}>")
            i += 1
            continue
            
        # 【修正】：使用正規表示式取代老舊的 startswith 邏輯
        # 支援 0~3 個前導空格，並可精準抽取 > 後方的一個非強制的空格或縮排
        bq_match = re.match(r'^ {0,3}&gt;([ \t]?)(.*)$', line)
        if bq_match:
            content = bq_match.group(2)
            if current_block_type != 'blockquote':
                close_current_block()
                current_block_type = 'blockquote'
            current_block_content.append(content)
            i += 1
            continue
            
        ul_match = re.match(r'^ {0,3}[*\-+]\s+(.*)$', line)
        if ul_match:
            if current_block_type != 'ul':
                close_current_block()
                current_block_type = 'ul'
            current_block_content.append(ul_match.group(1))
            i += 1
            continue
            
        ol_match = re.match(r'^ {0,3}\d+\.\s+(.*)$', line)
        if ol_match:
            if current_block_type != 'ol':
                close_current_block()
                current_block_type = 'ol'
            current_block_content.append(ol_match.group(1))
            i += 1
            continue

        # Markdown 表格解析邏輯 (Lookahead)
        if '|' in line and (i + 1) < len(lines):
            next_line = lines[i + 1]
            if '|' in next_line and is_delimiter_row(next_line):
                close_current_block() # 清空當前可能有段落的區塊
                
                # 1. 解析分隔對齊設定
                raw_aligns = next_line.strip().strip('|').split('|')
                alignments = []
                for cell in raw_aligns:
                    cell_str = cell.strip()
                    if cell_str.startswith(':') and cell_str.endswith(':'):
                        alignments.append('center')
                    elif cell_str.endswith(':'):
                        alignments.append('right')
                    elif cell_str.startswith(':'):
                        alignments.append('left')
                    else:
                        alignments.append('')
                
                # 2. 處理表頭 Header Row
                header_html = parse_table_row(line, 'th', alignments)
                
                table_rows = []
                table_rows.append("<thead>")
                table_rows.append(header_html)
                table_rows.append("</thead>")
                table_rows.append("<tbody>")
                
                # 跳過表頭與分隔線，準備處理 Body 資料列
                i += 2
                
                # 3. 持續讀取直到非表格列為止
                while i < len(lines):
                    r_line = lines[i]
                    r_stripped = r_line.strip()
                    
                    # 若遇到空行、新標題、或新程式碼區塊則終止表格
                    if not r_stripped:
                        break
                    if (r_stripped.startswith("PLHZBLOCKCODE") or 
                        re.match(r'^ {0,3}(?:-{3,}|\*{3,}|_{3,})$', r_stripped) or
                        re.match(r'^ {0,3}(#{1,6})\s+', r_line) or
                        r_line.startswith('&gt;')):
                        break
                    if '|' not in r_line:
                        break
                        
                    row_html = parse_table_row(r_line, 'td', alignments)
                    table_rows.append(row_html)
                    i += 1
                    
                table_rows.append("</tbody>")
                
                # 合併輸出表格 HTML 區塊
                table_html = "<table>\n" + "\n".join(table_rows) + "\n</table>"
                output_blocks.append(table_html)
                continue
            
        if current_block_type != 'p':
            close_current_block()
            current_block_type = 'p'
        current_block_content.append(line)
        i += 1
        
    close_current_block()
    result = "\n".join(output_blocks)
    
    # 8. 依序還原所有純英數佔位符
    result = result.replace('PLHZBRTAGZ', '<br />') # 優先還原 HTML 換行標記
    
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
    # 更新內建 CSS 以支援現代美觀的表格與引言段落排版樣式
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        pre {{ background-color: #f4f4f4; padding: 16px; border-radius: 8px; overflow-x: auto; }}
        
        /* 引言現代化與多段落排版樣式 */
        blockquote {{ border-left: 4px solid #dfe2e5; color: #6a737d; padding-left: 16px; margin-left: 0; background-color: #f8f9fa; padding: 12px 16px; border-radius: 0 8px 8px 0; }}
        blockquote p {{ margin: 0 0 8px 0; }}
        blockquote p:last-child {{ margin-bottom: 0; }}
        
        .spoiler {{ background-color: #222; color: #222; padding: 2px 6px; border-radius: 4px; cursor: pointer; user-select: none; }}
        .spoiler.revealed {{ background-color: #f0f0f0; color: #d0021b; user-select: text; }}
        
        /* 表格現代化樣式 */
        table {{ border-collapse: collapse; width: 100%; margin: 24px 0; font-size: 0.95em; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        th, td {{ border: 1px solid #dfe2e5; padding: 12px 15px; text-align: left; }}
        th {{ background-color: #f6f8fa; font-weight: 600; color: #24292e; }}
        tr:nth-child(even) {{ background-color: #f8f9fa; }}
        tr:hover {{ background-color: #f1f3f5; }}
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

if __name__ == "__main__":
    test_markdown = """
# 奪回你的數位自主權！Linux Mint 21 實戰指南：擺脫微軟監視的極致流暢人生
嗨大家，我是那個每天都在跟編譯器吵架、熱愛開源技術的科技宅老王。
最近微軟的 Windows 11 動作頻頻，各種強推 AI、廣告與隱私搜集政策，簡真把使用者的電腦當成自家的後花園。身為一個對**數位自主權**有著異常執著的開源狂熱者，我今天真的忍不住要來跟大家推坑這款兼具顏值與效能的開源救星 —— **Linux Mint**！
||其實我只是不想被 Windows 11 的 Recall 監視器看光隱私，連半夜偷偷看迷因都被記錄真的太扯了||
如果你一直在考慮要跳槽到 Linux 陣營，卻又害怕指令介面像是駭客任務一樣難懂，那麼請放心，Linux Mint 將會是你的無痛首選。

## 【新功能測試 1】Markdown 美化表格測試
我們來看看這個新寫好的解析器是否能成功建立表格與對齊功能：

| 發行版名稱 | 開源協議 | 推薦指數 | 主要優點 |
| :--- | :---: | ---: | :--- |
| **Linux Mint** | GPL-2.0 | ⭐⭐⭐⭐⭐ | 乾淨、不耍流氓、介面最親切 |
| **Ubuntu** | GPL-2.0 | ⭐⭐⭐ | snap 機制拖慢速度，稍嫌笨重 |
| **Windows 11** | 專有商業 | ⭐ | 廣告一堆、隱私被看光光 |

## 【新功能測試 2】多重換行 <br> 與 Markdown 斷行大考驗
* **方式 A（行尾雙空格換行）**：  
  第一行後半部分（有雙空格）  
  第二行起點
* **方式 B（行尾反斜線符號）**：\
  第一行後半部分（有反斜線）\
  第二行起點
* **方式 C（嵌入 HTML `<br>` 原始碼）**：<br>第一行文字<br/>第二行文字（甚至混合大寫 <BR> 依然有效）

## 為什麼是 Linux Mint？（對，我就是不推 Ubuntu）
在 Linux 的世界裡，發行版（Distros）百家鳴。很多人會推老大哥 Ubuntu，但我偏不。目前的 Ubuntu 強推 Snap 套件格式，啟動慢又佔空間，簡直像是某種__新型態的綑綁銷售__。
相較之下，Linux Mint 堅持保持_乾淨、穩定、不囉唆_的系統體驗。它不搞那些花裡胡哨的商業小動作，完全由社群驅動。

### 桌面環境任你選：三劍客解析
Linux Mint 提供三種官方桌面環境，你可以根據你的硬體老舊程度來選擇：
 * **Cinnamon**：預設推薦！特效華麗且最符合 Windows 使用者的習慣，過渡期幾乎為零。
 * * **MATE**：走傳統經典路線，極其穩定，老電腦的續航神器。
 * * **XFCE**：輕量化之王，連十年前的祖傳筆電裝上去都能~~直接升天~~飛速運行。
> 「軟體就像性，免費的更好。」
> —— 林納斯·托瓦茲（Linus Torvalds）
> 
> 這位 Linux 之父的至理名言至今依然適用。數位自主權不只是免費，更是「免於被大科技公司掌控」的真正自由！
> 
## 裝機前的「保命」準備步驟
別急著把你的 Windows 磁區直接格式化，除非你非常有把握。請跟著以下步驟進：
 1. 備份你硬碟裡的珍貴資料（包括你私藏的迷因與程式碼原始檔）。
 2. 下載官方 ISO 映像檔並製作 USB 啟動碟。
在製作啟動碟時，只要下載好 ISO 檔，
然後用 Rufus 燒錄進隨身碟，重開機狂按 F12 進入 Boot 菜單就行了。
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
 * 這是一個原樣的星號：\*
 * 這是一個原樣的雷區符號：\|\|
 * 這是一個原樣的反斜線本身：\\
如果解析器把上面這些顯示成了奇怪的斜體或隱藏區塊，||**那我的代碼就真的寫得太爛了**||。
## 立即加入開源大家庭！
不要再猶豫了。點擊下方的連結，下載 Linux Mint，給你的老電腦第二次生命吧！
[Linux Mint 官方下載頁面](https://linuxmint.com/)

希望這篇碎碎念文章對你有所幫助。我們下次見，願開源力量與你同在！

"""
    full_html_content = markdown_to_full_html(test_markdown)
    print(full_html_content)