# 🧪 Configuración para Modo de Prueba de Stripe

## 📋 Pasos para configurar el entorno de prueba

### 1. Obtener las claves de prueba de Stripe

1. Ve a [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
2. Asegúrate de estar en el **modo de prueba** (toggle en la esquina superior izquierda)
3. Copia tu **clave pública de prueba** (pk_test_...)
4. Copia tu **clave secreta de prueba** (sk_test_...)

### 2. Configurar las claves

#### En `carrito.js`:
```javascript
const stripe = Stripe('pk_test_TU_CLAVE_PUBLICA_AQUI');
```

#### En `stripe_test_config.py`:
```python
STRIPE_SECRET_KEY_TEST = 'sk_test_TU_CLAVE_SECRETA_AQUI'
STRIPE_PUBLIC_KEY_TEST = 'pk_test_TU_CLAVE_PUBLICA_AQUI'
```

### 3. Configurar URLs (si es necesario)

Si usas puertos diferentes a los predeterminados, actualiza en `stripe_test_config.py`:

```python
FRONTEND_URL = 'http://localhost:3000'  # Tu servidor frontend
SUCCESS_URL = 'http://localhost:4242/success'  # Tu servidor backend
CANCEL_URL = 'http://localhost:4242/cancel'
```

### 4. Ejecutar el servidor

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de Stripe
python stripe_server.py
```

### 5. Probar el flujo

1. Abre tu sitio web en `http://localhost:3000`
2. Añade productos al carrito
3. Procede al pago
4. Usa las tarjetas de prueba de Stripe:
   - **Éxito**: `4242 4242 4242 4242`
   - **Declinada**: `4000 0000 0000 0002`
   - **Requerir autenticación**: `4000 0025 0000 3155`

### 6. Verificar el tracking

- Abre las herramientas de desarrollador (F12)
- Ve a la pestaña "Console"
- Deberías ver logs del tracking de Facebook Pixel
- Verifica en Facebook Events Manager que se registren los eventos

## 🔍 Tarjetas de prueba de Stripe

| Número | Descripción |
|--------|-------------|
| `4242 4242 4242 4242` | Pago exitoso |
| `4000 0000 0000 0002` | Pago declinado |
| `4000 0025 0000 3155` | Requiere autenticación |
| `4000 0000 0000 9995` | Fondos insuficientes |

**Fecha de vencimiento**: Cualquier fecha futura  
**CVC**: Cualquier código de 3 dígitos  
**ZIP**: Cualquier código postal

## ⚠️ Importante

- **NUNCA** uses claves de producción en modo de prueba
- Las transacciones de prueba **NO** se cobran
- Los datos de prueba se eliminan automáticamente
- Cambia a modo de producción solo cuando esté listo para lanzar

## 🐛 Solución de problemas

### Error: "Invalid API Key"
- Verifica que estés usando claves de prueba (pk_test_/sk_test_)
- Asegúrate de que las claves estén correctamente copiadas

### Error: "CORS"
- Verifica que el servidor esté ejecutándose en el puerto correcto
- Asegúrate de que las URLs en la configuración sean correctas

### No se registran eventos de Facebook
- Verifica que el Facebook Pixel esté cargado correctamente
- Revisa la consola del navegador para errores
- Asegúrate de que el valor total se esté pasando correctamente














