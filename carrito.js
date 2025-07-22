// Clave pública de Stripe (¡reemplázala por la tuya!)
const stripe = Stripe('pk_live_51RiBJlAV1sSXblTcz3sH2w36Nd753TcxPOGaRFdj1qKLi1EfDqd3N6S1zXq8RTRVQgxv3SBT31uW3kmDKxZG1t6A00vdarrbHY');

// --- FUNCIONES DEL CARRITO ---

/**
 * Actualiza el número que se muestra en el icono del carrito en la navegación.
 */
function actualizarContadorCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const totalItems = carrito.reduce((total, producto) => total + (producto.cantidad || 0), 0);
    
    document.querySelectorAll('.carrito-cantidad').forEach(contador => {
        if (contador) {
            contador.textContent = totalItems;
        }
    });
}

/**
 * Renderiza los productos del carrito en la página y actualiza el resumen.
 */
function cargarCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const carritoProductos = document.getElementById('carrito-productos');
    const carritoVacio = document.getElementById('carrito-vacio');
    const carritoContenedor = document.querySelector('.carrito-contenedor');

    if (!carritoContenedor || !carritoProductos || !carritoVacio) return;

    if (carrito.length === 0) {
        carritoVacio.style.display = 'flex';
        carritoContenedor.style.display = 'none';
    } else {
        carritoVacio.style.display = 'none';
        carritoContenedor.style.display = 'grid';
        
        carritoProductos.innerHTML = '';
        let subtotal = 0;

        carrito.forEach((producto, index) => {
            const precio = parseFloat(producto.precio) || 0;
            const cantidad = parseInt(producto.cantidad) || 0;
            subtotal += precio * cantidad;

            carritoProductos.innerHTML += `
                <div class="producto-carrito">
                    <img src="${producto.imagen}" alt="${producto.nombre}" onerror="this.src='/assets/placeholder.jpg';">
                    <div class="producto-info">
                        <h3>${producto.nombre}</h3>
                        <p class="producto-precio">${precio.toFixed(2)} €</p>
                        <div class="cantidad-controls">
                            <button class="btn-cantidad" onclick="actualizarCantidad(${index}, -1)" aria-label="Disminuir cantidad">-</button>
                            <span>${cantidad}</span>
                            <button class="btn-cantidad" onclick="actualizarCantidad(${index}, 1)" aria-label="Aumentar cantidad">+</button>
                        </div>
                    </div>
                    <button class="btn-eliminar" onclick="eliminarProducto(${index})" aria-label="Eliminar producto">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
        });

        actualizarResumen(subtotal);
    }

    actualizarContadorCarrito();
    habilitarBotonPago();
}

/**
 * Actualiza la cantidad de un producto en el carrito.
 * @param {number} index - El índice del producto en el array del carrito.
 * @param {number} cambio - El cambio a aplicar en la cantidad (+1 o -1).
 */
function actualizarCantidad(index, cambio) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    if (carrito[index]) {
        carrito[index].cantidad = Math.max(1, (parseInt(carrito[index].cantidad, 10) || 0) + cambio);
        localStorage.setItem('carrito', JSON.stringify(carrito));
        cargarCarrito();
    }
}

/**
 * Elimina un producto del carrito.
 * @param {number} index - El índice del producto a eliminar.
 */
function eliminarProducto(index) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito.splice(index, 1);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    cargarCarrito();
}

/**
 * Actualiza el resumen del pedido (subtotal, envío y total).
 * @param {number} subtotal - El subtotal de los productos.
 */
function actualizarResumen(subtotal) {
    const envio = subtotal > 50 ? 0 : 5.99;
    const total = subtotal + envio;

    document.getElementById('subtotal').textContent = `${subtotal.toFixed(2)} €`;
    document.getElementById('envio').textContent = `${envio.toFixed(2)} €`;
    document.getElementById('total').textContent = `${total.toFixed(2)} €`;
}

/**
 * Habilita o deshabilita el botón de "Proceder al Pago" según si hay productos.
 */
function habilitarBotonPago() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const btnComprar = document.getElementById('btn-comprar');
    if (btnComprar) {
        if (carrito.length > 0) {
            btnComprar.disabled = false;
            btnComprar.style.opacity = '1';
            btnComprar.style.cursor = 'pointer';
        } else {
            btnComprar.disabled = true;
            btnComprar.style.opacity = '0.5';
            btnComprar.style.cursor = 'not-allowed';
        }
    }
}

// --- LÓGICA DE PAGO CON STRIPE ---

/**
 * Procesa el pago llamando al backend para crear una sesión de Stripe Checkout.
 */
async function procesarPagoConStripe() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    
    // Aquí puedes añadir campos si quieres recoger más datos, como nombre y dirección
    const nombreCliente = "Cliente"; // Opcional: obtener de un input
    const direccionCliente = "Sin dirección"; // Opcional: obtener de un input

    if (carrito.length === 0) {
        alert("Tu carrito está vacío.");
        return;
    }

    try {
        const response = await fetch('https://anita-pinturitas-server.onrender.com/crear-sesion', { // Asegúrate que la URL es correcta
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                carrito: carrito,
                nombre: nombreCliente,
                direccion: direccionCliente
            })
        });

        const data = await response.json();

        if (response.ok && data.id) {
            // Redirigir a la página de pago de Stripe
            await stripe.redirectToCheckout({ sessionId: data.id });
        } else {
            console.error('Error al crear la sesión de pago:', data.error);
            alert(`Error al procesar el pago: ${data.error || 'Error desconocido del servidor.'}`);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        alert('No se pudo conectar con el servidor de pagos. Revisa tu conexión o inténtalo más tarde.');
    }
}


// --- EVENT LISTENERS ---

document.addEventListener('DOMContentLoaded', () => {
    // Cargar el carrito en cuanto la página esté lista
    if (document.getElementById('carrito-productos')) {
        cargarCarrito();
    }
    
    // Listener para el botón principal de pago
    const btnComprar = document.getElementById('btn-comprar');
    if (btnComprar) {
        btnComprar.addEventListener('click', (evento) => {
            evento.preventDefault(); // Prevenir cualquier acción por defecto
            procesarPagoConStripe();
        });
    }

    // Actualizar contador en toda la web si otra pestaña modifica el carrito
    window.addEventListener('storage', (e) => {
        if (e.key === 'carrito') {
            actualizarContadorCarrito();
            // Si estamos en la página del carrito, la recargamos para ver cambios
            if (document.getElementById('carrito-productos')) {
                cargarCarrito();
            }
        }
    });
    
    // Asegurarse de que el contador esté siempre actualizado al cargar cualquier página
    actualizarContadorCarrito();
});
