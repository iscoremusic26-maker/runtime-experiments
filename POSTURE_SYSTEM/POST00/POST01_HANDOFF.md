# POST01 — Handoff: observador pasivo de E_OC (NO AUTORIZADO TODAVÍA)

Requiere autorización expresa del usuario. **No cambia ningún comportamiento**: no hay postura, ni supresión, ni HUD, ni escrituras en el juego.

## Objetivo
Validar en Windows/DX12 el gate G1 (`ARCHITECTURE_DECISION.md` §6): el hook, la contabilidad de impactos, la admisión y el orden con otros mods.

## Contenido del mod `.dusk` (independiente, sin dependencias obligatorias de otros mods)
- `add_mod(... FEATURES game)` con el SDK de 2.0.3. Se mantiene `/Zc:inline-` para conservar `MOD_META_RECORD`, como hizo DEVF CP01 (`fe47c8b:DEVF/CP01_STAGE_BOKOBLIN_MINIMAL/SOURCE_REVIEW.md:14`).
- `DEFINE_HOOK(&daE_OC_c::damage_check, EocDamageCheck)`. Se registra primero `add_post` y luego `add_pre`, ambos con `HookAction` = `HOOK_CONTINUE` y prioridad 0.
- `static_assert` de los offsets Win64 que se lean, calculados con `offsetof` contra las cabeceras del SDK: `fopAc_ac_c::health` (el binario usa `+0x656`), `daE_OC_c::field_0x6cc` (el binario usa `+0x8ec`, **no 0x6cc**), `mActionMode`, `mOcState`, `mName`, `mFlags`. Los comentarios `/* 0x… */` de la cabecera son de la versión retail y no se usan.
- Solo lecturas: `name`, `mName` (con `strcmp`), el bit de estado `0x10000`, `mSphs_at[0].GetAtAtp()`, `field_0x560`, `health`, el modo y el estado, `field_0x6cc`, el TG de `cc[0/1]`, `mFlags`, y en el POST `mAtInfo` (tipo de AT, potencia, `mHitDirection`).
- Ledger de 32 entradas, con clave (`fpcM_GetID`, puntero, tick de primera vista).
- Log acotado: un evento por impacto aceptado (`POST01_HIT id gen mode_pre→mode_post state hp_pre→hp_post at_type power my_class admitted reason`), eventos de admisión y desalojo, y un resumen cada 600 ticks. Límite duro de 2000 líneas por sesión.

## Comprobaciones de CI (pueden dar PASS de CI, nunca de juego)
1. Compila con el workflow privado. La auditoría del PE muestra un solo objetivo de hook y los imports revisados, sin `setActionMode` ni `offTgSph` todavía.
2. Laboratorio del ledger y del clasificador con dobles falsos: E_OC, E_OC2, `atp` 2, bit ausente, reutilización de puntero con otro ID.
3. Negativo: el mod no escribe en la memoria del juego. Auditoría estática de escrituras igual a la `passivity_audit` de HM.

## Pruebas humanas (Windows/DX12, el usuario)
1. Solo Posture POST01: Bokoblin nativo en Faron u Ordon. Golpes de espada ordinarios, combo de 4, giro, salto, escudo, flecha, bumerán, tirachinas, bomba y Finish.
2. Lo mismo con HM + Bars (el par validado del 2026-10-13).
3. Lo mismo con DEVF CP21 (Blue, Red y Black), incluyendo la reentrada en una sala.
4. Pausa, cambio de sala y cierre limpio.

## Criterios de aceptación de G1
- Aparece el log de instalación sin el aviso `was inlined into callers` (`hook.cpp:433-436`).
- Cada golpe aceptado se registra **exactamente una vez**. Los golpes dentro del bloqueo `field_0x6cc` no se registran.
- El HP posterior coincide con lo que muestra Bars, con y sin HM.
- Los modos registrados siguen la tabla de T§3: DAMAGE k, BIG_DAMAGE k, DEATH.
- Los E_OC2 y los Black/Red aparecen como `admitted=0`. Se comprueba en el log qué ocurre con DEVF Blue (dato para D1).
- La jugabilidad es idéntica a no tener el mod (observación humana).

## Señales de bloqueo (detenerse y reportar)
Fallo de instalación del hook, aviso de inline, doble conteo, HP incoherente, crash, cualquier cambio de comportamiento, o un log que supere el límite.

## Rollback
Retirar el `.dusk` de la carpeta `mods` con Dusklight cerrado. El mod no guarda datos persistentes ni toca partidas.
