# Cuadra — dividir gastos compartidos (React Native + Expo)

Proyecto del Laboratorio 04 de *Plataformas Emergentes* (UNSA, 2026B).
Problema elegido mediante AHP: repartir gastos entre compañeros y saber quién le debe a quién.

## Qué incluye
- Reparto igual, por porcentaje, por montos y por partes (dinero en céntimos enteros, método del mayor resto).
- Saldos por persona y liquidación con el mínimo de transferencias (voraz + búsqueda exacta para k ≤ 16).
- Persistencia local (AsyncStorage), resumen por categoría, datos de ejemplo.

## Ejecutar
```bash
npm install
npx expo start --web        # desarrollo
npx expo export --platform web
npm test                    # Vitest (núcleo de dominio)
```
`docs/` contiene los scripts de análisis (AHP, simulación Monte Carlo, wireframes), diagramas y capturas.
Solo se verificó la versión web; no se compiló para Android/iOS.
