"""Genera informe.html (página publicable) a partir de datos.py."""
import html, os
import datos

E = html.escape
P = sorted(datos.P, key=lambda x: -x["score"])

TOP7 = [
    dict(n=1, ref=1, titulo="Fichas de diagnóstico para técnicos de aire acondicionado",
         modelo="100 Fichas de Fallas de Aire Acondicionado (ES) · 100 Fiches de Pannes (FR) · 100 Schede di Guasti HVAC (IT)",
         datos="≈38 anuncios activos entre 2 páginas · anuncio más viejo del 30-ago (37 días) · ya traducido a 3 idiomas",
         por_que="Es el único producto del estudio donde el operador ya probó la traducción: el mismo pack corre en español, francés e italiano. Nicho de oficio, comprador con plata (cada diagnóstico bien hecho le paga la visita) y poca competencia: 3-4 anunciantes.",
         lanzar="PT-BR primero (Brasil: verano + la mayor base de técnicos de LATAM), después Argentina, Chile, Paraguay y Uruguay en ES. En el norte, versión \"bombas de calor y calefacción\" para España e Italia.",
         idioma="Portugués de Brasil y español rioplatense", precio="US$9-17 / R$37-67 + order bump \"fichas de placas inverter\"",
         riesgo="Bajo. Escribí fichas propias: no copies el PDF de la competencia."),
    dict(n=2, ref=8, titulo="Workbook de regulación del sistema nervioso (y estudio bíblico)",
         modelo="Printable WITH Lisa (EE. UU.)",
         datos="79 anuncios activos · desde 16-sep · retargeting \"You came back…\" · siempre \"90% off\"",
         por_que="La página tiene 79 anuncios y rota productos (sistema nervioso, ejercicios somáticos, Biblia, fonética, regulación emocional para adolescentes) sobre una misma promesa de precio. \"Regular el sistema nervioso\" está creciendo en español y casi nadie lo vende como workbook imprimible.",
         lanzar="México, Colombia, España y la comunidad hispana de EE. UU. La línea bíblica funciona muy bien en México, Guatemala y Colombia.",
         idioma="Español neutro", precio="US$7-12 con precio ancla tachado; bump \"versión para adolescentes\"",
         riesgo="Medio: el original dice \"the cure for anxiety\". Usá \"herramientas para calmar tu cuerpo\", nunca \"cura\"."),
    dict(n=3, ref=6, titulo="\"50 adornos navideños en fieltro\" (colecciones por temporada)",
         modelo="Universo do Feltro (Brasil)",
         datos="≈66 anuncios activos · desde 10-sep · nueva colección cada 1-2 semanas (Halloween → Navidad)",
         por_que="Encadena colecciones de 50 moldes por fecha, así que siempre tiene algo nuevo que anunciar. En español hay vendedoras de fieltro, pero ninguna con este formato de colección; además la Navidad empieza ya.",
         lanzar="España, México, Colombia, Perú y Chile, de octubre a mediados de diciembre. Después: San Valentín, Día de la Madre, Pascua.",
         idioma="Español neutro (\"fieltro\", \"moldes\")", precio="US$5-9 por colección; bump \"pack de 3 colecciones\"",
         riesgo="Bajo. Ojo con personajes con licencia (Disney, El Chavo): usá diseños genéricos."),
    dict(n=4, ref=2, titulo="Guía NCLEX con advertorial \"Leé esto si estás estudiando para el NCLEX\"",
         modelo="Maya Bennett (Canadá/EE. UU.) + Alexa Paige (mismo copy)",
         datos="72 anuncios activos · ≥27 con más de 20 días · el más viejo del 5-sep",
         por_que="Un solo gancho escalado a 72 anuncios durante un mes es una señal clara de que vende. El comprador gana en dólares, y hay ocho o más anunciantes de NCLEX, lo que confirma la demanda sin saturarla.",
         lanzar="Inglés para EE. UU., Canadá y Filipinas (la mayor exportadora de enfermeros). Segunda versión: \"NCLEX para enfermeros hispanohablantes\" en México, Colombia y Puerto Rico.",
         idioma="Inglés y español", precio="US$9-19; bump \"300 preguntas tipo examen\"",
         riesgo="Bajo. No prometas \"aprobado garantizado\"."),
    dict(n=5, ref=14, titulo="Mapas visuales técnicos (mecánica industrial, automatización, ingeniería civil)",
         modelo="Mapas Visuales PRO (Perú), que ya exporta a Italia",
         datos="23 anuncios activos · más viejo del 18-sep (18 días: le faltan 2 para cumplir el filtro)",
         por_que="El nicho de mapas para salud está saturado (11 o más anunciantes); el técnico no. El operador ya lo traduce al italiano, lo que demuestra que viaja bien.",
         lanzar="Brasil en portugués (cursos técnicos tipo SENAI, enorme volumen); México y Colombia en español.",
         idioma="Portugués de Brasil", precio="R$27-47 / US$7-10",
         riesgo="Bajo."),
    dict(n=6, ref=3, titulo="100 actividades sensoriales para tu bebé (0-5 años)",
         modelo="Crescere Giocando (Italia)",
         datos="22 anuncios activos · el más viejo del 18-jun: 110 días seguidos con el mismo producto",
         por_que="Es el producto más estable del estudio: un solo producto anunciado sin pausa durante casi 4 meses. En español casi no hay versión digital; lo que aparece son centros y jugueterías.",
         lanzar="España y México primero; después Chile, Colombia y Brasil (PT). En el sur, \"actividades para las vacaciones de verano\" (diciembre-febrero).",
         idioma="Español neutro + portugués", precio="US$7-12; bump \"plan semanal imprimible por edad\"",
         riesgo="Bajo. Existe un libro francés con el mismo título (Sylvie d'Esclaibes): hacé contenido 100 % propio."),
    dict(n=7, ref=9, titulo="Novela romántica personalizada: vos sos la protagonista",
         modelo="Soft Sins (Alemania, 94 anuncios) + Ember Books (EE. UU.)",
         datos="94 anuncios activos en Soft Sins; 44 creados antes del 22-sep que la herramienta no deja ver (confianza media en la antigüedad)",
         por_que="Es lo más exótico del estudio. Funciona en dos idiomas con dos operadores distintos y no encontramos ningún anunciante en español. El público de BookTok en México, Argentina y España es enorme, y con IA el costo de producción es casi cero.",
         lanzar="México y Argentina (BookTok fuerte, CPM barato) y España (mayor poder adquisitivo). Lanzalo en octubre, antes de que suban los CPM de Black Friday y Navidad.",
         idioma="Español con versión rioplatense", precio="US$9-15 por novela; bump \"capítulo extra\" o \"versión audio\"",
         riesgo="Medio: contenido adulto. Mantené el anuncio y la portada sin desnudos ni texto explícito, porque Meta rechaza contenido sexual."),
]

