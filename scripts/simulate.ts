/**
 * Experimento Monte Carlo: ¿cuántas transferencias hacen falta para cuadrar un grupo?
 * Compara cuatro estrategias usando EXACTAMENTE el mismo código que la app.
 * Uso: npx tsx scripts/simulate.ts > ../data/sim.json
 */
import { computeBalances } from '../src/core/balances';
import { naiveTransfers, settleGreedy, settleOptimal } from '../src/core/settle';
import { splitEqual } from '../src/core/split';
import type { Group } from '../src/core/types';

function rng(seed: number) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}
function normal(r: () => number) {
  const u = Math.max(r(), 1e-12), v = r();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

/** Supuestos del modelo (declarados en el informe): montos lognormales (mediana S/60), participación 70 %. */
function makeGroup(r: () => number, n: number, m: number, rounded: boolean): { g: Group; perExpense: number } {
  const ids = Array.from({ length: n }, (_, i) => `p${i}`);
  let perExpense = 0;
  const expenses = Array.from({ length: m }, (_, k) => {
    let part = ids.filter(() => r() < 0.7);
    while (part.length < 2) part = ids.filter(() => r() < 0.7);
    let amt = Math.min(150000, Math.max(500, Math.round(Math.exp(Math.log(6000) + 0.9 * normal(r)))));
    if (rounded) amt = Math.max(500, Math.round(amt / 500) * 500); // montos en múltiplos de S/ 5
    const paidBy = ids[Math.floor(r() * n)];
    perExpense += part.filter((x) => x !== paidBy).length;
    return { id: `e${k}`, title: '', amountCents: amt, paidBy, category: 'otros' as const, date: '', mode: 'equal' as const, owed: splitEqual(amt, part, k) };
  });
  return {
    g: { id: 'g', name: '', emoji: '', meId: ids[0], members: ids.map((id) => ({ id, name: id })), expenses, settlements: [], createdAt: '' },
    perExpense,
  };
}

const sizes = [3, 4, 5, 6, 8, 10, 12];
const counts = [5, 10, 20];
const TRIALS = 2000;
const rows: any[] = [];
for (const scenario of ['continuo', 'redondeado']) {
 for (const n of sizes) {
  for (const m of counts) {
    const r = rng(1000 * n + m + (scenario === 'redondeado' ? 7 : 0));
    for (let t = 0; t < TRIALS; t++) {
      const { g, perExpense } = makeGroup(r, n, m, scenario === 'redondeado');
      const bal = computeBalances(g);
      const k = Object.values(bal).filter((v) => v !== 0).length;
      rows.push({
        scenario, n, m, t, k,
        perExpense,
        naive: naiveTransfers(g).length,
        greedy: settleGreedy(bal).length,
        optimal: settleOptimal(bal).length,
      });
    }
  }
 }
}

// Escalamiento del tiempo de la búsqueda exacta (peor caso: k = n personas con saldo distinto de cero)
const timing: any[] = [];
for (const k of [6, 8, 10, 12, 14, 16, 18, 20]) {
  const r = rng(77 + k);
  const samples: number[] = [];
  const reps = k <= 16 ? 30 : 5;
  for (let i = 0; i < reps; i++) {
    const bal: Record<string, number> = {};
    let s = 0;
    for (let j = 0; j < k - 1; j++) {
      const v = Math.round((r() - 0.5) * 20000) || 1;
      bal[`p${j}`] = v;
      s += v;
    }
    bal[`p${k - 1}`] = -s || 1;
    // Para medir el algoritmo exacto saltándonos el límite práctico, se invoca la DP directamente.
    const t0 = performance.now();
    settleOptimalForced(bal);
    samples.push(performance.now() - t0);
  }
  samples.sort((a, b) => a - b);
  timing.push({ k, median_ms: samples[Math.floor(samples.length / 2)], reps });
}

function settleOptimalForced(bal: Record<string, number>) {
  const people = Object.entries(bal).filter(([, v]) => v !== 0);
  const k = people.length;
  const size = 1 << k;
  const sum = new Int32Array(size);
  for (let m = 1; m < size; m++) {
    const low = m & -m;
    sum[m] = sum[m ^ low] + people[31 - Math.clz32(low)][1];
  }
  const dp = new Int8Array(size);
  for (let m = 1; m < size; m++) {
    let best = -1;
    for (let i = 0; i < k; i++) if (m & (1 << i)) best = Math.max(best, dp[m ^ (1 << i)]);
    dp[m] = best + (sum[m] === 0 ? 1 : 0);
  }
  return dp[size - 1];
}

console.log(JSON.stringify({ trials: TRIALS, sizes, counts, rows, timing }));
