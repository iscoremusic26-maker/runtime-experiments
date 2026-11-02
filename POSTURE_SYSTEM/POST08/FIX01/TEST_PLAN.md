# POST08 FIX01 0.8.1: plan de pruebas

**Niveles de evidencia:**
- **SIM:** simulación temporal por fases en `tests/parry_lab.cpp` (`run_sim`): `mod_update`, `execute` de Link y del Bokoblin en ambos órdenes, y la pasada de colisión con transición nativa a `GUARD_SLIP`.
- **CORE:** núcleos puros.
- **SRC/BIN:** auditoría de fuente y desensamblado.
- **HUMAN:** prueba del usuario.

| P | Caso | Evidencia |
|---|---|---|
| P01 | Shield Attack a tiempo, Link ejecuta después del Bokoblin | SIM: `CONFIRMED` 1, daño a Link 0 |
| P02 | Ídem, Link ejecuta **antes** (pasa a `GUARD_SLIP` antes del PRE) | SIM: `CONFIRMED` 1, `transitioned≥1`. **Con la semántica de 0.8.0: `NORMAL_GUARD`, 0 candidatos** (`ROOT_CAUSE_REPRODUCED`); 0.8.0 solo funcionaba con el orden contrario |
| P03 | Guardia normal | SIM: `NORMAL_GUARD`, 0 parries, Link protegido |
| P04/P05 | Shield Attack sin golpe enemigo | SIM: sin contacto, 0 |
| P06 | Por detrás | SIM: `NOT_BLOCKED`, daño nativo conservado |
| P07 | Demasiado pronto | SIM: `MISSED_EARLY` (anticipación de 10 a 17 ticks) |
| P08 | Demasiado tarde | SIM: el golpe dañó antes; nunca se reinterpreta |
| P09 | Límites de la ventana | SIM: anticipación −6..+20 × ritmo del enemigo 1/1,15/2 × 2 órdenes → `CONFIRMED` exactamente en 0..9; CORE: `in_window` en delta 9 (sí), 9,5 (no) y tope de 12 ticks (no) |
| P10 | Instantánea caducada o ausente | SIM: `NO_PASS_SNAPSHOT`; CORE: `pass_for` ligado a tick e id |
| P11/P12/P14 | Transiciones y seriales | CORE: el rastreador abre y cierra el serial, registra el proc de salida y la duración, no hereda nada al cambiar de Link y cierra si Link desaparece |
| P13 | Dos esferas | CORE (T11), SIM: un solo parry |
| P15 | Nuevo ataque del mismo enemigo | CORE (T13) |
| P16/P31 | Dos Bokoblins en el mismo tick | CORE (T14, T29): independientes, sin cruzar tokens |
| P17/P18/P19/P32 | Fallo cerrado (Link no válida, identidad, latched, evento) | CORE (T15, T16, T20, T35, T42) |
| P20 | Black en furia | CORE (T10, T37): `FURY_CHIP_POSSIBLE` |
| P21/P22 | Ritmo de Expansion / Black normal | SIM a ×1,15 y ×2 (el tiempo se mide en Link); CORE (T09) |
| P23/P24/P25 | Postura y ruptura | CORE (T17–T21, T26, T27); `posture_core`/`break_core` sin cambios desde 0.8.0 |
| P26/P27/P28 | Espada ×1,50, Escudo → Helm, 50/0, FIX_REARM50 | CORE (T22–T25) |
| P29 | HUD | `hud_lab` (57 742 comprobaciones), `hud_core` sin cambios |
| P30 | EHB/HM | sin escrituras de vida (BIN); HUMAN |
| P33 | FPS de presentación | la ventana usa frames de Link avanzados por ticks; `fapGm_Execute` va por tick de simulación [S]; HUMAN |
| P34 | Logs | CORE: histograma; telemetría `SHIELD_ATTACK_START/END`/`EVENT`/`SUMMARY` 1-3 |
| P35 | Negativos | 112 mutaciones (incluidas `fix01_uses_now_state`, `fix01_window_uses_now`, `fix01_snapshot_any_tick`/`_any_link`, `fix01_judge_uses_now`, `fix01_observe_*`); auditoría PE + 11 negativos PE |
| P36 | Coste | todo O(1) por llamada y estático (64 episodios, 1 rastreador); topes de log |
| P37 | Paquete | descarga independiente (CI) y local por ID: SHA, `mod.json`, PE |
| P38 | Diferencial | BIN: escrituras idénticas a 0.8.0; `break`/`hud`/`posture` sin cambios; 10 labs heredados con los mismos conteos |

**HUMAN pendiente:** sensación de la ventana, al menos un `CONFIRMED` real, Link sin daño, sin mareo por debajo de 100, ruptura por parry, los 8 mods y FPS.
