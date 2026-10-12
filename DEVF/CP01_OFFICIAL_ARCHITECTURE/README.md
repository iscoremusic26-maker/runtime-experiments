# DEVF CP01 — arquitectura sobre el host oficial

Evaluación independiente desde `765e16dcd86c1eeda45bad80a2c1380129565429`.
Producto objetivo: `.dusk` cargado por Dusklight oficial 2.0.3 Windows x64 DX12, sin cambios al ejecutable, hooks/detours internos, recursos originales ni partidas.

Estado: **CP02 NO-GO**, **DISARMED_NO_REGISTRATION**. No hay colocación aprobada, TEST activo ni instalación. La implementación `DEVF/CP01` y los experimentos anteriores se conservan íntegros.

Se evalúan dos rutas: colocaciones de perfiles nativos sin callbacks de DEVF, y adaptadores por instancia mediante servicios/ABI oficiales. La primera no demuestra por sí sola las variantes avanzadas del producto.

El prototipo independiente serializa registros ACTR/TGSC de `E_SB` y conserva un cierre de compilación permanente. No tiene configuración que pueda armarlo. Los valores del laboratorio son datos sintéticos de codificación, no una ubicación del juego. Los targets explícitos de CI no empaquetan `.dusk`, no instalan y no compilan el host. Se publican solo textos propios.

La evidencia estática reproducible está en `evidence/source-references.json`. El laboratorio Windows nuevo se publica mediante el workflow `devf-cp01-official-architecture.yml`. Los informes finales se completan después de recibir sus resultados.
