// Theme switcher functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Theme toggle event handler
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        // Set initial state based on saved theme
        if (savedTheme === 'dark') {
            themeToggle.classList.add('active');
        }
        
        // Add click event listener
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            // Apply new theme
            document.documentElement.setAttribute('data-theme', newTheme);
            
            // Save to localStorage
            localStorage.setItem('theme', newTheme);
            
            // Update toast message
            showToast(`تم تفعيل الوضع ${newTheme === 'dark' ? 'المظلم' : 'المضيء'}`);
        });
    }
    
    // Glass card effects
    applyGlassEffects();
    
    // Add animation classes
    addAnimationClasses();
    
    // Add interactive elements
    setupInteractiveElements();
});

// Apply glass effect to selected elements
function applyGlassEffects() {
    // Add glass-card class to selected cards
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        heroSection.classList.add('glass-card');
    }
    
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.classList.add('glass-card');
    });
    
    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) {
        uploadArea.classList.add('glass-card');
    }
}

// Add animation classes to elements
function addAnimationClasses() {
    // Add fade-in animation to major sections
    const elements = document.querySelectorAll('.card, .hero-section h1, .feature-card, .upload-area');
    elements.forEach((element, index) => {
        element.classList.add('animate-fade-in');
        element.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add pulse to primary action button
    const mainActionBtn = document.querySelector('#submit-btn');
    if (mainActionBtn) {
        mainActionBtn.classList.add('btn-pulse');
    }
}

// Setup interactive elements
function setupInteractiveElements() {
    // Make cards interactive
    const cards = document.querySelectorAll('.card:not(.feature-card)');
    cards.forEach(card => {
        card.classList.add('interactive-hover');
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-success');
    buttons.forEach(button => {
        button.classList.add('interactive-element');
    });
}

// Toast notification
function showToast(message) {
    const toastContainer = document.querySelector('.toast-container');
    
    // Create container if it doesn't exist
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.innerHTML = `
        <div class="toast-body">
            ${message}
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Add to container
    document.querySelector('.toast-container').appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Create cool ripple effect on button clicks
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn')) {
        // Create ripple element
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        e.target.appendChild(ripple);

        // Set position
        const rect = e.target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        // Remove after animation completes
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});

// Image preview with zoom effect
document.addEventListener('DOMContentLoaded', function() {
    const resultImages = document.querySelectorAll('.result-card img');
    
    resultImages.forEach(img => {
        img.addEventListener('click', function() {
            // Create overlay
            const overlay = document.createElement('div');
            overlay.className = 'image-preview-overlay';
            
            // Create image container
            const imgContainer = document.createElement('div');
            imgContainer.className = 'image-preview-container';
            
            // Create image element
            const previewImg = document.createElement('img');
            previewImg.src = this.src;
            previewImg.className = 'image-preview';
            
            // Add close button
            const closeBtn = document.createElement('button');
            closeBtn.className = 'image-preview-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.addEventListener('click', function() {
                overlay.classList.remove('active');
                setTimeout(() => {
                    overlay.remove();
                }, 300);
            });
            
            // Append elements
            imgContainer.appendChild(previewImg);
            imgContainer.appendChild(closeBtn);
            overlay.appendChild(imgContainer);
            document.body.appendChild(overlay);
            
            // Activate overlay with a delay for animation
            setTimeout(() => {
                overlay.classList.add('active');
            }, 10);
            
            // Close on overlay click
            overlay.addEventListener('click', function(e) {
                if (e.target === overlay) {
                    overlay.classList.remove('active');
                    setTimeout(() => {
                        overlay.remove();
                    }, 300);
                }
            });
        });
    });
}); 