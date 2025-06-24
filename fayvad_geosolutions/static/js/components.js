// Fayvad Geosolutions - Components JavaScript
// File: static/js/components.js

// Service Card Interactions
class ServiceCard {
    constructor(element) {
        this.element = element;
        this.init();
    }
    
    init() {
        this.element.addEventListener('mouseenter', this.onMouseEnter.bind(this));
        this.element.addEventListener('mouseleave', this.onMouseLeave.bind(this));
        this.element.addEventListener('click', this.onClick.bind(this));
    }
    
    onMouseEnter() {
        this.element.style.transform = 'translateY(-10px) scale(1.02)';
    }
    
    onMouseLeave() {
        this.element.style.transform = 'translateY(0) scale(1)';
    }
    
    onClick() {
        const serviceLink = this.element.querySelector('a') || this.element.dataset.href;
        if (serviceLink) {
            window.location.href = serviceLink.href || serviceLink;
        }
    }
}

// Statistics Counter Animation
class StatsCounter {
    constructor(element) {
        this.element = element;
        this.target = parseInt(this.element.textContent.replace(/\D/g, ''));
        this.suffix = this.element.textContent.replace(/[\d,]/g, '');
        this.hasAnimated = false;
        this.init();
    }
    
    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.hasAnimated) {
                    this.animate();
                    this.hasAnimated = true;
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(this.element);
    }
    
    animate() {
        const duration = 2000;
        const steps = 60;
        const stepValue = this.target / steps;
        const stepTime = duration / steps;
        let current = 0;
        let step = 0;
        
        const timer = setInterval(() => {
            step++;
            current = Math.min(stepValue * step, this.target);
            
            // Add easing effect
            const progress = step / steps;
            const eased = 1 - Math.pow(1 - progress, 3); // Ease out cubic
            const value = Math.floor(this.target * eased);
            
            this.element.textContent = value.toLocaleString() + this.suffix;
            
            if (step >= steps) {
                this.element.textContent = this.target.toLocaleString() + this.suffix;
                clearInterval(timer);
            }
        }, stepTime);
    }
}

// Team Card Flip Effect
class TeamCard {
    constructor(element) {
        this.element = element;
        this.isFlipped = false;
        this.init();
    }
    
    init() {
        this.createBackSide();
        this.element.addEventListener('click', this.flip.bind(this));
    }
    
    createBackSide() {
        const backData = this.element.dataset;
        if (backData.skills || backData.experience) {
            const backSide = document.createElement('div');
            backSide.className = 'team-card-back';
            backSide.innerHTML = `
                <div class="team-back-content">
                    ${backData.skills ? `<div class="team-skills">
                        <h4>Skills</h4>
                        <p>${backData.skills}</p>
                    </div>` : ''}
                    ${backData.experience ? `<div class="team-experience">
                        <h4>Experience</h4>
                        <p>${backData.experience}</p>
                    </div>` : ''}
                </div>
            `;
            this.element.appendChild(backSide);
        }
    }
    
    flip() {
        this.isFlipped = !this.isFlipped;
        this.element.classList.toggle('flipped', this.isFlipped);
    }
}

// Project Gallery
class ProjectGallery {
    constructor(element) {
        this.element = element;
        this.images = Array.from(element.querySelectorAll('.gallery-image'));
        this.currentIndex = 0;
        this.init();
    }
    
    init() {
        if (this.images.length > 1) {
            this.createControls();
            this.createDots();
            this.autoPlay();
        }
    }
    
    createControls() {
        const controls = document.createElement('div');
        controls.className = 'gallery-controls';
        controls.innerHTML = `
            <button class="gallery-prev" aria-label="Previous image">‹</button>
            <button class="gallery-next" aria-label="Next image">›</button>
        `;
        
        this.element.appendChild(controls);
        
        controls.querySelector('.gallery-prev').addEventListener('click', () => this.prev());
        controls.querySelector('.gallery-next').addEventListener('click', () => this.next());
    }
    
    createDots() {
        const dots = document.createElement('div');
        dots.className = 'gallery-dots';
        
        this.images.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.className = 'gallery-dot';
            dot.setAttribute('aria-label', `Go to image ${index + 1}`);
            if (index === 0) dot.classList.add('active');
            
            dot.addEventListener('click', () => this.goTo(index));
            dots.appendChild(dot);
        });
        
        this.element.appendChild(dots);
        this.dots = Array.from(dots.children);
    }
    
    next() {
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.updateGallery();
    }
    
    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        this.updateGallery();
    }
    
    goTo(index) {
        this.currentIndex = index;
        this.updateGallery();
    }
    
    updateGallery() {
        this.images.forEach((img, index) => {
            img.classList.toggle('active', index === this.currentIndex);
        });
        
        if (this.dots) {
            this.dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === this.currentIndex);
            });
        }
    }
    
    autoPlay() {
        setInterval(() => {
            if (!this.element.matches(':hover')) {
                this.next();
            }
        }, 5000);
    }
}

