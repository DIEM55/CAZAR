#!/usr/bin/env node
// veredicto.mjs — la aritmética del método, determinística.
// Entrada: un JSON (archivo o stdin) con la config del usuario y UNA campaña con sus conjuntos.
// Salida: un veredicto por conjunto + veredicto de campaña, en JSON (--json) o tabla.
//
//   node scripts/veredicto.mjs plantillas/entrada.example.json
//   cat entrada.json | node scripts/veredicto.mjs --json
//
// Donde el criterio es ambiguo, esta calculadora NO fuerza una decisión: devuelve ZONA GRIS o
// CANDIDATO CON RESERVAS para que el informe presente las dos lecturas. Con dinero real, forzar
// una regla en un caso dudoso quema anuncios buenos.
//
// Esquema de entrada (ver plantillas/entrada.example.json):
// {
//   "config": { "precio": 17, "mercado": "europa|latam|francia|anglo", "pasarela_externa": true },
//   "campana": {
//     "nombre": "...", "tipo": "abo|cbo|pocket", "dias": 1,
//     "conjuntos": [ {
//        "nombre": "AD1 G7", "estado": "ACTIVE|PAUSED",
//        "gasto": 2.10, "impresiones": 98, "clics": 7, "cpm": 21.4, "ctr": 7.14, "cpc": 0.30,
//        "lpv": 5, "ic": 0, "compras": 1, "valor": 18.5,
//        "roas_amplio": 8.8,   // ROAS en la ventana más amplia que exista (opcional)
//        "roas_corto": 0.0,    // ROAS de la ventana corta, para detectar desacuerdo (opcional)
//        "dias": [ {"fecha":"2026-09-04","gasto":3.2,"compras":1,"valor":17}, ... ]  // opcional
//     } ]
//   }
// }

import { readFileSync } from "node:fs";

// ---------- bandas ----------
const BANDAS = {
  latam:   { piso: 2.0, cpm: { bueno: 4,  flojo: 10, roto: 15, catastrofico: 15 } },
  europa:  { piso: 2.0, cpm: { bueno: 20, flojo: 30, roto: 30, catastrofico: 40 } },
  anglo:   { piso: 2.0, cpm: { bueno: 20, flojo: 30, roto: 30, catastrofico: 40 } },
  francia: { piso: 2.0, cpm: { bueno: 25, flojo: 30, roto: 30, catastrofico: 65 } },
};
const CTR = { bueno: 1.8, roto: 1.0 };
const CPC = { bueno: 0.55, roto: 0.90 };
const ROAS_CORTE = 2.0;
const ROAS_BORDE = 0.15;           // ±15 % alrededor del corte = zona gris
const INT = { bajo: 0.15, bueno: 0.25 };
const TECHO_FRAC = { abo: 0.5, cbo: 0.5, pocket: 0.7 };
const TRAMO_CON_FLOJA = 0.66;      // una secundaria floja acorta el permiso

const num = (v) => {
  if (v === null || v === undefined || v === "") return 0;
  if (typeof v === "number") return v;
  const s = String(v).replace(/[^0-9,.\-]/g, "").replace(/\.(?=\d{3}(\D|$))/g, "").replace(",", ".");
  const n = parseFloat(s);
  return Number.isFinite(n) ? n : 0;
};
const fmt = (n, d = 2) => (n === null || n === undefined ? "—" : Number(n).toFixed(d));

function clasificar(c, b) {
  const fallas = [];
  const impr = num(c.impresiones), clics = num(c.clics);
  const ctr = c.ctr !== undefined ? num(c.ctr) : (impr ? (clics / impr) * 100 : 0);
  const cpm = num(c.cpm);
  const cpc = clics ? (c.cpc !== undefined ? num(c.cpc) : num(c.gasto) / clics) : null;

  if (cpm >= b.cpm.catastrofico) fallas.push({ metrica: "CPM", nivel: "catastrofico", valor: cpm });
  else if (cpm >= b.cpm.roto) fallas.push({ metrica: "CPM", nivel: "roto", valor: cpm });
  else if (cpm >= b.cpm.bueno) fallas.push({ metrica: "CPM", nivel: "flojo", valor: cpm });

  if (clics === 0 && impr >= 80) fallas.push({ metrica: "CTR", nivel: "catastrofico", valor: 0 });
  else if (ctr < CTR.roto && impr >= 100) fallas.push({ metrica: "CTR", nivel: "catastrofico", valor: ctr });
  else if (ctr < CTR.roto) fallas.push({ metrica: "CTR", nivel: "roto", valor: ctr });
  else if (ctr < CTR.bueno) fallas.push({ metrica: "CTR", nivel: "flojo", valor: ctr });

  if (cpc !== null) {
    if (cpc >= CPC.roto) fallas.push({ metrica: "CPC", nivel: "roto", valor: cpc });
    else if (cpc >= CPC.bueno) fallas.push({ metrica: "CPC", nivel: "flojo", valor: cpc });
  }
  return { fallas, ctr, cpm, cpc, impr, clics };
}

