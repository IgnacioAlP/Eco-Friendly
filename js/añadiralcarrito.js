// Seleccionar el botón "Añadir al carrito" 
const addToCartButtons = document.querySelectorAll('.add-to-cart');

addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Obtener los datos del producto desde los atributos del botón
        const product = {
            id: button.dataset.id,
            vendor: button.dataset.vendor, // Información del vendedor
            name: button.dataset.name,
            price: parseFloat(button.dataset.price), // Asegurarse de que el precio sea un número
            quantity: 1, // Al añadir al carrito, por defecto se pone una cantidad de 1
            subtotal: parseFloat(button.dataset.price), // El subtotal inicial es igual al precio
            image: button.parentElement.querySelector('img').src // Obtener la URL de la imagen
        };

        // Verificar que el precio es un número válido
        if (isNaN(product.price)) {
            alert('El precio del producto no es válido.');
            return;
        }

        // Recuperar el carrito desde el localStorage o inicializar uno vacío
        const cart = JSON.parse(localStorage.getItem('cart')) || [];

        // Verificar si el producto ya está en el carrito
        const existingProductIndex = cart.findIndex(item => item.id === product.id);

        if (existingProductIndex >= 0) {
            // Si el producto ya está en el carrito, actualizar la cantidad y el subtotal
            cart[existingProductIndex].quantity += 1;
            cart[existingProductIndex].subtotal = cart[existingProductIndex].price * cart[existingProductIndex].quantity;  // Actualizar el subtotal
        } else {
            // Si el producto no está en el carrito, añadirlo
            cart.push(product);
        }

        // Guardar el carrito actualizado en el localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Actualizar el contador del carrito
        updateCartCounter();

        // Opcional: Puedes mostrar un mensaje o actualizar el icono del carrito
        alert('Producto añadido al carrito');
    });
});

// Función para actualizar el contador del carrito
function updateCartCounter() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCounter = document.getElementById('cart-counter');
    
    // Calcular el total de productos en el carrito
    const totalItems = cart.reduce((total, product) => total + product.quantity, 0);

    // Actualizar el contador visual
    cartCounter.textContent = totalItems;
}

// Llamar a la función para actualizar el contador al cargar la página
window.addEventListener('load', () => {
    updateCartCounter();

    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartProductContainer = document.getElementById('cart-product-container');
    const subtotalElement = document.querySelector('.subtotal');
    const totalElement = document.querySelector('.total');

    cartProductContainer.innerHTML = ''; // Limpiar el contenedor

    let subtotal = 0;

    cart.forEach(product => {
        // Crear una fila para cada producto en el carrito
        const productRow = document.createElement('div');
        productRow.classList.add('row');
        
        productRow.innerHTML = `
            <div class="col-1 esp"></div>
            <div class="col-5 produ">
                <div class="row">
                    <div class="col-4 imgcarrito">
                        <img src="${product.image}" alt="${product.name}"/>
                    </div>
                    <div class="col-7">
                        <br>
                        <p class="desc1">${product.name}</p>
                        <p class="desc2">Vendido por: ${product.vendor}</p>
                    </div>
                </div>
            </div>
            <div class="col-2 produ">
                <br>
                <br>
                <label class="oval-label">S/ ${(product.price).toFixed(2)}</label>
            </div>
            <div class="col-2 produ">
                <br>
                <br>
                <div class="mb-3">
                    <div class="input-group">
                        <button class="btn btn-outline-secondary decrease-quantity" type="button" data-id="${product.id}">-</button>
                        <input type="number" class="form-control text-center product-quantity" value="${product.quantity}" min="1" max="100" id="productQuantity-${product.id}" data-id="${product.id}" disabled>
                        <button class="btn btn-outline-secondary increase-quantity" type="button" data-id="${product.id}">+</button>
                    </div>
                </div>
            </div>
            <div class="col-2 produ">
                <br>
                <br>
                <label class="oval-label" id="subtotal-${product.id}">S/ ${(product.price * product.quantity).toFixed(2)}</label>
            </div>
        `;

        // Añadir la fila al contenedor
        cartProductContainer.appendChild(productRow);

        // Sumar el subtotal
        subtotal += product.price * product.quantity;
    });

    // Actualizar el subtotal y total
    subtotalElement.textContent = `S/${subtotal.toFixed(2)}`;
    totalElement.textContent = `S/${(subtotal + 9.32).toFixed(2)}`; // Agregar el costo de envío (S/9.32)

    // Reestablecer los event listeners de los botones
    resetQuantityButtons();
});

