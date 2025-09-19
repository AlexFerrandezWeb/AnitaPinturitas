#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar el archivo facebook-feed-v2.xml con formato compatible con Meta
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generar_facebook_feed_meta():
    # Cargar los productos desde el archivo JSON
    with open('productos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Crear el elemento raíz del RSS con formato correcto para Meta
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:g', 'http://base.google.com/ns/1.0')
    
    # Crear el canal
    channel = ET.SubElement(rss, 'channel')
    
    # Información del canal
    title = ET.SubElement(channel, 'title')
    title.text = 'Anita Pinturitas - Productos'
    
    link = ET.SubElement(channel, 'link')
    link.text = 'https://anitapinturitas.es'
    
    description = ET.SubElement(channel, 'description')
    description.text = 'Catálogo de productos de cosmética natural Anita Pinturitas'
    
    # Contador de productos
    total_productos = 0
    
    # Procesar cada categoría y sus productos
    for categoria in data.get('categorias', []):
        categoria_nombre = categoria.get('nombre', '')
        print(f"Procesando categoría: {categoria_nombre}")
        
        for producto in categoria.get('productos', []):
            total_productos += 1
            
            # Crear elemento item
            item = ET.SubElement(channel, 'item')
            
            # ID del producto
            g_id = ET.SubElement(item, 'g:id')
            g_id.text = producto.get('id', '')
            
            # Título del producto
            g_title = ET.SubElement(item, 'g:title')
            g_title.text = producto.get('nombre', '')
            
            # Descripción del producto
            g_description = ET.SubElement(item, 'g:description')
            g_description.text = producto.get('descripcion', '')
            
            # Enlace del producto
            g_link = ET.SubElement(item, 'g:link')
            g_link.text = f"https://anitapinturitas.es/producto.html?id={producto.get('id', '')}"
            
            # Enlace de la imagen
            g_image_link = ET.SubElement(item, 'g:image_link')
            imagen_url = producto.get('imagen', '')
            if imagen_url.startswith('/'):
                imagen_url = f"https://anitapinturitas.es{imagen_url}"
            elif not imagen_url.startswith('http'):
                imagen_url = f"https://anitapinturitas.es/{imagen_url.lstrip('/')}"
            g_image_link.text = imagen_url
            
            # Precio del producto
            g_price = ET.SubElement(item, 'g:price')
            g_price.text = f"{producto.get('precio', 0):.2f} EUR"
            
            # Disponibilidad
            g_availability = ET.SubElement(item, 'g:availability')
            g_availability.text = 'in stock'
            
            # Condición
            g_condition = ET.SubElement(item, 'g:condition')
            g_condition.text = 'new'
            
            # Marca
            g_brand = ET.SubElement(item, 'g:brand')
            g_brand.text = 'Anita Pinturitas'
            
            # Tipo de producto
            g_product_type = ET.SubElement(item, 'g:product_type')
            g_product_type.text = categoria_nombre
            
            # Categoría
            g_product_category = ET.SubElement(item, 'g:product_category')
            g_product_category.text = categoria_nombre
    
    print(f"Total de productos procesados: {total_productos}")
    
    # Crear el XML con formato correcto
    xml_str = ET.tostring(rss, encoding='utf-8', method='xml')
    
    # Escribir el archivo con formato correcto
    with open('facebook-feed-v2.xml', 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(xml_str)
    
    print("Archivo facebook-feed-v2.xml generado exitosamente")
    print(f"Total de productos incluidos: {total_productos}")

if __name__ == "__main__":
    generar_facebook_feed_meta()


