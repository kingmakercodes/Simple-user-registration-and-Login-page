import {validateEmail, validatePassword} from "./validators.js";


document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent form submission


    // collect form values
    const fullname= document.querySelector('input[name="fullname"]').value.trim()
    const email= document.querySelector('input[name="email"]').value.trim()
    const password= document.querySelector('input[name="password"]').value.trim()

    // client-side validation
    if (!fullname) {
        alert('Name is required!');
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address!');
    }

    if (!validatePassword(password)) {
        alert('Password must be at least 8 characters long and a mix of letters, numbers and special characters.');
    }

    // if all validation pass, proceed with request
    const formData= {fullname, email, password};

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

    } catch (err) {  // errors to be handled properly
        console.error('Error:', err);
        alert('An error occurred. Please try again.');
    }
});