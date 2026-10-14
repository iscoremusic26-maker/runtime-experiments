# CP04.4 — Recuperación privada

Estado **CP04_4_BLOCKED_WITH_EVIDENCE**. No mod nuevo instalado/compilado; sólo documentación, evidencia derivada y herramienta propia de procedencia. CP05/CP06 no iniciados.

- Repositorio privado: `iscoremusic26-maker/Mods-Duskligh`.
- Rama: `feature/devf-cp04-4-black-bokoblin`.
- Base: `139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f`, CP03 humano.
- Checkpoint temprano de recuperación: `a3c6b934e27c40c2044dfc6c83eb835c0b0a1c95` (padre CP03).
- [PR30 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/30), base `feature/devf-cp03-hp-diagnostic`, no merge.
- Tag final solicitado: `DEVF_CP04_4_BLACK_BOKOBLIN_BLOCKED_WITH_EVIDENCE`; sólo será reportado publicado después de verificar su destino remoto.
- Historial anterior: snapshot de heads/tags previo en [evidence/previous-refs.json](evidence/previous-refs.json). No se actualiza ninguna ref anterior.
- CP04.3 referencia conservada: `3b7f65b3f4268ae30d4f5832001114b8a6b260ce`, tag `DEVF_CP04_3_PRIVATE_SCENT_MARKER_OFFLINE_TEST`; runtime NO-GO aportado por usuario no convierte ese paquete en visual PASS.

Para restaurar en entorno nuevo, clonar el repo privado **a directorio nuevo**, fetch refs, checkout detached del tag final si existe (o del commit exacto de este informe de cierre). Ejecutar el verificador estático. No reset/clean sobre un workspace con cambios ajenos. El tag de la base CP03 y todas sus rutas permanecen intactos; no reejecutar sus suites, ubicación o auditorías.

## Qué se conserva y qué falta

Se conserva el estudio nuevo de propiedad Model/ModelData/packets, diffDL, current vertex colors, regeneración/interpolación, loader/rawbuffer y captura Aurora/D3D12; ver ROOT_CAUSE. No reconstruir partículas ni recompilar CP03. No se ha preparado ni perdido un recoloreador CP04.4: no se admitió su diseño. El Cloud no ofreció archivos locales recuperables en esta sesión; el estado real está en GitHub.

Falta exclusivamente: (1) canales y separación de material del E_OC2 efectivo, (2) cerrar ownership/reconstrucción/retire de una ruta individual, (3) si se admite, implementar y ejecutar tests/build/paquete/descarga nuevos y prueba humana. La interfaz pendiente se describe con límites explícitos; no se afirma inexistencia absoluta de APIs JKR o privadas de J3D.

Rollback de esta revisión documental: no requiere tocar instalación. Conservar CP03 histórico o instalación vanilla según estado previo del usuario. No crear/eliminar ramas/tags previos. No ejecutar juego ni cambiar saves al recuperar.

El workflow nuevo sólo verifica Git/procedencia y sella un tag único; resultados concretos y SHA se agregan al terminar, sin fingir autorreferencia del commit que contiene este archivo.
