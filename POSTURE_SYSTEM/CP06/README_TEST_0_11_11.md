# Light Fades Twice 0.11.11 — CP06 PRIVATE TEST: instalación, prueba y rollback

[Descargar artifact privado 13543119520](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42298979283/artifacts/13543119520) · [CI 42298979283](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42298979283) · caduca 2026-12-06 22:02 UTC (17:02 Panamá).

Archivo único: `LIGHT_FADES_TWICE_CP06_0_11_11_PRIVATE_TEST_windows-amd64_0ef0ad282483.dusk` · 174626 bytes · SHA-256 `7bcebf6ff442147d6741daf65d9b1e2128b524af8219296272ab64f236d15be3` (del `.dusk`, no del ZIP).

## Instalación
1. Cerrar el juego. Extraer el `.dusk` del ZIP. Sacar de la carpeta de mods **solo** el `.dusk` anterior de Light Fades Twice (guardarlo). Copiar el nuevo. Un único Light Fades Twice activo.
2. No tocar los otros siete mods (EVF 0.15.0, Bokoblin Expansion 0.17.0, Enemy Health Bars CP06 Armos TEST, Enemy Health Multiplier CP11, Zora Swim, Luau Support, Dusklight Randomizer), opciones ni partidas.

## Prueba A (aislada, opcional)
Solo este `.dusk`: arranque, Blue 2+2, R/R+B, postura/HUD. Sin Expansion no existen Red/Black de Expansion ni furia: no se valoran aquí.

## Prueba B (prioritaria, 8 mods, DX12)
1. **Blue 2+2:** los dos primeros golpes algo más rápidos y pausas más cortas; golpes 3 y 4 igual que antes. Dos parries reales seguidos en 3 y 4 (cada uno con R+B nuevo y movimiento visible del escudo).
2. **Red:** normal y Red4 = golpe, pausa, **pareja central rápida y pegada**, pausa, remate. Bloqueo/parry en los cuatro. **Especial ×2** (golpe muy rápido, sin cambio de frecuencia): intentar parry pulsando R+B **antes** del impacto; si llega tarde, el log mostrará `CP06_PARRY_TIMING`.
3. **Black normal:** Black8 = dos aislados + ráfaga de cinco + remate; Black7 = pareja rápida, dos pausas y cierre de cuatro con cadencia propia. Parry en golpes rápidos; con postura 100 el combo se corta (legítimo).
4. **Black furia:** parry con Shield Attack a tiempo debe dar postura y **no restar vida**; puede verse el destello rojo de Expansion (no controlado por este mod). La guardia normal sigue costando ¼ de corazón.
5. **R sostenido** 20–30 s ante Blue/Red/Black: deben seguir atacando, sin rebotes antes de abrir el golpe; comparar soltando R.
6. Golpes de espada con postura <100: sin tambaleo prematuro (Blue/Red/Black/furia, también en recoil y final de B/C). A 100: ruptura, castigo, Finish.
7. Varios enemigos, pausa, sala, muerte, HUD (barras sin desplazarse, prompts como antes).
8. FPS en un encuentro comparable a 0.11.10 (misma sala, resolución, enemigos y mods). `PERF_WINDOW` de Expansion mide ticks, no FPS.
9. Cerrar el juego normalmente (líneas `SHUTDOWN`, `CP06_SUMMARY`). Anotar variante, patrón, número de golpe y síntoma; no hace falta publicar el log.

## Rollback
Juego cerrado, retirar solo el `.dusk` 0.11.11 y volver a **0.11.10** (`9c8f0074962386d7f46984cab43c0cff8fb429911d731e846aa52bef44e4bb4f`, artifact 13338164623, caduca 2026-12-04). Si hiciera falta, **0.11.7** (`e446ed3ee1111837a9feed628adf939942a006e60913fe66b00d48986b71826e`). Nunca dos versiones a la vez.

No se hizo PR, merge, tag ni release. Nada de esto se ejecutó en el juego: todo lo jugable queda **HUMAN_RUNTIME_PENDING**.