// Función para actualizar la cantidad de un producto en el carrito
function updateQuantity(productId, change) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const productIndex = cart.findIndex(product => product.id === productId);

    if (productIndex >= 0) {
        const product = cart[productIndex];

        // Cambiar la cantidad (no permitir cantidades menores a 1)
        product.quantity += change;

        // Si la cantidad es menor que 1, restablecerla a 1 (no permitir valores menores)
        if (product.quantity < 1) {
            product.quantity = 1;
        }

        // Actualizar el subtotal
        product.subtotal = product.price * product.quantity;

        // Guardar el carrito actualizado en el localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Actualizar la UI: input, contador, resumen y subtotal del producto
        updateCartCounter();
        updateCartSummary();
        updateProductQuantityInput(productId, product.quantity); // Actualizar el input con la nueva cantidad
        updateProductSubtotal(productId, product.subtotal); // Actualizar el subtotal del producto
    }
}

// Función para actualizar el subtotal visualmente en la UI
function updateProductSubtotal(productId, subtotal) {
    const subtotalElement = document.getElementById(`subtotal-${productId}`);
    if (subtotalElement) {
        subtotalElement.textContent = `S/ ${subtotal.toFixed(2)}`;
    }
}

// Función para actualizar la UI del input de cantidad
function updateProductQuantityInput(productId, quantity) {
    const quantityInput = document.querySelector(`#productQuantity-${productId}`);
    if (quantityInput) {
        quantityInput.value = quantity;
    }
}

// Aumentar cantidad
function resetQuantityButtons() {
    // Asegurarse de que los botones de aumentar y disminuir se reinicien
    document.querySelectorAll('.increase-quantity').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            updateQuantity(productId, 1); // Aumentar cantidad
        });
    });

    document.querySelectorAll('.decrease-quantity').forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-id');
            updateQuantity(productId, -1); // Disminuir cantidad
        });
    });
}

// Función para eliminar producto
document.querySelectorAll('.remove-product').forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.getAttribute('data-id');
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const productIndex = cart.findIndex(product => product.id === productId);

        if (productIndex >= 0) {
            cart.splice(productIndex, 1);
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartCounter();
            updateCartSummary();
            updateCartUI();
        }
    });
});

// Función para actualizar el resumen del carrito (subtotal, total)
function updateCartSummary() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    let subtotal = 0;

    // Calcular el subtotal
    cart.forEach(product => {
        subtotal += product.price * product.quantity;
    });

    const subtotalElement = document.querySelector('.subtotal');
    const totalElement = document.querySelector('.total');
    
    subtotalElement.textContent = `S/${subtotal.toFixed(2)}`;
    totalElement.textContent = `S/${(subtotal + 9.32).toFixed(2)}`; // Agregar el costo de envío (S/9.32)
}

// Seleccionar todos los botones de "Añadir al carrito"


addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Obtener los datos del producto desde los atributos del botón
        const product = {
            id: button.dataset.id,
            name: button.dataset.name,
            price: parseFloat(button.dataset.price), // Convertir a número
            vendor: button.dataset.vendor,
            quantity: 1, // Se agrega un producto por defecto
            subtotal: parseFloat(button.dataset.price), // El subtotal es igual al precio al principio
            image: button.closest('.card').querySelector('img').src // Obtener la URL de la imagen del producto
        };

        // Verificar que el precio es un número válido
        if (isNaN(product.price)) {
            alert('El precio del producto no es válido.');
            return;
        }

        // Recuperar el carrito desde localStorage (si existe)
        let cart = JSON.parse(localStorage.getItem('cart')) || [];

        // Verificar si el producto ya existe en el carrito
        const existingProductIndex = cart.findIndex(item => item.id === product.id);

        if (existingProductIndex >= 0) {
            // Si el producto ya está en el carrito, solo se incrementa la cantidad
            cart[existingProductIndex].quantity += 1;
            cart[existingProductIndex].subtotal = cart[existingProductIndex].price * cart[existingProductIndex].quantity; // Actualiza el subtotal
        } else {
            // Si el producto no está en el carrito, lo añadimos
            cart.push(product);
        }

        // Guardar el carrito actualizado en localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Actualizar el contador del carrito
        updateCartCounter();

        // Mostrar mensaje de que el producto fue añadido
        alert('Producto añadido al carrito');
    });
});

// Función para actualizar el contador del carrito
function updateCartCounter() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCounter = document.getElementById('cart-counter');

    // Calcular el número total de productos en el carrito
    const totalItems = cart.reduce((total, product) => total + product.quantity, 0);

    // Actualizar el contador en la interfaz
    cartCounter.textContent = totalItems;
}

// Llamar a la función para actualizar el contador al cargar la página
window.addEventListener('load', () => {
    updateCartCounter();
});
//-----------------detalle_ prouducto----------------


// Función que se ejecuta cuando se hace clic en "Añadir al carrito"
document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        // Obtener los datos del producto
        const productId = this.getAttribute('data-id');
        const productName = this.getAttribute('data-name');
        const productPrice = this.getAttribute('data-price');
        const productVendor = this.getAttribute('data-vendor');

        // Crear un objeto con los datos del producto
        const product = {
            id: productId,
            name: productName,
            price: parseFloat(productPrice),
            vendor: productVendor,
            quantity: 1 // Por defecto, la cantidad es 1
        };

        // Obtener el carrito actual desde localStorage (o crear uno nuevo si no existe)
        let cart = JSON.parse(localStorage.getItem('cart')) || [];

        // Verificar si el producto ya está en el carrito
        const existingProductIndex = cart.findIndex(item => item.id === product.id);

        if (existingProductIndex >= 0) {
            // Si el producto ya está en el carrito, incrementamos la cantidad
            cart[existingProductIndex].quantity += 1;
        } else {
            // Si no está en el carrito, lo agregamos
            cart.push(product);
        }

        // Guardar el carrito actualizado en localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Actualizar el contador del carrito
        updateCartCounter();
        
        // Mostrar mensaje de éxito
        alert('Producto añadido al carrito');
    });
});

// Función para actualizar el contador del carrito
function updateCartCounter() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCounter = document.getElementById('cart-counter');
    cartCounter.textContent = cart.reduce((total, product) => total + product.quantity, 0); // Sumar todas las cantidades
}

window.addEventListener('load', function() {
    // Obtener el carrito desde localStorage
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Si el carrito está vacío
    if (cart.length === 0) {
        document.getElementById('cart-items').innerHTML = '<p>No hay productos en el carrito.</p>';
        return;
    }

    // Obtener el contenedor donde se mostrarán los productos
    const cartContainer = document.getElementById('cart-items');
    cartContainer.innerHTML = ''; // Limpiar el contenido anterior

    // Recorrer los productos en el carrito y mostrarlos
    cart.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('cart-item');
        productElement.innerHTML = `
            <h3>${product.name}</h3>
            <p>Precio: S/${product.price}</p>
            <p>Cantidad: ${product.quantity}</p>
            <button class="remove-btn" data-id="${product.id}">Eliminar</button>
        `;
        cartContainer.appendChild(productElement);
    });

    // Actualizar el total del carrito
    updateCartTotal(cart);
    
    // Añadir eventos para eliminar productos del carrito
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
            removeProductFromCart(this.getAttribute('data-id'));
        });
    });
});

