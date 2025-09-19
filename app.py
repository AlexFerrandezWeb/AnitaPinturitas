#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def pagina_de_inicio():
    """
    Ruta principal que muestra la página de inicio de Anita Pinturitas
    """
    return render_template('index.html')

@app.route('/test')
def test():
    """
    Endpoint de prueba simple
    """
    return "¡Funciona! El servidor está activo."

if __name__ == '__main__':
    print("🚀 Iniciando servidor de prueba...")
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
