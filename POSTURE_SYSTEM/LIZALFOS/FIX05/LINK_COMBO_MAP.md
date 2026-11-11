# Mapa de los espadazos de Link (Dusklight 2.0.3)

Fuente: `src/d/actor/d_a_alink_cut.inc` y `d_a_alink_HIO_data.inc` del SDK `40457c6`, inspección de código. Los nombres son los nativos. La columna "llegada" se calcula con `ceil((inicio AT − inicio clip) / velocidad)`.

| Corte (CUT_TYPE) | Proc | Clip | Inicio clip | Velocidad | AT frames | Cancelación | Rebote nativo | Llegada (ticks) | ¿Alcanzable en 0.12.4? |
|---|---|---|---|---|---|---|---|---|---|
| `NM_VERTICAL` | `PROC_CUT_NORMAL` | `ANM_CUT_NM_VERTICAL` | 2 | 1,2 | 5..10 | 16 | `ANM_CUT_RECOIL_A` | 3 | Sí |
| `NM_LEFT` | `PROC_CUT_NORMAL` | `ANM_CUT_NM_LEFT` | 2 | 1,2 | 7..13 | 16 | `ANM_CUT_RECOIL_A` | 5 | **No** |
| `NM_RIGHT` | `PROC_CUT_NORMAL` | `ANM_CUT_NM_RIGHT` | 3 | 1,2 | 7..12,5 | 16 | `ANM_CUT_RECOIL_A` | 4 | Justo |
| `COMBO_STAB` | `PROC_CUT_NORMAL` | `ANM_CUT_COMBO_STAB` | 3 | 1,1 | 3..10 | 17 | `ANM_CUT_RECOIL_A` | 0 | Sí |
| `NM_STAB` | `PROC_CUT_NORMAL` | `ANM_CUT_NM_STAB` | 4 | 1,1 | 3..10 | 17 | `ANM_CUT_RECOIL_B` | 0 | Sí |
| `FINISH_LEFT` (combo) | `PROC_CUT_FINISH` | `ANM_CUT_FINISH_LEFT` | 3 | 1,0 | 7..12 | 21 | `ANM_CUT_RECOIL_A` | 4 | Justo |
| `FINISH_VERTICAL` (combo) | `PROC_CUT_FINISH` | `ANM_CUT_FINISH_VERTICAL` | 1 | 1,0 | 5..11 | 17 | `ANM_CUT_RECOIL_A` | 4 | Justo |
| `FINISH_STAB` (combo) | `PROC_CUT_FINISH` | `ANM_CUT_FINISH_STAB` | 3 | 1,1 | 10..17 | 23 | `ANM_CUT_RECOIL_A` | 7 | **No** |
| `FINISH_RIGHT` (combo) | `PROC_CUT_FINISH` | `ANM_CUT_FINISH_RIGHT` | 1 | 1,1 | 8..14 | 17 | `ANM_CUT_RECOIL_A` | 7 | **No** |

"Justo": la ventana solo alcanzaba si la espada tocaba en el primer tick del AT.

## Evidencia del log humano (230009)

De la apertura de una ventana preparada a su primer contacto, en las líneas conservadas (32 casos): 5 o 6 ticks acabaron en parry, y 7, 8, 9 (13 casos), 10 y 12 acabaron en bloqueo ordinario. Las llegadas calculadas más dos ticks de latencia del motor (3→5, 4→6, 5→7, 7→9) coinciden con esos picos.

## Rutas sin rebote

`changeCutReverseProc` solo se llama desde `procCutNormal`, `procCutFinish`, `procCutJump` (con `ANM_CUT_JUMP`, que no cambia de proc) y `procCutJumpLand`. Giro, cargas, salto grande, `CUT_DOWN` y `CUT_HEAD` no tienen clip de retroceso. En esas rutas no se gasta el token ni se acredita parry.

## Entrada y encadenado

- `setComboReserb` memoriza una pulsación de B durante el corte. La transición ocurre en `checkCutCancelNextMode` pasado el frame de cancelación, ya con el AT cerrado.
- Cada corte nuevo llama a `setCutType` una vez. `lz.swing_tick` solo deduplica dos llamadas del mismo tick, y un tick no puede contener dos AT distintos.
- `COMBO_LINK event=SWING` registra `buffered=1` cuando la pulsación estaba memorizada.
