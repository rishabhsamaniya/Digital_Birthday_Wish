/**
 * Birthday Memories - Animation Canvas & Visual Effects Engine
 */
window.BirthdayAnimations = {
    enabled: true,

    init() {
        // Respect prefers-reduced-motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.enabled = false;
            return;
        }
        console.log('🎉 Animation Engine Ready');
    },

    triggerConfetti(containerId = 'theme-root') {
        if (!this.enabled) return;
        const container = document.getElementById(containerId) || document.body;
        const colors = ['#f43f5e', '#fbbf24', '#ec4899', '#8b5cf6', '#34d399'];

        for (let i = 0; i < 50; i++) {
            const piece = document.createElement('div');
            piece.className = 'fixed pointer-events-none z-50 rounded-sm';
            piece.style.width = `${Math.random() * 8 + 6}px`;
            piece.style.height = `${Math.random() * 12 + 6}px`;
            piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            piece.style.left = `${Math.random() * 100}vw`;
            piece.style.top = `-20px`;
            piece.style.opacity = Math.random() + 0.5;
            piece.style.transform = `rotate(${Math.random() * 360}deg)`;

            const duration = Math.random() * 3 + 2.5;
            piece.style.transition = `transform ${duration}s linear, top ${duration}s cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity ${duration}s ease-out`;

            container.appendChild(piece);

            setTimeout(() => {
                piece.style.top = `${100 + Math.random() * 20}vh`;
                piece.style.transform = `rotate(${Math.random() * 720}deg) translateX(${Math.random() * 100 - 50}px)`;
                piece.style.opacity = '0';
            }, 50);

            setTimeout(() => {
                piece.remove();
            }, duration * 1000);
        }
    },

    spawnFloatingHeart(x, y) {
        if (!this.enabled) return;
        const heart = document.createElement('div');
        heart.innerHTML = '❤️';
        heart.className = 'fixed pointer-events-none z-50 text-xl animate-bounce';
        heart.style.left = `${x || Math.random() * 90 + 5}px`;
        heart.style.top = `${y || Math.random() * 90 + 5}px`;
        heart.style.transition = 'all 2s ease-out';

        document.body.appendChild(heart);

        setTimeout(() => {
            heart.style.transform = 'translateY(-100px) scale(1.4)';
            heart.style.opacity = '0';
        }, 50);

        setTimeout(() => heart.remove(), 2000);
    }
};

document.addEventListener('DOMContentLoaded', () => BirthdayAnimations.init());
