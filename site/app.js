(function(){
  // All figures live in data.js (window.CDF_DATA) so the weekly source check
  // can refresh the dashboard by updating that one file.
  var D=window.CDF_DATA||{meta:{},years:[],seats:156,provinces:[],movement:{},delivered:[],news:[],pilot:null};
  var YEARS=D.years;
  var SEATS=D.seats;
  var PROVINCES=D.provinces;
  var state={year:2026,province:"Copperbelt",query:""};
  // Reported release / utilisation figures, amounts in K millions.
  var MOVEMENT=D.movement;

  function fmtM(v){ // millions
    if(v>=1000) return "K"+(v/1000).toFixed(2).replace(/\.?0+$/,"")+"bn";
    return "K"+(v%1===0?v.toFixed(0):v.toFixed(1))+"m";
  }
  function fmtFull(v){ return "K"+v.toFixed(2)+"m"; }
  function perOf(y){ for(var i=0;i<YEARS.length;i++) if(YEARS[i].year===y) return YEARS[i].per; return 40; }
  function components(totalM){
    var admin=totalM*0.05, rest=totalM-admin;
    return [
      {key:"community",label:"Community projects",desc:"Infrastructure, water, roads — incl. 5% disaster contingency within this share",pct:57,color:"#167347",amount:rest*0.60},
      {key:"empower",label:"Youth & women empowerment",desc:"40% grants · 60% soft loans",pct:19,color:"#e87511",amount:rest*0.20},
      {key:"bursary",label:"Bursaries",desc:"Secondary boarding & skills development",pct:19,color:"#b78a12",amount:rest*0.20},
      {key:"admin",label:"Administration",desc:"Capped at 5% of the fund",pct:5,color:"#5c6b60",amount:admin}
    ];
  }

  var pills=document.getElementById("yearPills"); if(pills){
  YEARS.forEach(function(y){
    var b=document.createElement("button");
    b.className="ypill"; b.type="button"; b.textContent=y.year;
    b.setAttribute("aria-pressed", y.year===state.year?"true":"false");
    b.addEventListener("click",function(){ setYear(y.year); });
    pills.appendChild(b); pills.appendChild(document.createTextNode(" "));
  });

  }
  var barsEl=document.getElementById("bars"); if(barsEl){
  var maxPer=40;
  YEARS.forEach(function(y){
    var c=document.createElement("button");
    c.className="barcol"+(y.year===state.year?" sel":""); c.type="button";
    c.setAttribute("aria-label", y.year+": K"+y.per+" million per constituency");
    c.innerHTML='<span class="amt">K'+y.per+'</span><span class="bar" style="height:'+Math.max(3,(y.per/maxPer)*72)+'%"></span><span class="yr">'+y.year+'</span>';
    c.addEventListener("click",function(){ setYear(y.year); });
    barsEl.appendChild(c);
  });

  }
  function renderDonut(totalM){
    if(!document.getElementById("donut")) return;
    var comps=components(totalM), svg=document.getElementById("donut");
    var cx=84,cy=84,r=62,sw=22,circ=2*Math.PI*r,off=0,parts="";
    comps.forEach(function(c){
      var frac=c.amount/totalM, len=frac*circ;
      parts+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+c.color+'" stroke-width="'+sw+'" stroke-dasharray="'+Math.max(0,len-2)+' '+circ+'" stroke-dashoffset="'+(-off)+'" transform="rotate(-90 '+cx+' '+cy+')"/>';
      off+=len;
    });
    parts+='<text x="'+cx+'" y="'+(cy-4)+'" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="26" fill="currentColor">'+fmtM(totalM)+'</text>';
    parts+='<text x="'+cx+'" y="'+(cy+16)+'" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.65">per constituency</text>';
    svg.innerHTML=parts;
    var leg=document.getElementById("legend"); leg.innerHTML="";
    comps.forEach(function(c){
      var d=document.createElement("div"); d.className="leg";
      d.innerHTML='<span class="sw" style="background:'+c.color+'"></span><span><span class="t">'+c.label+' ('+c.pct+'%)</span><br><span class="d">'+c.desc+'</span></span><span class="a">'+fmtFull(c.amount)+'</span>';
      leg.appendChild(d);
    });
    document.getElementById("splitSub").textContent="For a "+fmtM(totalM)+" allocation ("+state.year+"), under the CDF Guidelines.";
  }


  function slugOf(nm){ return nm.toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,''); }
  var mapBuilt = false;
  function renderMap(){
    var svg = document.getElementById('zmMap');
    if (!svg || !window.ZM_PROVINCES) return;
    var per = perOf(state.year);
    var allocs = PROVINCES.map(function(pr){ return pr.seats * per; });
    var mn = Math.min.apply(null, allocs), mx = Math.max.apply(null, allocs);
    function shade(t){
      var c1 = [231, 240, 231], c2 = [23, 92, 46];
      var c = c1.map(function(v, i){ return Math.round(v + (c2[i] - v) * t); });
      return 'rgb(' + c.join(',') + ')';
    }
    if (!mapBuilt) {
      mapBuilt = true;
      PROVINCES.forEach(function(pr){
        var d = window.ZM_PROVINCES[pr.name];
        if (!d) return;
        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        path.dataset.province = pr.name;
        var title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
        title.textContent = pr.name;
        path.appendChild(title);
        path.addEventListener('click', function(){
          window.location.href = 'provinces/' + slugOf(pr.name) + '.html';
        });
        svg.appendChild(path);
      });
    }
    svg.querySelectorAll('path').forEach(function(path){
      var pr = null;
      PROVINCES.forEach(function(x){ if (x.name === path.dataset.province) pr = x; });
      if (!pr) return;
      var t = (mx - mn) ? (pr.seats * per - mn) / (mx - mn) : 0.5;
      var sel = pr.name === state.province;
      path.setAttribute('fill', shade(0.2 + 0.8 * t));
      path.setAttribute('stroke', sel ? '#d4a017' : '#ffffff');
      path.setAttribute('stroke-width', sel ? '3' : '1.2');
      path.querySelector('title').textContent = pr.name + ' — ' + pr.seats + ' constituencies · ' + fmtM(pr.seats * per) + ' in ' + state.year;
    });
  }
  function renderProvinces(){
    if(!document.getElementById("provList")) return;
    var per=perOf(state.year);
    document.getElementById("pAllocHead").textContent=state.year+" allocation";
    var list=document.getElementById("provList"); list.innerHTML="";
    var shown=0;
    PROVINCES.forEach(function(p){
      if(state.query && p.name.toLowerCase().indexOf(state.query.toLowerCase())===-1) return;
      shown++;
      var total=p.seats*per, share=(p.seats/SEATS*100);
      var b=document.createElement("button"); b.type="button";
      b.className="prow"+(p.name===state.province?" sel":"");
      b.innerHTML='<span class="pn">'+p.name+'</span><span class="num">'+p.seats+'<span>seats</span></span><span class="num">'+fmtM(total)+'<span>in '+state.year+'</span></span><span class="num share">'+share.toFixed(1)+'%<span>of fund</span></span>';
      b.addEventListener("click",function(){ window.location.href="provinces/"+slugOf(p.name)+".html"; });
      list.appendChild(b);
    });
    if(!shown) list.innerHTML='<p class="empty">No province matches that search.</p>';
    document.getElementById("provNote").textContent="Province totals are constituency count × "+fmtM(per)+" for "+state.year+" — CDF allocates equally per constituency, not by population.";
    renderMap();
  }

  function renderDetail(){
    if(!document.getElementById("detailCard")) return;
    var per=perOf(state.year);
    var p=null; PROVINCES.forEach(function(x){ if(x.name===state.province) p=x; });
    if(!p) p=PROVINCES[0];
    var total=p.seats*per, comps=components(total);
    var html='<h3>'+p.name+' Province</h3><p class="sub">'+p.seats+' constituencies · '+fmtM(per)+' each in '+state.year+'</p>';
    html+='<div class="big">'+fmtM(total)+'</div><p class="sub" style="margin:2px 0 0">total CDF allocation for '+state.year+'</p><div class="split">';
    comps.forEach(function(c){
      html+='<div class="srow"><span class="st">'+c.label+'<small>'+c.pct+'% of province total</small></span><span class="sa">'+fmtM(c.amount)+'</span></div>';
    });
    html+='</div><p class="chart-note">That works out to about '+fmtM(total/ (p.seats))+' per constituency in this province — the same as everywhere else in Zambia, by design.</p>';
    var yrs=(D.years||[]).slice().sort(function(a,b){var av=(typeof a==='object')?a.year:a, bv=(typeof b==='object')?b.year:b; return av-bv;});
    if(yrs.length>1){
      html+='<h4 class="yt-head">'+p.name+' by year</h4><table class="ytable"><thead><tr><th>Year</th><th>Per constituency</th><th>Province total</th></tr></thead><tbody>';
      yrs.forEach(function(y){
        var yv=(typeof y==='object')?y.year:y, r=(typeof y==='object'&&y.per!=null)?y.per:perOf(yv);
        html+='<tr'+(yv===state.year?' class="yr-on"':'')+'><td>'+yv+'</td><td>'+fmtM(r)+'</td><td>'+fmtM(p.seats*r)+'</td></tr>';
      });
      html+='</tbody></table><p class="chart-note">Every year for this province — the highlighted row is the year selected at the top of the page.</p>';
    }
    document.getElementById("detailCard").innerHTML=html;
  }

  function flowRow(label,sub,fillCls,widthPct,valueHtml){
    return '<div class="frow"><div class="fl">'+label+'<small>'+sub+'</small></div><div class="track"><div class="fill '+fillCls+'" style="width:'+widthPct+'%"></div></div><div class="fv">'+valueHtml+'</div></div>';
  }

  function renderFlow(){
    if(!document.getElementById("flowCard")) return;
    var per=perOf(state.year), total=per*SEATS, mv=MOVEMENT[state.year];
    var html='<h3 style="margin-bottom:14px">'+state.year+' — from allocation to use</h3>';
    html+=flowRow("Allocated", state.year+" budget — 156 × K"+per.toFixed(1)+"m", "", 100, fmtM(total)+"<small>100%</small>");
    if(mv){
      html+=flowRow("Released","Reported disbursed to constituencies","o", mv.releasedPct, fmtM(mv.released)+"<small>≈"+mv.releasedPct+"% of allocation</small>");
      html+=flowRow("Utilisation","Reported share of funds put to use","r", mv.util, mv.util+"%<small>reported rate</small>");
      html+=flowRow("Community projects approved", mv.projCount.toLocaleString("en-GB")+" projects approved nationally in "+state.year, "", mv.projPct, fmtM(mv.projAmt)+"<small>"+mv.projPct+"% of "+state.year+" allocation</small>");
    }else if(state.year===2026){
      html+=flowRow("Released","Releases are reported as the budget year runs","o",0,'<span class="np">Not yet reported</span>');
      html+=flowRow("Utilisation","Reported once constituencies spend released funds","r",0,'<span class="np">Not yet reported</span>');
      html+=flowRow("Community projects approved","Approvals are published as councils submit project lists","",0,'<span class="np">Not yet reported</span>');
    }else{
      html+=flowRow("Released","No national release figure published for "+state.year+" in this snapshot","o",0,'<span class="np">Not published</span>');
      html+=flowRow("Utilisation","No national utilisation figure published for "+state.year+" in this snapshot","r",0,'<span class="np">Not published</span>');
      html+=flowRow("Community projects approved","No national approvals total published for "+state.year+" in this snapshot","",0,'<span class="np">Not published</span>');
    }
    document.getElementById("flowCard").innerHTML=html;
  }

  function renderMoveTable(){
    if(!document.getElementById("moveTable")) return;
    var el=document.getElementById("moveTable"); el.innerHTML="";
    var head=document.createElement("div"); head.className="mhead";
    head.innerHTML="<span>Year</span><span>Allocated</span><span>Released</span><span>Utilisation</span>";
    el.appendChild(head);
    YEARS.forEach(function(y){
      var total=y.per*SEATS, mv=MOVEMENT[y.year];
      var relHtml, utilHtml;
      if(mv){
        relHtml=fmtM(mv.released)+"<small>≈"+mv.releasedPct+"% of allocation</small>";
        utilHtml=mv.util+"%<small>reported rate</small>";
      }else if(y.year===2026){
        relHtml='<span class="np2">Not yet reported</span>';
        utilHtml='<span class="np2">—</span>';
      }else{
        relHtml='<span class="np2">Not published</span>';
        utilHtml='<span class="np2">—</span>';
      }
      var b=document.createElement("button"); b.type="button";
      b.className="mrow"+(y.year===state.year?" sel":"");
      b.setAttribute("aria-label", y.year+": "+fmtM(total)+" allocated. Tap to view "+y.year+" across the dashboard.");
      b.innerHTML='<span class="myr">'+y.year+'</span><span class="mnum">'+fmtM(total)+'<small>K'+y.per.toFixed(1)+'m × 156</small></span><span class="mnum">'+relHtml+'</span><span class="mnum mutil">'+utilHtml+'</span>';
      b.addEventListener("click",function(){ setYear(y.year); });
      el.appendChild(b);
    });
  }

  function setYear(y){
    state.year=y;
    var per=perOf(y), idx=0;
    YEARS.forEach(function(yy,i){ if(yy.year===y) idx=i; });
    if(document.getElementById("kPer")){
    document.getElementById("kPer").textContent="K"+per.toFixed(1)+"m";
    document.getElementById("kPerSub").textContent="Equal allocation to every constituency";
    var total=per*SEATS;
    document.getElementById("kTotal").textContent=fmtM(total);
    document.getElementById("kTotalSub").textContent="156 constituencies × K"+per.toFixed(1)+"m";
    if(idx>0){
      var prev=YEARS[idx-1].per, ch=((per-prev)/prev*100);
      document.getElementById("kChange").textContent=(ch>=0?"+":"")+ch.toFixed(1)+"%";
      document.getElementById("kChangeSub").textContent="Up from K"+prev.toFixed(1)+"m in "+YEARS[idx-1].year;
    }else{
      document.getElementById("kChange").textContent="—";
      document.getElementById("kChangeSub").textContent="Baseline year in this series";
    }
    var growth=per/1.6;
    document.getElementById("kGrowth").textContent=(growth%1===0?growth.toFixed(0):growth.toFixed(1))+"×";
    }
    if(pills){ var pillBtns=pills.querySelectorAll(".ypill");
    YEARS.forEach(function(yy,i){ pillBtns[i].setAttribute("aria-pressed", yy.year===y?"true":"false"); });
    }
    if(barsEl){ var cols=barsEl.querySelectorAll(".barcol");
    YEARS.forEach(function(yy,i){ cols[i].className="barcol"+(yy.year===y?" sel":""); });
    }
    renderDonut(per); renderFlow(); renderMoveTable(); renderProvinces(); renderDetail();
  }

  function renderDelivered(){
    var el=document.getElementById("deliveredTiles"); if(!el) return;
    el.innerHTML="";
    (D.delivered||[]).forEach(function(t){
      var d=document.createElement("div"); d.className="tile";
      d.innerHTML='<div class="v">'+t.value+'</div><div class="t">'+t.title+'</div><div class="d">'+t.desc+'</div>';
      el.appendChild(d);
    });
  }

  function renderNews(){
    var sec=document.getElementById("newsSection"), el=document.getElementById("newsList");
    if(!sec||!el) return;
    var items=D.news||[];
    if(!items.length){ sec.style.display="none"; return; }
    el.innerHTML="";
    items.forEach(function(n,i){
      var d=document.createElement("article");
      if(i>0) d.style.cssText="border-top:1px solid var(--line);margin-top:22px;padding-top:20px";
      var paras=String(n.text||"").split(/\n\n+/).filter(function(p){return p.trim();});
      var html='<h3 style="margin:0;font-size:1.22rem;line-height:1.3">'+n.title+'</h3><div class="sub" style="margin:3px 0 8px">'+n.date+' · '+n.source+'</div>';
      html+=paras.map(function(p){ return '<p style="margin:0 0 10px;line-height:1.55">'+p+'</p>'; }).join("");
      if(n.url) html+='<p style="margin:2px 0 0"><a href="'+n.url+'" target="_blank" rel="noopener">Read the source →</a></p>';
      d.innerHTML=html;
      el.appendChild(d);
    });
  }

  if(D.meta){
    var sd=document.getElementById("snapDate");
    if(sd&&D.meta.snapshotDate) sd.textContent=D.meta.snapshotDate;
    var lc=document.getElementById("lastChecked");
    if(lc&&D.meta.lastChecked) lc.textContent="Data last checked: "+D.meta.lastChecked+" — refreshed by a weekly source check of ministry, council and news publications.";
  }
  renderDelivered();
  renderNews();

  /* ---------- scenario tool ---------- */
  var scSeatsVal = 226;
  function yearTotal(y){ return perOf(y) * (typeof SEATS !== 'undefined' ? SEATS : 156); }
  function renderScenario(){
    if(!document.getElementById('scRate')) return;
    var rate = parseFloat(document.getElementById('scRate').value) || 0;
    var total = rate * scSeatsVal;
    document.getElementById('scTotal').textContent = fmtM(total);
    var base = yearTotal(2026);
    var diff = total - base, pct = base ? (diff/base*100) : 0;
    document.getElementById('scVs').textContent =
      (diff >= 0 ? '+' : '-') + fmtM(Math.abs(diff)) + ' (' + (diff>=0?'+':'') + pct.toFixed(1) + '%) vs 2026 actual (' + fmtM(base) + ')';
    document.querySelectorAll('#scSeats .ypill').forEach(function(b){
      b.classList.toggle('on', +b.dataset.seats === scSeatsVal);
    });
  }
  var _sr=document.getElementById('scRate'); if(_sr) _sr.addEventListener('input', renderScenario);
  document.querySelectorAll('#scSeats .ypill').forEach(function(b){
    b.addEventListener('click', function(){ scSeatsVal = +b.dataset.seats; renderScenario(); });
  });

  /* ---------- Lusaka pilot explorer ---------- */
  var STATUS = {
    approved:{label:'Approved', color:'#8a6d1a'}, funded:{label:'Funded', color:'#33607e'},
    in_progress:{label:'In progress', color:'#b35c12'}, completed:{label:'Completed', color:'#1c6b3c'},
    stalled:{label:'Stalled', color:'#a12c2c'}, completed_unused:{label:'Completed, unused', color:'#6b4fa1'},
    unknown:{label:'Status not stated', color:'#777'}
  };
  function fmtKwacha(m){
    if (m === null || m === undefined) return 'not published';
    var k = m * 1000000;
    if (k >= 10000000) return 'K' + m.toFixed(2).replace(/\.00$/, '') + 'm';
    return 'K' + Math.round(k).toLocaleString('en-GB');
  }
  function badge(st){
    var d = STATUS[st] || STATUS.unknown;
    return '<span class="badge" style="background:' + d.color + '">' + d.label + '</span>';
  }
  var pilotSel = null, pilotStatus = 'all', xpProv = null;
  function xpData(){ return (D && D.projects) ? D.projects : null; }
  function xpProvince(){
    var X = xpData(); if (!X) return null;
    return X.provinces.filter(function(p){ return p.name === xpProv; })[0] || null;
  }
  function pilotFiltered(cc){
    var q = (document.getElementById('projSearch').value || '').toLowerCase();
    return cc.projects.filter(function(pr){
      if (pilotStatus !== 'all' && pr.status !== pilotStatus) return false;
      if (q && pr.name.toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
  }
  function fyStripFor(el, total, years, known){
    if (!el) return;
    var chips = Object.keys(years || {}).sort().map(function(y){
      return '<span class="fychip"><b>' + y + '</b>' + years[y] + ' projects</span>';
    }).join('');
    var unknown = total - (known || 0);
    if (unknown > 0) chips += '<span class="fychip dim"><b>Not published</b>' + unknown + ' projects</span>';
    el.innerHTML = chips;
  }
  function renderProjects(){
    var X = xpData();
    if (!X || !document.getElementById('pilotSection')) return;
    document.getElementById('pilotSection').hidden = false;
    var P = xpProvince();
    var q = (document.getElementById('projSearch').value || '').toLowerCase();
    var pc = document.getElementById('provChips');
    if (pc) {
      pc.innerHTML = '<button type="button" class="chip' + (!xpProv ? ' on' : '') + '" aria-pressed="' + (!xpProv) + '" data-pv="">All provinces</button>' +
        X.provinces.map(function(p){
          return '<button type="button" class="chip' + (xpProv === p.name ? ' on' : '') + '" aria-pressed="' + (xpProv === p.name) + '" data-pv="' + p.name + '">' + p.name + ' · ' + p.totalProjects + '</button>';
        }).join('');
      pc.querySelectorAll('.chip').forEach(function(b){
        b.addEventListener('click', function(){ xpProv = b.dataset.pv || null; pilotSel = null; renderProjects(); });
      });
    }
    var seen = {};
    (P ? [P] : X.provinces).forEach(function(p){ p.constituencies.forEach(function(cc){ cc.projects.forEach(function(pr){ seen[pr.status] = 1; }); }); });
    var schips = ['all'].concat(Object.keys(STATUS).filter(function(k){ return seen[k]; }));
    document.getElementById('statusChips').innerHTML = schips.map(function(k){
      return '<button type="button" class="chip' + (pilotStatus === k ? ' on' : '') + '" aria-pressed="' + (pilotStatus === k) + '" data-st="' + k + '">' +
        (k === 'all' ? 'All statuses' : STATUS[k].label) + '</button>';
    }).join('');
    document.querySelectorAll('#statusChips .chip').forEach(function(b){
      b.addEventListener('click', function(){ pilotStatus = b.dataset.st; renderProjects(); });
    });
    var listEl = document.getElementById('pilotConsts');
    var note = document.getElementById('pilotNote');
    if (q) {
      var hits = [];
      X.provinces.forEach(function(p){ p.constituencies.forEach(function(cc){ cc.projects.forEach(function(pr){
        if (pilotStatus !== 'all' && pr.status !== pilotStatus) return;
        if (pr.name.toLowerCase().indexOf(q) > -1) hits.push({p: p.name, c: cc.name, pr: pr});
      }); }); });
      listEl.innerHTML = '<div class="prow sel"><span class="pname">Search results</span><span class="pdetail-x">' + hits.length + ' projects match</span></div>';
      document.getElementById('pdName').textContent = 'Search — all provinces';
      document.getElementById('pdMeta').textContent = hits.length + ' projects match · showing up to 200';
      var shown = hits.slice(0, 200);
      document.getElementById('pdBody').innerHTML = '<div id="projDetailSlot"></div>' + (shown.length ? shown.map(function(h, i){
        return '<div class="prow jrow" data-i="' + i + '"><span class="pname">' + h.pr.name + ' <span class="pdetail-x">' + h.c + ', ' + h.p + '</span></span>' +
          '<span class="amt">' + fmtKwacha(h.pr.budgetM) + '</span>' + badge(h.pr.status) + '</div>';
      }).join('') : '<p class="chart-note">No projects match this search.</p>');
      document.querySelectorAll('#pdBody .jrow').forEach(function(r){
        r.addEventListener('click', function(){ var h = shown[+r.dataset.i]; if (h && h.pr.url) window.location.href = h.pr.url; });
      });
      if (note) note.textContent = 'Searching all ' + X.totalProjects + ' tracked projects across ' + X.provinces.length + ' provinces. Clear the search to browse by province.';
      fyStripFor(document.getElementById('fyStrip'), X.totalProjects, X.fundingYears, X.fundingYearKnown);
      return;
    }
    if (!P) {
      listEl.innerHTML = X.provinces.map(function(p){
        return '<div class="prow" data-pv="' + p.name + '"><span class="pname">' + p.name + '</span>' +
          '<span class="pdetail-x">' + p.totalProjects + ' projects · ' + p.constituencies.length + ' constituencies</span></div>';
      }).join('');
      listEl.querySelectorAll('.prow').forEach(function(r){
        r.addEventListener('click', function(){ xpProv = r.dataset.pv; pilotSel = null; renderProjects(); });
      });
      document.getElementById('pdName').textContent = 'All provinces';
      document.getElementById('pdMeta').textContent = X.totalProjects + ' projects tracked across ' + X.provinces.length + ' provinces';
      var _bud = 0, _mix = {}, _cats = {};
      X.provinces.forEach(function(p){ p.constituencies.forEach(function(cc){ cc.projects.forEach(function(pr){
        _bud += pr.budgetM || 0; _mix[pr.status] = (_mix[pr.status] || 0) + 1; _cats[pr.category] = (_cats[pr.category] || 0) + 1;
      }); }); });
      var _mixTxt = Object.keys(_mix).sort(function(a, b){ return _mix[b] - _mix[a]; }).map(function(k){ return (STATUS[k] ? STATUS[k].label : k) + ' ' + _mix[k]; }).join(' · ');
      var _topCats = Object.keys(_cats).sort(function(a, b){ return _cats[b] - _cats[a]; }).slice(0, 5).map(function(k){ return k.charAt(0).toUpperCase() + k.slice(1) + ' ' + _cats[k]; }).join(' · ');
      var _summary = '<p class="chart-note"><b>' + X.totalProjects + ' projects · ' + fmtKwacha(Math.round(_bud * 100) / 100) + ' in published budgets</b></p>' +
        '<p class="chart-note">' + _mixTxt + '</p>' +
        '<p class="chart-note">Most tracked categories — ' + _topCats + '</p>';
      document.getElementById('pdBody').innerHTML = '<div id="projDetailSlot"></div>' + _summary + X.provinces.map(function(p){
        return '<div class="prow jrow" data-pv="' + p.name + '"><span class="pname">' + p.name + '</span>' +
          '<span class="pdetail-x">' + p.totalProjects + ' projects' + (p.fundingYearKnown ? ' · funding year published for ' + p.fundingYearKnown : '') + '</span></div>';
      }).join('');
      document.querySelectorAll('#pdBody .jrow').forEach(function(r){
        r.addEventListener('click', function(){ xpProv = r.dataset.pv; pilotSel = null; renderProjects(); });
      });
      if (note) note.textContent = X.totalProjects + ' projects tracked across ' + X.provinces.length + ' provinces. Pick a province to browse its constituencies. Every project links to its published source; amounts are shown only where the source published them.';
      fyStripFor(document.getElementById('fyStrip'), X.totalProjects, X.fundingYears, X.fundingYearKnown);
      return;
    }
    listEl.innerHTML = P.constituencies.map(function(cc){
      var known = cc.projects.filter(function(x){return x.budgetM !== null;}).length;
      return '<div class="prow' + (cc.name === pilotSel ? ' sel' : '') + '" data-c="' + cc.name + '">' +
        '<span class="pname">' + cc.name + '</span>' +
        '<span class="pdetail-x">' + cc.count + ' projects' + (known ? ' · ' + fmtKwacha(cc.budgetM) + ' published' : '') + '</span></div>';
    }).join('');
    listEl.querySelectorAll('.prow').forEach(function(r){
      r.addEventListener('click', function(){ pilotSel = r.dataset.c; renderProjects(); });
    });
    if (!pilotSel || !P.constituencies.some(function(x){ return x.name === pilotSel; })) {
      document.getElementById('pdName').textContent = P.name + ' province';
      document.getElementById('pdMeta').textContent = P.totalProjects + ' projects · ' + P.constituencies.length + ' constituencies — pick one to browse its projects';
      var mix = {};
      P.constituencies.forEach(function(cc){ cc.projects.forEach(function(pr){ mix[pr.status] = (mix[pr.status] || 0) + 1; }); });
      var mixTxt = Object.keys(mix).map(function(k){ return (STATUS[k] ? STATUS[k].label : k) + ': ' + mix[k]; }).join(' · ');
      var top = P.constituencies.slice().sort(function(a,b){return b.count - a.count;}).slice(0, 5);
      document.getElementById('pdBody').innerHTML = '<div id="projDetailSlot"></div>' +
        '<p class="chart-note">' + mixTxt + '</p>' +
        '<p class="chart-note">Projects arrive in per-year council lists — a constituency showing many projects is usually showing several funding years at once, not one big approval. Biggest in ' + P.name + ':</p>' +
        top.map(function(cc){ return '<div class="prow jrow" data-sel="' + cc.name + '"><span class="pname">' + cc.name + '</span><span class="pdetail-x">' + cc.count + ' projects</span></div>'; }).join('');
      document.querySelectorAll('#pdBody .jrow').forEach(function(r){
        r.addEventListener('click', function(){ pilotSel = r.dataset.sel; renderProjects(); });
      });
      if (note) note.textContent = P.totalProjects + ' projects tracked across ' + P.constituencies.length + ' ' + P.name + ' constituencies. Pick a constituency on the left to browse its projects, grouped by funding year where the lists publish one.';
      fyStripFor(document.getElementById('fyStrip'), P.totalProjects, P.fundingYears, P.fundingYearKnown);
      return;
    }
    var cc = P.constituencies.filter(function(x){ return x.name === pilotSel; })[0];
    var items = pilotFiltered(cc);
    document.getElementById('pdName').textContent = cc.name + ' constituency — ' + P.name;
    document.getElementById('pdMeta').innerHTML = items.length + ' of ' + cc.count + ' published projects shown' + (cc.url ? ' · <a href="' + cc.url + '">Open the ' + cc.name + ' page →</a>' : '');
    var groups = {}, order = [];
    items.forEach(function(pr){ var k = pr.fundingYear ? String(pr.fundingYear) : ''; if (!(k in groups)) { groups[k] = []; order.push(k); } groups[k].push(pr); });
    order.sort(function(a, b){ if (a === '') return 1; if (b === '') return -1; return b - a; });
    var grouped = order.length > 1;
    var flat = [];
    var _titles = cc.projects.map(function(pr){ return (pr.source && pr.source.title) || ''; });
    function _hasT(ws){ return _titles.some(function(t){ var L = t.toLowerCase(); return ws.some(function(w){ return L.indexOf(w) > -1; }); }); }
    var _kinds = [];
    if (_hasT(['approved', 'approval'])) _kinds.push('approval lists');
    if (_hasT(['commission', 'handover', 'handed over'])) _kinds.push('commissioning / handover reports');
    if (_hasT(['minutes'])) _kinds.push('CDFC minutes');
    if (_hasT(['newsletter'])) _kinds.push('council newsletters');
    if (_hasT(['catalogue', 'database', 'project list', 'projects list', 'list of'])) _kinds.push('published project lists');
    if (_hasT(['tender', 'zppa', 'e-gp', 'invitation for bids'])) _kinds.push('tender notices');
    if (!_kinds.length) _kinds.push('council and news reports');
    var _rec = 'Record: based on ' + _kinds.join(', ') + '.';
    var _st = {}; cc.projects.forEach(function(pr){ _st[pr.status] = 1; });
    if (_kinds.indexOf('approval lists') === -1 && _st.completed && !_st.approved)
      _rec += ' No approval list has been published for this constituency — the public record here starts at handover.';
    var html = '<div id="projDetailSlot"></div><p class="chart-note">' + _rec + '</p>';
    order.forEach(function(k){
      if (grouped) html += '<div class="ghead">' + (k ? k + ' CDF' : 'Funding year not published') + ' — ' + groups[k].length + ' projects</div>';
      groups[k].forEach(function(pr){
        flat.push(pr);
        html += '<div class="prow jrow" data-i="' + (flat.length - 1) + '"><span class="pname">' + pr.name + '</span>' +
          '<span class="amt">' + fmtKwacha(pr.budgetM) + '</span>' + badge(pr.status) + '</div>';
      });
    });
    if (!items.length) html += '<p class="chart-note">No projects match this filter.</p>';
    document.getElementById('pdBody').innerHTML = html;
    document.querySelectorAll('#pdBody .jrow').forEach(function(r){
      r.addEventListener('click', function(){
        var pr = flat[+r.dataset.i];
        if (pr && pr.url) { window.location.href = pr.url; return; }
        showProject(pr);
      });
    });
    var fyTxt = '';
    if (P.fundingYears && P.fundingYearKnown) {
      var parts = Object.keys(P.fundingYears).sort().map(function(y){ return y + ': ' + P.fundingYears[y]; }).join(' · ');
      fyTxt = ' Funding year is published for ' + P.fundingYearKnown + ' of ' + P.totalProjects + ' projects (' + parts + '); the rest are published without one.';
    }
    if (note) note.textContent =
      P.totalProjects + ' projects tracked across ' + P.constituencies.length + ' ' + P.name + ' constituencies. ' +
      'Every project links to its published source; amounts are shown only where the source published them.' + fyTxt;
    fyStripFor(document.getElementById('fyStrip'), P.totalProjects, P.fundingYears, P.fundingYearKnown);
  }
  function showProject(pr){
    var rows = [
      ['Status', (STATUS[pr.status] || STATUS.unknown).label + (pr.completionPct ? ' · ' + pr.completionPct + '% complete' : '')],
      ['Budget', fmtKwacha(pr.budgetM)],
      ['Funding year', pr.fundingYear ? String(pr.fundingYear) : 'Not published'],
      ['Ward', pr.ward || '—'], ['Category', pr.category || '—'],
      ['Contractor', pr.contractor || '—']
    ];
    var html = '<div class="pdetail"><h3>' + pr.name + '</h3><div class="meta">' +
      rows.map(function(r){ return '<div><b>' + r[0] + '</b>' + r[1] + '</div>'; }).join('') + '</div>';
    if (pr.photo) html += '<figure><img src="' + pr.photo.url + '" alt="Project photo"><figcaption>Photo: ' + (pr.photo.credit || '') + '</figcaption></figure>';
    if (pr.note) html += '<p class="chart-note">' + pr.note + '</p>';
    if (pr.source) html += '<p class="chart-note">Source: ' + (pr.source.url ? '<a href="' + pr.source.url + '" target="_blank" rel="noopener">' + pr.source.publisher + '</a>' : pr.source.publisher) + (pr.source.title ? ' — ' + pr.source.title : '') + '</p>';
    html += '</div>';
    var slot = document.getElementById('projDetailSlot');
    slot.innerHTML = html;
    if (slot.scrollIntoView) slot.scrollIntoView({behavior:'smooth', block:'nearest'});
  }
  function renderGallery(){
    var grid = document.getElementById('photoGrid');
    if (!grid || !D || !D.projects) return;
    var total = 0, html = '';
    D.projects.provinces.forEach(function(p){
      var items = [];
      p.constituencies.forEach(function(cc){ cc.projects.forEach(function(pr){ if (pr.photo) items.push({pr: pr, cc: cc.name}); }); });
      if (!items.length) return;
      total += items.length;
      html += '<h3 class="ghead">' + p.name + ' — ' + items.length + ' photographed</h3><div class="ggrid">' +
        items.map(function(x){
          var st = STATUS[x.pr.status] ? STATUS[x.pr.status].label : x.pr.status;
          return '<a class="gcard" href="' + x.pr.url + '"><img src="' + x.pr.photo.url + '" alt="Photo: ' + x.pr.name.replace(/"/g, '') + '" loading="lazy">' +
            '<span class="gb"><b>' + x.pr.name + '</b>' +
            '<span class="gm">' + x.cc + ' constituency · ' + st + '</span>' +
            '<span class="gc">Photo: ' + (x.pr.photo.credit || '') + '</span></span></a>';
        }).join('') + '</div>';
    });
    grid.innerHTML = html;
    var sum = document.getElementById('photoCount');
    if (sum) sum.textContent = total;
  }
  var _ps=document.getElementById('projSearch'); if(_ps) _ps.addEventListener('input', renderProjects);
  renderScenario();
  renderProjects();
  renderGallery();

  var _pv=document.getElementById("provSearch"); if(_pv) _pv.addEventListener("input",function(e){ state.query=e.target.value; renderProvinces(); });
  setYear(2026);
})();
