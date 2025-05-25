import Masonry from 'masonry-layout';
import imagesLoaded from 'imagesloaded';

export function initMasonry() {
    const grid = document.querySelector('.masonry-grid');
    if (!grid) return;
    
    const masonry = new Masonry(grid, {
        itemSelector: '.portfolio-item',
        columnWidth: '.portfolio-item',
        percentPosition: true,
        transitionDuration: '0.3s'
    });
    
    // Reinitialize masonry after images are loaded
    imagesLoaded(grid).on('progress', () => {
        masonry.layout();
    });
} 