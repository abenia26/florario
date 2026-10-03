// Cuenta atrás y botón de compartir de las páginas interiores. El HTML ya trae la fecha escrita;
// esto solo añade "faltan X días".
// data-when: una o varias fechas separadas por espacios
//   "9-21"    → 21 de septiembre (fecha fija)
//   "5-w0-2"  → 2.º domingo de mayo (mes-wDíaSemana-n, 0 = domingo), igual que las rule de index.html
// data-names y data-ids (opcionales, separados por "|") van en el mismo orden que data-when.
(() => {
  // Idioma de la página (<html lang>): "es" o "en"
  const en = document.documentElement.lang === "en";
  const t = (es, eng) => en ? eng : es;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const fmt = new Intl.DateTimeFormat(en ? "en" : "es", { weekday: "short", day: "numeric", month: "short" });
  const utc = d => Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());

  function nthWeekday(y, m, wd, n) {
    const first = new Date(y, m - 1, 1);
    return new Date(y, m - 1, 1 + (wd - first.getDay() + 7) % 7 + (n - 1) * 7);
  }
  function parse(s, y) {
    const [m, a, n] = s.split("-");
    return a.startsWith("w") ? nthWeekday(y, +m, +a.slice(1), +n) : new Date(y, m - 1, +a);
  }

  document.querySelectorAll("[data-when]").forEach(el => {
    const whens = el.dataset.when.split(" ");
    const names = el.dataset.names ? el.dataset.names.split("|") : [];
    const ids = el.dataset.ids ? el.dataset.ids.split("|") : [];
    let best = null;
    whens.forEach((s, k) => {
      for (const y of [today.getFullYear(), today.getFullYear() + 1]) {
        const d = parse(s, y);
        const n = Math.round((utc(d) - utc(today)) / 864e5);
        if (n >= 0 && (!best || n < best.n)) best = { d, n, k };
      }
    });
    if (!best) return;
    const lead = best.n === 0 ? t("Es hoy", "It’s today") : best.n === 1 ? t("día para", "day to go") : t("días para", "days to go");
    el.querySelector(".next-num").textContent = best.n === 0 ? t("¡Hoy!", "Today!") : best.n;
    el.querySelector(".next-label").textContent = `${lead} · ${fmt.format(best.d)}`;
    if (names[best.k]) el.querySelector(".next-name").textContent = names[best.k];
    if (ids[best.k] && el.tagName === "A") el.href = el.getAttribute("href").replace(/#.*$/, "") + "#" + ids[best.k];
  });

  // Índice "En esta página": plegado en móvil, abierto en escritorio (columna lateral).
  const toc = document.querySelector(".toc details");
  if (toc && matchMedia("(min-width: 960px)").matches) toc.open = true;

  // Mensajes para la tarjeta: copiar el texto al portapapeles.
  document.querySelectorAll("[data-copy]").forEach(btn => {
    const label = btn.textContent;
    btn.hidden = false;
    btn.addEventListener("click", () => {
      const text = btn.closest("li").querySelector("q").textContent;
      const done = msg => { btn.textContent = msg; setTimeout(() => { btn.textContent = label; }, 1800); };
      try {
        navigator.clipboard.writeText(text).then(() => done(t("Copiado ✓", "Copied ✓")), () => done(t("No se pudo copiar", "Couldn’t copy")));
      } catch (e) { done(t("No se pudo copiar", "Couldn’t copy")); }
    });
  });

  // Generador de tarjeta: el mensaje elegido y una flor en una imagen 1080×1920 (<canvas>), para
  // descargarla o compartirla. Todo en el navegador, sin servidor.
  const msgSection = document.getElementById("mensajes");
  if (msgSection && document.createElement("canvas").getContext) {
    const FLOWERS = [["#F2C230", t("Amarilla", "Yellow")], ["#3F72E0", t("Azul", "Blue")], ["#8A4FD8", t("Morada", "Purple")],
                     ["#EE7FA8", t("Rosa", "Pink")], ["#D7263D", t("Roja", "Red")], ["#F6F4EC", t("Blanca", "White")]];
    const pageColor = getComputedStyle(document.body).getPropertyValue("--fc").trim().toUpperCase();
    let color = (FLOWERS.find(([c]) => c === pageColor) || FLOWERS[0])[0];
    let text = "";
    const panel = document.createElement("div");
    panel.className = "card-maker";
    panel.hidden = true;
    panel.innerHTML = `<canvas width="1080" height="1920" aria-label="${t("Vista previa de la tarjeta", "Card preview")}" role="img"></canvas>
      <div class="cm-side"><p class="cm-h">${t("Tu tarjeta", "Your card")}</p>
      <div class="cm-colors" role="group" aria-label="${t("Color de la flor", "Flower color")}">${FLOWERS.map(([c, n]) =>
        `<button type="button" class="cm-color" data-color="${c}" aria-label="${n}" title="${n}" style="--c:${c}"></button>`).join("")}</div>
      <div class="cm-actions"><button type="button" class="btn primary" data-cm="share">${t("Compartir", "Share")}</button>
      <button type="button" class="btn" data-cm="download">${t("Descargar", "Download")}</button></div>
      <p class="cm-status" role="status"></p></div>`;
    msgSection.appendChild(panel);
    const canvas = panel.querySelector("canvas");

    function wrap(ctx, str, max) {
      const words = str.split(" "), lines = [];
      let line = "";
      for (const w of words) {
        const test = line ? line + " " + w : w;
        if (ctx.measureText(test).width > max && line) { lines.push(line); line = w; } else line = test;
      }
      lines.push(line);
      return lines;
    }
    async function draw() {
      try { await document.fonts.load('800 80px "Bricolage Grotesque"'); } catch (e) { /* sin fuentes: usa la del sistema */ }
      const ctx = canvas.getContext("2d"), W = 1080, H = 1920;
      // Fondo sólido y encima un velo del color de la flor (sin transparencias en la imagen final)
      ctx.fillStyle = "#F6F4EC"; ctx.fillRect(0, 0, W, H);
      const bg = ctx.createLinearGradient(0, 0, W, H);
      bg.addColorStop(0, "rgba(246,244,236,0)"); bg.addColorStop(1, color === "#F6F4EC" ? "#DCE5D2" : color + "44");
      ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
      // Flor: pétalos en elipse alrededor de un centro, como en la rueda del calendario
      ctx.save(); ctx.translate(W / 2, 560);
      for (let k = 0; k < 8; k++) {
        ctx.save(); ctx.rotate(k * Math.PI / 4);
        ctx.beginPath(); ctx.ellipse(0, -150, 70, 150, 0, 0, Math.PI * 2);
        ctx.fillStyle = color === "#F6F4EC" ? "#FFFFFF" : color; ctx.fill();
        ctx.lineWidth = 4; ctx.strokeStyle = "rgba(27,33,24,.25)"; ctx.stroke(); ctx.restore();
      }
      ctx.beginPath(); ctx.arc(0, 0, 72, 0, Math.PI * 2); ctx.fillStyle = "#2A2F25"; ctx.fill(); ctx.restore();
      // Mensaje
      ctx.fillStyle = "#1B2118"; ctx.textAlign = "center";
      let size = 84, lines;
      do { ctx.font = `800 ${size}px "Bricolage Grotesque", system-ui, sans-serif`; lines = wrap(ctx, text, 900); size -= 4; } while (lines.length * size * 1.15 > 640 && size > 44);
      const lh = (size + 4) * 1.15, top = 1060 + (640 - lines.length * lh) / 2 + lh * .8;
      lines.forEach((l, i) => ctx.fillText(l, W / 2, top + i * lh));
      ctx.font = '500 34px "DM Mono", monospace'; ctx.fillStyle = "#525A4D";
      ctx.fillText("calendariodeflores.com", W / 2, 1800);
      panel.querySelectorAll(".cm-color").forEach(b => b.setAttribute("aria-pressed", b.dataset.color === color));
    }
    const status = panel.querySelector(".cm-status");
    const blob = () => new Promise(ok => canvas.toBlob(ok, "image/png"));
    const fileName = t("tarjeta-florario.png", "florario-card.png");
    async function download() {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(await blob());
      a.download = fileName;
      document.body.appendChild(a); a.click();
      setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
      status.textContent = t("Tarjeta descargada.", "Card downloaded.");
    }
    panel.addEventListener("click", async e => {
      const c = e.target.closest(".cm-color");
      if (c) { color = c.dataset.color; draw(); return; }
      const act = e.target.closest("[data-cm]");
      if (!act) return;
      if (act.dataset.cm === "download") return download();
      const file = new File([await blob()], fileName, { type: "image/png" });
      if (navigator.canShare && navigator.canShare({ files: [file] })) navigator.share({ files: [file] }).catch(() => {});
      else download();
    });
    document.querySelectorAll(".msgs li").forEach(li => {
      const btn = document.createElement("button");
      btn.type = "button"; btn.className = "copy"; btn.textContent = t("Tarjeta", "Card");
      btn.addEventListener("click", () => {
        text = li.querySelector("q").textContent;
        panel.hidden = false; status.textContent = "";
        draw().then(() => panel.scrollIntoView({ behavior: "smooth", block: "nearest" }));
      });
      li.appendChild(btn);
    });
  }

  // Compartir: menú nativo del móvil si existe; si no, copiar el enlace.
  document.querySelectorAll("[data-share]").forEach(btn => {
    const status = btn.closest(".share")?.querySelector(".share-status");
    btn.hidden = false;
    if (!navigator.share) btn.textContent = t("Copiar enlace", "Copy link");
    btn.addEventListener("click", () => {
      const { url, title, text } = btn.dataset;
      if (navigator.share) {
        navigator.share({ title, text: text || title, url }).catch(() => {});
        return;
      }
      const fallback = () => { if (status) status.textContent = `${t("Copia este enlace:", "Copy this link:")} ${url}`; };
      try {
        navigator.clipboard.writeText(url).then(() => { if (status) status.textContent = t("Enlace copiado.", "Link copied."); }, fallback);
      } catch (e) { fallback(); }
    });
  });

  // Barra fija inferior (solo móvil, por CSS): aparece cuando los botones de arriba ya no se ven
  // y se esconde al llegar al pie, para no tapar los enlaces.
  const bar = document.querySelector(".sticky-bar");
  const anchor = document.querySelector(".share-top");
  const foot = document.querySelector(".site-foot");
  if (bar && anchor && "IntersectionObserver" in window) {
    let past = false, atFoot = false;
    const update = () => {
      const show = past && !atFoot;
      bar.hidden = false;
      bar.classList.toggle("on", show);
      document.body.classList.toggle("has-bar", show);
    };
    new IntersectionObserver(([e]) => { past = !e.isIntersecting && e.boundingClientRect.top < 0; update(); }).observe(anchor);
    if (foot) new IntersectionObserver(([e]) => { atFoot = e.isIntersecting; update(); }).observe(foot);
  }
})();
