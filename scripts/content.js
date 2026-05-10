// 1. 獲取當前網址的所有參數字串
const queryString = window.location.search;

// 2. 使用 URLSearchParams 進行解析
const urlParams = new URLSearchParams(queryString);
// 3. 獲取特定的參數值
const postName = urlParams.get('post');
document.addEventListener('DOMContentLoaded', function() {
    if (postName) {
        console.log("正在讀取文章：" + postName);

        // 1. 先抓 JSON 設定檔
        fetch(`posts-json/${postName}.json`)
        .then(res => {
            if (!res.ok) throw new Error("JSON missing");
            return res.json(); // 直接轉成 JSON 物件
        })
        .then(data => {
            document.getElementById('title').innerText = data.title;
            document.getElementById('time').innerText = `西元 ${data.time[0]} 年（民國 ${data.time[0] - 1911} 年）${data.time[1] < 10 ? '0' : ''}${data.time[1]} 月 ${data.time[2]} 日`;
            // 可以順便改網頁標籤標題
            document.title = `${data.title} | Niugnep 的部落格`;
        })
        .catch(err => console.error("設定檔讀取失敗:", err));

        // 2. 抓 Markdown 內容
        fetch(`posts-md/${postName}.md`)
        .then(res => {
            if (!res.ok) throw new Error("MD missing");
            return res.text();
        })
        .then(text => {
            // 使用 marked 轉換，並放入 content 區塊
            document.getElementById('content').innerHTML = marked.parse(text);
        })
        .catch(err => {
            document.getElementById('content').innerHTML = `
            <div style="text-align:center; padding: 50px;">
            <h2>(｡•́︿•̀｡) 找不到文章</h2>
            <p>這篇文章可能還在草稿夾裡，或者被外星人劫走了。</p>
            <a href="index.html" style="color: var(--accent-color);">回首頁</a>
            </div>
            `;
        });
    } else {
        // 如果網址沒帶參數，自動導回首頁或顯示提示
        document.getElementById('content').innerHTML = "請選擇一篇文章閱讀。";
    }
});
