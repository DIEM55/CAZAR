# Instalación de Admin Supremo de Sin Filtros

> Si querés la versión corta, está en `LEEME.txt`. Esto es el detalle.

## 1. Qué necesitás

| Qué | Obligatorio | Para qué |
|---|---|---|
| **Claude Code** (terminal, app de escritorio o web) | Sí | corre la skill |
| **El conector de Meta Ads** | No | leer tus campañas y crear las nuevas. Sin él funciona igual analizando **capturas de pantalla**; hace falta solo para que te **monte** campañas. |
| **Node.js ≥ 18** | No | la calculadora de veredictos. Sin Node la skill decide igual y te lo avisa en el informe. |

Ninguna llave, ningún pago, ninguna cuenta extra. **Nada de lo que le muestres sale de tu
computadora**: no hay servidor, no se reporta uso, no se guarda nada afuera.

## 2. Instalar

### Lo más fácil: que lo haga Claude Code

Guardá el zip donde quieras, abrí Claude Code y pegá esto cambiando la ruta:

> Instalá la skill que está en `"C:\Users\TU-USUARIO\Downloads\admin-supremo-sfi.zip"`:
> descomprimila en `~/.claude/skills/` (tiene que quedar la carpeta
> `~/.claude/skills/admin-supremo-sfi`), abrí su `SKILL.md`, corré `node tests/casos.mjs` si tengo
> Node, y hacé conmigo la configuración inicial.

### A mano

Descomprimí el zip dentro de `~/.claude/skills/`:

- **Windows:** `C:\Users\TU-USUARIO\.claude\skills\`
- **macOS / Linux:** `~/.claude/skills/`

Tiene que quedar `~/.claude/skills/admin-supremo-sfi/SKILL.md`. Cerrá y reabrí Claude Code.

Comprobación opcional, si tenés Node:

```bash
cd ~/.claude/skills/admin-supremo-sfi
node tests/casos.mjs
node scripts/veredicto.mjs plantillas/entrada.example.json
```

El primero tiene que terminar en **"Todos los casos pasan."**

## 3. El conector de Meta Ads

Se agrega desde los conectores de Claude, buscando **Meta Ads**, y se autoriza con la cuenta de
Facebook que tenga acceso a tu Business Manager.

Sin conector, la skill te va a pedir **capturas del Administrador de Anuncios a nivel conjunto de
anuncios**, con estas columnas: importe gastado, impresiones, clics en el enlace, CPM, CTR, CPC,
visitas a la página de destino, pagos iniciados, compras y valor de conversión. Pedila de **hoy**,
de los **últimos 3 días** y de **máximo**, e incluí los conjuntos apagados — ahí es donde más veces
aparece un anuncio que apagaste por error.

## 4. La configuración

La primera vez te hace dos o tres preguntas y guarda `admin-supremo-sfi.json` **en la carpeta donde
estés trabajando** (no dentro de la skill). Junto a él va `admin-supremo-sfi-historial.json`, que
es lo que le permite no repetirte la misma clase ni el mismo diagnóstico todos los días.

Los dos archivos son tuyos: podés abrirlos, leerlos y borrarlos. Borrar el primero reconfigura;
borrar el segundo hace que empiece de cero con las clases.

**Al actualizar la skill a una versión nueva, no los borres** — el zip no los trae justamente para
no pisártelos.

## 5. Cómo se usa

- **Analizar:** *"revisá mis campañas de hoy"*, *"qué apago"*. Devuelve un informe con un estado por
  conjunto. **Propone**; si querés que apague algo, pedíselo y lo hace uno por uno con tu OK.
- **Montar:** *"montame una campaña de testeo para X con estos creativos"*. Crea la ABO con la
  estructura del método y la deja **pausada**.
- **Pre-escalar:** cuando el informe marque un candidato, *"montá la pre-escala del AD3"*.
- **Aprender:** *"explicame el CPC"*, *"qué columnas tengo que poner en el Administrador"*.

**Todos los días**, una vez a la mañana antes de tocar nada. Y otra vez a las pocas horas de lanzar
una tanda nueva.

## 6. Actualizar a una versión nueva

Descomprimí el zip nuevo encima de la carpeta vieja. Tu configuración y tu historial no están
adentro del zip, así que sobreviven.

## 7. Problemas frecuentes

| Síntoma | Qué pasó | Qué hacer |
|---|---|---|
| "No veo ninguna cuenta publicitaria" | El conector entró con otro perfil, o no tenés rol en el Business Manager | Revisá con qué cuenta de Facebook iniciaste sesión y tu rol en la cuenta |
| Aparecen cuentas que no son tuyas | Tenés acceso por agencia o por trabajo | Elegí la tuya; queda guardada |
| Funcionaba y dejó de funcionar | El acceso del conector caducó | Volvé a conectar el conector de Meta Ads |
| `node` no se encuentra | No está instalado o no está en el PATH | No es obligatorio. Si lo querés: Windows `winget install OpenJS.NodeJS.LTS` · macOS `brew install node`, y reabrí la terminal |
| La skill no se activa sola | La frase no menciona campañas, anuncios ni Meta | Decí "revisá mis campañas", o invocala con `/admin-supremo-sfi` |
| Me dice que un conjunto es "no decidible" | Cobrás por una pasarela externa y Meta no ve todas tus ventas | Pasale el conteo de ventas de tu pasarela para ese período |
