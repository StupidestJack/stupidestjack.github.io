def markdown_to_html(markdown_text):
    lines = markdown_text.split("\n")
    html = []

    in_code = False
    in_ul = False
    in_table = False

    for line in lines:
        stripped = line.strip()

        # =========================
        # 程式碼區塊 ```
        # =========================
        if stripped.startswith("```"):
            if not in_code:
                html.append("<pre><code>")
                in_code = True
            else:
                html.append("</code></pre>")
                in_code = False
            continue

        if in_code:
            html.append(
                line.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )
            continue

        # =========================
        # 表格
        # =========================
        if "|" in stripped:
            cols = [c.strip() for c in stripped.strip("|").split("|")]

            # 跳過 --- 分隔線
            if all(set(c) <= {"-"} for c in cols):
                continue

            if not in_table:
                html.append("<table border='1'>")
                in_table = True

            html.append("<tr>")
            for col in cols:
                html.append(f"<td>{col}</td>")
            html.append("</tr>")
            continue
        else:
            if in_table:
                html.append("</table>")
                in_table = False

        # =========================
        # 清單 (* 或 -)
        # =========================
        if stripped.startswith("* ") or stripped.startswith("- "):
            if not in_ul:
                html.append("<ul>")
                in_ul = True

            item = stripped[2:]
            html.append(f"<li>{item}</li>")
            continue
        else:
            if in_ul:
                html.append("</ul>")
                in_ul = False

        # =========================
        # 標題
        # =========================
        if stripped.startswith("### "):
            html.append(f"<h3>{stripped[4:]}</h3>")

        elif stripped.startswith("## "):
            html.append(f"<h2>{stripped[3:]}</h2>")

        elif stripped.startswith("# "):
            html.append(f"<h1>{stripped[2:]}</h1>")

        # =========================
        # 粗體
        # =========================
        elif stripped.startswith("**") and stripped.endswith("**"):
            html.append(f"<b>{stripped[2:-2]}</b>")

        # =========================
        # 斜體
        # =========================
        elif stripped.startswith("*") and stripped.endswith("*"):
            html.append(f"<i>{stripped[1:-1]}</i>")

        # =========================
        # 空行
        # =========================
        elif stripped == "":
            html.append("<br>")

        # =========================
        # 一般段落
        # =========================
        else:
            html.append(f"<span>{stripped}</span><br>")

    # 防止沒關閉
    if in_ul:
        html.append("</ul>")

    if in_table:
        html.append("</table>")

    if in_code:
        html.append("</code></pre>")

    return "\n".join(html)


# =========================
# 測試
# =========================

if __name__ == "__main__":
    md = """
    # 標題
    ## 二標題
    ### 三標題
    這是段落
    這是段落
    這是段落
    這是段落

    ## 清單
    * 第一項
    - 第二項

    ## 表格
    | 名字 | 年齡 |
    | --- | --- |
    | 小明 | 14 |
    | 小華 | 15 |

    ## 程式碼
    ```
    print("Hello")
    print("World")
    ```

    ## 嵌入式
    <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ?si=xyC_AbcErwKT9q_2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    """

    result = markdown_to_html(md)
    print(result)