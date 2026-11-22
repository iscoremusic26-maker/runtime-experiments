# Prueba humana — LIGHT FADES TWICE 0.13.16 DKN01 FIX07

Estado: HUMAN_RUNTIME_PENDING. Windows DX12. Un solo `.dusk` de Light Fades Twice activo.

## Preparación
- **Sesión A (aislada):** solo `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX07_0_13_16_PRIVATE_TEST_windows-amd64_<sha12>.dusk`; retira las versiones anteriores de LFT y el resto de mods para esta sesión. Darknut normal por tu método habitual (Enemy Spawner), sin tocar partidas ni instalación.
- **Sesión B (habitual):** si A va bien, tu configuración de mods de siempre, con FIX07 como único LFT.
- Rollback inmediato: el `.dusk` 0.13.15 (ver MANIFEST). Al terminar cada sesión guarda el log completo de `%APPDATA%\TwilitRealm\Dusklight\logs` sin sobrescribirlo y envíalo con su nombre.

## Checklist (en este orden)
1. **F1-C3** (el combo de cuatro cortes de F1 con pausas largas): las pausas deben ser claramente más cortas (≈0,8 / 1,9 / 1,9 / 1,3 s). Los otros tres combos F1, los de F2/F3 y los counters deben sentirse igual que en 0.13.15.
2. **Ejecuciones F1:** en rupturas distintas, Mortal Draw y Shield Attack → Helm Splitter. Cada una quita 120 HP en total (log `F1_EXECUTION_CONTACT ... effective_damage=`), la armadura cae por progreso. Con menos de 120 HP restantes debe empezar la transformación.
3. **Maza lanzada (F1 → F2):** en transformaciones distintas, (a) bloquéala con el escudo: +50 postura de Link; (b) déjate dar: +60 postura y el daño de vida normal; (c) parry: chispa naranja + choque agudo, sin daño; (d) esquívala: nada. Un solo efecto por lanzamiento (log `MACE_CONTACT`).
4. **Salto ofensivo F2/F3:** aléjate (≈ 5-8 m) de frente en terreno llano. Casi siempre (90 %) debe saltar hacia ti y encadenar directamente un combo; a veces (10 %) acercarse andando. Intenta cortarlo con B, escudo, rodada o salto: no debe cortarse; tú sí puedes bloquear o hacer parry al combo. Repite junto a un borde, una pared o agua: no debe saltar (`LEAP_REFUSED_GEOMETRY`). En F1 no salta (`LEAP_F1_NOT_AVAILABLE`).
5. **Esquivas de Link (i-frames):** contra Darknut, Lizalfos, Chilfos o Bokoblin, esquiva en el momento del golpe: rodada adelante (0,30 s), salto lateral (0,20 s), salto atrás (0,20 s). Un golpe que te atraviesa dentro de esa ventana no debe hacer daño ni postura (log `LDG01 event=CONTACT result=EVADED`). La rodada adelante NO protege contra la estocada del Darknut. Fuera de la ventana, o esquivando sin enemigo cerca y sin fijar, el daño es normal.
6. **Tras resucitar y tras levantarse:** Link muy cerca (salta atrás si hay suelo detrás), a media distancia (se queda), lejos (salta adelante si es seguro). Primero se gira hacia ti; nunca ataca al aterrizar.
7. **Muerte definitiva en F3** (Finish o resistencia agotada): la espada se oscurece a la vez y al mismo ritmo que el cuerpo. En caídas recuperables, F2, el clip de resurrección y al levantarse NO debe oscurecerse; otro Darknut no se ve afectado.
8. **Chispas, destello y sonido:** parries en ambos sentidos (golpes de escudo, patadas, los dos cortes del doble, estocadas, la maza): chispa naranja en el contacto, destello cálido en ESE contacto y choque agudo. Comprueba de pasada otros enemigos, LGC01 (R / R+B) y la estabilidad.

## Comparación A/B
- A: sin otros mods, comprueba cada punto. B: repite 1, 4, 5 y 8 con tus mods habituales; si algo difiere entre A y B, anótalo (otro mod puede tocar el mismo efecto o colisión).
- Si algo va peor que en 0.13.15, vuelve al `.dusk` 0.13.15 y repite ese punto para comparar.

## Qué contarnos
Espada oscura sí/no; ritmo F1-C3; frecuencia y justicia del salto + combo; si alguna esquiva bien medida te dañó o alguna mal medida te salvó; maza (postura); chispa, destello o sonido que falte (cuándo y en qué ataque).
