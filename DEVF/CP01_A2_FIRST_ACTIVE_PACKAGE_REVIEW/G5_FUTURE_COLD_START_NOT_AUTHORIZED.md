# NO EJECUTAR TODAVÍA — plan futuro de sesión

**ACTIVE-CAPABLE / NOT INSTALLED / NOT RUN / SESSION NOT AUTHORIZED.**

Dusklight **2.0.3 Windows x64/DX12**; paquete ID`dev.devf.cp01_eoc_first_active_pilot` versión`0.0.1`; fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`.

Este plan exige aprobación posterior explícita del paquete concreto y de una sesión. **La DLL está técnicamente armada y podría solicitar un E_OC automáticamente al pasar A/B/C; no espera un botón de confirmación.** No instalar, cargar ni iniciar el juego ahora.

1. Revisar ID/version/provider/manifiesto y riesgos. Comprobar `.dusk` SHA`f1475a82dc0d4783f2dcedd1d0748390733ff0f5006ddd54842691246397bd78`/33897bytes; EXE oficial SHA`ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`/52309504bytes. No modificarlo. Mantener el paquete fuera de las carpetas buscadas por el juego hasta autorización.
2. Identificar por el operador las rutas reales configuradas de mods, data, saves, autosaves y configuración. Respaldar sin sobrescribir backups; conservar lista/settings de mods y acordar reversión. Las rutas son configurables: no se inventa una ruta de instalación. Salir o quitar el mod no revierte progreso.
3. Preparar un proceso frío oficial2.0.3/DX12, aislado reversiblemente de Randomizer, otros mods de actores/hooks/layers/recursos y otros DEVF. La sesión histórica Luau/Randomizer/1867 textures no certifica aislamiento. Si no se acredita aislamiento/restauración, detenerse antes de instalar.
4. Acordar un estado alcanzable por juego normal en F_SP121/room3/logical6, sin teleport, flags o save edits. Link requiere XZ>=1600 e inmovilidad; otros actores también XZ>=1600 por centros. El censo global estricto puede denegar. Los13 snapshots G4B no validan esta política; C sigue sin certificación física. No aflojar guards ni mover/reemplazar actores para forzar PASS.
5. Autorizar como máximo un intento en una sesión concreta. La futura instalación será con proceso completamente cerrado y carpeta verificada, sin DLL suelta ni cambio de EXE/recursos; sin overwrite ni IDs duplicados. Cargar el paquete permite que la primera condición elegible encole automáticamente. Prohibido hot reload/re-enable en vivo o retry con otra imagen/sesión sin revisión humana.
6. Conservar en privado líneas DEVF_PILOT en orden: init/ABI/PackageProviderArmed, A/B/C y captura/update, Link XZ, latch, layer, create begin/result+ID, restore, REQUESTED/PENDING/READY/STOP/budget. Copiar solo esas líneas sanitizadas; no publicar logs completos. READY no demuestra render/collider y el logger void/budget puede perder evidencia; ausencia de log no es PASS.
7. Parar ante versión incompatible, crash/freeze, cambio de room/layer/owner/evento, restore fallido, ID/cola/fase inciertos, timeout, log fallido, actor inesperado o comportamiento/progreso anómalo. STOP no cancela. FULL EXIT humano ante incertidumbre; sin cancel/delete, forced scene, parche host o retry. Preservar notas y log privado; restore/relaunch se rige por el plan aprobado.
8. Tras cerrar completamente, retirar únicamente el archivo nuevo de la carpeta verificada, preservar históricos y revisar estado/backups antes de restaurar nada. No declarar limpieza/rollback por salir. Evaluar G5 solo con evidencia real; G6 y CP02 siguen pendientes.

No se ejecutó ninguna sesión en esta entrega. **NO EJECUTAR TODAVÍA.**
