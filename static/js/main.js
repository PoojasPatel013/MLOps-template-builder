document.addEventListener('DOMContentLoaded', () => {
    function showNotification(type, message) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        const notifications = document.getElementById('notifications');
        if (notifications) {
            notifications.appendChild(notification);
            
            notification.classList.add('fade-in');
            setTimeout(() => {
                notification.classList.remove('fade-in');
                notification.classList.add('fade-out');
            }, 2000);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }
    }

    const directoryPickerBtn = document.getElementById('directoryPicker');
    const directoryPathInput = document.getElementById('directoryPath');
    const directoryPathHidden = document.getElementById('directoryPathHidden');
    if (directoryPickerBtn && directoryPathInput && directoryPathHidden) {
        directoryPickerBtn.addEventListener('click', async () => {
            try {
                if (!('showDirectoryPicker' in window)) {
                    showNotification('error', 'Directory picker is not supported in this browser');
                    return;
                }
                const handle = await window.showDirectoryPicker();
                
                if (handle) {
                    window.selectedDirectory = handle;
                    const fullPath = await handle.resolve();
                    
                    directoryPathInput.value = fullPath;
                    directoryPathHidden.value = fullPath;
                    
                    showNotification('success', 'Directory selected successfully');
                } else {
                    showNotification('error', 'No directory selected');
                }
            } catch (error) {
                if (error.name === 'AbortError') {
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

    const form = document.getElementById('templateForm');
    const submitButton = form.querySelector('button[type="submit"]');
    if (form && submitButton) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const directoryPathHidden = document.getElementById('directoryPathHidden');
            if (!directoryPathHidden || !directoryPathHidden.value) {
                showNotification('error', 'Please select a directory first');
                return;
            }

            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = 'Generating...';
            submitButton.disabled = true;

            try {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData.entries());
                
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
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
