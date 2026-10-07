# Cómo se lee y cómo se monta con el conector de Meta Ads

Referencia operativa para las herramientas del conector de Meta (`ads_get_ad_entities`,
`ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_update_entity`,
`ads_activate_entity`, `ads_get_ad_preview`, `ads_get_ad_accounts`, `ads_get_datasets`).
Antes de pasar un campo, verificarlo con `ads_get_field_context`.

## 1. Leer una cuenta

1. `ads_get_ad_accounts` → listar y dejar que el usuario elija (se guarda en la config).
2. Campañas: nivel `campaign`, `date_preset: today`, `sort: amount_spent_descending`, campos
   `id, name, effective_status, amount_spent, created_time, daily_budget`. **La API pagina sin
   avisar**: si hay `next_cursor`, seguir.
3. Conjuntos de UNA campaña: nivel `adset`, `filtering: [{field: "campaign.id", operator:
   "EQUAL", value: ["<id>"]}]`, `sort: amount_spent_descending`, campos:
   `id, name, effective_status, daily_budget, amount_spent, impressions, clicks, cpm, ctr, cpc,
   landing_page_view, omni_initiated_checkout, offsite_conversion_fb_pixel_purchase,
   offsite_conversion_fb_pixel_purchase_values, purchase_roas`.
   Pedir la misma lista con `date_preset` = `today`, `yesterday`, `last_3d`, `last_7d`,
   `maximum`. Para día por día: `date_preset: maximum` + `time_increment: "1"`.
4. **Incluir los apagados** (no filtrar por estado): la regla de reactivar depende de verlos.
5. La edad de la campaña sale de `created_time` (o `start_time` del conjunto).

Formato de salida de Meta: montos como `"$3,38 USD"`, porcentajes como `"2,63%"`. Normalizar a
número antes de calcular. Un `cpc` nulo = 0 clics.

## 2. Verificar el píxel

`ads_get_datasets` → `ads_get_dataset_stats` (agregación por evento / host) o
`ads_get_dataset_details` con `last_fired_time`. Lo que importa: que exista un píxel con el
evento **Purchase** disparando desde el dominio de la landing o del checkout. Si no dispara
todavía, se avisa; el objetivo sigue siendo Ventas + Compra.

## 3. Montar una ABO de testeo (el orden exacto)

1. **Campaña** — `ads_create_campaign`: `objective: OUTCOME_SALES`, `buying_type: AUCTION`,
   `status: PAUSED`, `special_ad_categories: []`, nombre según `estructuras.md`. Sin presupuesto a
   nivel campaña (eso la hace ABO).
2. **Conjuntos** — `ads_create_ad_set`, uno por creativo, nombre `ADn GN`:
   - `daily_budget` en centavos (500 = $5, 700 = $7).
   - `optimization_goal: OFFSITE_CONVERSIONS`, `billing_event: IMPRESSIONS`,
     `bid_strategy: LOWEST_COST_WITHOUT_CAP`.
   - `promoted_object: {pixel_id: "<píxel>", custom_event_type: "PURCHASE"}`.
   - `attribution_spec: [{event_type: "CLICK_THROUGH", window_days: 7}, {event_type:
     "VIEW_THROUGH", window_days: 1}]`.
   - `start_time`: mañana a las 00:00 o 02:00 **en la zona horaria de la cuenta**, en ISO con
     offset. Si la sesión pasa la medianoche, decir explícitamente qué día se eligió.
   - `status: ACTIVE`.
   - `targeting` **completo desde el primer intento** (ver 3.1).
3. **Anuncios** — `ads_create_ad` con creativo inline (ver 3.2), nombre `ADn GN` igual que su
   conjunto, `status: ACTIVE`.
4. **Verificar** (ver 4) y entregar el link de Ads Manager con la campaña en PAUSED.

### 3.1. El `targeting` de cada conjunto

```json
{
  "geo_locations": {"countries": ["IT"], "location_types": ["home", "recent"]},
  "locales": [],
  "targeting_automation": {"advantage_audience": 0},
  "publisher_platforms": ["facebook", "instagram", "messenger", "threads"],
  "facebook_positions": ["feed", "instream_video", "story", "search", "facebook_reels",
                         "facebook_reels_overlay", "profile_feed", "notification"],
  "instagram_positions": ["stream", "story", "reels", "explore_home", "profile_feed", "ig_search"],
  "messenger_positions": ["story"],
  "threads_positions": ["threads_stream"],
  "device_platforms": ["mobile", "desktop"]
}
```

- **Francés:** `countries` = los países de Europa y `locales` = el código del francés (leer el id
  con `ads_get_field_context` o el buscador de targeting). Es el único caso con `locales`.
- **Sin edad, sin género, sin intereses.** `advantage_audience: 0` para que no expanda.
- **Por qué el spec de ubicaciones va siempre:** un conjunto creado sin ubicaciones explícitas
  sale en *Advantage+* y mete **WhatsApp**, **Audience Network**, right column y marketplace sin
  avisar. Es el default de la API, no un error puntual.
