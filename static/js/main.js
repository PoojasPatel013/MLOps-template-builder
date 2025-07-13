document.addEventListener('DOMContentLoaded', () => {
    // Add directory picker button
    const directoryPickerBtn = document.getElementById('directoryPicker');
    const directoryPathInput = document.getElementById('directoryPath');
    const directoryPathHidden = document.getElementById('directoryPathHidden');
    const notifications = document.getElementById('notifications');

    // Directory picker functionality
    if (directoryPickerBtn && directoryPathInput && directoryPathHidden) {
        directoryPickerBtn.addEventListener('click', async () => {
            try {
                // Request permission for directory access
                const handle = await window.showDirectoryPicker();
                
                if (handle) {
                    // Store the directory handle
                    window.selectedDirectory = handle;
                    
                    // Get the absolute path
                    const fullPath = await handle.resolve();
                    
                    // Update both visible and hidden inputs
                    directoryPathInput.value = fullPath;
                    directoryPathHidden.value = fullPath;
                    
                    showNotification('success', 'Directory selected successfully');
                } else {
                    showNotification('error', 'No directory selected');
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    // User cancelled the picker
                    return;
                }
                if (error.name === 'NotAllowedError') {
                    showNotification('error', 'Permission denied to access directory. Please allow access in browser settings.');
                } else {
                    showNotification('error', 'Failed to select directory: ' + error.message);
                }
            }
        });
    }

    // Form submission handling
    const form = document.getElementById('templateForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Get the directory path from the hidden input
            const directoryPathHidden = document.getElementById('directoryPathHidden');
            if (!directoryPathHidden || !directoryPathHidden.value) {
                showNotification('error', 'Please select a directory first');
                return;
            }

            // Get submit button and show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            if (!submitButton) return;

            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = 'Generating...';
            submitButton.disabled = true;

            try {
                // Get form data
                const formData = new FormData(form);
                const data = Object.fromEntries(formData.entries());
                
                // Send request to server
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                if (response.ok) {
                    showNotification('success', 'Template generated successfully!');
                    showNotification('info', `Project created at: ${result.project_path}`);
                } else {
                    throw new Error(result.error || 'Failed to generate template');
                }
            } catch (error) {
                showNotification('error', error.message || 'An error occurred');
            } finally {
                // Re-enable submit button
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });
    }
    const result = response.json();
                
                if (response.ok) {
                    // Success case
                    const message = result.message || 'Template generated successfully';
                    showNotification(message, true);
                    
                    // Add project path to the notification
                    if (result.project_path) {
                        showNotification('info', `Project created at: ${result.project_path}`);
                    }
                } else {
                    // Error case
                    const errorMessage = result.error || 'Failed to generate template';
                    showNotification(errorMessage, false);
                }
            }
        );

    // Update preview when form changes
    form.addEventListener('input', updatePreview);

    // Add smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

// Notification handling
function showNotification(message, isSuccess) {
    const notification = document.createElement('div');
    notification.className = `notification ${isSuccess ? 'success' : 'error'}`;
    notification.textContent = message;
    
    const notifications = document.getElementById('notifications');
    if (notifications) {
        notifications.appendChild(notification);
        
        // Add animation classes
        notification.classList.add('fade-in');
        setTimeout(() => {
            notification.classList.remove('fade-in');
            notification.classList.add('fade-out');
        }, 2000);
        
        // Remove notification after animation
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}
