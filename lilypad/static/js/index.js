let username_input = document.getElementById('username');
let password_input = document.getElementById('password');
let email_input = document.getElementById('email');
let submit_button = document.getElementById('submit');

document.addEventListener('DOMContentLoaded', function() {
    submit_button.addEventListener('click', function() {
        let username = username_input.value;
        let password = password_input.value;
        let email = email_input.value;
        let data = {
            username: username,
            password: password,
            email: email
        };
        fetch('/api/register', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(response) {
            if (response.status === 200) {
                window.location.href = '/browse';
            } else {
                alert('Invalid Credentials!');
            }
        });
    });
});