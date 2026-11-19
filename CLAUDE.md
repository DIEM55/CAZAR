# Notas del proyecto (para Claude)

## Pagos
- **Antes de hablar de pasarelas, billeteras o métodos de pago por país, LEER `docs/pasarelas-de-cobro-whop-impulpay.md`** (lista completa de Impul Pay/Whop por región y por país). No contestar de memoria.
- El usuario NO tiene Stripe. No proponer Stripe ni "métodos locales de Stripe" como solución.
- Pasarela operativa en las tiendas de plantillas cerámicas (da, no, pl, nl, zh-TW): solo Impul Pay (Whop). PayPal, Mercado Pago, Stripe y transferencia: no conectados (verificado el 2026-11-19 con impultienda_ver_pagos).
- Si hay que mejorar el checkout fuera de Dinamarca, las opciones válidas son las que ofrezca Impul Pay/Whop, PayPal u otras pasarelas que el usuario confirme que tiene. Preguntar antes de asumir una.

## Producto y mercados
- Producto: método de plantillas cerámicas (tiendas en Impultienda, página de Meta "Ebooks del Futuro").
- Funciona en Dinamarca. Probados con peor resultado: Noruega, Polonia, Taiwán. Países Bajos en curso desde ~9 nov 2026.
- Excluir Latinoamérica / español al buscar mercados nuevos.
- Orden recomendado de lanzamiento (análisis del 2026-11-19): Alemania/Austria/Suiza, Suecia, Finlandia. Reservas: Francia, Países Bajos. Descartados por ahora: Grecia, Hungría.