def chip(t):
    return f'<span class="chip t{t}">{t}</span>'

rows = []
for p in P:
    rows.append(
        f'<tr data-tier="{p["tier"]}"><td class="num">{p["score"]}</td><td>{chip(p["tier"])}</td>'
        f'<td><strong>{E(p["producto"])}</strong><br><span class="sub">{E(p["pagina"])} · {E(p["origen"])}</span></td>'
        f'<td class="num">{p["ads"]}</td><td class="num">{p["dias"]}</td><td>{E(p["idiomas"])}</td>'
        f'<td class="num">{p["clones"]}</td><td class="sub">{E(p["pais"])}</td>'
        f'<td><a href="{p["links"][0]}" target="_blank" rel="noopener">Ver</a></td></tr>')

cards = []
for t in TOP7:
    p = next(x for x in datos.P if x["n"] == t["ref"])
    c = p["comp"]
    cards.append(f'''
<article class="pick">
  <header>
    <span class="rank">{t["n"]}</span>
    <div><h3>{E(t["titulo"])}</h3><p class="model">Modelo: {E(t["modelo"])}</p></div>
    <span class="score" title="Score 0-100">{p["score"]}</span>
  </header>
  <p class="facts">{E(t["datos"])}</p>
  <p>{E(t["por_que"])}</p>
  <dl>
    <dt>Dónde lanzar</dt><dd>{E(t["lanzar"])}</dd>
    <dt>Idioma</dt><dd>{E(t["idioma"])}</dd>
    <dt>Precio sugerido</dt><dd>{E(t["precio"])} <span class="sub">(estimación: no pudimos abrir las landings)</span></dd>
    <dt>Riesgo</dt><dd>{E(t["riesgo"])}</dd>
  </dl>
  <p class="bars"><span>Antig. {c["antig"]}/20</span><span>Volumen {c["vol"]}/20</span><span>Alcance {c["geo"]}/15</span><span>Creativos {c["div"]}/10</span><span>Clonado {c["clon"]}/20</span><span>Funnel {c["funnel"]}/15</span></p>
  <p class="links">{" ".join(f'<a href="{l}" target="_blank" rel="noopener">Anuncio {i+1}</a>' for i, l in enumerate(p["links"]))}</p>
</article>''')

