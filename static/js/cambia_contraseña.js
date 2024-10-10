document.addEventListener('DOMContentLoaded', function() {
    const cambiarContraseñaForm = document.getElementById('cambiarContraseñaForm');

    if (cambiarContraseñaForm) {
        cambiarContraseñaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            actualizarContraseña();
        });
    }
});

function actualizarContraseña() {
    const correo = document.getElementById('correoActualizar').value;
    const nuevaContraseña = document.getElementById('nuevaContraseña').value;

    if (correo && nuevaContraseña) {
        fetch('/cambiar_contraseña', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                correo: correo,
                nueva_contraseña: nuevaContraseña
            })
        })
        .then(response => response.json())
        .then(data => {
            const resultadoDiv = document.getElementById('resultado');
            if (data.mensaje) {
                resultadoDiv.textContent = data.mensaje;
                resultadoDiv.className = data.mensaje === 'Contraseña actualizada correctamente' ? 'alert alert-success' : 'alert alert-danger';
                if (data.mensaje === 'Contraseña actualizada correctamente') {
                    setTimeout(() => {
                        window.location.href = '/inicio_siga'; }, 2000);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const resultadoDiv = document.getElementById('resultado');
            resultadoDiv.textContent = "Error al cambiar la contraseña";
            resultadoDiv.className = 'alert alert-danger';
        });
    } else {
        alert("Por favor, ingrese todos los campos!");
    }
}
