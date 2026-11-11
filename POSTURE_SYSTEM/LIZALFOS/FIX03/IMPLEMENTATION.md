# Light Fades Twice FIX03 0.12.3: implementación

Base compilada 0.12.2 `c242770e4f155e206590be978a800c461ae4ebc6`. Rama nueva partida del commit de documentos `1e88c3a`, que no cambia nada en `POSTURE_SYSTEM/POST05`. Ritmos, combos, balance, IA y velocidad del Shield Attack (×1,00) no cambian.

Estado: **HUMAN_RUNTIME_PENDING**. Nada de esto se ejecutó en el juego real.

## P0-1. Parry real en cada impacto

**Causa raíz, demostrada.** La cadena de escudo de Link se cancelaba en cada tick por una puerta exclusiva de Bokoblins. `cp04_maintenance()` hacía `if(!cp04_sim_safe()) c4.shield.cancel()`, y `cp04_sim_safe()` exige `g.layout==1`, un valor que solo se fija al golpear con espada a un E_OC. En una pelea solo contra Lizalfos valía −1 toda la sesión.

Firma exacta en los dos logs 0.12.2: `chain_buffered=0`, `rearms=0`, `dpair=0`, y `matched + gap_arms == chain_cancelled` (429+359=788 y 287+204=491): cada armado se cancelaba exactamente una vez. El laboratorio de 0.12.2 no lo vio porque no modelaba ese mantenimiento; ahora lo modela y reproduce esa misma aritmética con la puerta antigua.

**Corrección.**
- `src/cp04_adapter.inc`: la cadena se cancela solo por seguridad del mundo de Link (`cp04_world_safe`). Los combos Blue conservan su puerta.
- `src/mod.cpp` (`post08_step`): un parry que sea el primer contacto con un E_OC evalúa él mismo la comprobación pura de layout; antes acababa en `WRITER_CLOSED`.

**P3-1.** No hay impedimento técnico: el laboratorio da parry en ese impacto con entrada correcta. Tiene la preparación más corta de las aperturas (12 ticks frente a 17,6 de N y 30 de cola). En los logs, 20 de 24 contactos llegaron con Link en `ATN_ACTOR_WAIT/MOVE` (sin pulsar aún) y en los casos muestreados con Shield Attack la pulsación cayó en el mismo tick del contacto (`link_delta=0.00`), sin movimiento del escudo todavía. Esa ventana no se ensanchó: un parry exige movimiento real del clip.

**Ventana alcanzable en D2.** Con D1 en el tick t, D2 llega hacia t+11; una pulsación nueva entre t+1 y t+10 reinicia el clip nativo desde `GUARD_SLIP` dentro del hueco entre ventanas.

## P0-2. Escudo, cuerpo y orientación

**Causa raíz.** El código decidía "frente" por la orientación del cuerpo (±67,5°), pero el motor bloquea con la esfera real `tate_sph`, colocada en el brazo izquierdo (`JNT_ARML2*(50,0,30)`). Además la guardia nativa no gira nunca. Con el Lizalfos de costado, el escudo recibía el golpe y a la vez el cuerpo perdía HP (`block_rear_rejected` = 30 y 17 en los dos logs).

**Corrección** (`src/liz_core.hpp`, `src/liz_adapter.inc`).
- Cubre si el centro real del escudo está al menos 10 unidades hacia Link desde el centro del cuerpo, y nunca más allá de ±112,5° del cuerpo.
- Un único veredicto por pase de colisión, reutilizado por el crédito (+5) y por el arbitraje escudo/cuerpo.
- La invulnerabilidad preventiva del cuerpo exige escudo presentado **y** orientado; sigue siendo posible herir por el lado descubierto o la espalda.
- La guardia gira con la ley nativa de `e_dn_fight_run`: `cLib_addCalcAngleS2(cur, search, 2, 0x800)`.
- Nueva telemetría `LIZ_SHIELD event=CONTACT` con la geometría real de cada contacto, porque la pose BCK no se puede leer fuera del juego.

## P1-3. Chispa original naranja y choque más agudo

**Ruta nativa, verificada en el EXE.** `SetAtTgGObjInf` → `ProcAtTgHitmark` → `dComIfGp_setHitMark` → `dPa_control_c::setHitMark` → dos `dPa_control_c::set` (`ID_ZI_J_HITNG_A/B`). El sonido: `setGuardSe` o `def_se_set` → `Z2SoundObjBase::startCollisionSE`, que devuelve el handle de esa reproducción.

