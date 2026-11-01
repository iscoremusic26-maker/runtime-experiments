# POST03 — Detección, clasificación y deduplicación de impactos (TEST privado): runbook

**Estado:** `HUMAN_RUNTIME_PENDING`. Compila con MSVC y supera las auditorías de CI, pero **nadie lo ha cargado en Dusklight**. `POST03_RUNTIME_PASS` solo tras tu log real.
POST03 **reemplaza** a POST02 (y a POST01): ID propio `dev.posture.post03_hit_classification`, versión `0.3.0`. Nunca cargues dos de la serie a la vez.

## Qué hace y qué no
- Hace: sobre la identidad/ciclo de vida de POST02, emite **como máximo un evento** por procesamiento real de un golpe en un Bokoblin E_OC, con veredicto (`HIT_CONFIRMED`, `FINISH_NATIVE_OBSERVED`, …) y familia de ataque solo cuando el juego mismo la determinó (ver `HIT_EVENT_CONTRACT.md`).
- No hace: ni postura, ni HUD, ni supresión, ni Finish inducido, ni escrituras en el juego, ni `setActionMode`/`offTgSph`, ni segundo hook. «Pasivo» = sin cambios deliberados; el hook cuesta algo de CPU (no se mide equivalencia).

## Artefacto
- **Enlace directo del artefacto (ZIP de GitHub con el .dusk):** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41280823158/artifacts/13073232413 (repo privado: requiere sesión con acceso).
- Comando opcional: `gh run download 41280823158 --repo iscoremusic26-maker/codex-cp00-inputs --name POST03_TEST_41280823158_1`
- El ZIP contiene `POSTURE_POST03_HIT_CLASSIFICATION_windows-amd64_f350522fc209.dusk` (**19688 bytes**), `DOWNLOAD_MANIFEST.json` y `SHA256SUMS.txt`. **Instala solo el .dusk.**
- SHA-256 del .dusk: `59c8145e6c29914ef4b602b892d35d73ba6f0946923270ab278387f992ad3c9f` (`Get-FileHash -Algorithm SHA256`; si difiere, detente). Caduca el **2026-12-01 06:27 UTC**.
- Host: Dusklight 2.0.3 (`dusklight.exe` SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`); con otra versión el mod se niega a cargar.

## Instalar / quitar (juego cerrado)
1. Cierra Dusklight del todo; respalda partidas/config como siempre.
2. **Retira** el .dusk de POST02 (y cualquier POST01) de `%APPDATA%\TwilitRealm\Dusklight\mods`.
3. Copia el .dusk de POST03. Zora Swim puede quedar si lo anotas como mod adicional.
4. Quitar: cierra el juego y borra el .dusk. No guarda nada en disco ni toca partidas.

## Fases (sin repetir lo ya establecido)
- **A — arranque.** Busca `POST03_INIT`, `POST03_TARGET` (`inline_sites_flag=0`) y `POST03_HOOK_INSTALLED`; ningún `was inlined into callers`.
- **B — impactos nativos, sin otros mods de combate.** Con un E_OC ya conocido: un golpe, espera a que venza el cooldown, repite (varias señales). Espada normal y, si el equipo está disponible y sin forzar nada, combo/ataque fuerte, flecha, bomba, bumerán, tirachinas, escudo, bola de hierro. Observa también varios impactos no letales, al menos uno letal si es viable, un E_OC2 excluido y un Finish natural si aparece. Lo que no tengas: `NOT_TESTED_OPTIONAL`.
- **C — doble esfera / reentrada.** Eventos con `tg=cc0+cc1` cuando aparezcan solos; más de un Bokoblin; sal y vuelve (ids y `generation` distintos, nada heredado).
- **D — coexistencia** (solo si B y C son estables): POST03 + HM CP11 ×2 + Bars CP06 + DEVF 0.15.0 + Expansion 0.17.0 (+ inocuos ya usados). Observa un Blue que cambie `AtAtp` (`ADMISSION_CHANGED … identity=KEPT`) y un E_OC2 excluido. Contrasta con HM **solo** eventos del mismo actor y tipo; no totales sin contexto.
- **E — cierre.** Sal por el menú; busca `POST03_SUMMARY tag=SHUTDOWN`, `POST03_HIT_SUMMARY tag=SHUTDOWN`, `POST03_CONSERVATION tag=SHUTDOWN ok=1` y `POST03_SHUTDOWN`.

## Líneas de log
| Línea | Significado |
|---|---|
| `POST03_INIT` / `POST03_TARGET` / `POST03_HOOK_INSTALLED` / `POST03_HOOK_FAILED` / `POST03_DISABLED` | carga o apagado (mod inerte) |
| `POST03_INSTANCE_FIRST_SEEN`, `…_ADMISSION_CHANGED`, `…_DEATH_SEEN`, `…_RETIRED`, `…_UNVERIFIED` | ciclo de vida, **misma semántica que POST02** (solo `LOOKUP_ABSENT_VERIFIED` tiene `delete_claim=1`) |
| `POST03_HIT_EVENT … kind= … family= … tg= …` | **un** evento por procesamiento: `HIT_CONFIRMED`, `FINISH_NATIVE_OBSERVED`, y (acotados a 30) `HIT_PROCESSED_SIGNATURE_MISMATCH`, `HIT_CANDIDATE_NOT_PROCESSED`, `FINISH_UNEXPECTED_STATE` |
| `POST03_SUMMARY` / `POST03_HIT_SUMMARY` / `POST03_CONSERVATION` | contadores: `raw_tg`, `dual_tg`, `confirmed`, `processed_mismatch`, `not_processed`, `finish`, `cooldown_blocked`, `cooldown_with_tg`, `no_tg`, `duplicates_suppressed`, `cross_generation_drops`, `classification_unavailable`, `family(…)`, etc. |
Tope duro de 2000 líneas por sesión (ciclo de vida 600, golpes 1000, otros 300, resumen 100). Ningún log por frame.

## Qué esperar (sin declarar nada por adelantado)
- Un golpe procesado debe dar **un** `HIT_CONFIRMED`; con `tg=cc0+cc1` sigue siendo uno. Los golpes dentro del cooldown no dan evento (suben `cooldown_blocked`; con DEVF puede subir `cooldown_with_tg` por su bloqueo de Helm Splitter: esperado).
- `family=` solo lo que el juego eligió; `AMBIGUOUS`, `OTHER_VERIFIED` y `UNAVAILABLE` son resultados válidos y honestos. **Los valores `at=0x…` reales son la primera medición en juego**: si una familia parece incorrecta, es un hallazgo, no un fallo del runbook.
- `POST03_CONSERVATION ok=1` y `pending=0` al cerrar.
- `CalcDivideInfo`, avisos de texturas y los `PERF_WINDOW` de Expansion (`MEASUREMENT_NOT_AN_ERROR`) ya existían sin POST03: anota la cantidad, no se atribuyen.

## Detente y retira el .dusk si
Hook parcial, `inline_sites_flag=1`, crash, caída fuerte de FPS o cambio de combate; un mismo golpe con dos `HIT_EVENT`; `tg=cc0+cc1` generando dos eventos; un golpe en cooldown etiquetado `HIT_CONFIRMED`; una familia concreta en un evento no procesado; un `id` retirado con `LOOKUP_ABSENT_VERIFIED` que vuelve a ejecutar `damage_check`; HP de HM incoherente atribuible a añadir POST03 (investigar, no culpar sin control). Conserva el log y no sigas con otras configuraciones.

## Qué enviar
Configuración exacta de mods y versiones, SHA-256 del .dusk usado, resultado por fase y el **log completo** de cada sesión (como hasta ahora). Capturas o vídeo solo para un fallo visual concreto. No hace falta confirmar rutinariamente que el combate «se ve normal».

## Decisiones pendientes (POST03 es compatible con cualquiera)
D1 Blue de DEVF (origen indeterminable) · D2 ATTACK como modo de supresión (hipótesis de POST05) · D3 no se cancela ningún BIG_DAMAGE · D4 no se tocan bumerán/escudo · D5 barra de postura sin calcular ni dibujar.
