// Cuenta atrás de las páginas-guía. El HTML ya trae la fecha escrita; esto solo añade "faltan X días".
// data-when: una o varias fechas separadas por espacios
//   "9-21"    → 21 de septiembre (fecha fija)
//   "5-w0-2"  → 2.º domingo de mayo (mes-wDíaSemana-n, 0 = domingo), igual que las rule de index.html
// data-names y data-ids (opcionales, separados por "|") van en el mismo orden que data-when.
(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const fmt = new Intl.DateTimeFormat("es", { weekday: "short", day: "numeric", month: "short" });
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
    const lead = best.n === 0 ? "Toca hoy" : best.n === 1 ? "día para" : "días para";
    el.querySelector(".next-num").textContent = best.n === 0 ? "¡Hoy!" : best.n;
    el.querySelector(".next-label").textContent = `${lead} · ${fmt.format(best.d)}`;
    if (names[best.k]) el.querySelector(".next-name").textContent = names[best.k];
    if (ids[best.k] && el.tagName === "A") el.href = el.getAttribute("href").replace(/#.*$/, "") + "#" + ids[best.k];
    el.setAttribute("aria-label", `${names[best.k] || el.querySelector(".next-name").textContent}: ${best.n === 0 ? "hoy" : `faltan ${best.n} días`}. Ver en el calendario.`);
  });
})();
