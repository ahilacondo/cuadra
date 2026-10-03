export const colors = {
  bg: '#F7F3EC', // sillar cálido
  card: '#FFFFFF',
  ink: '#1D2B26',
  inkSoft: '#5B6B64',
  line: '#E6E0D4',
  primary: '#1E6B52', // verde campiña
  primaryDark: '#14503D',
  primarySoft: '#DDEFE7',
  accent: '#BC3E17', // rocoto (oscurecido tras la auditoría de contraste: antes #E4572E)
  accentSoft: '#FBE3DA',
  gold: '#F2B544',
  goldSoft: '#FCF0D5',
  pos: '#1E6B52',
  neg: '#BC3E17',
};

export const radius = { sm: 10, md: 16, lg: 22, pill: 999 };
export const space = (n: number) => n * 4;

export const memberPalette = ['#1E6B52', '#BC3E17', '#3B6FB6', '#8A5CC2', '#A8650A', '#1D7A70', '#B5446E', '#5C6B73'];

export const shadow = {
  shadowColor: '#1D2B26',
  shadowOpacity: 0.07,
  shadowRadius: 12,
  shadowOffset: { width: 0, height: 4 },
  elevation: 2,
} as const;
