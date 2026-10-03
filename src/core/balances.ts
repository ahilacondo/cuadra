import type { Group } from './types';

/**
 * Saldo neto por miembro en céntimos.
 *  > 0  : le deben dinero (pagó de más)
 *  < 0  : debe dinero (pagó de menos)
 * La suma de todos los saldos es siempre 0.
 */
export function computeBalances(g: Group): Record<string, number> {
  const bal: Record<string, number> = {};
  g.members.forEach((m) => (bal[m.id] = 0));
  for (const e of g.expenses) {
    bal[e.paidBy] = (bal[e.paidBy] ?? 0) + e.amountCents;
    for (const [id, v] of Object.entries(e.owed)) bal[id] = (bal[id] ?? 0) - v;
  }
  for (const s of g.settlements) {
    bal[s.from] = (bal[s.from] ?? 0) + s.amountCents;
    bal[s.to] = (bal[s.to] ?? 0) - s.amountCents;
  }
  return bal;
}

export function totalSpent(g: Group): number {
  return g.expenses.reduce((s, e) => s + e.amountCents, 0);
}

export function paidByMember(g: Group): Record<string, number> {
  const out: Record<string, number> = {};
  g.members.forEach((m) => (out[m.id] = 0));
  g.expenses.forEach((e) => (out[e.paidBy] += e.amountCents));
  return out;
}

export function owedByMember(g: Group): Record<string, number> {
  const out: Record<string, number> = {};
  g.members.forEach((m) => (out[m.id] = 0));
  g.expenses.forEach((e) => Object.entries(e.owed).forEach(([id, v]) => (out[id] += v)));
  return out;
}

export function spentByCategory(g: Group): Record<string, number> {
  const out: Record<string, number> = {};
  g.expenses.forEach((e) => (out[e.category] = (out[e.category] ?? 0) + e.amountCents));
  return out;
}
