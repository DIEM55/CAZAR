# Las estructuras — qué se monta y con qué parámetros

Qué campaña va en cada momento de la vida de un creativo.

## El mapa

| Etapa | Cuándo | Estructura | Presupuesto | Pasa a la siguiente con |
|---|---|---|---|---|
| **1. Testeo** | producto nuevo o tanda nueva de creativos | **ABO de testeo**: 4-6 conjuntos (hasta 7), **1 anuncio por conjunto** | **$5/día mínimo** por conjunto · **$7 recomendado** | un ROAS alto sostenido **dos días seguidos** → ganador |
| 1b. Testeo de variaciones | hooks o formato de un anuncio que ya ganó | **CBO de testeo**: presupuesto en la campaña; desde 3 anuncios | **$20/día mínimo** en la campaña ($30 habitual) | ídem |
| **2. Pre-escala** | el anuncio es ganador | **CBO Pocket** (3-5 conjuntos, 1-5 ganadores por conjunto, con post ID) **o ABO Pocket** (30 conjuntos × $1,29) | Pocket **$30/día mínimo** | aguanta la escala uno o dos días → soporta más |
| **3. Escalado duro** | pasó la pre-escala | **Esta skill no lo monta.** Ver abajo. | — | — |

> **Un ganador nunca salta del testeo al escalado duro.** Siempre pasa por la pre-escala, cuyo
> único objetivo es averiguar si el anuncio soporta una escala más dura antes de ponerle plata de
> verdad encima.

### Cuándo ABO y cuándo CBO para testear

- **ABO** cuando se comparan **creativos distintos** uno contra otro: cada uno con su presupuesto,
  para que ninguno se quede sin datos porque Meta decidió por vos.
- **CBO de testeo** solo para **variaciones de un ganador** (hooks, formato, duración): misma
  estructura, presupuesto en la campaña, desde 3 anuncios.

### La pre-escala

- **Entrada:** un ganador confirmado (`analisis.md` §7). Con reservas, no entra.
- **CBO Pocket:** 3-5 conjuntos idénticos (`Conjunto 1` … `Conjunto 5`), en cada uno 1 a 5 anuncios
  ganadores cableados a su **post ID** — así conservan los comentarios, los me gusta y las
  compartidas que ya juntaron, que es la mitad de por qué funcionan. Presupuesto en la campaña,
  $30/día mínimo. Nombre: `PRODUCTO PAÍS CBO POCKET | ADn Gn | DD-MM-AA`.
- **ABO Pocket:** 30 conjuntos idénticos a **$1,29/día** cada uno, el mismo ganador por post ID.
  Nombre: `PRODUCTO PAÍS ABO ESCALADO | ADn Gn | DD-MM-AA`.
- **Se apaga si gastó demasiado sin una sola venta** — el corte lo calcula `veredicto.mjs` a partir
  del precio del producto. Si lo pasa, se juzga con las reglas normales de `analisis.md`.
- **Salida:** que sostenga el rendimiento uno o dos días. Ahí empieza el escalado duro, y ahí
  termina esta skill.

### El escalado duro — lo que es y por qué no se monta acá

Cuando la pre-escala aguanta, lo que sigue son estructuras que mueven **cientos o miles de dólares
por día**: campañas con puja por costo objetivo repartida en una escalera de conjuntos, o Pockets
con presupuestos varias veces más grandes. Se revisan cada pocas horas, se suben y se bajan en
caliente, y un error no se paga con veinte dólares.

**Explicá qué es si preguntan. No lo armes.** No es una limitación técnica: es que a esa altura las
decisiones dependen de márgenes, de caja, de capacidad de entrega y de cuánto aguanta la cuenta —
cosas que ninguna herramienta puede leer de tu Administrador. Ver `diagnosticos.md` F8b.

### Cuentas: testeo y escalado separados

La pre-escala y el escalado conviene que vivan en **otra cuenta publicitaria** que la de testeo, para
que la escala no le compita a la campaña de donde salió el anuncio. Es una práctica extendida entre
quienes escalan infoproductos, **no una regla confirmada por Meta** — se presenta así. Lo habitual es
tener al menos una cuenta de testeo y una de escala.

---

## Los parámetros de montaje

| Parámetro | Regla |
|---|---|
| **Objetivo / evento** | **Siempre Ventas, evento Compra** del píxel. No se optimiza a otro evento. Si "no ve compras" al principio es porque todavía no recibió el evento, no un motivo para cambiarlo. |
| **Píxel** | El usuario **asegura que esté bien instalado en todas partes** (página de venta y checkout). Antes de montar, verificar que exista y esté activo; si no hay evento Compra, avisar y no cambiar el objetivo. |
| **Segmentación** | **Ninguna** (broad): sin intereses, sin edad, sin género. |
| **Países** | **Por idioma del producto.** Idioma de un solo país → ese país (italiano → Italia, rumano → Rumania, checo → Chequia). Idioma de varios países → la región filtrando por idioma (francés → Europa completa + idioma francés). Español → preguntar. Inglés → **preguntar siempre**. |
| **Ubicaciones** | **Manuales, sin WhatsApp y sin Audience Network.** El default de la API mete WhatsApp sin avisar: pasar siempre el spec explícito (`api-meta.md`). |
| **Atribución** | **7 días clic / 1 día vista.** |
| **Nombres** | Campaña `PRODUCTO PAÍS \| GN \| ABO \| DD-MM-AA` (la fecha es la del arranque). Conjunto y anuncio: `ADn GN`. El usuario da producto, país y número de grupo; la abreviación del producto se fija la primera vez y no cambia. Una cuenta con nombres libres es ilegible a los tres meses. |
| **Hora de arranque** | **Preguntar: 00:00 o 02:00** del día siguiente, hora de la cuenta. Recomendar 02:00 cuando el mercado está adelantado: al despertar ya hay gasto y se frenan los conjuntos ineficientes antes de que se disparen. |
| **Creativos** | Videos o imágenes ya subidos a la biblioteca de la cuenta, o una URL pública. **Un creativo por conjunto.** |
| **Copys y títulos** | **Preguntar si los tiene.** Si no, **escribirlos**: texto primario + título + descripción, a partir de lo que dice el anuncio. CTA **Más información**. |
| **URL de destino** | La da el usuario, tal cual. |
| **Presupuesto mínimo** | **$5 por conjunto** (ABO) · **$20 por campaña** (CBO). Si no llega, se **achica la tanda** (menos conjuntos), nunca el presupuesto por conjunto: cuatro conjuntos con datos valen más que siete sin datos. |
| **Mejoras automáticas de Meta** | Las de contenido (Advantage+ creative) apagadas; "adaptar a la ubicación" puede quedar. El checkbox **Anuncios multianunciante** no tiene campo de API: **lo destilda el usuario a mano** en cada anuncio antes de que arranque. |
| **Activación** | Conjuntos y anuncios **activos**; **la campaña queda PAUSADA** y la prende el usuario después de revisar. |

**Dos umbrales dependen del precio del producto** — por eso se pregunta al arrancar: hasta dónde se
deja correr un conjunto sin una venta en testeo, y hasta dónde en pre-escala. Los calcula
`veredicto.mjs`; el informe dice el número en dólares, no la fórmula.
