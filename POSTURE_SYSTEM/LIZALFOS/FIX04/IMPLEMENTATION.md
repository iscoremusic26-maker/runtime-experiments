# Light Fades Twice FIX04 0.12.4: implementación

Base compilada 0.12.3 `2aa4abe2e3b4c420dc67c3588e7ba8427eab9b71`. Ritmos, combos, balance, Z-target, parries de Link y velocidad del Shield Attack (×1,00) no cambian. P3-1 no se tocó, por orden del usuario.

Estado: **HUMAN_RUNTIME_PENDING**. Nada de esto se ejecutó en el juego real.

La evidencia recortada del log humano está en `EVIDENCE_LOG_0_12_3.json`.

## P0. Defensa y cobertura real

**Causa raíz, demostrada.** 0.12.3 exigía que el ancla del brazo (`JNT_ARML2*(50,0,30)`) estuviera al menos 10 unidades hacia Link. La pose sostenida del escudo no lo cumple.

Datos del log, contactos reales de espada contra `tate_sph`, por modo de guardia:

| Modo | Bloqueo | Parry | Daño al cuerpo con ese mismo tajo | Sin crédito ni daño |
|---|---|---|---|---|
| 6 (alzando) | 3 | 2 | 7 | 6 |
| 7 (sostenido) | 1 | 0 | **25** | 14 |
| 8 (bajando) | 1 | 0 | 3 | 2 |

El motor registró 64 contactos con el escudo y solo 5 se acreditaron. Consecuencia en cadena:
1. `covers()` era falso con el escudo arriba (`guard_cover_ticks=86` frente a `guard_open_ticks=1098`).
2. `on_guard_post` retiraba la inmunidad del cuerpo.
3. El mismo tajo hería al cuerpo, `on_wound()` ponía `chain_count=0`.
4. Por eso `block_pairs=0`: la cadena de dos bloqueos no podía empezar. No hacía falta tocar probabilidades.

**Segundo defecto.** El veredicto guardado en `damage_check` nunca se reutilizaba: `on_exec_post` avanza `local` antes de comparar `pass_cover_local == local`. El mismo error dejó `LIZ_SHIELD` con 0 líneas en el log.

**Corrección** (`src/liz_core.hpp`, `src/liz_adapter.inc`).
- Cobertura = escudo **presentado** por el clip + Link dentro del **arco del cuerpo** + **contacto real** del motor con `tate_sph`.
- Arco asimétrico porque el escudo va en el brazo izquierdo: +112,5° hacia el lado del escudo, −67,5° hacia el lado descubierto.
- El parry sigue siendo frontal, ±67,5°.
- Mientras sube (fotogramas 0–2) o tras bajar (últimos 5 de modo 8) no protege: el daño es real.
- Cualquier tajo nuevo devuelve la esfera del escudo (`unk_timer_2=0`), no solo los que pasan el test de puntería.
- Un veredicto por contacto. Nueva traza `LIZ_TRACE` con actor, generación, epoch, serial, tick, modo, frame, ángulos, presentado, cubre, cuerpo, escudo, veredicto, HP y postura antes y después. Máximo 400 líneas.
- `LIZ_SUMMARY part=FIX04` resume la cadena completa y los veredictos.

**Límite.** El arco es una decisión de diseño sobre la orientación del cuerpo. La pose BCK no se leyó. `LIZ_TRACE` registra la posición real de la esfera para ajustar si la prueba humana lo pide.

## P0. Dos bloqueos → parry → rebote → contraataque

No se cambió la lógica de `note_block`, `deflect`, `arm_counter` ni ninguna probabilidad. El fallo estaba aguas arriba, en la cobertura. El laboratorio recorre ahora la cadena completa desde la primera herida, con tres poses de brazo y ambos resultados del 80 %.

## P1. PARRY_FX

**Causa raíz, demostrada.** Los dos avisos son el mismo destino, PRE y POST. Con la base ASLR deducida del propio log (`setRStatus` nombrado en otro aviso), la dirección resuelve a la RVA `0x818d80`: `def_se_set`. Su prólogo es `test rcx,rcx; je short`: un salto `rel8` dentro de los 5 bytes que funchook debe reubicar. El `pf.enabled = ok` todo-o-nada apagó el módulo entero.

**Corrección** (`src/parry_fx_adapter.inc`, `src/mod.cpp`).
- `def_se_set` ya no se engancha. Su única función es llamar a `startCollisionSE`, así que el choque del Lizalfos se reconoce en `Z2SoundObjBase::startCollisionSE` POST, por dueño (`sound.mSoundObjAnime` del actor cuyo Execute corre) y map info 40.
- Verificado en el EXE: `setGuardSe`, `Z2Creature` y `Z2CreatureEnemy` terminan en esa función por salto de cola, y `setHitMark` llega a `dPa_control_c::set`.
- Fallo aislado por función: sin ganchos de decisión no se toca nada; sin chispa, el sonido sigue; sin sonido, la chispa sigue.
- Diagnóstico por gancho: `PARRY_FX event=HOOK name= kind= result= resolved= anchor_delta=`. La distancia a un símbolo exportado no cambia con ASLR y no publica punteros.
- Cada callback se cuenta (`calls=` en el resumen): instalado y ejecutado son dos hechos distintos.
- Primer contacto con un Bokoblin: la vista previa evalúa el layout en lugar de depender de un valor aún no fijado.

**Color.** Mismo tono 28°. Novedad: un color real (saturación ≥10 %) recibe al menos 75 %, para que un azul pálido no acabe en crema. Blanco y gris no cambian. `EMITTER_CAPTURED` registra los valores reales; `EMITTER_NEUTRAL_NOT_RECOLORABLE` indicaría que el azul está en la textura, que no se leyó.

**Audio.** `movePitch(×1,12, 0)` sobre esa reproducción. Revisado en fuente: `JAISoundParams::mixOutAll` combina ese valor y nada lo reescribe. `AUDIO_PITCH_READBACK_OK` lo comprueba un tick después, solo si el dueño sigue vivo. Es evidencia de ejecución, no de audibilidad.

**Hallado por ASan en el laboratorio:** el primer diseño de esa lectura conservaba un puntero entre ticks. Corregido antes de compilar en CI.

## CI

- `ci/hook_prologue_audit.py` lee el EXE fijado de la CI y comprueba los prólogos de 23 destinos exportados. Debe además señalar `def_se_set`: un escáner ciego falla. Los destinos por nombre no están en la tabla de exportación; para ellos la evidencia es que el log no muestra fallos.
- `ci/build_windows.py`: `START`/`END` por fase, `[n/total]`, porcentaje de unidades realmente terminadas por etapa (build, labs, paquete) y total, sin ETA. El denominador se verifica al final.
- Límite por proceso derivado de las duraciones medidas, con `TIMEOUT <label>` y árbol de procesos terminado. El log se conserva.

## Propiedad de escrituras

Ningún escritor nativo nuevo y ningún import nuevo. Un gancho menos.
