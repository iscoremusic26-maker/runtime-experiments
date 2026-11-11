# Light Fades Twice FIX05 0.12.5: implementación

Base compilada 0.12.4 `334ec89ad84d171fe8317653e19e15ffc93b8b0e`. Ritmos, combos, balance, Z-target, Shield Attack, parries de Link y Bokoblins no cambian. P3-1 no se tocó, por orden del usuario.

Estado: **HUMAN_RUNTIME_PENDING**. Nada de esto se ejecutó en el juego real.

Evidencia recortada del log humano en `EVIDENCE_LOG_0_12_4.json`. Mapas en `LINK_COMBO_MAP.md` y `SPARK_MAP.md`.

## P0. Las cadenas de B

**Causa.** La ventana de parry (edad 3..7) se abría al iniciarse el tajo, en `setCutType`. Pero cada clip tarda distinto en abrir su AT: 3 ticks el vertical, 4 el derecho, 5 el izquierdo y 7 los remates. Con la latencia del motor, la edad del primer contacto era llegada + 3: el corte izquierdo y los remates llegaban después de cerrarse la ventana.

Datos del log 230009, de la apertura de ventana al primer contacto: 5 y 6 ticks acabaron en parry; 7, 8, 9 (13 casos), 10 y 12, en bloqueo. No era azar.

**Corrección** (`src/liz_core.hpp`, `src/liz_adapter.inc`).
- El token preparado observa el tajo y re-presenta el escudo cuando faltan 2 ticks para abrirse el AT real, leyendo el clip de Link (`field_0x3478`, frame y velocidad).
- La ventana no se ensancha y el 80 % no cambia.
- Si el AT de ese corte ya cerró, el token espera al siguiente.
- Si un tajo no llega al escudo, su token vuelve mientras dure el arriendo. No hay nueva tirada.
- Desde `FIGHT_RUN`, la guardia sube solo si faltan 3..5 ticks. Con menos no puede estar arriba y el token se conserva.
- Mientras espera, la vía de presión no consume ese tajo.
- En rutas sin clip de retroceso (giro, saltos) no se gasta el token.

La reacción de Link sigue siendo la nativa: `checkCutReverseAt` devuelve TRUE y `changeCutReverseProc` hace el resto. No se escribe su estado.

## P0. Un veredicto por contacto

**Causa.** Las cinco trazas tenían `mode=6 frame=1 presented=0`. La ventana admitía edad 3, que desde `FIGHT_RUN` es el frame 1 del clip, sin exigir escudo presentado. La regla del cuerpo sí lo exigía. Por eso el rebote y el crédito decían parry y el cuerpo recibía el mismo tajo.

**Corrección.**
- Un parry exige escudo presentado.
- El veredicto se toma una vez, antes del daño de ese Execute, y lo comparten rebote, FX, cuerpo y crédito.
- Un parry exige además que el clip de Link haya hecho su comprobación de rebote.
- Si otro impacto quitó HP en ese Execute, gana el daño y no hay parry (`LIZ_CONFLICT`).
- El estado de re-armado ya no sobrevive a una guardia nueva.

Consecuencia honesta: esos parries a frame 1 eran de la vía de presión, y ahora son daño legítimo o toque sin efecto.

## P1. Choque naranja

Causa y método en `SPARK_MAP.md`. Tres escritores nativos nuevos, sin ganchos nuevos: `pfx_native_work`, `pfx_native_child_tev`, `pfx_native_flash`. Dos imports nuevos: `GXSetTevColor` y `g_env_light`.

## P1. Sonido

`kPitch` pasa de ×1,12 a ×1,22, una vez por reproducción, sobre el tono base real de esa reproducción.

## Telemetría

`COMBO_LINK` (tajo, comprobación de rebote, estado posterior), `LIZ_RESPONSE` (motivo de cada contacto), `FX_PAIR`, `PARRY_SPARK_BLUE_RISK`, `PARRY_FX event=RESOURCE`, `LIZ_SUMMARY part=FIX05` y `part=FIX05_CUTS`, `PARRY_FX_SUMMARY part=FIX05`. Presupuestos ampliados, con contadores de líneas perdidas.

## Hallado durante el trabajo

- El laboratorio de 0.12.4 no modelaba la captura de color del port, así que validaba un tinte que no llegaba a pantalla.
- Una primera lectura del índice de textura usaba una tabla que puede ser nula. Corregido antes de compilar en CI y fijado con mutante.

## CI

Ver `CI_PROFILES.md`.
