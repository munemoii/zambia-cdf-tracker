/* The Gap Map (roadmap item 4, 2026-11-04): audited completed vs named
 * completed, per constituency. Renders entirely from window.CDF_CARDS —
 * the slim feed generate_feed.py emits from cdf.db — so the map can never
 * drift from the figures the constituency pages and share cards display.
 *
 * The two records:
 *  - counted: the Auditor-General's FY2024 report (published 23 December
 *    2025) — how many projects the audit counted as completed.
 *  - named:   the published record — completions councils have published
 *    BY NAME and this tracker holds, each traced to its source.
 * A constituency's gap = counted completed − named completed, floored at
 * zero: where more completions are named than the audit counted (the
 * published record covers more years than the audit cycle), the extra
 * names are that constituency's own and never cancel another's gap.
 */
(function () {
  var host = document.getElementById('gapTiles');
  if (!host || !window.CDF_CARDS) return;
  var detail = document.getElementById('gapDetail');
  var tableBody = document.querySelector('#gapTable tbody');
  var legendHost = document.getElementById('gapLegend');
  var stripHost = document.getElementById('gapStrip');

  // Province blocks in rough geographic reading order (schematic tile
  // grid — tiles are not constituency boundaries).
  var PROV_ORDER = ['North-Western', 'Northern', 'Muchinga', 'Luapula',
    'Copperbelt', 'Eastern', 'Western', 'Central', 'Lusaka', 'Southern'];

  // As-printed audit cautions, disclosed on the constituency pages too.
  var NOTES = {
    'chipili': 'Chipili † — the Auditor-General\u2019s FY2024 rows for Chipili are internally inconsistent as printed: the report prints more completed projects (36) than its own printed total assessed (32), and a negative never-started figure. Every figure here is shown exactly as printed, so treat Chipili\u2019s gap as printed, not settled.',
    'mwansabombwe': 'Mwansabombwe ‡ — as printed in the report, its completed + in progress + never started figures sum to one less than its printed total assessed. The completed figure is used exactly as printed; the same disclosure stands on its constituency page.'
  };
  var MARK = { 'chipili': ' †', 'mwansabombwe': ' ‡' };

  function model(slug, c) {
    var aComp = c.audit ? c.audit.completed : null;
    var nComp = c.published.completed;
    var gap = (aComp === null) ? null : Math.max(aComp - nComp, 0);
    var share = (aComp && gap !== null) ? gap / aComp : null;
    var bucket;
    if (aComp === null) bucket = 'nodata';
    else if (aComp === 0) bucket = 'none';
    else if (share === 0) bucket = 'g0';
    else if (share <= 0.25) bucket = 'g1';
    else if (share <= 0.50) bucket = 'g2';
    else if (share <= 0.75) bucket = 'g3';
    else bucket = 'g4';
    return { slug: slug, name: c.name, province: c.province, audit: c.audit,
             published: c.published, aComp: aComp, nComp: nComp,
             gap: gap, share: share, bucket: bucket };
  }

  var all = Object.keys(window.CDF_CARDS).map(function (s) { return model(s, window.CDF_CARDS[s]); });

  var BUCKETS = [
    { k: 'g0', label: 'Fully named', desc: 'every counted completion has a published name' },
    { k: 'g1', label: 'Up to a quarter unnamed', desc: '1–25% of counted completions still unnamed' },
    { k: 'g2', label: 'A quarter to a half unnamed', desc: '26–50% still unnamed' },
    { k: 'g3', label: 'Half to three-quarters unnamed', desc: '51–75% still unnamed' },
    { k: 'g4', label: 'Over three-quarters unnamed', desc: 'more than 75% still unnamed' },
    { k: 'none', label: 'No completions counted', desc: 'the FY2024 audit counted no completed projects here' },
    { k: 'nodata', label: 'Not in the audit tables', desc: 'no FY2024 audit row published for this constituency' }
  ];

  /* ---------- national strip ---------- */
  var totCounted = 0, totNamed = 0, totGap = 0, fullyNamed = 0;
  all.forEach(function (m) {
    if (m.aComp !== null) totCounted += m.aComp;
    totNamed += m.nComp;
    if (m.gap !== null) totGap += m.gap;
    if (m.bucket === 'g0') fullyNamed++;
  });
  if (stripHost) {
    stripHost.innerHTML =
      '<div class="bstat"><b>' + totCounted.toLocaleString('en-GB') + '</b><span>projects the Auditor-General counted as completed (FY2024 report)</span></div>' +
      '<div class="bstat"><b>' + totNamed.toLocaleString('en-GB') + '</b><span>completions councils have published by name — the tracked record</span></div>' +
      '<div class="bstat alert"><b>' + totGap.toLocaleString('en-GB') + '</b><span>counted completions still unnamed, added constituency by constituency</span></div>' +
      '<div class="bstat"><b>' + fullyNamed + ' of ' + all.length + '</b><span>constituencies where every counted completion has a published name</span></div>';
  }

  /* ---------- legend (explains itself, with live counts) ---------- */
  if (legendHost) {
    legendHost.innerHTML = BUCKETS.filter(function (b) {
      return all.some(function (m) { return m.bucket === b.k; });
    }).map(function (b) {
      var n = all.filter(function (m) { return m.bucket === b.k; }).length;
      return '<span class="gleg"><i class="gsw ' + b.k + '"></i><span><b>' + b.label + '</b> — ' +
        b.desc + ' (' + n + ' constituenc' + (n === 1 ? 'y' : 'ies') + ')</span></span>';
    }).join('');
  }

  /* ---------- detail panel ---------- */
  function pct(x) { return (Math.round(x * 1000) / 10).toFixed(1) + '%'; }
  function showDetail(m) {
    if (!detail) return;
    var h = '<h3>' + m.name + (MARK[m.slug] || '') + '</h3>' +
      '<p class="gsub">' + m.province + ' Province</p>';
    if (m.audit) {
      h += '<div class="grecs"><div class="grec"><p class="gk">The audit counted · FY2024</p>' +
        '<p class="grow"><span>Assessed</span><b>' + m.audit.audited + '</b></p>' +
        '<p class="grow"><span>Completed</span><b>' + m.audit.completed + '</b></p>' +
        '<p class="grow"><span>In progress</span><b>' + m.audit.inProgress + '</b></p>' +
        '<p class="grow"><span>Never started</span><b>' + m.audit.neverStarted + '</b></p></div>';
    } else {
      h += '<div class="grecs"><div class="grec"><p class="gk">The audit counted · FY2024</p>' +
        '<p class="gnote">Not published — this constituency does not appear in the FY2024 audit status tables.</p></div>';
    }
    h += '<div class="grec"><p class="gk">The published record · named projects</p>' +
      '<p class="grow"><span>Named, all stages</span><b>' + m.published.named + '</b></p>' +
      '<p class="grow"><span>Named completed</span><b>' + m.published.completed + '</b></p>' +
      '<p class="grow"><span>In progress</span><b>' + m.published.inProgress + '</b></p>' +
      '<p class="grow"><span>Approved</span><b>' + m.published.approved + '</b></p>' +
      '<p class="grow"><span>Still held for proof</span><b>' + m.published.held + '</b></p></div></div>';
    if (m.aComp === 0) {
      h += '<p class="ggap">The FY2024 audit counted <b>no completed projects</b> in ' + m.name +
        ' — it found its projects still in progress or never started, so there is no counted completion to name yet. The published record names ' +
        m.published.named + ' project' + (m.published.named === 1 ? '' : 's') + ', none yet published as completed.</p>';
    } else if (m.gap !== null && m.nComp > m.aComp) {
      h += '<p class="ggap">Councils have published names for <b>' + m.nComp + ' completions</b> here — more than the ' +
        m.aComp + ' the audit counted. The published record covers 2021–2026; the audit assessed one cycle. ' +
        m.name + ' is fully named, and its extra names do not cancel another constituency\u2019s gap.</p>';
    } else if (m.gap !== null) {
      h += '<p class="ggap"><b>' + m.gap + '</b> of the ' + m.aComp + ' completions the audit counted still have ' +
        'no published name — <b>' + pct(m.share) + '</b> of the counted completions are unnamed.</p>';
    }
    if (m.published.named === 0) {
      h += '<p class="gnote">This council has published no projects at all yet — everything on this page for ' + m.name + ' comes from the audit.</p>';
    }
    if (NOTES[m.slug]) h += '<p class="gnote">' + NOTES[m.slug] + '</p>';
    h += '<p><a href="constituencies/' + m.slug + '.html">See ' + m.name + '\u2019s full constituency page →</a></p>';
    detail.innerHTML = h;
    var btns = host.querySelectorAll('.gtile');
    for (var i = 0; i < btns.length; i++) {
      var on = btns[i].getAttribute('data-slug') === m.slug;
      btns[i].classList.toggle('sel', on);
      btns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  }

  /* ---------- tile grid, grouped by province ---------- */
  var byProv = {};
  all.forEach(function (m) { (byProv[m.province] = byProv[m.province] || []).push(m); });
  host.innerHTML = PROV_ORDER.filter(function (p) { return byProv[p]; }).map(function (p) {
    var ms = byProv[p].slice().sort(function (a, b) { return a.name < b.name ? -1 : 1; });
    var pCounted = 0, pNamed = 0, pGap = 0;
    ms.forEach(function (m) {
      if (m.aComp !== null) pCounted += m.aComp;
      pNamed += m.nComp; if (m.gap !== null) pGap += m.gap;
    });
    var barTotal = pNamed + pGap;
    var namedW = barTotal ? Math.round(pNamed / barTotal * 1000) / 10 : 0;
    var tiles = ms.map(function (m) {
      var big = m.bucket === 'none' ? '—' : String(m.gap);
      var lab = m.bucket === 'none' ? 'none counted' : (m.gap === 0 ? 'unnamed · all named' : 'unnamed');
      return '<button type="button" class="gtile ' + m.bucket + '" data-slug="' + m.slug + '" aria-pressed="false" ' +
        'title="' + m.name + ': audit counted ' + (m.aComp === null ? '—' : m.aComp) + ' completed; ' +
        m.nComp + ' named completed; ' + (m.gap === null ? '—' : m.gap) + ' still unnamed">' +
        '<span class="gn">' + m.name + (MARK[m.slug] || '') + '</span>' +
        '<span class="gv">' + big + '</span><span class="gl">' + lab + '</span></button>';
    }).join('');
    return '<div class="gprov"><div class="gprov-head"><h3>' + p + '</h3>' +
      '<p>Counted completed <b>' + pCounted + '</b> · Named completed <b>' + pNamed + '</b> · Still unnamed <b>' + pGap + '</b></p></div>' +
      '<div class="gbar" role="img" aria-label="' + p + ': ' + pNamed + ' named completions against ' + pGap + ' counted completions still unnamed, constituency by constituency">' +
      '<span class="gbar-named" style="width:' + namedW + '%"></span><span class="gbar-gap" style="width:' + (100 - namedW) + '%"></span></div>' +
      '<div class="gtiles">' + tiles + '</div></div>';
  }).join('');
  host.addEventListener('click', function (ev) {
    var t = ev.target.closest ? ev.target.closest('.gtile') : null;
    if (!t) return;
    var m = all.find(function (x) { return x.slug === t.getAttribute('data-slug'); });
    if (m) showDetail(m);
  });

  /* ---------- biggest gaps table (top 20 by unnamed count) ---------- */
  if (tableBody) {
    var ranked = all.filter(function (m) { return m.gap !== null && m.gap > 0; })
      .sort(function (a, b) {
        return (b.gap - a.gap) || ((b.share || 0) - (a.share || 0)) || (a.name < b.name ? -1 : 1);
      }).slice(0, 20);
    tableBody.innerHTML = ranked.map(function (m, i) {
      return '<tr><td>' + (i + 1) + '</td>' +
        '<td><a href="constituencies/' + m.slug + '.html">' + m.name + '</a>' + (MARK[m.slug] || '') + '</td>' +
        '<td>' + m.province + '</td><td>' + m.aComp + '</td><td>' + m.nComp + '</td>' +
        '<td><b>' + m.gap + '</b></td><td>' + pct(m.share) + '</td></tr>';
    }).join('');
  }

  /* default selection: the largest single gap */
  var first = all.filter(function (m) { return m.gap !== null; })
    .sort(function (a, b) { return b.gap - a.gap; })[0];
  if (first) showDetail(first);
})();
