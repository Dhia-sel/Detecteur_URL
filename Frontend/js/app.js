// ═══════════════════════════════════════════════════
//  BACKGROUND: PARTICLES + RADAR
// ═══════════════════════════════════════════════════
const canvas = document.getElementById('bgCanvas');
const ctx = canvas.getContext('2d');
let W, H, particles = [], radarAngle = 0, radarTrails = [];

function getAccentColor() {
  return getComputedStyle(document.body).getPropertyValue('--accent').trim();
}

function resize() {
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

// Init particles
function initParticles() {
  particles = [];
  const count = Math.floor(W * H / 14000);
  for (let i = 0; i < count; i++) {
    particles.push({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.4 + 0.3,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.25,
      alpha: Math.random() * 0.5 + 0.1,
      blink: Math.random() * Math.PI * 2,
    });
  }
}
initParticles();
window.addEventListener('resize', initParticles);

function drawBg() {
  ctx.clearRect(0, 0, W, H);

  // ── Particles ──
  const accent = getAccentColor();
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    p.blink += 0.02;
    if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
    if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
    const a = p.alpha * (0.6 + 0.4 * Math.sin(p.blink));
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = accent.replace(')', `,${a})`).replace('rgb(', 'rgba(').replace('#', '');
    ctx.globalAlpha = a;
    ctx.fillStyle = accent;
    ctx.fill();
    ctx.globalAlpha = 1;
  });

  // ── Particle connections ──
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 110) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = accent;
        ctx.globalAlpha = (1 - dist / 110) * 0.1;
        ctx.lineWidth = 0.5;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }
    }
  }

  // ── Constellation ──
  if (!window._stars) {
    const zone = { x: W * 0.55, y: H * 0.08, w: W * 0.44, h: H * 0.7 };
    window._stars = Array.from({ length: 55 }, () => ({
      x: zone.x + Math.random() * zone.w,
      y: zone.y + Math.random() * zone.h,
      r: 0.8 + Math.random() * 1.6,
      alpha: 0.3 + Math.random() * 0.55,
      blink: Math.random() * Math.PI * 2,
      blinkSpeed: 0.008 + Math.random() * 0.018,
      vx: (Math.random() - 0.5) * 0.06,
      vy: (Math.random() - 0.5) * 0.06,
      zone,
    }));
    window._constellT = 0;
  }
  window._constellT += 0.008;

  const stars = window._stars;
  // Move stars slowly
  stars.forEach(s => {
    s.x += s.vx; s.y += s.vy;
    s.blink += s.blinkSpeed;
    if (s.x < s.zone.x) s.vx = Math.abs(s.vx);
    if (s.x > s.zone.x + s.zone.w) s.vx = -Math.abs(s.vx);
    if (s.y < s.zone.y) s.vy = Math.abs(s.vy);
    if (s.y > s.zone.y + s.zone.h) s.vy = -Math.abs(s.vy);
  });

  // Draw constellation lines first
  for (let i = 0; i < stars.length; i++) {
    for (let j = i + 1; j < stars.length; j++) {
      const dx = stars[i].x - stars[j].x;
      const dy = stars[i].y - stars[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 95) {
        const pulse = 0.5 + 0.5 * Math.sin(window._constellT * 1.5 + i * 0.3);
        ctx.beginPath();
        ctx.moveTo(stars[i].x, stars[i].y);
        ctx.lineTo(stars[j].x, stars[j].y);
        ctx.strokeStyle = accent;
        ctx.globalAlpha = (1 - dist / 95) * 0.12 * pulse;
        ctx.lineWidth = 0.7;
        ctx.stroke();
        ctx.globalAlpha = 1;
      }
    }
  }

  // Draw stars
  stars.forEach((s, i) => {
    const twinkle = s.alpha * (0.55 + 0.45 * Math.sin(s.blink));
    // Glow
    const grd = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.r * 5);
    grd.addColorStop(0, accent);
    grd.addColorStop(1, 'transparent');
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r * 5, 0, Math.PI * 2);
    ctx.fillStyle = grd;
    ctx.globalAlpha = twinkle * 0.18;
    ctx.fill();
    // Core
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = accent;
    ctx.globalAlpha = twinkle;
    ctx.fill();
    ctx.globalAlpha = 1;
  });

  // Shooting star occasionally
  if (!window._shoot) window._shoot = { active: false, t: 0, next: 120 + Math.random() * 200 };
  window._shoot.t++;
  if (!window._shoot.active && window._shoot.t > window._shoot.next) {
    window._shoot.active = true;
    window._shoot.px = W * 0.58 + Math.random() * W * 0.3;
    window._shoot.py = H * 0.08 + Math.random() * H * 0.25;
    window._shoot.life = 1;
    window._shoot.angle = Math.PI * 0.28 + Math.random() * 0.3;
    window._shoot.speed = 5 + Math.random() * 5;
  }
  if (window._shoot.active) {
    window._shoot.life -= 0.04;
    window._shoot.px += Math.cos(window._shoot.angle) * window._shoot.speed;
    window._shoot.py += Math.sin(window._shoot.angle) * window._shoot.speed;
    const tx = window._shoot.px - Math.cos(window._shoot.angle) * 40;
    const ty = window._shoot.py - Math.sin(window._shoot.angle) * 40;
    const sg = ctx.createLinearGradient(tx, ty, window._shoot.px, window._shoot.py);
    sg.addColorStop(0, 'transparent');
    sg.addColorStop(1, accent);
    ctx.beginPath();
    ctx.moveTo(tx, ty);
    ctx.lineTo(window._shoot.px, window._shoot.py);
    ctx.strokeStyle = sg;
    ctx.globalAlpha = window._shoot.life * 0.8;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.globalAlpha = 1;
    if (window._shoot.life <= 0) {
      window._shoot.active = false;
      window._shoot.t = 0;
      window._shoot.next = 140 + Math.random() * 220;
    }
  }

  // ── EKG / Sound Waves (bottom-left zone) ──
  if (!window._waveT) window._waveT = 0;
  window._waveT += 0.018;
  const wt = window._waveT;

  const wCx = W * 0.26, wCy = H * 0.72;
  const wW = Math.min(W * 0.38, 360), wH = 80;
  const wX0 = wCx - wW / 2, wX1 = wCx + wW / 2;

  // 3 layered waves
  [0.9, 0.55, 0.28].forEach((alpha, li) => {
    const freq  = 1.8 + li * 0.9;
    const amp   = (wH / 2) * (0.5 - li * 0.1);
    const phase = li * 1.1;
    ctx.beginPath();
    for (let px = wX0; px <= wX1; px += 2) {
      const t2    = ((px - wX0) / wW) * Math.PI * 2 * freq - wt * 2.2 + phase;
      const base  = Math.sin(t2) * 0.4;
      const spike = Math.exp(-Math.pow(((px - wX0) / wW * freq - Math.floor((px - wX0) / wW * freq) - 0.5) * 6, 2)) * Math.sign(Math.sin(t2 * 0.5));
      const y = wCy + (base + spike) * amp;
      px === wX0 ? ctx.moveTo(px, y) : ctx.lineTo(px, y);
    }
    ctx.strokeStyle = accent;
    ctx.globalAlpha  = alpha * 0.12;
    ctx.lineWidth    = li === 0 ? 1.5 : 1;
    ctx.stroke();
    ctx.globalAlpha  = 1;
  });

  // Glowing scanhead
  const scanX = wX0 + ((wt * 40) % wW);
  const gradScan = ctx.createLinearGradient(scanX - 50, 0, scanX + 6, 0);
  gradScan.addColorStop(0, 'transparent');
  gradScan.addColorStop(1, accent);
  ctx.beginPath();
  ctx.moveTo(wX0, wCy);
  for (let px = wX0; px <= Math.min(scanX, wX1); px += 2) {
    const t2    = ((px - wX0) / wW) * Math.PI * 2 * 1.8 - wt * 2.2;
    const base  = Math.sin(t2) * 0.4;
    const spike = Math.exp(-Math.pow(((px - wX0) / wW * 1.8 - Math.floor((px - wX0) / wW * 1.8) - 0.5) * 6, 2)) * Math.sign(Math.sin(t2 * 0.5));
    ctx.lineTo(px, wCy + (base + spike) * (wH / 2 * 0.5));
  }
  ctx.strokeStyle  = gradScan;
  ctx.globalAlpha  = 0.65;
  ctx.lineWidth    = 1.8;
  ctx.stroke();
  ctx.globalAlpha  = 1;

  // Dot at scanhead tip
  if (scanX <= wX1) {
    const t2h = ((scanX - wX0) / wW) * Math.PI * 2 * 1.8 - wt * 2.2;
    const yh  = wCy + (Math.sin(t2h) * 0.4 + Math.exp(-Math.pow(((scanX - wX0) / wW * 1.8 - Math.floor((scanX - wX0) / wW * 1.8) - 0.5) * 6, 2)) * Math.sign(Math.sin(t2h * 0.5))) * (wH / 2 * 0.5);
    ctx.beginPath(); ctx.arc(scanX, yh, 3, 0, Math.PI * 2);
    ctx.fillStyle = accent; ctx.globalAlpha = 0.9; ctx.fill();
    ctx.beginPath(); ctx.arc(scanX, yh, 9, 0, Math.PI * 2);
    ctx.fillStyle = accent; ctx.globalAlpha = 0.12; ctx.fill();
    ctx.globalAlpha = 1;
  }

  // Baseline
  ctx.beginPath(); ctx.moveTo(wX0, wCy); ctx.lineTo(wX1, wCy);
  ctx.strokeStyle = accent; ctx.globalAlpha = 0.05; ctx.lineWidth = 1; ctx.stroke();
  ctx.globalAlpha = 1;

  requestAnimationFrame(drawBg);
}
drawBg();

