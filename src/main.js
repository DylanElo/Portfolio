
document.addEventListener('DOMContentLoaded', () => {
    // Add a clear entry point to the first professional case study.
    const firstCaseStudy = document.querySelector('#projects .project-item');
    if (firstCaseStudy && !firstCaseStudy.querySelector('[data-case-study-link]')) {
        const actions = document.createElement('div');
        actions.className = 'btn-row';
        actions.style.marginTop = '1.25rem';

        const link = document.createElement('a');
        link.href = 'case-studies/hotel-connectivity-onboarding.html';
        link.className = 'btn btn-primary';
        link.dataset.caseStudyLink = 'hotel-connectivity-onboarding';
        link.textContent = 'Read full case study';

        actions.appendChild(link);
        firstCaseStudy.appendChild(actions);
    }

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const links = document.querySelectorAll('.nav-links a');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');

            // Animate hamburger icon
            const spans = mobileMenuBtn.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    // Close mobile menu when clicking a link
    if (links) {
        links.forEach(link => {
            link.addEventListener('click', () => {
                if (!navLinks || !mobileMenuBtn) return;
                navLinks.classList.remove('active');
                const spans = mobileMenuBtn.querySelectorAll('span');
                if (spans.length === 3) {
                    spans[0].style.transform = 'none';
                    spans[1].style.opacity = '1';
                    spans[2].style.transform = 'none';
                }
            });
        });
    }

    // Intersection Observer for Fade-in Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => observer.observe(el));

    // Theme Toggle
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            themeToggle.textContent = 'Light';
        }

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            themeToggle.textContent = isDark ? 'Light' : 'Dark';
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }

    // Smooth Scrolling for Anchor Links (only for same-page anchors)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});
