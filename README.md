# Proyecto CAZAR

Sistema Sin Filtros · Módulo 1: caza de productos winner en Facebook Ads Library.

## Skill instalada

`.claude/skills/winners-free/SKILL.md` → se invoca con `/winners-free <nicho>`.

- `winners/00-registro.md` — registro acumulado de todo lo cazado (incluye descartes).
- `winners/[nicho]-[dd-mm].md` — una Ficha de Caza por candidata que llega a COPIAR o ARBITRAJE.

## Requisito

Conector oficial de Meta (Facebook) instalado y con una cuenta de ads activa, para usar
`ads_library_search`. Es solo lectura. Sin conector, la skill cae al modo manual sobre
`facebook.com/ads/library` vía Chrome MCP.
