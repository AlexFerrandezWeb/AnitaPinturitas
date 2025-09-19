#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def enviar_correo_notificacion(destinatario, asunto, detalles_pedido_html):
    """
    Función para enviar un correo de notificación de pedido usando Gmail.
    """
    # --- 1. Cargar Credenciales (desde Variables de Entorno) ---
    remitente = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS') # La contraseña de aplicación de 16 letras

    if not remitente or not password:
        print("Error: Las variables de entorno EMAIL_USER y EMAIL_PASS no están configuradas.")
        return False

    # --- 2. Construir el Mensaje ---
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    
    # Adjuntar el cuerpo del correo en formato HTML
    msg.attach(MIMEText(detalles_pedido_html, 'html'))
    
    # --- 3. Enviar el Correo vía SMTP de Gmail ---
    try:
        # Conectar al servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Iniciar conexión segura
        
        # Iniciar sesión
        server.login(remitente, password)
        
        # Enviar el correo
        texto_del_mensaje = msg.as_string()
        server.sendmail(remitente, destinatario, texto_del_mensaje)
        
        # Cerrar la conexión
        server.quit()
        
        print(f"Correo enviado exitosamente a {destinatario}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

def enviar_correo_pago_exitoso(datos_pago):
    """
    Envía un correo de notificación cuando se completa un pago
    """
    
    # Configuración del correo
    email_destino = "anamaria.amrrg@gmail.com"
    
    # Información básica del pago
    pago_id = datos_pago.get('id', 'N/A')
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    total = datos_pago.get('amount_total', 0) / 100  # Convertir de centavos a euros
    moneda = datos_pago.get('currency', 'eur').upper()
    
    # Información del cliente
    cliente = datos_pago.get('customer_details', {})
    nombre = cliente.get('name', 'No especificado')
    email_cliente = cliente.get('email', 'No especificado')
    telefono = cliente.get('phone', 'No especificado')
    
    # Dirección de envío
    direccion = cliente.get('address', {})
    direccion_completa = f"""
    {direccion.get('line1', '')} {direccion.get('line2', '')}
    {direccion.get('postal_code', '')} {direccion.get('city', '')}
    {direccion.get('state', '')} {direccion.get('country', '')}
    """.strip()
    
    # Productos comprados
    productos_html = ""
    if 'line_items' in datos_pago:
        for item in datos_pago['line_items']['data']:
            producto = item.get('description', 'Producto')
            cantidad = item.get('quantity', 1)
            precio_unitario = item.get('price', {}).get('unit_amount', 0) / 100
            precio_total = item.get('amount_total', 0) / 100
            
            productos_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{producto}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{cantidad}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{precio_unitario:.2f} {moneda}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{precio_total:.2f} {moneda}</td>
            </tr>
            """
    
    # Crear HTML del correo
    cuerpo_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; margin: -20px -20px 20px -20px; }}
            .section {{ margin-bottom: 20px; }}
            .section h3 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #f8f9fa; padding: 10px; text-align: left; border: 1px solid #ddd; }}
            .total {{ font-size: 18px; font-weight: bold; color: #4CAF50; }}
            .info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 ¡Nuevo Pedido Recibido! (#{pago_id})</h1>
                <p>Anita Pinturitas - Sistema de Notificaciones</p>
            </div>
            
            <div class="section">
                <h3>📋 Información del Pago</h3>
                <div class="info">
                    <p><strong>ID del Pago:</strong> {pago_id}</p>
                    <p><strong>Fecha y Hora:</strong> {fecha}</p>
                    <p><strong>Total Pagado:</strong> <span class="total">{total:.2f} {moneda}</span></p>
                </div>
            </div>
            
            <div class="section">
                <h3>👤 Detalles de Envío:</h3>
                <div class="info">
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Email:</strong> {email_cliente}</p>
                    <p><strong>Teléfono:</strong> {telefono}</p>
                    <p><strong>Dirección:</strong><br><pre style="margin: 0; white-space: pre-wrap;">{direccion_completa}</pre></p>
                </div>
            </div>
            
            <div class="section">
                <h3>🛍️ Productos Comprados:</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Precio Unitario</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {productos_html}
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h3>📦 Próximos Pasos</h3>
                <div class="info">
                    <p>1. <strong>Preparar el pedido</strong> con los productos listados arriba</p>
                    <p>2. <strong>Empacar</strong> cuidadosamente los productos</p>
                    <p>3. <strong>Enviar</strong> a la dirección proporcionada</p>
                    <p>4. <strong>Actualizar</strong> el estado del pedido en tu sistema</p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
                <p>Este correo fue generado automáticamente por el sistema de Anita Pinturitas</p>
                <p>Fecha: {fecha}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Llamar a la función para enviar el correo
    return enviar_correo_notificacion(
        destinatario=email_destino,
        asunto=f"Nuevo Pedido en anitapinturitas.es: #{pago_id}",
        detalles_pedido_html=cuerpo_html
    )
    
    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = email_origen
        msg['To'] = email_destino
        msg['Subject'] = f"💰 NUEVO PAGO COMPLETADO - {datos_pago.get('id', 'N/A')}"
        
        # Crear contenido del correo
        contenido = crear_contenido_correo(datos_pago)
        msg.attach(MIMEText(contenido, 'html', 'utf-8'))
        
        # Conectar y enviar
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_origen, email_password)
        
        text = msg.as_string()
        server.sendmail(email_origen, email_destino, text)
        server.quit()
        
        print(f"✅ Correo enviado exitosamente para pago {datos_pago.get('id', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando correo: {str(e)}")
        return False

def crear_contenido_correo(datos_pago):
    """
    Crea el contenido HTML del correo con los datos del pago
    """
    
    # Información básica del pago
    pago_id = datos_pago.get('id', 'N/A')
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    total = datos_pago.get('amount_total', 0) / 100  # Convertir de centavos a euros
    moneda = datos_pago.get('currency', 'eur').upper()
    
    # Información del cliente
    cliente = datos_pago.get('customer_details', {})
    nombre = cliente.get('name', 'No especificado')
    email_cliente = cliente.get('email', 'No especificado')
    telefono = cliente.get('phone', 'No especificado')
    
    # Dirección de envío
    direccion = cliente.get('address', {})
    direccion_completa = f"""
    {direccion.get('line1', '')} {direccion.get('line2', '')}
    {direccion.get('postal_code', '')} {direccion.get('city', '')}
    {direccion.get('state', '')} {direccion.get('country', '')}
    """.strip()
    
    # Productos comprados
    productos_html = ""
    if 'line_items' in datos_pago:
        for item in datos_pago['line_items']['data']:
            producto = item.get('description', 'Producto')
            cantidad = item.get('quantity', 1)
            precio_unitario = item.get('price', {}).get('unit_amount', 0) / 100
            precio_total = item.get('amount_total', 0) / 100
            
            productos_html += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">{producto}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{cantidad}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{precio_unitario:.2f} {moneda}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{precio_total:.2f} {moneda}</td>
            </tr>
            """
    
    # Crear HTML del correo
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; margin: -20px -20px 20px -20px; }}
            .section {{ margin-bottom: 20px; }}
            .section h3 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #f8f9fa; padding: 10px; text-align: left; border: 1px solid #ddd; }}
            .total {{ font-size: 18px; font-weight: bold; color: #4CAF50; }}
            .info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 NUEVO PAGO COMPLETADO</h1>
                <p>Anita Pinturitas - Sistema de Notificaciones</p>
            </div>
            
            <div class="section">
                <h3>📋 Información del Pago</h3>
                <div class="info">
                    <p><strong>ID del Pago:</strong> {pago_id}</p>
                    <p><strong>Fecha y Hora:</strong> {fecha}</p>
                    <p><strong>Total Pagado:</strong> <span class="total">{total:.2f} {moneda}</span></p>
                </div>
            </div>
            
            <div class="section">
                <h3>👤 Datos del Cliente</h3>
                <div class="info">
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Email:</strong> {email_cliente}</p>
                    <p><strong>Teléfono:</strong> {telefono}</p>
                </div>
            </div>
            
            <div class="section">
                <h3>📍 Dirección de Envío</h3>
                <div class="info">
                    <pre style="margin: 0; white-space: pre-wrap;">{direccion_completa}</pre>
                </div>
            </div>
            
            <div class="section">
                <h3>🛍️ Productos Comprados</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Precio Unitario</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {productos_html}
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h3>📦 Próximos Pasos</h3>
                <div class="info">
                    <p>1. <strong>Preparar el pedido</strong> con los productos listados arriba</p>
                    <p>2. <strong>Empacar</strong> cuidadosamente los productos</p>
                    <p>3. <strong>Enviar</strong> a la dirección proporcionada</p>
                    <p>4. <strong>Actualizar</strong> el estado del pedido en tu sistema</p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
                <p>Este correo fue generado automáticamente por el sistema de Anita Pinturitas</p>
                <p>Fecha: {fecha}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    # Datos de prueba
    datos_prueba = {
        'id': 'cs_test_123456789',
        'amount_total': 6100,  # 61.00 EUR en centavos
        'currency': 'eur',
        'customer_details': {
            'name': 'Juan Pérez',
            'email': 'juan@ejemplo.com',
            'phone': '+34612345678',
            'address': {
                'line1': 'Calle Mayor 123',
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
    
    print("🧪 Probando envío de correo...")
    resultado = enviar_correo_pago_exitoso(datos_prueba)
    if resultado:
        print("✅ Correo de prueba enviado exitosamente")
    else:
        print("❌ Error en el envío del correo de prueba")