// Función para actualizar el total del carrito
function updateCartTotal(cart) {
    const totalElement = document.getElementById('cart-total');
    const total = cart.reduce((sum, product) => sum + (product.price * product.quantity), 0);
    totalElement.textContent = 'Total: S/' + total.toFixed(2);
}

// Función para eliminar un producto del carrito
function removeProductFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Filtrar el carrito para eliminar el producto con el id especificado
    cart = cart.filter(product => product.id !== productId);
    
    // Guardar el carrito actualizado en localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Recargar la página para mostrar los cambios
    window.location.reload();
}
// Función que se ejecuta cuando se hace clic en "Añadir al carrito"
document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        // Obtener los datos del producto
        const productId = this.getAttribute('data-id');
        const productName = this.getAttribute('data-name');
        const productPrice = this.getAttribute('data-price');
        const productVendor = this.getAttribute('data-vendor');
        const productImage = this.closest('.product').querySelector('img').src; // Obtener la imagen del producto

        // Crear un objeto con los datos del producto
        const product = {
            id: productId,
            name: productName,
            price: parseFloat(productPrice),
            vendor: productVendor,
            image: productImage, // Añadir la imagen al objeto
            quantity: 1 // Por defecto, la cantidad es 1
        };

        // Obtener el carrito actual desde localStorage (o crear uno nuevo si no existe)
        let cart = JSON.parse(localStorage.getItem('cart')) || [];

        // Verificar si el producto ya está en el carrito
        const existingProductIndex = cart.findIndex(item => item.id === product.id);

        if (existingProductIndex >= 0) {
            // Si el producto ya está en el carrito, incrementamos la cantidad
            cart[existingProductIndex].quantity += 1;
        } else {
            // Si no está en el carrito, lo agregamos
            cart.push(product);
        }

        // Guardar el carrito actualizado en localStorage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Actualizar el contador del carrito
        updateCartCounter();
        
        // Mostrar mensaje de éxito
        alert('Producto añadido al carrito');
    });
});

// Función para actualizar el contador del carrito
function updateCartCounter() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCounter = document.getElementById('cart-counter');
    cartCounter.textContent = cart.reduce((total, product) => total + product.quantity, 0); // Sumar todas las cantidades
}

window.addEventListener('load', function() {
    // Obtener el carrito desde localStorage
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Si el carrito está vacío
    if (cart.length === 0) {
        document.getElementById('cart-items').innerHTML = '<p>No hay productos en el carrito.</p>';
        return;
    }

    // Obtener el contenedor donde se mostrarán los productos
    const cartContainer = document.getElementById('cart-items');
    cartContainer.innerHTML = ''; // Limpiar el contenido anterior

    // Recorrer los productos en el carrito y mostrarlos
    cart.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('cart-item');
        productElement.innerHTML = `
            <div class="cart-item-image">
                <img src="${product.image}" alt="${product.name}"> <!-- Mostrar la imagen -->
            </div>
            <div class="cart-item-info">
                <h3>${product.name}</h3>
                <p>Precio: S/${product.price}</p>
                <p>Cantidad: ${product.quantity}</p>
                <button class="remove-btn" data-id="${product.id}">Eliminar</button>
            </div>
        `;
        cartContainer.appendChild(productElement);
    });

    // Actualizar el total del carrito
    updateCartTotal(cart);
    
    // Añadir eventos para eliminar productos del carrito
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
            removeProductFromCart(this.getAttribute('data-id'));
        });
    });
});

// Función para actualizar el total del carrito
function updateCartTotal(cart) {
    const totalElement = document.getElementById('cart-total');
    const total = cart.reduce((sum, product) => sum + (product.price * product.quantity), 0);
    totalElement.textContent = 'Total: S/' + total.toFixed(2);
    
}

// Función para eliminar un producto del carrito
function removeProductFromCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Filtrar el carrito para eliminar el producto con el id especificado
    cart = cart.filter(product => product.id !== productId);
    
    // Guardar el carrito actualizado en localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Recargar la página para mostrar los cambios
    window.location.reload();
}
///////confirmaciom 


 // Función para cargar los productos del carrito y actualizar la tabla de resumen
