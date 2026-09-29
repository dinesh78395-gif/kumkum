/**
 * Open When… — Chapter 10 Handmade Love Story Scrapbook
 * Minimal, cozy, romantic, and gentle.
 */

// ============================================================================
// 1. DATA CONFIGURATION (Easily customizable image & audio paths)
// ============================================================================
const LETTERS = [
  {
    id: 'miss-me',
    emoji: '💗',
    label: 'OPEN WHEN',
    mood: 'you miss me',
    theme: 'theme-pink',
    title: 'Open When You Miss Me ♡',
    image: 'images/miss-me.jpg',
    audio: 'audio/miss-me.mp3',
    badge: 'Chapter 10 • Envelope 01'
  },
  {
    id: 'sad',
    emoji: '💙',
    label: 'OPEN WHEN',
    mood: "you're sad",
    theme: 'theme-blue',
    title: "Open When You're Sad ♡",
    image: 'images/sad.jpg',
    audio: 'audio/sad.mp3',
    badge: 'Chapter 10 • Envelope 02'
  },
  {
    id: 'mad',
    emoji: '🧡',
    label: 'OPEN WHEN',
    mood: "you're mad at me",
    theme: 'theme-peach',
    title: "Open When You're Mad at Me ♡",
    image: 'images/mad.jpg',
    audio: 'audio/mad.mp3',
    badge: 'Chapter 10 • Envelope 03'
  },
  {
    id: 'cant-sleep',
    emoji: '💜',
    label: 'OPEN WHEN',
    mood: "you can't sleep",
    theme: 'theme-lavender',
    title: "Open When You Can't Sleep ♡",
    image: 'images/cant-sleep.jpg',
    audio: 'audio/cant-sleep.mp3',
    badge: 'Chapter 10 • Envelope 04'
  },
  {
    id: 'hug',
    emoji: '💚',
    label: 'OPEN WHEN',
    mood: 'you need a hug',
    theme: 'theme-sage',
    title: 'Open When You Need a Hug ♡',
    image: 'images/hug.jpg',
    audio: 'audio/hug.mp3',
    badge: 'Chapter 10 • Envelope 05'
  },
  {
    id: 'birthday',
    emoji: '🎂',
    label: 'OPEN ON',
    mood: 'your birthday',
    theme: 'theme-birthday',
    title: 'Open on Your Birthday ♡',
    image: 'images/birthday.jpg',
    audio: 'audio/birthday.mp3',
    badge: 'Chapter 10 • Envelope 06'
  }
];

// ============================================================================
// 2. DOM ELEMENTS
// ============================================================================
const openingScreen = document.getElementById('opening-screen');
const lettersScreen = document.getElementById('letters-screen');
const letterViewScreen = document.getElementById('letter-view-screen');

const btnOpenLetters = document.getElementById('btn-open-letters');
const btnBack = document.getElementById('btn-back');
const envelopesGrid = document.getElementById('envelopes-grid');

// Letter View details
const letterBadge = document.getElementById('letter-badge');
const letterTitle = document.getElementById('letter-title');
const mangaImage = document.getElementById('manga-image');

// Audio elements
const nativeAudio = document.getElementById('native-audio');
const audioPlayBtn = document.getElementById('audio-play-btn');
const playIcon = document.getElementById('play-icon');
const playLabel = document.getElementById('play-label');
const scrubberBar = document.getElementById('scrubber-bar');
const scrubberFill = document.getElementById('scrubber-fill');
const scrubberThumb = document.getElementById('scrubber-thumb');
const currentTimeEl = document.getElementById('current-time');
const durationTimeEl = document.getElementById('duration-time');
const audioStatusMessage = document.getElementById('audio-status-message');
const audioPlayerCard = document.getElementById('audio-player-card');

// Canvas
const canvas = document.getElementById('ambient-canvas');

// State
let currentActiveLetter = null;
let isAudioScrubbing = false;

// ============================================================================
// 3. INITIALIZATION & ENVELOPE RENDERING
// ============================================================================
function init() {
  renderEnvelopes();
  setupEventListeners();
  initAmbientCanvas();
}

/**
 * Render the 6 handmade envelopes into the grid
 */
function renderEnvelopes() {
  envelopesGrid.innerHTML = '';

  LETTERS.forEach((letter) => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = `envelope-card ${letter.theme}`;
    card.setAttribute('aria-label', `${letter.label} ${letter.mood}`);
    card.dataset.id = letter.id;

    card.innerHTML = `
      <div class="envelope-flap" aria-hidden="true"></div>
      <div class="envelope-stamp" aria-hidden="true">
        <span class="stamp-heart">♡</span>
        <span class="stamp-postmark">CH.10</span>
      </div>
      <div class="envelope-content">
        <span class="envelope-emoji" aria-hidden="true">${letter.emoji}</span>
        <span class="envelope-label">${letter.label}</span>
        <span class="envelope-mood">${letter.mood}</span>
        <div class="wax-seal" aria-hidden="true">♡</div>
      </div>
    `;

    card.addEventListener('click', () => handleEnvelopeClick(card, letter));
    envelopesGrid.appendChild(card);
  });
}

