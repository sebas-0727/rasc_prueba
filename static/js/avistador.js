document.addEventListener('DOMContentLoaded', function() {
    const registroForm = document.getElementById('registroForm');

    registroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        registrarAvistador();
    });

    async function registrarAvistador() {
        const nombres = document.getElementById('nombres').value;
        const ficha = document.getElementById('ficha').value;
        const correo = document.getElementById('correo').value;

        try {
            const response = await fetch('/registrar_avistador', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nombres, ficha, correo }),
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const data = await response.json();
                if (data.error) {
                    console.error('Error:', data.error);
                    // Aquí podrías mostrar un mensaje de error al usuario
                }
            }
        } catch (error) {
            console.error('Error en registrarAvistador:', error);
            // Aquí también puedes mostrar un mensaje de error al usuario
        }
    }
});
