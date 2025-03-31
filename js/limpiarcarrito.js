// Función para limpiar el carrito y el localStorage
function clearCart() {
    // Eliminar los productos del carrito en localStorage
    localStorage.removeItem('cart');

    // Limpiar el contador visual del carrito
    updateCartCounter();

    // Actualizar la interfaz de usuario (vaciar el contenedor del carrito)
    updateCartUI();
}

// Función para actualizar la UI del carrito
function updateCartUI() {
    const cartContainer = document.getElementById('cart-product-container');
    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Limpiar el contenedor de productos (vaciar el carrito)
    cartContainer.innerHTML = '';

    // Si el carrito está vacío, mostrar un mensaje
    if (cart.length === 0) {
        cartContainer.innerHTML = '<br> <p class="nota">El carrito está vacío.</p>';
    } else {
        // Mostrar los productos en el carrito (si hay productos)
        cart.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('cart-item');
            productElement.innerHTML = `
                <div>${product.name}</div>
                <div>S/${product.price}</div>
                <div>${product.quantity}</div>
                <div>S/${(product.price * product.quantity).toFixed(2)}</div>
                <button class="remove-from-cart" data-id="${product.id}">Eliminar</button>
            `;
            cartContainer.appendChild(productElement);
        });

        // Añadir un evento para eliminar productos
        document.querySelectorAll('.remove-from-cart').forEach(button => {
            button.addEventListener('click', function() {
                const productId = button.getAttribute('data-id');
                removeProductFromCart(productId);
            });
        });
    }

    // Actualizar el resumen del carrito
    updateCartSummary();
}

// Función para actualizar el resumen del carrito (subtotales, total, etc.)
function updateCartSummary() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const subtotalElement = document.querySelector('.subtotal');
    const totalElement = document.querySelector('.total');
    
    let subtotal = 0;

    // Calcular el subtotal
    cart.forEach(product => {
        subtotal += product.price * product.quantity;
    });

    // Actualizar los elementos del resumen
    subtotalElement.textContent = `S/${subtotal.toFixed(2)}`;
    totalElement.textContent = `S/${(subtotal + 9.32).toFixed(2)}`; // Asumimos un costo de envío fijo de S/9.32
}

// Función para actualizar el contador del carrito
function updateCartCounter() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCounter = document.getElementById('cart-counter');
    
    // Calcular el total de productos en el carrito
    const totalItems = cart.reduce((total, product) => total + product.quantity, 0);

    // Actualizar el contador visual
    cartCounter.textContent = totalItems;
}

// Añadir el evento al botón de "Limpiar Carrito"
document.getElementById('clear-cart-btn').addEventListener('click', clearCart);
////////////////////////////////////////////////////////////////////////////////////
