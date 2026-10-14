# CP03 v0.3.1 — diagnóstico privado de HP

**SOURCE_VERIFIED · BUILD_PASS · PACKAGE_VERIFIED · DOWNLOAD_VERIFIED · HUMAN_RUNTIME_NOT_TESTED.** Listo para prueba humana Windows x64/DX12; no es CP03_DIAGNOSTIC_PASS_RUNTIME ni estable. No CP04/CP06.

La versión v0.3.0 y sus refs/artefacto se conservan intactos. El usuario reportó HP_APPLIED 220→150 para ActorId 147/581/784, combate/muerte normales y respawn; esos antecedentes se guardan como USER_REPORTED, sin medición por impacto ni logs personales nuevos. Base de recuperación: `76c53b6bcc61228df3b5a19f35b28fc777d4bde9`.

v0.3.1 conserva policy.hpp byte a byte, payload StageService y una única escritura inicial health=150. Añade POST oficial al mismo execute, con pares PRE/POST de ID/HP sin punteros persistentes. Observación desde 150: no hay falsa pérdida 70. HP_DELTA/HP_INCREASE_OBSERVED miden cambios netos, con signo, pérdida efectiva y ordinal. No atribuyen espada, bomba o potencia bruta; cero UNKNOWN_OR_SPECIAL. Cambios entre llamadas se marcan OBSERVED_BETWEEN_EXECUTES. Sin cambios: ningún evento. Máximo 32 deltas, un aviso de supresión y resumen limitado por instancia.

- [Descargar TEST privado v0.3.1](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826/artifacts/11881653953), **11975 bytes**, SHA256 `0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344`.
- [CI Windows SUCCESS](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826): MSVC 19.51.36260 x64, Windows SDK 10.0.26100.0. 17 casos nuevos TEST_FAKE PASS, cuatro negativos PE rechazados, paquete y ambas descargas verificados.
- Fuente compilada `9dd5b8efd4ad98f1d6260820d782e101366a0f8b`; CI `7fd3628ee8bfeb30f8070db061220796c1c15b4a`. Checkpoint final añade solo informes/evidencia; fuente compilada sin cambios.
- Recuperación: tag `DEVF_CP03_HP_DIAGNOSTIC_OFFLINE_TEST`, rama `feature/devf-cp03-hp-diagnostic`, [PR25](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/25). CI en [PR17](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/17), rama `ci/devf-cp03-hp-diagnostic`. Draft, sin merge.

[Fuente y seguridad](SOURCE_REVIEW.md), [imports reales](IMPORT_REVIEW.md), [build/paquete](BUILD_AND_PACKAGE.md), [matriz](TEST_RESULTS.md), [recuperación](RECOVERY.md), [prueba humana/reversión](HUMAN_TEST.md). No ActorService, detours manuales, cambios de host/SDK/originales/saves/AI/colisiones/field_0x560 ni observación masiva. No se cargó la DLL o ejecutó el juego desde Codex.

Module ID conservado: instalar **solo un CP03**, retirando v0.3.0; nunca ambos juntos. Control instrumental original omitido para no ampliar alcance. A/B E_OC2 de CP02 en otra sesión, nunca confundir con E_OC de 40.
