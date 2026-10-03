import React from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View, ViewStyle, TextInputProps } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { colors, radius, shadow, memberPalette } from './theme';

export function Screen({ children, scroll = true, footer }: { children: React.ReactNode; scroll?: boolean; footer?: React.ReactNode }) {
  const body = scroll ? (
    <ScrollView contentContainerStyle={s.scroll} keyboardShouldPersistTaps="handled" showsVerticalScrollIndicator={false}>
      {children}
    </ScrollView>
  ) : (
    <View style={s.scroll}>{children}</View>
  );
  return (
    <View style={s.outer}>
      <SafeAreaView style={s.inner} edges={['top', 'bottom']}>
        {body}
        {footer}
      </SafeAreaView>
    </View>
  );
}

export function TopBar({ title, subtitle, onBack, right }: { title: string; subtitle?: string; onBack?: () => void; right?: React.ReactNode }) {
  return (
    <View style={s.topbar}>
      {onBack ? (
        <Pressable onPress={onBack} style={s.iconBtn} accessibilityLabel="Volver" testID="btn-back">
          <Feather name="arrow-left" size={20} color={colors.ink} />
        </Pressable>
      ) : null}
      <View style={{ flex: 1 }}>
        <Text style={s.title} numberOfLines={1}>{title}</Text>
        {subtitle ? <Text style={s.subtitle} numberOfLines={1}>{subtitle}</Text> : null}
      </View>
      {right}
    </View>
  );
}

export function Card({ children, style }: { children: React.ReactNode; style?: ViewStyle }) {
  return <View style={[s.card, style]}>{children}</View>;
}

export function Button({ label, onPress, variant = 'primary', icon, disabled, testID }: { label: string; onPress: () => void; variant?: 'primary' | 'ghost' | 'danger' | 'soft'; icon?: keyof typeof Feather.glyphMap; disabled?: boolean; testID?: string }) {
  const bg = variant === 'primary' ? colors.primary : variant === 'danger' ? colors.accent : variant === 'soft' ? colors.primarySoft : 'transparent';
  const fg = variant === 'primary' || variant === 'danger' ? '#fff' : variant === 'soft' ? colors.primaryDark : colors.primary;
  return (
    <Pressable
      testID={testID}
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [s.btn, { backgroundColor: bg, opacity: disabled ? 0.45 : pressed ? 0.85 : 1, borderWidth: variant === 'ghost' ? 1.5 : 0, borderColor: colors.primary }]}
    >
      {icon ? <Feather name={icon} size={18} color={fg} style={{ marginRight: 8 }} /> : null}
      <Text style={[s.btnText, { color: fg }]}>{label}</Text>
    </Pressable>
  );
}

