# Puerta CP00 — actualización Windows
**GO técnico de CP00 para abordar CP01 únicamente tras autorización. CP01 NO iniciado.**

| Criterio original CP00 | Resultado |
|---|---|
| Fuente y distribución 2.0.3 exactas accesibles | PASS; hashes y CRC coinciden |
| SDK/ABI, servicios, símbolos y referencia nativa contrastados | PASS de análisis y verificación estática; límites runtime documentados |
| Repo aislado, checkpoint y recuperación Git | PASS; original 8a14628/tag DEVF_CP00 recuperado por fetch desde GitHub |
| Build mínima nativa Windows x64 sin reconstruir el juego | PASS; MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0 |
| Paquete, DLL, exports, imports y versiones de servicios verificables | PASS; run 38184306482, evidencia y hashes conservados |
| Rutas A/B y experimento CP02 evaluables | PASS de propuesta; decisión arquitectónica permanece CP02 |
| Informes y checkpoint de etapa | PASS; rama y tag nuevo DEVF_CP00_WINDOWS |

El NO-GO anterior por ausencia de build Win64 está resuelto. El handoff original exige build mínima y estrategia evaluable en CP00; sitúa proof of life Actor/Stage en CP01, reutilización de IA en CP02 y aislamiento visual en CP04. GO no certifica esas etapas ni autoriza iniciarlas por sí mismo.

**Pendiente, fuera de aceptación CP00:** cargar el probe en el host real, comprobar resolución de servicios y rechazo runtime de versión, lifecycle, escena, IA, colisión y render Windows/DX12. Todo permanece NOT_TESTED. No instalar este artefacto como TEST ni llamarlo mod final. Las comprobaciones runtime antes de un TEST siguen vigentes.

> Nota de navegación (2026-10-17): documento histórico de CP00. El estado actual del proyecto (CP08–CP10) está en `DEVF/TRANSFER_01_HANDOFF_2026-10-17.md`.
