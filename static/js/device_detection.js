function getDeviceType() {
    const width = window.innerWidth;
    let deviceType;
    if (width <= 425) {
        deviceType = 3; // Mobile
    } else if (width >= 426 && width < 769) {
        deviceType = 4; // Tablet
    } else {
        deviceType = 8; // Laptop and Desktop
    }
    return deviceType;
}

function updateDeviceType() {
    let deviceType = getDeviceType();
    fetch('/api/save-device-type/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ device_type: deviceType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.refresh) {
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Debounce function to limit how often a function can fire
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

// Call updateDeviceType on load
window.addEventListener("load", updateDeviceType);

// Call updateDeviceType on resize with debounce
window.addEventListener('resize', debounce(() => {
    updateDeviceType();
}, 250));

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}