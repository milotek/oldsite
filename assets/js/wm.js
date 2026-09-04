// Workspace switching, the way the window manager does it: press the number.
(function () {
  "use strict";

  var pills = Array.prototype.slice.call(document.querySelectorAll(".ws"));
  var keys = document.getElementById("keys");
  var toggle = document.getElementById("keys-toggle");
  var clock = document.getElementById("clock");

  function showKeys(on) {
    if (!keys || !toggle) return;
    keys.hidden = !on;
    toggle.setAttribute("aria-expanded", String(on));
  }

  if (toggle) {
    toggle.addEventListener("click", function () { showKeys(keys.hidden); });
  }
  if (keys) {
    keys.addEventListener("click", function () { showKeys(false); });
  }

  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var el = e.target;
    if (el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName))) return;

    if (e.key === "Escape") { showKeys(false); return; }
    if (e.key === "?") { e.preventDefault(); showKeys(keys && keys.hidden); return; }

    var hit = pills.filter(function (p) { return p.dataset.key === e.key; })[0];
    if (hit && !hit.classList.contains("is-active")) {
      e.preventDefault();
      window.location.href = hit.getAttribute("href");
    }
  });

  // Local time in London, because that is where I am and it is the only
  // honest thing a status bar can tell you about someone else's machine.
  if (clock) {
    var fmt;
    try {
      fmt = new Intl.DateTimeFormat("en-GB", {
        hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "Europe/London"
      });
    } catch (err) { return; }
    var tick = function () { clock.textContent = fmt.format(new Date()); };
    tick();
    setInterval(tick, 15000);
  }
})();
