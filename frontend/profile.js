const profileInfo= document.querySelector('#profile-info');
const logoutBtn= document.querySelector('#logout-btn');

// function to fetch user profile information
async function fetchUserProfile(){
    const token= localStorage.getItem('token');

    if (!token){

        // redirect to login page if token is missing
        window.location.href= 'auth.html'
    }

    try {
        const response= await fetch('http://127.0.0.1:5000/profile', {
            method: 'GET',
            credentials: 'include', // include credentials (cookies)
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const result= await response.json();

        if (response.ok){

            // displays the user profile info. this preferably should be the user's dashboard html page or something
            profileInfo.innerHTML= `
                <p><strong>ID:</strong> ${result.id}</p>
                <p><strong>Full Name:</strong> ${result.fullname}</p>
                <p><strong>Email:</strong> ${result.email}</p>
            `;
        } else {
            profileInfo.textContent= result.error || 'Failed to fetch profile data.';
            window.location.href= 'auth.html';
        }
    } catch (err){
        console.log('Error:', err);
        profileInfo.textContent= 'An error occurred. Please try again later.';
    }
}

// logout button function
logoutBtn.addEventListener('click',async ()=> {
    // clear cookie on the backend and redirect to login page
    await fetch('http://127.0.0.1:5000/logout', {
        method: 'POST',
        credentials: 'include'
    });

    window.location.href= 'auth.html'
    alert('Signed out successfully!')
})

// fetch user profile on page load
fetchUserProfile();