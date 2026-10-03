import type { CategoryId } from '@/core/types';

export const CATEGORIES: { id: CategoryId; label: string; icon: string; color: string }[] = [
  { id: 'alquiler', label: 'Alquiler', icon: 'home', color: '#1E6B52' },
  { id: 'servicios', label: 'Servicios', icon: 'zap', color: '#A8650A' },
  { id: 'comida', label: 'Comida', icon: 'shopping-cart', color: '#BC3E17' },
  { id: 'transporte', label: 'Transporte', icon: 'navigation', color: '#3B6FB6' },
  { id: 'salida', label: 'Salidas', icon: 'music', color: '#8A5CC2' },
  { id: 'otros', label: 'Otros', icon: 'tag', color: '#5C6B73' },
];

export const categoryOf = (id: CategoryId) => CATEGORIES.find((c) => c.id === id) ?? CATEGORIES[5];

export const GROUP_EMOJIS = ['🏠', '🎓', '✈️', '🍕', '🎉', '🛒', '⚽', '🚌'];
