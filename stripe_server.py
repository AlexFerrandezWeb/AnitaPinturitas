import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
from stripe_config import ALLOWED_COUNTRIES, SHIPPING_OPTIONS, SUCCESS_URL, CANCEL_URL, CURRENCY

app = Flask(__name__)
CORS(app)

# Sustituye por tu clave secreta de Stripe (sk_test_... o sk_live_...)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion():
    data = request.get_json()
    carrito = data.get('carrito', [])

    line_items = []
    for producto in carrito:
        line_items.append({
            'price_data': {
                'currency': CURRENCY,
                'product_data': {
                    'name': producto['nombre'],
                },
                'unit_amount': int(float(producto['precio']) * 100),
            },
            'quantity': int(producto['cantidad']),
        })

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
            # Configuración para mostrar información de envío
            shipping_options=SHIPPING_OPTIONS,
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=4242, debug=True) 