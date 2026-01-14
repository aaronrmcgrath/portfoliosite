/**
 * Easter Eggs for aaronrmcgrath.com
 * - Konami Code: Activates sparkle mouse trail
 * - Snow Toggle: Hidden button in top-left triggers snowfall
 */

(function() {
    'use strict';

    // ===== KONAMI CODE → SPARKLE TRAIL =====
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
    let konamiIndex = 0;
    let sparklesActive = localStorage.getItem('sparklesActive') === 'true';

    // Sparkle state
    let sparkleCanvas = null;
    let sparkleCtx = null;
    let particles = [];
    let sparkleAnimationId = null;
    let mouseX = 0;
    let mouseY = 0;

    // Sparkle colors (gold, white, violet - matches site theme)
    const sparkleColors = [
        '#FFD700', // gold
        '#FFFFFF', // white
        '#7c3aed', // violet (site accent)
        '#a78bfa', // light violet
        '#FFF8DC', // cornsilk
    ];

    function initSparkleCanvas() {
        if (sparkleCanvas) return;

        sparkleCanvas = document.createElement('canvas');
        sparkleCanvas.id = 'sparkle-canvas';
        sparkleCanvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
        document.body.appendChild(sparkleCanvas);
        sparkleCtx = sparkleCanvas.getContext('2d');

        function resize() {
            sparkleCanvas.width = window.innerWidth;
            sparkleCanvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);
    }

    function createSparkle(x, y) {
        const count = 3 + Math.floor(Math.random() * 3);
        for (let i = 0; i < count; i++) {
            particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 4,
                vy: (Math.random() - 0.5) * 4 - 1,
                size: 2 + Math.random() * 4,
                color: sparkleColors[Math.floor(Math.random() * sparkleColors.length)],
                life: 1,
                decay: 0.02 + Math.random() * 0.02
            });
        }
    }

    function animateSparkles() {
        if (!sparkleCtx) return;

        sparkleCtx.clearRect(0, 0, sparkleCanvas.width, sparkleCanvas.height);

        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.1; // gravity
            p.life -= p.decay;

            if (p.life <= 0) {
                particles.splice(i, 1);
                continue;
            }

            sparkleCtx.save();
            sparkleCtx.globalAlpha = p.life;
            sparkleCtx.fillStyle = p.color;
            sparkleCtx.shadowBlur = 10;
            sparkleCtx.shadowColor = p.color;

            // Draw a 4-point star
            sparkleCtx.beginPath();
            const s = p.size;
            sparkleCtx.moveTo(p.x, p.y - s);
            sparkleCtx.lineTo(p.x + s * 0.3, p.y - s * 0.3);
            sparkleCtx.lineTo(p.x + s, p.y);
            sparkleCtx.lineTo(p.x + s * 0.3, p.y + s * 0.3);
            sparkleCtx.lineTo(p.x, p.y + s);
            sparkleCtx.lineTo(p.x - s * 0.3, p.y + s * 0.3);
            sparkleCtx.lineTo(p.x - s, p.y);
            sparkleCtx.lineTo(p.x - s * 0.3, p.y - s * 0.3);
            sparkleCtx.closePath();
            sparkleCtx.fill();
            sparkleCtx.restore();
        }

        sparkleAnimationId = requestAnimationFrame(animateSparkles);
    }

    function startSparkles() {
        initSparkleCanvas();
        sparkleCanvas.style.display = 'block';

        document.addEventListener('mousemove', handleSparkleMouseMove);
        document.addEventListener('touchmove', handleSparkleTouch);
        animateSparkles();
    }

    function stopSparkles() {
        if (sparkleCanvas) {
            sparkleCanvas.style.display = 'none';
        }
        document.removeEventListener('mousemove', handleSparkleMouseMove);
        document.removeEventListener('touchmove', handleSparkleTouch);
        if (sparkleAnimationId) {
            cancelAnimationFrame(sparkleAnimationId);
            sparkleAnimationId = null;
        }
        particles = [];
    }

    function handleSparkleMouseMove(e) {
        createSparkle(e.clientX, e.clientY);
    }

    function handleSparkleTouch(e) {
        if (e.touches.length > 0) {
            createSparkle(e.touches[0].clientX, e.touches[0].clientY);
        }
    }

    function toggleSparkles() {
        sparklesActive = !sparklesActive;
        localStorage.setItem('sparklesActive', sparklesActive);

        if (sparklesActive) {
            startSparkles();
            console.log('%c✨ Sparkle mode activated! ✨', 'color: #FFD700; font-size: 16px; font-weight: bold;');
        } else {
            stopSparkles();
            console.log('%c Sparkle mode deactivated', 'color: #666; font-size: 12px;');
        }
    }

    // Konami code listener
    document.addEventListener('keydown', function(e) {
        if (e.code === konamiCode[konamiIndex]) {
            konamiIndex++;
            if (konamiIndex === konamiCode.length) {
                toggleSparkles();
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });

    // Restore sparkle state on page load
    if (sparklesActive) {
        startSparkles();
    }


    // ===== SNOW EFFECT =====
    let snowActive = localStorage.getItem('snowActive') === 'true';
    let snowCanvas = null;
    let snowCtx = null;
    let snowflakes = [];
    let snowAnimationId = null;

    function initSnowCanvas() {
        if (snowCanvas) return;

        snowCanvas = document.createElement('canvas');
        snowCanvas.id = 'snow-canvas';
        snowCanvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9998;';
        document.body.appendChild(snowCanvas);
        snowCtx = snowCanvas.getContext('2d');

        function resize() {
            snowCanvas.width = window.innerWidth;
            snowCanvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);
    }

    function createSnowflakes() {
        const count = Math.floor(window.innerWidth / 10); // Density based on screen width
        for (let i = 0; i < count; i++) {
            snowflakes.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                size: 1 + Math.random() * 3,
                speed: 0.5 + Math.random() * 1.5,
                wind: (Math.random() - 0.5) * 0.5,
                opacity: 0.3 + Math.random() * 0.7
            });
        }
    }

    function animateSnow() {
        if (!snowCtx) return;

        snowCtx.clearRect(0, 0, snowCanvas.width, snowCanvas.height);

        for (let i = 0; i < snowflakes.length; i++) {
            const s = snowflakes[i];
            s.y += s.speed;
            s.x += s.wind + Math.sin(s.y * 0.01) * 0.5;

            // Reset snowflake when it goes off screen
            if (s.y > snowCanvas.height) {
                s.y = -10;
                s.x = Math.random() * snowCanvas.width;
            }
            if (s.x > snowCanvas.width) s.x = 0;
            if (s.x < 0) s.x = snowCanvas.width;

            snowCtx.save();
            snowCtx.globalAlpha = s.opacity;
            snowCtx.fillStyle = '#FFFFFF';
            snowCtx.shadowBlur = 5;
            snowCtx.shadowColor = '#ADD8E6';
            snowCtx.beginPath();
            snowCtx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
            snowCtx.fill();
            snowCtx.restore();
        }

        snowAnimationId = requestAnimationFrame(animateSnow);
    }

    function startSnow() {
        initSnowCanvas();
        snowCanvas.style.display = 'block';
        if (snowflakes.length === 0) {
            createSnowflakes();
        }
        animateSnow();
    }

    function stopSnow() {
        if (snowCanvas) {
            snowCanvas.style.display = 'none';
        }
        if (snowAnimationId) {
            cancelAnimationFrame(snowAnimationId);
            snowAnimationId = null;
        }
    }

    // Expose toggle function globally for the button
    window.toggleSnow = function() {
        snowActive = !snowActive;
        localStorage.setItem('snowActive', snowActive);

        const btn = document.getElementById('snow-toggle');
        if (btn) {
            btn.setAttribute('aria-pressed', snowActive);
        }

        if (snowActive) {
            startSnow();
        } else {
            stopSnow();
        }
    };

    // Initialize snow state on load
    if (snowActive) {
        startSnow();
        // Update button state if it exists
        setTimeout(function() {
            const btn = document.getElementById('snow-toggle');
            if (btn) {
                btn.setAttribute('aria-pressed', 'true');
            }
        }, 0);
    }


    // ===== REDUCED MOTION SUPPORT =====
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    function handleReducedMotion() {
        if (prefersReducedMotion.matches) {
            // Disable animations for users who prefer reduced motion
            if (sparklesActive) {
                stopSparkles();
            }
            if (snowActive) {
                stopSnow();
            }
        } else {
            // Re-enable if preferences change
            if (sparklesActive) {
                startSparkles();
            }
            if (snowActive) {
                startSnow();
            }
        }
    }

    prefersReducedMotion.addEventListener('change', handleReducedMotion);
    // Initial check
    if (prefersReducedMotion.matches && (sparklesActive || snowActive)) {
        console.log('%cEaster egg animations disabled (prefers-reduced-motion)', 'color: #888;');
    }

})();