// ─── Draw tick marks on disk ───
function drawDiskTicks() {
  const svg = document.getElementById('ticks');
  svg.innerHTML = '';
  const cx = 85, cy = 85, r = 65, innerR = 60;
  for (let i = 0; i < 40; i++) {
    const angle = (i / 40) * Math.PI * 2 - Math.PI / 2;
    const isMajor = i % 10 === 0;
    const len = isMajor ? 8 : 5;
    const x1 = cx + Math.cos(angle) * (r + 4);
    const y1 = cy + Math.sin(angle) * (r + 4);
    const x2 = cx + Math.cos(angle) * (r + 4 + len);
    const y2 = cy + Math.sin(angle) * (r + 4 + len);
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1); line.setAttribute('y1', y1);
    line.setAttribute('x2', x2); line.setAttribute('y2', y2);
    line.setAttribute('class', isMajor ? 'disk-tick-major' : 'disk-tick');
    svg.appendChild(line);
  }
}
drawDiskTicks();

// ═══════════════════════════════════════════════════
//  THEME SWITCHER
// ═══════════════════════════════════════════════════
function setTheme(t, btn) {
  document.body.className = 'theme-' + t;
  document.querySelectorAll('.theme-dot').forEach(d => d.classList.remove('active'));
  btn.classList.add('active');
  // Re-init particles on theme change
  setTimeout(initParticles, 50);
}

