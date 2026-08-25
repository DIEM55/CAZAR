---
name: winners-free
description: Encuentra productos winner en Facebook Ads Library en todo el mundo sin gastar en ads, los puntúa en dos ejes (validación y oportunidad) y devuelve una Ficha de Caza lista para modelar. Usar cuando el usuario dice "winners free", "cazar", "buscar winner", "buscar whales", "analizar nicho", "espiar ads" o pide investigar un mercado.
---

# WINNERS FREE · v2

Caza de productos winner en Ads Library. Módulo 1 del Sistema Sin Filtros.

Skill autónoma. El argumento es el **nicho o keyword** a investigar (ej: "recetas keto", "IA para abogados"). Corre sola y devuelve una **Ficha de Caza** por cada candidata que pasa el filtro, más un registro acumulado de todo lo cazado.

Es el **Módulo 1** del sistema: `/winners-free` → `/modelar` → `/lanzar`. La Ficha de Caza es el input del módulo siguiente, así que se completa entera aunque falte algún dato (marcando el hueco).

## Qué hace

1. Barrido mundial sin filtro de país.
2. Separa infoproducto real del ruido local por footprint.
3. Cuenta el arsenal completo de cada candidata (el paso que separa al que parece grande del que lo es).
4. Puntúa en **dos ejes independientes** y da veredicto por matriz.
5. Emite la Ficha de Caza y actualiza el registro.

## Requisito ⚠️

Usa `ads_library_search` del **conector oficial de Meta** (el de Facebook, NO un MCP de terceros). Tiene que estar instalado y con al menos una cuenta de ads activa en la sesión. Si está diferida, cargarla con ToolSearch.
- Es **solo lectura**: no toca la cuenta ni crea nada → cero riesgo de baneo.
- **Fallback sin conector**: caza manual en `facebook.com/ads/library` vía Chrome MCP, con los mismos filtros y la misma lectura de señales. Más lento, mismo resultado.

---

## Paso 1 — Barrido mundial

Llamar a `ads_library_search` con:
- `search_terms`: **una** keyword por llamada (matchea el texto del creativo). 3-5 variaciones del nicho.
- `countries`: **omitir** → busca en todos los países. Así cae el whale que se esconde detrás del snapshot de un solo país.
- `ad_active_status`: `ACTIVE`.
- `limit`: hasta 50.
- `advertiser_request`: el pedido del usuario con sus palabras.

**Generar keywords por 4 ejes:**
| Eje | Ejemplos |
|---|---|
| Formato | ebook, guía, plantilla, kit, método, protocolo, desafío |
| Compra impulsiva | en 7 días, sin dieta, paso a paso, desde casa |
| Footprint técnico | hotmart, gumroad, payhip, kiwify (como texto del creativo) |
| Traducción | método, segredo, desafio, renda extra, secar barriga, reconquista |

Brasil suele ser la cuna de las olas low-ticket → correr siempre las variantes en portugués aunque el objetivo sea otro mercado.

## Paso 2 — Filtrar el ruido

Una keyword genérica trae basura local: clínicas, nutricionistas, farmacias, marcas personales. Antes de contar arsenales, descartar:
- Marcas personales (no modelables).
- Follow-me ads (perfiles que solo juntan seguidores, no venden).
- Redes de novelas/apps camufladas con copy del nicho (cloaking).
- Ecommerce físico si buscás infoproducto.

## Paso 3 — Contar el arsenal · el paso clave

Por cada candidata: `ads_library_search` con `page_ids: ["<id>"]` → devuelve **todos** sus ads. Ahí se ve el arsenal real y la antigüedad del ad más viejo activo.

> Una página puede mostrar 13 ads en el barrido y tener solo 14 en total. Otra muestra 13 y tiene 126. El barrido no distingue: este paso sí.

**El filtro madre escala por tamaño de mercado.** El umbral fijo de 50 hace que todo mercado chico dé "descartar", que es justo la señal de hueco leída al revés:

| Mercado | Umbral de winner |
|---|---|
| BR · US · MX · ES | 50+ ads activos |
| IT · FR · DE · PT | 20+ ads activos |
| Nórdicos · Europa del Este | 12+ ads activos |

Más el requisito de antigüedad: el ad **más viejo activo** arrancó hace **3+ días**. Lo que arrancó hoy es un tester validando. Ojo: volumen alto de ads nuevos NO descalifica — es señal de que está escalando ahora mismo. Se mira el más viejo, no los nuevos.

## Paso 4 — Capturar la oferta (obligatorio)

Sin esto la ficha no sirve para modelar. Por cada candidata que pasó el filtro, entrar a la landing y registrar:
- **Precio** y moneda. Si hay order bump o upsell visible, anotarlo.
- **Formato del producto**: ebook, curso, plantillas, comunidad, servicio.
- **Plataforma de checkout**: Hotmart, Kiwify, Shopify, Stripe, etc. Delata el nivel de madurez del operador.
- **Estructura de la landing**: VSL, texto largo, quiz, directo a checkout.
- **Garantía y escasez** que usan.

## Paso 5 — Extraer los hooks

Identificar los **3 creativos más duplicados** del arsenal. Un creativo repetido 10-20 veces ya ganó el test interno del anunciante: son los ángulos a modelar primero.

De cada uno, transcribir la **primera línea o los primeros 3 segundos** y nombrar el dolor que ataca. Eso alimenta directo el guion de video.

## Paso 6 — Cruce de demanda

