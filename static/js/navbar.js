/**
 * Navbar Enhancement Script
 * - Scroll effects
 * - Mobile menu toggle
 * - Active link highlighting
 */

document.addEventListener('DOMContentLoaded', function() {
  const header = document.getElementById('header');
  const navmenu = document.getElementById('navmenu');
  const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
  const navLinks = document.querySelectorAll('.navmenu ul li a');

  // ============================================
  // SCROLL EFFECT
  // ============================================
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // ============================================
  // MOBILE MENU TOGGLE
  // ============================================
  if (mobileNavToggle) {
    mobileNavToggle.addEventListener('click', function() {
      navmenu.classList.toggle('active');
      mobileNavToggle.classList.toggle('active');
    });
  }

  // ============================================
  // CLOSE MOBILE MENU ON LINK CLICK
  // ============================================
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      navmenu.classList.remove('active');
      if (mobileNavToggle) {
        mobileNavToggle.classList.remove('active');
      }
    });
  });

  // ============================================
  // ACTIVE LINK HIGHLIGHTING (Fallback)
  // ============================================
  const currentPath = window.location.pathname;
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // ============================================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && document.querySelector(href)) {
        e.preventDefault();
        document.querySelector(href).scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});

/**
 * Scroll-to-Top Button
 */
document.addEventListener('DOMContentLoaded', function() {
  const scrollTop = document.getElementById('scroll-top');

  if (scrollTop) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 300) {
        scrollTop.style.display = 'flex';
        scrollTop.style.opacity = '1';
      } else {
        scrollTop.style.display = 'none';
        scrollTop.style.opacity = '0';
      }
    });

    scrollTop.addEventListener('click', function(e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
});

/**
 * Preloader
 */
window.addEventListener('load', function() {
  const preloader = document.getElementById('preloader');
  if (preloader) {
    preloader.style.display = 'none';
  }
});
