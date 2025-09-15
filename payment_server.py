from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import stripe
import os
import json

app = Flask(__name__)
CORS(app)

# Configuración de Stripe - Usar variable de entorno
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# PRUEBA DEFINITIVA - Mostrar qué clave está usando
print("=" * 50)
print("🔍 DIAGNÓSTICO DE VARIABLES DE ENTORNO:")
print("=" * 50)

# Verificar todas las variables de entorno relacionadas con Stripe
env_vars = ['STRIPE_SECRET_KEY']
for var in env_vars:
    value = os.environ.get(var)
    if value:
        print(f"✅ {var}: {value[-6:]}")
    else:
        print(f"❌ {var}: NO CONFIGURADA")

print("=" * 50)
print("🔑 CLAVE FINAL EN USO:")
if stripe.api_key:
    print(f"✅ CLAVE (últimos 6): [{stripe.api_key[-6:]}]")
    print(f"✅ CLAVE COMPLETA: {stripe.api_key}")
else:
    print("❌ NO HAY CLAVE CONFIGURADA")
print("=" * 50)

# Configuración
CURRENCY = 'eur'
SUCCESS_URL = 'https://anitapinturitas.com/success'
CANCEL_URL = 'https://anitapinturitas.com/cancel'
ALLOWED_COUNTRIES = ['ES', 'PT', 'FR', 'IT', 'DE', 'GB']
IMAGEN_POR_DEFECTO = "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&crop=center"

SHIPPING_OPTIONS = [
    {
        'shipping_rate_data': {
            'type': 'fixed_amount',
            'fixed_amount': {
                'amount': 500,  # 5€
                'currency': CURRENCY,
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

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok', 
        'message': 'NUEVO SERVidor funcionando correctamente - VERSION 2025',
        'version': 'payment-server-2025',
        'timestamp': '2025-01-27-15:45',
        'server': 'payment_server.py'
    })

@app.route('/debug', methods=['GET'])
def debug():
    return jsonify({
        'status': 'debug',
        'message': 'Debug endpoint funcionando',
        'version': 'payment-server-2025',
        'timestamp': '2025-01-27-15:45',
        'routes': ['/test', '/debug', '/pagar-ahora-2025']
    })

@app.route('/pagar-ahora-2025', methods=['POST'])
def pagar_ahora_2025():
    try:
        print("🚀 NUEVO SERVIDOR /pagar-ahora-2025 - Sin automatic_payment_methods")
        data = request.get_json()
        carrito = data.get('carrito', [])

        subtotal = sum(float(producto['precio']) * int(producto['cantidad']) for producto in carrito)
        envio_gratuito = subtotal >= 62

        line_items = []
        for producto in carrito:
            product_data = {
                'name': producto['nombre'],
                'images': []
            }

            imagen_url = producto.get('imagen')
            if imagen_url:
                if imagen_url.startswith('/'):
                    imagen_url = f"https://anitapinturitas.com{imagen_url}"
                elif not imagen_url.startswith('http'):
                    imagen_url = f"https://anitapinturitas.com/{imagen_url.lstrip('/')}"
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

        shipping_options = [] if envio_gratuito else SHIPPING_OPTIONS

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
            shipping_options=shipping_options,
            locale='es',
            billing_address_collection='required',
            payment_method_types=['card', 'paypal'],  # Versión corregida sin automatic_payment_methods
            metadata={
                'source': 'anita_pinturitas_web'
            }
        )
        
        print(f"🚀 NUEVO SERVIDOR /pagar-ahora-2025 - Sesión creada exitosamente: {session.id}")
        print("✅ Sin automatic_payment_methods - Solo payment_method_types=['card', 'paypal']")
        return jsonify({'id': session.id})
        
    except Exception as e:
        print(f"Error al crear sesión: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/cancel', methods=['GET'])
def cancel():
    return jsonify({'message': 'Pago cancelado'})

@app.route('/success', methods=['GET'])
def success():
    return jsonify({'message': 'Pago exitoso'})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Servidor funcionando correctamente', 'status': 'OK'})

@app.route('/debug', methods=['GET'])
def debug():
    """Endpoint de diagnóstico para verificar archivos"""
    import os
    files_info = {}
    
    # Verificar si productos.json existe
    if os.path.exists('productos.json'):
        files_info['productos.json'] = 'EXISTS'
        try:
            with open('productos.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                files_info['productos_count'] = len(data.get('categorias', []))
        except Exception as e:
            files_info['productos_error'] = str(e)
    else:
        files_info['productos.json'] = 'NOT FOUND'
    
    # Listar archivos en el directorio actual
    files_info['current_files'] = os.listdir('.')
    
    return jsonify(files_info)

@app.route('/facebook-feed.xml', methods=['GET'])
def facebook_feed():
    """Genera el feed de productos para Meta (Facebook) en formato XML"""
    try:
        # Cargar los productos desde el JSON
        with open('productos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Iniciar el XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
        xml += '<channel>\n'
        xml += '<title>Anita Pinturitas - Productos</title>\n'
        xml += '<link>https://anitapinturitas.com</link>\n'
        xml += '<description>Catálogo de productos de cosmética natural Anita Pinturitas</description>\n'
        
        # Procesar cada categoría y sus productos
        for categoria in data.get('categorias', []):
            for producto in categoria.get('productos', []):
                xml += '<item>\n'
                xml += f'<g:id>{producto.get("id", "")}</g:id>\n'
                xml += f'<g:title><![CDATA[{producto.get("nombre", "")}]]></g:title>\n'
                xml += f'<g:description><![CDATA[{producto.get("descripcion", "")}]]></g:description>\n'
                xml += f'<g:link>https://anitapinturitas.com/producto.html?id={producto.get("id", "")}</g:link>\n'
                xml += f'<g:image_link>https://anitapinturitas.com{producto.get("imagen", "")}</g:image_link>\n'
                xml += f'<g:price>{producto.get("precio", 0)} EUR</g:price>\n'
                xml += '<g:availability>in stock</g:availability>\n'
                xml += '<g:condition>new</g:condition>\n'
                xml += '<g:brand>Anita Pinturitas</g:brand>\n'
                xml += f'<g:product_type><![CDATA[{categoria.get("nombre", "")}]]></g:product_type>\n'
                xml += '</item>\n'
        
        xml += '</channel>\n'
        xml += '</rss>'
        
        # Devolver como XML
        return Response(xml, mimetype='text/xml')
        
    except Exception as e:
        print(f"Error generando feed de Facebook: {e}")
        return Response(f'<error>Error generando feed: {str(e)}</error>', 
                       mimetype='text/xml', status=500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 