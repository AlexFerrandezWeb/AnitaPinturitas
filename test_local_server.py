import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)

# Configuración básica
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')  # Usar clave de prueba

ALLOWED_COUNTRIES = ['ES']
CURRENCY = 'eur'
SUCCESS_URL = 'https://anitapinturitas.es/success'
CANCEL_URL = 'https://anitapinturitas.es/carrito.html'
IMAGEN_POR_DEFECTO = "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&crop=center"

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion():
    try:
        print("Recibida petición para crear sesión")
        data = request.get_json()
        carrito = data.get('carrito', [])

        line_items = []
        for producto in carrito:
            product_data = {
                'name': producto['nombre'],
                'images': []
            }

            imagen_url = producto.get('imagen')
            if imagen_url:
                if imagen_url.startswith('/'):
                    imagen_url = f"https://anitapinturitas.es{imagen_url}"
                elif not imagen_url.startswith('http'):
                    imagen_url = f"https://anitapinturitas.es/{imagen_url.lstrip('/')}"
                product_data['images'].append(imagen_url)
            else:
                product_data['images'].append(IMAGEN_POR_DEFECTO)

            line_items.append({
                'price_data': {
                    'currency': CURRENCY,
                    'product_data': product_data,
                    'unit_amount': int(float(producto['precio']) * 100),
                },
                'quantity': int(producto['cantidad']),
            })

        # Configuración MÍNIMA sin parámetros problemáticos
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
            shipping_address_collection={
                'allowed_countries': ALLOWED_COUNTRIES,
            },
            phone_number_collection={
                'enabled': True,
            },
            locale='es',
            billing_address_collection='required'
        )

        print(f"Sesión creada exitosamente: {session.id}")
        return jsonify({'id': session.id})

    except Exception as e:
        print(f"Error al crear sesión: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok', 'message': 'Servidor local funcionando correctamente'})

@app.route('/diagnostico', methods=['GET'])
def diagnostico():
    return jsonify({
        'version': 'LOCAL_TEST_v1.0',
        'fecha': '2025-01-27',
        'caracteristicas': [
            'Sin automatic_payment_methods',
            'Sin payment_method_types',
            'Configuración mínima',
            'Servidor local'
        ],
        'stripe_api_key': 'Configurada' if stripe.api_key else 'No configurada',
        'mensaje': 'Esta es la versión local de prueba'
    })

if __name__ == '__main__':
    print("Iniciando servidor local de prueba...")
    print(f"Clave de Stripe configurada: {'Sí' if stripe.api_key else 'No'}")
    app.run(host='0.0.0.0', port=5000, debug=True) 