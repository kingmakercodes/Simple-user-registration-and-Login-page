// Switching Forms
function switchToLogin() {
    document.getElementById('signup-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
}

function switchToSignUp() {
    document.getElementById('signup-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
}

document.getElementById('signup-form').addEventListener('submit', async function(e){
    e.preventDefault();

    // Collect signup form values
    const fullname= document.querySelector('#signup-form input[name="fullname"]').value.trim();
    const email= document.querySelector('#signup-form input[name="email"]').value.trim();
    const password= document.querySelector('#signup-form input[name="password"]').value.trim();

    // Simple validation for signup forms
    if (!fullname) {
        alert('Name field is empty!');
        return;
    }
    if (!email) {
        alert('Email field empty!');
        return;
        // pass in logic to handle checking of valid real world email addresses here
    }
    if (!password) {
        alert('Password field is empty!');
        return;
    }

    // Proceed with network request for signup
    const formData= {fullname, email, password};

    try{
        const response= await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(formData)
        });
        
        const result= await response.json();
        alert(result.message || result.error);

    } catch (err) {
        console.error('Error:', err);
        alert('An error has occurred. Please try again!');
    }

});

// Event Listener for Login Form
document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    // Collect form values
    const email = document.querySelector('#login-form input[name="email"]').value.trim();
    const password = document.querySelector('#login-form input[name="password"]').value.trim();

    // Simple validation for login form
    if (!email) {
        alert("Email is required.");
        return;
    }
    if (!password) {
        alert("Password is required.");
        return;
    }

    // Proceed with network request for login
    const formData = { email, password };

    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
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
