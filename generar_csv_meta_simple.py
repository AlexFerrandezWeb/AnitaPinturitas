#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
from datetime import datetime

def generar_csv_meta_simple():
    """Genera un CSV compatible con Meta Commerce Manager con solo las columnas obligatorias"""
    
    # Cargar productos desde JSON
    with open('productos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Campos obligatorios para Meta (catálogo estándar)
    campos_obligatorios = [
        'id',                    # ID único del producto
        'title',                 # Título del producto
        'description',           # Descripción
        'link',                  # URL del producto
        'image_link',           # URL de la imagen
        'price',                 # Precio con moneda
        'availability',          # Disponibilidad (in stock, out of stock, preorder)
        'condition',             # Condición (new, used, refurbished)
        'brand',                 # Marca
        'product_type'           # Tipo de producto (categoría)
    ]
    
    # Crear archivo CSV
    with open('facebook-feed-final.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
                    'link': f"https://anitapinturitas.es/producto.html?id={producto['id']}",
                    'image_link': f"https://anitapinturitas.es{producto['imagen']}",
                    'price': f"{producto['precio']:.2f} EUR",
                    'availability': 'in stock',
                    'condition': 'new',
                    'brand': 'Anita Pinturitas',
                    'product_type': categoria_nombre  # Tipo de producto (categoría)
                }
                
                writer.writerow(row)
    
    print(f"✅ CSV generado: facebook-feed-final.csv")
    print(f"📊 Total de productos: {sum(len(cat['productos']) for cat in data['categorias'])}")
    print(f"🏪 Marca: Anita Pinturitas")
    print(f"🌐 Dominio: anitapinturitas.es")
    print(f"📋 Columnas: {', '.join(campos_obligatorios)}")

if __name__ == "__main__":
    generar_csv_meta_simple()
