# Prueba real y reversión — pendiente, no ejecutada

El artefacto actual es BUILD ONLY, no un TEST aprobado: no instalarlo para obtener apariciones. La implementación disponible tiene las apariciones desactivadas. Estas instrucciones describen la prueba siguiente de CP01 cuando se resuelvan los bloqueos; no autorizan CP02.

## Requisitos para habilitar una ubicación
1. Obtener evidencia en Dusklight 2.0.3 Windows x64/DX12 del stage, room y layer reales, posición/orientación, suelo/colisión, ausencia de solapamiento con scripts/actores retail y disponibilidad de Wrock. La ubicación del demo no basta por sí sola.
2. Construir el registro con stage_actor_data_class del SDK exacto, revisar el diff y probar una única autoridad Stage. No añadir simultáneamente create_actor runtime. No modificar .dzs/.dzr, ROM ni save.
3. Resolver o acotar con evidencia de proceso limpio el fallo de unload: nunca desactivar/recargar el mod con actor activo o creando. Probar destrucción por salida normal de escena, incluyendo carga pendiente y recursos fallidos, antes de una aprobación TEST. Si hay callbacks retenidos o MOD_UNAVAILABLE, conservar logs y detener prueba.
4. Recompilar y superar el laboratorio/paquete del checkpoint revisado antes de etiquetar DEVF_CP01_TEST.dusk. El checkpoint actual no incluye ese paquete.

## Instalación futura de un TEST aprobado
- Cerrar completamente Dusklight. Conservar las versiones originales, partidas y el mod anterior si existiera; no sobrescribirlos.
- Comprobar hash del TEST aprobado y copiar únicamente ese nuevo .dusk en %APPDATA%\TwilitRealm\Dusklight\mods. No sustituir EXE, DLL retail ni otros mods.
- Iniciar un proceso nuevo de Dusklight 2.0.3, escoger DX12 y confirmar versión/backend. Activar una sola prueba CP01, sin hot reload. Primero conservar log de imports/registro sin actor; después probar la ubicación verificada conforme a la revisión autorizada.
- Guardar evidencia de created/ready, callback tick/draw y colisión visible, room/layer, salir/recargar sala sin duplicados y deleted con recursos liberados. Un PASS de laboratorio no sustituye estos resultados. Si aparece crash o limpieza incompleta, cerrar el proceso y conservar log/dump.

## Reversión
Cerrar el proceso antes de cualquier retirada. Quitar únicamente el nuevo .dusk TEST de la carpeta de mods y restaurar la copia anterior, si la había. Reiniciar el juego y comprobar baseline. No tocar ROM, partidas, EXE, archivos de escena ni otros mods. No usar Disable/Reload como mecanismo de recuperación con actor vivo mientras el unload permanezca sin certificar.
