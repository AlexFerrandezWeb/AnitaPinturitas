#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
import stripe
import os
import json
from enviar_correo_pago import enviar_correo_pago_exitoso

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

@app.route('/webhook-stripe', methods=['POST'])
def webhook_stripe():
    """
    Webhook que recibe notificaciones de Stripe cuando se completa un pago
    """
    
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
    app.run(host='0.0.0.0', port=5001, debug=True)
