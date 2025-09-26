// static/js/script.js - Global JavaScript Functions

$(document).ready(function() {
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Smooth scroll for internal links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });
    
    // Form validation helper
    window.validateEmail = function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    };
    
    // Show loading state on buttons
    window.showLoading = function(button) {
        const originalText = $(button).html();
        $(button).data('original-text', originalText);
        $(button).html('<span class="loading"></span> Loading...').prop('disabled', true);
    };
    
    window.hideLoading = function(button) {
        const originalText = $(button).data('original-text');
        $(button).html(originalText).prop('disabled', false);
    };
    
    // Confirm dialog helper
    window.confirmAction = function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    };
    
    // Toast notification (simple version)
    window.showToast = function(message, type = 'success') {
        const toast = $(`
            <div class="alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3" 
                 role="alert" style="z-index: 9999;">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(toast);
        
        setTimeout(function() {
            toast.fadeOut('slow', function() {
                $(this).remove();
            });
        }, 3000);
    };
    
    // Image preview helper
    window.previewImage = function(input, previewElement) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                $(previewElement).attr('src', e.target.result);
            };
            
            reader.readAsDataURL(input.files[0]);
        }
    };
    
    // Character counter for textareas
    $('textarea[maxlength]').each(function() {
        const maxLength = $(this).attr('maxlength');
        const counter = $('<small class="text-muted float-end"></small>');
        $(this).after(counter);
        
        const updateCounter = () => {
            const remaining = maxLength - $(this).val().length;
            counter.text(`${remaining} characters remaining`);
        };
        
        $(this).on('input', updateCounter);
        updateCounter();
    });
    
    // Prevent double submission
    $('form').on('submit', function() {
        $(this).find('button[type="submit"]').prop('disabled', true);
    });
    
    // Auto-focus first input in modals
    $('.modal').on('shown.bs.modal', function() {
        $(this).find('input:text:visible:first').focus();
    });
    
    // Image error handling
    $('img').on('error', function() {
        if (!$(this).hasClass('error-handled')) {
            $(this).addClass('error-handled');
            const width = $(this).attr('width') || 150;
            $(this).attr('src', `https://via.placeholder.com/${width}`);
        }
    });
    
    // Tooltip initialization (if Bootstrap tooltips are used)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Utility Functions

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    return 'Just now';
}

// Truncate text
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

// Copy to clipboard
function copyToClipboard(text) {
    const temp = $('<textarea>');
    $('body').append(temp);
    temp.val(text).select();
    document.execCommand('copy');
    temp.remove();
    showToast('Copied to clipboard!', 'success');
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Debounce function for search inputs
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

// LocalStorage helper (for future use)
const storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage error:', e);
        }
    },
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Storage error:', e);
            return null;
        }
    },
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Storage error:', e);
        }
    }
};

// AJAX error handler
$(document).ajaxError(function(event, jqxhr, settings, thrownError) {
    console.error('AJAX Error:', thrownError);
    showToast('An error occurred. Please try again.', 'danger');
});

// Prevent form resubmission on page refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

console.log('TaskStreak App Loaded! 🔥');