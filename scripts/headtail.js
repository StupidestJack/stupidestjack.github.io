// 頁首的 HTML
const headerHTML = `
<header>
<div class="logo"><a href="index.html">Niugnep 的部落格</a></div>
<nav>
<a href="index.html">首頁</a>
<a href="about.html">關於我</a>
<a href="posts.html">所有文章</a>
</nav>
</header>
`;

// 頁尾的 HTML
const footerHTML = `
<footer>
<p>&copy; 2026~ Niugnep | 文章基於 CC BY 4.0 授權 | <a href="https://github.com/">GitHub</a></p>
</footer>
`;
window.addEventListener('load', function() {
    console.log("頁首頁尾注入中...");
    document.body.insertAdjacentHTML('afterbegin', headerHTML);
    document.body.insertAdjacentHTML('beforeend', footerHTML);
});