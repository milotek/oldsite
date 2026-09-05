// Lightbox for the gallery and project screenshots. Without JS the links still
// open the full image directly, which is the whole point of using <a href>.
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('a.lightbox'));
  if (!links.length) return;

  var box = document.createElement('div');
  box.className = 'lb';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Image viewer');
  box.innerHTML =
    '<button class="lb-close" type="button" aria-label="Close">&times;</button>' +
    '<button class="lb-nav lb-prev" type="button" aria-label="Previous">&larr;</button>' +
    '<button class="lb-nav lb-next" type="button" aria-label="Next">&rarr;</button>' +
    '<img alt=""><p class="lb-cap"></p>';
  document.body.appendChild(box);

  var img = box.querySelector('img');
  var cap = box.querySelector('.lb-cap');
  var index = 0;
  var opener = null;

  function show(i) {
    index = (i + links.length) % links.length;
    var link = links[index];
    var caption = link.getAttribute('data-caption') || '';
    img.src = link.getAttribute('href');
    img.alt = caption;
    cap.textContent = caption;
  }

  function open(i, from) {
    opener = from;
    show(i);
    box.classList.add('on');
    document.body.style.overflow = 'hidden';
    box.querySelector('.lb-close').focus();
  }

  function close() {
    box.classList.remove('on');
    document.body.style.overflow = '';
    img.src = '';
    if (opener) opener.focus();
  }

  links.forEach(function (link, i) {
    link.addEventListener('click', function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return;
      ev.preventDefault();
      open(i, link);
    });
  });

  box.querySelector('.lb-close').addEventListener('click', close);
  box.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
  box.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
  box.addEventListener('click', function (ev) {
    if (ev.target === box || ev.target === img) close();
  });
  document.addEventListener('keydown', function (ev) {
    if (!box.classList.contains('on')) return;
    if (ev.key === 'Escape') close();
    if (ev.key === 'ArrowLeft') show(index - 1);
    if (ev.key === 'ArrowRight') show(index + 1);
  });
})();