// Testimonial Slider
class TestimonialSlider {
    constructor(element) {
        this.element = element;
        this.testimonials = Array.from(element.querySelectorAll('.testimonial'));
        this.currentIndex = 0;
        this.init();
    }
    
    init() {
        if (this.testimonials.length > 1) {
            this.createSlider();
            this.autoRotate();
        }
    }
    
    createSlider() {
        this.element.classList.add('testimonial-slider');
        
        const controls = document.createElement('div');
        controls.className = 'slider-controls';
        controls.innerHTML = `
            <button class="slider-prev">‹</button>
            <div class="slider-indicators">
                ${this.testimonials.map((_, i) => `
                    <button class="slider-dot ${i === 0 ? 'active' : ''}" data-index="${i}"></button>
                `).join('')}
            </div>
            <button class="slider-next">›</button>
        `;
        
        this.element.appendChild(controls);
        
        // Event listeners
        controls.querySelector('.slider-prev').addEventListener('click', () => this.prev());
        controls.querySelector('.slider-next').addEventListener('click', () => this.next());
        
        controls.querySelectorAll('.slider-dot').forEach((dot, index) => {
            dot.addEventListener('click', () => this.goTo(index));
        });
        
        this.updateSlider();
    }
    
    next() {
        this.currentIndex = (this.currentIndex + 1) % this.testimonials.length;
        this.updateSlider();
    }
    
    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.testimonials.length) % this.testimonials.length;
        this.updateSlider();
    }
    
    goTo(index) {
        this.currentIndex = index;
        this.updateSlider();
    }
    
    updateSlider() {
        this.testimonials.forEach((testimonial, index) => {
            testimonial.style.display = index === this.currentIndex ? 'block' : 'none';
        });
        
        const dots = this.element.querySelectorAll('.slider-dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }
    
    autoRotate() {
        setInterval(() => {
            if (!this.element.matches(':hover')) {
                this.next();
            }
        }, 7000);
    }
}

// Animated Progress Bars
class ProgressBar {
    constructor(element) {
        this.element = element;
        this.percentage = parseInt(element.dataset.percentage) || 0;
        this.hasAnimated = false;
        this.init();
    }
    
    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.hasAnimated) {
                    this.animate();
                    this.hasAnimated = true;
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(this.element);
    }
    
    animate() {
        const fill = this.element.querySelector('.progress-fill');
        const text = this.element.querySelector('.progress-text');
        
        if (fill) {
            fill.style.width = '0%';
            fill.style.transition = 'width 2s ease-out';
            
            setTimeout(() => {
                fill.style.width = this.percentage + '%';
            }, 100);
        }
        
        if (text) {
            let current = 0;
            const timer = setInterval(() => {
                current += this.percentage / 60; // 60 steps over 2 seconds
                if (current >= this.percentage) {
                    text.textContent = this.percentage + '%';
                    clearInterval(timer);
                } else {
                    text.textContent = Math.floor(current) + '%';
                }
            }, 33);
        }
    }
}

// Masonry Grid Layout
class MasonryGrid {
    constructor(element) {
        this.element = element;
        this.items = Array.from(element.children);
        this.columns = parseInt(element.dataset.columns) || 3;
        this.gap = parseInt(element.dataset.gap) || 20;
        this.init();
    }
    
    init() {
        this.layout();
        window.addEventListener('resize', this.debounce(() => this.layout(), 250));
    }
    
    layout() {
        const containerWidth = this.element.offsetWidth;
        const columnWidth = (containerWidth - (this.columns - 1) * this.gap) / this.columns;
        const columnHeights = new Array(this.columns).fill(0);
        
        this.items.forEach(item => {
            const shortestColumn = columnHeights.indexOf(Math.min(...columnHeights));
            const x = shortestColumn * (columnWidth + this.gap);
            const y = columnHeights[shortestColumn];
            
            item.style.position = 'absolute';
            item.style.left = x + 'px';
            item.style.top = y + 'px';
            item.style.width = columnWidth + 'px';
            
            columnHeights[shortestColumn] += item.offsetHeight + this.gap;
        });
        
        this.element.style.height = Math.max(...columnHeights) + 'px';
        this.element.style.position = 'relative';
    }
    
    debounce(func, wait) {
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
}

// Parallax Background
class ParallaxBackground {
    constructor(element) {
        this.element = element;
        this.speed = parseFloat(element.dataset.speed) || 0.5;
        this.init();
    }
    
    init() {
        window.addEventListener('scroll', this.throttle(() => this.updatePosition(), 16));
    }
    
    updatePosition() {
        const scrolled = window.pageYOffset;
        const rect = this.element.getBoundingClientRect();
        const elementTop = rect.top + scrolled;
        const elementHeight = rect.height;
        const windowHeight = window.innerHeight;
        
        // Only animate if element is in viewport
        if (scrolled + windowHeight > elementTop && scrolled < elementTop + elementHeight) {
            const yPos = (scrolled - elementTop) * this.speed;
            this.element.style.transform = `translateY(${yPos}px)`;
        }
    }
    