// ═══════════════════════════════════════════════════
//  NAVIGATION
// ═══════════════════════════════════════════════════
function showSec(id, btn) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
  document.getElementById('sec-' + id).classList.add('active');
  btn.classList.add('active');
}

// ═══════════════════════════════════════════════════
//  EXAMPLES
// ═══════════════════════════════════════════════════
const EXAMPLES = {
  data:  'data:text/html;base64,PGh0bWw+PHNjcmlwdD5hbGVydCgnWW91IGhhdmUgYmVlbiBoYWNrZWQnKTs8L3NjcmlwdD48L2h0bWw+',
  phish: 'http://192.168.1.1/paypal/verify-account.php?token=abc123&redirect=true',
  ip:    'https://accounts.secure-login.verify-paypal.com/login?user=victim',
  safe:  'https://github.com/Dhia-sel/Detecteur_URL',
};
function setEx(k) {
  document.getElementById('urlInput').value = EXAMPLES[k];
  document.getElementById('urlInput').focus();
}

// ═══════════════════════════════════════════════════
//  SCAN ENGINE
// ═══════════════════════════════════════════════════
const STEPS = ['Classify', 'Parse', 'Lexical Scan', 'Behaviour Scan', 'ML Score', 'Format'];
const sleep = ms => new Promise(r => setTimeout(r, ms));
let scanCount = 0;

