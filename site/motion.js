/* Home-page motion: count-up KPIs, growing bars, developments ticker,
   a pulse on the pilot province, and a photo slideshow that activates
   automatically when verified project photos exist in the feed. */
(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var D = window.CDF_DATA || null;

  /* ---------- count-up KPIs ---------- */
  var cancelled = false;
  var yp = document.getElementById('yearPills');
  if (yp) yp.addEventListener('click', function () { cancelled = true; });

  // kTotal text is like "K6.24bn":
  (function () {
    var el = document.getElementById('kTotal');
    if (!el || reduced) return;
    var m = (el.textContent || '').match(/^K([\d.]+)(bn|m)$/);
    if (!m) return;
    var target = parseFloat(m[1]), unit = m[2], dec = unit === 'bn' ? 2 : 1, t0 = null;
    function frame(ts) {
      if (cancelled) { el.textContent = 'K' + target.toFixed(dec) + unit; return; }
      if (!t0) t0 = ts;
      var t = Math.min(1, (ts - t0) / 1300), e = 1 - Math.pow(1 - t, 3);
      el.textContent = 'K' + (target * e).toFixed(dec) + unit;
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();
  (function () {
    var el = document.getElementById('kPer');
    if (!el || reduced) return;
    var m = (el.textContent || '').match(/^K([\d.]+)m$/);
    if (!m) return;
    var target = parseFloat(m[1]), t0 = null;
    function frame(ts) {
      if (cancelled) { el.textContent = 'K' + target.toFixed(1) + 'm'; return; }
      if (!t0) t0 = ts;
      var t = Math.min(1, (ts - t0) / 1100), e = 1 - Math.pow(1 - t, 3);
      el.textContent = 'K' + (target * e).toFixed(1) + 'm';
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();
  (function () {
    var el = document.getElementById('kGrowth');
    if (!el || reduced) return;
    var m = (el.textContent || '').match(/^([\d.]+)×$/);
    if (!m) return;
    var target = parseFloat(m[1]), t0 = null;
    function frame(ts) {
      if (cancelled) { el.textContent = target + '×'; return; }
      if (!t0) t0 = ts;
      var t = Math.min(1, (ts - t0) / 1100), e = 1 - Math.pow(1 - t, 3);
      var v = target * e;
      el.textContent = (v % 1 === 0 || t === 1 ? v.toFixed(0) : v.toFixed(1)) + '×';
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();

  /* ---------- growing year bars ---------- */
  var bars = document.querySelectorAll('#bars .bar');
  if (bars.length && !reduced) {
    bars.forEach(function (b, i) {
      var h = b.style.height;
      b.style.height = '0%';
      setTimeout(function () { b.style.height = h; }, 120 + i * 70);
    });
  }

  /* ---------- developments ticker ---------- */
  if (D && D.news && D.news.length) {
    var anchor = document.querySelector('.board') || document.querySelector('.kpis');
    if (anchor) {
      var items = D.news.map(function (n) {
        return '<span class="tick-item"><b>' + n.date + '</b> — ' + n.title + '</span>';
      }).join('<span class="tick-dot">●</span>');
      var tick = document.createElement('a');
      tick.className = 'ticker';
      tick.href = 'developments.html';
      tick.innerHTML = '<span class="tick-label">Latest</span><span class="tick-viewport"><span class="tick-track">' +
        items + '<span class="tick-dot">●</span>' + items + '<span class="tick-dot">●</span></span></span>';
      anchor.parentNode.insertBefore(tick, anchor.nextSibling);
    }
  }

  /* ---------- pulse on the pilot province (Lusaka) ---------- */
  var svg = document.getElementById('zmMap');
  if (svg && !reduced) {
    [0, 1400].forEach(function (delay) {
      var c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', '484'); c.setAttribute('cy', '497'); c.setAttribute('r', '26');
      c.setAttribute('class', 'pulse-ring');
      c.style.animationDelay = delay + 'ms';
      svg.appendChild(c);
    });
  }

  /* ---------- photo slideshow (activates when photos exist) ---------- */
  if (D && D.pilot) {
    var photos = [];
    D.pilot.constituencies.forEach(function (cc) {
      cc.projects.forEach(function (pr) {
        if (pr.photo) photos.push({ pr: pr, cc: cc.name });
      });
    });
    if (photos.length) {
      var board2 = document.querySelector('header.top') || document.querySelector('.ticker') || document.querySelector('.board');
      var wrap = document.createElement('div');
      wrap.className = 'proofwrap';
      wrap.innerHTML = '<div class="slides-head"><p class="eyebrow">Proof of Delivery</p>' +
        '<p class="slides-sub">CDF projects, photographed where they stand — every image captioned with its project and source.</p></div>';
      var slidesBox = document.createElement('div');
      slidesBox.className = 'slides';
      slidesBox.setAttribute('role', 'region');
      slidesBox.setAttribute('aria-label', 'Proof of Delivery — CDF project photos');
      slidesBox.innerHTML = photos.map(function (x, i) {
        return '<figure class="slide' + (i === 0 ? ' on' : '') + '">' +
          '<img src="' + x.pr.photo.url + '" alt="Photo: ' + x.pr.name.replace(/"/g, '') + '" loading="lazy">' +
          '<figcaption class="cap"><b>' + x.pr.name + '</b><span>' + x.cc + ' constituency · ' +
          (x.pr.photo.credit || '') + '</span></figcaption></figure>';
      }).join('');
      wrap.appendChild(slidesBox);
      if (board2) board2.parentNode.insertBefore(wrap, board2.nextSibling);
      if (photos.length > 1 && !reduced) {
        var cur = 0, slides = slidesBox.querySelectorAll('.slide');
        setInterval(function () {
          slides[cur].classList.remove('on');
          cur = (cur + 1) % slides.length;
          slides[cur].classList.add('on');
        }, 5200);
      }
    }
  }
})();
