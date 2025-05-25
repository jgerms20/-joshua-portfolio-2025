// Content management system integration
export class CMS {
    constructor() {
        this.baseUrl = 'https://api.your-cms.com';
        this.cache = new Map();
    }
    
    async getPortfolioItems() {
        if (this.cache.has('portfolio')) {
            return this.cache.get('portfolio');
        }
        
        const response = await fetch(`${this.baseUrl}/portfolio`);
        const data = await response.json();
        this.cache.set('portfolio', data);
        return data;
    }
    
    async getBlogPosts() {
        if (this.cache.has('blog')) {
            return this.cache.get('blog');
        }
        
        const response = await fetch(`${this.baseUrl}/blog`);
        const data = await response.json();
        this.cache.set('blog', data);
        return data;
    }
} 