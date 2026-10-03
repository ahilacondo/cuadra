/**
 * Reparto de un monto entero (céntimos) según pesos, con el método del mayor resto
 * (Hamilton). Garantiza que la suma de las partes sea EXACTAMENTE el total, sin
 * errores de punto flotante. `offset` rota el desempate para que el céntimo sobrante
 * no recaiga siempre en la misma persona entre un gasto y otro.
 */
export function splitByWeights(
  total: number,
  weights: Record<string, number>,
  offset = 0,
): Record<string, number> {
  const ids = Object.keys(weights);
  const out: Record<string, number> = {};
  const sumW = ids.reduce((s, id) => s + weights[id], 0);
  if (ids.length === 0 || sumW <= 0) return out;

  const parts = ids.map((id, i) => {
    const exact = (total * weights[id]) / sumW;
    const floor = Math.floor(exact);
    return { id, floor, frac: exact - floor, order: (i + offset) % ids.length };
  });
  let rest = total - parts.reduce((s, p) => s + p.floor, 0);
  const byRemainder = [...parts].sort((a, b) => b.frac - a.frac || a.order - b.order);
  for (const p of byRemainder) {
    out[p.id] = p.floor + (rest > 0 ? 1 : 0);
    if (rest > 0) rest -= 1;
  }
  return out;
}

export function splitEqual(total: number, ids: string[], offset = 0): Record<string, number> {
  const w: Record<string, number> = {};
  ids.forEach((id) => (w[id] = 1));
  return splitByWeights(total, w, offset);
}

/** Diferencia entre el total y la suma de montos exactos (0 = cuadra). */
export function exactDiff(total: number, amounts: Record<string, number>): number {
  return total - Object.values(amounts).reduce((s, v) => s + v, 0);
}
