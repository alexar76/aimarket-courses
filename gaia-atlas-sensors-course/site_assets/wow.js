/* GAIA/ATLAS sensor mesh — 3D-ish rotating globe, LIVE pins, particle atmosphere.
   Canvas 2D only (no three.js). Scene id feel: sensor mesh. */
(() => {
  const canvas = document.getElementById("wow");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W = 0, H = 0, DPR = 1;
  const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
  let t = 0;

  const PINS = [
    { lat: 52.52, lon: 13.41, live: true, label: "om-wx-01" },
    { lat: 37.62, lon: -122.37, live: true, label: "nws" },
    { lat: 35.68, lon: 139.76, live: true, label: "om-jp" },
    { lat: -33.87, lon: 151.21, live: true, label: "om-au" },
    { lat: 40.71, lon: -74.01, live: true, label: "marine" },
    { lat: 51.5, lon: -0.12, live: true, label: "uk" },
    { lat: 46.95, lon: 7.45, live: false, label: "ws-01" },
    { lat: 1.35, lon: 103.82, live: true, label: "om-sg" },
    { lat: -23.55, lon: -46.63, live: true, label: "om-br" },
    { lat: 55.75, lon: 37.62, live: true, label: "om-ru" },
  ];

  function resize() {
    const parent = canvas.parentElement || document.body;
    const rect = parent.getBoundingClientRect();
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.width = Math.max(320, rect.width) * DPR;
    H = canvas.height = Math.max(220, rect.height) * DPR;
    canvas.style.width = Math.max(320, rect.width) + "px";
    canvas.style.height = Math.max(220, rect.height) + "px";
  }
  resize();
  addEventListener("resize", resize);

  function aim(x, y) {
    const r = canvas.getBoundingClientRect();
    mouse.tx = (x - r.left) / Math.max(r.width, 1) - 0.5;
    mouse.ty = (y - r.top) / Math.max(r.height, 1) - 0.5;
  }
  addEventListener("mousemove", (e) => aim(e.clientX, e.clientY));
  addEventListener(
    "touchmove",
    (e) => {
      if (e.touches[0]) aim(e.touches[0].clientX, e.touches[0].clientY);
    },
    { passive: true }
  );

  const PARTICLE_N = reduce ? 40 : 110;
  const particles = Array.from({ length: PARTICLE_N }, () => ({
    a: Math.random() * Math.PI * 2,
    b: (Math.random() - 0.5) * Math.PI,
    r: 0.55 + Math.random() * 0.55,
    s: 0.2 + Math.random() * 0.8,
    c: Math.random() > 0.5 ? "103,232,249" : "52,211,153",
  }));

  function project(lat, lon, rotY, rotX, R) {
    const φ = (lat * Math.PI) / 180;
    const λ = (lon * Math.PI) / 180 + rotY;
    let x = Math.cos(φ) * Math.sin(λ);
    let y = Math.sin(φ);
    let z = Math.cos(φ) * Math.cos(λ);
    const cx = Math.cos(rotX), sx = Math.sin(rotX);
    const y2 = y * cx - z * sx;
    const z2 = y * sx + z * cx;
    y = y2;
    z = z2;
    const cx0 = W * 0.58 + mouse.x * 28 * DPR;
    const cy0 = H * 0.52 + mouse.y * 18 * DPR;
    return {
      x: cx0 + x * R,
      y: cy0 - y * R,
      z,
      visible: z > -0.15,
    };
  }

  function drawGlobe(R, rotY, rotX) {
    const cx0 = W * 0.58 + mouse.x * 28 * DPR;
    const cy0 = H * 0.52 + mouse.y * 18 * DPR;

    // atmosphere glow
    const glow = ctx.createRadialGradient(cx0, cy0, R * 0.55, cx0, cy0, R * 1.35);
    glow.addColorStop(0, "rgba(103,232,249,0.10)");
    glow.addColorStop(0.55, "rgba(52,211,153,0.05)");
    glow.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(cx0, cy0, R * 1.35, 0, Math.PI * 2);
    ctx.fill();

    // sphere body
    const body = ctx.createRadialGradient(
      cx0 - R * 0.35,
      cy0 - R * 0.4,
      R * 0.1,
      cx0,
      cy0,
      R
    );
    body.addColorStop(0, "rgba(30,58,95,0.55)");
    body.addColorStop(0.45, "rgba(12,24,42,0.72)");
    body.addColorStop(1, "rgba(4,10,18,0.9)");
    ctx.beginPath();
    ctx.arc(cx0, cy0, R, 0, Math.PI * 2);
    ctx.fillStyle = body;
    ctx.fill();

    // meridians / parallels
    ctx.strokeStyle = "rgba(103,232,249,0.14)";
    ctx.lineWidth = Math.max(1, 1 * DPR);
    for (let i = -2; i <= 2; i++) {
      ctx.beginPath();
      for (let lon = -180; lon <= 180; lon += 6) {
        const p = project(i * 28, lon, rotY, rotX, R);
        if (lon === -180) ctx.moveTo(p.x, p.y);
        else if (p.visible) ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }
    for (let lon = 0; lon < 180; lon += 30) {
      ctx.beginPath();
      let started = false;
      for (let lat = -80; lat <= 80; lat += 4) {
        const p = project(lat, lon, rotY, rotX, R);
        if (!p.visible) {
          started = false;
          continue;
        }
        if (!started) {
          ctx.moveTo(p.x, p.y);
          started = true;
        } else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }

    // rim
    ctx.strokeStyle = "rgba(103,232,249,0.35)";
    ctx.lineWidth = 1.5 * DPR;
    ctx.beginPath();
    ctx.arc(cx0, cy0, R, 0, Math.PI * 2);
    ctx.stroke();
  }

  function drawPins(R, rotY, rotX) {
    const pulse = 0.55 + 0.45 * Math.sin(t * 0.08);
    for (const pin of PINS) {
      const p = project(pin.lat, pin.lon, rotY, rotX, R * 1.02);
      if (!p.visible) continue;
      const depth = (p.z + 1) / 2;
      const r = (pin.live ? 3.2 : 2.2) * DPR * (0.65 + depth * 0.5);
      const color = pin.live ? "103,232,249" : "148,163,184";
      if (pin.live) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, r * (2.8 + pulse), 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${color},${0.12 + 0.1 * pulse})`;
        ctx.fill();
      }
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${color},${0.55 + depth * 0.4})`;
      ctx.fill();
      if (pin.live && depth > 0.45) {
        ctx.fillStyle = `rgba(226,232,240,${0.35 + depth * 0.4})`;
        ctx.font = `${10 * DPR}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillText(pin.label, p.x + 6 * DPR, p.y - 4 * DPR);
      }
    }
  }

  function drawParticles(R, rotY, rotX) {
    for (const q of particles) {
      const lat = (q.b * 180) / Math.PI;
      const lon = ((q.a + t * 0.004 * q.s) * 180) / Math.PI;
      const p = project(lat, lon, rotY, rotX, R * q.r);
      if (!p.visible) continue;
      const alpha = 0.15 + 0.35 * ((p.z + 1) / 2);
      ctx.fillStyle = `rgba(${q.c},${alpha})`;
      ctx.fillRect(p.x, p.y, 1.6 * DPR, 1.6 * DPR);
    }
  }

  function frame() {
    t += reduce ? 0.35 : 1;
    mouse.x += (mouse.tx - mouse.x) * 0.06;
    mouse.y += (mouse.ty - mouse.y) * 0.06;
    ctx.clearRect(0, 0, W, H);

    // soft mesh backdrop
    ctx.fillStyle = "rgba(7,11,18,0.15)";
    ctx.fillRect(0, 0, W, H);

    const R = Math.min(W, H) * 0.34;
    const rotY = t * (reduce ? 0.0025 : 0.0065) + mouse.x * 0.9;
    const rotX = 0.35 + mouse.y * 0.35;

    drawGlobe(R, rotY, rotX);
    drawParticles(R, rotY, rotX);
    drawPins(R, rotY, rotX);

    // scan arc
    const cx0 = W * 0.58 + mouse.x * 28 * DPR;
    const cy0 = H * 0.52 + mouse.y * 18 * DPR;
    const sweep = (t * 0.02) % (Math.PI * 2);
    ctx.beginPath();
    ctx.strokeStyle = "rgba(52,211,153,0.25)";
    ctx.lineWidth = 2 * DPR;
    ctx.arc(cx0, cy0, R * 1.08, sweep, sweep + 0.9);
    ctx.stroke();

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
