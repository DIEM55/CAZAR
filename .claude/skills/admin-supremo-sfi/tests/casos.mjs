// Los casos que fijan la calculadora.
//   node tests/casos.mjs
//
// Dos familias:
//   A) Casos de decisión — la calculadora tiene que ejecutar el veredicto correcto.
//   B) Casos de recorte — casos donde el método completo ejecutaría un veredicto fino y esta
//      versión tiene que DECLARAR (ZONA GRIS / CANDIDATO CON RESERVAS) en vez de decidir.
//      Si alguno de estos empieza a devolver una decisión dura, alguien portó una regla que no
//      corresponde a esta versión. Es el gate: no se entrega un zip con estos tests en rojo.

import { veredictos } from "../scripts/veredicto.mjs";

let fallos = 0;
const ok = (nombre, cond, detalle) => {
  if (!cond) { fallos++; console.log(`  x ${nombre}  ${detalle ?? ""}`); }
  else console.log(`  . ${nombre}`);
};
const estado = (res, n) => res.conjuntos.find((c) => c.conjunto === n)?.estado;

// ============================ A) CASOS DE DECISIÓN ============================

// --- Caso 1: línea base (Francia, día 1, pagos iniciados rotos por AD1) ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "francia", pasarela_externa: true },
    campana: { nombre: "CURSO FRA G7", tipo: "abo", dias: 1, conjuntos: [
      { nombre: "AD1 G7", gasto: 2.10, impresiones: 98,  clics: 7, cpm: 21.4, ctr: 7.14, cpc: 0.30, lpv: 5, ic: 0, compras: 1, valor: 18.5 },
      { nombre: "AD2 G7", gasto: 3.50, impresiones: 103, clics: 3, cpm: 34,   ctr: 2.90, cpc: 1.17, lpv: 4, ic: 1, compras: 0 },
      { nombre: "AD3 G7", gasto: 2.40, impresiones: 83,  clics: 1, cpm: 29,   ctr: 1.20, cpc: 2.40, lpv: 1, ic: 0, compras: 0 },
      { nombre: "AD4 G7", gasto: 3.03, impresiones: 233, clics: 4, cpm: 13,   ctr: 1.72, cpc: 0.76, lpv: 4, ic: 0, compras: 0 },
      { nombre: "AD5 G7", gasto: 1.73, impresiones: 115, clics: 0, cpm: 15,   ctr: 0,    cpc: null, lpv: 0, ic: 0, compras: 0 },
      { nombre: "AD6 G7", gasto: 1.40, impresiones: 78,  clics: 4, cpm: 18,   ctr: 5.13, cpc: 0.35, lpv: 2, ic: 0, compras: 0 },
    ] } });
  console.log("Caso 1 — línea base FRA, día 1");
  ok("pagos iniciados rotos detectados (AD1 vendió sin ninguno)", r.ic_roto === true);
  ok("AD1 mantener (vendió)", estado(r, "AD1 G7") === "MANTENER", estado(r, "AD1 G7"));
  ok("AD2 off (CPM y CPC fuera de rango)", estado(r, "AD2 G7") === "OFF", estado(r, "AD2 G7"));
  ok("AD3 off (CPC roto)", estado(r, "AD3 G7") === "OFF", estado(r, "AD3 G7"));
  ok("AD4 off (dos flojas, nadie llegó al pago)", estado(r, "AD4 G7") === "OFF", estado(r, "AD4 G7"));
  ok("AD5 off antes del piso (CTR en 0 con 115 impresiones)", estado(r, "AD5 G7") === "OFF", estado(r, "AD5 G7"));
  ok("AD6 esperar (no llegó al piso)", estado(r, "AD6 G7") === "ESPERAR", estado(r, "AD6 G7"));
  ok("orden por gasto", r.conjuntos[0].conjunto === "AD2 G7" && r.conjuntos[1].conjunto === "AD4 G7");
}

// --- Caso 2: secundarias limpias y una sola floja (Europa) ---
{
  const r = veredictos({
    config: { precio: 15, mercado: "europa" },
    campana: { nombre: "CURSO ITA G6", tipo: "abo", dias: 1, conjuntos: [
      { nombre: "AD8 G6", gasto: 2.00, impresiones: 105, clics: 7, cpm: 19, ctr: 6.77, cpc: 0.28, lpv: 4, ic: 0, compras: 0 },
      { nombre: "AD7 G6", gasto: 2.53, impresiones: 120, clics: 5, cpm: 21, ctr: 4.27, cpc: 0.51, lpv: 5, ic: 0, compras: 0 },
      { nombre: "AD3 G6", gasto: 2.06, impresiones: 108, clics: 2, cpm: 19, ctr: 1.87, cpc: 1.00, lpv: 1, ic: 0, compras: 0 },
    ] } });
  console.log("Caso 2 — CURSO ITA G6");
  ok("AD8 tramo (todo en rango)", estado(r, "AD8 G6") === "TRAMO", estado(r, "AD8 G6"));
  ok("AD8 lleva su techo en dólares", typeof r.conjuntos.find((c) => c.conjunto === "AD8 G6").techo === "number");
  ok("AD7 off (CPM flojo y nadie llegó al pago)", estado(r, "AD7 G6") === "OFF", estado(r, "AD7 G6"));
  ok("AD3 off (CPC roto)", estado(r, "AD3 G6") === "OFF", estado(r, "AD3 G6"));
}

