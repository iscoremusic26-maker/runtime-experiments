# Continuidad — CP-R00

Fuente `40457c6adb381928e4b5fef6ed459ed291edd5e2`, árbol `e4b79b565b2842f711f7c9f2390f56ef11063157`; objetivo Windows x64 / DX12 / GZ2E01. Rama `research/dusklight-203-dusk-atlas` desde CP00 seguro `747ecc410162ed76f9aa68dbe9e9e2ad4e4d8c3f`.

Completado: acceso a tres repositorios, tag y SHA exactos, revisión de ramas/PR históricos en solo lectura, certificación por hashes de la fuente disponible, inventario clasificado de 19367 archivos y 488 directorios con archivos descendientes. Cuatro gitlinks externos faltantes y un batch Android de bytes distintos están identificados en SOURCE_PIN.md. No se ha modificado fuente ni creado un mod.

Primera acción al continuar: leer README.md, SOURCE_PIN.md, INVENTORY.md y este archivo; incorporar los informes de implementaciones en progreso y sus fragmentos de evidencia. Prioridad: todos los servicios reales, loader/hooks/ABI y orden de cleanup; después escenas/guardado, jugador/actores y presentación. No repetir el inventario salvo cambio de pin o de herramienta. No contar análisis pendiente como completado.

En esta sesión el ZIP se extrajo en `work/source/dusklight-2.0.3` y los borradores están en `work/atlas/DUSKLIGHT_RESEARCH`. Son rutas efímeras de ejecución, no una dependencia del atlas. Para regenerar el inventario desde otra copia certificada: `python DUSKLIGHT_RESEARCH/tools/inventory.py RUTA_FUENTE RUTA_SALIDA_SEPARADA`.

Persistencia mediante conector GitHub: Git/gh del entorno no conectaban correctamente. Crear árboles/commits sobre el HEAD de esta rama, comprobar el diff restringido a DUSKLIGHT_RESEARCH y actualizar ref sin force con expected_sha. No escribir en upstream ni CI. No tocar fuente PR #80/#81 o CI #65/#66.

Las afirmaciones del juego requieren futuras pruebas expresamente fuera de esta campaña estática. No hay tarea programada ni ejecución de fondo prometida.
