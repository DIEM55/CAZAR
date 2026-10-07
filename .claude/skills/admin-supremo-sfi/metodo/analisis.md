# Cómo se juzga cada conjunto

Se recorre **en orden**. Cada paso o decide, o pasa al siguiente. Todo lo de acá se evalúa con datos
que Meta trae solo.

**Regla de oro de esta skill:** donde el criterio es ambiguo, **se declara, no se resuelve**. Con
dinero real, forzar una regla en un caso dudoso quema anuncios buenos. Los estados `ZONA GRIS`,
`CANDIDATO CON RESERVAS` y `NO DECIDIBLE` no son fallas de la herramienta: son el lugar donde el
criterio de un operador vale más que cualquier tabla.

---

## 0. Qué datos hacen falta

Por conjunto y por ventana:

| Dato | Campo de Meta (nivel `adset`) |
|---|---|
| Gasto | `amount_spent` |
| Impresiones, clics | `impressions`, `clicks` |
| CPM, CTR, CPC | `cpm`, `ctr`, `cpc` |
| Visitas a la página (LPV) | `landing_page_view` |
| Pagos iniciados (IC) | `omni_initiated_checkout` |
| Compras y valor | `offsite_conversion_fb_pixel_purchase`, `..._values` |
| ROAS | `purchase_roas` (o valor ÷ gasto) |
| Estado y presupuesto | `effective_status`, `daily_budget` |

**Ventanas:** `today`, `yesterday`, `last_3d`, `last_7d`, `maximum`. Para las rachas hace falta el
día por día (`time_increment: "1"`).

**Y dos datos que Meta no trae**, que están en la config: el **precio del producto** y el
**mercado**.

---

## 1. Orden: por gasto, de mayor a menor

Siempre. Donde hay más dinero en juego se decide primero. Vale para las campañas y para los
conjuntos dentro de cada campaña.

---

## 2. Sanidad de los datos, antes de juzgar nada

### 2.1. ¿Los pagos iniciados están rotos?

Un pago iniciado en 0 **no prueba nada por sí solo**: puede ser real. Lo que delata el fallo es una
**venta sin pago iniciado** — no se vende sin pasar por el checkout.

| Visitas | IC | Ventas | Lectura |
|---|---|---|---|
| > 0 | 0 | 0 | El dato **funciona**: nadie inició el checkout. La intención se puede mirar. |
| > 0 | 0 | ≥ 1 | **Imposible → el dato está roto.** Se descarta la intención **para toda la campaña**. |

La evidencia se lee **a nivel campaña**: si un conjunto vendió sin pago iniciado, a los demás
conjuntos de esa campaña ya no se les exige. El informe lo avisa.

### 2.2. ¿El ROAS es confiable?

Con **pasarela externa** (Hotmart, Kiwify y similares), Meta puede mostrar ROAS 0 con ventas
reales. Si las secundarias están sanas y el ROAS no cierra con ellas (CTR bien, CPC sano, visitas,
pagos iniciados y cero compras durante días), el conjunto se marca **NO DECIDIBLE por tracking** y
**no se propone apagar por ROAS**. Se le pide al usuario el conteo de ventas de su pasarela para ese
período.

**Regla de fondo:** *un ROAS que sabemos incompleto no ejecuta.* Cuando la pasarela cuenta más
ventas que Meta, la diferencia es tracking perdido, no ausencia de ventas, y el beneficio de la duda
va al conjunto.

---

## 3. Conjunto CON ventas → se decide por ROAS

Si el conjunto tiene al menos una venta en la ventana amplia, **las secundarias y los pagos
iniciados no se miran**. Venta > intención > secundarias, siempre.

### 3.1. La ventana que ejecuta es la más amplia que EXISTE

Nunca se decide con la foto de un solo día. Las ventanas 3d / 7d son "desde el inicio" truncadas:
manda **la más amplia que la campaña tenga**.

| Edad de la campaña | Ventana que ejecuta |
|---|---|
| 1 día | la venta salva: **MANTENER**. Un solo día no decide nada más |
| 2 días | ayer + hoy |
| 3 días | 3d |
| 5-7 días | 5d / 7d |
| más | 7d o desde el inicio |

