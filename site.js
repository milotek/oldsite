"use strict";

// Workspaces. The hash is the router; the bar links are plain anchors so the
// browser does the navigation and this only reacts to it.
const WORKSPACES = ["home", "projects", "games", "art", "cv", "contact"];
const ALIASES = { "": "home", arts: "art", resume: "cv" };
const sections = WORKSPACES.map((id) => document.getElementById(id));
const wsLinks = [...document.querySelectorAll(".workspaces a")];
const wsName = document.getElementById("ws-name");
let currentIndex = -1;

function workspaceFromHash() {
  const raw = decodeURIComponent(location.hash.slice(1)).toLowerCase();
  const name = ALIASES[raw] ?? raw;
  return WORKSPACES.includes(name) ? name : "home";
}

function showWorkspace(name) {
  const next = WORKSPACES.indexOf(name);
  if (next === currentIndex) return;
  const fromRight = currentIndex === -1 || next > currentIndex;
  sections.forEach((el, i) => {
    el.classList.remove("slide");
    el.classList.toggle("active", i === next);
  });
  const active = sections[next];
  active.style.setProperty("--dx", fromRight ? "40px" : "-40px");
  void active.offsetWidth;
  active.classList.add("slide");
  wsLinks.forEach((a, i) => {
    if (i === next) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  wsName.textContent = name;
  document.title = name === "home" ? "milotek" : `milotek · ${name}`;
  currentIndex = next;
  window.scrollTo({ top: 0, behavior: "instant" });
}

window.addEventListener("hashchange", () => showWorkspace(workspaceFromHash()));
showWorkspace(workspaceFromHash());

// Clock. London time on purpose: it is my bar, not the visitor's.
const clock = document.getElementById("clock");
const lockClock = document.getElementById("lock-clock");
const lockDate = document.getElementById("lock-date");
const timeFmt = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", hour: "2-digit", minute: "2-digit" });
const dateFmt = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", weekday: "long", day: "numeric", month: "long" });
function tick() {
  const now = new Date();
  const t = timeFmt.format(now);
  clock.textContent = t;
  clock.dateTime = now.toISOString();
  clock.title = dateFmt.format(now) + ", London";
  lockClock.textContent = t;
  lockDate.textContent = dateFmt.format(now);
}
tick();
setInterval(tick, 10000);

// Splash text, in the Minecraft sense.
const SPLASHES = [
  "no lake, no play",
  "de_dust2 in mat_fullbright",
  "gaps_in 8, gaps_out 16",
  "now with 100% fewer marquees",
  "the vault is mostly private, sorry",
  "ask me about surf physics",
  "yes the wallpaper is tf2",
  "master layout, mfact 0.5",
  "rebuilds from a flake, unlike me",
  "built on a thinkpad, probably",
  "=^)",
];
const splash = document.getElementById("splash");
let splashIndex = Math.floor(Math.random() * SPLASHES.length);
splash.textContent = SPLASHES[splashIndex];
splash.addEventListener("click", () => {
  splashIndex = (splashIndex + 1) % SPLASHES.length;
  splash.textContent = SPLASHES[splashIndex];
});

// Recently pushed repos, straight from GitHub's API. Unauthenticated, so a
// busy visitor can hit the rate limit; the fallback copy covers that. The
// events feed would be closer to a real git log, but it stopped carrying
// commit messages, so this is the honest version.
const gitlog = document.getElementById("gitlog");
function timeAgo(iso) {
  const s = Math.max(1, Math.round((Date.now() - new Date(iso)) / 1000));
  const units = [["y", 31536000], ["mo", 2592000], ["d", 86400], ["h", 3600], ["m", 60]];
  for (const [label, size] of units) if (s >= size) return Math.floor(s / size) + label;
  return s + "s";
}
async function loadGitLog() {
  try {
    const res = await fetch("https://api.github.com/users/milotek/repos?sort=pushed&per_page=7", {
      headers: { Accept: "application/vnd.github+json" },
    });
    if (!res.ok) throw new Error(res.status);
    const repos = (await res.json()).filter((r) => !r.fork);
    if (repos.length === 0) throw new Error("no repos");
    gitlog.replaceChildren(
      ...repos.map((r) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = r.html_url;
        a.className = "sha";
        a.textContent = r.name;
        const msg = document.createElement("span");
        msg.className = "msg";
        msg.textContent = (r.description || "no description, sorry") + " ";
        const lang = document.createElement("span");
        lang.className = "repo";
        lang.textContent = r.language ? r.language.toLowerCase() : "";
        const when = document.createElement("span");
        when.className = "when";
        when.textContent = " " + timeAgo(r.pushed_at);
        msg.append(lang, when);
        li.append(a, msg);
        return li;
      }),
    );
  } catch {
    gitlog.innerHTML = '<li><span class="sha">fatal:</span><span class="msg muted">github said no (rate limit, probably). <a href="https://github.com/milotek">see the real thing</a></span></li>';
  }
}
loadGitLog();

// Lightbox for the art workspace.
const lightbox = document.getElementById("lightbox");
const lbImg = document.getElementById("lb-img");
const lbCaption = document.getElementById("lb-caption");
const lbFile = document.getElementById("lb-file");
const artLinks = [...document.querySelectorAll("#gallery a")];
let artIndex = 0;
function openArt(i) {
  artIndex = (i + artLinks.length) % artLinks.length;
  const a = artLinks[artIndex];
  lbImg.src = a.href;
  lbImg.alt = a.querySelector("img").alt;
  lbCaption.textContent = a.dataset.caption;
  lbFile.textContent = `${a.href.split("/").pop()} [${artIndex + 1}/${artLinks.length}]`;
  if (!lightbox.open) lightbox.showModal();
}
artLinks.forEach((a, i) => a.addEventListener("click", (e) => { e.preventDefault(); openArt(i); }));
document.getElementById("lb-prev").addEventListener("click", () => openArt(artIndex - 1));
document.getElementById("lb-next").addEventListener("click", () => openArt(artIndex + 1));
document.getElementById("lb-close").addEventListener("click", () => lightbox.close());
lightbox.addEventListener("click", (e) => { if (e.target === lightbox) lightbox.close(); });

// hyprlock, minus the security.
const lock = document.getElementById("lock");
const lockInput = document.getElementById("lock-input");
document.getElementById("lock-btn").addEventListener("click", () => {
  lock.hidden = false;
  lockInput.textContent = " ";
  tick();
});
function unlock() { lock.hidden = true; }
lock.addEventListener("click", unlock);

document.addEventListener("keydown", (e) => {
  if (!lock.hidden) {
    if (e.key.length === 1) {
      lockInput.textContent += "•";
      if (lockInput.textContent.length > 6) setTimeout(unlock, 150);
    } else if (e.key === "Enter" || e.key === "Escape") unlock();
    return;
  }
  if (lightbox.open) {
    if (e.key === "ArrowLeft") openArt(artIndex - 1);
    if (e.key === "ArrowRight") openArt(artIndex + 1);
    return;
  }
  if (e.altKey || e.ctrlKey || e.metaKey || e.target.closest("input, textarea")) return;
  const n = Number(e.key);
  if (n >= 1 && n <= WORKSPACES.length) location.hash = "#" + WORKSPACES[n - 1];
});
