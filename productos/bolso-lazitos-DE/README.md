# Schleifentasche · Bolso lazitos en alemán

Reconstrucción del PDF "Bolso lazitos" (comprado con derechos de reventa) para el
mercado germanoparlante: DE · AT · CH · LI · LU.

## Por qué se reconstruye y no se traduce

El PDF original es a su vez una **traducción automática rota del inglés**, con los
errores **quemados dentro de las imágenes**:

- "DIAGRAMA DE RECOLECCIÓN" ← *gathering diagram* (es fruncido, no recolección)
- "Hilvanando.fila 1: 0.5 crofnos.crudo borde" ← *basting row 1: 0.5 cm from raw edge*
- "HEM25-cmdoble pliegue - prensa amd pespunte" ← *press and topstitch* ("amd" = OCR roto)
- "GRAINLINE" y "Finished: 46 cm" quedaron sin traducir
- Pulgadas por todos lados: huella del original en inglés

Traducir eso al alemán habría heredado todos los errores.

## Qué cambia respecto del original

| | Original | Reconstruido |
|---|---|---|
| Diagramas | JPEG a 110-121 DPI | **Vectorial** (texto real, nítido a cualquier escala) |
| Peso | 1,7 MB | 100 KB |
| Calibración de impresión | No tiene | **Cuadrado de 10 cm** en página 1 |
| Unidades | cm + pulgadas mezcladas | Solo cm |
| Terminología | Traducción literal | Nahtzugabe · Fadenlauf · Stoffbruch · absteppen · Rüsche |

Formato A4 (210×297 mm) en ambos: no hubo que re-maquetar.

## Cómo regenerar el PDF

```bash
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --no-sandbox \
  --print-to-pdf=Schleifentasche-TEST-DE.pdf --no-pdf-header-footer \
  "file://$PWD/schleifentasche.html"
```

## Estado

- [x] Página de calibración (Testquadrat 10 cm)
- [x] Schnittteil 1 · Taschenkörper (42 × 51 cm)
- [ ] Portada + marca (pendiente: definir nombre comercial en alemán)
- [ ] Descripción, materiales y lista de corte (pp. 3-4 del original)
- [ ] Schnittteil 2 · Rüschenstreifen (280 × 23 cm)
- [ ] Schnittteil 3 · Träger (173 × 10 cm)
- [ ] Nähanleitung paso a paso — **ojo**: en el original los pasos están
      desordenados (arranca en el 8 y termina en el 3) y hay frases cortadas
- [ ] Fotos del producto terminado (reusar las del original)

## Pendiente legal antes de vender en DE/AT

Impressum en la web y renuncia expresa al Widerrufsrecht (14 días) antes de la
descarga, que es lo estándar para producto digital en esos mercados.
