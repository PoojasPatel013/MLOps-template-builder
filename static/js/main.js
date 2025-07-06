document.addEventListener('DOMContentLoaded', () => {
    // Form submission handling
    const form = document.getElementById('templateForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = 'Generating...';
            submitButton.disabled = true;

            try {
                // Collect form data
                const formData = new FormData(form);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }

                // Send request
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                // Show success message
                showNotification(result.message, response.ok);
            } catch (error) {
                console.error('Error:', error);
                showNotification('An error occurred while generating the template', false);
            } finally {
                // Reset button
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });
    }

    // Add smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

function showNotification(message, isSuccess) {
    const alert = document.createElement('div');
    alert.className = `alert ${isSuccess ? 'alert-success' : 'alert-error'}`;
    alert.textContent = message;
    
    // Add to body
    document.body.appendChild(alert);
    
    // Remove after 3 seconds
    setTimeout(() => {
        alert.remove();
    }, 3000);
}
