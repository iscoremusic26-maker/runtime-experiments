# Gates mínimos: implementación, autorización y observación

**Estrategia recomendada A2; estrategia propuesta ≠ autorización de módulo activo ≠ autorización runtime.** Estados históricos intactos: G2 PASS_RUNTIME_OBSERVED limitado; G4 G4_RESOURCE_VERIFIED_POSITION_BLOCKED / NO_SAFE_POSITION_VERIFIED; G5 NO-GO; G6 NOT_VERIFIED; CP02 NO-GO; descarga DLL/perfiles personalizados BLOCKED independiente.

## Antes de implementación experimental: siguiente tarea, inicialmente desarmada

| Prioridad / requisito | Evidencia existente | Carencia y aceptación |
|---|---|---|
| I1. Alcance y contrato | E_OC CURRENT, modo0, FFFFFFFF, XFF14, recursos; SDK exacto y GameService epoch2. PASS_STATIC. | Aprobar estrategia/alcance explícitamente; una sola solicitud, callbackNULL, ningún Stage edit, sin hooks. Esta revisión no implementa nada. |
| I2. Resolver owner por room node | G2 reader valida ID/perfil/init y capas registradas sin cachear pointers; siete E_OC owner6, Link owner5. PASS_STATIC y observación histórica limitada. | Diseñar adaptación desarmada del resolver: vínculo child/node/escena, transición/estado de sala, contadores, previous registrado, revalidación local. Nunca fijar owner6 del log. |
| I3. Scope y tracking | Export/import y captura oficial de current acreditados; ActorService encola por ID. PASS_STATIC. | Revisión del controlador, slot ID reservado, latch antes de intento, restauración LIFO, error/throw/aceptación incierta, reentrada rechazada. Lab dirigido posterior, no suite histórica. |
| I4. Política de lifetime | Call path nativo y limitación delete/cancel acreditados. | Cierre completo sin hot reload/desactivar; no cancel ABI, pointers duraderos, perfiles/callbacks propios ni recursos DLL en actor. No prometer rollback manteniendo el juego abierto. |

**No se necesita antes de diseñar/compilar el consumidor desarmado:** un XYZ aprobado, demostrar todas las trayectorias, enumerar todo el progreso del juego o retirar/recrear room3. Un controlador puede rechazar siempre activación mientras ubicación siga pendiente. Si no logra demostrar el contrato local de owner, no se convierte en activo.

## Antes de autorizar una única prueba manual

| Prioridad / requisito | Ya satisfecho / alcance | Pendiente verificable |
|---|---|---|
| R1. Consumidor exacto, sin hooks | SDK/exports anteriores y observador anterior; no certifican nuevos imports. | MSVC/Windows SDK link del consumidor nuevo + lab scope/latch/errores + revisión independiente de código/paquete. No rebuild del host, tests solo afectados. |
| R2. Owner y contexto del instante | G2 demuestra que existe la relación sala/hijo en una sesión real, no pin de lifetime. | Guardas fail-closed del nuevo controlador, sala completa/activa sin teardown/transición/pendientes, caller y child registrados, escena y Link vivos en el tick; auditoría del scope sin reentrada destructiva. Podrá observarse baseline dirigido con autorización aparte si hace falta. |
| R3. Ubicación local de ensayo | ARC, modelos/BCK y cotas condicionadas401/494/501; soporte local/Acch, paredes/objetos/rutas/Digpl ya documentados. PASS_STATIC condicionado. | Admitir **un punto** y un intervalo operativo: superficie/material/pendiente/agua, clearance inicial suficiente para cuerpo/arma, sin overlap de originales ni trigger/evento local plausible, con observación de riesgos dinámicos pertinentes. El punto antiguo sigue sin admitir. No inventar radio/horizonte de contención. |
| R4. Admisión y recursos efectivos | FILIbitSwFF cubre filtro genérico concreto; FFFFFFFF sentinels; E_OC y E_ocb íntegros, registered G2, overlays del servicio0. | Verificar contexto actual sin forzar layer6/progreso y acceso a recursos requeridos mediante APIs/evidencia de instalación. Registered no equivale a fase completa; carga/heap final se observarán durante Create. No se exige hash de cada buffer runtime antes de solicitar. |
| R5. Estado de sesión | D3D12 oficial en G2 con Randomizer/Luau/texturas activos. | Ejecutable intacto, baseline lo más aislado posible, configuración y versión documentadas; backup saves/config, plan de no guardar/no escritura deliberada, comprobar autosave oficial y su prevención reversible antes de ensayo. Si no puede prevenirse un guardado inesperado de forma permitida, detener y revisar; cerrar proceso no revierte un save escrito. |
| R6. Permiso y recuperación | Políticas anteriores, nada instalado. | Paquete futuro separado/reversible, verificación independiente, autorización expresa de instalación/prueba manual; timeout finito declarado de pending/observación y criterios de parada, posibilidad de cierre externo si host cuelga. No hot reload. |

