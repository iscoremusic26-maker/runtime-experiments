# POST04 — Núcleo numérico pasivo de postura (TEST privado): runbook

**Estado:** `POST04_HUMAN_RUNTIME_PENDING`. Compila con MSVC y supera las auditorías de CI, pero **nadie lo ha cargado en Dusklight**. No existe `POST04_RUNTIME_PASS` hasta tu log real.
POST04 **reemplaza** a POST03.1, POST03, POST02 y POST01: ID propio `dev.posture.post04_numeric_observer`, versión `0.4.0`. **Nunca los cargues a la vez**: los cinco enganchan el mismo método (`daE_OC_c::damage_check`) y los IDs distintos no lo impiden.

## Qué hace y qué no
- Hace: sobre el observador de POST03.1 (identidad, un evento por golpe, familia nativa sin falsificar) lleva una **postura entera por instancia** (0–100): +25 por golpe de espada confirmado, +50 por bola de hierro, +0 para cualquier otra familia, recuperación gradual con retardo y una marca `POST04_BREAK_READY` al llegar a 100. Todo se ve **solo en el log**.
- No hace: no escribe nada en el juego; no cambia HP, IA, reacciones, sonido ni colisiones; no derriba, no provoca flinch ni Finish; no dibuja ninguna barra. `POST04_BREAK_READY` **no** produce ningún derribo. Si ves cualquiera de esas cosas, es un hallazgo de **otro** origen o un fallo: detente.
- Los valores (25/50/100/120/6) son una política de laboratorio **provisional** (`POST04_POSTURE_POLICY.md`).

