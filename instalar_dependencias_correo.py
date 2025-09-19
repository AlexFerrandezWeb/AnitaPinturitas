#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para instalar las dependencias necesarias para el envío de correos
"""

import subprocess
import sys

def instalar_dependencias():
    """
    Instala las dependencias necesarias para el sistema de correos
    """
    
    dependencias = [
        'flask',
        'stripe',
        'flask-cors'
    ]
    
    print("🔧 Instalando dependencias para el sistema de correos...")
    
    for dependencia in dependencias:
        try:
            print(f"📦 Instalando {dependencia}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependencia])
            print(f"✅ {dependencia} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {dependencia}: {e}")
            return False
    
    print("\n🎉 Todas las dependencias instaladas correctamente")
    print("\n📋 Próximos pasos:")
    print("1. Configura la contraseña de aplicación de Gmail")
    print("2. Configura el webhook de Stripe")
    print("3. Ejecuta el servidor de webhook")
    
    return True

if __name__ == "__main__":
    instalar_dependencias()
