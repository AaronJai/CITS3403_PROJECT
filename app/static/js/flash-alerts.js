// filepath: c:\Users\Aaron\git\CITS3403_PROJECT\app\static\js\flash-alerts.js

// Function to dismiss an alert with a smooth slide-out animation
function dismissAlert(alertId) {
    const alertElement = document.getElementById(alertId);
    
    if (alertElement) {
        // Add slide-out and fade-out classes
        alertElement.classList.add('opacity-0', 'translate-x-full');
        
        // Remove the element after animation completes
        setTimeout(() => {
            alertElement.remove();
            
            // Check if there are no more alerts
            const flashContainer = document.getElementById('flash-messages');
            if (flashContainer && flashContainer.children.length === 0) {
                flashContainer.remove();
            }
        }, 300); // Match this to the CSS transition duration
    }
}

// Function to auto-dismiss alerts after a delay
function setupAutoDismiss() {
    const alerts = document.querySelectorAll('.flash-alert');
    
    alerts.forEach((alert, index) => {
        // Different delays for different alerts so they don't all disappear at once
        // Success messages disappear faster than errors
        const category = alert.classList.contains('bg-red-50') ? 'error' : 
                        alert.classList.contains('bg-yellow-50') ? 'warning' : 
                        alert.classList.contains('bg-green-50') ? 'success' : 'info';
        
        const delay = category === 'error' ? 10000 : 
                      category === 'warning' ? 7000 : 
                      category === 'success' ? 5000 : 6000;
        
        // Add a slight stagger to the timing
        setTimeout(() => {
            const alertId = alert.id;
            if (document.getElementById(alertId)) {
                dismissAlert(alertId);
            }
        }, delay + (index * 300));
    });
}

// Setup when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    setupAutoDismiss();
    
    // Add entry animation with slide-in effect
    const alerts = document.querySelectorAll('.flash-alert');
    alerts.forEach((alert, index) => {
        // Initially set with translate-x-full and opacity-0 in the HTML
        
        // Stagger the appearance of each alert with slide-in animation
        setTimeout(() => {
            alert.classList.remove('translate-x-full', 'opacity-0');
            alert.classList.add('translate-x-0', 'opacity-100');
        }, 100 + (index * 150));
    });
});