export function Avatar({ name, index, size = 36 }: { name: string; index: number; size?: number }) {
  const c = memberPalette[index % memberPalette.length];
  return (
    <View style={{ width: size, height: size, borderRadius: size / 2, backgroundColor: c, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={{ color: '#fff', fontWeight: '700', fontSize: size * 0.42 }}>{name.trim().charAt(0).toUpperCase()}</Text>
    </View>
  );
}

export function Chip({ label, selected, onPress, icon, color, testID }: { label: string; selected?: boolean; onPress?: () => void; icon?: keyof typeof Feather.glyphMap; color?: string; testID?: string }) {
  const c = color ?? colors.primary;
  return (
    <Pressable testID={testID} onPress={onPress} style={[s.chip, selected && { backgroundColor: c, borderColor: c }]}>
      {icon ? <Feather name={icon} size={14} color={selected ? '#fff' : c} style={{ marginRight: 6 }} /> : null}
      <Text style={[s.chipText, selected && { color: '#fff' }]}>{label}</Text>
    </Pressable>
  );
}

export function Segmented({ options, value, onChange }: { options: { id: string; label: string }[]; value: string; onChange: (id: string) => void }) {
  return (
    <View style={s.seg}>
      {options.map((o) => (
        <Pressable key={o.id} testID={`seg-${o.id}`} onPress={() => onChange(o.id)} style={[s.segItem, value === o.id && s.segActive]}>
          <Text style={[s.segText, value === o.id && { color: colors.ink, fontWeight: '700' }]}>{o.label}</Text>
        </Pressable>
      ))}
    </View>
  );
}

export function Field({ label, error, ...props }: TextInputProps & { label: string; error?: string }) {
  return (
    <View style={{ marginBottom: 14 }}>
      <Text style={s.label}>{label}</Text>
      <TextInput placeholderTextColor="#9AA6A0" style={[s.input, !!error && { borderColor: colors.accent }]} {...props} />
      {error ? <Text style={s.error}>{error}</Text> : null}
    </View>
  );
}

export function Empty({ icon, title, text, children }: { icon: keyof typeof Feather.glyphMap; title: string; text: string; children?: React.ReactNode }) {
  return (
    <View style={s.empty}>
      <View style={s.emptyIcon}>
        <Feather name={icon} size={30} color={colors.primary} />
      </View>
      <Text style={s.emptyTitle}>{title}</Text>
      <Text style={s.emptyText}>{text}</Text>
      <View style={{ marginTop: 16, alignSelf: 'stretch', gap: 10 }}>{children}</View>
    </View>
  );
}

export const textStyles = StyleSheet.create({
  h2: { fontSize: 17, fontWeight: '700', color: colors.ink },
  body: { fontSize: 15, color: colors.ink },
  soft: { fontSize: 13, color: colors.inkSoft },
});

const s = StyleSheet.create({
  outer: { flex: 1, backgroundColor: colors.bg, alignItems: 'center' },
  inner: { flex: 1, width: '100%', maxWidth: 560 },
  scroll: { padding: 16, paddingBottom: 32, flexGrow: 1 },
  topbar: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 14 },
  iconBtn: { width: 40, height: 40, borderRadius: 20, backgroundColor: colors.card, alignItems: 'center', justifyContent: 'center', ...shadow },
  title: { fontSize: 24, fontWeight: '800', color: colors.ink, letterSpacing: -0.4 },
  subtitle: { fontSize: 13, color: colors.inkSoft, marginTop: 1 },
  card: { backgroundColor: colors.card, borderRadius: radius.md, padding: 14, ...shadow },
  btn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 14, paddingHorizontal: 18, borderRadius: radius.pill },
  btnText: { fontSize: 15, fontWeight: '700' },
  chip: { flexDirection: 'row', alignItems: 'center', minHeight: 40, paddingVertical: 8, paddingHorizontal: 14, borderRadius: radius.pill, borderWidth: 1.5, borderColor: colors.line, backgroundColor: colors.card },
  chipText: { fontSize: 13.5, fontWeight: '600', color: colors.ink },
  seg: { flexDirection: 'row', backgroundColor: '#EAE4D8', borderRadius: radius.pill, padding: 3 },
  segItem: { flex: 1, minHeight: 40, justifyContent: 'center', paddingVertical: 9, alignItems: 'center', borderRadius: radius.pill },
  segActive: { backgroundColor: '#fff', ...shadow },
  segText: { fontSize: 13.5, color: colors.inkSoft, fontWeight: '600' },
  label: { fontSize: 13, fontWeight: '700', color: colors.inkSoft, marginBottom: 6 },
  input: { backgroundColor: '#fff', borderWidth: 1.5, borderColor: colors.line, borderRadius: radius.sm, paddingHorizontal: 14, paddingVertical: 12, fontSize: 16, color: colors.ink },
  error: { color: colors.accent, fontSize: 12.5, marginTop: 5, fontWeight: '600' },
  empty: { alignItems: 'center', paddingVertical: 36, paddingHorizontal: 12 },
  emptyIcon: { width: 68, height: 68, borderRadius: 34, backgroundColor: colors.primarySoft, alignItems: 'center', justifyContent: 'center', marginBottom: 14 },
  emptyTitle: { fontSize: 19, fontWeight: '800', color: colors.ink, textAlign: 'center' },
  emptyText: { fontSize: 14.5, color: colors.inkSoft, textAlign: 'center', marginTop: 6, lineHeight: 21 },
});
