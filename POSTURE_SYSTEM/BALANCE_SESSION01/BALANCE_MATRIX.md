# Matriz numérica reproducible — 0.11.2

Medidor normalizado y saturado0..100. Orden de columnas: Sword / Parry / IronBall.

| Variante | Pesos | Contactos desde0 | Contactos desde 25 |
|---|---|---|---|
| Blue |25 /40 /50|4 /3 /2|3 /2 /2|
| Red |17 /27 /33|6 /4 /4|5 /3 /3|
| Black |13 /20 /25|8 /5 /4|6 /4 /3|
| Black Fury |13 /20 /25|8 /5* /4|6 /4* /3|

*Solo si un parry está admitido por POST08; Fury/chip sigue vetado en las condiciones anteriores. No se habilita por esta tabla.

Secuencias desde cero, sin regeneración ni otros contactos:

- Red Iron:0→33→66→99→100. **33×3=99; necesita el cuarto contacto.**
- Black Sword:0→13→26→39→52→65→78→91→100.
- Red Parry:0→27→54→81→100.
- Blue Parry:0→40→80→100.
- Black Parry:0→20→40→60→80→100.

Desde25: Blue Sword25+3×25=100; Red Sword25+5×17=110→100; Black Sword25+6×13=103→100. Parries2/3/4; Iron 2/3/3. Desde getup 0 se usa la primera tabla, sin heredar el25.

Son conteos de laboratorio con actor vivo y sin recuperación entre golpes. Saturación descarta el exceso; unidades contables=after-before. En juego, regeneración, daño letal y familias/intervalos mezclados pueden cambiar los conteos.

| Escenario de HP (contexto, no identificación) | Efecto autorizado |
|---|---|
| Blue220,2HP/s |Peso Blue; su curación no se modifica|
| Red330,3HP/s |Peso Red; lifesteal/ventana de aliados nativos de Expansion|
| Black440,4HP/s |Peso Black; furia no cambia resistencia numérica|
| Red239→322, máximo330 previamente observado |Regeneración de postura4→5; identidad Red y curación+83 intactas|
| HM x2 |No implica HP440/660/880 ni divide todo daño; sin intervención nueva|
| Helm Splitter100+50=150HP |Bonus heredado, sin convertir150HP en postura ni en IronBall|

Tasas de postura conservadas:>75/>50/>25/>10/>0%=5/4/3/2/1 puntos normalizados/s; retraso de 120 ticks elegibles a 30 Hz. No se escala la tasa por resistencia conceptual100/150/200. Política0.11.3 fuera de alcance.
