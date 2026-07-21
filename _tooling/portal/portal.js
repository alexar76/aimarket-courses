/* AIMarket Courses portal — starfield + academy node graph */
(() => {
  const canvas = document.getElementById('galaxy');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W, H, DPR, cx, cy;
  const mouse = { x: 0, y: 0, tx: 0, ty: 0 };

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.width = innerWidth * DPR;
    H = canvas.height = innerHeight * DPR;
    canvas.style.width = innerWidth + 'px';
    canvas.style.height = innerHeight + 'px';
    cx = W / 2;
    cy = H / 2;
  }
  resize();
  addEventListener('resize', resize);
  function aim(x, y) {
    mouse.tx = x / innerWidth - 0.5;
    mouse.ty = y / innerHeight - 0.5;
  }
  addEventListener('mousemove', (e) => aim(e.clientX, e.clientY));
  addEventListener('touchmove', (e) => {
    if (e.touches[0]) aim(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: true });

  const area = innerWidth * innerHeight;
  const COUNT = Math.max(120, Math.min(420, Math.floor(area / 2800)));
  const stars = [];
  const palette = ['#38e0ff', '#7b5cff', '#9fe9ff', '#ffffff', '#38ffa6'];
  for (let i = 0; i < COUNT; i++) {
    stars.push({
      x: Math.random() * 2 - 1,
      y: Math.random() * 2 - 1,
      z: Math.random() * 0.9 + 0.1,
      r: Math.random() * 1.3 + 0.35,
      c: palette[(Math.random() * palette.length) | 0],
      tw: Math.random() * Math.PI * 2,
    });
  }

  const NODE_LABELS = ['Labs', 'Oracles', 'Trust', 'MCP', 'Hub', 'Proofs', 'Colab', 'Factory'];
  const nodes = NODE_LABELS.map((label, i) => {
    const a = (i / NODE_LABELS.length) * Math.PI * 2;
    return {
      a,
      rad: 0.28 + (i % 3) * 0.06,
      spd: 0.00016 + (i % 4) * 0.00005,
      size: 2.2 + (i % 3),
      c: i % 2 ? '#7b5cff' : '#38e0ff',
      label,
    };
  });

  const warp = reduce ? 0.0003 : 0.0016;
  const drift = reduce ? 0.22 : 1;
  let t = 0;

  function frame() {
    t += 1;
    mouse.x += (mouse.tx - mouse.x) * 0.05;
    mouse.y += (mouse.ty - mouse.y) * 0.05;
    ctx.clearRect(0, 0, W, H);

    const minDim = Math.min(W, H);
    const maxDim = Math.max(W, H);
    const px = mouse.x * 0.09 * minDim;
    const py = mouse.y * 0.09 * minDim;
    const spread = maxDim * 0.58;

    for (const s of stars) {
      s.z -= warp;
      if (s.z <= 0.02) {
        s.z = 1;
        s.x = Math.random() * 2 - 1;
        s.y = Math.random() * 2 - 1;
      }
      const k = 1 / s.z;
      const sx = cx + (s.x * spread * k) + px * k * 0.4;
      const sy = cy + (s.y * spread * k) + py * k * 0.4;
      const tw = 0.55 + 0.45 * Math.sin(t * 0.04 + s.tw);
      ctx.globalAlpha = tw * (1 - s.z * 0.35);
      ctx.fillStyle = s.c;
      ctx.beginPath();
      ctx.arc(sx, sy, s.r * k * DPR * 0.9, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    const positions = [];
    for (const n of nodes) {
      n.a += n.spd * drift;
      const nx = cx + Math.cos(n.a) * n.rad * minDim + px * 0.35;
      const ny = cy + Math.sin(n.a) * n.rad * minDim * 0.55 + py * 0.35;
      positions.push({ x: nx, y: ny, n });
    }
    ctx.strokeStyle = 'rgba(56,224,255,0.08)';
    ctx.lineWidth = DPR;
    for (let i = 0; i < positions.length; i++) {
      const a = positions[i];
      const b = positions[(i + 2) % positions.length];
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }
    for (const p of positions) {
      const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.n.size * 4 * DPR);
      g.addColorStop(0, p.n.c);
      g.addColorStop(1, 'transparent');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.n.size * 4 * DPR, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(frame);
  }
  frame();
})();

/* Track filters */
(() => {
  const btns = document.querySelectorAll('.filter-btn');
  const tracks = document.querySelectorAll('[data-track]');
  if (!btns.length) return;
  btns.forEach((btn) => {
    btn.addEventListener('click', () => {
      btns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const track = btn.dataset.filter;
      tracks.forEach((el) => {
        el.hidden = track !== 'all' && el.dataset.track !== track;
      });
    });
  });
})();
