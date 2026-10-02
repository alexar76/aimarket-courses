/**
 * Dual-orbit hybrid seal — Canvas 2D “wow” for the course hero.
 * Cyan ring = Ed25519, violet ring = ML-DSA-65, center crystal = receipt,
 * seal stamps both orbits with particle trails. Decorative only — not crypto.
 */
(function () {
  function boot() {
    const canvas = document.getElementById("wow-canvas");
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext("2d");
    const caption = document.getElementById("wow-caption");

    let w = 0;
    let h = 0;
    let dpr = 1;
    let t0 = performance.now();
    let sealPulse = 0;
    const particles = [];

    function resize() {
      const parent = canvas.parentElement || canvas;
      const rect = parent.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = Math.max(280, Math.floor(rect.width || 640));
      h = Math.max(220, Math.floor(Math.min(340, w * 0.48)));
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function spawnTrail(x, y, color, vx, vy) {
      particles.push({
        x,
        y,
        vx: vx + (Math.random() - 0.5) * 0.4,
        vy: vy + (Math.random() - 0.5) * 0.4,
        life: 1,
        color,
        r: 1.2 + Math.random() * 2.2,
      });
    }

    function drawRing(cx, cy, rx, ry, angle, color, reverse, stamp) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(angle * (reverse ? -1 : 1));
      ctx.scale(1, 0.42); // 3D-ish foreshortening
      ctx.beginPath();
      ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
      ctx.strokeStyle = color;
      ctx.lineWidth = 2.4;
      ctx.shadowColor = color;
      ctx.shadowBlur = 14;
      ctx.stroke();
      ctx.shadowBlur = 0;

      // orbit bead
      const beadA = stamp ? stamp : 0;
      const bx = Math.cos(beadA) * rx;
      const by = Math.sin(beadA) * ry;
      ctx.beginPath();
      ctx.arc(bx, by, 4.5, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();

      // project bead back for particles (undo scale/rotate approximately)
      ctx.restore();
      const sx = cx + Math.cos(angle * (reverse ? -1 : 1) + beadA) * rx;
      const sy = cy + Math.sin(angle * (reverse ? -1 : 1) + beadA) * ry * 0.42;
      spawnTrail(sx, sy, color, reverse ? -0.3 : 0.3, 0.15);
      return { x: sx, y: sy };
    }

    function drawCrystal(cx, cy, pulse) {
      const s = 22 + pulse * 6;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(Math.PI / 4);
      const g = ctx.createLinearGradient(-s, -s, s, s);
      g.addColorStop(0, "rgba(103,232,249,0.95)");
      g.addColorStop(0.5, "rgba(255,255,255,0.9)");
      g.addColorStop(1, "rgba(192,132,252,0.95)");
      ctx.fillStyle = g;
      ctx.strokeStyle = "rgba(255,255,255,0.65)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(0, -s);
      ctx.lineTo(s * 0.7, 0);
      ctx.lineTo(0, s);
      ctx.lineTo(-s * 0.7, 0);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    }

    function drawSealStamp(x, y, alpha) {
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(x, y);
      ctx.beginPath();
      ctx.arc(0, 0, 10, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(255,255,255,0.85)";
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(0, 0, 5, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(52,211,153,0.85)";
      ctx.fill();
      ctx.restore();
    }

    function frame(now) {
      const t = (now - t0) / 1000;
      ctx.clearRect(0, 0, w, h);

      // soft vignette
      const bg = ctx.createRadialGradient(w * 0.5, h * 0.55, 10, w * 0.5, h * 0.5, w * 0.55);
      bg.addColorStop(0, "rgba(14,20,32,0.15)");
      bg.addColorStop(1, "rgba(7,11,18,0)");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, w, h);

      const cx = w * 0.5;
      const cy = h * 0.52;
      const a1 = t * 0.85;
      const a2 = t * 1.05;
      sealPulse = 0.5 + 0.5 * Math.sin(t * 2.2);

      const cyan = "rgba(103,232,249,0.92)";
      const violet = "rgba(192,132,252,0.92)";

      const p1 = drawRing(cx, cy, Math.min(w, h) * 0.38, Math.min(w, h) * 0.38, a1, cyan, false, t * 2.4);
      const p2 = drawRing(cx, cy, Math.min(w, h) * 0.28, Math.min(w, h) * 0.28, a2, violet, true, -t * 2.8);

      drawCrystal(cx, cy, sealPulse);

      // seal stamps hit both orbits periodically
      const stampPhase = (Math.sin(t * 1.6) + 1) / 2;
      if (stampPhase > 0.72) {
        const a = (stampPhase - 0.72) / 0.28;
        drawSealStamp(p1.x, p1.y, a);
        drawSealStamp(p2.x, p2.y, a);
      }

      // particles
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life -= 0.018;
        if (p.life <= 0) {
          particles.splice(i, 1);
          continue;
        }
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * p.life, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
        ctx.globalAlpha = 1;
      }
      if (particles.length > 220) particles.splice(0, particles.length - 220);

      // labels
      ctx.font = "600 11px 'Space Grotesk', sans-serif";
      ctx.fillStyle = cyan;
      ctx.fillText("Ed25519", 16, 22);
      ctx.fillStyle = violet;
      ctx.fillText("ML-DSA-65", 16, 38);
      ctx.fillStyle = "rgba(226,232,240,0.75)";
      ctx.fillText("receipt", cx - 18, cy + Math.min(w, h) * 0.22);

      requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener("resize", resize);
    if (caption && !caption.textContent) {
      caption.textContent = "Dual orbits · one sealed receipt";
    }
    requestAnimationFrame(frame);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