R3 no obliga a probar ausencia universal de detección social ni navegación perfecta. Detección/WALK son comportamiento nativo esperado y resultados observables, no por sí solos corrupción del host. Sí debe excluirse una interferencia local plausible con progreso o un spawn inicial inseguro. El movimiento no queda físicamente confinado por timeout; si sale del área observada, se detiene la sesión. El tiempo de reacción humano y la primera ejecución dentro de Create son riesgos residuales explícitos: no llamar seguro a un punto por prometer detenerse rápido.

El censo global completo y flags concretos0x1E08/0x0C01 dejan de ser requisitos universales del ensayo. Consultar solo condiciones necesarias para ese caso: actores próximos que puedan interferir, evento/transición actual y layer efectivo/procedencia conocida. La presencia natural y FILIFF no certifican el estado entero de la partida. Si un riesgo local requiere un estado no observado, esa pieza concreta continúa pendiente.

## Verificable únicamente durante el ensayo autorizado

| Comprobación | Estado hoy | Evidencia de aceptación |
|---|---|---|
| Request único y posterior readiness | NOT_TESTED / NOT_VERIFIED | ID propio, pending→actor nativo completo; perfil/room/owner esperado, sin callback DLL; no confundir ausencia de request con éxito. |
| Owner de instancia y draw | NOT_VERIFIED | Layer hija validada y propietario observado; render Link/E_OC normal, sin draws duplicados/ciclos o errores DX12. Foto sola no prueba ownership. |
| Comportamiento inicial | NOT_VERIFIED | Log/clip del intervalo, animación/movimiento nativos; documentar detección/estado real, sin forzar WAIT ni HIO. |
| Suelo/arma/contacto visible | NOT_VERIFIED | Observación real del punto y límites; no proclamar PASS de colisión/combate sin ejercicio específico. |
| Fallo o cierre supervisado | NOT_VERIFIED | Consumo único, sin retry, salida completa; preservar evidencia si request no termina. No prometer limpieza interna por terminar el proceso. |

## Diferibles hasta G6 o framework/CP02

- Destrucción y recreación natural de room3, retención RTBL, doble entrada, stage/room/layer changes con instancia viva: **G6**, no requisito de recarga para A2 inicial. No retirarlo si el diseño intenta transicionar en el primer ensayo.
- Cancelación precisa de pending, eliminación de actor manteniendo host abierto, familia completa de descendientes, reenable y descarga dinámica: garantías posteriores, NO-GO si se prometen ahora. Primer ensayo usa exclusivamente cierre completo.
- Navegación bajo múltiples combates/eventos/progresiones, censo completo de todas las salas, bounds runtimeF32 universales, footprint/IK perfecto y múltiples enemigos: producto estable. No borrar incertidumbres existentes ni inventar región segura.
- Stats, AI, recompensas, apariencia/colliders por instancia y persistencia: variantes posteriores. Bloqueo DLL personalizado permanece separado y no se exige resolver para callbacks exclusivamente nativos.

**Camino mínimo:** aprobar diseño → controlador A2 desarmado y revisión/link/lab dirigidos → admitir punto y condiciones locales con evidencia específica → revisar paquete y pedir autorización manual → un ensayo. Ningún gate se aprueba automáticamente con este documento.
