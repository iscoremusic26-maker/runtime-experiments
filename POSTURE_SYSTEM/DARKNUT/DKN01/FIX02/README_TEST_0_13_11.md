# Guía de prueba humana — LIGHT FADES TWICE 0.13.11 DKN01 FIX02 (prioridad de arriba abajo)

Estado: **HUMAN_RUNTIME_PENDING**. Instala solo este `.dusk`. Envía el `dusklight-*.log` de cada sesión.

1. **Crash (lo más importante):** pelea larga en fase 2 y 3 atacando mucho con B de frente. Esperado: el Darknut a veces alza la guardia ANTES de tu golpe (log `ADAPTIVE_GUARD`) y el juego NO se cierra. Repite lo que hacías en 0.13.10 (Shield Attack tras sus combos).
2. **Distancia al bloquear:** bloquea con el escudo combos completos en fase 1 y fase 2. Link debe retroceder un paso corto y firme, no salir despedido. Log `LINK_SLIP_CAPPED`.
3. **Levantamiento FIX02:** rompe su postura en F2, haz Mortal Draw o Shield Attack + Helm Splitter, y NO hagas Finish. A los ~6 s debe levantarse con la animación de FIX02, con la misma vida (log `GETUP_START clip=FIX02 role=GETUP`, `GETUP_DONE`). No debe pasar a fase 3.
4. Repite 3 con **Finish** en F2 (FIX02 como resurrección → fase 3) y en F3 (muerte definitiva).
5. **Parry:** intenta parry a cada golpe de cada combo (especialmente los dos cortes del doble y las estocadas seguidas). Dinos qué golpe concreto no se pudo parar.
6. **Ofensiva:** no deberían verse saltos hacia delante del Darknut ni ataques que no sean sus combos/golpes sueltos/patada/escudo/contraataque. Log esperado: 0 `UNAUTHORIZED_NATIVE_ATTACK`.
7. **Lizalfos:** pelea con varios; no debe pegarse a Link ni quedar detrás de él tras una embestida o un coletazo; mismo ritmo de combos. Prueba cerca de paredes y en desniveles.
8. Regresiones: Bokoblins, Chilfos, barra de postura, otros Darknut (Templo del Tiempo, "Darknut (Sword)").
