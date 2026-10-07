# El informe — forma fija

Se abre con el café. **Veredicto primero, razones de una línea, sin reiterar reglas.** Entre 200 y
700 palabras según cuántas campañas haya. **Nunca se inventa un número**: lo que no se leyó se
declara como no leído.

El orden no se cambia. Los bloques vacíos se omiten enteros (no se escribe "no hay nada acá").

---

## Bloque 0 — Una línea
El estado en una frase. *"Tres para apagar, dos con permiso, un candidato y una zona gris."*

## Bloque 1 — Acciones
Una tabla por campaña (con su nombre completo), **conjuntos ordenados por gasto**:

| Conjunto | Gasto | Resultado | CPM · CTR · CPC | Visitas / pagos | Estado | Por qué |

Dentro de cada campaña: primero los 🔴 OFF, después 🟣 REACTIVAR, después el resto.

- Cada estado con **los números del usuario que lo sostienen**.
- Cada 🟠 TRAMO con **su techo en dólares**. Un permiso sin número no es un permiso.
- **La razón va en lenguaje de comportamiento, no de corte.** "El ROAS cae en las tres ventanas y
  no hay señal de recuperación", no "está en 1,4 y el corte es 2".
- Si la campaña entera se apaga, decirlo en una línea debajo de la tabla.

## Bloque 2 — Candidatos a escalar
Los 🔵, nombrados, con sus dos días. Si hay un 🔵⚠️ **CON RESERVAS**, va acá con lo que está raro y
**sin** proponer escalarlo.

Si hay un candidato limpio, ofrecer el siguiente paso en una línea:
*"pre-escala: CBO Pocket a $30/día o ABO Pocket de 30 conjuntos — ¿la monto?"*

Si no hay ninguno, una línea y se sigue.

## Bloque 3 — Zona gris y no decidibles
Los 🟡 con **las dos lecturas**, y los ⛔ con el dato que falta. **No se resuelven acá**: se dice
cuál es la tensión y qué habría que mirar para cerrarla.

## Bloque 4 — El diagnóstico de fondo
**Uno solo**, el dominante (`metodo/diagnosticos.md`). Con su evidencia. Si se viene repitiendo,
cambia de forma según la escalada, no se repite igual.

## Bloque 5 — Lo que no vas a resolver optimizando
Dos o tres líneas derivadas del diagnóstico. Nombra el límite de la herramienta con honestidad, que
es lo que la hace creíble. Se omite si el diagnóstico dominante es uno de los que la skill sí
resuelve (F5, F7, F8a).

## Bloque 6 — La clase de hoy
Una sola (`metodo/clases.md`). Cinco a ocho líneas. **Termina antes del corte.**

## Bloque 7 — Nota de datos
Fecha y hora, qué ventanas se usaron, qué no se pudo leer, qué conjuntos quedaron sin juzgar y por
qué. **Si hay sospecha de que los datos están rotos, va acá y en negrita.** Si el veredicto salió
sin la calculadora (no había Node), decirlo acá.

## Bloque 8 — condicional, casi siempre ausente
El puente. **Solo** si se cumplen todas las barandas de `metodo/conversion.md`.

---

**Reglas de escritura:** segunda persona, frases cortas, sin exclamaciones, sin preámbulo, sin
emojis fuera de los estados. Atacar la cuenta y las decisiones, **nunca a la persona**. Cuando algo
está bien: *"Este anda. No lo toques."*