async function runScan() {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) { document.getElementById('urlInput').focus(); return; }

  // Reset
  document.getElementById('results').style.display = 'none';
  document.getElementById('results').classList.remove('show');
  document.getElementById('emptyState').style.display = 'none';
  ['cardDisk','cardFlags','cardKV','cardCmt'].forEach(id => {
    document.getElementById(id).classList.remove('visible');
  });

  const btn = document.getElementById('scanBtn');
  btn.innerHTML = '<div class="spin"></div> Analyzing...';
  btn.classList.add('loading');

  const pw = document.getElementById('progWrap');
  pw.classList.add('show');
  const ps = document.getElementById('progSteps');
  ps.innerHTML = STEPS.map((s, i) =>
    `<div class="pstep" id="pstep${i}"><div class="pstep-dot"></div>${s}</div>`
  ).join('');

  for (let i = 0; i < STEPS.length; i++) {
    document.getElementById(`pstep${i}`).classList.add('active');
    document.getElementById('progFill').style.width = ((i + 1) / STEPS.length * 100) + '%';
    await sleep(230 + Math.random() * 170);
    document.getElementById(`pstep${i}`).classList.remove('active');
    document.getElementById(`pstep${i}`).classList.add('done');
  }

  await sleep(180);
  pw.classList.remove('show');
  btn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="7" cy="7" r="5"/><path d="m11 11 3 3"/></svg> Analyze';
  btn.classList.remove('loading');

  scanCount++;
  document.getElementById('scanMeta').textContent = scanCount + ' scan' + (scanCount > 1 ? 's' : '');

  const report = analyzeURL(url);
  renderReport(report, url);
}

// ─── Analysis ───
function entropy(s) {
  const f = {};
  for (const c of s) f[c] = (f[c] || 0) + 1;
  return Object.values(f).reduce((h, v) => { const p = v / s.length; return h - p * Math.log2(p); }, 0);
}
function computeScore(r) {
  let s = 0;
  const l = r.data.lexical, b = r.data.behaviour;
  s += (l.semantic_score || 0) * 15;
  s += (l.code_score || 0) * 20;
  s += Math.min((l.entropy || 0) * 3, 18);
  s += (l.symbol_ratio || 0) * 15;
  s += (b.risky_mime || 0) * 15;
  s += (b.base64 || 0) * 8;
  s += (b.hidden_html || 0) * 15;
  s += (b.uses_ip || 0) * 20;
  s += (b.long_subdomain || 0) * 8;
  return Math.min(Math.round(s), 100);
}

