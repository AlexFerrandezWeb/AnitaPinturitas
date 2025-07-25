import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
from stripe_config import ALLOWED_COUNTRIES, SHIPPING_OPTIONS, SUCCESS_URL, CANCEL_URL, CURRENCY

app = Flask(__name__)
CORS(app)

# Sustituye por tu clave secreta de Stripe (sk_test_... o sk_live_...)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def convertir_imagen_a_url_absoluta(imagen_path):
    """
    Convierte una ruta relativa de imagen en una URL absoluta para Stripe.
    """
    # URL base de tu sitio web
    base_url = "https://anitapinturitas.es"
    
    # Si la imagen ya es una URL completa, la devolvemos tal como está
    if imagen_path.startswith('http'):
        return imagen_path
    
    # Si es una ruta relativa, la convertimos en URL absoluta
    if imagen_path.startswith('/'):
        return base_url + imagen_path
    else:
        return base_url + '/' + imagen_path

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion():
    data = request.get_json()
    carrito = data.get('carrito', [])

    # Calcular el subtotal del pedido
    subtotal = sum(float(producto['precio']) * int(producto['cantidad']) for producto in carrito)
    
    # Determinar si el envío es gratuito (pedidos de 62€ o más)
    envio_gratuito = subtotal >= 62
    
    line_items = []
    for producto in carrito:
        # Convertir la imagen a URL absoluta para Stripe
        imagen_url = convertir_imagen_a_url_absoluta(producto['imagen'])
        
        line_items.append({
            'price_data': {
                'currency': CURRENCY,
                'product_data': {
                    'name': producto['nombre'],
                    'images': [imagen_url],  # Añadir imagen del producto
                },
                'unit_amount': int(float(producto['precio']) * 100),
            },
            'quantity': int(producto['cantidad']),
        })

    # Configurar opciones de envío dinámicamente
    shipping_options = []
    if not envio_gratuito:
        shipping_options = SHIPPING_OPTIONS

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
            # Configuración para solicitar dirección de envío
            shipping_address_collection={
                'allowed_countries': ALLOWED_COUNTRIES,
            },
            # Configuración para solicitar información del cliente
            customer_email=None,  # Stripe pedirá el email automáticamente
            # Configuración para solicitar número de teléfono
            phone_number_collection={
                'enabled': True,
            },
            # Configuración para mostrar información de envío (solo si no es gratuito)
            shipping_options=shipping_options,
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=4242, debug=True) 