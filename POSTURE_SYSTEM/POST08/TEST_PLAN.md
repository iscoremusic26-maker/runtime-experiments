# POST08 0.8.0: plan de pruebas

**Niveles de evidencia:**
- **CORE:** `tests/parry_lab.cpp`, núcleos puros con g++ y MSVC.
- **SRC/ABI:** fuente del host y EXE.
- **BIN:** DLL MSVC (auditoría PE, `static_assert` de offsets y desensamblado).
- **HUMAN:** prueba del usuario.

El laboratorio **no** puede probar el timing real, la colisión ni la vida de Link: eso queda en HUMAN.

| T | Qué | CORE | SRC/ABI/BIN | HUMAN |
|---|---|---|---|---|
| T01 | Shield Attack sin contacto | `None`, sin postura | El parry exige `AtHit` sobre un `TgCyl` de Link en la pasada | pendiente |
| T02 | Tardío (el golpe ya resuelto) | `MISSED_LATE` tras `NOT_BLOCKED`/`NORMAL_GUARD` | — | pendiente |
| T03 | Enemigo que no ataca | `None`/`NOT_ATTACKING` | — | pendiente |
| T04 | Golpe activo sin contacto real | `None` (otro objeto o sin marca) | — | pendiente |
| T05 | Desde detrás | `NOT_BLOCKED`: falla el rango frontal del escudo | `ChkShieldFrontRange` [S] | pendiente |
| T06 | Parry preciso | ventana [−1, +5] barrida cada 0,25 frames | frames de `ANM_SHIELD_ATTACK` [S+B] | pendiente |
| T07 | Grupo | solo el atacante | — | pendiente |
| T08 | Red (×2 permitido) | `CONFIRMED` | — | pendiente |
| T09 | Black normal (×1,15) | `CONFIRMED` | — | pendiente |
| T10 | Black en furia | `FURY_CHIP_POSSIBLE` (rechazado) | chip de Expansion [S] | pendiente: **sin PASS de Black en furia** |
| T11 | Dos esferas del mismo golpe | 1 confirmación, luego `DUPLICATE` | — | pendiente |
| T12 | Callbacks repetidos | `commit` idempotente | — | — |
| T13 | Dos ataques distintos | tokens distintos, también al reiniciar el clip | — | pendiente |
| T14 | Dos atacantes a la vez | independientes; nunca +80 a uno | — | pendiente |
| T15 | Identidad reciclada | sin herencia; `apply_parry` rechaza identidad caducada | — | — |
| T16 | Evento, congelado, muerto, vida ≤ 1, desactivado | rechazados | — | pendiente (salas y pausa) |
| T17 | 0 → 40 | ✔ | — | pendiente |
| T18 | 25 → 65 y 50 → 90 | ✔ (reinicia el retardo; regeneración tras 120 ticks) | — | pendiente |
| T19 | 60/65/75/90 → 100 | ✔ (cruza a 100 exacto; saturación contada) | 99 no es alcanzable con los pesos 25/50/40 (máximo sin latch: 90) | pendiente |
| T20 | Latched | rechazado, un solo cruce | — | pendiente |
| T21 | Cruce por parry | `BREAK_BY_PARRY` = aturdimiento de pie, sin bonus, caída ni Helm | — | pendiente |
| T22 | Espada decisiva después | ×1,50 | — | pendiente |
| T23 | Escudo real → Helm después | Helm sin preparación rechazado; con preparación, ×1,50 | — | pendiente |
| T24 | Sin castigo | de pie, recupera 50 | — | pendiente |
| T25 | FIX_REARM50 | rearme a 0 con salida redirigida | — | pendiente |
| T26 | Shield Attack ordinario | el escritor de desvío solo acepta PRE intacto o `DAMAGE 3` nativo; nunca BIG, daño de espada ni muerte | 0.8.0 no cambia POST05 | pendiente |
| T27 | Sin aturdimiento por debajo de 100 | solo un golpe activo (1\|2) se desvía, a estado 3 | ATTACK 3 sin `AtSet` [S] | pendiente |
| T28 | Link protegida | el parry exige `AtShieldHit` de esa esfera | sin `PlusDmg` [S]; vida de Link nunca escrita (auditoría) | pendiente (`POST08_LINK_LIFE_CHECK`) |
| T29 | Otro atacante sin desviar | conserva su resultado | — | pendiente |
| T30 | Vida del Bokoblin | un parry no es un golpe; vida igual exigida en `post08_step` | Shield Attack `AtAtp=0` [S] | pendiente (con HM ×2) |
| T31 | Pesos | espada 25, bola 50, el resto 0, parry 40 | — | — |
| T32 | HUD | destello en +40, un pulso | `hud_core` sin cambios | pendiente |
| T33 | Conservación | 40 rondas mixtas, auditoría ok; la corrupción se detecta | — | pendiente (`POST08_SUMMARY invariant_ok=1`) |
| T34 | POST05/06 | el parry no pasa por `consume` | — | pendiente |
| T35 | Fallo cerrado | token 0 o slot malo; latched sin ruptura → 50 | layout del EXE comprobado en ejecución | — |
| T36 | Reordenados | la postura deduplica por token | — | — |
| T37 | Chip | Red y Blue nunca; Black ≥ ×1,5, siempre | — | pendiente |
| T38 | Diferencial sin contacto | 500 casos: nada cambia | sin contacto, `post08_step` no escribe | pendiente |
| T39 | Logging acotado | 200 líneas | — | FPS pendiente |
| T40 | Desactivado | `None` siempre | — | — |
| T41 | Hooks compartidos | — | sin hooks nuevos; mismo `damage_check` PRE/POST; Expansion: PRE de `execute` antes, POST después [S] | pendiente |
| T42 | Link no válida o guardia normal | `LINK_INVALID` / `NORMAL_GUARD` | — | pendiente |

**Mutaciones:** 99, todas detectadas en local. El CI las ejecuta de nuevo.
