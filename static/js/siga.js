document.addEventListener('DOMContentLoaded', function () {
    // Manejo del formulario de registro SIGA
    const sigaForm = document.getElementById('sigaForm');
    sigaForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(sigaForm);
        const data = Object.fromEntries(formData);

        fetch('/registrar_siga', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else if (data.mensaje) {
                alert(data.mensaje);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Manejo del formulario de inicio de sesión
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const nombre = document.getElementById('loginNombre').value;
        const contraseña = document.getElementById('loginContraseña').value;

        fetch('/iniciar_sesion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nombre, contraseña })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje === 'Inicio de sesión exitoso') {
                alert("Acceso permitido. Bienvenido!");
                window.location.href = '/reptiles';
            } else {
                alert(data.mensaje);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error al iniciar sesión");
        });
    });

    // Configuración de los botones para mostrar/ocultar las contraseñas
    const toggleButtons = document.querySelectorAll('.password-toggle');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = this.previousElementSibling;
            const toggleIcon = this.querySelector('i');
            togglePassword(passwordField, toggleIcon);
        });
    });
});

function togglePassword(passwordField, toggleIcon) {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('bi-eye');
        toggleIcon.classList.add('bi-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('bi-eye-slash');
        toggleIcon.classList.add('bi-eye');
    }
}