- El **3d detecta, no ejecuta**: un 3d flojo con un 7d sano se deja.
- **"Hoy en cero" no apaga nada** si la ventana amplia aguanta.
- "Desde el inicio" se lee **solo con los conjuntos prendidos**.

### 3.2. El corte

| Situación | Acción |
|---|---|
| ROAS holgadamente por encima del corte en la ventana amplia | **MANTENER**. No lo toques. |
| ROAS claramente por debajo del corte en la ventana amplia | **OFF.** Sin redondeo. |
| ROAS **rondando el corte**, o ventana corta y larga en desacuerdo | **ZONA GRIS.** Se presentan las dos lecturas y decide el operador. |
| Días positivos y negativos alternados sin tendencia | **ZONA GRIS.** Un patrón inestable no se ejecuta desde una tabla. |

El corte está en la calculadora. **No se publica en el informe**: la razón se escribe en lenguaje de
comportamiento ("el ROAS cae en las tres ventanas y no hay señal de recuperación"), no de número de
corte.

### 3.3. Rachas de ceros

- **3 días consecutivos con cero ventas → OFF**, aunque las ventanas amplias den bien: esos números
  son arrastre.
- En campañas más jóvenes que 3 días: **toda la vida del conjunto en cero → OFF**.
- Un día suelto en cero no apaga nada.

---

## 4. Conjunto SIN ventas → piso, secundarias, intención

### 4.1. El piso de gasto: nada se juzga antes

Debajo del piso el conjunto queda **ESPERAR** y se relee más tarde. Un conjunto que no llegó al piso
no tiene suficiente información para condenarlo ni para salvarlo.

**Excepción — lo catastrófico ejecuta antes del piso.** CPM y CTR son señales *estructurales*: no se
corrigen con más gasto. Un CPM de $35 con $2 gastados sigue siendo $34 con $3.

- **CTR en 0 %** con impresiones suficientes (nadie hizo clic) → **OFF**.
- **CTR por el piso** con impresiones suficientes → **OFF**. No va a subir gastando treinta centavos
  más.
- **CPM catastrófico para el mercado** → **OFF** en el acto.

### 4.2. Las secundarias

Las bandas de CPM cambian por mercado; CTR y CPC son iguales en todos lados. Están en la
calculadora.

**El CPC es el árbitro.** Ni un CTR alto ni un CPM bajo salvan un CPC roto: un CTR del 8 % con un
CPC de un dólar significa que le gustó a gente que no te iba a comprar. El perdón de un CPM alto se
cobra en el CPC.

La cuenta de cuántas secundarias están fuera de banda, y cuál, es lo que decide entre OFF y TRAMO.
**Cuando el resultado queda en el borde** — una sola métrica floja y el resto sano, con la intención
justo en la raya — el estado es **ZONA GRIS**, no una decisión forzada.

### 4.3. Intención: pagos iniciados sobre visitas a la página

Se aplica solo si el dato no está roto (2.1). Con el dato roto, el conjunto se juzga por CPM, CTR y
CPC solamente, y el informe lo avisa.

- **Tráfico sin intención** (muchas visitas, casi ningún pago iniciado) → **OFF**, aunque CPM, CTR y
  CPC estén perfectos. Estás pagando clics de gente que entra y se va.
- **Con intención clara** → el conjunto compra tiempo: **TRAMO**.
- **En el medio** → **ZONA GRIS**.

Con pocas visitas el ratio no significa nada todavía: se usa como señal de presencia o ausencia, no
como porcentaje.

### 4.4. El techo: todo permiso lleva su número

Un conjunto sin ventas que se deja correr **se deja hasta un techo en dólares, dicho en el informe**.
Si llega al techo sin vender, se apaga.

- El techo **se dice siempre**: "TRAMO hasta $X". Un permiso sin número no es un permiso, es un
  descuido.
