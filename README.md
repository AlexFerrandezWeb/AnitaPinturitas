# Anita Pinturitas - Tienda Online de Cosmética Natural

## 📋 Descripción del Proyecto

Anita Pinturitas es una tienda online especializada en productos de cosmética natural, con un enfoque en marcas como Younique y Naturnua. La web ofrece una experiencia de compra completa con carrito de compras, procesamiento de pagos con Stripe, y un catálogo de productos organizado por categorías.

## 🌐 URL de Producción

- **Sitio Web:** https://anitapinturitas.com
- **Servidor Backend:** https://anita-pinturitas-server.onrender.com

## 🚀 Tecnologías Utilizadas

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos y diseño responsive
- **JavaScript (ES6+)** - Funcionalidad interactiva
- **Font Awesome** - Iconografía
- **Stripe.js** - Procesamiento de pagos

### Backend
- **Python 3.10** - Lenguaje de programación
- **Flask** - Framework web
- **Stripe API** - Procesamiento de pagos
- **CORS** - Cross-Origin Resource Sharing

### Hosting y Servicios
- **Hostinger** - Hosting del frontend
- **Render** - Hosting del backend
- **GitHub** - Control de versiones
- **Stripe** - Pasarela de pagos

## 📁 Estructura del Proyecto

```
anitaPinturitasV2/
├── 📄 Archivos HTML
│   ├── index.html              # Página principal
│   ├── carrito.html            # Carrito de compras
│   ├── productos.html          # Catálogo de productos
│   ├── producto.html           # Página individual de producto
│   ├── catalogo.html           # Catálogo por categorías
│   ├── registro.html           # Registro de usuarios
│   ├── success.html            # Página de éxito de compra
│   ├── envios.html             # Información de envíos
│   ├── politica-privacidad.html
│   ├── politica-devoluciones.html
│   └── terminos-condiciones.html
│
├── 🎨 Archivos CSS
│   ├── style.css               # Estilos principales
│   ├── carrito.css             # Estilos del carrito
│   ├── productos.css           # Estilos del catálogo
│   ├── producto.css            # Estilos de producto individual
│   ├── catalogo.css            # Estilos del catálogo
│   ├── reset.css               # Reset de estilos
│   ├── breadcrumbs.css         # Estilos de navegación
│   └── politica-privacidad.css
│
├── ⚡ Archivos JavaScript
│   ├── app.js                  # Funcionalidad principal
│   ├── carrito.js              # Lógica del carrito
│   ├── productos.js            # Lógica del catálogo
│   ├── producto.js             # Lógica de producto individual
│   └── catalogo.js             # Lógica del catálogo
│
├── 🐍 Backend Python
│   ├── payment_server.py       # Servidor principal de pagos
│   ├── stripe_server.py        # Servidor alternativo
│   ├── stripe_config.py        # Configuración de Stripe
│   ├── stripe_prod_config.py   # Configuración de producción
│   ├── stripe_test_config.py   # Configuración de pruebas
│   └── requirements.txt        # Dependencias Python
│
├── 📊 Datos
│   ├── productos.json          # Base de datos de productos
│   ├── catalogo.json           # Catálogo por categorías
│   ├── productos_facebook.csv  # Feed para Facebook
│   └── image_mapping.json      # Mapeo de imágenes
│
├── 🖼️ Recursos
│   └── assets/                 # Imágenes y recursos multimedia
│       ├── producto1.jpg - producto50.jpg
│       ├── foto-presentacion.jpg
│       └── placeholder.jpg
│
├── ⚙️ Configuración
│   ├── .htaccess               # Configuración Apache
│   ├── render.yaml             # Configuración de Render
│   ├── robots.txt              # Configuración SEO
│   ├── sitemap.xml             # Mapa del sitio
│   └── .gitignore              # Archivos ignorados por Git
│
└── 📚 Documentación
    ├── README.md               # Este archivo
    ├── SEO_RECOMENDACIONES.md  # Recomendaciones SEO
    ├── STRIPE_TEST_SETUP.md    # Configuración de Stripe
    └── FACEBOOK_FEED_SETUP.md  # Configuración del feed de Facebook
```

## 🛍️ Funcionalidades Principales

### 🏠 Página Principal (index.html)
- Hero section con productos destacados
- Navegación responsive
- Integración con Facebook Pixel
- SEO optimizado
- Enlaces a redes sociales

### 🛒 Carrito de Compras (carrito.html)
- Gestión de productos en el carrito
- Cálculo automático de totales
- Envío gratuito a partir de 62€
- Integración con Stripe para pagos
- Validación de formularios