function veredictoConjunto(c, ctx) {
  const { b, precio, icRoto, tipo, dias } = ctx;
  const gasto = num(c.gasto), compras = num(c.compras), valor = num(c.valor);
  const lpv = num(c.lpv), ic = num(c.ic);
  const m = clasificar(c, b);
  const techoMax = precio ? +(precio * (TECHO_FRAC[tipo] ?? 0.5)).toFixed(2) : null;
  const R = (estado, por_que, extra = {}) => ({
    conjunto: c.nombre, estado, gasto, por_que, ...extra,
    metricas: { cpm: fmt(m.cpm), ctr: fmt(m.ctr) + "%", cpc: fmt(m.cpc), lpv, ic, compras, valor },
  });

  // --- apagados: ¿reactivar? ---
  if ((c.estado || "").toUpperCase() === "PAUSED") {
    const r7 = c.roas_7d !== undefined ? num(c.roas_7d)
             : (c.roas_amplio !== undefined ? num(c.roas_amplio) : null);
    if (r7 !== null && r7 >= ROAS_CORTE) {
      return R("REACTIVAR A PRUEBA", `apagado, pero su ventana amplia sigue sana; re-prender con un techo corto y sentencia si no vende`, { sentencia: 4 });
    }
    return R("APAGADO", "sin señal en la ventana amplia que justifique re-prenderlo");
  }

  // --- con ventas: se decide por ROAS ---
  if (compras > 0) {
    const roas = c.roas_amplio !== undefined ? num(c.roas_amplio) : (gasto ? valor / gasto : 0);
    const serie = Array.isArray(c.dias)
      ? c.dias.map((d) => ({ ...d, roas: num(d.gasto) ? num(d.valor) / num(d.gasto) : 0, compras: num(d.compras) }))
      : null;

    if (serie && serie.length) {
      const ult = serie.slice(-3);
      if (ult.length >= 3 && ult.every((d) => d.compras === 0)) {
        return R("OFF", "tres días seguidos en cero; lo que muestra la ventana amplia es arrastre");
      }
      if (dias && dias <= 2 && serie.every((d) => d.compras === 0)) {
        return R("OFF", "toda su vida en cero");
      }
      // patrón inestable: días buenos y malos alternados, sin tendencia
      const signos = serie.map((d) => d.roas >= ROAS_CORTE);
      const cambios = signos.slice(1).filter((s, i) => s !== signos[i]).length;
      if (signos.length >= 4 && cambios >= 3) {
        return R("ZONA GRIS", `alterna días buenos y malos sin tendencia clara (ventana amplia ${fmt(roas)}); un patrón inestable no se ejecuta desde una tabla`, { roas });
      }
      const dosDias = serie.length >= 2 && serie.slice(-2).every((d) => d.roas >= ROAS_CORTE);
      if (dosDias && roas >= ROAS_CORTE) {
        const cae = serie.length >= 3 && serie.slice(-3).every((d, i, a) => i === 0 || d.roas < a[i - 1].roas);
        const intencionDeg = lpv >= 10 && !icRoto && ic / lpv < INT.bajo;
        if (cae || intencionDeg) {
          const motivo = cae ? "la curva viene cayendo día a día" : "la intención se degrada con las visitas intactas";
          return R("CANDIDATO CON RESERVAS", `sostuvo dos días seguidos, pero ${motivo}: mirar los días individuales antes de escalarlo`, { roas });
        }
        return R("CANDIDATO A ESCALAR", `sostuvo dos días seguidos (${serie.slice(-2).map((d) => fmt(d.roas)).join(" → ")}) y la ventana amplia acompaña`, { roas });
      }
    }

    // desacuerdo entre ventanas
    if (c.roas_corto !== undefined) {
      const corto = num(c.roas_corto);
      if ((corto >= ROAS_CORTE) !== (roas >= ROAS_CORTE)) {
        return R("ZONA GRIS", `la ventana corta y la amplia no coinciden (${fmt(corto)} contra ${fmt(roas)}): decide el operador`, { roas });
      }
    }
    // borde del corte
    if (Math.abs(roas - ROAS_CORTE) / ROAS_CORTE <= ROAS_BORDE) {
      return R("ZONA GRIS", `queda justo sobre la línea de corte (${fmt(roas)}): un día más lo define en cualquier dirección`, { roas });
    }
    if (roas < ROAS_CORTE) return R("OFF", `vende, pero lo que vuelve no paga lo que gasta en la ventana amplia (${fmt(roas)})`, { roas });
    return R("MANTENER", `la ventana amplia aguanta (${fmt(roas)})`, { roas });
  }

  // --- sin ventas ---
  const catastrofico = m.fallas.find((f) => f.nivel === "catastrofico");
  if (catastrofico) {
    const v = catastrofico.metrica === "CTR" ? fmt(catastrofico.valor) + "%" : "$" + fmt(catastrofico.valor);
    return R("OFF", `${catastrofico.metrica} catastrófico (${v}): es estructural, no se corrige con más gasto; se apaga aunque no haya llegado al piso`);
  }

  if (gasto < b.piso) {
    return R("ESPERAR", `todavía no gastó lo suficiente para juzgarlo; releerlo más tarde`);
  }

  // ROAS implausible por pasarela externa sin forma de verificar
  if (ctx.pasarelaSinTracker && m.fallas.length === 0 && lpv >= 8 && gasto >= (techoMax || 6)) {
    return R("NO DECIDIBLE", `secundarias sanas, ${lpv} visitas y cero compras registradas con pasarela externa: el ROAS puede estar incompleto. Pedir el conteo de ventas de la pasarela antes de tocarlo`);
  }

  const rotas = m.fallas.filter((f) => f.nivel === "roto");
  const flojas = m.fallas.filter((f) => f.nivel === "flojo");
  const desc = m.fallas.map((f) => `${f.metrica} ${f.metrica === "CTR" ? fmt(f.valor) + "%" : "$" + fmt(f.valor)}`).join(", ");

  if (rotas.length) {
    return R("OFF", `${desc} fuera de rango: una métrica rota no la salva un pago iniciado, solo una venta`);
  }

  const ratio = lpv ? ic / lpv : null;
  const tieneIC = !icRoto && ic >= 1;
  const soloCPC = flojas.length === 1 && flojas[0].metrica === "CPC";

  if (!icRoto && lpv >= 10 && ratio < INT.bajo) {
    return R("OFF", `tráfico sin intención de compra: ${ic} de ${lpv} visitas llegaron al pago`);
  }
  if (!icRoto && lpv >= 10 && ratio < INT.bueno && flojas.length >= 1) {
    return R("ZONA GRIS", `intención en el medio (${ic} de ${lpv}) y ${desc} fuera de rango: se puede leer para los dos lados`);
  }
  if (flojas.length >= 3) return R("OFF", `tres métricas fuera de rango (${desc})`);
  if (flojas.length === 2) {
    if (!tieneIC) return R("OFF", `${desc} fuera de rango y nadie llegó al pago`);
    return R("ZONA GRIS", `${desc} fuera de rango, pero hubo un pago iniciado: se puede leer para los dos lados`);
  }
  if (flojas.length === 1 && !soloCPC) {
    if (!tieneIC) return R("OFF", `${desc} fuera de rango y nadie llegó al pago`);
    return R("ZONA GRIS", `${desc} fuera de rango, pero hubo un pago iniciado: se puede leer para los dos lados`);
  }

  // tramo: un techo en dólares, dicho siempre
  let tramo = techoMax !== null ? techoMax : 6;
  if (flojas.length === 1) tramo = +(tramo * TRAMO_CON_FLOJA).toFixed(2);
  if (gasto >= tramo) {
    return R("OFF", `gastó $${fmt(gasto)} sin vender y las métricas no compran más tiempo`);
  }
  const razon = icRoto
    ? "los pagos iniciados están rotos en esta campaña, se juzga por CPM, CTR y CPC"
    : (lpv ? `intención ${ic} de ${lpv}` : "todavía sin visitas suficientes para leer la intención");
  const estado = desc ? `${razon}; ${desc} fuera de rango` : `${razon}; el resto en rango`;
  return R("TRAMO", `${estado} → dejarlo hasta $${fmt(tramo)}`, { techo: tramo });
}