## Artefacto
- **Enlace directo del artefacto (ZIP de GitHub con el .dusk):** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41320296108/artifacts/13089436064 (repo privado: requiere sesión con acceso). La API de Actions confirma que el id `13089436064` pertenece al run `41320296108` y se llama `POST04_TEST_41320296108_1`.
- Run: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41320296108 (jobs `build` e `independent-download` en éxito).
- Comando opcional: `gh run download 41320296108 --repo iscoremusic26-maker/codex-cp00-inputs --name POST04_TEST_41320296108_1`
- El ZIP (29018 bytes, SHA-256 `cc982b568f1468df27e9af4a37857b05a862530b675915e76b0613ce015b3ac3`) contiene `POSTURE_POST04_NUMERIC_OBSERVER_windows-amd64_ccf0f2d2b7b1.dusk` (**28145 bytes**), `DOWNLOAD_MANIFEST.json` y `SHA256SUMS.txt`. **Instala solo el .dusk.**
- SHA-256 del .dusk: `d43e46b37760f93090f162e3807f6b70640695dccda61870836000d1bf42f8f7` (`Get-FileHash -Algorithm SHA256`; si difiere, detente). SHA-256 de la DLL interna: `84c3fb46b7ee2e3791a7d4be6d090018c04ad0660e634c47f1ff9a26643b27d9` (58368 bytes). Caduca el **2026-12-01 15:16 UTC**.
- Compilado desde el commit fuente `ccf0f2d2b7b12092cf3407ae49bc8ba42a8ebd64` (rama `feature/posture-post04-numeric-core`), espejo de CI `9578db97647e9f60a33ad779182af4519158f78b`.
- Host: Dusklight 2.0.3 (`dusklight.exe` SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`); con otra versión el mod se niega a cargar.

## Instalar / quitar (juego cerrado)
1. Cierra Dusklight del todo; respalda partidas/config como siempre.
2. **Retira** de tu carpeta de mods el .dusk de POST03.1 (y cualquier POST03/02/01). Zora Swim puede quedar si lo anotas.
3. Copia solo el .dusk de POST04 (comprueba su SHA-256 con `Get-FileHash -Algorithm SHA256`; si difiere, detente).
4. Quitar: cierra el juego y borra el .dusk. No guarda nada en disco ni toca partidas.

## Fase A — POST04 + Zora Swim (opcional)
Objetivo: arranque limpio y la matemática con enemigos reales.
1. Arranca y busca en el log: `POST04_INIT` (`writes_to_game=0`, `game_actions=NONE`), `POST03_TARGET … resolve=MOD_OK … inline_sites_flag=0` y `POST03_HOOK_INSTALLED`. Ningún `was inlined into callers`.
2. Con Bokoblins nativos: golpea con **espada** y, si dispones de ella sin forzar nada, **bola de hierro**. Deja un Bokoblin con vida sin golpear unos **10–15 s** (≥ 300 ticks) para ver `POST04_POSTURE_REGEN`.
3. Cambia de zona/stage al menos una vez y vuelve a golpear (identidades y `generation` nuevas; nada heredado). Deja que algún Bokoblin muera con normalidad.
4. Cierra por el menú del juego.
Nota: con 40 HP un Bokoblin muere de 1–2 golpes de espada (en A1 ocurrió así), por lo que **en la fase A puede no verse acumulación ni `BREAK_READY`**: eso es esperado y no es un fallo; verás `action=SKIP reason=LETHAL` y `ZERO_WEIGHT_POLICY`. La acumulación suele verse en la fase B (HM da más HP).

## Fase B — 8/8 mods (solo si A es estable)
POST04 + HM CP11 + Enemy Health Bars CP06 + Enemy Variant Framework 0.15.0 + Bokoblin Expansion 0.17.0 + Zora Swim + Luau + Randomizer.
1. Golpes de espada y, si puedes, bola de hierro/bumerán/flecha sobre un Bokoblin con más HP. Cuatro espadazos bien separados a un actor de ~220 HP deben dar `0→25→50→75→100` y **una** línea `POST04_BREAK_READY`.
2. Un Blue (si aparece): la identidad sigue `origin=UNDETERMINED`; no se infiere nada por origen. Un `E_OC2` queda excluido (sin sidecar).
3. Comprueba que HP/HM/Bars se comportan como siempre (POST04 no los toca) y cierra por el menú.

## Líneas de log a buscar
Detalle y campos exactos: `POST04_POSTURE_EVENT_CONTRACT.md`.
| Línea | Qué esperar |
|---|---|
| `POST04_POSTURE_BIND` | una por Bokoblin E_OC admitido, `initial=0` |
| `POST04_POSTURE_HIT … action=APPLY` | solo `SWORD` (+25) e `IRON_BALL` (+50); `before+delta=after ≤ 100` |
| `… action=SKIP reason=…` | `LETHAL`, `ZERO_WEIGHT_POLICY` (BOOMERANG, OTHER_VERIFIED…), `BREAK_READY_LATCHED`, … (solo las 8 primeras por razón; el total va en el resumen) |
| `POST04_POSTURE_REGEN` | una por carrera de recuperación, no por tick |
| `POST04_BREAK_READY … game_action=NONE` | **una** por Bokoblin y ciclo; solo marca |
| `POST04_POSTURE_RETIRE` | `delete_claim=1` únicamente con `LOOKUP_ABSENT_VERIFIED` |
| `POST04_SUMMARY` / `POST04_CONSERVATION` | al cierre: `ok=1`, `underflow=overflow=generation_leak=multi_consume=0` |
Además deben seguir presentes `POST03_CONSERVATION … ok=1 pending=0`, `POST03_1_COLLIDER_DIAG` y `POST03_SHUTDOWN`. Tope duro de 2000 líneas por sesión.

## Detente y retira el .dusk si
Crash; `inline_sites_flag=1` o hook parcial; cambios visibles de HP/daño/reacción/sonido/IA/animación/Finish; barras de salud afectadas; caída fuerte de FPS; postura heredada entre generaciones; **un mismo golpe sumando dos veces** (p. ej. `tg=cc0+cc1`); `underflow/overflow/generation_leak/multi_consume ≠ 0`; `POST04_CONSERVATION ok=0`; direcciones completas o rutas en el log; cualquier escritura al juego. Conserva el log y no sigas con otras configuraciones.

## Qué enviar
Configuración exacta de mods y versiones, SHA-256 del .dusk usado, resultado por fase y el **log completo** de cada sesión, **por el chat** para análisis privado. **No subas logs íntegros a GitHub.** Después se genera la evidencia saneada con `tests/extract_post04_evidence.py` (lista blanca, comprobación de invariantes y escáner de privacidad; sin rutas, nombres de cuenta ni direcciones).

## Limitaciones conocidas de esta prueba
- La recuperación avanza con `mod_update` (tick de simulación, 1/30 s nominal a escala 1): `TIMEBASE_PAUSE_UNVERIFIED` — puede continuar con un menú abierto; si lo observas, anótalo (no es un fallo de POST04 por sí mismo).
- `CalcDivideInfo`, avisos de texturas y `PERF_WINDOW` de Expansion existían sin POST04: anota la cantidad, no se atribuyen.
- No se espera ni se mide una barra de postura, un derribo ni rendimiento. No declares fallo porque un Bokoblin de 40 HP muera antes de cuatro golpes.
- Decisiones pendientes que POST04 no resuelve: D1 Blue de DEVF, D2 ATTACK como supresión, D3 BIG_DAMAGE, D4 bumerán/escudo, D5 barra de postura.
