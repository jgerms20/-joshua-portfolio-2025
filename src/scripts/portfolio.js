import { CMS } from './cms.js';
import { initMasonry } from './masonry.js';

const cms = new CMS();

async function initPortfolio() {
    const portfolioItems = await cms.getPortfolioItems();
    const grid = document.querySelector('.masonry-grid');
    
    // Render portfolio items
    portfolioItems.forEach(item => {
        const element = createPortfolioItem(item);
        grid.appendChild(element);
    });
    
    // Initialize masonry layout
    initMasonry();
    
    // Initialize filters
    initFilters();
}

function createPortfolioItem(item) {
    const element = document.createElement('div');
    element.className = `portfolio-item ${item.category}`;
    element.innerHTML = `
        <img src="${item.image}" alt="${item.title}" loading="lazy">
        <div class="portfolio-item-content">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
        </div>
    `;
    return element;
}

function initFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.dataset.filter;
            
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter items
            const items = document.querySelectorAll('.portfolio-item');
            items.forEach(item => {
                if (filter === 'all' || item.classList.contains(filter)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Reinitialize masonry
            initMasonry();
        });
    });
}

// Initialize portfolio when DOM is loaded
document.addEventListener('DOMContentLoaded', initPortfolio); 