# DEVF CP01 — arquitectura sobre el host oficial

Evaluación independiente desde `765e16dcd86c1eeda45bad80a2c1380129565429`.
Producto objetivo: `.dusk` cargado por Dusklight oficial 2.0.3 Windows x64 DX12, sin cambios al ejecutable, hooks/detours internos, recursos originales ni partidas.

Estado: **CP02 NO-GO**, **DISARMED_NO_REGISTRATION**. No hay colocación aprobada, TEST activo ni instalación. La implementación `DEVF/CP01` y los experimentos anteriores se conservan íntegros.

Se evalúan dos rutas: colocaciones de perfiles nativos sin callbacks de DEVF, y adaptadores por instancia mediante servicios/ABI oficiales. La primera no demuestra por sí sola las variantes avanzadas del producto.

El prototipo independiente serializa registros ACTR/TGSC de `E_SB` y conserva un cierre de compilación permanente. No tiene configuración que pueda armarlo. Los valores del laboratorio son datos sintéticos de codificación, no una ubicación del juego. Los targets explícitos de CI no empaquetan `.dusk`, no instalan y no compilan el host. Se publican solo textos propios.

**Resultado nuevo:** Windows/MSVC, 26 expectativas de laboratorio PASS, módulo service-only compile/link PASS y tipos públicos del ABI compile-only PASS. [Run verificable](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38277234930). No acredita aparición, render, colisión, descarga runtime ni DX12.

| Entrega | Informe |
|---|---|
| Arquitectura recomendada, GO/NO-GO y experimento futuro | [ARCHITECTURE_DECISION.md](ARCHITECTURE_DECISION.md) |
| Objetivo completo por funcionalidad, clases A/B/C y alternativas | [FEASIBILITY_MATRIX.md](FEASIBILITY_MATRIX.md) |
| Contratos exactos de las rutas nativas/avanzadas | [ROUTES_AND_CONTRACTS.md](ROUTES_AND_CONTRACTS.md) |
| Riesgos originales frente al experimento | [OFFICIAL_HOST_RISKS.md](OFFICIAL_HOST_RISKS.md) |
| Funciones/API, hashes y líneas de fuentes | [SOURCE_REVIEW.md](SOURCE_REVIEW.md), [JSON](evidence/source-references.json) |
| Nuevas pruebas, intento inicial y logs persistentes | [TEST_RESULTS.md](TEST_RESULTS.md) |
| Rama/tag/PR y reproducción limitada | [RECOVERY.md](RECOVERY.md) |

La definición de colocaciones originales puede evitar callbacks DLL de actor. El acceso ABI a datos por instancia ofrece vías reales de investigación para variantes; su semántica y aislamiento deben verificarse por enemigo. No se reduce el producto a colocaciones vanilla. Retirar una definición Stage no elimina automáticamente actores/request ya creados.
