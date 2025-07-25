import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)

# Configuración directa sin archivo externo para simplificar
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Configuración simplificada
ALLOWED_COUNTRIES = ['ES']
CURRENCY = 'eur'
SUCCESS_URL = 'https://anitapinturitas.es/success'
CANCEL_URL = 'https://anitapinturitas.es/carrito.html'

SHIPPING_OPTIONS = [
    {
        'shipping_rate_data': {
            'type': 'fixed_amount',
            'fixed_amount': {
                'amount': 695,  # 6.95€ en centavos
                'currency': 'eur',
            },
            'display_name': 'Envío estándar',
            'delivery_estimate': {
                'minimum': {
                    'unit': 'business_day',
                    'value': 3,
                },
                'maximum': {
                    'unit': 'business_day',
                    'value': 5,
                },
            },
        },
    },
]

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion():
    try:
        print("Recibida petición para crear sesión")
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        carrito = data.get('carrito', [])
        print(f"Carrito: {carrito}")

        # Calcular el subtotal del pedido
        subtotal = sum(float(producto['precio']) * int(producto['cantidad']) for producto in carrito)
        print(f"Subtotal: {subtotal}")
        
        # Determinar si el envío es gratuito (pedidos de 62€ o más)
        envio_gratuito = subtotal >= 62
        print(f"Envío gratuito: {envio_gratuito}")
        
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

        # Configurar opciones de envío dinámicamente
        shipping_options = []
        if not envio_gratuito:
            shipping_options = SHIPPING_OPTIONS

        print(f"Creando sesión con {len(line_items)} productos")
        print(f"URLs - Success: {SUCCESS_URL}, Cancel: {CANCEL_URL}")

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
            shipping_address_collection={
                'allowed_countries': ALLOWED_COUNTRIES,
            },
            customer_email=None,
            phone_number_collection={
                'enabled': True,
            },
            shipping_options=shipping_options,
        )
        
        print(f"Sesión creada exitosamente: {session.id}")
        return jsonify({'id': session.id})
        
    except Exception as e:
        print(f"Error al crear sesión: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok', 'message': 'Servidor funcionando correctamente'})

if __name__ == '__main__':
    print("Iniciando servidor de Stripe...")
    print(f"Clave de Stripe configurada: {'Sí' if stripe.api_key else 'No'}")
    app.run(port=4242, debug=True) 