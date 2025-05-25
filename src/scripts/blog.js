import { CMS } from './cms.js';

const cms = new CMS();

async function initBlog() {
    const posts = await cms.getBlogPosts();
    const container = document.querySelector('.blog-posts');
    
    if (!container) return;
    
    posts.forEach(post => {
        const element = createBlogPost(post);
        container.appendChild(element);
    });
}

function createBlogPost(post) {
    const element = document.createElement('article');
    element.className = 'blog-post';
    element.innerHTML = `
        <div class="blog-post-image">
            <img src="${post.image}" alt="${post.title}" loading="lazy">
        </div>
        <div class="blog-post-content">
            <h2>${post.title}</h2>
            <div class="blog-post-meta">
                <time datetime="${post.date}">${formatDate(post.date)}</time>
                <span class="blog-post-category">${post.category}</span>
            </div>
            <p>${post.excerpt}</p>
            <a href="/blog/${post.slug}" class="btn btn-secondary">Read More</a>
        </div>
    `;
    return element;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Initialize blog when DOM is loaded
document.addEventListener('DOMContentLoaded', initBlog); 