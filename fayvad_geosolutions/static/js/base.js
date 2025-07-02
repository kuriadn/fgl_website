// Fayvad Geosolutions - Base JavaScript
// File: static/js/base.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initNavigation();
    initScrollEffects();
    initAnimations();
    initForms();
    initModals();
    initTabs();
    initAccordions();
    
    // Navigation functionality
    function initNavigation() {
        const header = document.querySelector('.main-header');
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const navMenu = document.querySelector('.navbar-nav');
        const navLinks = document.querySelectorAll('.nav-link');
        
        // Mobile menu toggle
        if (mobileToggle && navMenu) {
            mobileToggle.addEventListener('click', function() {
                navMenu.classList.toggle('show');
            });
            
            // Close mobile menu when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.navbar') && navMenu.classList.contains('show')) {
                    navMenu.classList.remove('show');
                }
            });
        }
        
        // Header scroll effect
        if (header) {
            window.addEventListener('scroll', function() {
                if (window.scrollY > 100) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            });
        }
        
        // Active navigation link
        function setActiveNavLink() {
            const currentPath = window.location.pathname;
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                const href = link.getAttribute('href');
                
                if (href === currentPath || 
                    (currentPath === '/' && href === '/') ||
                    (currentPath.startsWith(href) && href !== '/')) {
                    link.classList.add('active');
                }
            });
        }
        
        setActiveNavLink();
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const headerHeight = header ? header.offsetHeight : 0;
                    const targetPosition = target.offsetTop - headerHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // Scroll effects and animations
    function initScrollEffects() {
        // Intersection Observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, observerOptions);
        
        // Observe elements with animation classes
        document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right').forEach(el => {
            observer.observe(el);
        });
        
        // Counter animation for statistics
        const counters = document.querySelectorAll('.stat-number');
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
    
    // Counter animation
    function animateCounter(element) {
        const target = parseInt(element.textContent.replace(/\D/g, ''));
        const suffix = element.textContent.replace(/[\d,]/g, '');
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                element.textContent = target.toLocaleString() + suffix;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString() + suffix;
            }
        }, 16);
    }
    
    // Initialize animations
    function initAnimations() {
        // Add entrance animations to cards
        const cards = document.querySelectorAll('.service-card, .team-card, .project-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('fade-in');
        });
        
        // Parallax effect for hero sections
        const heroSections = document.querySelectorAll('.hero');
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            heroSections.forEach(hero => {
                const rate = scrolled * -0.5;
                hero.style.transform = `translateY(${rate}px)`;
            });
        });
    }
    
    // Form handling
    function initForms() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!validateForm(form)) {
                    e.preventDefault();
                }
            });
            
            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    validateField(input);
                });
                
                input.addEventListener('input', function() {
                    if (input.classList.contains('is-invalid')) {
                        validateField(input);
                    }
                });
            });
        });
        
        // Newsletter form AJAX submission
        const newsletterForm = document.querySelector('#newsletter-form');
        if (newsletterForm) {
            newsletterForm.addEventListener('submit', function(e) {
                e.preventDefault();
                submitNewsletterForm(this);
            });
        
        
        // Contact form AJAX submission
        const contactForm = document.querySelector('#contact-form');
        if (contactForm) {
            contactForm.addEventListener('submit', function(e) {
                e.preventDefault();
                submitContactForm(this);
            });
        }
    }
    
    // Form validation
    function validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required.';
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid email address.';
            }
        }
        
        // Phone validation
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[\+]?[\d\s\-\(\)]+$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid phone number.';
            }
        }
        
        // Update field state
        if (isValid) {
            field.classList.remove('is-invalid');
            hideFieldError(field);
        } else {
            field.classList.add('is-invalid');
            showFieldError(field, message);
        }
        
        return isValid;
    }
    
    function showFieldError(field, message) {
        let errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            field.parentNode.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }
    
    function hideFieldError(field) {
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    }
    
    // AJAX form submissions
    function submitNewsletterForm(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.textContent = 'Subscribing...';
        submitBtn.disabled = true;
        
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Thank you for subscribing to our newsletter!', 'success');
                form.reset();
            } else {
                showNotification(data.message || 'An error occurred. Please try again.', 'error');
            }
        })
        .catch(error => {
            showNotification('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    }
    
    function submitContactForm(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Thank you for your message! We\'ll get back to you soon.', 'success');
                form.reset();
            } else {
                showNotification(data.message || 'An error occurred. Please try again.', 'error');
            }
        })
        .catch(error => {
            showNotification('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
    }
    
    // Modal functionality
    function initModals() {
        const modalTriggers = document.querySelectorAll('[data-modal]');
        const modals = document.querySelectorAll('.modal-overlay');
        const modalCloses = document.querySelectorAll('.modal-close');
        
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                const modalId = this.getAttribute('data-modal');
                const modal = document.getElementById(modalId);
                if (modal) {
                    openModal(modal);
                }
            });
        });
        
        modalCloses.forEach(close => {
            close.addEventListener('click', function() {
                const modal = this.closest('.modal-overlay');
                if (modal) {
                    closeModal(modal);
                }
            });
        });
        
        modals.forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    closeModal(this);
                }
            });
        });
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const activeModal = document.querySelector('.modal-overlay.active');
                if (activeModal) {
                    closeModal(activeModal);
                }
            }
        });
    }
    
    function openModal(modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function closeModal(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    // Tabs functionality
    function initTabs() {
        const tabContainers = document.querySelectorAll('.tabs-container');
        
        tabContainers.forEach(container => {
            const tabButtons = container.querySelectorAll('.tab-button');
            const tabContents = container.querySelectorAll('.tab-content');
            
            tabButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const target = this.getAttribute('data-tab');
                    
                    // Remove active states
                    tabButtons.forEach(btn => btn.classList.remove('active'));
                    tabContents.forEach(content => content.classList.remove('active'));
                    
                    // Add active states
                    this.classList.add('active');
                    const targetContent = container.querySelector(`#${target}`);
                    if (targetContent) {
                        targetContent.classList.add('active');
                    }
                });
            });
        });
    }
    
    // Accordion functionality
    function initAccordions() {
        const accordions = document.querySelectorAll('.accordion');
        
        accordions.forEach(accordion => {
            const headers = accordion.querySelectorAll('.accordion-header');
            
            headers.forEach(header => {
                header.addEventListener('click', function() {
                    const item = this.parentNode;
                    const content = item.querySelector('.accordion-content');
                    const isActive = this.classList.contains('active');
                    
                    // Close all items in this accordion
                    headers.forEach(h => {
                        h.classList.remove('active');
                        h.parentNode.querySelector('.accordion-content').classList.remove('active');
                    });
                    
                    // Open clicked item if it wasn't active
                    if (!isActive) {
                        this.classList.add('active');
                        content.classList.add('active');
                    }
                });
            });
        });
    }
    
    // Utility functions
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Add styles if not already added
        if (!document.querySelector('#notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    max-width: 400px;
                    padding: 1rem;
                    border-radius: 5px;
                    color: white;
                    z-index: 10000;
                    animation: slideInRight 0.3s ease;
                }
                .notification-success {
                    background: #28a745;
                }
                .notification-error {
                    background: #dc3545;
                }
                .notification-info {
                    background: #17a2b8;
                }
                .notification-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .notification-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.2rem;
                    cursor: pointer;
                    margin-left: 1rem;
                }
                @keyframes slideInRight {
                    from { transform: translateX(100%); }
                    to { transform: translateX(0); }
                }
            `;
            document.head.appendChild(styles);
        }
        
        document.body.appendChild(notification);
        
        // Close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', function() {
            removeNotification(notification);
        });
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                removeNotification(notification);
            }
        }, 5000);
    }
    
    function removeNotification(notification) {
        notification.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
    
    // Search functionality
    function initSearch() {
        const searchForms = document.querySelectorAll('.search-form');
        
        searchForms.forEach(form => {
            const input = form.querySelector('input[type="search"]');
            const resultsContainer = form.querySelector('.search-results');
            
            if (input && resultsContainer) {
                const debouncedSearch = debounce(function(query) {
                    if (query.length >= 3) {
                        performSearch(query, resultsContainer);
                    } else {
                        resultsContainer.innerHTML = '';
                        resultsContainer.style.display = 'none';
                    }
                }, 300);
                
                input.addEventListener('input', function() {
                    debouncedSearch(this.value.trim());
                });
                
                // Hide results when clicking outside
                document.addEventListener('click', function(e) {
                    if (!form.contains(e.target)) {
                        resultsContainer.style.display = 'none';
                    }
                });
            }
        });
    }
    
    function performSearch(query, container) {
        fetch(`/search/?q=${encodeURIComponent(query)}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                container.innerHTML = data.results.map(result => `
                    <div class="search-result-item">
                        <h4><a href="${result.url}">${result.title}</a></h4>
                        <p>${result.excerpt}</p>
                    </div>
                `).join('');
                container.style.display = 'block';
            } else {
                container.innerHTML = '<div class="search-no-results">No results found</div>';
                container.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            container.innerHTML = '<div class="search-error">Search temporarily unavailable</div>';
            container.style.display = 'block';
        });
    }
    
    // Lazy loading for images
    function initLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Back to top button
    function initBackToTop() {
        const backToTopBtn = document.createElement('button');
        backToTopBtn.className = 'back-to-top';
        backToTopBtn.innerHTML = '↑';
        backToTopBtn.setAttribute('aria-label', 'Back to top');
        
        // Add styles
        const styles = `
            .back-to-top {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 50px;
                height: 50px;
                background: #1e3c72;
                color: white;
                border: none;
                border-radius: 50%;
                font-size: 1.2rem;
                cursor: pointer;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
                z-index: 1000;
            }
            .back-to-top.visible {
                opacity: 1;
                visibility: visible;
            }
            .back-to-top:hover {
                background: #ffd700;
                color: #1e3c72;
                transform: translateY(-2px);
            }
        `;
        
        if (!document.querySelector('#back-to-top-styles')) {
            const styleElement = document.createElement('style');
            styleElement.id = 'back-to-top-styles';
            styleElement.textContent = styles;
            document.head.appendChild(styleElement);
        }
        
        document.body.appendChild(backToTopBtn);
        
        // Show/hide based on scroll position
        const toggleBackToTop = throttle(function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        }, 100);
        
        window.addEventListener('scroll', toggleBackToTop);
        
        // Scroll to top functionality
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Initialize additional features
    initSearch();
    initLazyLoading();
    initBackToTop();
    
    // Service worker registration (if available)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/sw.js')
                .then(function(registration) {
                    console.log('ServiceWorker registration successful');
                })
                .catch(function(err) {
                    console.log('ServiceWorker registration failed');
                });
        });
    }
    
    // Performance monitoring
    if (window.performance && window.performance.timing) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const timing = window.performance.timing;
                const loadTime = timing.loadEventEnd - timing.navigationStart;
                
                if (loadTime > 3000) {
                    console.warn('Page load time is high:', loadTime + 'ms');
                }
            }, 0);
        });
    }
});

// Global utility functions
window.FayvaGeosolutions = {
    showNotification: function(message, type) {
        // Re-expose notification function globally if needed
        const event = new CustomEvent('showNotification', {
            detail: { message, type }
        });
        document.dispatchEvent(event);
    },
    
    scrollToElement: function(selector, offset = 0) {
        const element = document.querySelector(selector);
        if (element) {
            const headerHeight = document.querySelector('.main-header')?.offsetHeight || 0;
            const targetPosition = element.offsetTop - headerHeight - offset;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }
};