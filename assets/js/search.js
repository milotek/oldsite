/* Client-side search over index.json.
   Progressive enhancement: with JS off the header form submits to /index/,
   which is the same data rendered as a plain page. */
(function () {
  var input = document.getElementById('q');
  var form = input && input.closest('form');
  var results = document.getElementById('results');
  var page = document.getElementById('page');
  var root = document.body.dataset.root || './';
  if (!input || !results || !page) return;

  var records = null, pending = null, sel = -1, rows = [];

  // The counted placeholder is nice but clips under about 620px, so the markup
  // ships the short one and we upgrade it when there's room.
  function sizePlaceholder() {
    var full = input.dataset.full;
    if (full) input.placeholder = window.innerWidth >= 620 ? full : 'search projects, art, writing';
  }
  sizePlaceholder();
  window.addEventListener('resize', sizePlaceholder);

  function load() {
    if (records) return Promise.resolve(records);
    if (!pending) {
      pending = fetch(root + 'index.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          records = data.records.map(function (r) {
            r._hay = (r.t + ' ' + r.k + ' ' + r.g.join(' ') + ' ' + r.d + ' ' + r.y + ' ' + r.s).toLowerCase();
            r._t = r.t.toLowerCase();
            return r;
          });
          return records;
        });
    }
    return pending;
  }

  function score(rec, tokens) {
    var total = 0;
    for (var i = 0; i < tokens.length; i++) {
      var tok = tokens[i];
      if (rec._hay.indexOf(tok) === -1) return 0;
      if (rec._t === tok) total += 12;
      else if (rec._t.indexOf(tok) === 0) total += 8;
      else if (rec._t.indexOf(tok) !== -1) total += 5;
      if (rec.g.indexOf(tok) !== -1) total += 6;
      if (rec.k === tok) total += 4;
      total += 1;
    }
    return total;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function href(rec) {
    return /^(https?:|mailto:)/.test(rec.u) ? rec.u : root + rec.u;
  }

  function render(q) {
    var tokens = q.toLowerCase().split(/\s+/).filter(Boolean);
    var hits = [];
    for (var i = 0; i < records.length; i++) {
      var s = score(records[i], tokens);
      if (s > 0) hits.push([s, records[i]]);
    }
    hits.sort(function (a, b) {
      if (b[0] !== a[0]) return b[0] - a[0];
      return (b[1].y || '').localeCompare(a[1].y || '');
    });

    if (!hits.length) {
      results.innerHTML =
        '<div class="res-empty"><img src="' + root + 'assets/img/noresults.webp" alt="" width="200" height="200">' +
        '<p>Nothing for <b>' + esc(q) + '</b>.</p>' +
        '<p class="mono">try: nix &middot; lua &middot; godot &middot; hardware &middot; art</p></div>';
      rows = [];
      sel = -1;
      return;
    }

    var html = '<p class="res-count"><b>' + hits.length + '</b> result' + (hits.length === 1 ? '' : 's') +
      ' for &ldquo;' + esc(q) + '&rdquo;</p><div class="rows">';
    for (var j = 0; j < hits.length; j++) {
      var r = hits[j][1];
      html += '<a class="row" href="' + esc(href(r)) + '">' +
        '<span class="row-kind">' + esc(r.k) + '</span>' +
        '<span class="row-main"><span class="row-title">' + esc(r.t) + '</span>' +
        '<span class="row-blurb">' + esc(r.d) + '</span></span>' +
        '<span class="row-meta">' + esc(r.y || r.s) + '</span></a>';
    }
    html += '</div><p class="res-hint">&uarr;&darr; to move, enter to open, esc to clear</p>';
    results.innerHTML = html;
    rows = results.querySelectorAll('.row');
    sel = -1;
  }

  function apply(q, push) {
    q = q.trim();
    form.classList.toggle('active', !!q);
    if (!q) {
      results.hidden = true;
      results.innerHTML = '';
      page.hidden = false;
      rows = [];
      sel = -1;
    } else {
      load().then(function () {
        if (input.value.trim() !== q) return;
        render(q);
        results.hidden = false;
        page.hidden = true;
      });
    }
    if (push) {
      var url = location.pathname + (q ? '?q=' + encodeURIComponent(q) : '') + location.hash;
      history.replaceState(null, '', url);
    }
  }

  function move(delta) {
    if (!rows.length) return;
    if (sel >= 0) rows[sel].classList.remove('sel');
    sel = (sel + delta + rows.length + 1) % (rows.length + 1);
    if (sel === rows.length) { sel = -1; input.focus(); return; }
    rows[sel].classList.add('sel');
    rows[sel].scrollIntoView({ block: 'nearest' });
  }

  input.addEventListener('input', function () { apply(input.value, true); });
  form.addEventListener('submit', function (e) {
    if (rows.length) { e.preventDefault(); (rows[sel >= 0 ? sel : 0]).click(); }
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Escape') { input.value = ''; apply('', true); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      input.focus();
      input.select();
    }
  });

  var initial = new URLSearchParams(location.search).get('q');
  if (initial) { input.value = initial; apply(initial, false); }
  else { load(); }
})();
