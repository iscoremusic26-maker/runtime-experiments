# NO EJECUTAR TODAVÍA — plan para autorización separada

Este documento no autoriza instalación, empaquetado, sesión ni spawn. No hay `.dusk` activo ni DLL entregable. Se revisará primero el paquete experimental separado y después la sesión cold-start G5.

Antes de una sesión futura:

1. Aceptar explícitamente el alcance experimental de C y los riesgos residuales, revisar provider de admisión y una nueva build/auditoría. Confirmar ejecutable oficial2.0.3 Windowsx64/DX12 intacto; no usar el host experimental ni modificarlo.
2. Identificar y respaldar saves, autosaves y configuración reales de la instalación. Confirmar una restauración reversible; no inventar rutas ni editar progreso. Full exit o desinstalación no revierten escrituras de save/autosave.
3. Cold start, sin hot reload. Aislar reversiblemente Randomizer y mods de actores/layers/hooks/recursos; Luau y1867 reemplazos presentes en la sesión antigua no prueban aislamiento. No borrar configuración ni recursos.
4. Cargar la partida normalmente en F_SP121 room3/logical6, sin teleport, comandos de escenas, flags o save edits. Revisar cumplimiento real del nuevo guard: Link>=1600 XZ, velocidades públicas cero, censo completo e identificable, medio y contexto A/B/C. El umbral no garantiza seguridad física; si el guard deniega, no desactivarlo para forzar el ensayo.
5. Revisar y autorizar por separado como máximo un E_OC y una sesión. No usar reload/reinitialization/error como retry. La política no obliga a mover Link ni altera AI/combate/cámara.
6. Criterios de parada: cambio de room/scene/layer/owner/evento, incertidumbre de cola/ID/fase, scope restore fallido, timeout, desaparición, falta de evidencia/traza o comportamiento adverso. STOP significa ninguna nueva mutación, no desaparición garantizada del actor; cerrar el proceso completo por acción humana y preservar líneas DEVF_PILOT.
7. Evidencia mínima: init/version, prechecks, distancias/IDs/contexto, intento/layer, requestbegin/result exacto, restore, requested/pending/ready y terminales/budget. Añadir evidencia real de render/animación/colisión/limpieza cuando se observe; ACTOR_READY_OBSERVED no valida esas categorías.
8. Terminar mediante full exit. Revisión de progreso y restauración solo bajo el plan y autorización pertinentes. Ningún script de instalación/ejecución se entrega aquí.

No G5/G6/CP02 en esta tarea. El único trabajo siguiente propuesto es revisión/autorización separadas del paquete activo, seguidas de la autorización de sesión G5, no ejecución automática.
