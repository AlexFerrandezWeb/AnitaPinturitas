import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)

# Sustituye por tu clave secreta de Stripe (sk_test_... o sk_live_...)
stripe.api_key = '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'

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion():
    data = request.get_json()
    carrito = data.get('carrito', [])
    nombre = data.get('nombre', '')
    direccion = data.get('direccion', '')

    line_items = []
    for producto in carrito:
        line_items.append({
            'price_data': {
                'currency': 'eur',
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
            success_url='https://tusitio.com/success',
            cancel_url='https://tusitio.com/cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=4242, debug=True) 