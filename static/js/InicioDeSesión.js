function togglePasswordVisibility() {
    const passwordField = document.getElementById("password");
    const eyeIcon = document.querySelector(".toggle-password");

    if (passwordField.type === "password") {
        passwordField.type = "text"; // Muestra la contraseña
        eyeIcon.src = "/img/ojo 2.png"; // Cambia la imagen del ojo (ajusta la ruta)
    } else {
        passwordField.type = "password"; // Oculta la contraseña
        eyeIcon.src = "/img/ojo (3).png"; // Cambia la imagen del ojo (ajusta la ruta)
    }
}




// Función para redirigir al usuario a otra página
function redirectToPage() {
    // Redirigir a la página que desees
    window.location.href = "index.html";  // Aquí reemplazas con la URL del destino
}



