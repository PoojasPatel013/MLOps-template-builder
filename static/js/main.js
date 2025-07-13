document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');

    // Notification handling
    function showNotification(type, message) {
        console.log(`Showing notification: ${type} - ${message}`);
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

    // Initialize elements
    console.log('Initializing elements...');
    const directoryPickerBtn = document.getElementById('directoryPicker');
    const directoryPathInput = document.getElementById('directoryPath');
    const directoryPathHidden = document.getElementById('directoryPathHidden');
    const notificationsContainer = document.getElementById('notifications');
    const form = document.getElementById('templateForm');
    let submitButton = null;

    console.log('Element initialization results:');
    console.log('directoryPickerBtn:', directoryPickerBtn ? 'found' : 'not found');
    console.log('directoryPathInput:', directoryPathInput ? 'found' : 'not found');
    console.log('directoryPathHidden:', directoryPathHidden ? 'found' : 'not found');
    console.log('notificationsContainer:', notificationsContainer ? 'found' : 'not found');
    console.log('form:', form ? 'found' : 'not found');

    // Directory picker functionality
    if (directoryPickerBtn && directoryPathInput && directoryPathHidden) {
        console.log('Setting up directory picker...');
        directoryPickerBtn.addEventListener('click', async () => {
            try {
                console.log('Directory picker clicked');
                if (!('showDirectoryPicker' in window)) {
                    showNotification('error', 'Directory picker is not supported in this browser');
                    return;
                }
                const handle = await window.showDirectoryPicker();
                
                if (handle) {
                    console.log('Directory selected successfully');
                    window.selectedDirectory = handle;
                    const fullPath = await handle.resolve();
                    directoryPathInput.value = fullPath;
                    directoryPathHidden.value = fullPath;
                    showNotification('success', 'Directory selected successfully');
                } else {
                    console.log('No directory selected');
                    showNotification('error', 'No directory selected');
                }
            } catch (error) {
                console.error('Directory picker error:', error);
                if (error.name === 'AbortError') {
                    console.log('Directory picker aborted');
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

    // Form handling
    if (form) {
        console.log('Setting up form handler...');
        submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            console.log('Submit button found');
            form.addEventListener('submit', async (e) => {
                console.log('Form submitted');
                e.preventDefault();
                
                const directoryPathHidden = document.getElementById('directoryPathHidden');
                if (!directoryPathHidden || !directoryPathHidden.value) {
                    console.log('No directory selected');
                    showNotification('error', 'Please select a directory first');
                    return;
                }

                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = 'Generating...';
                submitButton.disabled = true;

                try {
                    console.log('Getting form data...');
                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData.entries());
                    
                    console.log('Form data:', data);
                    
                    console.log('Sending request to backend...');
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });

                    console.log('Response received:', response);
                    
                    if (!response.ok) {
                        console.error('Response not OK:', response.status);
                        const errorData = await response.json();
                        console.error('Error data:', errorData);
                        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();
                    console.log('Result:', result);
                    
                    if (result.error) {
                        console.error('Result contains error:', result.error);
                        throw new Error(result.error);
                    }

                    showNotification('success', 'Template generated successfully!');
                    showNotification('info', `Project created at: ${result.project_path}`);
                } catch (error) {
                    console.error('Error generating template:', error);
                    showNotification('error', error.message || 'An error occurred while generating the template');
                } finally {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }
            });
        } else {
            console.error('Submit button not found');
        }
    } else {
        console.error('Form not found');
    }

    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