- El techo **no es infinito ni renovable de oficio**. Esta skill da el techo del tramo actual; qué
  pasa cuando ese techo se agota y las métricas siguen sanas es una decisión de criterio, y se
  declara como tal.
- **El gasto no apaga solo: apaga el gasto sin métricas que lo justifiquen.**
- Al revisar una cuenta, buscá primero el patrón más caro que existe: **gasto alto + cero ventas +
  secundarias flojas**. Eso no es una decisión difícil, es una vigilancia que falló.

---

## 5. CBO (presupuesto en la campaña)

- Mismas reglas. Se ordena por gasto y se juzgan **solo los conjuntos que pasaron el piso**; los que
  están debajo ni se evalúan ni se apagan.
- El reparto es desparejo, no unipersonal.
- **Apagar es redirigir presupuesto**: lo que gastaba el conjunto apagado fluye al ganador. Es una
  palanca activa, no solo un corte.
- La **pre-escala** es más paciente que una ABO de testeo: las secundarias buenas compran más
  tiempo. Tiene además su propio corte por gasto sin venta, en la calculadora.

---

## 6. La campaña

- Si al apagar el último conjunto la campaña queda vacía → **se apaga la campaña**.
- Si ningún conjunto prendido vendió nunca desde el inicio → **se apaga la campaña**.
- Al día 1 sin ventas, la campaña se lee conjunto por conjunto; no se juzga en bloque.

---

## 7. Candidatos a escalar

Un ganador es un conjunto que **sostuvo un ROAS alto dos días individuales seguidos**, mejor si
viene subiendo.

**Antes de declararlo, mirá la forma de la curva**, no solo los dos días:

| Lo que ves | Estado |
|---|---|
| Dos días sostenidos, curva estable o subiendo, intención intacta | 🔵 **CANDIDATO A ESCALAR** |
| Pasa los dos días **pero** la curva viene cayendo día a día, o la intención se degrada con las visitas intactas | 🔵⚠️ **CANDIDATO CON RESERVAS** — se nombra, se dice qué está raro, y **no se propone escalar todavía**. Pedir los días individuales y volver a mirarlo mañana. |

Un candidato confirmado va a **pre-escala**, nunca directo al escalado duro (`estructuras.md`).

---

## 8. Revisar también los apagados

Un conjunto apagado cuya ventana amplia **sigue sana** se **re-prende a prueba con sentencia**: se
le da un techo corto en dólares y si lo gasta sin vender, off definitivo.

Encontrarle a alguien un anuncio que apagó por error es de las cosas más valiosas de cada corrida.
Por eso se piden **siempre** también los conjuntos apagados.

---

## 9. Presupuesto en ABO

La base es la de la tanda. Un conjunto que va muy bien varios días se puede subir a nivel conjunto.
Cuando decae, **se vuelve a la base — no se apaga**. Desescalar no es matar.

---

## 10. Los estados (exactamente uno por conjunto)

| Estado | Cuándo |
|---|---|
| 🔴 **OFF** | Cualquier regla de apagado. |
| 🟢 **MANTENER** | Vende y la ventana amplia aguanta. |
| 🟠 **TRAMO hasta $X** | Sin ventas, pero las métricas compran tiempo. **Siempre con el número.** |
| ⚪ **ESPERAR** | No llegó al piso y nada catastrófico. |
| 🔵 **CANDIDATO A ESCALAR** | Ganador confirmado. |
| 🔵⚠️ **CANDIDATO CON RESERVAS** | Pasa el filtro pero la curva o la intención no acompañan. |
| 🟣 **REACTIVAR A PRUEBA** | Apagado cuya ventana amplia sigue sana. |
| 🟡 **ZONA GRIS** | Lecturas en desacuerdo. Se presentan las dos. |
| ⛔ **NO DECIDIBLE** | Tracking roto o ROAS implausible. Se pide el dato que falta. |

**Cada estado va con su razón en lenguaje de comportamiento, no con su número de corte.**

> "Apagá este conjunto: el ROAS cae en las tres ventanas y no hay señal de recuperación." ✅
> "Apagalo: está en 1,4 y el corte es 2." ❌
