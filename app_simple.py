#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configurar CORS para permitir peticiones desde tu dominio y el servicio de Render
CORS(app, resources={r"/*": {"origins": [
    "https://anitapinturitas.es", 
    "https://www.anitapinturitas.es",
    "https://anita-pinturitas-server.onrender.com"  # Frontend de Render
]}})

@app.route('/')
def pagina_de_inicio():
    """
    Ruta principal que muestra la página de inicio de Anita Pinturitas
    """
    return render_template('index.html')

@app.route('/webhook-test', methods=['GET'])
def webhook_test():
    """
    Endpoint de prueba para verificar que el servidor funciona
    """
    return jsonify({
        'status': 'Servidor funcionando',
        'message': 'El servidor está activo y respondiendo'
    })

@app.route('/crear-sesion', methods=['POST'])
def crear_sesion_stripe():
    """
    Crea una sesión de Stripe Checkout para el carrito
    """
    try:
        data = request.get_json()
        carrito = data.get('carrito', [])
        
        if not carrito:
            return jsonify({'error': 'El carrito está vacío'}), 400
        
        # Simular respuesta exitosa para probar CORS
        return jsonify({
            'status': 'success',
            'message': 'CORS funcionando correctamente',
            'carrito_recibido': len(carrito)
        })
        
    except Exception as e:
        print(f"Error en crear-sesion: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/<path:filename>')
def serve_static(filename):
    """
    Sirve archivos estáticos (CSS, JS, imágenes) desde la raíz del sitio
    """
    try:
        return app.send_static_file(filename)
    except:
        return "Archivo no encontrado", 404

if __name__ == '__main__':
    print("🚀 Iniciando servidor simple...")
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
