import { useState } from 'react';
import { Pressable, Text, View } from 'react-native';
import { useRouter } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { useStore } from '@/state/store';
import { GROUP_EMOJIS } from '@/data/categories';
import { Avatar, Button, Card, Field, Screen, TopBar } from '@/ui/kit';
import { colors } from '@/ui/theme';

export default function NewGroup() {
  const r = useRouter();
  const { createGroup } = useStore();
  const [name, setName] = useState('');
  const [emoji, setEmoji] = useState('🏠');
  const [members, setMembers] = useState<string[]>(['Yo']);
  const [draft, setDraft] = useState('');
  const [tried, setTried] = useState(false);

  const nameErr = tried && name.trim().length < 2 ? 'Escribe un nombre para el grupo' : undefined;
  const memErr = tried && members.length < 2 ? 'Agrega al menos a otra persona' : undefined;

  const addMember = () => {
    const v = draft.trim();
    if (!v) return;
    if (members.some((m) => m.toLowerCase() === v.toLowerCase())) return;
    setMembers([...members, v]);
    setDraft('');
  };

  const save = () => {
    setTried(true);
    if (name.trim().length < 2 || members.length < 2) return;
    const id = createGroup(name.trim(), emoji, members);
    r.replace(`/group/${id}`);
  };

  return (
    <Screen footer={<View style={{ padding: 16, paddingTop: 4 }}><Button testID="btn-create" label="Crear grupo" icon="check" onPress={save} /></View>}>
      <TopBar title="Nuevo grupo" onBack={() => r.back()} />
      <Field testID="input-group-name" label="Nombre del grupo" placeholder="Ej. Cuarto compartido – Octubre" value={name} onChangeText={setName} error={nameErr} />

      <Text style={{ fontSize: 13, fontWeight: '700', color: colors.inkSoft, marginBottom: 8 }}>Ícono</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 18 }}>
        {GROUP_EMOJIS.map((e) => (
          <Pressable key={e} onPress={() => setEmoji(e)} style={{ width: 48, height: 48, borderRadius: 14, alignItems: 'center', justifyContent: 'center', backgroundColor: emoji === e ? colors.primarySoft : '#fff', borderWidth: 2, borderColor: emoji === e ? colors.primary : colors.line }}>
            <Text style={{ fontSize: 24 }}>{e}</Text>
          </Pressable>
        ))}
      </View>

      <Text style={{ fontSize: 13, fontWeight: '700', color: colors.inkSoft, marginBottom: 8 }}>Integrantes ({members.length})</Text>
      <Card style={{ gap: 10, marginBottom: 12 }}>
        {members.map((m, i) => (
          <View key={m} style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
            <Avatar name={m} index={i} />
            <Text style={{ flex: 1, fontSize: 16, color: colors.ink, fontWeight: '600' }}>{m}{i === 0 ? '  (tú)' : ''}</Text>
            {i > 0 ? (
              <Pressable testID={`rm-member-${i}`} onPress={() => setMembers(members.filter((x) => x !== m))} hitSlop={10}>
                <Feather name="x" size={18} color={colors.inkSoft} />
              </Pressable>
            ) : null}
          </View>
        ))}
      </Card>
      <View style={{ flexDirection: 'row', gap: 10, alignItems: 'flex-start' }}>
        <View style={{ flex: 1 }}>
          <Field testID="input-member" label="Agregar persona" placeholder="Nombre" value={draft} onChangeText={setDraft} onSubmitEditing={addMember} error={memErr} />
        </View>
        <View style={{ marginTop: 24 }}>
          <Pressable testID="btn-add-member" onPress={addMember} style={{ width: 50, height: 50, borderRadius: 25, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' }}>
            <Feather name="plus" size={22} color="#fff" />
          </Pressable>
        </View>
      </View>
    </Screen>
  );
}
