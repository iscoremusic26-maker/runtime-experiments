# POST07 0.7.0: implementación

| Campo | Valor |
|---|---|
| Rama fuente | `feature/posture-post07-hud` |
| Base | POST06 rework 0.6.1 `5037d3f` |
| Commit de código | `c23a69c7cf62ea30d66424ddb662949a29b5cf99` |
| Commit compilado | `f0e92c9f1d74d1b2d46447705fe1353cb3833eb8` (añade el pin PE revisado) |
| CI | run 41392661597, artefacto 13118435513 |
| Rama CI | `ci/posture-post07-hud` (desde `3860ca5`, la base CI de 0.6.1) |
| ID del mod | `dev.posture.post05_selective_reactions`, el mismo de siempre |
| Versión | `0.7.0` |
| Nombre en el menú | "Enemy Posture System PRIVATE TEST" (sin POST06) |

## 1. Arquitectura

```
                 tick de simulación (hilo del juego)                                  fotogramas de presentación
 damage_check PRE/POST (POST05/06, sin cambios) ─┐
 mod_update (POST04: regeneración)               │
 dMeter2_c::_execute POST ── ++sim_tick          │
 dMeter2_c::_draw POST (1.º tras _execute) ──────┴─> hud_sim_pass:
     · recorre g_fopAcTg_Queue SOLO LECTURA (≤4096 nodos)
     · E_OC vivo ↔ slot del ledger (Life::Active, MISMO puntero E id)
     · copia: postura/latched/dead/frozen (POST04), fase POST06 (misma identidad)
     · ancla EHB-equivalente + visibilidad (proyección, LOS, distancia)
     · post07::publish → Frame (≤16 DrawRec por valor, sin direcciones)
     · registra anclas en InterpService (opcional)
     · encola NUESTRO paquete en la lista 2D XLU solo si el HUD nativo está encolado
                                                     painter 2D ──> HudPacket::draw → hud_packet_paint:
                                                                    · lee SOLO hg.frame
                                                                    · ancla interpolada (opcional) → mDoLib_project
                                                                    · J2DOrthoGraph local → setColor/fillBox
 dMeter2_c::_delete PRE / mod_shutdown ─> hud_drop_all: limpia la tabla, olvida claves, saca el paquete de las listas
```

- **Hilo:**
  - la simulación y el pintor corren en el hilo del juego, uno detrás de otro;
  - el pintor nunca toca un actor: solo lee copias del último tick;
  - un actor borrado entre ticks no deja puntero vivo (`H19`, `H22`).
- **Patrón:** el mismo modelo de fotograma que Enemy Health Bars CP06 [S `game_bars.cpp`], reimplementado. **No hay dependencia de EHB, Expansion ni EVF.**
- **Imports nuevos del EXE (28):**
  - 24 son un subconjunto de los que ya importa el DLL publicado de EHB CP06 [B];
  - los otros 4 (`J2DGrafContext::place`, `setPort`, `setScissor` y `setup2D`) son ranuras de la vtable de `J2DGrafContext`. MSVC la emite en `mod.cpp.obj` por `/Zc:inline-` y el destructor virtual en línea [C, mapa del run 41392200339]. El mod no los llama directamente.
- **Imports nuevos del CRT:**
  - `free`: solo lo referencia el destructor con borrado de esa vtable, que nunca se invoca (objeto en la pila);
  - `sqrtf`: viene de `cXyz::abs`.
- **Auditoría PE:** fija cada import con su razón.

## 2. Lo que escribe

| Escritor | Qué toca | Novedad |
|---|---|---|
| `restore_reaction`, `write_vitality`, `helm_set_cut`, `helm_guard_duplicate` | actor y Link (auditados en POST05/POST06) | **sin cambios** |
| HUD | **ningún actor ni estado de postura**. Solo **nuestro puntero de paquete** en la lista 2D XLU del juego, mediante `dDlst_list_c::set` (en línea `set2DXlu`), y su retirada (`scrub_all`) al borrar el medidor o al apagar el mod | nuevo |

La auditoría de fuente (`ci/source_audit.py`) lo garantiza. Dentro del bloque HUD:
- no se puede llamar a ningún escritor ni a `rearm`, `step`, `commit`, `consume`, `g.rx`…;
- solo se puede leer `g.pe.px.entry`, `g.br.slot`, `g.eng.obs.ledger.slot` y `g.eng.obs.disabled`;
- no hay escrituras a través de punteros.

Además, en todo el código:
- un único recorrido de `g_fopAcTg_Queue`, dentro de `hud_sim_pass`;
- un único `queue_after_hud`;
- `scrub_all` solo dentro de `hud_drop_all`;
- el pintor no nombra actores ni el motor.

## 3. Ganchos

