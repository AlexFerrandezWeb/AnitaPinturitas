#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar facebook-feed-meta.xml en formato ATOM compatible con Meta
"""

import json
from datetime import datetime

def generar_atom_feed():
    # Cargar productos
    with open('productos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fecha actual
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Crear ATOM feed
    atom_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    atom_content += '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:g="http://base.google.com/ns/1.0">\n'
    atom_content += f'<title>Anita Pinturitas - Productos</title>\n'
    atom_content += f'<link href="https://anitapinturitas.es"/>\n'
    atom_content += f'<updated>{now}</updated>\n'
    atom_content += f'<author><name>Anita Pinturitas</name></author>\n\n'
    
    total = 0
    
    for categoria in data.get('categorias', []):
        categoria_nombre = categoria.get('nombre', '')
        print(f"Procesando: {categoria_nombre}")
        
        for producto in categoria.get('productos', []):
            total += 1
            
            # Procesar imagen
            imagen_url = producto.get('imagen', '')
            if imagen_url.startswith('/'):
                imagen_url = f"https://anitapinturitas.es{imagen_url}"
            elif not imagen_url.startswith('http'):
                imagen_url = f"https://anitapinturitas.es/{imagen_url.lstrip('/')}"
            
            # Crear entry
            atom_content += '<entry>\n'
            atom_content += f'<g:id>{producto.get("id", "")}</g:id>\n'
            atom_content += f'<g:title><![CDATA[{producto.get("nombre", "")}]]></g:title>\n'
            atom_content += f'<g:description><![CDATA[{producto.get("descripcion", "")}]]></g:description>\n'
            atom_content += f'<g:link>https://anitapinturitas.es/producto.html?id={producto.get("id", "")}</g:link>\n'
            atom_content += f'<g:image_link>{imagen_url}</g:image_link>\n'
            atom_content += f'<g:price>{producto.get("precio", 0):.2f} EUR</g:price>\n'
            atom_content += '<g:availability>in stock</g:availability>\n'
            atom_content += '<g:condition>new</g:condition>\n'
            atom_content += '<g:brand>Anita Pinturitas</g:brand>\n'
            atom_content += f'<g:product_type><![CDATA[{categoria_nombre}]]></g:product_type>\n'
            atom_content += f'<updated>{now}</updated>\n'
            atom_content += '</entry>\n\n'
    
    atom_content += '</feed>\n'
    
    # Escribir archivo
    with open('facebook-feed-meta.xml', 'w', encoding='utf-8') as f:
        f.write(atom_content)
    
    print(f"✅ Feed ATOM generado con {total} productos")
    print("✅ Formato ATOM compatible con Meta")

if __name__ == "__main__":
    generar_atom_feed()
