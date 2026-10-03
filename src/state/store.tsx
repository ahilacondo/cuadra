import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Expense, Group, Settlement } from '@/core/types';
import { demoGroup } from '@/data/demo';

const KEY = 'cuadra.v1';

export const uid = () => Math.random().toString(36).slice(2, 9) + Date.now().toString(36).slice(-4);
export const today = () => new Date().toISOString().slice(0, 10);

interface Store {
  hydrated: boolean;
  groups: Group[];
  getGroup: (id: string) => Group | undefined;
  createGroup: (name: string, emoji: string, memberNames: string[]) => string;
  deleteGroup: (id: string) => void;
  saveExpense: (groupId: string, e: Expense) => void;
  deleteExpense: (groupId: string, expenseId: string) => void;
  addSettlement: (groupId: string, s: Omit<Settlement, 'id' | 'date'>) => void;
  loadDemo: () => string;
  resetAll: () => void;
}

const Ctx = createContext<Store | null>(null);

export function StoreProvider({ children }: { children: React.ReactNode }) {
  const [groups, setGroups] = useState<Group[]>([]);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(KEY)
      .then((raw) => {
        if (raw) setGroups(JSON.parse(raw));
      })
      .catch(() => {})
      .finally(() => setHydrated(true));
  }, []);

  useEffect(() => {
    if (hydrated) AsyncStorage.setItem(KEY, JSON.stringify(groups)).catch(() => {});
  }, [groups, hydrated]);

  const patch = useCallback(
    (id: string, fn: (g: Group) => Group) => setGroups((gs) => gs.map((g) => (g.id === id ? fn(g) : g))),
    [],
  );

  const value = useMemo<Store>(
    () => ({
      hydrated,
      groups,
      getGroup: (id) => groups.find((g) => g.id === id),
      createGroup: (name, emoji, memberNames) => {
        const id = uid();
        const members = memberNames.map((n, i) => ({ id: i === 0 ? 'yo-' + id : uid(), name: n }));
        setGroups((gs) => [
          { id, name, emoji, meId: members[0].id, members, expenses: [], settlements: [], createdAt: today() },
          ...gs,
        ]);
        return id;
      },
      deleteGroup: (id) => setGroups((gs) => gs.filter((g) => g.id !== id)),
      saveExpense: (gid, e) =>
        patch(gid, (g) => {
          const exists = g.expenses.some((x) => x.id === e.id);
          return { ...g, expenses: exists ? g.expenses.map((x) => (x.id === e.id ? e : x)) : [e, ...g.expenses] };
        }),
      deleteExpense: (gid, eid) => patch(gid, (g) => ({ ...g, expenses: g.expenses.filter((x) => x.id !== eid) })),
      addSettlement: (gid, s) =>
        patch(gid, (g) => ({ ...g, settlements: [{ ...s, id: uid(), date: today() }, ...g.settlements] })),
      loadDemo: () => {
        const d = demoGroup();
        setGroups((gs) => [d, ...gs.filter((g) => g.id !== d.id)]);
        return d.id;
      },
      resetAll: () => setGroups([]),
    }),
    [groups, hydrated, patch],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useStore() {
  const c = useContext(Ctx);
  if (!c) throw new Error('StoreProvider ausente');
  return c;
}
