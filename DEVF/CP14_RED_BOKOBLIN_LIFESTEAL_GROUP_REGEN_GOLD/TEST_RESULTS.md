# CP14 — resultados verificados
| Evidencia | Estado |
|---|---|
| SOURCE_IMPLEMENTED | `e30218bb5a07c9316ffeba083bccd08c8253a285` |
| LAB_PASS | `cp14_lab` 16/16 (local g++ y Windows MSVC); mutaciones de `red_policy.hpp` muertas (local) |
| WINDOWS_MSVC_PASS | run [39161904036](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39161904036), CI `57df068`. 297 blobs fijados; 0 avisos C4477/C4473. Todos los labs previos con sus conteos (66/26/30/22/28/36/4/7/22/9/20, cp13 26) y el editor CP13 39/42/71/110/25 |
| INDEPENDENT_DOWNLOAD_PASS | job CI `independent-download` + descarga local: ZIP 896 102 B `da7dfa7b…6e6f` |
| HUMAN_RUNTIME_PENDING | ver HUMAN_TEST.md |

**Entregable:**
- `BokoblinExpansion_0.11.0_CP14_TEST.dusk`: 87 808 B, SHA256 `c798811c77bc53b261d8a06ad9c1dcca5bb577e659e4feb6500efd5b649bb256`. DLL `c4179663…9360`, `CP14_PE_ABI_PASS`, 1 hook (`daE_OC_c::execute`), 3 imports de juego nuevos revisados.
- Requiere el Provider 0.13.0 de CP13 (`3a3c874e…7634e`). CP14 no lo reentrega.
- El provider recompilado para regresión no es byte-idéntico al de CP13 (MSVC no reproducible). La fuente es la misma y está fijada, y pasa auditoría y 19 negativos.

Artefacto [12149266383](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39161904036/artifacts/12149266383), caduca el 2026-11-17 20:10:32 UTC. No hay copia permanente.
