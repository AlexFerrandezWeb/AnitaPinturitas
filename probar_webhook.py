#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para probar el webhook de Stripe localmente
"""

import requests
import json

def probar_webhook_local():
    """
    Prueba el webhook localmente
    """
    
    # URL del webhook local
    webhook_url = "http://localhost:5001/webhook-stripe"
    test_url = "http://localhost:5001/webhook-test"
    
    print("🧪 Probando webhook de Stripe...")
    
    # Probar endpoint de test
    try:
        response = requests.get(test_url)
        if response.status_code == 200:
            print("✅ Webhook funcionando correctamente")
            print(f"📋 Respuesta: {response.json()}")
        else:
            print(f"❌ Error en webhook: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al webhook")
        print("💡 Asegúrate de que el webhook esté ejecutándose:")
        print("   python webhook_stripe.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def probar_correo():
    """
    Prueba el envío de correo directamente
    """
    
    print("\n📧 Probando envío de correo...")
    
    try:
        from enviar_correo_pago import enviar_correo_pago_exitoso
        
        # Datos de prueba
        datos_prueba = {
            'id': 'cs_test_123456789',
            'amount_total': 6100,  # 61.00 EUR
            'currency': 'eur',
            'customer_details': {
                'name': 'Cliente de Prueba',
                'email': 'cliente@ejemplo.com',
                'phone': '+34612345678',
                'address': {
                    'line1': 'Calle de Prueba 123',
                    'line2': '2º A',
                    'postal_code': '28001',
                    'city': 'Madrid',
                    'state': 'Madrid',
                    'country': 'ES'
                }
            },
            'line_items': {
                'data': [
                    {
                        'description': 'NUA GOLD (Crema Facial) - 50 Ml.',
                        'quantity': 1,
                        'price': {'unit_amount': 6100},
                        'amount_total': 6100
                    }
                ]
            }
        }
        
        resultado = enviar_correo_pago_exitoso(datos_prueba)
        
        if resultado:
            print("✅ Correo de prueba enviado exitosamente")
            print("📧 Revisa anitapinturitas6@gmail.com")
        else:
        print("❌ Error enviando correo de prueba")
        print("💡 Verifica la configuración de EMAIL_USER y EMAIL_PASS")
            
    except ImportError as e:
        print(f"❌ Error importando módulo: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema de correos...")
    print("=" * 50)
    
    probar_webhook_local()
    probar_correo()
    
    print("\n" + "=" * 50)
    print("📋 Próximos pasos:")
    print("1. Configura las variables de entorno en Render")
    print("2. Despliega el webhook en Render")
    print("3. Configura el webhook en Stripe Dashboard")
    print("4. Haz una compra de prueba")
