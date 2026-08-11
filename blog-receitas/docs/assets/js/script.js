// ===== Mobile Menu Toggle =====
(function initMenu() {
  const toggle = document.getElementById('menuToggle');
  const nav = document.getElementById('nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

// ===== Header shadow on scroll =====
(function initHeaderScroll() {
  const header = document.getElementById('header');
  if (!header) return;
  const onScroll = () => {
    if (window.scrollY > 8) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

// ===== Reveal on scroll (IntersectionObserver) =====
(function initReveal() {
  const items = document.querySelectorAll('.reveal');
  if (!items.length) return;
  if (!('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('visible'));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );
  items.forEach((el) => observer.observe(el));
})();

// ===== Animated counters =====
(function initCounters() {
  const nums = document.querySelectorAll('[data-count]');
  if (!nums.length) return;

  const animate = (el) => {
    const target = parseInt(el.dataset.count, 10) || 0;
    const duration = 1400;
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target).toString();
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toString();
    };
    requestAnimationFrame(step);
  };

  if (!('IntersectionObserver' in window)) {
    nums.forEach(animate);
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );
  nums.forEach((el) => observer.observe(el));
})();

// ===== Newsletter / CTA / Contact forms (demo, no backend) =====
(function initForms() {
  const handlers = [
    { form: 'newsletterForm', msg: 'Inscrição realizada! Verifique seu e-mail.' },
    { form: 'ctaForm', msg: 'Pronto! Você foi inscrito na newsletter.' },
    { form: 'contactForm', msg: 'Mensagem enviada! Responderemos em até 2 dias úteis.' },
  ];
  handlers.forEach(({ form, msg }) => {
    const el = document.getElementById(form);
    if (!el) return;
    el.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = el.querySelector('button[type="submit"]');
      const original = btn ? btn.textContent : '';
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Enviando…';
      }
      setTimeout(() => {
        el.reset();
        if (btn) {
          btn.textContent = msg;
          btn.style.background = 'var(--emerald)';
          btn.style.color = 'var(--white)';
          setTimeout(() => {
            btn.textContent = original;
            btn.disabled = false;
            btn.style.background = '';
            btn.style.color = '';
          }, 2600);
        }
      }, 700);
    });
  });
})();

// ===== Highlight active category from query string =====
(function highlightActiveCategory() {
  const params = new URLSearchParams(window.location.search);
  const cat = params.get('cat');
  if (!cat) return;
  document.querySelectorAll('.nav__link').forEach((link) => {
    const url = link.getAttribute('href') || '';
    if (url.includes('cat=' + cat)) link.classList.add('active');
    else if (!url.startsWith('/categoria.html')) link.classList.remove('active');
  });
})();
