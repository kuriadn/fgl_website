// Fayvad Geosolutions - Utilities JavaScript
// File: static/js/utils.js

/**
 * Utility functions for Fayvad Geosolutions website
 */

// DOM Ready utility
const domReady = (callback) => {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', callback);
    } else {
        callback();
    }
};

// Debounce function
const debounce = (func, wait, immediate = false) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
};

// Throttle function
const throttle = (func, limit) => {
    let inThrottle;
    return function(...args) {
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

// Get CSRF token
const getCSRFToken = () => {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return decodeURIComponent(value);
        }
    }
    return null;
};

// AJAX utility
const ajax = {
    get: (url, options = {}) => {
        return fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            ...options
        });
    },
    
    post: (url, data = {}, options = {}) => {
        const csrfToken = getCSRFToken();
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            body: JSON.stringify(data),
            ...options
        });
    },
    
    postForm: (url, formData, options = {}) => {
        const csrfToken = getCSRFToken();
        return fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            body: formData,
            ...options
        });
    }
};

// Local storage utility
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return false;
        }
    },
    
    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return defaultValue;
        }
    },
    
    remove: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return false;
        }
    },
    
    clear: () => {
        try {
            localStorage.clear();
            return true;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return false;
        }
    }
};

// URL utility
const url = {
    getParams: () => {
        const params = new URLSearchParams(window.location.search);
        const result = {};
        for (const [key, value] of params) {
            result[key] = value;
        }
        return result;
    },
    
    setParam: (key, value) => {
        const url = new URL(window.location);
        url.searchParams.set(key, value);
        window.history.pushState({}, '', url);
    },
    
    removeParam: (key) => {
        const url = new URL(window.location);
        url.searchParams.delete(key);
        window.history.pushState({}, '', url);
    },
    
    buildQuery: (params) => {
        const query = new URLSearchParams();
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                query.append(key, value);
            }
        });
        return query.toString();
    }
};

