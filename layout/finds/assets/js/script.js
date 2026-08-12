/* =====================================================
   FINDS BLOG - SCRIPT.JS
   Interactivity: theme toggle, mobile menu, language
   selector, cookie banner, reveal animations, contact
   form. Progressive enhancement — site works without JS.
   ===================================================== */

(function () {
  'use strict';

  /* ---------- 1. Theme Toggle ---------- */
  const THEME_KEY = 'finds-blog-theme';

  function getStoredTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }
  function storeTheme(theme) {
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
  }
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
  }

  // Apply early to avoid flash (inline script in head handles this too)
  const savedTheme = getStoredTheme();
  if (savedTheme) {
    applyTheme(savedTheme);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.querySelector('.theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        storeTheme(next);
      });
    }

    /* ---------- 2. Mobile Menu ---------- */
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    if (menuToggle && mainNav) {
      menuToggle.addEventListener('click', function () {
        menuToggle.classList.toggle('open');
        mainNav.classList.toggle('open');
        const expanded = menuToggle.classList.contains('open');
        menuToggle.setAttribute('aria-expanded', expanded);
      });
      // Close on nav link click (mobile)
      mainNav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          menuToggle.classList.remove('open');
          mainNav.classList.remove('open');
          menuToggle.setAttribute('aria-expanded', 'false');
        });
      });
    }

    /* ---------- 3. Language Selector ---------- */
    const langBtn = document.querySelector('.lang-btn');
    const langDropdown = document.querySelector('.lang-dropdown');
    if (langBtn && langDropdown) {
      langBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        langDropdown.classList.toggle('open');
        const expanded = langDropdown.classList.contains('open');
        langBtn.setAttribute('aria-expanded', expanded);
      });
      document.addEventListener('click', function () {
        langDropdown.classList.remove('open');
        langBtn.setAttribute('aria-expanded', 'false');
      });
      langDropdown.addEventListener('click', function (e) { e.stopPropagation(); });
    }

    /* ---------- 4. Cookie Banner ---------- */
    const COOKIE_KEY = 'finds-blog-cookie-consent';
    const banner = document.querySelector('.cookie-banner');

    function getCookieConsent() {
      try { return localStorage.getItem(COOKIE_KEY); } catch (e) { return null; }
    }
    function setCookieConsent(value) {
      try { localStorage.setItem(COOKIE_KEY, value); } catch (e) {}
    }

    if (banner) {
      const consent = getCookieConsent();
      if (!consent) {
        setTimeout(function () { banner.classList.add('show'); }, 800);
      }
      const acceptBtn = banner.querySelector('.cookie-accept');
      const rejectBtn = banner.querySelector('.cookie-reject');
      const customizeBtn = banner.querySelector('.cookie-customize');

      if (acceptBtn) {
        acceptBtn.addEventListener('click', function () {
          setCookieConsent('accepted');
          banner.classList.remove('show');
        });
      }
      if (rejectBtn) {
        rejectBtn.addEventListener('click', function () {
          setCookieConsent('rejected');
          banner.classList.remove('show');
        });
      }
      if (customizeBtn) {
        customizeBtn.addEventListener('click', function () {
          window.location.href = 'cookies.html';
        });
      }
    }

    /* ---------- 5. Reveal on Scroll ---------- */
    const reveals = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window && reveals.length > 0) {
      const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
      reveals.forEach(function (el) { observer.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add('visible'); });
    }

    /* ---------- 6. Contact Form ---------- */
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
      contactForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const feedback = document.querySelector('#form-feedback');
        const name = contactForm.querySelector('#name').value.trim();
        const email = contactForm.querySelector('#email').value.trim();
        const message = contactForm.querySelector('#message').value.trim();

        if (!name || !email || !message) {
          if (feedback) {
            feedback.className = 'form-feedback show';
            feedback.style.background = 'rgba(220, 38, 38, 0.1)';
            feedback.style.color = '#DC2626';
            feedback.style.border = '1px solid #DC2626';
            feedback.textContent = 'Por favor, preencha todos os campos obrigatórios.';
          }
          return;
        }
        // Simulate submission (replace with real endpoint)
        if (feedback) {
          feedback.className = 'form-feedback show success';
          feedback.textContent = 'Mensagem enviada com sucesso! Entraremos em contato em breve.';
        }
        contactForm.reset();
      });
    }

    /* ---------- 7. Share Buttons ---------- */
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const url = btn.getAttribute('data-url') || window.location.href;
        const title = btn.getAttribute('data-title') || document.title;
        const type = btn.getAttribute('data-share');
        let shareUrl = '';
        if (type === 'whatsapp') {
          shareUrl = 'https://wa.me/?text=' + encodeURIComponent(title + ' ' + url);
        } else if (type === 'facebook') {
          shareUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url);
        } else if (type === 'twitter') {
          shareUrl = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url);
        } else if (type === 'linkedin') {
          shareUrl = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url);
        }
        if (shareUrl) {
          window.open(shareUrl, '_blank', 'noopener,noreferrer,width=600,height=500');
        }
      });
    });

    /* ---------- 8. 404 Search ---------- */
    const errorSearch = document.querySelector('.error-search');
    if (errorSearch) {
      errorSearch.addEventListener('submit', function (e) {
        e.preventDefault();
        const query = errorSearch.querySelector('input').value.trim();
        if (query) {
          window.location.href = 'index.html?q=' + encodeURIComponent(query);
        }
      });
    }

    /* ---------- 9. Header shadow on scroll ---------- */
    const header = document.querySelector('.site-header');
    if (header) {
      let lastScroll = 0;
      window.addEventListener('scroll', function () {
        const scroll = window.pageYOffset;
        if (scroll > 10) {
          header.style.boxShadow = 'var(--shadow)';
        } else {
          header.style.boxShadow = 'var(--shadow-sm)';
        }
        lastScroll = scroll;
      }, { passive: true });
    }
  });
})();
