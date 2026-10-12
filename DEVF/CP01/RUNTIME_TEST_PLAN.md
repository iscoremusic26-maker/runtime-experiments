# Prueba Windows y reversión — revisión bloqueada

**No hay TEST de actor aprobado ni una instalación que autorizar en este checkpoint.** No copiar/activar la build desarmada esperando un actor. Puede obtenerse evidencia de ubicación con el juego original y sin mod, siguiendo LOCATION_EVIDENCE.md.

Antes de cualquier futura prueba activa, acreditar ubicación/recursos/eventos y una garantía de host que drene pendientes y retenga perfil/contexto/DLL ante fallo; el retorno de shutdown y evitar manualmente Reload no sustituyen esa garantía. Resolver también el archivo async (resDelete no acepta phase 1). No abrir requirements mediante un booleano sin evidencia ni implementar hooks improvisados.

Cuando exista un TEST técnicamente justificado y revisión autorizada:
1. Cerrar completamente Dusklight, guardar copia de configuración/partida y de cualquier DEVF anterior. Verificar hash de TEST y confirmar host exacto 2.0.3/DX12. Copiar únicamente TEST a %APPDATA%\TwilitRealm\Dusklight\mods, sin sobrescribir EXE/ROM/escenas/otros mods.
2. Arrancar un proceso nuevo. Usar una única autoridad de aparición en la ubicación/capa verificadas. Registrar create/ready/tick/draw/delete y contexto de sala, preservar vanilla, no guardar progreso como parte de prueba. Capturar render, colisión y salida/reentrada/capa con logs reales; FAIL detiene ejecución.
3. Solo después de garantías y evidencia, probar el mecanismo de desactivación autorizado. No usar hot reload con actores en un host que sigue sin barrera.

Reversión: cerrar proceso; retirar solo nuevo TEST y restaurar copia anterior si existía; reiniciar baseline y conservar logs/dumps. No borrar ROM, saves, EXE o archivos de escenario. No ejecutar estas acciones automáticamente.