export function veredictos(input) {
  const cfg = input.config || {};
  const camp = input.campana || {};
  const mercado = (cfg.mercado || "europa").toLowerCase();
  const b = BANDAS[mercado] || BANDAS.europa;
  const precio = cfg.precio ? num(cfg.precio) : null;
  const tipo = (camp.tipo || "abo").toLowerCase();
  const conjuntos = camp.conjuntos || [];

  // sanidad: los pagos iniciados están rotos si algún conjunto vendió sin ninguno
  const testigo = conjuntos.find((c) => num(c.compras) > 0 && num(c.ic) === 0 && num(c.lpv) > 0);
  const icRoto = Boolean(testigo);
  const pasarelaSinTracker = Boolean(cfg.pasarela_externa);
  const ctx = { b, precio, icRoto, tipo, dias: camp.dias, pasarelaSinTracker };

  const ordenados = [...conjuntos].sort((x, y) => num(y.gasto) - num(x.gasto));
  const out = ordenados.map((c) => {
    // en CBO, lo que no pasó el piso ni se juzga ni se apaga
    if (tipo !== "abo" && (c.estado || "ACTIVE").toUpperCase() !== "PAUSED"
        && num(c.gasto) < b.piso && num(c.compras) === 0) {
      const m = clasificar(c, b);
      if (!m.fallas.find((f) => f.nivel === "catastrofico")) {
        return { conjunto: c.nombre, estado: "ESPERAR", gasto: num(c.gasto),
                 por_que: "presupuesto en la campaña: todavía no le tocó gasto suficiente, ni se juzga ni se apaga" };
      }
    }
    return veredictoConjunto(c, ctx);
  });

  const vivos = out.filter((v) => !["OFF", "APAGADO"].includes(v.estado));
  const avisos = [];
  if (icRoto) avisos.push(`Pagos iniciados ROTOS en esta campaña: ${testigo.nombre} vendió sin registrar ninguno. La intención se desactivó para todos los conjuntos.`);
  if (pasarelaSinTracker) avisos.push("Cobrás por una pasarela externa: el ROAS de Meta puede estar incompleto. Antes de apagar por ROAS, cruzá con el conteo de ventas de la pasarela.");
  let campana = "SIGUE";
  if (!vivos.length && conjuntos.length) campana = "APAGAR CAMPAÑA (no queda ningún conjunto prendido)";

  const candidatos = out.filter((v) => v.estado === "CANDIDATO A ESCALAR").map((v) => v.conjunto);
  const reservas = out.filter((v) => v.estado === "CANDIDATO CON RESERVAS").map((v) => v.conjunto);
  const grises = out.filter((v) => v.estado === "ZONA GRIS").map((v) => v.conjunto);

  return {
    campana: camp.nombre, tipo, mercado, precio,
    techo_sin_venta: precio ? +(precio * (TECHO_FRAC[tipo] ?? 0.5)).toFixed(2) : null,
    ic_roto: icRoto, avisos, veredicto_campana: campana,
    candidatos, candidatos_con_reservas: reservas, zona_gris: grises, conjuntos: out,
  };
}

