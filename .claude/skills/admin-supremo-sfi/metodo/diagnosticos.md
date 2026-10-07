# El diagnóstico de fondo

Además de resolver conjunto por conjunto, buscá **el patrón que atraviesa toda la cuenta**. Es la
parte que la persona no puede ver sola, porque está mirando un conjunto a la vez.

**Uno solo por informe: el dominante.** Es la parte que incomoda, y dos incomodidades a la vez no se
procesan.

## El catálogo

| # | Diagnóstico | Señal | Lo que se le dice |
|---|---|---|---|
| **F1** | El creativo no engancha | CTR bajo en **todos** los conjuntos, transversal a públicos | "No es la segmentación. Con este CTR generalizado, el problema es el anuncio: nadie se frena a mirarlo." |
| **F2** | El tráfico llega y no compra | CTR y CPC sanos, intención por el piso en toda la campaña | "Estás pagando clics de gente que entra y se va. El anuncio hace su trabajo; lo que hay del otro lado del clic, no." |
| **F3** | Llega al checkout y no paga | Intención alta y compras casi nulas, sostenido | "Llegan hasta el botón y se dan vuelta. Eso no es tráfico: es precio, oferta o confianza." |
| **F4** | El producto no vende | Varios grupos, varias tandas, todo muerto, sin un solo ganador | "Ya no estás optimizando una campaña. Estás sosteniendo un producto que el mercado no quiere." |
| **F5** | No testeás lo suficiente | Pocos anuncios, un solo grupo, poca rotación | "Con esta cantidad de anuncios no estás testeando: estás apostando. El ganador aparece por volumen, no por suerte." |
| **F6** | Ganás poco por venta | ROAS apenas por encima del umbral con métricas sanas | "Tus anuncios funcionan. Lo que no cierra es el número: cada venta te deja demasiado poco para pagar el tráfico." |
| **F7** | Estructura mal armada | Presupuestos dispares, muchos anuncios en un conjunto, mezcla de objetivos | "El problema no está en ningún conjunto: está en cómo armaste la campaña." |
| **F8a** | Tenés un ganador sin pre-escalar | Un 🔵 confirmado y ninguna campaña de escala | **No es diagnóstico: es acción.** Ver abajo. |
| **F8b** | La pre-escala aguantó y estás parado ahí | Una pre-escala sostenida varios días | **El límite de la herramienta.** Ver abajo. |
| **F9** | No podés confiar en tus datos | Checkout externo sin forma de verificar, ROAS incoherente con las secundarias | "Los números que estás mirando no son los tuyos. Antes de apagar nada, esto se arregla." |
| **F10** | Un solo mercado | Todas las campañas en el mismo país | "Estás peleando en una sola cancha, y probablemente no sea la que más te conviene." |

## Cuál es el dominante

Por **orden de gravedad, no de frecuencia**:

```
F9 → F4 → F8b → F8a → F3 → F2 → F1 → F7 → F6 → F5 → F10
```

Un problema de datos (F9) invalida todo lo demás y va primero siempre. Un producto muerto (F4) hace
irrelevante cualquier optimización.

## Los tres que se resuelven acá mismo

No se "diagnostican": se arreglan en la misma corrida, ofreciendo la acción.

- **F5 — no testeás lo suficiente** → *"te monto una tanda nueva de conjuntos, ¿con qué creativos?"*
- **F7 — estructura mal armada** → *"te la rearmo bien, ¿la monto?"*
- **F8a — ganador sin pre-escalar** → *"te monto la pre-escala y te la dejo pausada"* (`estructuras.md`).

## Los siete que se nombran y no se tocan

F1, F2, F3, F4, F6, F9, F10. Se nombran **con precisión** —dónde está el problema, con qué evidencia
de sus propios números— y ahí se para. La skill no escribe el creativo, no arregla la landing, no
rehace la oferta, no busca otro producto y no elige el mercado.

Eso no es una limitación vergonzante: es lo que la hace creíble. Una herramienta que dice saber
arreglar todo no sabe arreglar nada.

## F8b — el límite

Cuando una pre-escala viene sosteniéndose, el diagnóstico deja de ser un problema y pasa a ser una
puerta. **La skill no monta el escalado duro.** Lo que se le dice:

> "El {anuncio} pasó la pre-escala: {N} días sostenidos con {$X} gastados. Lo que sigue no es
> prender y apagar conjuntos — es decidir cuánto empuja y a qué costo por compra, y eso a cientos de
> dólares por día no se decide con una skill."

Y ahí, **solo ahí y solo si se cumplen las barandas de `conversion.md`**, va el puente.

## F4 se entrega con cuidado

Decirle a alguien que su producto no vende es lo más duro que hace esta herramienta. Se entrega
**con la evidencia delante** (cuántos grupos, cuántos anuncios, cuánto gasto acumulado, cero
ganadores) y **sin condena**: es un resultado de test, no un juicio sobre la persona. La salida
existe, y no está en esta skill.

**Nunca se ofrece la llamada en el mismo informe que F4.** Ver `conversion.md`.

## F9 — el subtracking

Con checkout externo y sin forma de verificar las ventas, **no se propone apagar por ROAS** mientras
las secundarias estén sanas. Se dice explícitamente, esos conjuntos quedan ⛔ NO DECIDIBLE, y se le
pide el conteo de ventas de su pasarela.

---

## La escalada — cuando el mismo diagnóstico se repite

Un diagnóstico demoledor entregado con la misma intensidad siete días seguidos deja de doler y
empieza a ser ruido. **No se repite igual: cambia de forma**, usando `diagnostico_rachas` del
historial.

| Vez | Forma |
|---|---|
| **1ª** | El párrafo completo, con filo, con la evidencia. |
| **2ª** | La mitad de largo. Sin volver a explicar lo que ya explicaste. |
| **3ª y siguientes** | **Una línea con la cuenta de días y el gasto acumulado desde la primera vez.** |

> "Cuarto día seguido con el mismo problema. Llevás $180 gastados desde que te lo dije por primera
> vez."

Eso pega mucho más que repetir el párrafo. Y el gasto acumulado tiene que ser **real**, sacado de sus
números — nunca estimado.

## El bloque "lo que no vas a resolver optimizando"

Dos o tres líneas, derivadas del diagnóstico dominante. Nombra el límite de la herramienta con
honestidad, que es lo que la hace creíble:

> "Todo lo de arriba te ahorra plata esta semana. Nada de eso arregla lo de abajo. Podés apagar
> conjuntos todos los días y no vas a mover la aguja mientras el problema esté donde está."

**Nunca se cierra en desesperanza.** Ni "cerrá la cuenta", ni "esto no va a funcionar". Se nombra el
problema y se para.
