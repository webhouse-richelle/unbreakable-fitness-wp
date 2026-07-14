
class Component extends DCLogic {
  state = { mobileOpen: false };
  toggleMenu = () => this.setState(s => ({ mobileOpen: !s.mobileOpen }));
  closeMenu = () => this.setState({ mobileOpen: false });
  onSubscribe = (e) => {
    e.preventDefault();
    const inp = e.target.querySelector('input');
    const btn = e.target.querySelector('button');
    if (btn) { btn.textContent = "You're in ✓"; }
    if (inp) { inp.value = ''; inp.blur(); }
  };

  componentDidMount() {
    const nav = document.querySelector('[data-nav]');
    const bar = document.querySelector('[data-progress]');
    this._onScroll = () => {
      const y = window.scrollY || window.pageYOffset;
      if (nav) {
        if (y > 40) {
          nav.style.background = '#000';
          nav.style.borderBottom = '1px solid #1a1a1a';
          nav.style.boxShadow = '0 8px 30px rgba(0,0,0,.5)';
        } else {
          nav.style.background = 'transparent';
          nav.style.borderBottom = '1px solid transparent';
          nav.style.boxShadow = 'none';
        }
      }
      if (bar) {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
      }
    };
    window.addEventListener('scroll', this._onScroll, { passive: true });
    this._onScroll();

    // Reveals
    const rv = Array.prototype.slice.call(document.querySelectorAll('[data-rv]'));
    rv.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(32px)';
      el.style.transitionProperty = 'opacity, transform';
      el.style.transitionDuration = '.85s';
      el.style.transitionTimingFunction = 'cubic-bezier(.16,1,.3,1)';
      el.style.transitionDelay = (parseInt(el.dataset.d || '0', 10)) + 'ms';
      el.style.willChange = 'opacity, transform';
    });
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (en.isIntersecting) {
            en.target.style.opacity = '1';
            en.target.style.transform = 'none';
            io.unobserve(en.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      rv.forEach(el => io.observe(el));
      this._io = io;
    } else {
      rv.forEach(el => { el.style.opacity = '1'; el.style.transform = 'none'; });
    }
    this._revealFallback = setTimeout(() => {
      rv.forEach(el => { el.style.opacity = '1'; el.style.transform = 'none'; });
    }, 3500);

    // Counters
    const counters = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
    if ('IntersectionObserver' in window) {
      const co = new IntersectionObserver((entries) => {
        entries.forEach(en => {
          if (!en.isIntersecting) return;
          const el = en.target;
          const target = parseFloat(el.dataset.count);
          const suffix = el.dataset.suffix || '';
          const decimals = (String(el.dataset.count).indexOf('.') > -1) ? 1 : 0;
          const dur = 1500;
          const start = performance.now();
          const step = (t) => {
            const p = Math.min((t - start) / dur, 1);
            const ease = 1 - Math.pow(1 - p, 3);
            const val = (target * ease).toFixed(decimals);
            el.textContent = val + suffix;
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = target.toFixed(decimals) + suffix;
          };
          requestAnimationFrame(step);
          co.unobserve(el);
        });
      }, { threshold: 0.6 });
      counters.forEach(el => co.observe(el));
      this._co = co;
    }

    // Hero mouse parallax
    const hero = document.querySelector('[data-hero]');
    if (hero) {
      this._hero = hero;
      this._onMove = (ev) => {
        const r = hero.getBoundingClientRect();
        const cx = (ev.clientX - r.left) / r.width - 0.5;
        const cy = (ev.clientY - r.top) / r.height - 0.5;
        hero.querySelectorAll('[data-px]').forEach(el => {
          const sp = parseFloat(el.dataset.px);
          el.style.transform = 'translate(' + (cx * sp) + 'px,' + (cy * sp) + 'px)';
        });
      };
      hero.addEventListener('mousemove', this._onMove);
    }
  }

  componentWillUnmount() {
    if (this._onScroll) window.removeEventListener('scroll', this._onScroll);
    if (this._io) this._io.disconnect();
    if (this._co) this._co.disconnect();
    if (this._hero && this._onMove) this._hero.removeEventListener('mousemove', this._onMove);
    if (this._revealFallback) clearTimeout(this._revealFallback);
  }

  renderVals() {
    return {
      mobileOpen: this.state.mobileOpen,
      toggleMenu: this.toggleMenu,
      closeMenu: this.closeMenu,
      onSubscribe: this.onSubscribe,
    };
  }
}
</script>


</body></html>"
  