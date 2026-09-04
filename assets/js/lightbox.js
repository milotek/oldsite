/* Art gallery lightbox. The thumbnails link straight to the full image, so
   with JS off clicking one still shows the picture. */
(function () {
  var links = document.querySelectorAll('.art-open');
  if (!links.length) return;
  var box = null;

  function close() {
    if (!box) return;
    box.remove();
    box = null;
    document.removeEventListener('keydown', onKey);
  }

  function onKey(e) { if (e.key === 'Escape') close(); }

  function open(a) {
    close();
    box = document.createElement('div');
    box.className = 'lb';
    box.innerHTML =
      '<span class="lb-x">esc</span><div class="lb-in">' +
      '<img src="' + a.getAttribute('href') + '" alt="' + a.dataset.title + '">' +
      '<p><b>' + a.dataset.title + '</b> &middot; ' + a.dataset.cap + '</p></div>';
    box.addEventListener('click', close);
    document.body.appendChild(box);
    document.addEventListener('keydown', onKey);
  }

  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', function (e) {
      e.preventDefault();
      open(this);
    });
  }
})();
