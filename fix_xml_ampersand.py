#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir el archivo XML reemplazando & por &amp; y añadiendo CDATA
"""

def fix_xml_ampersand():
    # Leer el archivo actual
    with open('facebook-feed-v2.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar & por &amp; en las descripciones y títulos
    # Esto es más seguro que CDATA para Meta
    content = content.replace(' & ', ' &amp; ')
    content = content.replace('& ', '&amp; ')
    content = content.replace(' &', ' &amp;')
    
    # Escribir el archivo corregido
    with open('facebook-feed-v2.xml', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Archivo facebook-feed-v2.xml corregido")
    print("Caracteres & reemplazados por &amp;")

if __name__ == "__main__":
    fix_xml_ampersand()




