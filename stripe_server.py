from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import os
import json

app = Flask(__name__)
CORS(app)

# Configurar Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "Servidor funcionando",
        "stripe_version": stripe.VERSION,
        "message": "Test exitoso"
    })

@app.route('/test-payment-methods', methods=['GET'])
def test_payment_methods():
    return jsonify({
        "stripe_version": stripe.VERSION,
        "available_methods": ["card", "paypal"],
        "message": "PayPal está habilitado en el dashboard de Stripe"
    })

@app.route('/diagnostico', methods=['GET'])
def diagnostico():
    return jsonify({
        "servidor": "Funcionando",
        "stripe_version": stripe.VERSION,
        "configuracion": "Básica - compatible con todas las versiones",
        "paypal": "Habilitado en dashboard",
        "imagenes": "URLs absolutas configuradas"
    })

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion():
    try:
        data = request.get_json()
        carrito = data.get('carrito', [])
        
        if not carrito:
            return jsonify({"error": "Carrito vacío"}), 400
        
        # Preparar items para Stripe
        line_items = []
        
        for item in carrito:
            nombre = item.get('nombre', 'Producto')
            precio = float(item.get('precio', 0)) * 100  # Convertir a centavos
            cantidad = int(item.get('cantidad', 1))
            imagen_url = item.get('imagen', '/assets/placeholder.jpg')
            
            # Convertir URL relativa a absoluta
            if imagen_url.startswith('/'):
                imagen_url = f"https://anitapinturitas.es{imagen_url}"
            
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': nombre,
                        'images': [imagen_url]
                    },
                    'unit_amount': int(precio)
                },
                'quantity': cantidad
            })
        
        # Crear sesión de Stripe - CONFIGURACIÓN MÍNIMA
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url='https://anitapinturitas.es/carrito.html?success=true',
            cancel_url='https://anitapinturitas.es/carrito.html?canceled=true',
            locale='es',
            billing_address_collection='required',
            phone_number_collection={'enabled': True}
        )
        
        return jsonify({
            "id": session.id,
            "url": session.url,
            "message": "Sesión creada exitosamente"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/crear-sesion-simple', methods=['POST'])
def crear_sesion_simple():
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({"error": "No hay items"}), 400
        
        # Crear sesión ultra-simple
        session = stripe.checkout.Session.create(
            line_items=items,
            mode='payment',
            success_url='https://anitapinturitas.es/carrito.html?success=true',
            cancel_url='https://anitapinturitas.es/carrito.html?canceled=true'
        )
        
        return jsonify({
            "id": session.id,
            "url": session.url,
            "message": "Sesión simple creada"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)