// ---------- CLI ----------
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith("veredicto.mjs")) {
  const args = process.argv.slice(2);
  const json = args.includes("--json");
  const file = args.find((a) => !a.startsWith("--"));
  const raw = file ? readFileSync(file, "utf8") : readFileSync(0, "utf8");
  const res = veredictos(JSON.parse(raw));
  if (json) { console.log(JSON.stringify(res, null, 2)); process.exit(0); }
  console.log(`\n${res.campana}  [${res.tipo.toUpperCase()} · ${res.mercado} · precio ${res.precio ?? "?"}]`);
  for (const a of res.avisos) console.log(`  ! ${a}`);
  console.log("");
  const w = Math.max(8, ...res.conjuntos.map((v) => v.conjunto.length));
  for (const v of res.conjuntos) {
    const mm = v.metricas
      ? `CPM ${v.metricas.cpm} · CTR ${v.metricas.ctr} · CPC ${v.metricas.cpc} · visitas/pagos ${v.metricas.lpv}/${v.metricas.ic} · compras ${v.metricas.compras}`
      : "";
    console.log(`  ${v.conjunto.padEnd(w)}  $${fmt(v.gasto).padStart(6)}  ${v.estado.padEnd(24)} ${v.por_que}`);
    if (mm) console.log(`  ${"".padEnd(w)}          ${mm}`);
  }
  console.log(`\n  Campaña: ${res.veredicto_campana}`);
  if (res.candidatos.length) console.log(`  Candidatos a escalar: ${res.candidatos.join(", ")}`);
  if (res.candidatos_con_reservas.length) console.log(`  Con reservas: ${res.candidatos_con_reservas.join(", ")}`);
  if (res.zona_gris.length) console.log(`  Zona gris (decide el operador): ${res.zona_gris.join(", ")}`);
  console.log("");
}
