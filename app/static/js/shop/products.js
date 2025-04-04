document.addEventListener("DOMContentLoaded", function() {
    // Scroll behavior for category navigation
    const categoryNav = document.querySelector('.category-nav');
    let lastScroll = 0;
    const threshold = 50; // pixels to scroll before hiding
    
    // Make category nav sticky
    categoryNav.style.position = 'sticky';
    categoryNav.style.top = '0';
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            // At top of page - always show navbar
            categoryNav.style.transform = 'translateY(0)';
            return;
        }
        
        if (currentScroll > lastScroll && currentScroll > threshold) {
            // Scrolling down past threshold - hide navbar
            categoryNav.style.transform = 'translateY(-100%)';
        } else if (currentScroll < lastScroll || currentScroll < threshold) {
            // Scrolling up or not past threshold - show navbar
            categoryNav.style.transform = 'translateY(0)';
        }
        
        lastScroll = currentScroll;
 });
});


document.addEventListener("DOMContentLoaded", function() {
    // Category Navigation
    const categoryBtns = document.querySelectorAll('.category-btn');
    const productCategories = document.querySelectorAll('.product-category');
    
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const categoryId = this.dataset.category;
            
            // Update active category button
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding product category
            productCategories.forEach(cat => {
                cat.classList.remove('active');
                if (cat.id === `category-${categoryId}`) {
                    cat.classList.add('active');
                }
            });
        });
    });
    
    // Quantity Selector
    document.querySelectorAll('.qty-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            let value = parseInt(input.value);
            
            if (this.classList.contains('plus')) {
                input.value = value + 1;
            } else if (this.classList.contains('minus') && value > 1) {
                input.value = value - 1;
            }
        });
    });
    
    // Add to Cart Functionality
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent link navigation
            const productId = this.getAttribute('data-product-id');
            const quantityInput = document.getElementById(`quantity-${productId}`);
            const quantity = quantityInput.value;
            
            fetch("/shop/add_to_cart", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification("Added to cart successfully!");
                } else {
                    showNotification("Failed to add to cart: " + data.error, false);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showNotification("An error occurred", false);
            });
        });
    });
    
    // Cart Notification
    function showNotification(message, isSuccess = true) {
        const notification = document.getElementById('cart-notification');
        const messageEl = document.getElementById('notification-message');
        
        messageEl.textContent = message;
        notification.style.backgroundColor = isSuccess ? 'var(--success-color)' : 'var(--error-color)';
        notification.classList.add('show');
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
    
    // Make sure buttons and inputs remain clickable
    document.querySelectorAll('.quantity-input, .qty-btn, .add-to-cart-btn').forEach(el => {
        el.style.zIndex = '3';
        el.style.position = 'relative';
    });
});
