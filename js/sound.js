/* ══════════════════════════════════════════════
   FERI — Sound Engine (Web Audio API)
   Piano/Hall-Effect Click Sounds
   ══════════════════════════════════════════════ */
const SoundEngine = (() => {
  let ctx = null;
  let enabled = true;

  function getCtx() {
    if (!ctx) {
      try {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
      } catch(e) {
        enabled = false;
      }
    }
    if (ctx && ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  // Create a piano-like tone
  function playTone({ freq = 440, type = 'sine', attack = 0.002, decay = 0.08, gain = 0.25, detune = 0 } = {}) {
    if (!enabled) return;
    const ac = getCtx();
    if (!ac) return;

    const now = ac.currentTime;
    const osc = ac.createOscillator();
    const gainNode = ac.createGain();
    const compressor = ac.createDynamicsCompressor();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, now);
    osc.detune.setValueAtTime(detune, now);

    gainNode.gain.setValueAtTime(0, now);
    gainNode.gain.linearRampToValueAtTime(gain, now + attack);
    gainNode.gain.exponentialRampToValueAtTime(0.001, now + attack + decay);

    compressor.threshold.setValueAtTime(-20, now);
    compressor.knee.setValueAtTime(10, now);
    compressor.ratio.setValueAtTime(4, now);

    osc.connect(gainNode);
    gainNode.connect(compressor);
    compressor.connect(ac.destination);

    osc.start(now);
    osc.stop(now + attack + decay + 0.01);
  }

  // Hall-effect multi-layer sound (Samsung C7 Pro style)
  function playHallEffect() {
    // Main click body
    playTone({ freq: 1100, type: 'sine', attack: 0.001, decay: 0.025, gain: 0.18 });
    // Harmonic overtone
    setTimeout(() => playTone({ freq: 2200, type: 'sine', attack: 0.001, decay: 0.015, gain: 0.06 }), 2);
    // Subtle low thud
    playTone({ freq: 280, type: 'sine', attack: 0.001, decay: 0.04, gain: 0.08 });
  }

  // Piano key tones (C major scale)
  const PIANO_NOTES = {
    C4:  261.63, D4:  293.66, E4:  329.63,
    F4:  349.23, G4:  392.00, A4:  440.00,
    B4:  493.88, C5:  523.25, D5:  587.33,
    E5:  659.25, G5:  783.99, A5:  880.00,
    Bb3: 233.08, Eb4: 311.13
  };

  const sounds = {
    click: () => playHallEffect(),

    nav: () => {
      playTone({ freq: 880, type: 'sine', attack: 0.001, decay: 0.04, gain: 0.12 });
    },

    addToCart: () => {
      // Ascending C-E-G arpeggio (happy)
      playTone({ freq: PIANO_NOTES.C5, type: 'triangle', attack: 0.002, decay: 0.12, gain: 0.3 });
      setTimeout(() => playTone({ freq: PIANO_NOTES.E5, type: 'triangle', attack: 0.002, decay: 0.10, gain: 0.25 }), 80);
      setTimeout(() => playTone({ freq: PIANO_NOTES.G5, type: 'triangle', attack: 0.002, decay: 0.14, gain: 0.22 }), 160);
    },

    removeItem: () => {
      playTone({ freq: PIANO_NOTES.Bb3, type: 'triangle', attack: 0.002, decay: 0.10, gain: 0.18 });
      setTimeout(() => playTone({ freq: PIANO_NOTES.G4, type: 'triangle', attack: 0.002, decay: 0.08, gain: 0.12 }), 70);
    },

    orderSuccess: () => {
      // C major chord + ascending melody
      const melody = [
        { freq: PIANO_NOTES.C4, delay: 0,   gain: 0.28 },
        { freq: PIANO_NOTES.E4, delay: 0,   gain: 0.22 },
        { freq: PIANO_NOTES.G4, delay: 0,   gain: 0.18 },
        { freq: PIANO_NOTES.C5, delay: 120, gain: 0.30 },
        { freq: PIANO_NOTES.E5, delay: 240, gain: 0.25 },
        { freq: PIANO_NOTES.G5, delay: 360, gain: 0.20 },
        { freq: PIANO_NOTES.A5, delay: 480, gain: 0.22 },
        { freq: PIANO_NOTES.C5, delay: 600, gain: 0.25 },
      ];
      melody.forEach(({ freq, delay, gain }) => {
        setTimeout(() => playTone({ freq, type: 'triangle', attack: 0.003, decay: 0.2, gain }), delay);
      });
    },

    wishlist: () => {
      playTone({ freq: PIANO_NOTES.A5, type: 'sine', attack: 0.002, decay: 0.08, gain: 0.2 });
      setTimeout(() => playTone({ freq: PIANO_NOTES.C5, type: 'sine', attack: 0.002, decay: 0.07, gain: 0.15 }), 60);
    },

    error: () => {
      playTone({ freq: 200, type: 'sawtooth', attack: 0.002, decay: 0.06, gain: 0.15 });
      setTimeout(() => playTone({ freq: 180, type: 'sawtooth', attack: 0.001, decay: 0.05, gain: 0.12 }), 80);
    },

    coupon: () => {
      // Coin-like sound
      playTone({ freq: 1800, type: 'sine', attack: 0.001, decay: 0.08, gain: 0.2 });
      setTimeout(() => playTone({ freq: 2200, type: 'sine', attack: 0.001, decay: 0.06, gain: 0.15 }), 50);
    },

    pageChange: () => {
      playTone({ freq: 660, type: 'sine', attack: 0.001, decay: 0.035, gain: 0.10 });
    },

    toggle: () => {
      playTone({ freq: 440, type: 'square', attack: 0.001, decay: 0.02, gain: 0.08 });
    },

    notification: () => {
      playTone({ freq: 900, type: 'sine', attack: 0.002, decay: 0.06, gain: 0.15 });
      setTimeout(() => playTone({ freq: 1100, type: 'sine', attack: 0.002, decay: 0.08, gain: 0.15 }), 100);
    }
  };

  function play(name) {
    if (!enabled) return;
    try {
      if (sounds[name]) sounds[name]();
    } catch(e) {
      // Silently fail
    }
  }

  function setEnabled(val) { enabled = val; }
  function isEnabled() { return enabled; }

  // Attach ripple effect to element
  function addRipple(el) {
    el.style.position = 'relative';
    el.style.overflow = 'hidden';
    el.addEventListener('click', (e) => {
      const ripple = document.createElement('span');
      ripple.classList.add('ripple-effect');
      ripple.style.left = e.offsetX + 'px';
      ripple.style.top = e.offsetY + 'px';
      el.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  }

  return { play, setEnabled, isEnabled, addRipple };
})();

// Global shorthand
function playSound(name) { SoundEngine.play(name); }

// Auto-attach click sound to all interactive elements
document.addEventListener('DOMContentLoaded', () => {
  // Attach hall-effect to all buttons and links globally
  document.addEventListener('click', (e) => {
    const target = e.target.closest('button, a, .filter-chip, .category-chip, .brand-chip, .orders-tab, .payment-option, .product-card, .settings-item');
    if (target && !target.dataset.nosound) {
      SoundEngine.play('click');
    }
  });
});
