/* Zambia CDF Tracker — constituency share card (roadmap item 2, 2026-11-04).
 *
 * Draws the frozen constituency-card standard (Operating System Addendum 4;
 * blueprint realised in fb-demos/build_lunte_v8.py + cardlib.py) onto a
 * canvas in the visitor's browser, from window.CDF_CARDS — the slim feed
 * model/generate_feed.py emits from cdf.db in the same run as data.js.
 * No pre-rendered card images are stored, so a downloaded card always
 * matches the record the page displays.
 *
 * Grammar (identical to the blueprint): gold kicker over the constituency
 * name; two sharp contrast lines; THE AUDIT COUNTED (audited total,
 * segmented bar, Completed / In progress / Never started as count · %,
 * largest-remainder shares summing to exactly 100.0); THE PUBLISHED
 * RECORD (named total; Projects named [grey], Named completed, In
 * progress, Approved, Still held — plus Stalled / Status not stated rows
 * only when a constituency genuinely has such projects, so the stage
 * rows always account for every named project); one sharp closing line;
 * gold tagline "The audit counted them. We name them."; muted source
 * line; standard footer. Colour law as on the Facebook cards (lifted
 * shades on the dark-green ground): gold = approved/paper, steel blue =
 * in progress, deep green = completed, red = never started / stalled /
 * held, grey = named / not stated.
 *
 * Canvas simplifications vs the PIL blueprint: text is drawn with the
 * site's Barlow / Barlow Condensed webfonts (loaded on demand; system
 * sans fallback if they cannot load), and the Zambia-outline watermark
 * is composited with a flat 0.5 alpha instead of a per-pixel alpha
 * multiply. Layout coordinates, colours and wording are the blueprint's.
 */
