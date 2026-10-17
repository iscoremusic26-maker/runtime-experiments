# Cambios CP00 — Windows
Se conservan commit/tag original y documentos de análisis anteriores. Se publica una rama de checkpoint privada, sin sobrescribir ramas existentes ni merge automático. Se añade workflow mínimo, script de preparación/verificación y evidencia de Actions Windows. El probe retiene la dirección de un símbolo público del juego para comprobar el enlace real, sin llamarlo, y añade /Zc:__cplusplus. Usa headers Aurora externos fijados por commit.

CI mirror en rama nueva del repo privado de insumos y PR #1 en borrador; ZIP, SHA256SUMS.txt, .gitattributes y main no cambiaron. Fuente original, EXE, ROM, partidas, mods y smoke Linux preservados. No instalación en PC, hook, spawn, modificación de escenario, framework ni CP01. Binarios propios de compilación solo en artifact de Actions; ningún binario original subido a logs/artefactos.

Informes actualizados: BUILD_ENV, TEST_RESULTS, GO_NO_GO, SOURCES_AND_VERSIONS, SERVICE_CAPABILITIES, handoff y resume. Evidence conserva hashes/resultados y extractos de los pasos de compilación/verificación, sin tokens ni contenido de ZIP original. Las advertencias de compilación se preservan como evidencia.

> Nota de navegación (2026-10-17): documento histórico de CP00. El estado actual del proyecto (CP08–CP10) está en `DEVF/TRANSFER_01_HANDOFF_2026-10-17.md`.