// --- Caso 3: ventanas y rachas ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "europa" },
    campana: { nombre: "VENTANAS", tipo: "abo", dias: 6, conjuntos: [
      { nombre: "RACHA", gasto: 30, impresiones: 4000, clics: 90, cpm: 7.5, ctr: 2.25, cpc: 0.33, lpv: 70, ic: 20, compras: 4, valor: 68, roas_amplio: 2.27,
        dias: [ { gasto: 5, compras: 2, valor: 34 }, { gasto: 5, compras: 2, valor: 34 }, { gasto: 5, compras: 0, valor: 0 }, { gasto: 5, compras: 0, valor: 0 }, { gasto: 5, compras: 0, valor: 0 } ] },
      { nombre: "VIVE", gasto: 20, impresiones: 2600, clics: 60, cpm: 7.7, ctr: 2.31, cpc: 0.33, lpv: 50, ic: 15, compras: 4, valor: 68, roas_amplio: 3.40,
        dias: [ { gasto: 5, compras: 1, valor: 17 }, { gasto: 5, compras: 1, valor: 17 }, { gasto: 5, compras: 1, valor: 17 }, { gasto: 5, compras: 1, valor: 17 } ] },
      { nombre: "HUNDIDO", gasto: 24, impresiones: 3000, clics: 70, cpm: 8, ctr: 2.33, cpc: 0.34, lpv: 55, ic: 12, compras: 1, valor: 17, roas_amplio: 0.71 },
    ] } });
  console.log("Caso 3 — ventanas y rachas");
  ok("RACHA off (tres días seguidos en cero pese a la ventana amplia)", estado(r, "RACHA") === "OFF", estado(r, "RACHA"));
  ok("VIVE candidato (sostenido y estable)", estado(r, "VIVE") === "CANDIDATO A ESCALAR", estado(r, "VIVE"));
  ok("HUNDIDO off (la ventana amplia no paga el gasto)", estado(r, "HUNDIDO") === "OFF", estado(r, "HUNDIDO"));
  ok("candidatos listados", r.candidatos.includes("VIVE"));
}

// --- Caso 4: apagados que merecen otra oportunidad ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "europa" },
    campana: { nombre: "APAGADOS", tipo: "abo", dias: 9, conjuntos: [
      { nombre: "REVIVE", estado: "PAUSED", gasto: 22, impresiones: 2800, clics: 65, cpm: 7.9, ctr: 2.32, cpc: 0.34, lpv: 50, ic: 14, compras: 3, valor: 51, roas_amplio: 2.32 },
      { nombre: "MUERTO", estado: "PAUSED", gasto: 18, impresiones: 2400, clics: 50, cpm: 7.5, ctr: 2.08, cpc: 0.36, lpv: 40, ic: 5, compras: 0, valor: 0, roas_amplio: 0 },
    ] } });
  console.log("Caso 4 — apagados");
  ok("REVIVE se re-prende a prueba", estado(r, "REVIVE") === "REACTIVAR A PRUEBA", estado(r, "REVIVE"));
  ok("MUERTO queda apagado", estado(r, "MUERTO") === "APAGADO", estado(r, "MUERTO"));
}

// --- Caso 5: CBO y pasarela externa ---
{
  const cbo = veredictos({
    config: { precio: 20, mercado: "europa" },
    campana: { nombre: "CBO", tipo: "cbo", dias: 2, conjuntos: [
      { nombre: "C1", gasto: 0.90, impresiones: 60, clics: 1, cpm: 15, ctr: 1.67, cpc: 0.90, lpv: 1, ic: 0, compras: 0 },
    ] } });
  console.log("Caso 5 — CBO y pasarela");
  ok("C1 esperar (no le tocó gasto suficiente en una CBO)", estado(cbo, "C1") === "ESPERAR", estado(cbo, "C1"));

  const pas = veredictos({
    config: { precio: 20, mercado: "europa", pasarela_externa: true },
    campana: { nombre: "PASARELA", tipo: "abo", dias: 5, conjuntos: [
      { nombre: "SANO", gasto: 12, impresiones: 1600, clics: 40, cpm: 7.5, ctr: 2.50, cpc: 0.30, lpv: 15, ic: 6, compras: 0, valor: 0 },
    ] } });
  ok("SANO no decidible (secundarias sanas, cero compras, pasarela externa)", estado(pas, "SANO") === "NO DECIDIBLE", estado(pas, "SANO"));
  ok("el aviso de pasarela sale en el informe", pas.avisos.some((a) => a.includes("pasarela")));
}

