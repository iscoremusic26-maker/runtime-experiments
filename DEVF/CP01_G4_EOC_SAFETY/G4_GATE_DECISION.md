# G4 — decisión del expediente

**G4_BLOCKED_WITH_EXACT_NEXT_INPUT. Ubicación: NO_SAFE_POSITION_VERIFIED.** Mantener `DISARMED_NO_REGISTRATION`. G5 no autorizado; CP02 NO-GO. Este checkpoint documenta una revisión, no un G4 superado.

| Gate | Estado | Evidencia y límite |
|---|---|---|
| G0 enemigo/contexto | PARTIAL; selección PASS_STATIC | Preset E_OC y FILI conservados; room3/logical6 observados en G2. Sin nueva posición/envolvente ni admisión de una adición |
| G1 observador/build | PASS_STATIC + PASS_LAB históricos | SDK/MSVC/link/guardas y47 controles del paquete conservados, sin recompilar ni repetir suites |
| G2 observación | PASS_RUNTIME_OBSERVED limitado | Log primario íntegro:28 capturas,7 originales móviles,owners diferenciados,D3D12 y cierre normal del observador; usuario confirma visual normal. Baseline con Randomizer/texturas |
| G4 referencias de recursos | PASS_STATIC; expediente PARTIAL | Fuente oficial/headers: modelos3/4, BCK0x1B y joints/colliders; presencia de recursos registrada en G2 |
| G4 archivos/envolvente | BLOCKED; NOT_VERIFIED | E_OC/E_ocb no disponibles en corpus. Sin SHA/estructura/índices reales, dimensiones de modelos ni máximos animados de cuerpo/arma |
| G4 ubicación | BLOCKED; NO_SAFE_POSITION_VERIFIED | WRock/terreno anteriores reutilizados. Distancias muestreadas nuevas; Link488.5791 al punto anterior. Sin volumen/movimiento con márgenes acreditados |
| A1 propiedad por carga natural | PASS_STATIC condicionado | ROOM_SCENE→Stage Add→request CURRENT hija según fuente; no prueba de Add ejecutada, readiness, nueva owner o limpieza |
| G5 una aparición | NO-GO; NOT_TESTED | No autorizado, sin recursos/envolvente/ubicación/aislamiento/control runtime suficiente; no se implementó ni ejecutó |
| G6 retiro/transición/limpieza | NOT_VERIFIED; NOT_TESTED | Contratos nativos conservados; ninguna nueva instancia para probarlos |
| Descarga DLL de perfiles personalizados | BLOCKED independiente | Resultado previo conservado; no se investigó, parcheó ni resolvió con G2 |
| CP02 | NO-GO | No iniciada; G4 abierto y garantías del framework pendientes |

PASS_STATIC significa evidencia de código/formatos o geometría dentro del alcance declarado; PASS_LAB solo laboratorio ejecutado identificado; PASS_RUNTIME_OBSERVED únicamente sesión real documentada. PARTIAL es expediente incompleto; NOT_VERIFIED es ausencia de evidencia suficiente; NOT_TESTED es operación no ejecutada; BLOCKED identifica un requisito imprescindible; NO-GO impide avanzar. No son estados intercambiables.

## Resuelto durante esta revisión

- Integridad del adjunto anonimizado,2182 líneas y28 capturas; diferencia explícita respecto del hash del original no recibido.
- Censo y capas propietarios completos, severidades reales, cierre normal y condiciones no aisladas; origen220/221 sin atribución inventada.
- Uso de todas las posiciones muestreadas para agregados/distancias. No se certifican trayectorias continuas ni se confunden requests con instancias vivas.
- Inventarios disponibles y `.dusk` oficiales: no aportan los dos ARC. Fuente de disco/overlays y extracción mínima identificadas.
- Ruta A1 natural y su propiedad CURRENT hija confirmadas estáticamente, sin ejecutar APIs ni modificar observador/host.

## Bloqueo preciso y siguiente acción mínima

Se necesitan **solo E_OC/E_ocb completos, privados, con SHA256/tamaños y procedencia de la fuente efectiva GZ2E01 de G2**. [EOC_RESOURCE_VERIFICATION](EOC_RESOURCE_VERIFICATION.md) describe la exportación de lectura de dos entradas, manifiesto y canal privado. No se pide ROM, EXE, SDK, log ni recursos anteriores.

Esos archivos son necesarios para fundamentar modelo/joints/arma/BCK y una envolvente con la cual contrastar suelo, obstáculos y zonas de movimiento. Su recepción abre únicamente una revisión offline pendiente; no acredita automáticamente posición segura ni autoriza G5. Después pueden persistir requisitos puntuales de escenario/progreso/runtime, enumerados en [EOC_POSITION_SAFETY](EOC_POSITION_SAFETY.md) y [A1_G5_PREREQUISITES](A1_G5_PREREQUISITES.md).

Esta tarea se detiene aquí. No se entrega artefacto TEST activo ni se solicita ejecutar el juego.
