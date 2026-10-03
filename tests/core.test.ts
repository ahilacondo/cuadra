import { describe, it, expect } from 'vitest';
import { parseAmount, formatPEN } from '../src/core/money';
import { splitEqual, splitByWeights, exactDiff } from '../src/core/split';
import { computeBalances } from '../src/core/balances';
import { settleGreedy, settleOptimal, naiveTransfers, applyTransfers } from '../src/core/settle';
import type { Group } from '../src/core/types';

function rng(seed: number) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}

function randomGroup(seed: number, n: number, m: number): Group {
  const r = rng(seed);
  const members = Array.from({ length: n }, (_, i) => ({ id: `m${i}`, name: `M${i}` }));
  const ids = members.map((x) => x.id);
  const expenses = Array.from({ length: m }, (_, k) => {
    const part = ids.filter(() => r() < 0.6);
    const participants = part.length ? part : [ids[0]];
    const amount = Math.round(500 + r() * 20000);
    return {
      id: `e${k}`,
      title: 'x',
      amountCents: amount,
      paidBy: ids[Math.floor(r() * n)],
      category: 'otros' as const,
      date: '2026-10-01',
      mode: 'equal' as const,
      owed: splitEqual(amount, participants, k),
    };
  });
  return { id: 'g', name: 'g', emoji: '🏠', meId: 'm0', members, expenses, settlements: [], createdAt: '' };
}

describe('dinero', () => {
  it('parsea montos con punto o coma', () => {
    expect(parseAmount('12.5')).toBe(1250);
    expect(parseAmount('12,50')).toBe(1250);
    expect(parseAmount('0.05')).toBe(5);
    expect(parseAmount('abc')).toBeNull();
    expect(parseAmount('-3')).toBeNull();
    expect(parseAmount('1.234')).toBeNull();
  });
  it('formatea en soles', () => {
    expect(formatPEN(123450)).toBe('S/ 1,234.50');
    expect(formatPEN(-5)).toBe('-S/ 0.05');
  });
});

describe('reparto', () => {
  it('100.00 entre 3 suma exactamente 100.00 (sin errores de redondeo)', () => {
    const r = splitEqual(10000, ['a', 'b', 'c']);
    expect(Object.values(r).reduce((s, v) => s + v, 0)).toBe(10000);
    expect(Math.max(...Object.values(r)) - Math.min(...Object.values(r))).toBe(1);
  });
  it('el céntimo sobrante rota entre gastos', () => {
    const a = splitEqual(100, ['a', 'b', 'c'], 0);
    const b = splitEqual(100, ['a', 'b', 'c'], 1);
    expect(a).not.toEqual(b);
  });
  it('porcentajes y partes respetan la suma', () => {
    const p = splitByWeights(9999, { a: 50, b: 30, c: 20 });
    expect(Object.values(p).reduce((s, v) => s + v, 0)).toBe(9999);
    const q = splitByWeights(1000, { a: 2, b: 1 });
    expect(q.a).toBe(667);
    expect(q.b).toBe(333);
  });
  it('detecta montos exactos que no cuadran', () => {
    expect(exactDiff(1000, { a: 400, b: 500 })).toBe(100);
    expect(exactDiff(1000, { a: 500, b: 500 })).toBe(0);
  });
});

describe('saldos y liquidación', () => {
  it('ejemplo clásico: A paga 90 entre A,B,C', () => {
    const g: Group = {
      id: 'g', name: 'g', emoji: '', meId: 'A', createdAt: '',
      members: [{ id: 'A', name: 'A' }, { id: 'B', name: 'B' }, { id: 'C', name: 'C' }],
      expenses: [{ id: '1', title: 'cena', amountCents: 9000, paidBy: 'A', category: 'comida', date: '', mode: 'equal', owed: { A: 3000, B: 3000, C: 3000 } }],
      settlements: [],
    };
    const bal = computeBalances(g);
    expect(bal).toEqual({ A: 6000, B: -3000, C: -3000 });
    expect(settleOptimal(bal)).toHaveLength(2);
  });

  it('cadena A→B→C se reduce a un solo pago', () => {
    // A le debe 10 a B, B le debe 10 a C  =>  A paga 10 a C
    const bal = { A: -1000, B: 0, C: 1000 };
    const t = settleOptimal(bal);
    expect(t).toEqual([{ from: 'A', to: 'C', amountCents: 1000 }]);
  });

  it('propiedades sobre 300 grupos aleatorios', () => {
    for (let i = 0; i < 300; i++) {
      const n = 3 + (i % 8);
      const g = randomGroup(i + 1, n, 4 + (i % 12));
      const bal = computeBalances(g);
      expect(Object.values(bal).reduce((s, v) => s + v, 0)).toBe(0);
      const k = Object.values(bal).filter((v) => v !== 0).length;
      const gr = settleGreedy(bal);
      const op = settleOptimal(bal);
      const nv = naiveTransfers(g);
      // todos los saldos quedan en cero
      for (const v of Object.values(applyTransfers(bal, gr))) expect(v).toBe(0);
      for (const v of Object.values(applyTransfers(bal, op))) expect(v).toBe(0);
      for (const v of Object.values(applyTransfers(bal, nv))) expect(v).toBe(0);
      // jerarquía de calidad
      expect(op.length).toBeLessThanOrEqual(gr.length);
      expect(gr.length).toBeLessThanOrEqual(Math.max(0, k - 1));
      expect(op.length).toBeLessThanOrEqual(nv.length);
    }
  });

  it('los pagos registrados reducen la deuda', () => {
    const g = randomGroup(7, 4, 6);
    const before = computeBalances(g);
    const t = settleOptimal(before)[0];
    g.settlements.push({ id: 's', from: t.from, to: t.to, amountCents: t.amountCents, date: '' });
    const after = computeBalances(g);
    expect(Math.abs(after[t.from])).toBeLessThan(Math.abs(before[t.from]) + 1);
    expect(Object.values(after).reduce((s, v) => s + v, 0)).toBe(0);
  });
});
