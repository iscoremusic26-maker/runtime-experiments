# Prueba humana de 0.13.9 (DARKNUT MINIBOSS DKN01)

Estado: **HUMAN_RUNTIME_PENDING**. Solo tu prueba en Dusklight confirma el resultado.

## Instalación
1. Cierra Dusklight. Comprueba el SHA-256 del `.dusk` 0.13.9 (`Get-FileHash -Algorithm SHA256`).
2. Guarda el 0.13.8 y quítalo. Debe quedar **un solo** Light Fades Twice en `mods`.
3. Volver atrás: 0.13.8 `f14d9ce7…1ee0` (FULL 43488594715).

## Requisitos
- Invoca con Enemy Spawner el **"Darknut"** normal (no "Darknut (Sword)").
- Ending Blow aprendido para la ruta del Finish.
- Perfil A: solo Light Fades Twice + Enemy Spawner. Perfil B: tus 8 mods habituales. Guarda un log por perfil.

## Pruebas, por prioridad
1. **Vertical / lateral (fase 1).** Bloquea los mazazos sueltos. Log `DARKNUT_IMPACT … move=F1_A_LATERAL_0x05` / `F1_B_VERTICAL_0x06`. Dime si el que el log llama *VERTICAL* es de verdad el golpe de arriba abajo. Si están cruzados, solo hay que intercambiar la atribución.
2. **Continuidad de combos.** Espera `DARKNUT_COMBO_START combo=F1-Cx/F2-Cx`. ¿Encadena los golpes sin congelarse, sin saltos y sin giros instantáneos? ¿El ritmo se parece a tus audios? (`DARKNUT_COMBO_SWING … interval_error_ticks`).
3. **Parry por golpe.** Shield Attack (R+B) en cada impacto, también en los dos cortes de B y en las dos estocadas seguidas de F2-C2. Log `DARKNUT_PARRY` por cada uno; tu postura no sube con el parry; la del Darknut sí. Un parry no corta el combo.
4. **B1 (final de F2-C1).** Solo el primer corte, más lento; sin segundo corte, sin sonido ni golpe del segundo; vuelve a la guardia (`COMBO_END reason=B1_RECOVERY`).
5. **Barra de postura del Darknut.** Sube con parries y golpes; baja tras ~2 s; llena = tambaleo.
6. **Tambaleo.** Solo al llenar la barra. Dura ~3 s o 3 golpes tuyos (`DARKNUT_PUNISH_HIT hits=n/3`), sin repetir la animación; luego levanta la guardia y bloquea (`DARKNUT_GUARD_RECOVER`). Los golpes normales sin barra llena **no** lo hacen tambalearse.
7. **HP y armadura (fase 1).** La armadura cae poco a poco (`DARKNUT_ARMOR_PROGRESS`), nunca toda de golpe, y la transformación nativa (lanza la maza, saca la espada) solo cuando `hp1=0/420`.
8. **Fase 2.** `DARKNUT_PHASE_TRANSITION event=PHASE2_START posture=0/130 res2=480/480`. Tus golpes bajan `res2`; sin tambaleo hasta llenar la barra.
9. **Guardia de Link.** Bloquear golpes sube tu postura (no se rompe tu guardia antes de 100). La patada y el golpe de escudo empujan mucho.
10. **Pasividad.** Quédate con el escudo levantado ~1.3 s sin atacar (o ~2.5 s sin escudo) cerca y de frente: patada (F2) o golpe de escudo (F1) suelto (`DARKNUT_PASSIVE_DETECT`), y luego vuelve a su IA sin encadenar un ataque.
11. **Resurrección FIX02.** Primera derrota en fase 2: cae, Finish opcional, se levanta **una vez** con la animación nueva (`DKR01 event=RESURRECTION_START`, `DARKNUT_THRESHOLD event=REVIVE_RESET … res2=480/480 posture=0/130`). Segunda derrota: muerte nativa definitiva (`DARKNUT_SECOND_DEATH`).
12. **FPS y otros enemigos.** Sin bajadas de FPS en los combos. Bokoblins, Lizalfos, Chilfos y el "Darknut (Sword)" como en 0.13.8.

## STOP inmediato (cierra, quita el `.dusk`, envía el log)
Crash; Darknut congelado o inmortal; tambaleo en bucle; armadura que cae entera sin motivo; Link con la guardia rota antes de 100; golpes fantasma o daño doble.

## Líneas de log útiles
`DKN01 event=INSTALL … enabled=1 hooks=1 dkr01=1`, `DARKNUT_CREATE`, `DARKNUT_*`, `DKR01 event=*`, `DKN01_SUMMARY why=SHUTDOWN`, `DKR01_SUMMARY why=SHUTDOWN`.
