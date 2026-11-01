# POST03.1 — Corrección de la guarda de collider + diagnóstico (TEST privado): runbook

**Estado:** `HUMAN_RUNTIME_PENDING`. Compila con MSVC y supera auditorías de CI, pero **nadie lo ha cargado en Dusklight**. La corrección es `SOURCE_FIX_IMPLEMENTED`; `CLASSIFICATION_FIXED` solo tras tu log.
Reemplaza a POST03/02/01: ID propio `dev.posture.post03_1_collider_classification`, v0.3.1. Con otro ID que POST03, **Dusklight cargaría ambos si los dejas en la carpeta** (los duplicados solo se descartan con el mismo ID, `loader.cpp:159-163`): **retira siempre POST03 antes**.

## Artefacto
- **Enlace directo (ZIP de GitHub con el .dusk):** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41313246091/artifacts/13085797554 (repo privado: requiere sesión con acceso).
- Run: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41313246091
- Comando opcional: `gh run download 41313246091 --repo iscoremusic26-maker/codex-cp00-inputs --name POST031_TEST_41313246091_1`
- El ZIP contiene `POSTURE_POST031_COLLIDER_CLASSIFICATION_windows-amd64_cab67784e418.dusk` (**20534 bytes**), `DOWNLOAD_MANIFEST.json` y `SHA256SUMS.txt`. **Instala solo el .dusk.**
- SHA-256 del .dusk: `1f140011a20c4d28bc790af358ccb26d4247f69c3d69399ac72756475ed89cbd` (`Get-FileHash -Algorithm SHA256`; si difiere, detente). Caduca el **2026-12-01 13:52 UTC**.
- Host: Dusklight 2.0.3 (`dusklight.exe` SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`).

## Instalar / quitar (juego cerrado)
1. Cierra Dusklight del todo; respalda como siempre.
2. **Retira POST03 (y POST02/POST01)** de tu carpeta de mods (la que ya usas). Zora Swim puede quedar si lo anotas.
3. Copia el .dusk de POST03.1. Para quitarlo: cierra el juego y bórralo. No guarda nada en disco.

## Fases cortas (POST03 ya se probó A/B; no se repite)
- **A1 — combate sin mods de combate.** Arranca y comprueba `POST03_1_INIT` (con `sizeof_cCcD_Obj`/`alignof_cCcD_Obj`), `POST03_TARGET … inline_sites_flag=0` y `POST03_HOOK_INSTALLED`. Con un Bokoblin E_OC conocido: varios golpes de espada (no letales y uno letal si es viable). **Importa recargar/cambiar de stage al menos una vez** (Link se recrea y es lo que POST03 mostró que cambiaba el resultado) y volver a golpear. Salida por el menú.
- **B1 — solo si A1 es estable.** POST03.1 + HM CP11 + Bars CP06 + EVF 0.15.0 + Expansion 0.17.0 (+ los habituales). E_OC nativo y Blue (sin atribuir origen), un E_OC2 excluido, un cambio de `AtAtp` con `identity=KEPT`. No hace falta igualar los eventos de HM con los de POST03.1.
- **C — si el problema persiste:** no hacen falta sesiones largas; los diagnósticos deciden (§Cómo leerlo).
- **F — cierre normal:** `POST03_SUMMARY`, `POST03_HIT_SUMMARY`, **`POST03_1_COLLIDER_DIAG`**, `POST03_CONSERVATION ok=1 pending=0`, `POST03_SHUTDOWN`.

## Cómo leerlo (sin direcciones: son clases)
| Resultado | Significa |
|---|---|
| `deref_ok_mod8_4 > 0` y `family=SWORD` en instancias de Link donde antes salía `UNAVAILABLE` | hipótesis de alineación de 4 **confirmada**; la clasificación funciona |
| `sel_class=mod8_4` + `SELECTED_FRESH_MATCH_*` y aun así `UNAVAILABLE` (`AT_TYPE_READ_REFUSED`) | otra causa; se investiga con estos contadores |
| `reason=SELECTED_NOT_EQUAL_TO_RAW_CC0_CC1` dominante | `mpCollider` no es el hit obj crudo: **no** se clasifica; STOP_NO_SAFE_COLLIDER_CLASSIFICATION para esa clase |
| `sel_class=mod4_bad` o `too_low` | el valor no es un puntero a collider; sin lectura |
| `deref_ok_mod8_0` solamente | el fallo no era de alineación (se leyó igual que antes) |

## Criterios para cerrar la clasificación
SWORD repetible en varios impactos y, si es posible, varios Bokoblins/instancias de Link; 1 procesado ⇒ como máximo 1 evento (`cc0+cc1` = un evento); 0 anomalías, 0 `post_generation_mismatch`, `CONSERVATION ok=1`. Si la familia no puede obtenerse con seguridad queda `UNAVAILABLE` (no se fabrica SWORD). Un `CLASSIFICATION_RUNTIME_PASS` requiere esos logs.

## Detente y retira el .dusk si
Crash; caída severa de FPS atribuible; cambio de HP/modos/sonido/comportamiento; `inline_sites_flag=1` o `was inlined into callers`; `POST03_1_…` fallido o desactivado; un evento por golpe repetido o un `cc0+cc1` que genere dos eventos; **cualquier línea del log con una dirección de memoria completa**. `CalcDivideInfo`, texturas y `PERF_WINDOW` (`MEASUREMENT_NOT_AN_ERROR`) existían antes: anota la cantidad, no se atribuyen.

## Qué enviar
Configuración exacta de mods y versiones, SHA-256 del .dusk, resultado por fase y el **log completo** de cada sesión (como hasta ahora). No hace falta confirmar rutinariamente que el combate «se ve normal».

## Decisiones pendientes (compatible con cualquiera)
D1 Blue (origen indeterminable) · D2 ATTACK como modo de supresión (hipótesis de POST05) · D3 no se cancela BIG_DAMAGE · D4 no se tocan bumerán/escudo · D5 barra de postura sin calcular ni dibujar. G2/G3 `NOT_STARTED`.
