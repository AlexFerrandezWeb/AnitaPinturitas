<?php
// LÍNEA 1 (MUY IMPORTANTE): Le decimos al navegador que esto es un archivo XML.
header("Content-Type: text/xml; charset=utf-8");

// LÍNEA 2 (LA CLAVE): Imprimimos la declaración XML como un texto usando 'echo'.
echo '<?xml version="1.0" encoding="UTF-8"?>';

// A partir de aquí, el resto del código que genera el feed
echo '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">';
echo '<channel>';
echo '<title>Anita Pinturitas - Productos</title>';
echo '<link>https://anitapinturitas.es</link>';
echo '<description>Catálogo de productos de Anita Pinturitas</description>';
echo '<lastBuildDate>' . gmdate('D, d M Y H:i:s') . ' GMT</lastBuildDate>';

// Cargar productos desde JSON
$productos_json = file_get_contents('productos.json');
$data = json_decode($productos_json, true);

$total = 0;

foreach ($data['categorias'] as $categoria) {
    $categoria_nombre = $categoria['nombre'];
    echo "\n";
    
    foreach ($categoria['productos'] as $producto) {
        $total++;
        
        // Procesar imagen
        $imagen_url = $producto['imagen'];
        if (strpos($imagen_url, '/') === 0) {
            $imagen_url = 'https://anitapinturitas.es' . $imagen_url;
        } elseif (!strpos($imagen_url, 'http') === 0) {
            $imagen_url = 'https://anitapinturitas.es/' . ltrim($imagen_url, '/');
        }
        
        // Crear item con campos OBLIGATORIOS de Meta
        echo '<item>';
        
        // 1. g:id (OBLIGATORIO) - Identificador único
        echo '<g:id>' . htmlspecialchars($producto['id']) . '</g:id>';
        
        // 2. g:title (OBLIGATORIO) - Título con mayúscula inicial
        $titulo = ucwords($producto['nombre']);
        echo '<g:title><![CDATA[' . $titulo . ']]></g:title>';
        
        // 3. g:description (OBLIGATORIO) - Descripción detallada
        echo '<g:description><![CDATA[' . $producto['descripcion'] . ']]></g:description>';
        
        // 4. g:availability (OBLIGATORIO) - Disponibilidad
        echo '<g:availability>in stock</g:availability>';
        
        // 5. g:condition (OBLIGATORIO) - Estado del producto
        echo '<g:condition>new</g:condition>';
        
        // 6. g:price (OBLIGATORIO) - Precio con formato correcto
        $precio = number_format((float)$producto['precio'], 2, '.', '');
        echo '<g:price>' . $precio . ' EUR</g:price>';
        
        // 7. g:link (OBLIGATORIO) - Enlace al producto
        echo '<g:link>https://anitapinturitas.es/producto.html?id=' . urlencode($producto['id']) . '</g:link>';
        
        // 8. g:image_link (OBLIGATORIO) - URL de la imagen
        echo '<g:image_link>' . htmlspecialchars($imagen_url) . '</g:image_link>';
        
        // 9. g:brand (OBLIGATORIO) - Marca
        echo '<g:brand>Anita Pinturitas</g:brand>';
        
        // Campos adicionales recomendados
        echo '<g:product_type><![CDATA[' . $categoria_nombre . ']]></g:product_type>';
        echo '<g:google_product_category>Health &amp; Beauty &gt; Personal Care &gt; Cosmetics</g:google_product_category>';
        
        echo '</item>';
        echo "\n";
    }
}

echo '</channel>';
echo '</rss>';
?>