### 📦 Catálogo de Productos (productos.html)
- Visualización de todos los productos
- Filtros por categoría
- Búsqueda de productos
- Paginación
- Enlaces a productos individuales

### 🎯 Página de Producto (producto.html)
- Información detallada del producto
- Galería de imágenes
- Botón de añadir al carrito
- Productos relacionados
- Meta tags optimizados

### 📋 Catálogo por Categorías (catalogo.html)
- Organización por líneas de productos
- Navegación por categorías
- Enlaces a productos específicos

## 💳 Sistema de Pagos

### Stripe Integration
- **Clave Pública:** `pk_live_51RiBJlAV1sSXblTcz3sH2w36Nd753TcxPOGaRFdj1qKLi1EfDqd3N6S1zXq8RTRVQgxv3SBT31uW3kmDKxZG1t6A00vdarrbHY`
- **Procesamiento:** Servidor Python en Render
- **URL del Servidor:** `https://anita-pinturitas-server.onrender.com`
- **Endpoints:**
  - `POST /crear-sesion` - Crear sesión de pago
  - `GET /facebook-feed.xml` - Feed de productos para Meta
  - `GET /test` - Endpoint de prueba
  - `GET /debug` - Diagnóstico del servidor

## 🔧 Configuración del Entorno

### Requisitos del Sistema
- Python 3.10+
- Node.js (para desarrollo local)
- Git
- Navegador web moderno

### Instalación Local
```bash
# Clonar el repositorio
git clone https://github.com/AlexFerrandezWeb/AnitaPinturitasV2.git

# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar servidor local
python payment_server.py
```

### Variables de Entorno
```bash
# Stripe
STRIPE_SECRET_KEY=sk_live_...

# Flask
FLASK_ENV=production
PORT=5000
```

## 📱 Responsive Design

La web está optimizada para:
- **Desktop** (1200px+)
- **Tablet** (768px - 1199px)
- **Mobile** (320px - 767px)

## 🔍 SEO y Marketing

### Meta Tags
- Títulos optimizados para cada página
- Descripciones meta personalizadas
- Keywords relevantes
- Canonical URLs
- Open Graph tags

### Analytics
- **Google Analytics:** G-BR8JHHRQL9
- **Facebook Pixel:** 638002358969786

### Sitemap y Robots
- `sitemap.xml` - Mapa del sitio
- `robots.txt` - Directivas para crawlers

## 🚀 Despliegue

### Frontend (Hostinger)
1. Subir archivos HTML, CSS, JS y assets
2. Configurar dominio `anitapinturitas.com`
3. Configurar SSL

### Backend (Render)
1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Desplegar automáticamente desde `main`

## 📊 Base de Datos de Productos

### Estructura (productos.json)
```json
{
  "categorias": [
    {
      "id": "categoria_id",
      "nombre": "Nombre de la categoría",
      "productos": [
        {
          "id": "producto_id",
          "nombre": "Nombre del producto",
          "precio": 29.99,
          "descripcion": "Descripción detallada",
          "imagen": "/assets/producto1.jpg",
          "url": "https://buy.stripe.com/..."
        }
      ]
    }
  ]
}
```

## 🎨 Diseño y UX

### Paleta de Colores
- **Primario:** #ff69b4 (Rosa)
- **Secundario:** #f8f9fa (Gris claro)
- **Acento:** #ff1493 (Rosa intenso)
- **Texto:** #333 (Gris oscuro)

### Tipografía
- **Principal:** Arial, sans-serif
- **Tamaños:** Responsive (rem units)

## 🔒 Seguridad

- HTTPS en producción
- Validación de formularios
- Sanitización de datos
- CORS configurado
- Variables de entorno para claves sensibles

## 📈 Rendimiento

- Imágenes optimizadas
- CSS y JS minificados
- CDN para recursos externos
- Caché del navegador
- Lazy loading de imágenes

## 🐛 Debugging y Logs

### Endpoints de Diagnóstico
- `GET /test` - Estado del servidor
- `GET /debug` - Información de archivos y configuración

### Logs del Servidor
- Logs de peticiones HTTP
- Errores de Stripe
- Diagnóstico de variables de entorno

## 📞 Soporte y Contacto

- **Desarrollador:** Alex Ferrandez
- **Cliente:** Ana María Ramos Rodríguez
- **Email:** [Contacto del cliente]
- **Web:** https://anitapinturitas.com

## 📝 Changelog

### v1.0.2
- Integración completa con Stripe
- Sistema de carrito funcional
- Feed de Facebook para Meta
- Optimización SEO
- Diseño responsive mejorado

### v1.0.1
- Estructura básica de la web
- Catálogo de productos
- Diseño inicial

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

---

**Última actualización:** Septiembre 2025
**Versión:** 1.0.2
