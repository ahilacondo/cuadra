import { Pressable, Text, View } from 'react-native';
import { useRouter } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { useStore } from '@/state/store';
import { computeBalances, totalSpent } from '@/core/balances';
import { formatPEN } from '@/core/money';
import { Button, Card, Empty, Screen, TopBar, textStyles } from '@/ui/kit';
import { colors } from '@/ui/theme';

export default function Home() {
  const r = useRouter();
  const { groups, hydrated, loadDemo } = useStore();

  return (
    <Screen
      footer={
        groups.length > 0 ? (
          <View style={{ padding: 16, paddingTop: 4 }}>
            <Button testID="btn-new-group" label="Nuevo grupo" icon="plus" onPress={() => r.push('/group/new')} />
          </View>
        ) : null
      }
    >
      <TopBar title="Cuadra" subtitle="Gastos compartidos, cuentas claras" />
      {!hydrated ? null : groups.length === 0 ? (
        <Empty icon="users" title="Aún no tienes grupos" text="Crea un grupo con tus compañeros de cuarto, de viaje o de salida y anota los gastos. Cuadra calcula quién le debe a quién.">
          <Button testID="btn-new-group" label="Crear mi primer grupo" icon="plus" onPress={() => r.push('/group/new')} />
          <Button testID="btn-demo" label="Probar con datos de ejemplo" variant="soft" icon="play" onPress={() => r.push(`/group/${loadDemo()}`)} />
        </Empty>
      ) : (
        <View style={{ gap: 12 }}>
          {groups.map((g) => {
            const bal = computeBalances(g)[g.meId] ?? 0;
            return (
              <Pressable key={g.id} testID={`group-${g.id}`} onPress={() => r.push(`/group/${g.id}`)}>
                <Card style={{ flexDirection: 'row', alignItems: 'center', gap: 14 }}>
                  <View style={{ width: 52, height: 52, borderRadius: 16, backgroundColor: colors.primarySoft, alignItems: 'center', justifyContent: 'center' }}>
                    <Text style={{ fontSize: 26 }}>{g.emoji}</Text>
                  </View>
                  <View style={{ flex: 1 }}>
                    <Text style={textStyles.h2} numberOfLines={1}>{g.name}</Text>
                    <Text style={textStyles.soft}>{g.members.length} personas · {formatPEN(totalSpent(g))} en total</Text>
                    <Text style={{ fontSize: 13.5, fontWeight: '700', marginTop: 4, color: bal === 0 ? colors.inkSoft : bal > 0 ? colors.pos : colors.neg }}>
                      {bal === 0 ? 'Estás al día' : bal > 0 ? `Te deben ${formatPEN(bal)}` : `Debes ${formatPEN(-bal)}`}
                    </Text>
                  </View>
                  <Feather name="chevron-right" size={20} color={colors.inkSoft} />
                </Card>
              </Pressable>
            );
          })}
        </View>
      )}
    </Screen>
  );
}
