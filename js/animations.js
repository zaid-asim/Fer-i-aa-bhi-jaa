/* ══════════════════════════════════════════════
   FERI — Animations JS
   Confetti, Scroll Reveal, Particle System
   ══════════════════════════════════════════════ */

// ── Confetti System ──────────────────────────
const Confetti = (() => {
  let canvas, ctx2d, particles = [], animId = null;

  const COLORS = [
    '#1B8C4E','#F5A623','#E53935','#3B82F6',
    '#8B5CF6','#EC4899','#10B981','#F59E0B',
    '#EF4444','#06B6D4','#84CC16','#F97316'
  ];

  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = -20;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.size = Math.random() * 8 + 5;
      this.speedX = (Math.random() - 0.5) * 6;
      this.speedY = Math.random() * 4 + 3;
      this.rotation = Math.random() * 360;
      this.rotationSpeed = (Math.random() - 0.5) * 8;
      this.opacity = 1;
      this.shape = Math.random() > 0.4 ? 'rect' : 'circle';
      this.wobble = Math.random() * Math.PI * 2;
      this.wobbleSpeed = Math.random() * 0.1 + 0.05;
    }

    update() {
      this.wobble += this.wobbleSpeed;
      this.x += this.speedX + Math.sin(this.wobble) * 1.5;
      this.y += this.speedY;
      this.rotation += this.rotationSpeed;
      this.speedY += 0.12; // gravity
      if (this.y > canvas.height - 80) {
        this.opacity = Math.max(0, this.opacity - 0.04);
      }
    }

    draw() {
      ctx2d.save();
      ctx2d.globalAlpha = this.opacity;
      ctx2d.translate(this.x, this.y);
      ctx2d.rotate((this.rotation * Math.PI) / 180);
      ctx2d.fillStyle = this.color;

      if (this.shape === 'rect') {
        ctx2d.fillRect(-this.size / 2, -this.size / 4, this.size, this.size / 2);
      } else {
        ctx2d.beginPath();
        ctx2d.arc(0, 0, this.size / 2, 0, Math.PI * 2);
        ctx2d.fill();
      }
      ctx2d.restore();
    }

    isDead() { return this.opacity <= 0 || this.y > canvas.height + 50; }
  }

  function init() {
    canvas = document.getElementById('confettiCanvas');
    if (!canvas) return;
    ctx2d = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
  }

  function burst(count = 150) {
    if (!canvas) init();
    if (!canvas) return;

    // Launch particles from center-top
    for (let i = 0; i < count; i++) {
      setTimeout(() => {
        const p = new Particle();
        p.x = canvas.width / 2 + (Math.random() - 0.5) * 200;
        p.y = canvas.height * 0.25;
        p.speedY = Math.random() * -8 - 4;
        p.speedX = (Math.random() - 0.5) * 12;
        particles.push(p);
      }, Math.random() * 500);
    }

    if (!animId) animate();

    // Auto stop after 5s
    setTimeout(stop, 5000);
  }

  function animate() {
    if (!ctx2d) return;
    ctx2d.clearRect(0, 0, canvas.width, canvas.height);
    particles = particles.filter(p => {
      p.update();
      p.draw();
      return !p.isDead();
    });
    if (particles.length > 0) {
      animId = requestAnimationFrame(animate);
    } else {
      animId = null;
    }
  }

  function stop() {
    particles = [];
    if (animId) { cancelAnimationFrame(animId); animId = null; }
    if (ctx2d) ctx2d.clearRect(0, 0, canvas.width, canvas.height);
  }

  return { burst, stop, init };
})();

// ── Scroll Reveal (IntersectionObserver) ─────
const ScrollReveal = (() => {
  let observer;

  function init() {
    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

    // Observe all .reveal elements
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }

  function observe(container) {
    if (!observer) init();
    (container || document).querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }

  return { init, observe };
})();

// ── Splash Screen Logic ───────────────────────
function runSplash(onComplete) {
  const splash = document.getElementById('splash');
  if (!splash) { if (onComplete) onComplete(); return; }

  // Immediately notify app so DOM is rendered and interactive
  if (onComplete) onComplete();

  // Fast, silky fade out in 200ms
  setTimeout(() => {
    if (splash) {
      splash.classList.add('closing');
      setTimeout(() => {
        splash.style.display = 'none';
      }, 200);
    }
  }, 150);
}

function animateSplashParticles(canvas) {
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const particles = [];
  const colors = ['rgba(255,255,255,0.3)', 'rgba(255,255,255,0.15)', 'rgba(245,166,35,0.3)'];

  for (let i = 0; i < 40; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 4 + 1,
      dx: (Math.random() - 0.5) * 0.5,
      dy: (Math.random() - 0.5) * 0.5,
      color: colors[Math.floor(Math.random() * colors.length)],
      opacity: Math.random() * 0.6 + 0.2
    });
  }

  let running = true;
  function tick() {
    if (!running) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.dx; p.y += p.dy;
      if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();
    });
    requestAnimationFrame(tick);
  }
  tick();
  setTimeout(() => { running = false; }, 3500);
}

// ── Page Transition ───────────────────────────
function animatePageIn(container) {
  container.classList.remove('page-enter');
  void container.offsetWidth;
  container.classList.add('page-enter');

  // Observe new reveal elements
  setTimeout(() => ScrollReveal.observe(container), 50);
}

// ── Counter Animation ─────────────────────────
function animateCounter(el, target, duration = 800, prefix = '') {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) {
      start = target;
      clearInterval(timer);
    }
    el.textContent = prefix + Math.floor(start).toLocaleString('en-IN');
  }, 16);
}

// ── Image Lazy Loader ─────────────────────────
function setupLazyImages() {
  const imgObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          const src = img.dataset.src;
          img.src = src;
          img.onload = () => img.classList.add('loaded');
          img.onerror = () => {
            const label = encodeURIComponent((img.alt || 'Grocery Product').slice(0, 24));
            img.src = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300"><rect width="100%" height="100%" fill="%23F8FAFC"/><rect x="40" y="40" width="220" height="220" rx="16" fill="%23FFFFFF" stroke="%23E2E8F0" stroke-width="2"/><circle cx="150" cy="120" r="36" fill="%23EEF2F6"/><text x="150" y="128" font-size="28" text-anchor="middle">📦</text><text x="150" y="195" font-family="Inter,sans-serif" font-size="13" font-weight="600" fill="%23334155" text-anchor="middle">${label}</text><text x="150" y="218" font-family="Inter,sans-serif" font-size="11" font-weight="500" fill="%2316A34A" text-anchor="middle">100% Genuine</text></svg>`;
            img.classList.add('loaded');
          };
          imgObserver.unobserve(img);
        }
      }
    });
  }, { rootMargin: '200px' });

  document.querySelectorAll('img[data-src]').forEach(img => imgObserver.observe(img));
}

// ── Ripple on elements ────────────────────────
function addRippleToEl(el) {
  el.addEventListener('pointerdown', (e) => {
    const rect = el.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'ripple-effect';
    ripple.style.left = (e.clientX - rect.left) + 'px';
    ripple.style.top  = (e.clientY - rect.top) + 'px';
    el.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
}

// ── Badge pop animation ───────────────────────
function popBadge(el) {
  if (!el) return;
  el.style.animation = 'none';
  void el.offsetWidth;
  el.style.animation = 'badgePop 0.35s cubic-bezier(0.34,1.56,0.64,1)';
}
