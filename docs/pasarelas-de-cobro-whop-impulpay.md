# Pasarelas de cobro de WHOP e Impul Pay

Fuente: 6 fotos de pantalla de Configuraciones → Pagos → tarjeta Impul Pay, lista "Métodos de pago locales del checkout" (capturas del 6/11/2026). Impul Pay lo opera Whop. Puede faltar algún método entre capturas y la lista puede haber cambiado desde entonces: ante la duda, volver a mirar el panel.

## Reglas que valen para todos
- Tarjeta, Apple Pay y Google Pay siempre están y no se pueden apagar.
- Los métodos locales aparecen **solo si el checkout le muestra al comprador su moneda local** (hay que tener Markets con ese país). Si ve otra moneda, paga con tarjeta.
- Qué métodos aparecen en cada país lo decide Whop (por país, moneda y monto). Prender un método en la lista no asegura que se muestre.
- **BNPL** (compra ahora, pagá después) = marcados con `*`: además requieren "financing aprobado" en la cuenta de Whop. Si no está aprobado, el comprador no los ve.
- **Vale** = el comprador paga después y la venta queda "Voucher pendiente" hasta que paga. Recién ahí se aprueba y sale la entrega.
- **ACH y BECS** se acreditan en días hábiles.
- PayPal aparece solo si el vendedor conecta PayPal en su cuenta de whop.com y PayPal admite la moneda. Estado de PayPal en las tiendas: sin conectar (verificado 2026-11-19).
- El usuario NO tiene Stripe. No proponerlo.

## Lista completa (37)

### Global
1. Tarjetas — todas las regiones
2. PayPal — monedero digital — todos los países con métodos locales

### Europa
3. iDEAL — EUR — adeudo bancario — Países Bajos
4. Bancontact — EUR — adeudo bancario — Bélgica
5. MB WAY — EUR — monedero digital — Portugal
6. Satispay — EUR — monedero digital — Italia
7. Alma* — EUR — BNPL — Bélgica, Alemania, Francia, España, Italia
8. Oney (3x / 4x)* — EUR — BNPL — Francia
9. Klarna* — EUR, GBP, USD, CAD, AUD — BNPL — Alemania, Austria, Francia, España, Italia, Irlanda, Reino Unido, EE.UU., Canadá, Australia

### Norteamérica y Oceanía
10. Débito bancario (ACH) — USD — adeudo bancario — EE.UU. (días hábiles)
11. Sezzle* — USD — BNPL — EE.UU.
12. PayTo — AUD — pagos en tiempo real — Australia
13. Débito BECS — AUD — adeudo bancario — Australia (días hábiles)

### Latinoamérica
14. OXXO — MXN — efectivo (vale) — México
15. SPEI — MXN — pagos en tiempo real (vale) — México
16. Kueski Pay* — MXN — BNPL — México
17. Pix — BRL — pagos en tiempo real — Brasil
18. Boleto — BRL — efectivo (vale) — Brasil
19. PSE — COP — adeudo bancario — Colombia
20. Nequi — COP — monedero digital — Colombia
21. Bre-B — COP — pagos en tiempo real — Colombia
22. Bancolombia — COP — adeudo bancario — Colombia
23. Efecty — COP — efectivo (vale) — Colombia
24. Addi* — COP — BNPL — Colombia
25. Mercado Pago — CLP — monedero digital — Chile
26. Sencillito — CLP — efectivo (vale) — Chile
27. Servipag — CLP — efectivo (vale) — Chile
28. Yape — PEN — monedero digital — Perú

### Asia, África y Medio Oriente
29. DuitNow QR — MYR — pagos en tiempo real — Malasia
30. GrabPay — MYR, SGD — monedero digital — Malasia, Singapur
31. ShopeePay — MYR — monedero digital — Malasia
32. Touch 'n Go — MYR — monedero digital — Malasia
33. GCash — PHP — monedero digital — Filipinas
34. AlipayHK — HKD — monedero digital — Hong Kong
35. M-Pesa — KES — monedero digital — Kenia
36. Tabby* — AED, SAR — BNPL — Emiratos Árabes, Arabia Saudita
37. Tamara* — AED, SAR — BNPL — Emiratos Árabes, Arabia Saudita

## Por país (qué ofrece Impul Pay además de tarjeta, Apple Pay y Google Pay)
- **Alemania:** PayPal (si se conecta), Alma*, Klarna*
- **Arabia Saudita:** Tabby*, Tamara*
- **Australia:** PayTo, Débito BECS, Klarna*
- **Austria:** Klarna*
- **Bélgica:** Bancontact, Alma*
- **Brasil:** Pix, Boleto
- **Canadá:** Klarna*
- **Chile:** Mercado Pago, Sencillito, Servipag
- **Colombia:** PSE, Nequi, Bre-B, Bancolombia, Efecty, Addi*
- **Emiratos Árabes:** Tabby*, Tamara*
- **EE.UU.:** ACH, Sezzle*, Klarna*
- **España:** Alma*, Klarna*
- **Filipinas:** GCash
- **Francia:** Alma*, Oney*, Klarna*
- **Hong Kong:** AlipayHK
- **Irlanda:** Klarna*
- **Italia:** Satispay, Alma*, Klarna*
- **Kenia:** M-Pesa
- **Malasia:** DuitNow QR, GrabPay, ShopeePay, Touch 'n Go
- **México:** OXXO, SPEI, Kueski Pay*
- **Países Bajos:** iDEAL
- **Perú:** Yape
- **Portugal:** MB WAY
- **Reino Unido:** Klarna*
- **Singapur:** GrabPay

**Sin método local en la lista (solo tarjeta, Apple Pay, Google Pay y PayPal si se conecta):** Dinamarca, Noruega, Suecia, Finlandia, Polonia, Suiza, Hungría, Grecia, Letonia, República Checa, Taiwán, Japón y el resto de los países no nombrados arriba.

## Lo que Whop NO ofrece (según la base de conocimiento de Impultienda)
BLIK, Przelewy24, Swish, Vipps, MobilePay (Dinamarca y Finlandia), EPS, Amazon Pay, Bizum, UPI, Cash App, Scalapay, Affirm, Afterpay/Clearpay, Webpay, PagoEfectivo, Revolut Pay, Mercado Pago de México y los métodos de Corea del Sur. Tampoco hay SEPA, giropay ni SOFORT en la lista.

Impul Pay no cobra en pesos argentinos (ARS) ni bolívares (VES), y Whop no admite compradores de países sancionados.

## Lectura para los mercados de plantillas cerámicas (hechos, 2026-11-19)
- **Países Bajos:** iDEAL SÍ está disponible (la tienda ya tiene mercado en EUR para NL). El cierre bajo del checkout no se explica por falta de iDEAL.
- **Bélgica:** Bancontact disponible. Hay que agregar Bélgica al mercado en EUR de la tienda holandesa.
- **Alemania / Austria:** tarjeta + PayPal (hay que conectarlo) + Alma*/Klarna* (requieren financing).
- **Francia:** tarjeta + Alma*, Oney*, Klarna*.
- **Dinamarca (el que funciona), Noruega, Suecia, Finlandia, Polonia:** solo tarjeta/Apple Pay/Google Pay. Faltan Vipps, Swish, BLIK y MobilePay.
