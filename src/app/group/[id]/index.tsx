import { useMemo, useState } from 'react';
import { Linking, Pressable, Text, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import * as Clipboard from 'expo-clipboard';
import { Feather } from '@expo/vector-icons';
import { useStore } from '@/state/store';
import { computeBalances, owedByMember, paidByMember, spentByCategory, totalSpent } from '@/core/balances';
import { naiveTransfers, settleOptimal, EXACT_LIMIT } from '@/core/settle';
import { formatPEN } from '@/core/money';
import { fmtDate } from '@/core/format';
import { CATEGORIES, categoryOf } from '@/data/categories';
import type { Group, Transfer } from '@/core/types';
import { Avatar, Button, Card, Empty, Screen, Segmented, TopBar, textStyles } from '@/ui/kit';
import { colors } from '@/ui/theme';

type Tab = 'gastos' | 'saldos' | 'liquidar' | 'resumen';

export default function GroupScreen() {
  const { id, tab: tabParam } = useLocalSearchParams<{ id: string; tab?: string }>();
  const r = useRouter();
  const { getGroup, deleteGroup } = useStore();
  const g = getGroup(String(id));
  const [tab, setTab] = useState<Tab>((['gastos', 'saldos', 'liquidar', 'resumen'].includes(String(tabParam)) ? tabParam : 'gastos') as Tab);
  const [confirmDel, setConfirmDel] = useState(false);

  if (!g) {
    return (
      <Screen>
        <TopBar title="Grupo" onBack={() => r.replace('/')} />
        <Empty icon="alert-circle" title="Grupo no encontrado" text="Puede que se haya eliminado.">
          <Button label="Volver al inicio" onPress={() => r.replace('/')} />
        </Empty>
      </Screen>
    );
  }

  const bal = computeBalances(g);
  const mine = bal[g.meId] ?? 0;
  const idx = (mid: string) => Math.max(0, g.members.findIndex((m) => m.id === mid));
  const name = (mid: string) => g.members.find((m) => m.id === mid)?.name ?? '?';

  return (
    <Screen
      footer={
        tab === 'gastos' ? (
          <View style={{ padding: 16, paddingTop: 4 }}>
            <Button testID="btn-add-expense" label="Añadir gasto" icon="plus" onPress={() => r.push(`/group/${g.id}/expense`)} />
          </View>
        ) : null
      }
    >
      <TopBar
        title={`${g.emoji}  ${g.name}`}
        subtitle={`${g.members.length} personas`}
        onBack={() => r.replace('/')}
        right={
          <Pressable
            testID="btn-delete-group"
            hitSlop={10}
            onPress={() => {
              if (confirmDel) {
                deleteGroup(g.id);
                r.replace('/');
              } else setConfirmDel(true);
            }}
            style={{ paddingHorizontal: 10, paddingVertical: 8, borderRadius: 12, backgroundColor: confirmDel ? colors.accent : 'transparent' }}
          >
            {confirmDel ? <Text style={{ color: '#fff', fontWeight: '700', fontSize: 12.5 }}>¿Eliminar grupo?</Text> : <Feather name="trash-2" size={18} color={colors.inkSoft} />}
          </Pressable>
        }
      />

      <Card style={{ backgroundColor: mine >= 0 ? colors.primary : colors.accent, marginBottom: 14 }}>
        <Text style={{ color: 'rgba(255,255,255,0.8)', fontSize: 13, fontWeight: '600' }}>Tu saldo en el grupo</Text>
        <Text testID="my-balance" style={{ color: '#fff', fontSize: 30, fontWeight: '800', marginTop: 2 }}>
          {mine === 0 ? 'Estás al día' : formatPEN(Math.abs(mine))}
        </Text>
        {mine !== 0 ? <Text style={{ color: '#fff', fontSize: 14, fontWeight: '600' }}>{mine > 0 ? 'te deben en total' : 'debes en total'}</Text> : null}
        <Text style={{ color: 'rgba(255,255,255,0.8)', fontSize: 12.5, marginTop: 8 }}>Gasto total del grupo: {formatPEN(totalSpent(g))}</Text>
      </Card>

      <View style={{ marginBottom: 14 }}>
        <Segmented
          value={tab}
          onChange={(v) => setTab(v as Tab)}
          options={[
            { id: 'gastos', label: 'Gastos' },
            { id: 'saldos', label: 'Saldos' },
            { id: 'liquidar', label: 'Liquidar' },
            { id: 'resumen', label: 'Resumen' },
          ]}
        />
      </View>

      {tab === 'gastos' && <Gastos g={g} name={name} />}
      {tab === 'saldos' && <Saldos g={g} bal={bal} idx={idx} />}
      {tab === 'liquidar' && <Liquidar g={g} bal={bal} idx={idx} name={name} />}
      {tab === 'resumen' && <Resumen g={g} idx={idx} />}
    </Screen>
  );
}

function Gastos({ g, name }: { g: Group; name: (id: string) => string }) {
  const r = useRouter();
  const { deleteExpense } = useStore();
  const [pending, setPending] = useState<string | null>(null);
  type Row = { kind: 'e' | 's'; date: string; id: string };
  const rows: Row[] = [
    ...g.expenses.map((e) => ({ kind: 'e' as const, date: e.date, id: e.id })),
    ...g.settlements.map((s) => ({ kind: 's' as const, date: s.date, id: s.id })),
  ].sort((a, b) => (a.date < b.date ? 1 : -1));

  if (rows.length === 0)
    return <Empty icon="file-text" title="Sin gastos todavía" text="Anota el primer gasto: quién pagó, cuánto fue y entre quiénes se reparte." />;

  return (
    <View style={{ gap: 10 }}>
      {rows.map((row) => {
        if (row.kind === 's') {
          const s = g.settlements.find((x) => x.id === row.id)!;
          return (
            <Card key={s.id} style={{ flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: colors.primarySoft }}>
              <View style={{ width: 40, height: 40, borderRadius: 12, backgroundColor: '#fff', alignItems: 'center', justifyContent: 'center' }}>
                <Feather name="check-circle" size={20} color={colors.primary} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={textStyles.body}>{name(s.from)} le pagó a {name(s.to)}</Text>
                <Text style={textStyles.soft}>Pago registrado · {fmtDate(s.date)}</Text>
              </View>
              <Text style={{ fontWeight: '800', color: colors.primaryDark }}>{formatPEN(s.amountCents)}</Text>
            </Card>
          );
        }
        const e = g.expenses.find((x) => x.id === row.id)!;
        const c = categoryOf(e.category);
        const my = e.owed[g.meId];
        return (
          <Card key={e.id} style={{ padding: 0 }}>
            <Pressable testID={`expense-${e.id}`} onPress={() => r.push(`/group/${g.id}/expense?eid=${e.id}`)} style={{ flexDirection: 'row', alignItems: 'center', gap: 12, padding: 14 }}>
              <View style={{ width: 40, height: 40, borderRadius: 12, backgroundColor: c.color + '22', alignItems: 'center', justifyContent: 'center' }}>
                <Feather name={c.icon as any} size={19} color={c.color} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={textStyles.body} numberOfLines={1}>{e.title}</Text>
                <Text style={textStyles.soft} numberOfLines={1}>Pagó {name(e.paidBy)} · {fmtDate(e.date)} · {Object.keys(e.owed).length} pers.</Text>
              </View>
              <View style={{ alignItems: 'flex-end' }}>
                <Text style={{ fontWeight: '800', color: colors.ink, fontSize: 15.5 }}>{formatPEN(e.amountCents)}</Text>
                <Text style={{ fontSize: 12, color: colors.inkSoft }}>{my ? `tu parte ${formatPEN(my)}` : 'no participas'}</Text>
              </View>
            </Pressable>
            <View style={{ flexDirection: 'row', justifyContent: 'flex-end', paddingHorizontal: 14, paddingBottom: 10, marginTop: -4 }}>
              <Pressable
                testID={`del-${e.id}`}
                hitSlop={{ top: 14, bottom: 14, left: 24, right: 8 }}
                onPress={() => (pending === e.id ? deleteExpense(g.id, e.id) : setPending(e.id))}
              >
                <Text style={{ fontSize: 12.5, fontWeight: '700', color: pending === e.id ? colors.accent : colors.inkSoft }}>
                  {pending === e.id ? 'Toca otra vez para eliminar' : 'Eliminar'}
                </Text>
              </Pressable>
            </View>
          </Card>
        );
      })}
    </View>
  );
}

function Saldos({ g, bal, idx }: { g: Group; bal: Record<string, number>; idx: (id: string) => number }) {
  const max = Math.max(1, ...Object.values(bal).map(Math.abs));
  return (
    <Card style={{ gap: 14 }}>
      <Text style={textStyles.soft}>Verde: le deben dinero · Rojo: debe dinero</Text>
      {g.members.map((m) => {
        const v = bal[m.id] ?? 0;
        const w = (Math.abs(v) / max) * 100;
        return (
          <View key={m.id} testID={`bal-${m.id}`} style={{ gap: 6 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
              <Avatar name={m.name} index={idx(m.id)} size={30} />
              <Text style={{ flex: 1, fontWeight: '700', color: colors.ink, fontSize: 15 }}>{m.name}{m.id === g.meId ? ' (tú)' : ''}</Text>
              <Text style={{ fontWeight: '800', fontSize: 15, color: v === 0 ? colors.inkSoft : v > 0 ? colors.pos : colors.neg }}>
                {v > 0 ? '+' : ''}{formatPEN(v)}
              </Text>
            </View>
            <View style={{ height: 8, backgroundColor: '#EFE9DD', borderRadius: 4, overflow: 'hidden' }}>
              <View style={{ width: `${w}%`, height: 8, borderRadius: 4, backgroundColor: v >= 0 ? colors.pos : colors.neg }} />
            </View>
          </View>
        );
      })}
    </Card>
  );
}

function summaryText(g: Group, ts: Transfer[], name: (id: string) => string) {
  const lines = ts.map((t) => `• ${name(t.from)} → ${name(t.to)}: ${formatPEN(t.amountCents)}`);
  return `Cuentas de "${g.name}" (Cuadra)\n${lines.length ? lines.join('\n') : 'Todos están al día 🎉'}`;
}

function Liquidar({ g, bal, idx, name }: { g: Group; bal: Record<string, number>; idx: (id: string) => number; name: (id: string) => string }) {
  const { addSettlement } = useStore();
  const [copied, setCopied] = useState(false);
  const naive = useMemo(() => naiveTransfers(g), [g]);
  const best = useMemo(() => settleOptimal(bal), [bal]);
  const k = Object.values(bal).filter((v) => v !== 0).length;
  const saved = naive.length - best.length;

  if (best.length === 0)
    return <Empty icon="smile" title="¡Todos al día!" text="No hay deudas pendientes en este grupo. Cuando se registren nuevos gastos, aquí aparecerá cómo cuadrar." />;

  const text = summaryText(g, best, name);
  const copy = async () => {
    await Clipboard.setStringAsync(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  const wa = () => Linking.openURL(`https://wa.me/?text=${encodeURIComponent(text)}`);

  return (
    <View style={{ gap: 12 }}>
      <Card style={{ gap: 12 }}>
        <Text style={textStyles.h2}>Cuántos pagos hacen falta</Text>
        <View style={{ flexDirection: 'row', gap: 10 }}>
          <View style={{ flex: 1, backgroundColor: '#F1ECE1', borderRadius: 14, padding: 12 }}>
            <Text style={textStyles.soft}>Sin simplificar</Text>
            <Text testID="naive-count" style={{ fontSize: 28, fontWeight: '800', color: colors.inkSoft }}>{naive.length}</Text>
          </View>
          <View style={{ flex: 1, backgroundColor: colors.primarySoft, borderRadius: 14, padding: 12 }}>
            <Text style={{ fontSize: 13, color: colors.primaryDark }}>Con Cuadra</Text>
            <Text testID="best-count" style={{ fontSize: 28, fontWeight: '800', color: colors.primary }}>{best.length}</Text>
          </View>
        </View>
        <Text style={textStyles.soft}>
          {saved > 0 ? `Te ahorras ${saved} ${saved === 1 ? 'pago' : 'pagos'}. ` : ''}
          {k <= EXACT_LIMIT ? 'Calculado con búsqueda exacta (mínimo posible).' : 'Grupo grande: se usó una heurística.'}
        </Text>
      </Card>

      {best.map((t, i) => (
        <Card key={`${t.from}-${t.to}-${i}`} style={{ gap: 12 }}>
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
            <Avatar name={name(t.from)} index={idx(t.from)} />
            <Feather name="arrow-right" size={18} color={colors.inkSoft} />
            <Avatar name={name(t.to)} index={idx(t.to)} />
            <View style={{ flex: 1, marginLeft: 4 }}>
              <Text style={{ fontWeight: '700', color: colors.ink, fontSize: 15 }}>{name(t.from)} paga a {name(t.to)}</Text>
              <Text style={{ fontWeight: '800', color: colors.accent, fontSize: 18 }}>{formatPEN(t.amountCents)}</Text>
            </View>
          </View>
          <Button testID={`pay-${i}`} variant="soft" icon="check" label="Registrar como pagado" onPress={() => addSettlement(g.id, { from: t.from, to: t.to, amountCents: t.amountCents })} />
        </Card>
      ))}

      <View style={{ flexDirection: 'row', gap: 10 }}>
        <View style={{ flex: 1 }}><Button testID="btn-copy" variant="ghost" icon={copied ? 'check' : 'copy'} label={copied ? 'Copiado' : 'Copiar resumen'} onPress={copy} /></View>
        <View style={{ flex: 1 }}><Button testID="btn-wa" variant="ghost" icon="send" label="WhatsApp" onPress={wa} /></View>
      </View>
    </View>
  );
}

function Resumen({ g, idx }: { g: Group; idx: (id: string) => number }) {
  const total = totalSpent(g);
  const byCat = spentByCategory(g);
  const paid = paidByMember(g);
  const owed = owedByMember(g);
  const maxCat = Math.max(1, ...Object.values(byCat));
  if (g.expenses.length === 0) return <Empty icon="bar-chart-2" title="Sin datos aún" text="Cuando registres gastos verás aquí en qué se va el dinero del grupo." />;
  return (
    <View style={{ gap: 12 }}>
      <View style={{ flexDirection: 'row', gap: 10 }}>
        <Card style={{ flex: 1 }}>
          <Text style={textStyles.soft}>Total</Text>
          <Text style={{ fontSize: 20, fontWeight: '800', color: colors.ink }}>{formatPEN(total)}</Text>
        </Card>
        <Card style={{ flex: 1 }}>
          <Text style={textStyles.soft}>Promedio por persona</Text>
          <Text style={{ fontSize: 20, fontWeight: '800', color: colors.ink }}>{formatPEN(Math.round(total / g.members.length))}</Text>
        </Card>
      </View>
      <Card style={{ gap: 12 }}>
        <Text style={textStyles.h2}>Gasto por categoría</Text>
        {CATEGORIES.filter((c) => byCat[c.id]).sort((a, b) => byCat[b.id] - byCat[a.id]).map((c) => (
          <View key={c.id} style={{ gap: 5 }}>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
              <Text style={{ fontWeight: '600', color: colors.ink }}>{c.label}</Text>
              <Text style={{ color: colors.inkSoft, fontWeight: '600' }}>{formatPEN(byCat[c.id])} · {Math.round((byCat[c.id] / total) * 100)}%</Text>
            </View>
            <View style={{ height: 10, backgroundColor: '#EFE9DD', borderRadius: 5, overflow: 'hidden' }}>
              <View style={{ width: `${(byCat[c.id] / maxCat) * 100}%`, height: 10, backgroundColor: c.color, borderRadius: 5 }} />
            </View>
          </View>
        ))}
      </Card>
      <Card style={{ gap: 10 }}>
        <Text style={textStyles.h2}>Pagado vs. le corresponde</Text>
        <View style={{ flexDirection: 'row', justifyContent: 'flex-end', gap: 10 }}>
          <Text style={{ width: 92, textAlign: 'right', fontSize: 11.5, color: colors.inkSoft }}>pagó</Text>
          <Text style={{ width: 92, textAlign: 'right', fontSize: 11.5, color: colors.inkSoft }}>le corresponde</Text>
        </View>
        {g.members.map((m) => (
          <View key={m.id} style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
            <Avatar name={m.name} index={idx(m.id)} size={28} />
            <Text style={{ flex: 1, fontWeight: '600', color: colors.ink }}>{m.name}</Text>
            <Text style={{ width: 92, textAlign: 'right', color: colors.ink, fontWeight: '700' }}>{formatPEN(paid[m.id])}</Text>
            <Text style={{ width: 92, textAlign: 'right', color: colors.inkSoft, fontWeight: '600' }}>{formatPEN(owed[m.id])}</Text>
          </View>
        ))}
      </Card>
    </View>
  );
}