// ============================ B) CASOS DE RECORTE ============================
// Acá la respuesta correcta es NO decidir.

// --- Recorte 1: el pago iniciado no desempata la zona mediocre ---
{
  const r = veredictos({
    config: { precio: 15, mercado: "europa" },
    campana: { nombre: "MEDIOCRE", tipo: "abo", dias: 1, conjuntos: [
      { nombre: "AD1 G6", gasto: 2.34, impresiones: 100, clics: 4, cpm: 23, ctr: 4.0, cpc: 0.58, lpv: 3, ic: 1, compras: 0 },
    ] } });
  console.log("Recorte 1 — dos flojas con un pago iniciado");
  ok("declara zona gris en vez de conceder un tramo", estado(r, "AD1 G6") === "ZONA GRIS", estado(r, "AD1 G6"));
}

// --- Recorte 2: el ROAS al borde del corte no ejecuta ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "europa" },
    campana: { nombre: "BORDE", tipo: "abo", dias: 4, conjuntos: [
      { nombre: "RAYA", gasto: 20, impresiones: 2600, clics: 60, cpm: 7.7, ctr: 2.31, cpc: 0.33, lpv: 45, ic: 12, compras: 2, valor: 42, roas_amplio: 2.10 },
    ] } });
  console.log("Recorte 2 — ROAS justo sobre la línea");
  ok("declara zona gris en vez de sentenciar", estado(r, "RAYA") === "ZONA GRIS", estado(r, "RAYA"));
}

// --- Recorte 3: el patrón inestable no ejecuta ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "europa" },
    campana: { nombre: "OSCILA", tipo: "abo", dias: 5, conjuntos: [
      { nombre: "SUBE Y BAJA", gasto: 20, impresiones: 2600, clics: 60, cpm: 7.7, ctr: 2.31, cpc: 0.33, lpv: 45, ic: 12, compras: 3, valor: 47, roas_amplio: 2.35,
        dias: [ { gasto: 5, compras: 1, valor: 17 }, { gasto: 5, compras: 0, valor: 0 }, { gasto: 5, compras: 1, valor: 17 }, { gasto: 5, compras: 0, valor: 0 } ] },
    ] } });
  console.log("Recorte 3 — días alternados sin tendencia");
  ok("declara zona gris en vez de aplicar una sentencia más dura", estado(r, "SUBE Y BAJA") === "ZONA GRIS", estado(r, "SUBE Y BAJA"));
}

// --- Recorte 4: el candidato que no termina de convencer se nombra, no se resuelve ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "europa" },
    campana: { nombre: "FALSO", tipo: "abo", dias: 5, conjuntos: [
      { nombre: "CAE", gasto: 20, impresiones: 2600, clics: 60, cpm: 7.7, ctr: 2.31, cpc: 0.33, lpv: 45, ic: 12, compras: 5, valor: 60, roas_amplio: 3.00,
        dias: [ { gasto: 4, compras: 2, valor: 26 }, { gasto: 5, compras: 2, valor: 22 }, { gasto: 5, compras: 1, valor: 12 } ] },
    ] } });
  console.log("Recorte 4 — pasa el filtro pero la curva cae");
  ok("candidato con reservas, no candidato a secas", estado(r, "CAE") === "CANDIDATO CON RESERVAS", estado(r, "CAE"));
  ok("no entra en la lista de candidatos a escalar", !r.candidatos.includes("CAE"));
  ok("entra en la lista de reservas", r.candidatos_con_reservas.includes("CAE"));
}

// --- Recorte 5: ventanas en desacuerdo ---
{
  const r = veredictos({
    config: { precio: 17, mercado: "europa" },
    campana: { nombre: "DESACUERDO", tipo: "abo", dias: 7, conjuntos: [
      { nombre: "MIXTO", gasto: 35, impresiones: 4600, clics: 105, cpm: 7.6, ctr: 2.28, cpc: 0.33, lpv: 80, ic: 22, compras: 6, valor: 102, roas_amplio: 2.91, roas_corto: 0.85 },
    ] } });
  console.log("Recorte 5 — ventana corta y amplia en desacuerdo");
  ok("declara zona gris con las dos lecturas", estado(r, "MIXTO") === "ZONA GRIS", estado(r, "MIXTO"));
}

// ============================ resultado ============================
console.log("");
if (fallos) { console.log(`${fallos} caso(s) en rojo.`); process.exit(1); }
console.log("Todos los casos pasan.");
