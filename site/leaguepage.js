/* The Publishing League (roadmap item 5, 2026-11-04): councils ranked on
 * the record they themselves publish. Renders entirely from
 * window.CDF_LEAGUE — the feed generate_feed.py emits from cdf.db — so
 * the league can never drift from the record the project pages display.
 *
 * A project is credited to a council only when the publisher on its
 * source names that council (normalisation rules are documented in
 * generate_feed.py and printed on the page). Projects carried by
 * national publishers are counted separately in `excluded`, never
 * credited to a council. The completeness score is the simple average
 * of the three stated shares (status, funding year, amount), each
 * rounded to a whole percent first — the same rounding the provinces
 * publishing scorecard uses.
 */
(function () {
  var L = window.CDF_LEAGUE;
  if (!L) return;
  var stripHost = document.getElementById('leagueStrip');
  var bestHost = document.getElementById('leagueBest');
  var bestWrap = document.getElementById('leagueBestWrap');
  var tableBody = document.querySelector('#leagueTable tbody');
  var noneHost = document.getElementById('leagueNone');
  var noneWrap = document.getElementById('leagueNoneWrap');
  var exclHost = document.getElementById('leagueExcl');

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'];
  function fmtDate(d) {
    if (!d) return 'Not published';
    var p = d.split('-');
    if (p.length === 1) return p[0];
    if (p.length === 2) return MONTHS[parseInt(p[1], 10) - 1] + ' ' + p[0];
    return parseInt(p[2], 10) + ' ' + MONTHS[parseInt(p[1], 10) - 1] + ' ' + p[0];
  }
  function dateKey(d) {
    if (!d) return -1;
    var p = d.split('-');
    var y = parseInt(p[0], 10) || 0;
    var m = p.length > 1 ? parseInt(p[1], 10) : 12;
    var da = p.length > 2 ? parseInt(p[2], 10) : 31;
    return y * 10000 + m * 100 + da;
  }
  function num(n) { return n.toLocaleString('en-GB'); }

  /* ---------- national strip ---------- */
  if (stripHost) {
    stripHost.innerHTML =
      '<div class="bstat"><b>' + L.meta.councils + '</b><span>councils have published lists in the record</span></div>' +
      '<div class="bstat"><b>' + num(L.meta.attributed) + '</b><span>named projects were published by councils themselves</span></div>' +
      '<div class="bstat"><b>' + num(L.meta.councilCompleted) + '</b><span>of those are named completions</span></div>' +
      '<div class="bstat"><b>' + num(L.meta.unattributed) + '</b><span>named projects reached the record through national publishers instead</span></div>';
  }

  /* ---------- the standard-setters ---------- */
  var best = L.councils.filter(function (r) { return r.named >= 20 && r.composite >= 90; });
  if (bestHost && best.length) {
    bestHost.innerHTML = best.map(function (r) {
      return '<div class="card"><h3 style="margin-top:0">' + esc(r.council) + '</h3>' +
        '<p class="lgscore">' + r.composite.toFixed(1) + '</p>' +
        '<p style="margin:0">' + num(r.named) + ' named projects · ' + num(r.completed) + ' completed<br>' +
        'Status ' + r.statusPct + '% · Year ' + r.yearPct + '% · Amount ' + r.amountPct + '%</p>' +
        '<p class="lgconsts" style="margin-bottom:0">Publishes for: ' + r.constituencies.map(function (k) {
          return '<a href="constituencies/' + k.slug + '.html">' + esc(k.name) + '</a>';
        }).join(', ') + '</p></div>';
    }).join('');
  } else if (bestWrap) {
    bestWrap.style.display = 'none';
  }

  /* ---------- the full table (sortable; rank stays with the council) ---------- */
  var sortKey = 'rank', sortDir = 1;
  function rowHtml(r) {
    return '<tr><td>' + r.rank + '</td>' +
      '<td><b>' + esc(r.council) + '</b></td>' +
      '<td>' + num(r.named) + '</td><td>' + num(r.completed) + '</td>' +
      '<td>' + r.statusPct + '%</td><td>' + r.yearPct + '%</td><td>' + r.amountPct + '%</td>' +
      '<td class="lgcomp">' + r.composite.toFixed(1) + '</td>' +
      '<td>' + fmtDate(r.latest) + '</td>' +
      '<td class="lgconsts">' + r.constituencies.map(function (k) {
        return '<a href="constituencies/' + k.slug + '.html">' + esc(k.name) + '</a>';
      }).join(', ') + '</td></tr>';
  }
  function renderTable() {
    if (!tableBody) return;
    var rows = L.councils.slice();
    rows.sort(function (a, b) {
      var va, vb;
      if (sortKey === 'council') { va = a.council; vb = b.council; }
      else if (sortKey === 'latest') { va = dateKey(a.latest); vb = dateKey(b.latest); }
      else { va = a[sortKey]; vb = b[sortKey]; }
      if (va < vb) return -1 * sortDir;
      if (va > vb) return 1 * sortDir;
      return (b.composite - a.composite) || (b.named - a.named) || (a.council < b.council ? -1 : 1);
    });
    tableBody.innerHTML = rows.map(rowHtml).join('');
    var ths = document.querySelectorAll('#leagueTable thead th');
    ths.forEach(function (th) {
      var btn = th.querySelector('.lgsort');
      if (!btn) { th.removeAttribute('aria-sort'); return; }
      if (btn.getAttribute('data-k') === sortKey) {
        th.setAttribute('aria-sort', sortDir === 1 ? 'ascending' : 'descending');
        btn.innerHTML = btn.getAttribute('data-label') + ' <span class="arr" aria-hidden="true">' + (sortDir === 1 ? '↑' : '↓') + '</span>';
      } else {
        th.removeAttribute('aria-sort');
        btn.textContent = btn.getAttribute('data-label');
      }
    });
  }
  var sortBtns = document.querySelectorAll('#leagueTable .lgsort');
  sortBtns.forEach(function (btn) {
    btn.setAttribute('data-label', btn.textContent);
    btn.addEventListener('click', function () {
      var k = btn.getAttribute('data-k');
      if (k === sortKey) { sortDir = -sortDir; }
      else { sortKey = k; sortDir = (k === 'council' || k === 'rank') ? 1 : -1; }
      renderTable();
    });
  });
  renderTable();

  /* ---------- nothing usable published yet ---------- */
  if (noneHost && L.nothingYet && L.nothingYet.length) {
    noneHost.innerHTML = L.nothingYet.map(function (e) {
      var h = '<div class="card"><h3 style="margin-top:0">' +
        esc(e.council || (e.constituency + ' constituency')) + '</h3>' +
        '<p>' + esc(e.constituency) + ' constituency has <b>no named projects</b> on the record — ' +
        'its council has published nothing this tracker could list.</p>';
      if (e.note) h += '<p>' + esc(e.note) + '</p>';
      if (e.held) {
        h += '<p style="margin-bottom:0">' + e.held + ' published item' + (e.held === 1 ? '' : 's') +
          ' sit' + (e.held === 1 ? 's' : '') + ' in the tracker\u2019s held pile — published, but not in a form ' +
          'that names projects the tracker can honestly list.</p>';
      }
      h += '</div>';
      return h;
    }).join('');
  } else if (noneWrap) {
    noneWrap.style.display = 'none';
  }

  /* ---------- who else carried the record (method section) ---------- */
  if (exclHost) {
    exclHost.innerHTML = L.excluded.map(function (x) {
      return '<li>' + esc(x.label) + ' — ' + num(x.projects) + ' projects</li>';
    }).join('');
  }
})();
