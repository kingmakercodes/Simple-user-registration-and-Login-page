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
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const result= await response.json();

        if (response.ok){

            // display the user profile info
            profileInfo.innerHTML= `
                <p><strong>ID:</strong> ${result.id}</p>
                <p><strong>Full Name:</strong> ${result.fullname}</p>
                <p><strong>Email:</strong> ${result.email}</p>
            `;
        } else {
            profileInfo.textContent= result.error || 'Failed to fetch profile data.';
            localStorage.removeItem('token');
            window.location.href= 'auth.html';
        }
    } catch (err){
        console.log('Error:', err);
        profileInfo.textContent= 'An error occurred. Please try again later.';
    }
}

// logout button function
logoutBtn.addEventListener('click', ()=> {
    localStorage.removeItem('token');
    window.location.href= 'auth.html'                       // to rewrite login page separately and connect these to it
    alert('Signed out successfully!')
})

// fetch user profile on page load