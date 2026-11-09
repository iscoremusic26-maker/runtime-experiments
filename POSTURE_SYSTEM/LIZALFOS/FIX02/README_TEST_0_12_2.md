# Light Fades Twice 0.12.2: prueba humana (Windows / DX12)

Estado: **HUMAN_RUNTIME_PENDING**. Sonido, chispa, animación, colisión real y FPS solo se confirman aquí.

## Instalación (juego cerrado)
1. En tu carpeta de mods, sustituye **solo** el `.dusk` de Light Fades Twice.
2. Coloca únicamente `LIGHT_FADES_TWICE_LIZALFOS_FIX02_0_12_2_PRIVATE_TEST_windows-amd64_c242770e4f15.dusk`, SHA-256 `87725c176e595b7c69e20fff5bdd4b44764d050f2cb6b248a8b8dd32092f94ad`.
3. No dejes dos versiones. Conserva los otros ocho mods. No toques partidas.

## Rollback (juego cerrado)
`.dusk` 0.12.1, SHA-256 `08b18329128041b9b4bec99d10e2736fbd942fe58d4a1b037e7b88aef4480e23`, run 42531603399.

## Primero en el log
- `LIZ_POSTURE event=INSTALL ... enabled=1 ... gains=6/12/30/5/25`
- `LINK_BREAK_DAMAGE event=INSTALL enabled=1`
- Al cerrar: `LIZ_SUMMARY part=FIX02`, `LINK_BREAK_DAMAGE event=SUMMARY`, y un SHUTDOWN limpio.

## Lista priorizada
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 1 | Encadena 1 a 3 ataques contra un Lizalfos con escudo | Link **no rebota** en un bloqueo y puede seguir atacando. El Lizalfos no pierde HP | `LIZ_DEFLECT event=SWORD_NO_REBOUND_ORDINARY_BLOCK`, `LIZ_GUARD event=BLOCK gain=+5` |
| 2 | Dos bloqueos y un tercer corte | Puede ser parry en la ventana nueva, con re-alzado visible y rebote nativo. Si llega tarde, bloqueo | `PREPARE_ROLL`, `NEW_WINDOW`, `ENEMY_PARRY link_gain=+25 liz_gain=+0` |
| 3 | Tras un parry del Lizalfos | Un contraataque corto, normal o doble, y luego P1 a P4 con normalidad. Sin parry, ningún contraataque | `LIZ_COUNTER event=COUNTER_SELECTED source=` |
| 4 | Golpéalo sin que bloquee | Primera herida: no siempre sube el escudo. Tres heridas seguidas: casi seguro prepara guardia | `WOUND_ROLL pct=45/80/100`, `ENTER source=WOUND` |
| 5 | Nueve parries limpios de P3 | 96 en el octavo, ruptura justo en el noveno. Mira HP y barra | `LIZ_PARRY`, `LIZ_BREAK` |
| 6 | Espalda y lateral con escudo alzado | Daño en la espalda; ningún +5 falso | `block_rear_rejected` en `part=FIX02` |
| 7 | Rompe al Lizalfos y remata | Decisivo +50 %, una vez; no en el golpe que cruzó 100. Caída y Finish nativos | `LIZ_BREAK_BONUS base= extra=` |
| 8 | **Link roto** contra E_DN, E_OC y otro enemigo **no rastreado** | Daño ×1,5 en los tres | `LINK_BREAK_DAMAGE event=APPLIED base= extra= name=` |
| 9 | Link roto: caída, entorno, tu propia bomba | Sin extra | `SKIP_ENVIRONMENT`, `SKIP_NOT_HOSTILE`, `SKIP_UNATTRIBUTED` |
| 10 | Sonido, chispa y barrido del parry | Un sonido por contacto; ningún golpe mudo | `LIZ_IMPACT`, tu oído |
| 11 | Muchos enemigos | FPS sin caída nueva | Tu medición |
| 12 | Cerrar el juego | SHUTDOWN limpio | Fin del log |

Haz una pasada **A** solo con Light Fades Twice y otra **B** con los ocho mods si puedes. Si algo falla, dime patrón, impacto y distancia, y pásame el log.