/**
 * Handle opening an envelope
 */
function handleEnvelopeClick(cardElement, letter) {
  // Animate envelope opening
  cardElement.classList.add('is-opening');

  // Gentle transition to letter page
  setTimeout(() => {
    openLetterView(letter);
    cardElement.classList.remove('is-opening');
  }, 450);
}

/**
 * Transition into Letter View
 */
function openLetterView(letter) {
  currentActiveLetter = letter;

  // Update content
  letterBadge.textContent = letter.badge;
  letterTitle.textContent = letter.title;
  
  // Set image
  mangaImage.src = letter.image;
  mangaImage.alt = letter.title;

  // Prepare audio (NO AUTOPLAY)
  resetAudioPlayer();
  nativeAudio.src = letter.audio;
  nativeAudio.load();

  // Switch screens smoothly
  switchScreen(lettersScreen, letterViewScreen);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Transition back to Envelopes
 */
function returnToEnvelopes() {
  // Pause any audio playback
  if (!nativeAudio.paused) {
    nativeAudio.pause();
  }
  resetAudioPlayer();

  switchScreen(letterViewScreen, lettersScreen);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Smooth screen switcher
 */
function switchScreen(fromScreen, toScreen) {
  fromScreen.classList.add('fade-out');

  setTimeout(() => {
    fromScreen.classList.add('hidden');
    fromScreen.classList.remove('active', 'fade-out');

    toScreen.classList.remove('hidden');
    // Force reflow
    void toScreen.offsetWidth;
    toScreen.classList.add('active');
  }, 300);
}

// ============================================================================
// 4. CUSTOM AUDIO PLAYER LOGIC
// ============================================================================
function resetAudioPlayer() {
  nativeAudio.pause();
  nativeAudio.currentTime = 0;
  updatePlayButton(false);
  scrubberFill.style.width = '0%';
  scrubberThumb.style.left = '0%';
  scrubberBar.setAttribute('aria-valuenow', '0');
  currentTimeEl.textContent = '0:00';
  durationTimeEl.textContent = '0:00';
  audioStatusMessage.textContent = '';
}

function updatePlayButton(isPlaying) {
  if (isPlaying) {
    playIcon.textContent = '❚❚';
    playLabel.textContent = 'Pause';
    audioPlayBtn.setAttribute('aria-label', 'Pause voice note');
  } else {
    playIcon.textContent = '▶';
    playLabel.textContent = 'Play';
    audioPlayBtn.setAttribute('aria-label', 'Play voice note');
  }
}

function toggleAudioPlayback() {
  if (!nativeAudio.src) return;

  if (nativeAudio.paused) {
    audioStatusMessage.textContent = '';
    const playPromise = nativeAudio.play();

    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          updatePlayButton(true);
        })
        .catch((error) => {
          console.info('Audio note placeholder notice:', error);
          updatePlayButton(false);
          // Friendly gentle message when audio file hasn't been added yet
          const fileName = currentActiveLetter ? currentActiveLetter.audio : 'recording';
          audioStatusMessage.textContent = `Awaiting your voice note in ${fileName} ♡`;
        });
    }
  } else {
    nativeAudio.pause();
    updatePlayButton(false);
  }
}

function formatTime(seconds) {
  if (isNaN(seconds) || seconds < 0) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

// Time & Progress Updates
nativeAudio.addEventListener('timeupdate', () => {
  if (isAudioScrubbing) return;
  const current = nativeAudio.currentTime;
  const duration = nativeAudio.duration;

  currentTimeEl.textContent = formatTime(current);

  if (duration && !isNaN(duration) && duration > 0) {
    const percent = Math.min(100, Math.max(0, (current / duration) * 100));
    scrubberFill.style.width = `${percent}%`;
    scrubberThumb.style.left = `${percent}%`;
    scrubberBar.setAttribute('aria-valuenow', Math.round(percent));
  }
});

nativeAudio.addEventListener('loadedmetadata', () => {
  if (nativeAudio.duration && !isNaN(nativeAudio.duration)) {
    durationTimeEl.textContent = formatTime(nativeAudio.duration);
  }
});

nativeAudio.addEventListener('ended', () => {
  updatePlayButton(false);
  scrubberFill.style.width = '0%';
  scrubberThumb.style.left = '0%';
  currentTimeEl.textContent = '0:00';
});

nativeAudio.addEventListener('error', () => {
  updatePlayButton(false);
  const fileName = currentActiveLetter ? currentActiveLetter.audio : 'recording';
  audioStatusMessage.textContent = `Awaiting your voice note in ${fileName} ♡`;
});

// Scrubber Click & Drag interaction
function seekAudioFromEvent(e) {
  const rect = scrubberBar.getBoundingClientRect();
  const clientX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
  const clickX = Math.max(0, Math.min(clientX - rect.left, rect.width));
  const percent = clickX / rect.width;

  scrubberFill.style.width = `${percent * 100}%`;
  scrubberThumb.style.left = `${percent * 100}%`;

  if (nativeAudio.duration && !isNaN(nativeAudio.duration)) {
    nativeAudio.currentTime = percent * nativeAudio.duration;
    currentTimeEl.textContent = formatTime(nativeAudio.currentTime);
  }
}

scrubberBar.addEventListener('mousedown', (e) => {
  isAudioScrubbing = true;
  seekAudioFromEvent(e);

  const onMouseMove = (moveEvent) => {
    if (isAudioScrubbing) seekAudioFromEvent(moveEvent);
  };

  const onMouseUp = () => {
    isAudioScrubbing = false;
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
  };

  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);
});

