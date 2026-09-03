// Three small things: the avatar pat counter, the art lightbox, and the tab
// title sulking when you leave. Everything else on the site is plain HTML.
(() => {
  const avatar = document.querySelector(".avatar");
  if (avatar) {
    const label = avatar.querySelector(".pats");
    const milestones = [
      [1, "pats: 1. hi."],
      [10, "pats: 10. ok"],
      [25, "pats: 25. you can stop"],
      [50, "pats: 50. you did not stop"],
      [100, "pats: 100 >:3"],
      [250, "pats: 250. seek help"],
      [500, "pats: 500. respect."],
      [1000, "pats: 1000. touch grass, lovingly"],
    ];
    let pats = 0;
    try {
      pats = Number(localStorage.getItem("pats")) || 0;
    } catch {}
    const render = () => {
      label.textContent = pats ? `pats: ${pats}` : "pat me";
    };
    render();
    avatar.addEventListener("click", () => {
      pats += 1;
      try {
        localStorage.setItem("pats", String(pats));
      } catch {}
      render();
      const hit = milestones.find(([n]) => n === pats);
      if (hit) label.textContent = hit[1];
      label.classList.add("show");
      avatar.classList.remove("patted");
      void avatar.offsetWidth;
      avatar.classList.add("patted");
      const heart = document.createElement("span");
      heart.className = "float";
      heart.textContent = "";
      heart.style.left = `${35 + Math.random() * 30}%`;
      avatar.appendChild(heart);
      heart.addEventListener("animationend", () => heart.remove());
    });
  }

  const lightbox = document.querySelector("dialog.lightbox");
  if (lightbox) {
    const img = lightbox.querySelector("img");
    const caption = lightbox.querySelector("figcaption span");
    for (const link of document.querySelectorAll(".gallery a")) {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        img.src = link.href;
        img.alt = link.dataset.alt || "";
        caption.textContent = link.dataset.caption || "";
        lightbox.showModal();
      });
    }
    lightbox.querySelector("button").addEventListener("click", () => lightbox.close());
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) lightbox.close();
    });
    lightbox.addEventListener("close", () => img.removeAttribute("src"));
  }

  const title = document.title;
  document.addEventListener("visibilitychange", () => {
    document.title = document.hidden ? "come back :(" : title;
  });
})();
