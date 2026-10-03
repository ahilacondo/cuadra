/** Convierte un texto ("12.5", "12,50") en céntimos enteros. Devuelve null si no es válido. */
export function parseAmount(text: string): number | null {
  const t = text.trim().replace(/\s/g, '').replace(',', '.');
  if (!/^\d+(\.\d{0,2})?$/.test(t)) return null;
  const [int, dec = ''] = t.split('.');
  return parseInt(int, 10) * 100 + parseInt((dec + '00').slice(0, 2), 10);
}

function group3(n: number): string {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/** 123450 -> "1,234.50" */
export function formatNumber(cents: number): string {
  const abs = Math.abs(Math.round(cents));
  const int = Math.floor(abs / 100);
  const dec = (abs % 100).toString().padStart(2, '0');
  return `${group3(int)}.${dec}`;
}

/** 123450 -> "S/ 1,234.50" (con signo "-" si es negativo) */
export function formatPEN(cents: number): string {
  return `${cents < 0 ? '-' : ''}S/ ${formatNumber(cents)}`;
}

export function centsToInput(cents: number): string {
  return (cents / 100).toFixed(2);
}