**Decisión en el mismo pase.** La chispa nace y se calcula antes del veredicto del tick siguiente, así que el adaptador decide dentro del pase con los mismos jueces puros (`hit_input`, `judge_hit`, `contact_is_parry`) y las previsualizaciones `const` `LinkTrack::peek` / `Chain::peek_permits`. El veredicto del tick siguiente confirma o revierte; una discrepancia se cuenta (`reverted`).

**Solo cambia el color** (`src/parry_fx_core.hpp`, `src/parry_fx_adapter.inc`). Reemplazo de tono HSV a 28° conservando S, V y alfa, idempotente, en los campos `mPrmClr/mEnvClr` de esas instancias. `executeAfter` recolorea el emisor y el callback `draw` las partículas, porque `calc_p` corre después de `executeAfter` y puede reescribirlas. Ningún `JPAResource` se escribe. El callback nativo previo sigue encadenado.

**Tono.** `movePitch(×1,12, 0)` sobre el handle de esa reproducción; mismo sample.

**Riesgos declarados.**
- Si la textura de `HITNG` llevara el azul en sus píxeles (y no en `prm/env`), el cambio de color sería parcial. No se leyó el recurso. `PARRY_FX` registra los ID; el resultado visual es `HUMAN_RUNTIME_PENDING`.
- Partículas hijas dibujadas antes que las padres podrían mostrar un fotograma sin recolorear.
- La vista previa de E_OC no reproduce todas las condiciones de su commit; si este falla, se revierte y se cuenta, pero ese primer fotograma ya fue naranja.
- `dKy_SordFlush_set` (destello de iluminación del impacto) no es la chispa y no se toca.

## P1-4. Fijación estilo Sekiro

`src/lockon_core.hpp`, `src/lockon_adapter.inc`. Opción real `sekiro_lockon` en `ConfigService` (clave `mod.<id>.sekiro_lockon` de `config.json`, valor inicial **activado**), con un toggle ligado en el panel propio del mod: **Fijación de objetivos estilo Sekiro**.

- Actúa sobre el L lógico (`mHoldLockL/mTrigLockL`), sea cual sea el botón físico asignado. No toca R ni R+B. No se leyó la configuración de mandos del usuario.
- Un toque fija a un enemigo y la fijación sobrevive a la suelta; una segunda pulsación suelta y se oculta hasta soltar para que no vuelva a fijar.
- Stick derecho: un cambio por gesto (0,70 para disparar, 0,30 para rearmar), elige el enemigo más cercano en ese lado de la pantalla entre los candidatos nativos.
- HOLD y SWITCH nativos soportados. Con SWITCH, la segunda pulsación suelta en vez de ciclar.
- Con OFF, menús, pausa, eventos, muerte, lobo o caballo no se escribe nada. Entrar en un menú suelta la fijación.
- Sin `ConfigService` la función no existe y queda la fijación nativa.

## Propiedad de escrituras nuevas

| Escritor | Qué escribe |
|---|---|
| `lockon_native_pad` | L lógico y stick derecho de PAD_1, solo ese fotograma |
| `lockon_native_attention` | `mAttnStatus`, `mLockOnOffset`, `mLockTargetID`, `field_0x32e` |
| `pfx_native_colors` | `mPrmClr/mEnvClr` de las instancias capturadas y sus partículas |
| `pfx_native_callback` | `mpEmtrCallBack` de esas instancias, encadenado y restaurado al cerrar |
| `pfx_native_pitch` | `movePitch` de esa reproducción |

Offsets confirmados en el EXE 2.0.3 y fijados con `static_assert`; alcance binario en `ci/lft03_pe_audit.py`.

Hooks nuevos: `dCcS::ProcAtTgHitmark`, `dPa_control_c::setHitMark`, `dPa_control_c::set`, `Z2SoundObjBase::startCollisionSE`, `def_se_set`; más un PRE en `setGuardSe`. Los cuatro primeros son solo observados, nunca llamados. `startCollisionSE` se engancha por nombre de símbolo porque MSVC no puede inicializar como constante un puntero a miembro de una clase con herencia múltiple. El callback vive en almacenamiento estático y nunca se destruye, para que un emisor no quede apuntando a un objeto destruido.

## Límites

- Los laboratorios ejecutan los adaptadores de producción sobre stubs y rutas transcritas; no son el juego.
- La pose real del escudo no se ha leído: el laboratorio la modela con dos posiciones del brazo.
- Matriz A/B con los ocho mods y p50/p95/p99 quedan para la prueba humana.
- No se aseguran cero bugs.