// Element utility
const element = {
    create: (tag, attributes = {}, content = '') => {
        const el = document.createElement(tag);
        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                el.className = value;
            } else if (key === 'innerHTML') {
                el.innerHTML = value;
            } else {
                el.setAttribute(key, value);
            }
        });
        if (content) {
            el.textContent = content;
        }
        return el;
    },
    
    addClass: (el, className) => {
        if (el && className) {
            el.classList.add(className);
        }
    },
    
    removeClass: (el, className) => {
        if (el && className) {
            el.classList.remove(className);
        }
    },
    
    toggleClass: (el, className) => {
        if (el && className) {
            el.classList.toggle(className);
        }
    },
    
    hasClass: (el, className) => {
        return el && className ? el.classList.contains(className) : false;
    },
    
    show: (el) => {
        if (el) {
            el.style.display = '';
            el.removeAttribute('hidden');
        }
    },
    
    hide: (el) => {
        if (el) {
            el.style.display = 'none';
        }
    },
    
    toggle: (el) => {
        if (el) {
            const isHidden = el.style.display === 'none' || el.hasAttribute('hidden');
            if (isHidden) {
                element.show(el);
            } else {
                element.hide(el);
            }
        }
    },
    
    getOffset: (el) => {
        if (!el) return { top: 0, left: 0 };
        const rect = el.getBoundingClientRect();
        return {
            top: rect.top + window.pageYOffset,
            left: rect.left + window.pageXOffset
        };
    },
    
    isInViewport: (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// Animation utility
const animate = {
    fadeIn: (el, duration = 300) => {
        if (!el) return;
        el.style.opacity = '0';
        el.style.display = 'block';
        
        const start = performance.now();
        const fade = (timestamp) => {
            const progress = (timestamp - start) / duration;
            if (progress < 1) {
                el.style.opacity = progress;
                requestAnimationFrame(fade);
            } else {
                el.style.opacity = '1';
            }
        };
        requestAnimationFrame(fade);
    },
    
    fadeOut: (el, duration = 300) => {
        if (!el) return;
        
        const start = performance.now();
        const initialOpacity = parseFloat(getComputedStyle(el).opacity);
        
        const fade = (timestamp) => {
            const progress = (timestamp - start) / duration;
            if (progress < 1) {
                el.style.opacity = initialOpacity * (1 - progress);
                requestAnimationFrame(fade);
            } else {
                el.style.opacity = '0';
                el.style.display = 'none';
            }
        };
        requestAnimationFrame(fade);
    },
    
    slideDown: (el, duration = 300) => {
        if (!el) return;
        
        el.style.display = 'block';
        const height = el.scrollHeight;
        el.style.height = '0px';
        el.style.overflow = 'hidden';
        
        const start = performance.now();
        const slide = (timestamp) => {
            const progress = (timestamp - start) / duration;
            if (progress < 1) {
                el.style.height = (height * progress) + 'px';
                requestAnimationFrame(slide);
            } else {
                el.style.height = 'auto';
                el.style.overflow = '';
            }
        };
        requestAnimationFrame(slide);
    },
    
    slideUp: (el, duration = 300) => {
        if (!el) return;
        
        const height = el.scrollHeight;
        el.style.height = height + 'px';
        el.style.overflow = 'hidden';
        
        const start = performance.now();
        const slide = (timestamp) => {
            const progress = (timestamp - start) / duration;
            if (progress < 1) {
                el.style.height = (height * (1 - progress)) + 'px';
                requestAnimationFrame(slide);
            } else {
                el.style.height = '0px';
                el.style.display = 'none';
                el.style.overflow = '';
            }
        };
        requestAnimationFrame(slide);
    }
};

// Form validation utility
const validate = {
    email: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    phone: (phone) => {
        const re = /^[\+]?[\d\s\-\(\)]+$/;
        return re.test(phone);
    },
    
    required: (value) => {
        return value && value.trim().length > 0;
    },
    
    minLength: (value, min) => {
        return value && value.length >= min;
    },
    
    maxLength: (value, max) => {
        return value && value.length <= max;
    },
    
    url: (url) => {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }
};

// Date utility
const dateUtils = {
    format: (date, format = 'YYYY-MM-DD') => {
        if (!(date instanceof Date)) {
            date = new Date(date);
        }
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    },
    
    isValid: (date) => {
        return date instanceof Date && !isNaN(date);
    },
    
    addDays: (date, days) => {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    },
    
    diff: (date1, date2, unit = 'days') => {
        const diff = Math.abs(date2 - date1);
        switch (unit) {
            case 'seconds': return Math.floor(diff / 1000);
            case 'minutes': return Math.floor(diff / (1000 * 60));
            case 'hours': return Math.floor(diff / (1000 * 60 * 60));
            case 'days': return Math.floor(diff / (1000 * 60 * 60 * 24));
            default: return diff;
        }
    }
};

// Number utility
const numberUtils = {
    format: (number, decimals = 0, thousands = ',', decimal = '.') => {
        const n = Number(number);
        if (isNaN(n)) return number;
        
        const fixed = n.toFixed(decimals);
        const parts = fixed.split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousands);
        
        return parts.join(decimal);
    },
    
    currency: (amount, currency = 'KES', locale = 'en-KE') => {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    percentage: (value, total, decimals = 1) => {
        if (total === 0) return '0%';
        return ((value / total) * 100).toFixed(decimals) + '%';
    },
    
    clamp: (value, min, max) => {
        return Math.min(Math.max(value, min), max);
    },
    
    random: (min, max) => {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
};

// String utility
const stringUtils = {
    capitalize: (str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    },
    
    titleCase: (str) => {
        return str.replace(/\w\S*/g, (txt) => {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    },
    
    camelCase: (str) => {
        return str.replace(/[-_\s]+(.)?/g, (_, char) => char ? char.toUpperCase() : '');
    },
    
    kebabCase: (str) => {
        return str.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
    },
    
    truncate: (str, length, suffix = '...') => {
        if (str.length <= length) return str;
        return str.substring(0, length) + suffix;
    },
    
    stripHtml: (html) => {
        const doc = new DOMParser().parseFromString(html, 'text/html');
        return doc.body.textContent || '';
    },
    
    escape: (str) => {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
};

// Cookie utility
const cookies = {
    set: (name, value, days = 7, path = '/') => {
        const expires = new Date(Date.now() + days * 864e5).toUTCString();
        document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=${path}`;
    },
    
    get: (name) => {
        return document.cookie.split('; ').reduce((r, v) => {
            const parts = v.split('=');
            return parts[0] === name ? decodeURIComponent(parts[1]) : r;
        }, '');
    },
    
    delete: (name, path = '/') => {
        cookies.set(name, '', -1, path);
    },
    
    exists: (name) => {
        return cookies.get(name) !== '';
    }
};

// Device detection utility
const device = {
    isMobile: () => {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    },
    
    isTablet: () => {
        return /iPad|Android|Silk|Kindle|PlayBook/i.test(navigator.userAgent) && !device.isMobile();
    },
    
    isDesktop: () => {
        return !device.isMobile() && !device.isTablet();
    },
    
    getScreenSize: () => {
        const width = window.innerWidth;
        if (width < 576) return 'xs';
        if (width < 768) return 'sm';
        if (width < 992) return 'md';
        if (width < 1200) return 'lg';
        return 'xl';
    },
    
    hasTouch: () => {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }
};

// Performance utility
const perf = {
    measure: (name, fn) => {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        console.log(`${name}: ${end - start}ms`);
        return result;
    },
    
    debounceResize: (callback, delay = 250) => {
        return debounce(() => {
            callback(window.innerWidth, window.innerHeight);
        }, delay);
    },
    
    throttleScroll: (callback, delay = 16) => {
        return throttle((e) => {
            callback(window.pageYOffset, e);
        }, delay);
    },
    
    preloadImage: (src) => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = src;
        });
    },
    
    preloadImages: (srcs) => {
        return Promise.all(srcs.map(src => perf.preloadImage(src)));
    }
};

// Notification utility
const notify = {
    show: (message, type = 'info', duration = 5000) => {
        const notification = element.create('div', {
            className: `notification notification-${type}`,
            innerHTML: `
                <div class="notification-content">
                    <span class="notification-message">${stringUtils.escape(message)}</span>
                    <button class="notification-close" aria-label="Close">&times;</button>
                </div>
            `
        });
        
        document.body.appendChild(notification);
        
        // Close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => notify.remove(notification));
        
        // Auto remove
        if (duration > 0) {
            setTimeout(() => notify.remove(notification), duration);
        }
        
        // Animate in
        requestAnimationFrame(() => {
            notification.classList.add('show');
        });
        
        return notification;
    },
    
    remove: (notification) => {
        notification.classList.add('hide');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    },
    
    success: (message, duration) => notify.show(message, 'success', duration),
    error: (message, duration) => notify.show(message, 'error', duration),
    warning: (message, duration) => notify.show(message, 'warning', duration),
    info: (message, duration) => notify.show(message, 'info', duration)
};

// Loading utility
const loading = {
    show: (target = document.body, message = 'Loading...') => {
        const loader = element.create('div', {
            className: 'loading-overlay',
            innerHTML: `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                    <div class="loading-message">${stringUtils.escape(message)}</div>
                </div>
            `
        });
        
        target.appendChild(loader);
        return loader;
    },
    
    hide: (loader) => {
        if (loader && loader.parentNode) {
            animate.fadeOut(loader, 200);
            setTimeout(() => {
                if (loader.parentNode) {
                    loader.parentNode.removeChild(loader);
                }
            }, 200);
        }
    }
};

// Export utilities globally
window.FayvaUtils = {
    domReady,
    debounce,
    throttle,
    getCSRFToken,
    ajax,
    storage,
    url,
    element,
    animate,
    validate,
    dateUtils,
    numberUtils,
    stringUtils,
    cookies,
    device,
    perf,
    notify,
    loading
};

// Add notification styles if not present
domReady(() => {
    if (!document.querySelector('#notification-styles')) {
        const styles = element.create('style', {
            id: 'notification-styles',
            innerHTML: `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    max-width: 400px;
                    padding: 1rem;
                    border-radius: 8px;
                    color: white;
                    z-index: 10000;
                    transform: translateX(100%);
                    transition: transform 0.3s ease;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                }
                .notification.show {
                    transform: translateX(0);
                }
                .notification.hide {
                    transform: translateX(100%);
                }
                .notification-success { background: #28a745; }
                .notification-error { background: #dc3545; }
                .notification-warning { background: #ffc107; color: #212529; }
                .notification-info { background: #17a2b8; }
                .notification-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .notification-close {
                    background: none;
                    border: none;
                    color: inherit;
                    font-size: 1.2rem;
                    cursor: pointer;
                    margin-left: 1rem;
                    opacity: 0.8;
                }
                .notification-close:hover {
                    opacity: 1;
                }
                .loading-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 9999;
                }
                .loading-spinner {
                    background: white;
                    padding: 2rem;
                    border-radius: 8px;
                    text-align: center;
                }
                .spinner {
                    width: 40px;
                    height: 40px;
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #1e3c72;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 1rem;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                .loading-message {
                    color: #333;
                    font-weight: 500;
                }
            `
        });
        document.head.appendChild(styles);
    }
});