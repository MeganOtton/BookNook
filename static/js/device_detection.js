function getDeviceType() {
    const width = window.innerWidth;
    let deviceType;
    if (width <= 425) {
        deviceType = 3; // Mobile
        return deviceType; // Mobile
    } else if (width >= 426 && width < 769) {
        deviceType = 4; // Tablet
        return deviceType; // Tablet
    } else {
        deviceType = 8; // Laptop and Desktop
        return deviceType; // Laptop and Desktop
    }
    console.log("Current device type:", deviceType);
}


window.addEventListener("load", () => {
    let deviceType = getDeviceType();
    // deviceTypeForm.submit()
    let cookie = getCookie('csrftoken');  // Get CSRF token from cookies
    console.log("Cookie:", cookie);

    fetch('/api/save-device-type/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
        },
        body: JSON.stringify({ device_type: deviceType })  // Example data
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
    
    // Function to get CSRF token from cookies
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
});

// Call the function on load and resize
window.addEventListener('resize', () => {   
    let deviceType = getDeviceType();
    // deviceTypeForm.submit()
    let cookie = getCookie('csrftoken');  // Get CSRF token from cookies
    console.log("Cookie:", cookie);

    fetch('/api/save-device-type/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
        },
    })
    .then(response => response.json())
    .then(data => {
        if (deviceType !== data.message) {
            fetch('/api/save-device-type/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
                },
                body: JSON.stringify({ device_type: deviceType })  // Example data
            })
            .then(response => location.reload())
        }
    })
    .catch(error => console.error('Error:', error));


    
    // Function to get CSRF token from cookies
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

});