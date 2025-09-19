#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
import os
import json

# Importaciones opcionales para evitar errores de inicio
try:
    import stripe
    from enviar_correo_pago import enviar_correo_pago_exitoso
    STRIPE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Advertencia: {e}")
    STRIPE_AVAILABLE = False

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuración de Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
stripe_webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

@app.route('/')
def pagina_de_inicio():
    """
    Ruta principal que muestra la página de inicio de Anita Pinturitas
    """
    return render_template('index.html')

@app.route('/productos.html')
def productos():
    """
    Página de productos Naturnua
    """
    return render_template('productos.html')

@app.route('/catalogo.html')
def catalogo():
    """
    Catálogo de productos Younique
    """
    return render_template('catalogo.html')

@app.route('/carrito.html')
def carrito():
    """
    Página del carrito de compras
    """
    return render_template('carrito.html')

@app.route('/producto.html')
def producto():
    """
    Página individual de producto
    """
    return render_template('producto.html')

@app.route('/success.html')
def success():
    """
    Página de éxito después del pago
    """
    return render_template('success.html')

@app.route('/envios.html')
def envios():
    """
    Información de envíos
    """
    return render_template('envios.html')

@app.route('/politica-privacidad.html')
def politica_privacidad():
    """
    Política de privacidad
    """
    return render_template('politica-privacidad.html')

@app.route('/politica-devoluciones.html')
def politica_devoluciones():
    """
    Política de devoluciones
    """
    return render_template('politica-devoluciones.html')

@app.route('/terminos-condiciones.html')
def terminos_condiciones():
    """
    Términos y condiciones
    """
    return render_template('terminos-condiciones.html')

@app.route('/registro.html')
def registro():
    """
    Página de registro
    """
    return render_template('registro.html')

@app.route('/webhook-stripe', methods=['POST'])
def webhook_stripe():
    """
    Webhook que recibe notificaciones de Stripe cuando se completa un pago
    """
    
    if not STRIPE_AVAILABLE:
        print("❌ Stripe no está disponible")
        return jsonify({'error': 'Stripe not available'}), 500
    
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        # Verificar la firma del webhook
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
        
        print(f"🔔 Webhook recibido: {event['type']}")
        
        # Procesar el evento
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            procesar_pago_completado(session)
            
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            print(f"✅ Pago exitoso: {payment_intent['id']}")
            
        else:
            print(f"ℹ️ Evento no procesado: {event['type']}")
        
        return jsonify({'status': 'success'})
        
    except ValueError as e:
        print(f"❌ Error en payload: {str(e)}")
        return jsonify({'error': 'Invalid payload'}), 400
        
    except stripe.error.SignatureVerificationError as e:
        print(f"❌ Error de verificación de firma: {str(e)}")
        return jsonify({'error': 'Invalid signature'}), 400
        
    except Exception as e:
        print(f"❌ Error procesando webhook: {str(e)}")
        return jsonify({'error': 'Webhook processing failed'}), 500

def procesar_pago_completado(session):
    """
    Procesa un pago completado y envía notificación por correo
    """
    
    if not STRIPE_AVAILABLE:
        print("❌ Stripe no está disponible para procesar pago")
        return
    
    try:
        print(f"💰 Procesando pago completado: {session['id']}")
        
        # Obtener detalles completos de la sesión
        session_details = stripe.checkout.Session.retrieve(
            session['id'],
            expand=['line_items', 'customer']
        )
        
        # Preparar datos para el correo
        datos_pago = {
            'id': session_details['id'],
            'amount_total': session_details['amount_total'],
            'currency': session_details['currency'],
            'customer_details': session_details.get('customer_details', {}),
            'line_items': session_details.get('line_items', {})
        }
        
        # Enviar correo de notificación
        print("📧 Enviando correo de notificación...")
        resultado = enviar_correo_pago_exitoso(datos_pago)
        
        if resultado:
            print("✅ Notificación enviada exitosamente")
        else:
            print("❌ Error enviando notificación")
            
        # Aquí podrías agregar más lógica como:
        # - Actualizar base de datos
        # - Generar factura
        # - Crear orden de envío
        # - etc.
        
    except Exception as e:
        print(f"❌ Error procesando pago completado: {str(e)}")

@app.route('/webhook-test', methods=['GET'])
def webhook_test():
    """
    Endpoint de prueba para verificar que el webhook funciona
    """
    return jsonify({
        'status': 'Webhook funcionando',
        'message': 'El webhook está listo para recibir notificaciones de Stripe'
    })

@app.route('/<path:filename>')
def serve_static(filename):
    """
    Sirve archivos estáticos (CSS, JS, imágenes) desde la raíz del sitio
    """
    return app.send_static_file(filename)

if __name__ == '__main__':
    print("🚀 Iniciando servidor de webhook de Stripe...")
    print("📧 Correo de destino: anitapinturitas6@gmail.com")
    print("🔗 Webhook URL: /webhook-stripe")
    
    # Obtener el puerto de las variables de entorno (Render lo proporciona)
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
