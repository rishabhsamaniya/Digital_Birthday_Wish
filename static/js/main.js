/**
 * Birthday Memories - Core JS Engine
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('✨ Birthday Memories Engine Initialized [Phase 7]');

    // Initialize Scroll Reveal Observer
    initScrollObserver();
});

function initScrollObserver() {
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Global Dynamic Theme Applicator
window.applyTheme = function(themeData) {
    if (!themeData) return;
    const root = document.documentElement;
    if (themeData.primary) root.style.setProperty('--primary-color', themeData.primary);
    if (themeData.secondary) root.style.setProperty('--secondary-color', themeData.secondary);
    if (themeData.background) root.style.setProperty('--background-color', themeData.background);
    if (themeData.text) root.style.setProperty('--text-color', themeData.text);
    if (themeData.accent) root.style.setProperty('--accent-color', themeData.accent);
};