- **Por qué `location_types` explícito:** sin él Meta guarda `["home"]`, un tipo dado de baja, y
  el conjunto **no se puede duplicar** en Ads Manager (#1870194). Con el spec manual Meta agrega
  `frequently_in` por su cuenta y no se puede revertir: es cosmético, se tolera.
- **Verificar releyendo** el conjunto con el campo `targeting`: los campos **sin** prefijo
  `effective_` son los seteados; si solo aparecen `effective_*`, quedó en automático → corregir
  con `ads_update_entity` pasando el `targeting` completo (el update **reemplaza**, no mergea).

### 3.2. El creativo inline

Video:
```json
{"name": "PRODUCTO ADn GN Creative",
 "object_story_spec": {
   "page_id": "<página del usuario>", "instagram_user_id": "<IG del usuario>",
   "video_data": {"video_id": "<id de la biblioteca>", "image_url": "<miniatura>",
     "message": "<texto primario>", "title": "<título>",
     "call_to_action": {"type": "LEARN_MORE", "value": {"link": "<landing>"}}}},
 "degrees_of_freedom_spec": "{\"creative_features_spec\":{\"image_touchups\":{\"enroll_status\":\"OPT_OUT\"},\"text_optimizations\":{\"enroll_status\":\"OPT_OUT\"},\"enhance_cta\":{\"enroll_status\":\"OPT_OUT\"},\"add_text_overlay\":{\"enroll_status\":\"OPT_OUT\"},\"image_animation\":{\"enroll_status\":\"OPT_OUT\"},\"text_generation\":{\"enroll_status\":\"OPT_OUT\"},\"video_auto_crop\":{\"enroll_status\":\"OPT_OUT\"},\"media_type_automation\":{\"enroll_status\":\"OPT_OUT\"},\"site_extensions\":{\"enroll_status\":\"OPT_OUT\"},\"description_automation\":{\"enroll_status\":\"OPT_OUT\"}}}"}
```
Imagen: igual con `link_data` en vez de `video_data`:
`{"link": "<landing>", "picture": "<URL pública de la imagen>", "message", "name", "description",
"call_to_action": {"type": "LEARN_MORE"}}`.

- **Los videos exigen miniatura** (`image_url`); si no hay una buena, cualquiera sirve.
- **La imagen va como `picture` dentro de `link_data`.** En el top-level Meta la ignora en
  silencio y scrapea el `og:image` de la landing. Síntoma: varios creativos con el mismo
  `image_hash`.
- **Sin `instagram_user_id` el anuncio no se entrega en Instagram.** Pedir la cuenta de IG.
- `degrees_of_freedom_spec` va como **string JSON**; no combinar con `advantage_plus_creative`.
  `standard_enhancements` está deprecado: listar features individuales.
- **Los creativos son inmutables**: si algo salió mal, creativo nuevo + anuncio nuevo. El campo
  *Anuncios multianunciante* no existe en la API: lo destilda el usuario a mano.
- Con tracker externo: la cadena de parámetros va en `url_tags` del creativo (solo funciona en
  el creativo inline, no en `ads_create_creative`).
- Subida de archivos: la API **no sube desde el disco**; necesita una **URL pública directa** (no
  Drive). Si `ads_creative_upload_video` está deshabilitada en la cuenta, pedir al usuario que
  suba el video a la biblioteca desde Ads Manager y usar su `video_id`.

## 4. Verificación que no se negocia

1. **`ads_get_ad_preview` de CADA anuncio**, mirado a ojo, antes de entregar: el create nunca
   falla por imagen equivocada, crea el anuncio mal en silencio. Dos previews con la misma
   imagen siendo creativos distintos = og:image scrapeado → rehacer.
2. Releer los conjuntos: `targeting` seteado (no solo `effective_*`), `daily_budget`,
   `start_time`, `promoted_object`, `attribution_spec`.
3. Estados: conjuntos y anuncios `ACTIVE`, campaña `PAUSED`.

## 5. Activar, deshacer, avisos

- `ads_activate_entity` sobre conjuntos y anuncios; **nunca sobre la campaña** salvo pedido
  explícito. Un error `INTERNAL` al activar es transitorio: reintentar (hasta 3). En un
  *create*, en cambio, el objeto ya existe: **no** reintentar a ciegas (duplica).
- Un `DISAPPROVED` recién creado suele ser transitorio: revierte a `PENDING_REVIEW` solo. No
  rehacer el anuncio.
- El conector **no borra** anuncios (`DELETED` se fuerza a `PAUSED`): un anuncio malo se pausa y
  se renombra `… MALO — borrar`; la eliminación la hace el usuario en Ads Manager.
- Al entregar: "todo activo salvo la campaña — la prendés vos", con el link de Ads Manager
  (`ads_manager_url` viene en la respuesta).

## 6. CBO de testeo y pre-escala — diferencias con la ABO

**CBO de testeo** (solo para variaciones de un anuncio que ya ganó):
- Presupuesto en la campaña (`daily_budget` + `bid_strategy: LOWEST_COST_WITHOUT_CAP`), $20/día mínimo.
- Un conjunto por creativo, **sin** `daily_budget` propio: la API lo rechaza bajo CBO.
- Un anuncio por conjunto.

**CBO Pocket** (pre-escala):
- Presupuesto en la campaña, **$30/día mínimo**.
- **3 a 5 conjuntos idénticos**, llamados `Conjunto 1` … `Conjunto 5`.
- En cada uno, de 1 a 5 anuncios ganadores cableados por **post ID**
  (`object_story_id: "<page_id>_<post_id>"`), para que conserven la prueba social acumulada.

**ABO Pocket** (la otra forma de pre-escala):
- Presupuesto por conjunto: `daily_budget: 129` (= $1,29).
- **30 conjuntos idénticos**, el mismo ganador por post ID en todos.

El post ID se saca del anuncio ganador (`effective_object_story_id`). Los Reels a veces no se
pueden cablear por API: dejar el anuncio con el nombre y pedirle al usuario que pegue el post ID.
**Al pre-escalar, copiar la segmentación exacta de la campaña de origen**, no la regla genérica.

## 7. Lo que esta skill no monta

El **escalado duro** — Cost Cap, ABO Cost Cap, Pocket agresiva — no se arma acá. Ver
`estructuras.md` y `diagnosticos.md` F8b. No improvises una estructura de escala: si el usuario la
pide, explicale qué es y por qué no se decide desde una skill.
