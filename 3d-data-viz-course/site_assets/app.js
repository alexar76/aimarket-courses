(function () {
  const state = { lang: "en", data: null };

  function exerciseMods() {
    return state.data?.exerciseModules || state.data?.modules || [];
  }

  function t(key) {
    const cat = state.data.catalogs[state.lang] || state.data.catalogs.en;
    const parts = key.split(".");
    let node = cat;
    for (const p of parts) {
      if (!node || typeof node !== "object" || !(p in node)) return key;
      node = node[p];
    }
    return typeof node === "string" ? node : key;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function githubBlob(path) {
    const sub = state.data.repoSubpath ? `${state.data.repoSubpath}/` : "";
    return `https://github.com/${state.data.repo}/blob/main/${sub}${path}`;
  }

  function quickstartCommands() {
    const base = state.data.quickstartCommands || [];
    const name = t("site.certificate_name_placeholder") || "Your Name";
    return [...base, `python labs/run_exercises.py --certificate "${name}"`];
  }

  function labForModule(mod) {
    return state.data.labs.find((l) => l.module === mod);
  }

  function labStems() {
    return state.data.labs.map((l) => l.stem);
  }

  function trackPill(track) {
    if (track === "economy") return `<span class="pill track-economy">${t("site.hub_lite")}</span>`;
    if (track === "advanced") return `<span class="pill track-advanced">${t("site.advanced")}</span>`;
    return "";
  }

  function renderCertificatePanel() {
    const panel = document.getElementById("certificate-panel");
    if (!panel) return;
    const mods = exerciseMods();
    const sum = CourseProgress.summary(labStems(), mods);
    const total = sum.labsTotal + sum.exTotal;
    const done = sum.labsDone + sum.exDone;
    const pct = total ? Math.round((done / total) * 100) : 0;
    const namePh = t("site.certificate_name_placeholder") || "Your Name";
    const cmd = `python labs/run_exercises.py --certificate "${namePh}"`;

    // Optional personal progress (labs only) — does NOT unlock a browser certificate.
    let labRows = "";
    for (const lab of state.data.labs) {
      const modInfo = (state.data.catalogs[state.lang]?.modules || {})[lab.module] || {};
      const checked = CourseProgress.isLabDone(lab.stem) ? "checked" : "";
      labRows += `
        <label class="check-row">
          <input type="checkbox" data-lab="${lab.stem}" ${checked} />
          <span>${modInfo.title || lab.stem}</span>
        </label>`;
    }

    panel.innerHTML = `
      <p class="cert-intro">${t("site.certificate_intro")}</p>
      <div class="progress-bar" aria-hidden="true"><div class="progress-fill" style="width:${pct}%"></div></div>
      <p class="progress-label">${t("site.certificate_progress")}: ${done}/${total} (${pct}%) · ${t("site.certificate_progress_local")}</p>
      <div class="cert-grid">
        <div>
          <h3>${t("site.certificate_labs")}</h3>
          <div class="checklist">${labRows}</div>
        </div>
        <div>
          <h3>${t("site.certificate_exercises")}</h3>
          <p class="cert-hint">${t("site.certificate_exercises_cli")}</p>
          <pre class="cert-cli"><code>${cmd.replace(/</g, "&lt;")}</code></pre>
          <p class="note">${t("site.certificate_no_skip")}</p>
        </div>
      </div>
      <p class="cert-hint">${t("site.certificate_locked")}</p>`;

    panel.querySelectorAll("[data-lab]").forEach((el) => {
      el.addEventListener("change", () => {
        CourseProgress.setLabDone(el.dataset.lab, el.checked);
        renderCertificatePanel();
        renderLabs();
        renderModules();
      });
    });
  }

  function renderModules() {
    const grid = document.getElementById("modules-grid");
    if (!grid) return;
    grid.innerHTML = "";
    for (const mod of state.data.modules) {
      const info = (state.data.catalogs[state.lang].modules || {})[mod] || {};
      const lab = labForModule(mod);
      const card = document.createElement("article");
      card.className = "card";
      const title = info.title || mod;
      const concept = info.concept || "";
      const industry = info.industry || "";
      let pills = `<span class="pill">${mod.toUpperCase()}</span>`;
      let actions = "";
      if (lab) {
        const done = CourseProgress.isLabDone(lab.stem);
        pills += `<span class="pill lab">${t("site.has_lab")}</span>`;
        if (done) pills += `<span class="pill done">${t("site.certificate_mark_done")}</span>`;
        pills += trackPill(lab.track);
        actions = `
          <div class="actions">
            <a class="btn primary" href="${lab.colab}" target="_blank" rel="noopener">${t("site.open_colab")}</a>
            <a href="${githubBlob(lab.script)}">${t("site.view_source")}</a>
            <button type="button" class="btn mark-lab" data-stem="${lab.stem}">${done ? t("site.certificate_mark_done") : t("site.certificate_mark_lab")}</button>
          </div>`;
      } else {
        pills += `<span class="pill soon">${t("site.coming_soon")}</span>`;
      }
      card.innerHTML = `
        <h3>${escapeHtml(title)}</h3>
        <div class="meta">${escapeHtml(industry)}</div>
        <p>${escapeHtml(concept)}</p>
        ${pills}
        ${actions}`;
      grid.appendChild(card);
    }
    grid.querySelectorAll(".mark-lab").forEach((btn) => {
      btn.addEventListener("click", () => {
        const stem = btn.dataset.stem;
        CourseProgress.setLabDone(stem, !CourseProgress.isLabDone(stem));
        renderModules();
        renderLabs();
        renderCertificatePanel();
      });
    });
  }

  function renderLabs() {
    const list = document.getElementById("labs-grid");
    if (!list) return;
    list.innerHTML = "";
    for (const lab of state.data.labs) {
      const mod = lab.module.toUpperCase();
      const modInfo = (state.data.catalogs[state.lang].modules || {})[lab.module] || {};
      const done = CourseProgress.isLabDone(lab.stem);
      const item = document.createElement("article");
      item.className = "card";
      item.innerHTML = `
        <h3>${escapeHtml(modInfo.title || lab.stem)} ${done ? '<span class="pill done">' + t("site.certificate_mark_done") + "</span>" : ""}</h3>
        <div class="meta">${t("site.module")} ${mod} · ${lab.track}</div>
        <pre class="lab-doc">${escapeHtml(lab.docstring)}</pre>
        <div class="actions">
          <a class="btn primary" href="${lab.colab}" target="_blank" rel="noopener">${t("site.open_colab")}</a>
          <a href="${githubBlob(lab.script)}">${t("site.view_source")}</a>
          <button type="button" class="btn mark-lab" data-stem="${lab.stem}">${done ? t("site.certificate_mark_done") : t("site.certificate_mark_lab")}</button>
        </div>
        <p class="run-local">${t("site.run_local")}: <code class="inline">python ${lab.script}</code></p>`;
      list.appendChild(item);
    }
    list.querySelectorAll(".mark-lab").forEach((btn) => {
      btn.addEventListener("click", () => {
        const stem = btn.dataset.stem;
        CourseProgress.setLabDone(stem, !CourseProgress.isLabDone(stem));
        renderModules();
        renderLabs();
        renderCertificatePanel();
      });
    });
  }

  function renderQuickstart() {
    const panel = document.getElementById("quickstart-panel");
    if (!panel) return;
    const cmds = quickstartCommands();
    const lines = cmds
      .map((cmd) => `<span class="terminal-line"><span class="prompt">$ </span><span class="cmd">${escapeHtml(cmd)}</span></span>`)
      .join("");
    const termTitle = state.data.repoSubpath || "course";
    panel.innerHTML = `
      <p class="quickstart-intro">${t("site.quickstart_intro")}</p>
      <div class="terminal">
        <div class="terminal-bar">
          <div class="terminal-dots" aria-hidden="true"><span></span><span></span><span></span></div>
          <div class="terminal-title">${escapeHtml(termTitle)}</div>
          <button type="button" class="terminal-copy" id="quickstart-copy">${t("site.quickstart_copy")}</button>
        </div>
        <pre class="terminal-body" id="quickstart-cmds">${lines}</pre>
      </div>`;
    const copyBtn = panel.querySelector("#quickstart-copy");
    if (copyBtn) {
      copyBtn.addEventListener("click", async () => {
        const text = cmds.join("\n");
        try {
          await navigator.clipboard.writeText(text);
          const prev = copyBtn.textContent;
          copyBtn.textContent = t("site.quickstart_copied");
          setTimeout(() => {
            copyBtn.textContent = prev;
          }, 1600);
        } catch (_err) {
          /* ignore */
        }
      });
    }
  }

  function renderHero() {
    const c = state.data.catalogs[state.lang].course || {};
    const stats = state.data.stats || { modules: 9, labs: 8, languages: 3 };
    document.getElementById("title").textContent = c.title || "AIMarket Course";
    document.getElementById("tagline").textContent = c.tagline || "";
    document.getElementById("modules-heading").textContent = t("site.modules_heading");
    document.getElementById("labs-heading").textContent = t("site.labs_heading");
    document.getElementById("quickstart-heading").textContent = t("site.quickstart_heading");
    document.getElementById("certificate-heading").textContent = t("site.certificate_heading");
    const badge = document.getElementById("hero-badge");
    if (badge) badge.textContent = t("site.hero_badge");
    const certNav = document.getElementById("cert-nav");
    if (certNav) certNav.textContent = t("site.certificate_nav");
    document.getElementById("footer-note").textContent = t("site.footer");

    const statsEl = document.getElementById("hero-stats");
    if (statsEl) {
      statsEl.innerHTML = `
        <div class="stat"><strong>${stats.modules}</strong><span>${t("site.stat_modules")}</span></div>
        <div class="stat"><strong>${stats.labs}</strong><span>${t("site.stat_labs")}</span></div>
        <div class="stat"><strong>${stats.languages}</strong><span>${t("site.stat_langs")}</span></div>`;
    }

    const nav = document.getElementById("page-nav");
    if (nav) {
      nav.innerHTML = `
        <li><a href="#quickstart">${t("site.nav_quickstart")}</a></li>
        <li><a href="#certificate">${t("site.nav_certificate")}</a></li>
        <li><a href="#modules-section">${t("site.nav_modules")}</a></li>
        <li><a href="#labs">${t("site.nav_labs")}</a></li>`;
    }

    renderQuickstart();
  }

  function renderPage() {
    renderHero();
    renderCertificatePanel();
    renderModules();
    renderLabs();
  }

  function setLang(lang) {
    if (!state.data || !state.data.catalogs[lang]) return;
    state.lang = lang;
    localStorage.setItem("course-lang", lang);
    document.documentElement.lang = lang;
    document.querySelectorAll(".lang-switch button").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.lang === lang);
    });
    const c = state.data.catalogs[lang].course || {};
    document.title = c.title ? `${c.title} · AIMarket Courses` : "AIMarket Courses";
    renderPage();
  }

  function initLangSwitcher() {
    const switcher = document.getElementById("lang-switch");
    if (!switcher || switcher.dataset.bound === "1") return;
    switcher.dataset.bound = "1";
    switcher.addEventListener("click", (event) => {
      const btn = event.target.closest("button[data-lang]");
      if (!btn || !switcher.contains(btn)) return;
      setLang(btn.dataset.lang);
    });
    for (const lang of state.data.languages) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.dataset.lang = lang;
      btn.textContent = lang.toUpperCase();
      switcher.appendChild(btn);
    }
  }

  fetch("data/course.json")
    .then((r) => r.json())
    .then((data) => {
      state.data = data;
      initLangSwitcher();
      const saved = localStorage.getItem("course-lang");
      const initial = saved && data.catalogs[saved] ? saved : "en";
      setLang(initial);
    });
})();
