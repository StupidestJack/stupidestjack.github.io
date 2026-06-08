講真話我不知道為啥，我偏偏要寫一個自己的SSG。

## SSG是什麼？能吃嗎
~~不能吃但很好吃。~~
SSG，全名Static Site Generator，
翻譯即為靜態網站生成器。
靜態網站指的是幾乎不依賴JavaScript腳本，
就能顯示內容的網站，比如我說過很喜歡的[Ivon](ivonblog.com)，
他的部落格就是用SSG生成，讓不使用JS的使用者也能閱讀。

## 那為啥你說不知道為啥偏偏自己寫？
因為SSG這玩意其實市面上一堆。
我個人一方面希望部落格按自己的方式寫，
另一方面我幾乎沒用過任何SSG。
這裡讓AI舉了幾個例子：
 * Jekyll
 * Hugo
 * VitePress
其實我也只有用Jekyll，
用自己的腳本生成完再丟給GitHub生一次Pages才能看，
窮啊，誰叫Pages那麼香，一毛不花就能架網站。
但Jekyll不符合我要求啊，我有sitemap、rss什麼的。

## 寫了哪些檔案？
這些吧，應該算簡潔了。
 * headtail.py：建立頁首跟頁尾
 * htmlmaker.py：填空題，配合format建立各個網頁
 * markdown.py：讓AI寫的MD轉HTML，<br>不用markdown模組是為了在不同裝置上使用
 * metadata.py：就是網站一大堆Metadatas的生成器
 * timeline.py：建置我的動態牆
 * xmlbuild.py：建置sitemap跟rss
 * build.py：充其量就是拼積木
沒啦awa
是不是很簡潔呢（自肥）

## 有哪些坑？
超多啊
 - AI寫的MD生成器缺斤少兩，應該是指令沒下對
 - 單雙引號不能亂用（ex. `f"在雙引號裡的format{i["再套雙引號"]}"` 會讓Actions爆炸）
 - htmlmaker要記得怎麼拼接
 - 要能看懂哪裡出錯
這專案重建到現在三天四十個commits，
其實也挺離譜的。


~~順帶一題這文章是湊數的，我想拿去給Ivon放友站嘿嘿~~