# Configuración del Feed de Facebook para Meta

## ✅ ¿Qué he creado?

He añadido un endpoint en tu servidor de Python que genera automáticamente el feed de productos para Meta (Facebook) en formato XML.

## 🔗 URL del Feed

Una vez desplegado, tu feed estará disponible en:
```
https://anita-pinturitas-server.onrender.com/facebook-feed.xml
```

## 📋 Campos incluidos en el feed

El feed incluye todos los campos requeridos por Meta:
- ✅ **id**: ID único del producto
- ✅ **title**: Nombre del producto
- ✅ **description**: Descripción completa
- ✅ **link**: URL del producto en tu web
- ✅ **image_link**: URL de la imagen del producto
- ✅ **price**: Precio en EUR
- ✅ **availability**: "in stock" (todos los productos)
- ✅ **condition**: "new" (productos nuevos)
- ✅ **brand**: "Anita Pinturitas"
- ✅ **product_type**: Categoría del producto

## 🚀 Pasos para activar el feed

### 1. Subir los cambios a GitHub
```bash
git add .
git commit -m "Añadido feed de Facebook para Meta"
git push
```

### 2. Verificar que Render se actualice
- Ve a tu dashboard de Render
- Verifica que el servicio se esté desplegando con los nuevos cambios
- Espera a que termine el despliegue

### 3. Probar el feed
Visita: `https://anita-pinturitas-server.onrender.com/facebook-feed.xml`

Deberías ver un XML con todos tus productos.

### 4. Configurar en Meta Business Manager

1. Ve a **Meta Business Manager** → **Catálogos** → **Tu catálogo**
2. Ve a **Fuentes de datos** → **Añadir fuentes de datos**
3. Selecciona **Feed de datos**
4. Pega la URL: `https://anita-pinturitas-server.onrender.com/facebook-feed.xml`
5. Configura la frecuencia de actualización (recomiendo cada 6 horas)
6. Guarda y activa

## 🔄 Actualización automática

El feed se actualiza automáticamente cada vez que:
- Cambies el archivo `productos.json`
- Reinicies el servidor de Render

## 🛠️ Personalización

Si necesitas modificar el feed, edita la función `facebook_feed()` en `payment_server.py`:

```python
@app.route('/facebook-feed.xml', methods=['GET'])
def facebook_feed():
    # Aquí puedes modificar los campos del XML
```

## 📊 Ventajas de esta solución

1. **Automática**: Se actualiza solo cuando cambias productos
2. **Completa**: Incluye todos los campos requeridos por Meta
3. **Eficiente**: Se genera dinámicamente desde tu JSON
4. **Escalable**: Funciona con cualquier cantidad de productos
5. **Mantenible**: Un solo lugar para gestionar productos

## 🎯 Próximos pasos

1. Despliega los cambios
2. Prueba el feed
3. Configúralo en Meta Business Manager
4. ¡Disfruta de las ventas desde Facebook e Instagram!
