document.querySelector('form').addEventListener('submit', async function (e) {
    e.preventDefault();  // Prevent form submission

    // Helper function to validate email format
    function validateEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

// Helper function to validate password strength
    function validatePassword(password) {
        // Example: At least 8 characters, including letters, numbers, and special characters
        const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return passwordPattern.test(password);
    }

    // Collect form values
    const fullname = document.querySelector('input[name="fullname"]').value.trim();
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value.trim();

    // Client-side validation
    if (!fullname) {
        alert("Full name is required.");
        return;
    }

    if (!validateEmail(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    if (!validatePassword(password)) {
        alert("Password must be at least 8 characters long and contain a mix of letters, numbers, and special characters.");
        return;
    }

    // If all validations pass, proceed with the request
    const formData = { fullname, email, password };

    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        alert(result.message || result.error);

    } catch (err) {
        console.error('Error:', err);
        alert('An error has occurred. Please try again.');
    }
});