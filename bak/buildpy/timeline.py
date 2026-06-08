import buildpy.htmlmaker as htmlmk
import buildpy.headtail as ht
import buildpy.metadata as meta
import json
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
def make_timeline(timeline):
    articles = ''
    for i in timeline:
        article = f'''
        <article class="tl-card">
            <h3>{i["time"]}</h3>
            <p class="tl-des">
                {i["note"]}
            </p>
        </article>
        '''
        articles += article
    # print(articles)
    return articles

def build_timeline(timeline):
    html = htmlmk.html_template.format(
        '時間軸 | Niugnep 的部落格', # 第一部份：title
        f'''
        {meta.desc.format('由 Niugnep 撰寫的時間軸')} 
        {meta.og_title.format('時間軸 | Niugnep 的部落格')}
        {meta.og_desc.format('由 Niugnep 撰寫的時間軸')}
        {meta.author}
        <link rel="canonical" href="https://stupidestjack.github.io/timeline">
        {meta.pub_date.format(today)}
        ''', # 第二部份：metadatas
        f'''
        {ht.header}
        <div id="timeline">
            {make_timeline(timeline)}
        </div>
        {ht.footer}
        ''' # 第三部份：正文
    )
    return html
