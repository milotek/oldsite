// Drives the preview pane on the front page. Everything it shows is already
// in the DOM as a row, so with this file blocked the page still lists the lot.
(function () {
  var data = document.getElementById("roster-data");
  var pane = document.getElementById("pane");
  var roster = document.getElementById("roster");
  if (!data || !pane || !roster) return;

  var items = JSON.parse(data.textContent);
  var rows = Array.prototype.slice.call(roster.querySelectorAll(".rw"));
  var wide = window.matchMedia("(min-width: 1040px)");
  var current = -1;

  var el = {
    shot: document.getElementById("pane-shot"),
    group: document.getElementById("pgroup"),
    year: document.getElementById("pyear"),
    title: document.getElementById("ptitle"),
    tag: document.getElementById("ptag"),
    stack: document.getElementById("pstack"),
    body: document.getElementById("pbody"),
    open: document.getElementById("popen"),
    links: document.getElementById("plinks")
  };

  function text(node, value) { if (node) node.textContent = value || ""; }

  function select(i) {
    if (i === current || !items[i]) return;
    var it = items[i];
    if (rows[current]) rows[current].classList.remove("on");
    rows[i].classList.add("on");
    current = i;

    el.shot.innerHTML = "";
    if (it.thumb) {
      var img = document.createElement("img");
      img.src = it.thumb;
      img.width = 800;
      img.height = 450;
      img.alt = "";
      el.shot.appendChild(img);
    } else {
      var slate = document.createElement("span");
      slate.textContent = it.slate || it.title;
      el.shot.appendChild(slate);
    }

    text(el.group, it.group);
    text(el.year, it.year);
    text(el.title, it.title);
    text(el.tag, it.tagline);
    text(el.body, it.blurb);
    el.open.href = it.href;

    el.stack.innerHTML = "";
    it.stack.forEach(function (s) {
      var li = document.createElement("li");
      li.textContent = s;
      el.stack.appendChild(li);
    });

    el.links.innerHTML = "";
    it.links.slice(0, 3).forEach(function (l) {
      var a = document.createElement("a");
      a.href = l.url;
      a.textContent = l.label;
      el.links.appendChild(a);
    });
  }

  rows.forEach(function (row, i) {
    row.addEventListener("mouseenter", function () { if (wide.matches) select(i); });
    row.addEventListener("focus", function () { if (wide.matches) select(i); });
  });

  // Arrows only bite while focus is inside the list, so ordinary scrolling
  // never gets hijacked.
  roster.addEventListener("keydown", function (e) {
    var step = 0;
    if (e.key === "ArrowDown" || e.key === "j") step = 1;
    if (e.key === "ArrowUp" || e.key === "k") step = -1;
    if (!step) return;
    var from = rows.indexOf(document.activeElement);
    var next = Math.max(0, Math.min(rows.length - 1, (from < 0 ? 0 : from + step)));
    e.preventDefault();
    rows[next].focus();
  });

  if (wide.matches) select(0);
})();
