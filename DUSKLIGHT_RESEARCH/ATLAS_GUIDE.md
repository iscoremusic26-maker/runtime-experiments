# Guía de consulta del atlas

Esta guía orienta una pregunta técnica abstracta;no implementa ni diseña un mod. Fuente única Dusklight2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2`, Windows x64/DX12/GZ2E01 USA como objetivo. Las rutas son muestras estáticas, no garantías de compatibilidad. Véanse [pin](SOURCE_PIN.md),[readiness](V1_READINESS.md) y [auditoría enfocada](AUDIT_FINDINGS.md).

## Recorrido de una consulta

1. Formular la capacidad y el hito buscado:registrar, solicitar, consumir, crear, ejecutar, retirar o persistir. No tratarlos como sinónimos.
2. Buscar el área en [SYSTEM_INDEX](SYSTEM_INDEX.json). Leer scope, coverage, pending y reports. Un área READ puede tener cadenas concretas contrastadas;una CROSSCHECKED sigue siendo selectiva. Las 28 entradas no son 28 subsistemas enteramente comprendidos.
3. Consultar [SDK_AND_SERVICES](SDK_AND_SERVICES.md) y [matriz .dusk](DUSK_INTEGRATION_MATRIX.md). Preferir un contrato oficial si cubre exactamente esa capacidad. Un nombre parecido no amplía su alcance. GameService declara época ABI,no operaciones de gameplay.
4. Buscar nombre/firma en [SYMBOL_INDEX](SYMBOL_INDEX.json), revisar conditions/risks y seguir evidence_ids al [ledger](EVIDENCE_LEDGER.json). Abrir contrato, implementación y consumidor en sus permalinks del SHA fijo. Si un source no tiene url opcional,seguir su evidence_id o construir el enlace con repo/commit/path/line_start/line_end ya registrados;no usar HEAD móvil. No confundir localizador potencial con símbolo exportado.
5. Leer la ficha de ese sistema y [dependencias](SYSTEM_DEPENDENCIES.md). Identificar dueño de estado/storage, fase/hilo, gates, copia frente a préstamo y frontera de error. Distinguir retirada del registro de devolución del callback en curso y de liberación segura del código.
6. Comprobar [riesgos](RISK_REGISTER.md) y [preguntas](OPEN_QUESTIONS.md). Si falta una flecha causal,abrir solo la fuente mínima necesaria y marcar la incertidumbre;no extrapolar de otro servicio/actor. Conservar los supuestos de STATIC_INFERRED.
7. Separar lo pendiente para Windows:imagen exacta,versiones disponibles,export/manifiesto,firma/layout cuando se necesite,fase y coexistencia/rollback propios. Este atlas no ejecutó esas comprobaciones;no autoriza iniciarlas en la campaña documental.

## Cinco capacidades neutrales y sus fronteras

| Necesidad abstracta | Primera ruta y evidencia | Qué aclarar antes de una integración futura |
| --- | --- | --- |
| Registrar un actor | ActorService, SDK-001 y HOOK-029;[actores](systems/actors_ai_npcs.md),[runtime](systems/runtime_and_lifecycle.md) | Perfil propio,instancias y callbacks tienen vidas distintas. Un ID/request no es puntero vivo ni creación completada. unregister puede fallar;el teardown del loader no acredita unload seguro con instancias pendientes. StageService edita registros de carga, no sustituye ActorService. |
| Presentar texto | UiService para UIhost (CALLBACK-032..034/047..049);[HUD/J2D/BMG](systems/hud_ui_text.md),PRES-036..039/056..059/068..073;Message/Flow para sus contratos de resolución/grafos | UIhost Rml,panes del HUD,texto localizado y eventos son mecanismos distintos. No hay garantía de fuente/glifos/refresh ni tags TBX2 de assets por localizar la clase. Un callback de mensaje no es API genérica de draw J2D. |
| Registrar un callback | [Ownership/cancelación](systems/callback_ownership_and_cancellation.md),CALLBACK-001..003/009/023..026 | Save copia records;Host/Camera reconsultan handles;Http despacha resultados en frameBegin. Elegir la regla del servicio concreto. Retirada no demuestra callback drenado,user_data vivo o DLL descargable. Payload prestado se copia si debe sobrevivir la llamada. |
| Guardar datos propios | SaveService,[save/load](systems/save_load.md),WORLD-011/012/034..037 | set_blob copia y marca dirty;observer de guardado vanilla precede flush sidecar. Sin transacción conjunta ni durabilidad confirmada. Conservar esquema/slot/errores;no confundir con editar el save vanilla. FileService close consume handle incluso ante error (SDK-027/028). |
| Obtener o reemplazar un recurso | ResourceService o asset overlay según ruta;[recursos](systems/resources_archives_overlays.md),PRES-001..006/018/065..067 | ResourceService lee res/ propio y registra allocation. Un overlay se aplica a lecturas futuras y no reconstruye caches/instancias vivas. Datos del ARC,modelo,animador y trabajo de draw no comparten automáticamente dueño ni fin de vida. |

## Modelos, animación y texto: decisión por propiedad

Partir del consumidor y formato real. Las cadenas morf/BCK/BTK,skin,BTP/BRK/BPK,BLS/BLK,packets y film están en [modelos/materiales](systems/models_animations_materials.md);no constituyen un cargador universal ni demuestran LOD/BVA o DX12. La tabla resume muestras concretas, no destructores universales.

| Objeto / respaldo | Relación observada y evidencia | Retirada / condición que falta comprobar |
| --- | --- | --- |
| Buffer ResourceService | Copia malloc registrada al mod;PRES-001 | free requiere allocation propia,detach reclama esa lista. Eso no describe ownership de un archive vanilla ni consumidores externos del buffer. |
| ARC y recursos decodificados | Phase/archive/refcount en la cadena específica;PRES-044/047 y ficha de recursos | resDelete condicionado al estado de fase,no certifica destrucción de todo consumidor ni éxito interno propagado. Un overlay retirado no invalida por sí solo recursos cacheados. |
| J3DModelData frente a J3DModel | Modelo retiene ModelData y tiene buffers propios;PRES-044. Skin puede modificar arrays de ModelData en fast-path;PRES-102..105 | Instancia separada no implica datos aislados. Mantener backing/heap vivo y comprobar sharing/flags de la muestra. No usar sizeof histórico como layout Windows. |
| Animador BCK/BTK y material | Wrappers retienen punteros;setAnm puede fallar después de mutar parte;entry/remove cambia binding;PRES-045/046 | Desligar material no descarga ARC ni restaura cualquier estado anterior. BPK slot0 también tiene reglas específicas (PRES-158/159). No asumir transacción entre animadores. |
| Packet/lista de draw | Packet prestado conserva modelo/joint/material hasta draw;PRES-151..153 | Reset de buckets no libera packet ni prueba GPU idle. Almacén y backing deben sobrevivir al consumo;el cleanup del ejemplo no acredita drenaje universal. |
| BFN/font compartida/pane | Fuente puede referenciar backing BFN;getter cuenta referencia global y setFont presta sin sumar otra;PRES-036..039 | File-info destruye pantalla antes de soltar su referencia. No liberar fuente ajena ni backing mientras tablas/panes lo usan. Rama japonesa JUTCacheFont no se equipara a JUTResFont. |
| TextBoxEx/material/string | Material/font prestados desde screen;texto tiene buffer propio;PRES-056..059 | Ownership depende de constructor/TevBlock concreto. Retorno de setString no confirma allocation ni render. No todas las variantes de material/charset fueron auditadas. |

KYTAG09 (PRES-160/161) es film gráfico con selección por progreso;no escritor general de clima pese al nombre KYTAG. La iluminación que consume no lo convierte en política ambiental. Las otras etiquetas ambientales se consultan en su ficha y no heredan esta clasificación.

## Soporte del port: contrato oficial, host interno y frontera externa

| Familia | Ruta de consulta | Frontera útil |
| --- | --- | --- |
| UI,config,archivos,ventanas y red SDK | [Servicios](SDK_AND_SERVICES.md),[callbacks](systems/callback_ownership_and_cancellation.md),SDK-027/028 | Contratos propios con límites,versiones y handles. ConfigService no expone por analogía todas las CVars host;UiService no controla cualquier documento interno. Backend disponible no garantiza operación exitosa. No se hizo tráfico de prueba. |
| Logros y señales | [Logros internos](systems/port_achievements.md),PORT-001..005 | No AchievementService público auditado. Señal,RAM y JSON tienen gates distintos;no logros generados en esta campaña. |
| Presencia / speedrun | [Presencia](systems/port_presence.md),PORT-010..013;[LiveSplit](systems/port_speedrun_livesplit.md),PORT-006..009 | Interfaz interna/capacidad de compilación,no PresenceService/LiveSplitService acreditado. Contador nominal no mide FPS/GPU;ninguna conexión ni ACK observados. |
| Comandos y diagnóstico de disco | [Consola](systems/port_commands.md),PORT-014..017;[diagnóstico](systems/port_disc_validation.md),PORT-018..021 | Consumidores host reales, no autorización para ejecutar comandos o inspeccionar discos personales. Task done y progreso distintos;cancelación/backend precisan evidencia propia. |
| Logging y controller | [Runtime](systems/runtime_and_lifecycle.md),PORT-026..028 y [stub/console](systems/port_commands.md),PORT-029..031;[controles](systems/player_and_controls.md),PORT-032..034 | Ring/UIcopian texto según ruta;stub puede omitir líneas aunque callback retorne true. Asignación,captura cancelada y configuración durable no son equivalentes. No se abrieron logs/config ni dispositivos personales. |
| Aurora/Borealis/cosmetics/randomizer | [SOURCE_PIN](SOURCE_PIN.md),[ABI](HOOKING_AND_ABI.md),[memoria](systems/memory_ownership.md) | Cuatro gitlinks ausentes:BLOCKED_BY_EXTERNAL_SOURCE para sus internals. No inferir DX12,IO,workerdrain ni DLL/layout. Un futuro análisis requiere fuente exacta o evidencia binaria autorizada, no instalar dependencias para cerrar esta guía. |

## Mantenimiento después de la primera versión

Leer [CONTINUATION](CONTINUATION.md) y HEAD remoto antes de editar. Una nueva necesidad abre una pregunta pequeña:contrato→implementación→consumidor→error/cleanup. Si ya existe,precisar su límite en vez de duplicar IDs. Corregir contradicciones conservando ID y rastro del ajuste,como [CP-R96](AUDIT_FINDINGS.md).

Mantener READ/INVENTARIED donde corresponda. 25 contratos,26 candidatos,209 slots localizados,452 símbolos y cobertura selectiva no equivalen a implementaciones exhaustivamente auditadas o hooks disponibles. Cuatro backends ausentes,Android excepcional y0 runtime/ABI/exports medidos son límites permanentes de esta versión.

Validar con la herramienta protegida y fuente certificada;no modificarla para aprobar. Revisar diff solo DUSKLIGHT_RESEARCH/,HEAD/parent/tree,lease sin force y readback remoto. Ver [AGENTS](AGENTS.md). No implementar mods,ejecutar builds/juego/red ni integrar con Claude. Esta guía no altera permisos ni prepara otra plataforma de consumo. No trabajo en segundo plano.