La Ads Library muestra **oferta**, no demanda. Antes de dar veredicto, chequear que haya gente buscando esto y no tres tipos peleándose por nada:
- Volumen de búsqueda del término principal (Google Trends: tendencia a 12 meses, no solo el pico).
- Existencia de comunidades activas (subreddits, grupos de FB, foros) con gente pidiendo la solución.
- Si hay oferta fuerte y cero demanda rastreable fuera de Meta → la ola puede estar muriendo.

---

## Scoring · dos ejes

El score único de 4 señales mezclaba dos preguntas distintas. Van separadas.

### Eje A — VALIDACIÓN (0-3) · ¿esto es un winner real?
| Punto | Señal |
|---|---|
| ① | **Longevidad** — mismos ads corriendo 45+ días sin pausa |
| ② | **Volumen** — supera el umbral de su mercado sobre la MISMA oferta |
| ③ | **Duplicación** — un mismo creativo repetido 10+ veces, todos a la misma landing |

Señal extra que suma certeza (no puntúa, pero anotala): la misma oferta corriendo en 5-10 fanpages distintas = se esconde de los cloners, convierte seguro.

### Eje B — OPORTUNIDAD (0-3) · ¿hay lugar para mí?
| Punto | Señal |
|---|---|
| ① | **Hueco de mercado** — 0-3 players débiles en un destino prioritario |
| ② | **Ángulo libre** — el dolor principal no está saturado en ese destino |
| ③ | **Demanda confirmada** — el cruce del Paso 6 dio positivo |

### Veredicto por matriz

|  | **Oportunidad 2-3** | **Oportunidad 0-1** |
|---|---|---|
| **Validación 2-3** | 🟢 **COPIAR** — armá el test esta semana | 🟡 **ARBITRAJE** — modelá y lanzá en otro mercado |
| **Validación 0-1** | 🟠 **WATCHLIST** — revisar en 30 días | 🔴 **DESCARTAR** — con el motivo anotado |

El eje de competencia se lee aparte, contando cuántos anunciantes distintos atacan la misma promesa: 2-6 con gasto sostenido y ninguno dominando = espacio. 7+ con creativos calcados = saturado, apuntá a un avatar más específico. Un solo jugador con 100+ ads = no le compitas de frente, modelá y mudate de mercado.

## Arbitraje multi-mercado

Si sale un winner fuerte, chequear si el ángulo está libre en otro lado: misma búsqueda con `countries: ["<ISO-2>"]` y el término traducido.

**Orden de prioridad de destino:** 1) inglés · 2) Europa (IT/FR/DE) · 3) LATAM · 4) Brasil.
Se **modela** desde el mercado fuente (saturado, funnels maduros) y se **lanza** en un destino con pocos players débiles. Si en el destino ya hay testers con ads de pocos días, la ventana se está cerrando: entrás ya o no entrás.

---

## Output · Ficha de Caza

Una ficha por candidata que llegó a COPIAR o ARBITRAJE. Formato fijo:

```
FICHA DE CAZA · [nombre de la oferta]
Fecha: [dd/mm] · Nicho: [keyword] · Veredicto: [COPIAR / ARBITRAJE]

01 · EL JUGADOR
Página: [nombre] · [link a su Ads Library]
Landing: [url]
Ads activos: [n] · Más viejo: [n] días · Mercados: [países]

02 · LA OFERTA
Producto: [formato] · Precio: [monto + moneda]
Backend visible: [order bump / upsell / ninguno]
Checkout: [plataforma] · Landing: [VSL / texto largo / quiz]
Garantía: [cuál] · Escasez: [cuál]

03 · LOS ÁNGULOS
Hook 1 (repetido [n]x): "[primera línea]" → dolor: [cuál]
Hook 2 (repetido [n]x): "[primera línea]" → dolor: [cuál]
Hook 3 (repetido [n]x): "[primera línea]" → dolor: [cuál]
Snapshots: [ad_snapshot_url de cada uno]

04 · SCORE
Validación: [n]/3 — [qué señales cumple]
Oportunidad: [n]/3 — [qué señales cumple]
Competencia: [n] anunciantes atacando la misma promesa

05 · JUGADA
Mercado fuente: [país] → Mercado destino: [país]
Qué copiar tal cual: [lista]
Qué cambiar: [lista]
Riesgo principal: [cuál]

06 · HUECOS DE INFORMACIÓN
[Lo que no se pudo verificar y hay que chequear a mano]
```

Guardar como `winners/[nicho]-[dd-mm].md`.

## Registro acumulado

Mantener `winners/00-registro.md` con **todo** lo cazado, incluidos los descartes. Una línea por candidata:

`[fecha] | [nicho] | [página] | V:[n]/3 O:[n]/3 | [veredicto] | [motivo en 5 palabras]`

Sirve para tres cosas: no repetir nichos ya quemados, tener la watchlist de los que quedaron en validación baja para revisar a los 30 días, y detectar patrones propios (qué tipo de nicho te da winners y cuál te hace perder tiempo).

Antes de arrancar una caza nueva, leer el registro y avisar si el nicho ya se cazó antes.

## Handoff

Al cerrar, indicar el paso siguiente concreto según el veredicto:
- **COPIAR** → pasar la ficha a `/modelar` para armar avatar, oferta y ángulos.
- **ARBITRAJE** → repetir el barrido en el mercado destino para confirmar el hueco, después `/modelar`.
- **WATCHLIST** → agendar revisión a 30 días.

---

**Recordatorio:** el whale valida la **OFERTA**, no te salva de un test sucio. Landing degradada, pixel ciego o un solo conjunto queman igual. La caza te dice qué copiar; lo demás es ejecución.
