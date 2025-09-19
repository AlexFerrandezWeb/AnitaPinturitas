#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar facebook-feed-final.xml en formato RSS XML
Versión específica para Hostinger que mantiene la declaración XML
"""

import json
from datetime import datetime

def generar_meta_rss_hostinger():
    # Cargar productos
    with open('productos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fecha actual
    now = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Crear RSS feed - DECLARACIÓN XML OBLIGATORIA AL PRINCIPIO
    rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content += '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">\n'
    rss_content += '<channel>\n'
    rss_content += '<title>Anita Pinturitas - Productos</title>\n'
    rss_content += '<link>https://anitapinturitas.es</link>\n'
    rss_content += '<description>Catálogo de productos de Anita Pinturitas</description>\n'
    rss_content += f'<lastBuildDate>{now}</lastBuildDate>\n\n'
    
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
            
            # Crear item con campos OBLIGATORIOS de Meta
            rss_content += '<item>\n'
            
            # 1. g:id (OBLIGATORIO) - Identificador único
            rss_content += f'<g:id>{producto.get("id", "")}</g:id>\n'
            
            # 2. g:title (OBLIGATORIO) - Título con mayúscula inicial
            titulo = producto.get("nombre", "").title()
            rss_content += f'<g:title><![CDATA[{titulo}]]></g:title>\n'
            
            # 3. g:description (OBLIGATORIO) - Descripción detallada
            descripcion = producto.get("descripcion", "")
            rss_content += f'<g:description><![CDATA[{descripcion}]]></g:description>\n'
            
            # 4. g:availability (OBLIGATORIO) - Disponibilidad
            rss_content += '<g:availability>in stock</g:availability>\n'
            
            # 5. g:condition (OBLIGATORIO) - Estado del producto
            rss_content += '<g:condition>new</g:condition>\n'
            
            # 6. g:price (OBLIGATORIO) - Precio con formato correcto
            precio = float(producto.get("precio", 0))
            rss_content += f'<g:price>{precio:.2f} EUR</g:price>\n'
            
            # 7. g:link (OBLIGATORIO) - Enlace al producto
            rss_content += f'<g:link>https://anitapinturitas.es/producto.html?id={producto.get("id", "")}</g:link>\n'
            
            # 8. g:image_link (OBLIGATORIO) - URL de la imagen
            rss_content += f'<g:image_link>{imagen_url}</g:image_link>\n'
            
            # 9. g:brand (OBLIGATORIO) - Marca
            rss_content += '<g:brand>Anita Pinturitas</g:brand>\n'
            
            # Campos adicionales recomendados
            rss_content += f'<g:product_type><![CDATA[{categoria_nombre}]]></g:product_type>\n'
            rss_content += '<g:google_product_category>Health &amp; Beauty &gt; Personal Care &gt; Cosmetics</g:google_product_category>\n'
            
            rss_content += '</item>\n\n'
    
    rss_content += '</channel>\n'
    rss_content += '</rss>\n'
    
    # Escribir archivo - Codificación específica para Hostinger
    with open('facebook-feed-final.xml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(rss_content)
    
    print(f"✅ Feed RSS generado con {total} productos")
    print("✅ DECLARACIÓN XML OBLIGATORIA AL PRINCIPIO")
    print("✅ Formato RSS XML (preferido por Meta)")
    print("✅ TODOS los campos OBLIGATORIOS de Meta incluidos")
    print("✅ Codificación específica para Hostinger")

if __name__ == "__main__":
    generar_meta_rss_hostinger()


