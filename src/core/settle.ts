import type { Group, Transfer } from './types';

type Balances = Record<string, number>;

/**
 * Estrategia A — "sin simplificar": cada gasto genera deudas entre el pagador y cada
 * participante; solo se compensan las deudas cruzadas entre el MISMO par de personas.
 * Es lo que haría un grupo que se paga "gasto por gasto".
 */
export function naiveTransfers(g: Group): Transfer[] {
  const debt = new Map<string, number>(); // clave "deudor>acreedor"
  const add = (a: string, b: string, v: number) => {
    if (a === b || v === 0) return;
    debt.set(`${a}>${b}`, (debt.get(`${a}>${b}`) ?? 0) + v);
  };
  for (const e of g.expenses) for (const [id, v] of Object.entries(e.owed)) add(id, e.paidBy, v);
  for (const s of g.settlements) add(s.to, s.from, s.amountCents); // un pago reduce la deuda inversa

  const out: Transfer[] = [];
  const seen = new Set<string>();
  for (const key of debt.keys()) {
    const [a, b] = key.split('>');
    const pair = [a, b].sort().join('|');
    if (seen.has(pair)) continue;
    seen.add(pair);
    const ab = debt.get(`${a}>${b}`) ?? 0;
    const ba = debt.get(`${b}>${a}`) ?? 0;
    const net = ab - ba;
    if (net > 0) out.push({ from: a, to: b, amountCents: net });
    else if (net < 0) out.push({ from: b, to: a, amountCents: -net });
  }
  return out;
}

/**
 * Estrategia B — codiciosa: el que más debe le paga al que más se le debe.
 * Cada pago salda por completo al menos a una persona, así que usa a lo sumo k−1
 * transferencias (k = personas con saldo distinto de cero).
 */
export function settleGreedy(bal: Balances): Transfer[] {
  const debtors = Object.entries(bal)
    .filter(([, v]) => v < 0)
    .map(([id, v]) => ({ id, v: -v }));
  const creditors = Object.entries(bal)
    .filter(([, v]) => v > 0)
    .map(([id, v]) => ({ id, v }));
  const out: Transfer[] = [];
  while (debtors.length && creditors.length) {
    debtors.sort((a, b) => b.v - a.v);
    creditors.sort((a, b) => b.v - a.v);
    const d = debtors[0];
    const c = creditors[0];
    const amt = Math.min(d.v, c.v);
    out.push({ from: d.id, to: c.id, amountCents: amt });
    d.v -= amt;
    c.v -= amt;
    if (d.v === 0) debtors.shift();
    if (c.v === 0) creditors.shift();
  }
  return out;
}

/** Límite práctico para la búsqueda exacta (2^k estados). */
export const EXACT_LIMIT = 16;

/**
 * Estrategia C — óptima. Mínimo de transferencias = k − G, donde G es la mayor cantidad
 * de subgrupos de saldo cero en que se puede particionar a las k personas con saldo ≠ 0.
 * (Cada subgrupo de tamaño s se salda con s−1 pagos.) El problema es NP-difícil en
 * general; la programación dinámica sobre subconjuntos es O(2^k · k) y es viable para
 * los grupos pequeños típicos. Si k > EXACT_LIMIT se recurre a la estrategia B.
 */
export function settleOptimal(bal: Balances): Transfer[] {
  const people = Object.entries(bal).filter(([, v]) => v !== 0);
  const k = people.length;
  if (k === 0) return [];
  if (k > EXACT_LIMIT) return settleGreedy(bal);

  const size = 1 << k;
  const sum = new Int32Array(size);
  for (let m = 1; m < size; m++) {
    const low = m & -m;
    const i = 31 - Math.clz32(low);
    sum[m] = sum[m ^ low] + people[i][1];
  }
  const dp = new Int8Array(size);
  const prev = new Int32Array(size); // máscara previa que alcanzó el óptimo
  for (let m = 1; m < size; m++) {
    let best = -1;
    let from = 0;
    for (let i = 0; i < k; i++) {
      if (!(m & (1 << i))) continue;
      const p = m ^ (1 << i);
      if (dp[p] > best) {
        best = dp[p];
        from = p;
      }
    }
    dp[m] = best + (sum[m] === 0 ? 1 : 0);
    prev[m] = from;
  }

  // Reconstrucción: los cortes donde el acumulado vuelve a cero delimitan los grupos.
  const groups: number[][] = [];
  let m = size - 1;
  let current: number[] = [];
  while (m) {
    const p = prev[m];
    const removed = 31 - Math.clz32(m ^ p);
    current.push(removed);
    if (sum[p] === 0) {
      // p es un prefijo de saldo cero: los elementos acumulados forman un subgrupo cerrado
      groups.push(current);
      current = [];
    }
    m = p;
  }
  if (current.length) groups.push(current);

  const out: Transfer[] = [];
  for (const grp of groups) {
    const sub: Balances = {};
    grp.forEach((i) => (sub[people[i][0]] = people[i][1]));
    out.push(...settleGreedy(sub));
  }
  return out;
}

/** Solo cuenta (sin construir pagos): mínimo teórico de transferencias. */
export function minTransferCount(bal: Balances): number {
  return settleOptimal(bal).length;
}

/** Aplica transferencias a un conjunto de saldos (para verificar que todo queda en 0). */
export function applyTransfers(bal: Balances, ts: Transfer[]): Balances {
  const out = { ...bal };
  for (const t of ts) {
    out[t.from] = (out[t.from] ?? 0) + t.amountCents;
    out[t.to] = (out[t.to] ?? 0) - t.amountCents;
  }
  return out;
}
