# 📧 Configuración del Sistema de Correos para Pagos

## 🎯 Objetivo
Recibir un correo automático en `anamaria.amrrg@gmail.com` cada vez que un cliente complete un pago.

## 🔧 Configuración Requerida

### 1. Contraseña de Aplicación de Gmail

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Seguridad → Verificación en 2 pasos (debe estar activada)
3. Seguridad → Contraseñas de aplicaciones
4. Selecciona "Correo" y "Otro (nombre personalizado)"
5. Escribe "Anita Pinturitas Sistema"
6. Copia la contraseña generada (16 caracteres)

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con:

```bash
# Stripe
STRIPE_SECRET_KEY=sk_live_...  # Tu clave secreta de Stripe
STRIPE_WEBHOOK_SECRET=whsec_...  # Se obtiene al configurar el webhook

# Gmail
EMAIL_USER=anamaria.amrrg@gmail.com
EMAIL_PASS=tu_contraseña_de_16_caracteres

# URLs
SUCCESS_URL=https://anitapinturitas.es/success
CANCEL_URL=https://anitapinturitas.es/carrito.html
FRONTEND_URL=https://anitapinturitas.es
```

### 3. Configurar Webhook de Stripe

1. Ve al Dashboard de Stripe: https://dashboard.stripe.com/
2. Developers → Webhooks
3. "Add endpoint"
4. URL del endpoint: `https://tu-servidor.com/webhook-stripe`
5. Eventos a escuchar:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
6. Copia el "Signing secret" y ponlo en `STRIPE_WEBHOOK_SECRET`

## 🚀 Instalación y Ejecución

### 1. Instalar Dependencias
```bash
python instalar_dependencias_correo.py
```

### 2. Probar el Sistema de Correos
```bash
python enviar_correo_pago.py
```

### 3. Ejecutar el Webhook
```bash
python webhook_stripe.py
```

## 📧 Contenido del Correo

El correo incluirá:
- ✅ ID del pago
- ✅ Fecha y hora
- ✅ Total pagado
- ✅ Datos del cliente (nombre, email, teléfono)
- ✅ Dirección de envío completa
- ✅ Lista detallada de productos comprados
- ✅ Próximos pasos para el envío

## 🔍 Verificación

1. **Prueba local**: Ejecuta `python enviar_correo_pago.py`
2. **Prueba webhook**: Visita `https://tu-servidor.com/webhook-test`
3. **Prueba real**: Haz una compra de prueba en tu tienda

## 🛠️ Archivos Creados

- `enviar_correo_pago.py` - Sistema de envío de correos
- `webhook_stripe.py` - Webhook para recibir notificaciones de Stripe
- `instalar_dependencias_correo.py` - Instalador de dependencias
- `CONFIGURACION_CORREOS.md` - Este archivo de instrucciones

## ⚠️ Notas Importantes

1. **Seguridad**: Nunca subas el archivo `.env` a tu repositorio
2. **Producción**: Usa claves de Stripe en modo live para producción
3. **Gmail**: La contraseña de aplicación es específica para este sistema
4. **Webhook**: Debe estar en un servidor público (no localhost)

## 🆘 Solución de Problemas

### Error: "Invalid credentials"
- Verifica que la contraseña de aplicación de Gmail sea correcta
- Asegúrate de que la verificación en 2 pasos esté activada

### Error: "Webhook signature verification failed"
- Verifica que `STRIPE_WEBHOOK_SECRET` sea correcto
- Asegúrate de que la URL del webhook sea accesible públicamente

### No llegan correos
- Revisa la carpeta de spam
- Verifica que `anamaria.amrrg@gmail.com` sea correcto
- Comprueba los logs del servidor webhook
