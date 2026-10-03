export type SplitMode = 'equal' | 'percent' | 'exact' | 'shares';

export type CategoryId = 'alquiler' | 'servicios' | 'comida' | 'transporte' | 'salida' | 'otros';

export interface Member {
  id: string;
  name: string;
}

export interface Expense {
  id: string;
  title: string;
  amountCents: number;
  paidBy: string;
  category: CategoryId;
  date: string; // ISO yyyy-mm-dd
  mode: SplitMode;
  /** Cuánto le corresponde a cada participante (en céntimos). La suma es igual a amountCents. */
  owed: Record<string, number>;
}

export interface Settlement {
  id: string;
  from: string; // quien paga
  to: string; // quien recibe
  amountCents: number;
  date: string;
}

export interface Group {
  id: string;
  name: string;
  emoji: string;
  meId: string;
  members: Member[];
  expenses: Expense[];
  settlements: Settlement[];
  createdAt: string;
}

export interface Transfer {
  from: string;
  to: string;
  amountCents: number;
}
