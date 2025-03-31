// Esperar a que el documento esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los botones "Añadir al carrito"
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    // Obtener el contador del carrito
    const cartCounter = document.getElementById('cart-counter');
    
    // Verificar si hay un valor guardado en localStorage para el contador
    let cartCount = parseInt(localStorage.getItem('cartCount')) || 0;
    
    // Mostrar el valor inicial del contador
    cartCounter.textContent = cartCount;

    // Función para actualizar el contador en el carrito
    function updateCartCount() {
        cartCount += 1; // Aumentamos el contador
        localStorage.setItem('cartCount', cartCount); // Guardamos el nuevo valor en localStorage
        cartCounter.textContent = cartCount; // Actualizamos el contador en el DOM
    }

    // Añadir un evento de clic a cada botón "Añadir al carrito"
  
});



       // Función para actualizar el contador del carrito
       function updateCartCounter(count) {
        document.getElementById('cart-counter').textContent = count;
    }

    // Evento cuando se hace clic en el botón de limpiar carrito
    document.getElementById('clear-cart-btn').addEventListener('click', function() {
        // Reiniciar el contador del carrito a 0
        updateCartCounter(0);

        // Opcional: Aquí también puedes limpiar el carrito en localStorage o donde sea que lo guardes
        // localStorage.removeItem('cart'); // Si usas localStorage para el carrito
    });