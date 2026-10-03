import type { Group } from '@/core/types';
import { splitEqual, splitByWeights } from '@/core/split';

/** Datos de EJEMPLO para probar la app (no son datos reales de nadie). */
export function demoGroup(): Group {
  const ids = { yo: 'yo', camila: 'camila', diego: 'diego', valeria: 'valeria' };
  const all = Object.values(ids);
  const mk = (
    n: number,
    title: string,
    amountCents: number,
    paidBy: string,
    category: Group['expenses'][number]['category'],
    date: string,
    among: string[] = all,
  ) => ({
    id: `demo-e${n}`,
    title,
    amountCents,
    paidBy,
    category,
    date,
    mode: 'equal' as const,
    owed: splitEqual(amountCents, among, n),
  });
  const pollada = 8200;
  return {
    id: 'demo-grupo',
    name: 'Cuarto compartido',
    emoji: '🏠',
    meId: ids.yo,
    createdAt: '2026-10-01',
    members: [
      { id: ids.yo, name: 'Yo' },
      { id: ids.camila, name: 'Camila' },
      { id: ids.diego, name: 'Diego' },
      { id: ids.valeria, name: 'Valeria' },
    ],
    expenses: [
      mk(1, 'Alquiler de octubre', 120000, ids.camila, 'alquiler', '2026-10-01'),
      mk(2, 'Luz (Seal)', 9640, ids.yo, 'servicios', '2026-10-03'),
      mk(3, 'Agua (Sedapar)', 3870, ids.diego, 'servicios', '2026-10-03'),
      mk(4, 'Internet', 8990, ids.valeria, 'servicios', '2026-10-04'),
      mk(5, 'Mercado de la semana', 14360, ids.yo, 'comida', '2026-10-05', [ids.yo, ids.camila, ids.diego]),
      {
        id: 'demo-e6',
        title: 'Pollada del sábado',
        amountCents: pollada,
        paidBy: ids.diego,
        category: 'salida',
        date: '2026-10-08',
        mode: 'shares',
        owed: splitByWeights(pollada, { [ids.yo]: 1, [ids.camila]: 1, [ids.diego]: 2, [ids.valeria]: 1 }, 2),
      },
      mk(7, 'Taxi a la universidad', 1800, ids.valeria, 'transporte', '2026-10-09', [ids.valeria, ids.camila]),
      mk(8, 'Balón de gas', 5500, ids.camila, 'servicios', '2026-10-10'),
    ],
    settlements: [],
  };
}
