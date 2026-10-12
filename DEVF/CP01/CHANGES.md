# Cambios de revisión CP01 desde 092c1e6
- ActivationRequirements y start_guarded: build desarmada antes de registrar cualquier perfil, edit o actor. Política exacta DISARMED_NO_REGISTRATION, versión diagnóstica 0.1.1.
- ResourceLifecycle.release devuelve éxito/fallo; conserva archivo/refs ante fallo, pasa a closing y prohíbe nuevas cargas/callbacks. Cancelación UNK3 terminal.
- Rock comprueba retirada de colisión y fase de archivo antes del destructor, evita refs de heap fallido y no ejecuta transformaciones de un actor no listo. Sin inventar cancelación de mount pendiente.
- Controller rechaza callbacks opcionales de creación sin token de vida.
- Laboratorio incremental: nueve regresiones afectadas, 20 casos nuevos distintos en runs separados (14 + 6), cinco funciones upstream exactas con backends simulados y fixtures DLL Windows propias. No suite original de 16 completa ni CP00/SDK Linux.
- Auditoría dirigida de colas/desregistro/force-delete/archivo/unload, inventario de datos ausentes y guía de captura en Windows mediante vistas nativas.
- Informes/evidencia/hashes nuevos; PR #2 y ramas existentes actualizadas. Historial/tags originales y sus evidencias preservados.

Sin modificaciones de ZIP, source upstream, EXE, ROM, saves, escenarios, otros mods, hooks, PIN del mod, instalación, apariciones o CP02. No TEST aprobado. La build cerrada no aporta proof of life de actor: solo evita generar el estado inseguro mientras faltan garantías.

- Propiedad de colisión: inspección de referencias propias con APIs públicas, comprobación de índice/actor y rechazo de duplicados. Tras limpieza de escena solo retira el ID local si ya no hay referencias propias; nunca retira un slot reutilizado por otra colisión. Seis casos nuevos en el run final; suites previas no repetidas.

## Actualización de ubicación desde 58c4966

Evidencia F_SP121 recibida por Git LFS, íntegra y analizada. LOCATION_ANALYSIS y evidence/location-f-sp121-*.json documentan candidato geométrico condicionado y pendientes concretos. Bloqueo operativo superado; seguridad del lugar aún no aprobada, unload sin cambios. Mantener DISARMED_NO_REGISTRATION. No hubo cambios al módulo/host, nuevas compilaciones o repetición de suites, TEST activo ni CP02. Nuevo checkpoint de recuperación DEVF_CP01_LOCATION_F_SP121_REVIEW en rama documental existente.