(function () {
  "use strict";

  var W = 1080, H = 1080, M = 72, SCALE = 2;
  var GOLD = "#f2b01e", GREEN = "#2fa866", BLUE = "#6ea8c9", RED = "#e2604a",
      WHITE = "#ffffff", PALE = "#cfe0cf", MUTED = "#9db8a4", GREY = "#9aa79d",
      TRACK = "rgba(255,255,255,0.10)", HAIR = "rgba(255,255,255,0.24)";
  var TAGLINE = "The audit counted them. We name them.";

  function fontCB(s) { return "700 " + s + "px 'Barlow Condensed','Arial Narrow',sans-serif"; }
  function fontCS(s) { return "600 " + s + "px 'Barlow Condensed','Arial Narrow',sans-serif"; }
  function fontBR(s) { return "400 " + s + "px 'Barlow',sans-serif"; }
  function fontBS(s) { return "600 " + s + "px 'Barlow',sans-serif"; }

  /* Largest-remainder rounding in per-mille, ported from the blueprint's
     pcts(): returned shares are integers summing to exactly 1000
     (= 100.0%). Shares are taken over the sum of the three parts; the
     printed audited total is the report's own total (the two differ only
     for Mwansabombwe, whose FY2024 row is internally inconsistent as
     printed — disclosed on its constituency page). */
  function shares1000(parts) {
    var total = parts.reduce(function (a, b) { return a + b; }, 0);
    if (!total) return parts.map(function () { return 0; });
    var raw = parts.map(function (p) { return p * 1000 / total; });
    var fl = raw.map(function (r) { return Math.floor(r); });
    var rem = 1000 - fl.reduce(function (a, b) { return a + b; }, 0);
    var order = parts.map(function (_, i) { return i; }).sort(function (a, b) {
      return (raw[b] - fl[b]) - (raw[a] - fl[a]);
    });
    for (var k = 0; k < rem && k < order.length; k++) fl[order[k]] += 1;
    return fl;
  }
  function pct(sh) { return (sh / 10).toFixed(1) + "%"; }

  function buildModel(d) {
    var a = d.audit, p = d.published;
    var accounted = p.completed + p.inProgress + p.approved + p.stalled + p.notStated;
    if (accounted !== p.named)
      throw new Error("published stage buckets (" + accounted + ") do not sum to named (" + p.named + ")");

    var m = {
      name: d.name,
      kicker: "THE CONSTITUENCY DEVELOPMENT FUND · " + String(d.province).toUpperCase(),
      tagline: TAGLINE
    };

    /* --- the two sharp contrast lines + the closing line --- */
    var pc = p.completed;
    if (a) {
      var ac = a.completed;
      m.line1 = ac === 0
        ? "The audit counted no finished projects here."
        : "The audit counted " + ac + " finished project" + (ac === 1 ? "" : "s") + " here.";
      m.line2 = pc === 0
        ? "None are published as completed."
        : (pc < ac ? "Only " : "") + pc + (pc === 1 ? " is" : " are") + " published as completed.";
      var gap = ac - pc;
      if (gap > 0)
        m.closing = gap + " finished project" + (gap === 1 ? " has" : "s have") +
                    " no published name" + (gap === 1 ? "" : "s") + ".";
      else if (gap === 0 && ac > 0)
        m.closing = "Every finished project the audit counted is published by name.";
      else if (gap === 0)
        m.closing = "No completions are published yet — the names are still to come.";
      else
        m.closing = "The published record names more completions than the FY2024 audit counted — it covers more years.";
    } else {
      m.line1 = "The FY2024 audit record for this constituency is not published.";
      m.line2 = pc === 0
        ? "None are published as completed."
        : pc + (pc === 1 ? " is" : " are") + " published as completed.";
      m.closing = p.named > 0
        ? p.named + " project" + (p.named === 1 ? " is" : "s are") + " published by name — the audit count is not published."
        : "Nothing has been published by name here yet.";
    }

    /* --- THE AUDIT COUNTED --- */
    if (a) {
      var sh = shares1000([a.completed, a.inProgress, a.neverStarted]);
      if (sh[0] + sh[1] + sh[2] !== 1000) throw new Error("audit shares do not sum to 100.0");
      m.audit = {
        big: a.audited + " audited",
        sub: "Project status in the Auditor-General's FY2024 report",
        barParts: [a.completed, a.inProgress, a.neverStarted],
        rows: [
          [GREEN, "Completed", a.completed + " · " + pct(sh[0])],
          [BLUE, "In progress", a.inProgress + " · " + pct(sh[1])],
          [RED, "Never started", a.neverStarted + " · " + pct(sh[2])]
        ]
      };
    } else {
      m.audit = {
        big: "Not published", notPublished: true,
        sub: "The FY2024 report does not publish a count for this constituency",
        barParts: null,
        rows: [
          [GREY, "Completed", "Not published"],
          [GREY, "In progress", "Not published"],
          [GREY, "Never started", "Not published"]
        ]
      };
    }

    /* --- THE PUBLISHED RECORD --- */
    var rows = [
      [GREY, "Projects named", String(p.named)],
      [GREEN, "Named completed", String(p.completed)],
      [BLUE, "In progress", String(p.inProgress)],
      [GOLD, "Approved", String(p.approved)]
    ];
    if (p.stalled > 0) rows.push([RED, "Stalled", String(p.stalled)]);
    if (p.notStated > 0) rows.push([GREY, "Status not stated", String(p.notStated)]);
    rows.push([RED, "Still held", String(p.held)]);
    m.published = {
      big: p.named + " named",
      sub: "Projects named in council-published lists, on the tracker",
      rows: rows
    };

    /* --- source line --- */
    var src = [];
    if (a) src.push("Auditor-General's CDF Report FY2024");
    var pubs = d.publishers || [];
    if (pubs.length) {
      src = src.concat(pubs.slice(0, 3));
      if (pubs.length > 3) src.push("and others");
    } else {
      src.push("No council-published project list found yet");
    }
    m.source = src.join(" · ");
    return m;
  }

  function roundRectPath(ctx, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function legendRow(ctx, x, y, colour, label, value) {
    ctx.fillStyle = colour;
    roundRectPath(ctx, x, y + 6, 22, 22, 5);
    ctx.fill();
    ctx.fillStyle = WHITE;
    ctx.font = fontBS(34);
    ctx.fillText(label, x + 38, y);
    ctx.font = fontCB(40);
    var vw = ctx.measureText(value).width;
    ctx.fillText(value, W - M - vw, y - 4);
  }

  function sectionHead(ctx, y, label, big, bigColour, bigFont) {
    ctx.fillStyle = GOLD;
    ctx.font = fontCS(36);
    ctx.fillText(label, M, y);
    ctx.fillStyle = bigColour || WHITE;
    ctx.font = bigFont || fontCB(54);
    var bw = ctx.measureText(big).width;
    ctx.fillText(big, W - M - bw, y - 12);
    return y + 48;
  }

  function fitFont(ctx, text, make, size, floor, maxWidth) {
    var s = size;
    ctx.font = make(s);
    while (s > floor && ctx.measureText(text).width > maxWidth) {
      s -= 2;
      ctx.font = make(s);
    }
    return s;
  }

  /* Draws the card in logical 1080x1080 units (caller scales the
     context). Returns the y just below the tagline, for fit checks. */
  function draw(ctx, m, wm) {
    var grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, "#0b3520");
    grad.addColorStop(1, "#14532d");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);
    if (wm) {
      ctx.save();
      ctx.globalAlpha = 0.5;
      ctx.drawImage(wm, W - 560, H - 470, 640, 546);
      ctx.restore();
    }
    ctx.textBaseline = "top";
    ctx.textAlign = "left";

    /* headline zone */
    ctx.fillStyle = GOLD;
    ctx.font = fontCS(34);
    ctx.fillText(m.kicker, M, 48);
    var tsize = fitFont(ctx, m.name, fontCB, 76, 44, W - 2 * M);
    ctx.fillStyle = WHITE;
    ctx.font = fontCB(tsize);
    ctx.fillText(m.name, M, 96);
    var y = 198;
    ctx.font = fontBS(34);
    ctx.fillText(m.line1, M, y); y += 42;
    ctx.fillText(m.line2, M, y); y += 42;
    y += 10;
    ctx.strokeStyle = HAIR;
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(M, y); ctx.lineTo(W - M, y); ctx.stroke();
    y += 14;

    /* THE AUDIT COUNTED */
    y = sectionHead(ctx, y, "THE AUDIT COUNTED", m.audit.big,
                    m.audit.notPublished ? GREY : WHITE,
                    m.audit.notPublished ? fontCB(44) : fontCB(54));
    ctx.fillStyle = PALE;
    ctx.font = fontBR(25);
    ctx.fillText(m.audit.sub, M, y);
    y += 30;
    if (m.audit.barParts) {
      var total = m.audit.barParts.reduce(function (s, v) { return s + v; }, 0);
      var colours = [GREEN, BLUE, RED];
      ctx.save();
      roundRectPath(ctx, M, y, W - 2 * M, 50, 14);
      ctx.clip();
      ctx.fillStyle = TRACK;
      ctx.fillRect(M, y, W - 2 * M, 50);
      var cx = M;
      for (var i = 0; i < 3; i++) {
        var segw = total ? m.audit.barParts[i] / total * (W - 2 * M) : 0;
        if (segw > 0.5) {
          ctx.fillStyle = colours[i];
          ctx.fillRect(cx, y, segw, 50);
        }
        cx += segw;
      }
      ctx.restore();
    }
    y += 58;
    var steps = [43, 43, 46];
    for (var r = 0; r < 3; r++) {
      legendRow(ctx, M, y, m.audit.rows[r][0], m.audit.rows[r][1], m.audit.rows[r][2]);
      y += steps[r];
    }

    /* THE PUBLISHED RECORD */
    ctx.strokeStyle = HAIR;
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(M, y); ctx.lineTo(W - M, y); ctx.stroke();
    y += 14;
    y = sectionHead(ctx, y, "THE PUBLISHED RECORD", m.published.big);
    ctx.fillStyle = PALE;
    ctx.font = fontBR(25);
    ctx.fillText(m.published.sub, M, y);
    y += 30;
    var n = m.published.rows.length;
    var step = n > 5 ? 33 : 41, lastGap = n > 5 ? 38 : 42;
    for (var q = 0; q < n; q++) {
      legendRow(ctx, M, y, m.published.rows[q][0], m.published.rows[q][1], m.published.rows[q][2]);
      y += q < n - 1 ? step : lastGap;
    }

    /* closing line + tagline */
    ctx.fillStyle = WHITE;
    ctx.font = fontBS(29);
    ctx.fillText(m.closing, M, y);
    y += 35;
    ctx.fillStyle = GOLD;
    ctx.font = fontCS(30);
    ctx.fillText(m.tagline, M, y);
    var bottom = y + 40;

    /* footer (blueprint) */
    var ssize = fitFont(ctx, m.source, fontBR, 22, 15, W - 2 * M);
    ctx.fillStyle = MUTED;
    ctx.font = fontBR(ssize);
    ctx.fillText(m.source, M, H - 128);
    ctx.strokeStyle = GOLD;
    ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(M, H - 96); ctx.lineTo(W - M, H - 96); ctx.stroke();
    ctx.fillStyle = GOLD;
    ctx.font = fontCB(36);
    ctx.fillText("ZAMBIA CDF TRACKER", M, H - 82);
    ctx.fillStyle = WHITE;
    ctx.font = fontBS(30);
    var rtxt = "Follow every kwacha.";
    ctx.fillText(rtxt, W - M - ctx.measureText(rtxt).width, H - 80);
    ctx.fillStyle = MUTED;
    ctx.font = fontBR(22);
    var utxt = "followeverykwacha.com";
    ctx.fillText(utxt, W - M - ctx.measureText(utxt).width, H - 44);
    return bottom;
  }

  function init() {
    var sec = document.querySelector("section.sharecard[data-slug]");
    if (!sec || !window.CDF_CARDS) return;
    var slug = sec.getAttribute("data-slug");
    var d = window.CDF_CARDS[slug];
    if (!d) { sec.style.display = "none"; return; }
    var model;
    try { model = buildModel(d); } catch (e) { sec.style.display = "none"; return; }
    var canvas = sec.querySelector("canvas.cardcanvas");
    if (!canvas || !canvas.getContext) { sec.style.display = "none"; return; }
    var dl = sec.querySelector(".carddl"),
        open = sec.querySelector(".cardopen"),
        shareBtn = sec.querySelector(".cardshare");

    var wmImg = new Image();
    var wmReady = new Promise(function (res) {
      wmImg.onload = function () { res(wmImg); };
      wmImg.onerror = function () { res(null); };
    });
    wmImg.src = "../img/zm-outline.png";

    if (!document.querySelector("link[data-cardfonts]")) {
      var link = document.createElement("link");
      link.rel = "stylesheet";
      link.setAttribute("data-cardfonts", "");
      link.href = "https://fonts.googleapis.com/css2?family=Barlow:wght@400;600&family=Barlow+Condensed:wght@600;700&display=swap";
      document.head.appendChild(link);
    }
    var fontsReady = Promise.resolve();
    if (document.fonts && document.fonts.load) {
      fontsReady = Promise.race([
        Promise.all([
          document.fonts.load("700 76px 'Barlow Condensed'"),
          document.fonts.load("600 34px 'Barlow Condensed'"),
          document.fonts.load("600 34px 'Barlow'"),
          document.fonts.load("400 22px 'Barlow'")
        ]).catch(function () {}),
        new Promise(function (res) { setTimeout(res, 1800); })
      ]);
    }

    Promise.all([wmReady, fontsReady]).then(function (res) {
      var ctx = canvas.getContext("2d");
      if (!ctx) { sec.style.display = "none"; return; }
      ctx.setTransform(SCALE, 0, 0, SCALE, 0, 0);
      draw(ctx, model, res[0]);
      if (!canvas.toBlob) return;
      canvas.toBlob(function (blob) {
        if (!blob) return;
        var url = null;
        if (URL.createObjectURL) { try { url = URL.createObjectURL(blob); } catch (e) { url = null; } }
        if (!url && canvas.toDataURL) url = canvas.toDataURL("image/png");
        if (!url) return;
        if (dl) dl.href = url;
        if (open) open.href = url;
        if (shareBtn && navigator.canShare && window.File) {
          var file = new File([blob], slug + "-cdf-card.png", { type: "image/png" });
          if (navigator.canShare({ files: [file] })) {
            shareBtn.hidden = false;
            shareBtn.addEventListener("click", function () {
              navigator.share({
                files: [file],
                title: d.name + " — Zambia CDF Tracker",
                text: d.name + ": the audit counted them. We name them. followeverykwacha.com"
              }).catch(function () {});
            });
          }
        }
      }, "image/png");
    });
  }

  window.CDFCard = { buildModel: buildModel, draw: draw, shares1000: shares1000 };
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