page = f'''<title>Cazadero Octubre 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,500..800&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: un dossier de campo en una columna ancha; ranking primero, tabla completa después. */
:root {{
  --bg: #f5f6f1; --surface: #ffffff; --ink: #1d241d; --muted: #5d685c; --line: #d9ddd2;
  --blaze: #e2571a; --moss: #3f5a3a; --tA: #2f6b3a; --tB: #3a5f8a; --tC: #a06a12; --tD: #7a6f86;
  --display: "Archivo", "Arial Narrow", system-ui, sans-serif;
  --body: "IBM Plex Sans", system-ui, -apple-system, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #141914; --surface: #1c231c; --ink: #e7ebe3; --muted: #a3ad9f; --line: #2e382e;
  --blaze: #ff7a3d; --moss: #9cc493; --tA: #7fc48a; --tB: #8db3e0; --tC: #e0b25c; --tD: #b9aec6; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --bg: #141914; --surface: #1c231c; --ink: #e7ebe3; --muted: #a3ad9f; --line: #2e382e;
  --blaze: #ff7a3d; --moss: #9cc493; --tA: #7fc48a; --tB: #8db3e0; --tC: #e0b25c; --tD: #b9aec6; color-scheme: dark }}
body {{ background: var(--bg); color: var(--ink); font: 15px/1.6 var(--body); }}
.wrap {{ max-width: 1080px; margin: 0 auto; padding-inline: 20px; padding-block: 32px 64px; display: grid; gap: 40px; }}
h1, h2, h3 {{ font-family: var(--display); text-wrap: balance; margin: 0; line-height: 1.1; }}
h1 {{ font-size: clamp(2rem, 5vw, 3.2rem); font-stretch: 85%; font-weight: 800; letter-spacing: -.01em; }}
h2 {{ font-size: 1.5rem; font-stretch: 90%; font-weight: 700; }}
h3 {{ font-size: 1.15rem; font-weight: 700; }}
p {{ margin: 0; max-width: 72ch; }}
a {{ color: var(--blaze); }}
a:focus-visible, button:focus-visible {{ outline: 2px solid var(--blaze); outline-offset: 2px; }}
.eyebrow {{ font: 500 .75rem var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
.sub {{ color: var(--muted); font-size: .85rem; }}
.lead {{ display: grid; gap: 14px; }}
.lead p.big {{ font-size: 1.1rem; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 10px 28px; font-family: var(--mono); font-size: .85rem; color: var(--muted); }}
.stats b {{ color: var(--ink); font-size: 1.05rem; }}
section {{ display: grid; gap: 18px; }}
.picks {{ display: grid; gap: 18px; }}
.pick {{ background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--blaze); padding: 20px 22px; display: grid; gap: 12px; min-width: 0; }}
.pick header {{ display: grid; grid-template-columns: auto 1fr auto; gap: 14px; align-items: start; }}
.rank {{ font: 800 2rem/1 var(--display); color: var(--blaze); font-stretch: 75%; }}
.score {{ font: 500 1.1rem var(--mono); border: 1px solid var(--line); padding: 2px 8px; }}
.model {{ color: var(--muted); font-size: .88rem; margin-top: 4px; }}
.facts {{ font-family: var(--mono); font-size: .82rem; color: var(--moss); }}
dl {{ display: grid; grid-template-columns: 9.5em 1fr; gap: 6px 14px; margin: 0; }}
dt {{ font-weight: 600; font-size: .85rem; }}
dd {{ margin: 0; min-width: 0; }}
.bars {{ display: flex; flex-wrap: wrap; gap: 6px 14px; font: 500 .75rem var(--mono); color: var(--muted); }}
.links {{ display: flex; flex-wrap: wrap; gap: 12px; font-size: .85rem; }}
.chip {{ display: inline-block; font: 500 .72rem var(--mono); padding: 1px 7px; border: 1px solid currentColor; }}
.tA {{ color: var(--tA); }} .tB {{ color: var(--tB); }} .tC {{ color: var(--tC); }} .tD {{ color: var(--tD); }}
.legend {{ display: grid; gap: 6px; font-size: .9rem; }}
.filters {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.filters button {{ font: 500 .8rem var(--mono); background: var(--surface); color: var(--ink); border: 1px solid var(--line); padding: 5px 10px; cursor: pointer; }}
.filters button[aria-pressed="true"] {{ border-color: var(--blaze); color: var(--blaze); }}
.tablewrap {{ overflow-x: auto; border: 1px solid var(--line); background: var(--surface); }}
table {{ border-collapse: collapse; width: 100%; min-width: 860px; font-size: .88rem; }}
th, td {{ text-align: left; vertical-align: top; padding: 9px 10px; border-bottom: 1px solid var(--line); }}
th {{ font: 500 .72rem var(--mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); position: sticky; top: 0; background: var(--surface); }}
td.num {{ font-family: var(--mono); font-variant-numeric: tabular-nums; text-align: right; }}
.season {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
.season div {{ border-top: 3px solid var(--moss); padding-top: 10px; display: grid; gap: 8px; min-width: 0; }}
ul {{ margin: 0; padding-left: 1.1em; display: grid; gap: 6px; max-width: 75ch; }}
.note {{ border: 1px dashed var(--line); padding: 14px 16px; display: grid; gap: 8px; }}
@media (max-width: 560px) {{ dl {{ grid-template-columns: 1fr; }} .pick header {{ grid-template-columns: auto 1fr; }} .score {{ grid-column: 2; justify-self: start; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>

<div class="wrap">
  <div class="lead">
    <span class="eyebrow">Cazar · Biblioteca de anuncios de Meta · 6 de octubre de 2026</span>
    <h1>Cazadero de infoproductos: los 7 para modelar ya</h1>
    <p class="big">Revisamos más de 100 páginas en 9 idiomas (español, portugués, inglés, italiano, francés, alemán, polaco, turco e indonesio) y verificamos 30 productos página por página. Abajo están los 7 que conviene modelar ahora, con país, idioma, precio y temporada para cada uno.</p>
    <div class="stats"><span><b>8</b> cumplen el filtro duro (≥20 anuncios y anuncio activo con ≥20 días)</span><span><b>5</b> tienen volumen y antigüedad probable</span><span><b>7</b> están a pocos días del umbral</span><span><b>10</b> son exóticos con menos volumen</span></div>
  </div>

  <section>
    <h2>Veredicto: los 7 top</h2>
    <p class="sub">El orden combina el score, lo fácil que es modelarlo en español o portugués, la temporada y la competencia. No es solo el número.</p>
    <div class="picks">{"".join(cards)}</div>
    <div class="note">
      <strong>Por qué quedaron afuera dos productos con score alto</strong>
      <p>Moldes de costura infantil (Tudo para Costura, 78) y mapas de farmacología (Digi Aprende, 79) son ganadores claros en su idioma. Pero en español ya hay unos 12 vendedores de \"megapacks de moldes\" y 11 o más de \"mapas visuales\" de salud. Para entrar ahí hace falta un ángulo distinto: un molde premium por talla, o mapas para técnicos en vez de para salud.</p>
    </div>
  </section>

  <section>
    <h2>Los 30 auditados</h2>
    <div class="legend">
      <span>{chip("A")} Cumple el filtro duro: 20 o más anuncios activos y un anuncio activo con 20 o más días, verificado.</span>
      <span>{chip("B")} 20 o más anuncios; la antigüedad de más de 20 días es probable, pero la herramienta corta en 50 y no deja ver los más viejos.</span>
      <span>{chip("C")} 20 o más anuncios (o casi), con 6 a 19 días. Volvé a revisarlos la semana que viene.</span>
      <span>{chip("D")} Exótico y particular, con menos de 20 anuncios. Sirve como ángulo para modelar, no como prueba de ventas.</span>
    </div>
    <div class="filters" role="group" aria-label="Filtrar por nivel">
      <button type="button" id="f-all" data-f="all" aria-pressed="true">Todos</button>
      <button type="button" id="f-A" data-f="A" aria-pressed="false">A</button>
      <button type="button" id="f-B" data-f="B" aria-pressed="false">B</button>
      <button type="button" id="f-C" data-f="C" aria-pressed="false">C</button>
      <button type="button" id="f-D" data-f="D" aria-pressed="false">D</button>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th>Score</th><th>Nivel</th><th>Producto / página</th><th>Anuncios</th><th>Días</th><th>Idioma</th><th>Clones</th><th>Mejor país</th><th>Ref.</th></tr></thead>
      <tbody id="rows">{"".join(rows)}</tbody>
    </table></div>
    <p class="sub">Días = antigüedad del anuncio activo más viejo que pudimos ver. Clones = anunciantes distintos con una oferta casi igual. Score de 0 a 100: antigüedad 20, volumen 20, alcance 15, creativos 10, clonado 20 y funnel 15. El funnel quedó bajo en todos porque no pudimos abrir las landings.</p>
  </section>

  <section>
    <h2>Temporada y poder adquisitivo (octubre a diciembre de 2026)</h2>
    <div class="season">
      <div><h3>Hemisferio sur: empieza la primavera</h3>
        <ul><li>Brasil, Argentina, Chile, Uruguay y Paraguay entran en temporada de aire acondicionado: es el momento del pack HVAC.</li>
        <li>Las vacaciones de verano (diciembre a febrero) empujan las actividades para chicos.</li>
        <li>En Argentina conviene cobrar en USD o en pesos ajustados; Chile y Uruguay pagan más por el mismo PDF.</li></ul></div>
      <div><h3>Hemisferio norte: otoño e invierno</h3>
        <ul><li>Se pasa más tiempo adentro y llega la Navidad: fieltro, manualidades y regalos personalizados (novela) en España y EE. UU.</li>
        <li>Temporada de calefacción en España, Italia y Francia: versión \"bombas de calor\" del pack HVAC.</li>
        <li>EE. UU., Canadá y Alemania tienen el mayor poder adquisitivo (NCLEX, workbooks, novela).</li></ul></div>
      <div><h3>Calendario de pauta</h3>
        <ul><li>Octubre: lanzar y testear ahora, con CPM todavía bajos.</li>
        <li>Black Friday (27-nov) y diciembre: los CPM suben; escalá solo lo que ya tenga ROAS.</li>
        <li>Enero: propósitos de año nuevo, agendas, NCLEX y planes de alimentación.</li></ul></div>
    </div>
  </section>

  <section>
    <h2>¿Se puede automatizar?</h2>
    <p>Sí. Esta misma búsqueda puede correr sola cada semana como una rutina programada de Claude Code: vuelve a revisar los 30 page_id con Cazar, actualiza el Excel con la tendencia (sube, se mantiene o baja), busca candidatos nuevos con las mismas consultas y republica este informe con el mismo link. Para dejarla andando necesito dos datos: el día y la hora, y tu zona horaria.</p>
    <ul>
      <li>Necesita que el conector de Meta siga activo, con una cuenta publicitaria activa.</li>
      <li>No puede ver el botón de cada anuncio ni entrar a la landing, porque el entorno bloquea facebook.com. Eso se revisa a mano en los links \"Ver\".</li>
      <li>Cada corrida consume uso de Claude: con una vez por semana alcanza.</li>
    </ul>
  </section>

  <section class="note">
    <h2>Límites de este estudio</h2>
    <ul>
      <li>La API devuelve los 50 anuncios más nuevos de cada página. En páginas con más de 50 anuncios no se ve el más viejo, por eso existe el nivel B.</li>
      <li>Muchos anunciantes recrean sus anuncios cada pocos días. Por eso medimos cuánto tiempo lleva corriendo el producto, no cuánto dura cada anuncio.</li>
      <li>El botón (\"Más información\" o \"Enviar mensaje\") no viene en los datos. Lo inferimos por el título del link y descartamos todo lo que decía WhatsApp, \"Escríbeme\", \"Chatea\" o \"Converse conosco\".</li>
      <li>No pudimos abrir landings ni checkouts, así que los precios sugeridos son estimaciones y no datos medidos.</li>
      <li>Solo cubre Meta. Un producto puede estar ganando en TikTok o Google y no aparecer acá.</li>
      <li>El score indica validación de mercado. No garantiza ingresos.</li>
    </ul>
  </section>
</div>

<script>
(function () {{
  var btns = document.querySelectorAll('.filters button');
  var rows = document.querySelectorAll('#rows tr');
  function apply(f) {{
    btns.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.f === f)); }});
    rows.forEach(function (r) {{ r.hidden = !(f === 'all' || r.dataset.tier === f); }});
    try {{ localStorage.setItem('cazar-filtro', f); }} catch (e) {{}}
  }}
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ apply(b.dataset.f); }}); }});
  var saved = 'all';
  try {{ saved = localStorage.getItem('cazar-filtro') || 'all'; }} catch (e) {{}}
  apply(saved);
}})();
</script>
'''

out = os.path.join(os.path.dirname(__file__), "informe.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(page)
print("ok", out, len(page))