scrubberBar.addEventListener('touchstart', (e) => {
  isAudioScrubbing = true;
  seekAudioFromEvent(e);
}, { passive: true });

scrubberBar.addEventListener('touchmove', (e) => {
  if (isAudioScrubbing) seekAudioFromEvent(e);
}, { passive: true });

scrubberBar.addEventListener('touchend', () => {
  isAudioScrubbing = false;
});

// Accessible keyboard control on scrubber
scrubberBar.addEventListener('keydown', (e) => {
  if (!nativeAudio.duration) return;
  let newTime = nativeAudio.currentTime;

  if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
    newTime = Math.min(nativeAudio.duration, newTime + 5);
    e.preventDefault();
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
    newTime = Math.max(0, newTime - 5);
    e.preventDefault();
  }

  nativeAudio.currentTime = newTime;
});

// Image error fallback
mangaImage.addEventListener('error', () => {
  mangaImage.alt = 'Artwork waiting to be placed';
});

// ============================================================================
// 5. EVENT LISTENERS
// ============================================================================
function setupEventListeners() {
  // Opening button
  btnOpenLetters.addEventListener('click', () => {
    switchScreen(openingScreen, lettersScreen);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Back button
  btnBack.addEventListener('click', () => {
    returnToEnvelopes();
  });

  // Play audio button
  audioPlayBtn.addEventListener('click', toggleAudioPlayback);
}

// ============================================================================
// 6. AMBIENT CANVAS (Gentle, subtle floating hearts and tiny sparkles)
// ============================================================================
function initAmbientCanvas() {
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  // Create subtle floating particles
  const particles = [];
  const PARTICLE_COUNT = 18; // minimal, intimate, never overcrowded

  const colors = [
    'rgba(235, 115, 136, ',  // soft pink
    'rgba(146, 121, 202, ',  // soft lavender
    'rgba(104, 160, 222, ',  // soft blue
    'rgba(235, 155, 110, ',  // soft peach
    'rgba(110, 175, 125, '   // soft sage
  ];

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      size: Math.random() * 8 + 6,
      speedY: Math.random() * 0.4 + 0.15,
      speedX: (Math.random() - 0.5) * 0.2,
      opacity: Math.random() * 0.2 + 0.12,
      color: colors[Math.floor(Math.random() * colors.length)],
      angle: Math.random() * Math.PI * 2,
      spinSpeed: (Math.random() - 0.5) * 0.015,
      type: Math.random() > 0.35 ? 'heart' : 'sparkle'
    });
  }

  function drawHeart(x, y, size, color, opacity, angle) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.fillStyle = `${color}${opacity})`;
    ctx.beginPath();
    const d = size / 2;
    ctx.moveTo(0, d * 0.7);
    ctx.bezierCurveTo(d * 1.2, -d * 0.8, d * 2, d * 0.6, 0, d * 2);
    ctx.bezierCurveTo(-d * 2, d * 0.6, -d * 1.2, -d * 0.8, 0, d * 0.7);
    ctx.fill();
    ctx.restore();
  }

  function drawSparkle(x, y, size, color, opacity) {
    ctx.save();
    ctx.translate(x, y);
    ctx.fillStyle = `${color}${opacity})`;
    ctx.beginPath();
    ctx.arc(0, 0, size * 0.25, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let p of particles) {
      p.y -= p.speedY;
      p.x += p.speedX + Math.sin(p.y * 0.01) * 0.25;
      p.angle += p.spinSpeed;

      // Wrap around top/bottom
      if (p.y < -30) {
        p.y = height + 20;
        p.x = Math.random() * width;
      }
      if (p.x < -20) p.x = width + 20;
      if (p.x > width + 20) p.x = -20;

      if (p.type === 'heart') {
        drawHeart(p.x, p.y, p.size, p.color, p.opacity, p.angle);
      } else {
        drawSparkle(p.x, p.y, p.size, p.color, p.opacity);
      }
    }

    requestAnimationFrame(animate);
  }

  // Check if reduced motion is requested
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!motionQuery.matches) {
    animate();
  }
}

// Start when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