function analyzeURL(rawUrl) {
  const url = rawUrl.trim();
  const r = {
    url_type: 'unknown', parsed_url: {},
    data: { lexical: {}, behaviour: {} },
    comments: { lexical: [], behaviour: [] },
    recommendation: '', specific_insights: '', _score: 0
  };

  if (url.startsWith('data:')) {
    const m = url.match(/^data:([^;,]+)(;base64)?,(.*)$/s);
    if (m) {
      const mime = m[1], isB64 = !!m[2], raw = m[3];
      let decoded = raw;
      if (isB64) { try { decoded = atob(raw); } catch (e) {} }
      r.url_type = 'embedded';
      r.parsed_url = {
        schema: 'data', type_media: mime,
        longueur_donnees: raw.length,
        donnees: raw.substring(0, 20) + '...',
        donnees_totales: raw,
        donnees_decodees: decoded,
        base64: isB64
      };
      const hasScript = /<script/i.test(decoded), hasIframe = /<iframe/i.test(decoded);
      const hasSuspect = /login|verify|account|secure|update|confirm/i.test(decoded);
      const ent = entropy(raw), tags = (decoded.match(/<[a-z]/gi) || []).length;
      const symR = (raw.match(/[^a-zA-Z0-9]/g) || []).length / raw.length;
      r.data.lexical = {
        semantic_score: hasSuspect ? 1 : 0,
        code_score: (hasScript || hasIframe) ? 1 : 0,
        tag_count: tags, pwd_field: /type=.password/i.test(decoded) ? 1 : 0,
        entropy: parseFloat(ent.toFixed(4)),
        symbol_ratio: parseFloat(symR.toFixed(2))
      };
      const rMime = /html|javascript|exe/i.test(mime);
      r.data.behaviour = {
        risky_mime: rMime ? 1 : 0, base64: isB64 ? 1 : 0,
        hidden_html: (isB64 && /html/i.test(mime)) ? 1 : 0,
        is_unknown: 0, small_payload: raw.length < 200 ? 1 : 0
      };
      if (hasSuspect) r.comments.lexical.push('Suspicious semantic terms detected (login, verify, account, etc.).');
      else r.comments.lexical.push('No suspicious semantic terms detected.');
      if (hasScript || hasIframe) r.comments.lexical.push('Dangerous HTML tags detected — <script> or <iframe> injection.');
      else r.comments.lexical.push('No harmful code indicators detected.');
      if (ent > 4) r.comments.lexical.push('High character entropy — potential obfuscation or encoding.');
      if (symR > 0.15) r.comments.lexical.push('High symbol density indicates encoded or obfuscated content.');
      if (rMime) r.comments.behaviour.push('Risky MIME type in use (HTML, JavaScript, executable).');
      if (isB64) r.comments.behaviour.push('Base64 encoding detected — common phishing attack vector.');
      if (isB64 && /html/i.test(mime)) r.comments.behaviour.push('HTML content hidden in base64 — strong phishing indicator.');
      if (raw.length < 200) r.comments.behaviour.push('Small payload size — typical simple phishing page pattern.');
      r.specific_insights = 'Embedded data type: ' + mime;
    }
  } else {
    try {
      const u = new URL(url);
      const hasSuspect = /login|verify|paypal|bank|account|secure|update|confirm/i.test(url);
      const hasIP = /^\d{1,3}(\.\d{1,3}){3}$/.test(u.hostname);
      const longSub = u.hostname.split('.').length > 3;
      const ent = entropy(url);
      const symR = (url.match(/[^a-zA-Z0-9./:?=&-]/g) || []).length / url.length;
      const hasExe = /\.(exe|bat|ps1|sh|js|php)(\?|$)/i.test(u.pathname);
      r.url_type = u.protocol === 'https:' ? 'secure_http' : 'plain_http';
      r.parsed_url = {
        schema: u.protocol.replace(':', ''), host: u.hostname,
        port: u.port || (u.protocol === 'https:' ? '443' : '80'),
        path: u.pathname, query: u.search || '(none)',
        uses_https: u.protocol === 'https:'
      };
      r.data.lexical = {
        semantic_score: hasSuspect ? 1 : 0, code_score: hasExe ? 1 : 0,
        tag_count: 0, pwd_field: 0,
        entropy: parseFloat(ent.toFixed(4)),
        symbol_ratio: parseFloat(symR.toFixed(2))
      };
      r.data.behaviour = {
        risky_mime: hasExe ? 1 : 0, base64: /base64/i.test(url) ? 1 : 0,
        hidden_html: 0, is_unknown: 0,
        uses_ip: hasIP ? 1 : 0, long_subdomain: longSub ? 1 : 0
      };
      if (hasSuspect) r.comments.lexical.push('Suspicious keywords in URL (login, verify, bank, paypal, etc.).');
      if (hasIP) r.comments.lexical.push('IP address used as hostname — atypical of legitimate services.');
      if (longSub) r.comments.lexical.push('Deep subdomain chain — common spoofing technique.');
      if (ent > 3.8) r.comments.lexical.push('High URL entropy — possibly randomized or obfuscated domain.');
      if (hasExe) r.comments.behaviour.push('URL points to executable — potential malware distribution.');
      if (u.protocol !== 'https:') r.comments.behaviour.push('No HTTPS — data transmitted in cleartext.');
      r.specific_insights = `Schema: ${u.protocol.replace(':', '')} · Host: ${u.hostname}`;
    } catch (e) { r.recommendation = 'Cannot parse URL. Check format.'; }
  }
  const score = computeScore(r);
  r._score = score;
  r.recommendation = score >= 70
    ? 'High risk detected! This URL shows strong indicators of malicious intent. Do not proceed.'
    : score >= 40
    ? 'Moderate risk detected. Exercise caution before proceeding.'
    : 'Low risk detected. This URL appears relatively safe.';
  return r;
}

