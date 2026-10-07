# Muestras

Pruebas de capacidad, no parte de ningún producto.

## gato-astronauta.svg / .png

Demostración de ilustración **vectorial** (SVG escrito a mano, rasterizado con
Chromium headless a 1600×1600). Sirve como plantilla: degradados radiales para
fondos, lineales para volumen, y agrupación por partes para poder editar un
elemento sin tocar el resto.

Es el mismo motor que produce los diagramas de `productos/bolso-lazitos-DE/`.

**Qué prueba:** que portadas, íconos y separadores se pueden hacer sin ningún
generador de imágenes conectado.

**Qué no cubre:** fotorrealismo y mockups de producto. Para eso hace falta un
generador (Higgsfield u otro), hoy desconectado.

Rasterizar:

```bash
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --no-sandbox \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=800,800 \
  --screenshot=salida.png "file://$PWD/pagina-con-el-svg.html"
```
