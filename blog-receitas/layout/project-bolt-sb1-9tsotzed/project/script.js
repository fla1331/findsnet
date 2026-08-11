// ============ Header scroll state ============
(function () {
  var header = document.getElementById('siteHeader');
  if (!header) return;
  var onScroll = function () {
    if (window.scrollY > 8) header.classList.add('is-scrolled');
    else header.classList.remove('is-scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

// ============ Mobile nav toggle ============
(function () {
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  nav.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      nav.classList.remove('is-open');
      toggle.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

// ============ Active nav by category query param ============
(function () {
  var params = new URLSearchParams(window.location.search);
  var cat = params.get('cat');
  if (!cat) return;
  document.querySelectorAll('.nav-link').forEach(function (link) {
    var href = link.getAttribute('href') || '';
    var match = href.match(/[?&]cat=([^&]+)/);
    if (match && decodeURIComponent(match[1]) === cat) {
      link.classList.add('is-active');
    } else {
      link.classList.remove('is-active');
    }
  });

  // Update category page title/description if present
  var titles = {
    receitas: { title: 'Receitas Saudáveis', desc: 'Pratos que unem sabor e cuidado — para comer bem em qualquer refeição.' },
    nutricao: { title: 'Nutrição', desc: 'Ciência e prática para comer com inteligência e equilíbrio.' },
    longevidade: { title: 'Longevidade', desc: 'Hábitos que adicionam anos à vida e vida aos anos.' },
    'bem-estar': { title: 'Bem-Estar', desc: 'Cuidado, saúde e equilíbrio para o corpo e a mente.' }
  };
  var info = titles[cat];
  if (info) {
    var t = document.getElementById('categoryTitle');
    var d = document.getElementById('categoryDesc');
    if (t) t.textContent = info.title;
    if (d) d.textContent = info.desc;
    document.title = info.title + ' — Saúde & Longevidade';
  }
})();

// ============ Newsletter forms ============
(function () {
  var ids = ['newsletterFormHome', 'newsletterFormArticle'];
  ids.forEach(function (id) {
    var form = document.getElementById(id);
    if (!form) return;
    var success = document.getElementById(id.replace('Form', 'Success'));
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.email.value) return;
      form.hidden = true;
      if (success) success.hidden = false;
    });
  });
})();

// ============ Year in footer ============
(function () {
  var el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();
