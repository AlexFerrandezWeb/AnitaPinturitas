#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
from datetime import datetime

def generar_csv_meta():
    """Genera un CSV compatible con Meta Commerce Manager"""
    
    # Cargar productos desde JSON
    with open('productos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Campos obligatorios para Meta
    campos_obligatorios = [
        'id',                    # ID único del producto
        'title',                 # Título del producto
        'description',           # Descripción
        'availability',          # Disponibilidad (in stock, out of stock, preorder)
        'condition',             # Condición (new, used, refurbished)
        'price',                 # Precio con moneda
        'link',                  # URL del producto
        'image_link',           # URL de la imagen
        'brand',                # Marca
        'google_product_category', # Categoría de Google
        'product_type',         # Tipo de producto
        'store_code'            # Código de tienda (OBLIGATORIO para Meta)
    ]
    
    # Crear archivo CSV
    with open('productos_facebook_meta.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campos_obligatorios)
        writer.writeheader()
        
        # Procesar cada categoría y producto
        for categoria in data['categorias']:
            categoria_nombre = categoria['nombre']
            
            for producto in categoria['productos']:
                # Preparar datos del producto
                row = {
                    'id': producto['id'],
                    'title': producto['nombre'],
                    'description': producto['descripcion'],
                    'availability': 'in stock',
                    'condition': 'new',
                    'price': f"{producto['precio']:.2f} EUR",
                    'link': f"https://anitapinturitas.es/producto.html?id={producto['id']}",
                    'image_link': f"https://anitapinturitas.es{producto['imagen']}",
                    'brand': 'Anita Pinturitas',
                    'google_product_category': 'Health & Beauty > Personal Care > Cosmetics',
                    'product_type': categoria_nombre,
                    'store_code': 'ANITA_PINTURITAS'  # Código de tienda obligatorio
                }
                
                writer.writerow(row)
    
    print(f"✅ CSV generado: productos_facebook_meta.csv")
    print(f"📊 Total de productos: {sum(len(cat['productos']) for cat in data['categorias'])}")
    print(f"🏪 Código de tienda: ANITA_PINTURITAS")
    print(f"🌐 Dominio: anitapinturitas.es")

if __name__ == "__main__":
    generar_csv_meta()

