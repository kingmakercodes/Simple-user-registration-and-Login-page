document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent form submission

    const formData = {
        fname: document.querySelector('input[name="fname"]').value,
        email: document.querySelector('input[name="email"]').value,
        password: document.querySelector('input[name="password"]').value
    };

    try {
        const response = await fetch('/signup', {
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
        alert('An error occurred. Please try again.');
    }
});