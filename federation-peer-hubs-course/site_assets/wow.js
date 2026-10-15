/**
 * Federation peer graph — Canvas 2D hero.
 * Glowing hub nodes, announce pulses, quarantine ring on pending, approve flash bridging edges.
 * Parallax on pointer move. Pure canvas — no deps.
 */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var canvas = document.getElementById("federation-wow");
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0, H = 0;
    var t0 = performance.now();
    var pointer = { x: 0.5, y: 0.35, tx: 0.5, ty: 0.35 };
    var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var hubs = [
      { id: "hub", label: "modelmarket", role: "hub", r: 18 },
      { id: "atlas", label: "ATLAS", role: "trusted", r: 11 },
      { id: "gaia", label: "GAIA", role: "trusted", r: 11 },
      { id: "oracles", label: "oracles", role: "trusted", r: 10 },
      { id: "factory", label: "factory", role: "trusted", r: 10 },
      { id: "stranger", label: "stranger", role: "pending", r: 12 },
    ];

    var edges = [
      ["hub", "atlas"],
      ["hub", "gaia"],
      ["hub", "oracles"],
      ["hub", "factory"],
    ];

    var pulses = [];
    var approveFlash = 0;
    var bridged = false;
    var phase = 0; // 0 announce, 1 quarantine, 2 approve, 3 bridged hold

    function layout() {
      var rect = canvas.getBoundingClientRect();
      W = Math.max(320, rect.width);
      H = Math.max(220, rect.height);
      canvas.width = Math.floor(W * dpr);
      canvas.height = Math.floor(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      var cx = W * 0.52, cy = H * 0.48;
      hubs[0].x = cx;
      hubs[0].y = cy;
      var orbit = Math.min(W, H) * 0.32;
      for (var i = 1; i < hubs.length; i++) {
        var a = (i - 1) / (hubs.length - 1) * Math.PI * 1.55 - Math.PI * 0.85;
        if (hubs[i].role === "pending") {
          hubs[i].x = cx + orbit * 1.05;
          hubs[i].y = cy - orbit * 0.15;
        } else {
          hubs[i].x = cx + Math.cos(a) * orbit;
          hubs[i].y = cy + Math.sin(a) * orbit * 0.78;
        }
        hubs[i].ox = hubs[i].x;
        hubs[i].oy = hubs[i].y;
      }
      hubs[0].ox = cx;
      hubs[0].oy = cy;
    }

    function spawnPulse() {
      pulses.push({ from: "stranger", to: "hub", u: 0, life: 1 });
    }

    function byId(id) {
      for (var i = 0; i < hubs.length; i++) if (hubs[i].id === id) return hubs[i];
      return null;
    }

    function drawGlow(x, y, r, color, alpha) {
      var g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, color.replace("ALP", String(alpha)));
      g.addColorStop(1, color.replace("ALP", "0"));
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }

    function drawNode(n, time) {
      var px = (pointer.x - 0.5) * (n.role === "hub" ? 8 : 18);
      var py = (pointer.y - 0.5) * (n.role === "hub" ? 6 : 14);
      var x = n.ox + px;
      var y = n.oy + py + Math.sin(time * 0.0012 + (n.r || 10)) * (n.role === "pending" ? 2.5 : 1.2);
      n.x = x;
      n.y = y;

      if (n.role === "hub") {
        drawGlow(x, y, 56, "rgba(103,232,249,ALP)", 0.35);
        drawGlow(x, y, 28, "rgba(192,132,252,ALP)", 0.4);
      } else if (n.role === "pending") {
        drawGlow(x, y, 40, "rgba(251,113,133,ALP)", 0.28);
      } else {
        drawGlow(x, y, 26, "rgba(52,211,153,ALP)", 0.22);
      }

      if (n.role === "pending") {
        var ringR = n.r + 10 + Math.sin(time * 0.004) * 2;
        ctx.strokeStyle = "rgba(251,113,133,0.85)";
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 5]);
        ctx.beginPath();
        ctx.arc(x, y, ringR, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.strokeStyle = "rgba(251,113,133,0.25)";
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.arc(x, y, ringR + 6, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.beginPath();
      ctx.arc(x, y, n.r, 0, Math.PI * 2);
      if (n.role === "hub") {
        ctx.fillStyle = "rgba(14,20,32,0.95)";
        ctx.fill();
        ctx.strokeStyle = "rgba(103,232,249,0.95)";
        ctx.lineWidth = 2.5;
        ctx.stroke();
      } else if (n.role === "pending") {
        ctx.fillStyle = "rgba(30,12,18,0.95)";
        ctx.fill();
        ctx.strokeStyle = "rgba(251,113,133,0.9)";
        ctx.lineWidth = 2;
        ctx.stroke();
      } else {
        ctx.fillStyle = "rgba(10,24,20,0.95)";
        ctx.fill();
        ctx.strokeStyle = "rgba(52,211,153,0.85)";
        ctx.lineWidth = 1.8;
        ctx.stroke();
      }

      ctx.fillStyle = "rgba(238,242,255,0.88)";
      ctx.font = "600 11px Space Grotesk, system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(n.label, x, y + n.r + 16);
    }

    function drawEdge(a, b, alpha, flash) {
      var A = byId(a), B = byId(b);
      if (!A || !B) return;
      ctx.beginPath();
      ctx.moveTo(A.x, A.y);
      ctx.lineTo(B.x, B.y);
      if (flash > 0) {
        ctx.strokeStyle = "rgba(167,139,250," + (0.35 + flash * 0.65) + ")";
        ctx.lineWidth = 2 + flash * 3;
        ctx.shadowColor = "rgba(192,132,252,0.8)";
        ctx.shadowBlur = 18 * flash;
      } else {
        ctx.strokeStyle = "rgba(148,163,184," + alpha + ")";
        ctx.lineWidth = 1.2;
        ctx.shadowBlur = 0;
      }
      ctx.stroke();
      ctx.shadowBlur = 0;
    }

    function drawPulse(p, time) {
      var A = byId(p.from), B = byId(p.to);
      if (!A || !B) return;
      p.u += 0.011 * p.life;
      if (p.u > 1) return false;
      var x = A.x + (B.x - A.x) * p.u;
      var y = A.y + (B.y - A.y) * p.u;
      drawGlow(x, y, 18, "rgba(251,191,36,ALP)", 0.55 * (1 - p.u));
      ctx.beginPath();
      ctx.arc(x, y, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(253,224,71,0.95)";
      ctx.fill();
      return true;
    }

    function tick(now) {
      var time = now - t0;
      pointer.x += (pointer.tx - pointer.x) * 0.06;
      pointer.y += (pointer.ty - pointer.y) * 0.06;

      // Narrative loop: announce → quarantine hold → approve flash → bridge
      var cycle = reduced ? 0 : (time % 12000);
      if (!reduced) {
        if (cycle < 3500) {
          phase = 0;
          if (Math.random() < 0.04) spawnPulse();
          bridged = false;
          approveFlash = Math.max(0, approveFlash - 0.02);
        } else if (cycle < 7000) {
          phase = 1;
          approveFlash = Math.max(0, approveFlash - 0.02);
        } else if (cycle < 8500) {
          phase = 2;
          approveFlash = Math.min(1, approveFlash + 0.08);
          bridged = true;
        } else {
          phase = 3;
          approveFlash = Math.max(0.25, approveFlash - 0.01);
          bridged = true;
        }
      } else {
        bridged = true;
        approveFlash = 0.35;
      }

      ctx.clearRect(0, 0, W, H);

      // Parallax star dust
      var dx = (pointer.x - 0.5) * 20;
      var dy = (pointer.y - 0.5) * 14;
      for (var s = 0; s < 48; s++) {
        var sx = ((s * 97) % W) + dx * (0.2 + (s % 5) * 0.05);
        var sy = ((s * 53) % H) + dy * (0.15 + (s % 4) * 0.04);
        ctx.fillStyle = "rgba(226,232,240," + (0.08 + (s % 7) * 0.02) + ")";
        ctx.fillRect(sx, sy, 1.2, 1.2);
      }

      // Soft vignette plane
      var bg = ctx.createRadialGradient(W * 0.5, H * 0.45, 20, W * 0.5, H * 0.5, Math.max(W, H) * 0.55);
      bg.addColorStop(0, "rgba(103,232,249,0.05)");
      bg.addColorStop(0.55, "rgba(192,132,252,0.03)");
      bg.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, W, H);

      for (var e = 0; e < edges.length; e++) {
        drawEdge(edges[e][0], edges[e][1], 0.22, 0);
      }
      if (bridged) {
        drawEdge("hub", "stranger", 0.35, approveFlash);
      }

      pulses = pulses.filter(function (p) { return drawPulse(p, time); });

      for (var i = 0; i < hubs.length; i++) drawNode(hubs[i], time);

      // Caption chip
      var caption =
        phase === 0 ? "announce knock →" :
        phase === 1 ? "preview quarantine" :
        phase === 2 ? "approve flash" :
        "peer bridged";
      ctx.fillStyle = "rgba(14,20,32,0.72)";
      ctx.strokeStyle = "rgba(148,163,184,0.22)";
      ctx.lineWidth = 1;
      var cw = ctx.measureText(caption).width + 28;
      var cx = 16, cy = H - 36;
      roundRect(ctx, cx, cy, cw, 26, 13);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = "rgba(167,243,208,0.95)";
      ctx.font = "600 11px JetBrains Mono, ui-monospace, monospace";
      ctx.textAlign = "left";
      ctx.fillText(caption, cx + 14, cy + 17);

      requestAnimationFrame(tick);
    }

    function roundRect(c, x, y, w, h, r) {
      c.beginPath();
      c.moveTo(x + r, y);
      c.arcTo(x + w, y, x + w, y + h, r);
      c.arcTo(x + w, y + h, x, y + h, r);
      c.arcTo(x, y + h, x, y, r);
      c.arcTo(x, y, x + w, y, r);
      c.closePath();
    }

    function onMove(ev) {
      var rect = canvas.getBoundingClientRect();
      pointer.tx = (ev.clientX - rect.left) / Math.max(1, rect.width);
      pointer.ty = (ev.clientY - rect.top) / Math.max(1, rect.height);
    }

    window.addEventListener("resize", layout);
    canvas.addEventListener("pointermove", onMove);
    layout();
    requestAnimationFrame(tick);
  });
})();