| Gancho | Tipo | Uso |
|---|---|---|
| `daE_OC_c::damage_check` | PRE + POST | POST03–06, sin cambios |
| `daE_OC_c::executeDamage` | POST | POST06, sin cambios |
| `dMeter2_c::_execute` | POST | contador de ticks del HUD |
| `dMeter2_c::_draw` | POST | muestreo y encolado |
| `dMeter2_c::_delete` | PRE | siempre `HOOK_CONTINUE`; limpieza |

- Si falla un gancho del HUD, **el sistema de postura sigue intacto** y el HUD queda inerte (`POST07_INIT hud=OFF_HOOK_FAILED`).
- `InterpService` es un **import opcional**. Sin él, la barra sigue el ancla de simulación.

## 4. FIX_REARM50 (auditoría del ID 161)

**Log real de 0.6.1** (`dusklight-20261101-231855`, leído con permiso, copia temporal borrada) [R]:

- **ID 161 (Blue, E_OC, Expansion posible):**
  - `DOWN_FINISH>GETTING_UP age=118`;
  - después `GETTING_UP>TRACKING why=TECHNICAL_ABORT_ON_FEET_50 age=167 hp=179>179 rearm=50`.
- **ID 163 (Red, E_OC2):**
  - `age=96`;
  - después `REARM_AFTER_NATIVE_GET_UP_0 age=145`.
- **Mismo levantamiento:** los dos tardaron **49 ticks**, la duración nativa completa. Ningún golpe sobre el 161 en ese intervalo; su vida solo cambia por la regeneración de Expansion.
- **Qué hizo Expansion con el 161:**
  - `BLUE_COMBAT_RESET … native_mode=6 native_state=6`;
  - `BLUE_LINK_DETECTED … native_mode=3 native_state=5`: la salida nativa FIND 5 **sí ocurrió**;
  - `BLUE_CALL_ISSUED`;
  - `BLUE_SHOUT_REQUESTED_NATIVE_WATCH3`: su `execute` PRE llama a `setActionMode(Watch,3)` [S Expansion `mod.cpp:1049`] **antes** de que `damage_check` lo observe.
- **Conclusión:**
  - es el **caso (i)**: un BIG5 → BIG6 real y completo que sale vivo;
  - la regla `mode==3&&state==5` no veía la salida porque otro hook la redirigía en el mismo tick;
  - no es una interrupción legítima (ii) ni una observación defectuosa (iii).

**Cambio mínimo** en `break_core.hpp`:

```
GETTING_UP && !hit && hp>0 && drop_mode_safe(mode) && !(mode==3&&state==5)  ->  Rearm 0  (why=REARM_AFTER_NATIVE_GET_UP_REDIRECTED_0)
```

**Sin cambios:**
- **Golpe en esa misma llamada:** sigue en 50, el comportamiento conservador anterior.
- **Interrupción en DOWN_FINISH** (sin estado 6 observado): sigue en 50.
- **Muerte, agua o caída mortal:** DEAD.
- **Modos de guion:** esperan.
- **Mecánicas:** x1.50, Shield → Helm, timeout 50, sub-100, velocidades de Expansion y Finish/Down nativos.

**Diagnóstico:** `POST06_EVENT` añade `mode= state= hit=` y `POST06_SUMMARY` añade `rearms0_redirected=`.

**Laboratorio:** `break_lab` (reproduce el ID 161, 108 combinaciones de modo, estado y golpe, y casos límite) y 4 mutaciones.

## 5. Archivos

- `src/hud_core.hpp` (nuevo, puro):
  - geometría, color, `build()`;
  - máquina de estados por slot;
  - selección de los más cercanos;
  - ancla y visibilidad;
  - plantillas de la lista de dibujo;
  - mapeo de colores de J2D.
- `src/mod.cpp`: bloque `POST07` (ganchos, pase de simulación, paquete, limpieza, resumen `POST07_HUD_SUMMARY`) e inicialización `POST07_INIT`.
- `src/break_core.hpp`: FIX_REARM50 y campos de log.
- `src/lifecycle_core.hpp`: `kModVersion` 0.7.0.
- `tests/hud_lab.cpp`: H01–H28 y `--render`.
- `tests/break_lab.cpp`: FIX_REARM50.
- `tests/run_mutations.py`: 64 mutaciones (21 heredadas, 4 de rearme, 23 del HUD y 16 de auditoría).
- `ci/*`: auditorías, rama CI, nombre del paquete, renders de referencia como evidencia del CI.

## 6. Límites conocidos

- **Captura humana:** sin ella no hay `PIXEL_ALIGNMENT_PASS`. La alineación con EHB es `LAYOUT_PARTIAL`, idéntica por construcción a sus reglas publicadas.
- **Nodos del actor:** la barra se ancla con la misma regla que EHB, no con nodos del modelo.
- **Más de 16 barras visibles:** se pintan las 16 más cercanas.
- **Pausa:** el HUD se congela. La regeneración de POST04 sigue su propio reloj, sin cambios.