    throttle(func, limit) {
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
}

// Card Hover Effects
class CardHoverEffect {
    constructor(element) {
        this.element = element;
        this.init();
    }
    
    init() {
        this.element.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.element.addEventListener('mouseleave', this.onMouseLeave.bind(this));
    }
    
    onMouseMove(e) {
        const rect = this.element.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        this.element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
    }
    
    onMouseLeave() {
        this.element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    }
}

// Initialize components when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize service cards
    document.querySelectorAll('.service-card').forEach(card => {
        new ServiceCard(card);
    });
    
    // Initialize stats counters
    document.querySelectorAll('.stat-number').forEach(counter => {
        new StatsCounter(counter);
    });
    
    // Initialize team cards
    document.querySelectorAll('.team-card').forEach(card => {
        new TeamCard(card);
    });
    
    // Initialize project galleries
    document.querySelectorAll('.project-gallery').forEach(gallery => {
        new ProjectGallery(gallery);
    });
    
    // Initialize testimonial sliders
    document.querySelectorAll('.testimonials-container').forEach(slider => {
        new TestimonialSlider(slider);
    });
    
    // Initialize progress bars
    document.querySelectorAll('.progress-bar').forEach(bar => {
        new ProgressBar(bar);
    });
    
    // Initialize masonry grids
    document.querySelectorAll('.masonry-grid').forEach(grid => {
        new MasonryGrid(grid);
    });
    
    // Initialize parallax backgrounds
    document.querySelectorAll('[data-parallax]').forEach(element => {
        new ParallaxBackground(element);
    });
    
    // Initialize card hover effects
    document.querySelectorAll('.card-3d').forEach(card => {
        new CardHoverEffect(card);
    });
    
    // Add component styles
    addComponentStyles();
});

// Add CSS styles for components
function addComponentStyles() {
    if (document.querySelector('#component-styles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'component-styles';
    styles.textContent = `
        /* Team Card Flip Styles */
        .team-card {
            transition: transform 0.6s;
            transform-style: preserve-3d;
            cursor: pointer;
        }
        
        .team-card.flipped {
            transform: rotateY(180deg);
        }
        
        .team-card-back {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: #1e3c72;
            color: white;
            padding: 2rem;
            border-radius: 15px;
            transform: rotateY(180deg);
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .team-info {
            backface-visibility: hidden;
        }
        
        /* Gallery Styles */
        .gallery-image {
            display: none;
        }
        
        .gallery-image.active {
            display: block;
        }
        
        .gallery-controls {
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            transform: translateY(-50%);
        }
        
        .gallery-prev,
        .gallery-next {
            background: rgba(30, 60, 114, 0.8);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .gallery-prev:hover,
        .gallery-next:hover {
            background: #ffd700;
            color: #1e3c72;
        }
        
        .gallery-dots {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 0.5rem;
        }
        
        .gallery-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            border: none;
            background: rgba(255, 255, 255, 0.5);
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .gallery-dot.active,
        .gallery-dot:hover {
            background: #ffd700;
        }
        
        /* Testimonial Slider Styles */
        .testimonial-slider {
            position: relative;
        }
        
        .slider-controls {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .slider-prev,
        .slider-next {
            background: #1e3c72;
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .slider-prev:hover,
        .slider-next:hover {
            background: #ffd700;
            color: #1e3c72;
        }
        
        .slider-indicators {
            display: flex;
            gap: 0.5rem;
        }
        
        .slider-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2px solid #1e3c72;
            background: transparent;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .slider-dot.active,
        .slider-dot:hover {
            background: #ffd700;
            border-color: #ffd700;
        }
        
        /* Progress Bar Styles */
        .progress-bar {
            background: #f0f0f0;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            position: relative;
            margin: 1rem 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1e3c72, #ffd700);
            width: 0%;
            transition: width 2s ease-out;
        }
        
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: bold;
            color: #333;
            font-size: 0.9rem;
        }
        
        /* Card 3D Hover Effects */
        .card-3d {
            transition: transform 0.3s ease;
            transform-style: preserve-3d;
        }
        
        /* Loading States */
        .loading-skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Fade transitions */
        .fade-enter {
            opacity: 0;
            transform: translateY(20px);
        }
        
        .fade-enter-active {
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        
        .fade-exit {
            opacity: 1;
            transform: translateY(0);
        }
        
        .fade-exit-active {
            opacity: 0;
            transform: translateY(-20px);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .gallery-controls {
                display: none;
            }
            
            .gallery-dots {
                bottom: -30px;
            }
            
            .slider-controls {
                flex-direction: column;
                gap: 1rem;
            }
            
            .card-3d:hover {
                transform: none;
            }
        }
    `;
    
    document.head.appendChild(styles);
}