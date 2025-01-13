window.onload = function() {
    // Add a custom button for login
    const authorizeButton = document.createElement('button');
    authorizeButton.textContent = 'Login with Token';
    authorizeButton.style = 'margin: 10px; padding: 10px;';
    authorizeButton.onclick = function() {
        const phone_number = prompt("Enter your phone_number:");
        const password = prompt("Enter your password:");
        if (username && password) {
            fetch('/api/user/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ phone_number: phone_number, password: password }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.token) {
                        const apiKeyAuth = document.querySelector('[name="apiKeyAuth"]');
                        apiKeyAuth.value = `Bearer ${data.token}`;
                        alert("Login successful! Token added to Authorization header.");
                    } else {
                        alert("Login failed! Check your phone_number and password.");
                    }
                });
        }
    };

    // Append the button to the Swagger UI
    const swaggerUI = document.querySelector('.swagger-ui');
    if (swaggerUI) {
        swaggerUI.prepend(authorizeButton);
    }
};
