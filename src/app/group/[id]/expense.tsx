import { useMemo, useState } from 'react';
import { Pressable, Text, TextInput, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { today, uid, useStore } from '@/state/store';
import { centsToInput, formatPEN, parseAmount } from '@/core/money';
import { exactDiff, splitByWeights, splitEqual } from '@/core/split';
import { isIsoDate } from '@/core/format';
import { CATEGORIES } from '@/data/categories';
import type { CategoryId, Expense, SplitMode } from '@/core/types';
import { Avatar, Button, Card, Chip, Empty, Field, Screen, Segmented, TopBar } from '@/ui/kit';
import { colors } from '@/ui/theme';

const MODES: { id: SplitMode; label: string }[] = [
  { id: 'equal', label: 'Igual' },
  { id: 'percent', label: '%' },
  { id: 'exact', label: 'Montos' },
  { id: 'shares', label: 'Partes' },
];

export default function ExpenseForm() {
  const { id, eid } = useLocalSearchParams<{ id: string; eid?: string }>();
  const r = useRouter();
  const { getGroup, saveExpense } = useStore();
  const g = getGroup(String(id));
  const editing = g?.expenses.find((e) => e.id === eid);

  const [title, setTitle] = useState(editing?.title ?? '');
  const [amountText, setAmountText] = useState(editing ? centsToInput(editing.amountCents) : '');
  const [category, setCategory] = useState<CategoryId>(editing?.category ?? 'comida');
  const [paidBy, setPaidBy] = useState(editing?.paidBy ?? g?.meId ?? '');
  const [date, setDate] = useState(editing?.date ?? today());
  const [mode, setMode] = useState<SplitMode>(editing?.mode ?? 'equal');
  const [selected, setSelected] = useState<string[]>(editing ? Object.keys(editing.owed) : g?.members.map((m) => m.id) ?? []);
  const [vals, setVals] = useState<Record<string, string>>(() => {
    if (!editing) return {};
    const v: Record<string, string> = {};
    for (const [mid, c] of Object.entries(editing.owed)) v[mid] = editing.mode === 'exact' ? centsToInput(c) : '';
    return v;
  });
  const [tried, setTried] = useState(false);

  const total = parseAmount(amountText);

  const calc = useMemo(() => {
    if (!g) return { owed: {} as Record<string, number>, error: undefined as string | undefined };
    if (selected.length === 0) return { owed: {}, error: 'Elige al menos a una persona' };
    if (!total) return { owed: {}, error: undefined };
    const offset = g.expenses.length;
    if (mode === 'equal') return { owed: splitEqual(total, selected, offset), error: undefined };
    if (mode === 'exact') {
      const a: Record<string, number> = {};
      selected.forEach((m) => (a[m] = parseAmount(vals[m] ?? '') ?? 0));
      const d = exactDiff(total, a);
      return { owed: a, error: d === 0 ? undefined : d > 0 ? `Faltan ${formatPEN(d)} por asignar` : `Te pasas por ${formatPEN(-d)}` };
    }
    const w: Record<string, number> = {};
    selected.forEach((m) => {
      const n = parseFloat((vals[m] ?? '').replace(',', '.'));
      w[m] = isFinite(n) && n > 0 ? n : 0;
    });
    const sumW = Object.values(w).reduce((s, x) => s + x, 0);
    if (sumW === 0) return { owed: {}, error: mode === 'percent' ? 'Indica el porcentaje de cada uno' : 'Indica las partes de cada uno' };
    if (mode === 'percent' && Math.abs(sumW - 100) > 0.001) return { owed: splitByWeights(total, w, offset), error: `Los porcentajes suman ${sumW}% (deben sumar 100%)` };
    return { owed: splitByWeights(total, w, offset), error: undefined };
  }, [g, selected, total, mode, vals]);

  if (!g)
    return (
      <Screen>
        <TopBar title="Gasto" onBack={() => r.back()} />
        <Empty icon="alert-circle" title="Grupo no encontrado" text="Vuelve al inicio e inténtalo de nuevo." />
      </Screen>
    );

  const titleErr = tried && title.trim().length < 2 ? 'Describe el gasto (ej. Luz de octubre)' : undefined;
  const amountErr = tried && !total ? 'Ingresa un monto válido, ej. 45.50' : undefined;
  const dateErr = tried && !isIsoDate(date) ? 'Usa el formato AAAA-MM-DD' : undefined;

  const toggle = (mid: string) => {
    setSelected((s) => (s.includes(mid) ? s.filter((x) => x !== mid) : [...s, mid]));
  };
  const changeMode = (m: SplitMode) => {
    setMode(m);
    const v: Record<string, string> = {};
    if (m === 'percent') selected.forEach((x) => (v[x] = (100 / selected.length).toFixed(2).replace(/\.?0+$/, '')));
    if (m === 'shares') selected.forEach((x) => (v[x] = '1'));
    if (m === 'exact' && total) {
      const eq = splitEqual(total, selected);
      selected.forEach((x) => (v[x] = centsToInput(eq[x])));
    }
    setVals(v);
  };

  const save = () => {
    setTried(true);
    if (title.trim().length < 2 || !total || !isIsoDate(date) || calc.error) return;
    const e: Expense = {
      id: editing?.id ?? uid(),
      title: title.trim(),
      amountCents: total,
      paidBy,
      category,
      date,
      mode,
      owed: calc.owed,
    };
    saveExpense(g.id, e);
    r.back();
  };

  const sumPreview = Object.values(calc.owed).reduce((s, v) => s + v, 0);

  return (
    <Screen footer={<View style={{ padding: 16, paddingTop: 4 }}><Button testID="btn-save-expense" label={editing ? 'Guardar cambios' : 'Guardar gasto'} icon="check" onPress={save} /></View>}>
      <TopBar title={editing ? 'Editar gasto' : 'Nuevo gasto'} subtitle={g.name} onBack={() => r.back()} />

      <Field testID="input-title" label="¿Qué se pagó?" placeholder="Ej. Luz de octubre" value={title} onChangeText={setTitle} error={titleErr} />
      <Field testID="input-amount" label="Monto (S/)" placeholder="0.00" keyboardType="decimal-pad" value={amountText} onChangeText={setAmountText} error={amountErr} />

      <Text style={lbl}>Categoría</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
        {CATEGORIES.map((c) => (
          <Chip key={c.id} testID={`cat-${c.id}`} label={c.label} icon={c.icon as any} color={c.color} selected={category === c.id} onPress={() => setCategory(c.id)} />
        ))}
      </View>

      <Text style={lbl}>¿Quién pagó?</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
        {g.members.map((m) => (
          <Chip key={m.id} testID={`paid-${m.id}`} label={m.id === g.meId ? `${m.name} (tú)` : m.name} selected={paidBy === m.id} onPress={() => setPaidBy(m.id)} />
        ))}
      </View>

      <Field testID="input-date" label="Fecha" placeholder="AAAA-MM-DD" value={date} onChangeText={setDate} error={dateErr} />

      <Text style={lbl}>¿Cómo se reparte?</Text>
      <Segmented value={mode} onChange={(v) => changeMode(v as SplitMode)} options={MODES} />

      <Text style={[lbl, { marginTop: 16 }]}>¿Entre quiénes?</Text>
      <Card style={{ gap: 12 }}>
        {g.members.map((m, i) => {
          const on = selected.includes(m.id);
          return (
            <View key={m.id} style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
              <Pressable testID={`part-${m.id}`} onPress={() => toggle(m.id)} style={{ flexDirection: 'row', alignItems: 'center', gap: 12, flex: 1, minHeight: 40 }}>
                <View style={{ width: 24, height: 24, borderRadius: 7, borderWidth: 2, borderColor: on ? colors.primary : colors.line, backgroundColor: on ? colors.primary : '#fff', alignItems: 'center', justifyContent: 'center' }}>
                  {on ? <Feather name="check" size={15} color="#fff" /> : null}
                </View>
                <Avatar name={m.name} index={i} size={30} />
                <Text style={{ fontWeight: '600', color: on ? colors.ink : colors.inkSoft, fontSize: 15 }}>{m.name}</Text>
              </Pressable>
              {on && mode !== 'equal' ? (
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                  <TextInput
                    testID={`val-${m.id}`}
                    value={vals[m.id] ?? ''}
                    onChangeText={(t) => setVals({ ...vals, [m.id]: t })}
                    keyboardType="decimal-pad"
                    style={{ width: 78, textAlign: 'right', borderWidth: 1.5, borderColor: colors.line, borderRadius: 10, paddingHorizontal: 10, paddingVertical: 8, fontSize: 15, color: colors.ink, backgroundColor: '#fff' }}
                  />
                  <Text style={{ width: 22, color: colors.inkSoft, fontWeight: '700' }}>{mode === 'percent' ? '%' : mode === 'shares' ? 'pt' : 'S/'}</Text>
                </View>
              ) : null}
              {on && total ? <Text style={{ width: 84, textAlign: 'right', fontWeight: '800', color: colors.ink }}>{formatPEN(calc.owed[m.id] ?? 0)}</Text> : null}
            </View>
          );
        })}
      </Card>

      {total && selected.length ? (
        <View style={{ marginTop: 10 }}>
          {calc.error ? (
            <Text testID="split-error" style={{ color: colors.accent, fontWeight: '700', fontSize: 13.5 }}>⚠ {calc.error}</Text>
          ) : (
            <Text testID="split-ok" style={{ color: colors.primary, fontWeight: '700', fontSize: 13.5 }}>✓ El reparto cuadra: {formatPEN(sumPreview)} de {formatPEN(total)}</Text>
          )}
        </View>
      ) : null}
    </Screen>
  );
}

const lbl = { fontSize: 13, fontWeight: '700' as const, color: colors.inkSoft, marginBottom: 8 };
