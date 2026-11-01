# POST02 — Identidad por instancia y ciclo de vida (TEST privado): runbook de prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. Compila con MSVC y supera las auditorías de CI, pero **nadie lo ha cargado en Dusklight**. `LIFECYCLE_RUNTIME_PASS` solo tras tu log real.
POST02 **reemplaza** a POST01: no cargues los dos a la vez (ID propio `dev.posture.post02_instance_lifecycle`, versión `0.2.0`).

## Qué hace y qué no hace
- Hace: sigue cada Bokoblin (`daE_OC_c`) que ejecuta `damage_check` con una clave `id + generación` y registra su ciclo de vida: primera vez visto, muerte vista, retirada. Mantiene los registros de golpes de POST01 con `generation` y `life`.
- Consulta la existencia de los IDs ya vistos con `fopAcM_SearchByID` (solo lectura), **solo en `mod_update`**, 2 consultas cada 10 ticks.
- No hace: ni postura, ni HUD, ni supresión de reacciones, ni Finish, ni escrituras en el juego, ni `setActionMode`/`offTgSph`, ni segundo hook.
- «Pasivo» = sin cambios deliberados. El hook y las consultas cuestan algo de CPU; no se promete equivalencia exacta de tiempos.

## Artefacto
- **Enlace directo del artefacto (ZIP de GitHub que contiene el .dusk):** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41277388694/artifacts/13071996061 (repo privado: requiere sesión con acceso).
- Comando opcional: `gh run download 41277388694 --repo iscoremusic26-maker/codex-cp00-inputs --name POST02_TEST_41277388694_1`
- El ZIP contiene `POSTURE_POST02_INSTANCE_LIFECYCLE_windows-amd64_3d6539010fb2.dusk` (**16883 bytes**), `DOWNLOAD_MANIFEST.json` y `SHA256SUMS.txt`. **Instala solo el .dusk**, no el ZIP.
- SHA-256 del .dusk: `addeb770324f931947023d98fc804a4aab96f34637cd4114d6a9a5f26c5fff59`. Compruébalo con `Get-FileHash -Algorithm SHA256` antes de instalar; si difiere, detente. El artefacto caduca el **2026-12-01 05:34 UTC**.
- Host esperado: Dusklight 2.0.3 (`dusklight.exe` SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`). El mod se niega a cargar con otra versión.

## Instalar / quitar (juego cerrado)
1. Cierra Dusklight por completo y respalda partidas/configuración como siempre.
2. **Retira el .dusk de POST01** de `%APPDATA%\TwilitRealm\Dusklight\mods`.
3. Copia el .dusk de POST02. Para la fase B no dejes más mods de combate; si dejas otro inocuo (p. ej. Zora Swim), anótalo exactamente.
4. Para quitar: cierra Dusklight y borra el .dusk. No guarda nada en disco ni toca partidas.

## Fases (cortas y reproducibles)
- **A — instalar y arrancar.** Verifica el SHA y en el log las líneas `POST02_INIT`, `POST02_TARGET` y `POST02_HOOK_INSTALLED`.
- **B — ciclo de vida básico.** Con un Bokoblin E_OC que ya exista (no inventes coordenadas): deja que el mod lo vea, dale varios golpes y mátalo. Espera unos segundos después de que desaparezca, o cambia de sala. Mira que aparezcan, en este orden: `FIRST_SEEN` → `HIT_OBSERVED` → `DEATH_SEEN` (**sin** retirada inmediata) → más tarde `RETIRED reason=LOOKUP_ABSENT_VERIFIED`.
- **C — reentrada.** Sal de la zona/sala y vuelve; con instancias nuevas deben salir `generation` nuevas y nada del estado anterior. Repite con varios Bokoblins sin exigir todas las armas.
- **D — coexistencia incremental (solo si B y C son estables):** HM CP11 + Bars CP06; luego DEVF 0.15.0 + Expansion 0.17.0; la combinación total solo si lo anterior fue estable. Observa al menos un Blue de DEVF (`origin=UNDETERMINED`) y un E_OC2 excluido (`adm=E_OC2_EXCLUDED`). Con HP modificado por HM o `AtAtp` temporal no debe cambiar la identidad (a lo sumo `ADMISSION_CHANGED`, `identity=KEPT`).
- **E — estrés (opcional):** recarga/cambio de sala rápido y sesiones largas. No es requisito.
- **F — cierre.** Sal por el menú y busca `POST02_SUMMARY tag=SHUTDOWN` y `POST02_SHUTDOWN`.

## Líneas de log
| Línea | Significado |
|---|---|
| `POST02_INIT` / `POST02_TARGET` / `POST02_HOOK_INSTALLED` | carga. **`inline_sites_flag=1` o el aviso `was inlined into callers` ⇒ NO aprobado** |
| `POST02_HOOK_FAILED` / `POST02_DISABLED` | fallo de instalación o apagado: el mod queda inerte |
| `POST02_INSTANCE_FIRST_SEEN id= generation= adm= origin=` | primera llamada al hook para esa vida (no es la creación real) |
| `POST02_ADMISSION_CHANGED … identity=KEPT` | cambió el criterio de admisión; la instancia sigue siendo la misma |
| `POST02_HIT_OBSERVED id= generation= life= …` | como POST01, con `generation` y `life` |
| `POST02_INSTANCE_DEATH_SEEN … (NO_DELETE_CLAIM)` | HP≤0 o modo mortal nativo; el actor sigue en el ledger |
| `POST02_INSTANCE_RETIRED reason= delete_claim=` | `LOOKUP_ABSENT_VERIFIED` (`delete_claim=1`), `ADDRESS_REUSED_BY_OTHER_ID`, `IDENTITY_CONFLICT_…`, `CONTEXT_RETIRED`, `CAPACITY_EVICTED` (`delete_claim=0` salvo el primero) |
| `POST02_INSTANCE_UNVERIFIED reason=` | consulta no concluyente: **no** es borrado. Esperable: ninguno o muy pocos |
| `POST02_INSTANCE_REVALIDATED` | una instancia no verificada volvió a verse viva |
| `POST02_CAPACITY_EXHAUSTED` / `POST02_INVALID_KEY` | tabla llena con vivos / clave inválida: avisa |
| `POST02_SUMMARY` | contadores (periódico y al salir): `records_created`, `active`, `max_active`, `death_seen`, `absent_verified`, `context_retired`, `capacity_drops`, `capacity_evictions`, `unverified`, `revalidated`, `lookups`, `lookup_unavailable`, `unmatched_post`, `post_generation_mismatch`, `log_dropped`, `log_errors` |
Hay un tope duro de 2000 líneas por sesión (con presupuesto por clase) y ningún log por frame. El instante exacto del `create` no se puede observar sin otro hook (`NOT_OBSERVABLE`): `FIRST_SEEN` lo dice con `(not SPAWN_CONFIRMED)` y no se inventan eventos.

## Qué esperar y qué NO declarar
- Que un Bokoblin muerto aparezca como `DEATH_SEEN` y **después** retirado por la consulta es lo esperado; que se retire a la vez que muere sería un fallo de diseño.
- Una retirada puede tardar varios segundos (2 consultas cada 10 ticks, repartidas entre los vivos).
- **Fallo crítico a reportar:** un `id` retirado con `LOOKUP_ABSENT_VERIFIED` que luego vuelve a ejecutar `damage_check` con el mismo `id`.
- Los avisos `CalcDivideInfo` ya existían en las tres sesiones de POST01 (incluida la de control) y son una incidencia no atribuida; anótalos si aparecen, no se atribuyen a POST02 por defecto.

## Detente y retira el .dusk si
Aviso de inline, instalación parcial, crash, cambio perceptible de combate, log excesivo o inconsistencias graves. Conserva el log y no sigas con otras configuraciones hasta diagnosticar.

## Qué enviar
Configuración exacta de mods y versiones, SHA-256 del .dusk usado, resultado por fase y el **log de sesión completo** de Dusklight (como en las pruebas anteriores). Capturas o vídeo solo si hay un fallo visual concreto.

## Decisiones pendientes (POST02 es compatible con cualquiera)
D1 Blue de DEVF (origen indeterminable) · D2 ATTACK como modo de supresión (hipótesis de POST05) · D3 no se cancela ningún BIG_DAMAGE · D4 no se tocan bumerán/escudo · D5 barra de postura sin calcular ni dibujar.
