# POST01 — Observador pasivo (TEST privado): runbook de prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. El .dusk compila con MSVC y supera auditorías de CI, pero **nadie lo ha cargado en Dusklight**. G1 = `INSTRUMENTED_PENDING_RUNTIME`.

## Qué hace y qué no hace
- Hace: engancha UNA función, `daE_OC_c::damage_check` (PRE que siempre continúa + POST). Lee el estado del Bokoblin antes y después y escribe líneas `POST01_*` en el log de Dusklight.
- No hace: ni postura, ni HUD, ni supresión de reacciones, ni escrituras en el juego, ni `setActionMode`/`offTgSph`, ni `HOOK_SKIP_ORIGINAL`.
- «Pasivo» significa sin cambios deliberados de gameplay o datos. El hook añade algo de CPU: no se promete equivalencia exacta de tiempos antes de tu prueba.

## Artefacto
- Descarga (repo privado, ejecución CI **41274486531**, expira 2026-12-01):
  `gh run download 41274486531 --repo iscoremusic26-maker/codex-cp00-inputs --name POST01_TEST_41274486531_1`
- Archivo: `POSTURE_POST01_PASSIVE_OBSERVER_windows-amd64_ba7b7ac262ba.dusk`
- SHA-256: `adfe9f1884a7bb05fa4607b6814da48b670bc73be4060cbaf7df7eaac3ec9766` (12693 bytes). Compruébalo con `Get-FileHash -Algorithm SHA256` antes de instalar. Si difiere, detente.
- Host esperado: Dusklight 2.0.3, `dusklight.exe` SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`. El mod se niega a cargar con otra versión (`POST01_HOOK_FAILED stage=HOST_CHECK`).

## Instalar / quitar (juego cerrado)
1. Cierra Dusklight por completo. Respalda partidas y configuración como siempre.
2. Copia **solo este .dusk** a `%APPDATA%\TwilitRealm\Dusklight\mods`. Para la Fase B no debe haber más mods de combate activos.
3. Para quitar: cierra Dusklight y borra ese .dusk. No guarda nada en disco ni toca partidas.

## Fases
- **A — control (sin POST01):** un Bokoblin normal; anota sensación de combate, sonido, daño, reacciones, muerte y estabilidad. Anota los mods activos y sus versiones.
- **B — POST01 solo:** mismo tipo de enemigo. Arranca, golpea con la espada con pausas entre golpes, haz un combo si puedes, deja morir al Bokoblin, cambia de sala y sal por el menú. Confirma que el juego se comporta igual que en A.
- **C — coexistencia (solo si B es estable):** POST01 + HM/Bars (el par validado del 2026-10-13); luego POST01 + DEVF/Bokoblin Expansion; la combinación total solo si lo anterior fue estable. Un Blue de DEVF saldrá como `origin=UNDETERMINED`: es lo esperado.
- **D — opcional (SKIPPED si falta equipo o técnica):** escudo, giro, flecha, bomba, tirachinas, bumerán, salto, Finish.

## Líneas de log que buscar (por identificador)
| Línea | Significado |
|---|---|
| `POST01_INIT` | versión, `source_commit`, `host_build_id`; `at_type=OMITTED_NO_SAFE_ACTOR_GUARD` |
| `POST01_TARGET` | símbolo resuelto. **`inline_sites_flag=1` ⇒ G1 NO_APROBADO** |
| `POST01_HOOK_INSTALLED` | PRE y POST registrados |
| `POST01_HOOK_FAILED` / `POST01_DISABLED` | fallo de instalación o apagado: el mod queda inerte |
| `POST01_ACTOR_SEEN` | una vez por instancia: `adm=E_OC_CANDIDATE`, `E_OC2_EXCLUDED`, `UNKNOWN_UNSAFE`; `origin=UNDETERMINED` en candidatos |
| `POST01_HIT_OBSERVED` | un evento por llamada con TG: `tg`, `hp a>b`, `mode`, `state`, `cd` (cooldown), `verdict` |
| `POST01_ANOMALY` | cambio de estado sin TG ni Finish: pégalo en tu informe |
| `POST01_SUMMARY` | contadores (periódico y al salir) |
También busca en el log del host el aviso `was inlined into callers`.

## Qué esperar (sin declarar nada por adelantado)
- Con Bokoblin E_OC: un `HIT_OBSERVED` por golpe que entra en `damage_check`. `verdict=ACCEPTED_LIKELY` significa que el cooldown se puso (solo `damage_check` lo escribe) y cambió HP, modo o estado. No es una aceptación confirmada: `ACCEPTED_CONFIRMED` no se emite en POST01.
- Golpes dentro del bloqueo de 10/20 ticks no generan línea (se cuentan en el resumen).
- Un golpe con HP alterado por HM sigue siendo `ACCEPTED_LIKELY`; los valores absolutos de HP no se interpretan.
- No se promete «cada golpe se cuenta una vez» sobre todos los casos: solo se exige que lo observado sea consistente y sin dobles conteos evidentes. La deduplicación exhaustiva es de POST03.

## Detente y retira el .dusk si
Aviso de inline, instalación parcial, crash, cambio perceptible de combate, log excesivo (el tope duro es de 2000 líneas) o inconsistencias graves. Conserva el log y no sigas con otras configuraciones hasta diagnosticar.

## Qué enviar
Configuración exacta de mods y versiones, SHA-256 del .dusk usado, resultado observado por fase, el **log de sesión completo** de Dusklight (los archivos `dusklight-AAAAMMDD-HHMMSS.log` de pruebas anteriores; la carpeta no está verificada aquí, dime si no la localizas) y cualquier error. Capturas o vídeo solo si hay un fallo visual concreto.

## DECISIONES PENDIENTES (no resueltas; POST01 es compatible con cualquiera)
- **D1** DEVF Blue (recurso E_OC con la misma firma que el nativo): sin señal fiable de origen. Política posterior pendiente.
- **D2** ATTACK como modo de supresión: hipótesis para POST05, no un hecho.
- **D3** No se cancela ningún BIG_DAMAGE nativo. Diseño posterior.
- **D4** Bumerán, escudo y demás efectos utilitarios no se tocan.
- **D5** Barra de postura (debajo de la vida, desde el centro hacia ambos lados): sin cálculo ni dibujo todavía.
