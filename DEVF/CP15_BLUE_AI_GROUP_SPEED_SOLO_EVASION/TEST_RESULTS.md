# CP15 — resultados verificados
| Evidencia | Estado |
|---|---|
| SOURCE_IMPLEMENTED | `9fddfd9d445ade5d1ae5b4cc6f7d8380fc99f336` |
| LAB_PASS | `cp15_lab` 38/38 (g++ local y MSVC) contra un **port de la lógica nativa**, no contra el motor; `cp14_lab` 16/16 compilado contra el runtime CP15; mutaciones de la política muertas (local) |
| WINDOWS_MSVC_PASS | run [39166668585](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39166668585), CI `ea52ba9`. 335 blobs fijados, 0 avisos C4477/C4473. Todos los labs previos con sus conteos (66/26/30/22/28/36/4/7/22/9/20, cp13 26) y el editor CP13 39/42/71/110/25 |
| INDEPENDENT_DOWNLOAD_PASS | job `independent-download` + descarga local: ZIP 1 053 866 B `2a0463d7…2083` |
| HUMAN_RUNTIME_PENDING | ver HUMAN_TEST.md |

**Entregable:**
- `BokoblinExpansion_0.12.0_CP15_TEST.dusk`: 95 511 B, SHA256 `7444fe51a1eeec8b050775e2991473db08fb3f770b3b7f3028dddbe334d7670d`. DLL `39519969…6a36f`, `CP15_PE_ABI_PASS`, 1 hook (`daE_OC_c::execute`), 6 imports de juego nuevos revisados (solo lectura).
- Requiere el Provider 0.13.0 de CP13 (`3a3c874e…7634e`). CP15 no lo reentrega.
- El provider recompilado para regresión no es byte-idéntico al de CP13 (MSVC no reproducible); fuente igual y fijada, auditoría y 19 negativos correctos.

Artefacto [12150912657](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39166668585/artifacts/12150912657), caduca el 2026-11-17 21:13:30 UTC. No hay copia permanente.
