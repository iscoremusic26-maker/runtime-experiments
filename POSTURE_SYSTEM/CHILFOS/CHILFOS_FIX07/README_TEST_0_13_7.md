# Prueba humana de 0.13.7 (CHILFOS FIX07)

## Instalación
1. Cierra Dusklight.
2. Comprueba el SHA-256 del `.dusk` 0.13.7.
3. Guarda una copia del 0.13.6 y quítalo. Debe quedar un solo Light Fades Twice activo.
4. Para volver atrás, restaura el 0.13.6: `88adbfd6…1567` (run 43359820492).

## Perfiles
- **A:** Light Fades Twice solo. Enemy Spawner se puede usar únicamente para invocar enemigos, y hay que indicarlo.
- **B:** tu conjunto habitual (Expansion, EVF, Enemy Spawner, HM203, barras, Zora Swim…).

## Qué probar (Chilfos y Lizalfos; cinco minutos por punto)
1. **Back Slice repetido de frente:**
   - El primero puede entrar.
   - Desde el segundo, el enemigo mantiene la guardia alzada (el Chilfos deja de lanzar combos mientras dure el spam) y los Back Slices que caen en su frente se bloquean o se hacen parry sin perder HP.
   - El parry da chispa naranja, contraataque y +25 de postura a Link, y tu animación no se corta.
   - Por la espalda real, o mientras el enemigo ataca, el golpe entra.
   - En el log: `CHILFOS_DEFENSE_FIX07 event=GUARD_HOLD`, `event=CONTACT ... verdict=BLOCK|ENEMY_PARRY ... hp_before=X hp_after=X`, y en el Lizalfos `LIZ_DEFENSE_FIX07 event=CONTACT ... guard_effective=1`.
2. **Giro normal (rápido) y giro fuerte (cargado), en ambos sentidos:**
   - **Con el enemigo descubierto y la vida llena:** nunca muere de un golpe. Con la Espada Maestra quita unos 30 (giro) o 45 (fuerte), y la postura sube +8/+10 (Chilfos) o +10/+12 (Lizalfos).
   - **Con poca vida:** el giro sí puede rematarlo.
   - **Con su guardia de frente:** 0 HP, chispa de bloqueo y más postura que un bloqueo normal.
   - En el log: `SPECIAL_SKILL event=HP_COMMITTED ... result=BOUNDED`.
3. **Mortal Draw común (sin romper la postura):**
   - Con la vida llena quita unos 50 y no lo mata.
   - Con su guardia de frente, 0 HP.
   - Con poca vida, sí lo mata (`death=HP_ZERO`, `authorized_finisher=0`).
4. **Mortal Draw de REMATE:** rompe la postura del Chilfos (100) y pulsa B delante.
   - Debe morir de una vez, con la misma animación, sonido y altura que en 0.13.6.
   - En el log: `SPECIAL_SKILL event=NATIVE_DEATH ... authorized_finisher=1 source_of_finisher_token=POSTURE_B_REQUEST`.
   - Si hay otro Chilfos cerca sin romper, el mismo Mortal Draw no lo mata.
5. **Que nada se haya roto:**
   - Jump Strike: no letal, con 280 → 245 y +8 en el Chilfos.
   - Jump Attack con parry en el aire y retroceso al aterrizar.
   - Los cuatro combos de cada enemigo, parry → contraataque → combo (65 %) y el C3 con su lanza.
   - Helm Splitter, la ruptura a 100, las muertes por HP 0 con tajos normales, el HUD y las chispas.
6. **Bokoblins (Blue/Red/Black/Fury):**
   - Un giro fuerte o un Mortal Draw no los mata de un golpe con la vida llena.
   - Limitación conocida: con muy poca vida, el especial los deja a 2 HP y el siguiente golpe los mata.

## Comparte
Las líneas filtradas `SPECIAL_SKILL`, `CHILFOS_DEFENSE_FIX07`, `LIZ_DEFENSE_FIX07`, `CHILFOS_BREAK event=NATIVE_DEATH`, y los resúmenes:
- `CHILFOS_FIX07_SUMMARY`, `LIZ_FIX07_SUMMARY`;
- `SPECIAL_SKILL_SUMMARY` (las tres familias; `defended_hp_leak` debe ser 0);
- `CHILFOS_FIX06_SUMMARY`, `LIZ_SUMMARY`.

Si puedes, añade también un vídeo del punto 1 (spam de Back Slice de frente) y del punto 4 (remate).

Estado: `HUMAN_RUNTIME_PENDING`, `VISUAL_RUNTIME_PENDING` y `PERF_RUNTIME_PENDING` hasta tu prueba.