// ═══════════════════════════════════════════════════
//  RENDER
// ═══════════════════════════════════════════════════
function renderReport(r, rawUrl) {
  const s = r._score;
  const isH = s >= 70, isM = s >= 40 && s < 70;
  const scoreColor = isH ? 'var(--red-base)' : isM ? 'var(--amber)' : 'var(--green)';

  // URL label
  document.getElementById('resUrl').textContent = rawUrl.length > 55 ? rawUrl.substring(0, 55) + '...' : rawUrl;

  // Verdict pill
  const vp = document.getElementById('verdictPill');
  vp.className = 'verdict-pill ' + (isH ? 'vp-high' : isM ? 'vp-med' : 'vp-low');
  vp.innerHTML = `<span class="vp-dot"></span>${isH ? '⚠ HIGH RISK' : isM ? '⚡ MODERATE' : '✓ SAFE'}`;

  // Recommendation
  const rb = document.getElementById('recBox');
  rb.className = 'rec-box ' + (isH ? 'rec-high' : isM ? 'rec-med' : 'rec-low');
  document.getElementById('recEmoji').textContent = isH ? '🚨' : isM ? '⚠️' : '✅';
  document.getElementById('recTitle').textContent = isH ? 'High Risk Detected' : isM ? 'Moderate Risk' : 'Low Risk';
  document.getElementById('recMsg').textContent = r.recommendation;

  // Insight
  if (r.specific_insights) {
    const strip = document.getElementById('insightStrip');
    strip.style.display = 'flex';
    strip.classList.add('show');
    document.getElementById('insightVal').textContent = r.specific_insights;
  }

  // Show results container
  const res = document.getElementById('results');
  res.style.display = 'block';
  res.classList.add('show');

  // Staggered card reveals
  const cards = ['cardDisk', 'cardFlags', 'cardKV', 'cardCmt'];
  cards.forEach((id, i) => {
    setTimeout(() => document.getElementById(id).classList.add('visible'), i * 120);
  });

  // ── ML SCORE DISK ──
  setTimeout(() => {
    const circumference = 2 * Math.PI * 65; // 408.41
    const offset = circumference - (s / 100 * circumference);
    const prog = document.getElementById('diskProg');
    prog.style.stroke = scoreColor;
    document.getElementById('diskGlow').style.stroke = scoreColor;
    document.getElementById('diskGlow').style.opacity = isH ? '0.08' : '0.05';
    prog.style.strokeDashoffset = offset;

    // Animate number
    const numEl = document.getElementById('diskPct');
    numEl.style.color = scoreColor;
    let cur = 0;
    const iv = setInterval(() => {
      cur = Math.min(cur + 1, s);
      numEl.innerHTML = cur + '<span class="disk-pct-sym">%</span>';
      if (cur >= s) clearInterval(iv);
    }, 1600 / Math.max(s, 1));

    // Pulse rings for high risk
    if (isH) {
      ['pulse1', 'pulse2', 'pulse3'].forEach(id => {
        document.getElementById(id).style.display = 'block';
      });
    }

    // Risk label
    document.getElementById('riskLabel').textContent = isH ? 'CRITICAL' : isM ? 'MODERATE' : 'LOW';
    document.getElementById('riskLabel').style.color = scoreColor;
    document.getElementById('riskType').textContent = 'Type: ' + r.url_type.replace(/_/g, ' ').toUpperCase();
  }, 200);

  // Sub-score bars
  const l = r.data.lexical;
  const subDefs = [
    { label: 'Semantic',    val: l.semantic_score || 0, max: 1,  cls: 'sf-accent' },
    { label: 'Code Risk',   val: l.code_score || 0,     max: 1,  cls: 'sf-accent' },
    { label: 'Entropy',     val: l.entropy || 0,         max: 8,  cls: 'sf-amber'  },
    { label: 'Sym Ratio',   val: l.symbol_ratio || 0,   max: 1,  cls: 'sf-blue'   },
    { label: 'Tags',        val: l.tag_count || 0,       max: 20, cls: 'sf-green'  },
  ];
  const ss = document.getElementById('subScores');
  ss.innerHTML = subDefs.map(d => {
    const pct = Math.min(d.val / d.max * 100, 100);
    const display = typeof d.val === 'number' && !Number.isInteger(d.val) ? d.val.toFixed(2) : d.val;
    return `<div class="ssbar">
      <span class="ssbar-lbl">${d.label}</span>
      <div class="ssbar-track"><div class="ssbar-fill ${d.cls}" style="width:0%" data-w="${pct}%"></div></div>
      <span class="ssbar-val">${display}</span>
    </div>`;
  }).join('');
  setTimeout(() => {
    ss.querySelectorAll('.ssbar-fill').forEach(el => el.style.width = el.dataset.w);
  }, 400);

  // ── BEHAVIOUR FLAGS ──
  const beh = r.data.behaviour;
  const flagDefs = {
    risky_mime: 'RISKY MIME', base64: 'BASE64',
    hidden_html: 'HIDDEN HTML', is_unknown: 'UNKNOWN',
    small_payload: 'SMALL PAYLOAD', uses_ip: 'IP ADDRESS',
    long_subdomain: 'DEEP SUBDOMAIN'
  };
  document.getElementById('flagsGrid').innerHTML =
    Object.entries(flagDefs).filter(([k]) => beh[k] !== undefined).map(([k, lbl]) => `
      <div class="flag ${beh[k] ? 'flag-on' : 'flag-ok'}">
        <div class="flag-dot"></div>${lbl}
      </div>`).join('');

  // ── KV LIST ──
  document.getElementById('kvList').innerHTML =
    Object.entries(r.parsed_url).map(([k, v]) => {
      let cls = 'kv-v', val = String(v);
      if (k === 'donnees_decodees') cls = 'kv-v v-danger';
      if (k === 'donnees_totales') val = val.substring(0, 38) + '...';
      if (typeof v === 'boolean') val = `<span class="kv-bool ${v ? 'bool-t' : 'bool-f'}">${v}</span>`;
      return `<div class="kv-row">
        <div class="kv-k">${k.replace(/_/g, ' ').toUpperCase()}</div>
        <div class="${cls}">${val}</div>
      </div>`;
    }).join('');

  // ── COMMENTS with staggered appear ──
  const allCmts = [
    ...(r.comments.lexical || []).map(t => ({ t, src: 'LEX' })),
    ...(r.comments.behaviour || []).map(t => ({ t, src: 'BEH' }))
  ];
  const dangerKw = /dangerous|risky|phishing|obfusc|suspicious|base64|hidden|executable|IP address|injection/i;
  const okKw = /no harmful|no suspicious|no password/i;
  const cl = document.getElementById('cmtList');
  cl.innerHTML = allCmts.map((c, i) => {
    const type = okKw.test(c.t) ? 'ok' : dangerKw.test(c.t) ? 'danger' : 'warn';
    const icon = type === 'ok' ? '✓' : type === 'danger' ? '⚠' : '→';
    return `<div class="cmt cmt-${type}" id="cmt${i}">
      <span class="cmt-icon">${icon}</span>${c.t}
    </div>`;
  }).join('');

  // Stagger comments
  allCmts.forEach((_, i) => {
    setTimeout(() => {
      const el = document.getElementById('cmt' + i);
      if (el) el.classList.add('visible');
    }, 600 + i * 110);
  });

  res.scrollIntoView({ behavior: 'smooth', block: 'start' });}