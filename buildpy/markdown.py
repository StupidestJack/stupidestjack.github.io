#!/usr/bin/env python3
import re
import html
import sys
import os

def parse_inline(text):
    """
    處理 inline markdown
    """
    text = text.replace("<br>", "__BR__")

    # escape HTML
    text = html.escape(text)

    # 黑話 / 捏他 (spoiler)
    # 這裡使用 \|\| 來匹配 ||
    text = re.sub(
        r"\|\|(.*?)\|\|",
        r'<span class="spo">\1</span>',
        text
    )

    # link
    text = re.sub(
        r"\[(.*?)\]\((.*?)\)",
        r'<a href="\2">\1</a>',
        text
    )

    # 粗體
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )

    # 斜體
    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text
    )

    # 刪除線
    text = re.sub(
        r"~~(.*?)~~",
        r"<s>\1</s>",
        text
    )

    text = text.replace("__BR__", "<br>")
    return text


def markdown_to_html(markdown_text):
    lines = markdown_text.split("\n")
    html_out = []

    in_code = False
    in_ul = False
    in_ol = False
    in_table = False
    in_blockquote = False

    for line in lines:
        stripped = line.strip()

        # =====================================
        # 程式碼區塊
        # =====================================
        if stripped.startswith("```"):
            if not in_code:
                html_out.append("<pre><code>")
                in_code = True
            else:
                html_out.append("</code></pre>")
                in_code = False
            continue

        if in_code:
            html_out.append(
                line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            continue

        # =====================================
        # 原生 HTML
        # =====================================
        if stripped.startswith("<") and stripped.endswith(">"):
            html_out.append(stripped)
            continue

        # =====================================
        # 表格
        # =====================================
        if stripped.startswith("|") and stripped.endswith("|"):
            cols = [
                parse_inline(c.strip())
                for c in stripped.strip("|").split("|")
            ]

            # markdown table separator
            if all(set(c.replace(":", "")) <= {"-"} for c in cols):
                continue

            if not in_table:
                html_out.append("<table border='1'>")
                in_table = True

            html_out.append("<tr>")
            for col in cols:
                html_out.append(f"<td>{col}</td>")
            html_out.append("</tr>")
            continue
        else:
            if in_table:
                html_out.append("</table>")
                in_table = False

        # =====================================
        # blockquote
        # =====================================
        if stripped.startswith(">"):
            if not in_blockquote:
                html_out.append("<blockquote>")
                in_blockquote = True
            html_out.append(
                f"<p>{parse_inline(stripped[1:].strip())}</p>"
            )
            continue
        else:
            if in_blockquote:
                html_out.append("</blockquote>")
                in_blockquote = False

        # =====================================
        # unordered list
        # =====================================
        if stripped.startswith("* ") or stripped.startswith("- "):
            if not in_ul:
                html_out.append("<ul>")
                in_ul = True
            item = parse_inline(stripped[2:])
            html_out.append(f"<li>{item}</li>")
            continue
        else:
            if in_ul:
                html_out.append("</ul>")
                in_ul = False

        # =====================================
        # ordered list
        # =====================================
        if re.match(r"^\d+\.\s", stripped):
            if not in_ol:
                html_out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s", "", stripped)
            html_out.append(
                f"<li>{parse_inline(item)}</li>"
            )
            continue
        else:
            if in_ol:
                html_out.append("</ol>")
                in_ol = False

        # =====================================
        # 標題
        # =====================================
        if stripped.startswith("###### "):
            html_out.append(f"<h6>{parse_inline(stripped[7:])}</h6>")
        elif stripped.startswith("##### "):
            html_out.append(f"<h5>{parse_inline(stripped[6:])}</h5>")
        elif stripped.startswith("#### "):
            html_out.append(f"<h4>{parse_inline(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            html_out.append(f"<h3>{parse_inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html_out.append(f"<h2>{parse_inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html_out.append(f"<h1>{parse_inline(stripped[2:])}</h1>")

        # =====================================
        # hr
        # =====================================
        elif stripped in ["---", "***"]:
            html_out.append("<hr>")

        # =====================================
        # 空行
        # =====================================
        elif stripped == "":
            html_out.append("")

        # =====================================
        # 一般段落
        # =====================================
        else:
            # 順手幫你把結尾的 <p> 改回正確的 </p> 囉！
            html_out.append(f"<p>{parse_inline(stripped)}</p>")

    # =====================================
    # 強制關閉
    # =====================================
    if in_ul: html_out.append("</ul>")
    if in_ol: html_out.append("</ol>")
    if in_table: html_out.append("</table>")
    if in_blockquote: html_out.append("</blockquote>")
    if in_code: html_out.append("</code></pre>")

    return "\n".join(html_out)