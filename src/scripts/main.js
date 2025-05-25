// Main JavaScript file
import { initTheme } from './theme.js';
import { initAnimations } from './animations.js';
import { initNavigation } from './navigation.js';

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initAnimations();
    initNavigation();
}); 