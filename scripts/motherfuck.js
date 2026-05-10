document.addEventListener('DOMContentLoaded', () => {

    const container = document.getElementById('posts-container');

    fetch("posts.json")
    .then(res => res.json())
    .then(posts => {

        container.innerHTML = "";

        // Object.entries 轉陣列
        const postsArray = Object.entries(posts);

        // 最新文章排前面
        postsArray.reverse();

        postsArray.forEach(([postName, data]) => {

            const article = document.createElement('article');

            article.className = "post-card";

            article.innerHTML = `
                <h3>${data.title}</h3>

                <p class="post-time">
                    ${data.time[0]}/${data.time[1]}/${data.time[2]}
                </p>

                <p>
                    ${data.description}
                </p>
                <div class="tags">
                    ${
                        data.tags
                        ? data.tags.map(tag =>
                            `<span class="tag">${tag}</span>`
                        ).join("")
                        : ""
                    }
                </div>
            `;
            article.style.cursor = "pointer";
            article.addEventListener('click', () => {
                window.location.href =
                    `post_motherfuck.html?post=${postName}`;
            });

            container.appendChild(article); 
        });

    });
});