function updateCartSummary() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const tableBody = document.querySelector('#order-summary-table tbody');
    const totalPriceElement = document.querySelector('#total-price');
    let total = 0;

    tableBody.innerHTML = ''; // Limpiar tabla

    cart.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.name} (${product.quantity} x S/${product.price})</td>
            <td>S/${(product.price * product.quantity).toFixed(2)}</td>
        `;
        tableBody.appendChild(row);
        total += product.price * product.quantity;
    });

    // Sumar el costo de envío (S/ 9.32) al total
    const shippingCost = 9.32;
    total += shippingCost;

    // Mostrar el total final (con envío incluido)
    totalPriceElement.textContent = `S/${total.toFixed(2)}`;

    // Mostrar costo de envío en el resumen (opcional)
    const shippingRow = document.querySelector('#shipping-cost-row');
    if (shippingRow) {
        shippingRow.querySelector('.cost').textContent = `S/${shippingCost.toFixed(2)}`;
    } else {
        // Si no existe la fila de envío, agregarla dinámicamente
        const newRow = document.createElement('tr');
        newRow.id = 'shipping-cost-row';
        newRow.innerHTML = `
            <td><strong>Costo de envío</strong></td>
            <td class="cost">S/${shippingCost.toFixed(2)}</td>
        `;
        tableBody.appendChild(newRow);
    }

    // Activar el botón de finalizar compra si el carrito no está vacío
    const finalizeButton = document.querySelector('#finalize-btn');
    finalizeButton.disabled = cart.length === 0;
}

// Validación del formulario de facturación (Datos personales)
function validateBillingForm() {
    const form = document.querySelector('#billing-form');
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;

    // Limpiar los bordes de los campos
    inputs.forEach(input => {
        input.style.border = ''; // Eliminar cualquier borde rojo previo
    });

    // Verificar si todos los campos requeridos están llenos
    inputs.forEach(input => {
        if (input.value.trim() === '') {
            isValid = false;
        }
    });

    return isValid;
}

// Función para finalizar la compra
function finalizePurchase() {
    const paymentMethod = document.querySelector('input[name="payment-method"]:checked');
    const personalDetailsValid = validateBillingForm(); // Validar datos personales

    // Verificar si se ha seleccionado un medio de pago
    if (!paymentMethod) {
        alert('Por favor, selecciona un medio de pago para continuar.');
        return;
    }

    // Verificar si el formulario de facturación (datos personales) es válido
    if (!personalDetailsValid) {
        // Si no es válido, marcar los campos vacíos con borde rojo
        const form = document.querySelector('#billing-form');
        const inputs = form.querySelectorAll('input[required]');

        inputs.forEach(input => {
            if (input.value.trim() === '') {
                input.style.border = '2px solid red'; // Marcar los campos vacíos
            }
        });

        alert('Por favor, completa todos los campos del formulario de facturación.');
        return;
    }

    // Mostrar el modal de compra exitosa
    showSuccessModal();
}

// Mostrar el modal de compra exitosa
function showSuccessModal() {
    const modal = document.getElementById('success-modal');
    modal.style.display = 'flex'; // Mostrar el modal
}

// Cerrar el modal
function closeModal() {
    const modal = document.getElementById('success-modal');
    modal.style.display = 'none'; // Ocultar el modal
}

// Asignar eventos al botón de cerrar y al botón "Aceptar" del modal
document.getElementById('close-modal').addEventListener('click', closeModal);
document.getElementById('ok-btn').addEventListener('click', closeModal);

// Asignar evento al botón de finalizar compra
document.querySelector('#finalize-btn').addEventListener('click', finalizePurchase);

// Cargar carrito al cargar la página
window.onload = function() {
    updateCartSummary();
    validateBillingForm(); // Validar al cargar la página
};


//



