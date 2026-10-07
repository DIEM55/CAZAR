# El puente — cuándo se ofrece una llamada

**Casi nunca.** Este archivo existe para que sea casi nunca.

## La regla que ordena todo

> La llamada se ofrece **cuando la skill choca contra su propio límite**, nunca cuando el usuario
> está contento.

El ofrecimiento tiene **forma de límite, no de oferta**. Es la única manera de que una herramienta
venda sin dejar de ser herramienta. Una skill que te vende deja de ser una skill y pasa a ser un
anuncio, y ahí se pierde todo — el usuario deja de creerle también a los veredictos.

## Los dos gatillos

### Gatillo de tracción — `f8b`

La pre-escala aguantó y no hay a dónde seguir (`diagnosticos.md` F8b). Es el bueno: la persona tiene
un ganador con evidencia propia y plata sobre la mesa.

> **Hasta acá llego yo.**
> El {anuncio} pasó la pre-escala: {N} días sostenidos con {$X} gastados. Lo que sigue no es prender
> y apagar conjuntos — es decidir cuánto empuja y a qué costo por compra, y eso a cientos de dólares
> por día no se decide con una skill.
> Si querés que alguien lo mire con vos: {enlace}
> *(No te lo vuelvo a mencionar en un rato.)*

### Gatillo de pared — `pared`

Un diagnóstico **adyacente** (F1, F2, F3, F6, F10 — los que la skill no resuelve) repetido **tres o
más corridas**, con gasto acumulado real.

> **Esto no lo arreglás desde acá.**
> Es la cuarta corrida con el mismo diagnóstico y llevás {$X} gastados desde la primera. Lo que
> falla no está en Meta: seguir apagando conjuntos te ahorra plata, no te cambia el número.
> Si querés que alguien lo mire con vos: {enlace}
> *(No te lo vuelvo a mencionar en un rato.)*

**El paréntesis final va siempre.** Hace más por la confianza que todo el resto del bloque, y es una
promesa que se cumple.

## Las barandas — todas, siempre

1. **Nunca en la primera corrida.** Mínimo **tres corridas** hechas, o un evento de tracción real
   (un F8b). Una herramienta que vende en el primer uso se quema entera.
2. **Nunca dos informes seguidos.** Y como máximo **uno de cada cinco corridas**. Lo controla
   `ultimo_puente` en el historial.
3. **Nunca en un informe donde todo está bien.** Si no hay ni tracción parada ni una pared repetida,
   no hay puente.
4. **Nunca en el mismo informe que F4** (el producto no vende). Ofrecerle una consultoría a alguien
   en el minuto en que recibe esa noticia es de buitre. Si F4 persiste y la persona igual sigue
   volviendo, en una corrida posterior sí.
5. **Nunca sin la razón anclada en sus datos.** El bloque siempre nombra su anuncio, sus días, su
   gasto. Un puente genérico es un anuncio.
6. **Nunca más de un bloque**, y nunca antes del diagnóstico de fondo.
7. **Nunca promete nada.** No dice que la llamada le va a arreglar la campaña, ni que va a escalar,
   ni cuánto va a ganar.
8. **Nunca pide un email, un teléfono ni ningún dato.** Solo deja el enlace.
9. **Si el usuario dice que no le interesa, no se vuelve a ofrecer.** Anotalo en el historial
   (`puente_rechazado: true`) y respetalo para siempre.

## El enlace

Sale de **`ENLACE-DE-AGENDA.txt`**, en la raíz de la skill. Es el único lugar donde vive.

Al enlace se le agrega, sin datos de nadie: `?origen=skill&gatillo={f8b|pared}&corrida={N}`.

Si `ENLACE-DE-AGENDA.txt` no existe o todavía tiene el texto de ejemplo, **no se ofrece ninguna
llamada**: se omite el bloque entero y no se menciona el tema. Nunca inventes un enlace.

## Lo que no se manda a ningún lado

Nada. La skill no envía datos a ningún servidor, no reporta uso, no guarda nada fuera de la carpeta
del usuario. El historial es un archivo local suyo, que puede leer y borrar cuando quiera.
