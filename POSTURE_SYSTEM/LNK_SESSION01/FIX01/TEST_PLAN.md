# Verificación de SESSION01 FIX01

Toda prueba de C++ es **LAB_MODEL_ONLY**. No se ejecutó el juego ni se cargó la DLL. La observación del usuario de fallos en 0.10.0 prevalece sobre sus laboratorios positivos. Los logs completos nuevos no están disponibles localmente.

## Regresiones conservadas

| Laboratorio | Base 0.10.0 | FIX01 local |
|---|---:|---:|
| hit_lab | 1660 | 1660 |
| lifecycle_lab | 29558 | 29558 |
| collider_lab | 12826 | 12826 |
| posture_lab | 556878 | 556878 |
| reaction_lab | 36933 | 36933 |
| compat_lab | 55991 | 55992 |
| rb_lab | 21313 | 21313 |
| general_lab | 5560 | 5560 |
| break_lab | 243624 | 243624 |
| hud_lab | 57742 | 57742 |
| parry_lab | 1570 | 1570 |
| lnk_lab | 528 | 528 |
| lnks1_lab | 178 | 178 |
| fix01_lab | — | 21570 |

Sin reducción de casos. `compat_lab` añade una comprobación por el nuevo motivo de seguridad (39 nombres en vez de 38); las otras modificaciones heredadas solo actualizan la versión esperada y la aridad de ese enum. Se mantienen expectativas de comportamiento. ASAN+UBSAN en g++, con LeakSanitizer desactivado por la restricción de ptrace del entorno; binarios `-no-pie`. MSVC se ejecuta en CI sobre los mismos archivos del ledger, sin mezclar su evidencia con ejecuciones anteriores.

Base: 194/194 mutaciones. FIX01 añade 42 (35 de lógica y siete de fuente): 236 en total. Las nuevas reintroducen atribución tardía, tick incorrecto, fuente ajena, lectura sin resolución ambiental, daño eléctrico, falta de pérdida efectiva, chip como directo, generación ignorada, contacto obsoleto, ambigüedad, clip en bucle, ritmo inválido, animación cambiada, continuación sin prueba, monitor ciego tras armados históricos, muerte como recuperación, falso armado, salida sin terminación nativa y expiración como PASS.

La auditoría del materializador tiene cinco casos válidos (incluidos los bytes reales observados de MSVC) y diez rechazos estáticos. El auditor PE conserva los negativos heredados y añade cinco para los dos registros extendidos: tamaño, puntero nulo, código arbitrario, flags y nombre de objetivo. Ninguna de estas pruebas ejecuta un materializador o una DLL.

## Matriz LNK02

| Escenario solicitado | Evidencia de modelo/fuente | Comprobación humana |
|---|---|---|
| Directo Blue/Red/Black/furia | Unión nativa + pesos 30/35/40/45 | Cada variante por separado |
| Blue grupo / Blue legado / Unknown | Pesos y firmas por generación; grupo +5 | Variante/grupo reales |
| Vida perdida y atacante correcto | Primer Tg del consumidor + esfera exacta + timer y delta de vida | HP/barra/log |
| Falta de atribución | Sin recibo/fuente distinta → cero crédito | Daño de fuente no admitida |
| Daño ambiental, caída, lava | Rama nativa de polígono no cero o sin consumidor verificado → rechazo | Entorno sin crédito |
| Invulnerabilidad | Timer PRE no cero → recibo rechazado | Golpes sucesivos durante i-frames |
| Magic Armor | Sin delta efectivo → rechazo | Configuración real de armadura |
| Dos atacantes | Solo collider elegido por el consumidor; recibos ambiguos rechazados | Grupo mixto |
| Duplicados y obsoletos | Token, frescura FIX02, recibo usado y tick exacto | Repetición de contactos |
| Desfase de ticks | Dos órdenes de actores; tick ajeno o tardío rechazado | Validación del orden real |
| Primer cilindro ocupado por otro | No se roba la atribución de un cilindro posterior | Contactos simultáneos |
| Reciclaje / Link reemplazada | slot+id+generación y Link ID vigentes | Cambio de sala/recreación |
| Muerte de Link / evento | Estado inválido/simulación inactiva → cero crédito | Muerte/cinemática |
| Parry, bloqueo y shield chip | Excluidos de candidatos directos | Parry +0 Link, bloqueo único |
| Daño efectivo cero | No flanco/delta → cero postura | Golpe sin pérdida efectiva |
| Recuperación/HUD | Mismo contador, demora y barra heredada | Aspecto, posición y controles |

El caso reproducible del defecto original hace que Link consuma el Tg, arme invulnerabilidad y limpie el registro antes del callback del Bokoblin: la lectura antigua rechaza el contacto; la nueva unión lo atribuye y acredita una sola vez. No es una mera prueba que fija `tg_match=true`.

## Reproductor de registro At y ruptura por espada

El Breaker real recibe un golpe de espada cruzando 100 durante ATTACK: produce Stun inmediato. Modelo de las ramas nativas Set/ClrAtHitInf/ChkAtTg/executeAttack: esfera apagada no se registra, conserva AtHit y rebota antes del frame 14 con guardia; ruta corregida registra para limpieza y restituye Off, sin colisión adicional. Cobertura de cinco familias, cinco ritmos y grupos 1/2/4/8; conservación de todas las combinaciones de bits nativos, uno/dos contactos, mezcla de peticiones, duplicados, identidad/generación/tick erróneos, falta de frescura/ataque, limpieza fallida, falta de cc_set y expiración inconclusa. Siete nuevas mutaciones de lógica y una de fuente verifican estas barreras.

En juego, buscar también `LNK_S1_FIX01_AI_CLEANUP`: requested/leased/paired/next_tick_clear_verified/failed/expired_inconclusive. `paired` solo prueba restitución del bit; la limpieza efectiva requiere `next_tick_clear_verified`. La recuperación ofensiva exige además el monitor de ciclo nativo. Ningún contador aislado equivale a HUMAN_PASS.

## Matriz de IA y compatibilidad

| Escenario solicitado | Cobertura real disponible | Límite pendiente |
|---|---|---|
| Blue con guardia mantenida | Ciclo nativo modelado con armado y rebote inverso; terminal verificado | Pelea real |
| Varios golpes sub-100 / Shield repetidos | Gate de restauración en el proceso real; familias y retrasos heredados | Cronología real con hits repetidos |
| Alternar defensa, ataque y golpes | Regresiones POST05/POST08 y cancelaciones modeladas | Entrada del jugador y colisiones |
| Grupo x1.15/x1.30 | Ciclos modelados a 1/1.15/1.30/2, sin escribir ritmos | Cambios de grupo en juego |
| Compañeros entran/salen, reclutamiento | Fuente CP21 revisada, sin modificación de políticas | No se simula una IA completa de reclutamiento |
| Interrupciones consecutivas | Abortos legítimos separados de rachas sin progreso | Contexto de obstáculos y evasión |
| Red / Black / furia / legado | Mismo gate probado para todas las firmas; regresiones RB | Habilidades y velocidad en juego |
| Ataques acelerados | Forma de clip y ritmo coherentes; variantes de modelo | Contactos a ritmos reales |
| Antes/después de ruptura | break_lab heredado; observación tras ruptura/parry/supresión | Stun, Helm, Finish y levantamiento |
| Grupos 2/4/8, generaciones | Ciclos simultáneos y reciclaje sin herencia | Escenas reales |
| Cancelación legítima | Daño/KO/evento/objetivo inválido no prueba atasco | Todas las rutas nativas no modeladas |
| Abortos repetidos tras armados antiguos | Racha reciente detectada aunque exista historial de armado | Confirmación visual de la anomalía |
| Animación reiniciada sin progreso | Detector de reinicios/alternancias, sin escritura correctora | Causa real del reinicio |
| Ataque armado pero cancelado | No se declara recuperación sin rama terminal nativa | Salida real del ciclo |
| Terminal sin armado | Tampoco se declara recuperación | Armado/colisión en pantalla |
| Actor muere antes de verificar | Resultado de muerte distinto y anomalía retenida | Actor humano observado |
| Escena/actor que deja de ejecutar | Expiración inconclusa, nunca PASS | Carga real de salas |
| Espera legítima / Link inválida | Distancia, target, evento, KO y timers | Geometría, guion y reclutamiento |

Ningún número de laboratorio demuestra que el episodio del actor 222 haya quedado eliminado dentro del juego. Sí demuestra que las restauraciones inseguras modeladas se rechazan y que las anomalías que el monitor anterior podía ignorar ahora tienen categorías y contadores propios. No hay condición especial para ese actor.

| Mod | Revisión de integración | Estado jugable |
|---|---|---|
| Enemy Posture System 0.10.1 | Un contador y paquete acumulativo; ID fijo | HUMAN_RUNTIME_PENDING |
| EVF 0.15 | Servicio existente; sin dependencia nueva | HUMAN_RUNTIME_PENDING |
| Bokoblin Expansion 0.17 | CP21 exacto revisado; ritmos, grupo, reclutamiento, furia y habilidades sin modificar | HUMAN_RUNTIME_PENDING |
| Enemy Health Bars CP06 | Escritores/HUD heredados intactos | HUMAN_RUNTIME_PENDING |
| Enemy Health Multiplier CP11 x2 | Daño de vida nativo intacto; no multiplicador nuevo | HUMAN_RUNTIME_PENDING |
| Zora Swim 1.3 | Sin cambios de código/binario ni nuevas escrituras compartidas | HUMAN_RUNTIME_PENDING |
| Luau Support 1.0 | Sin dependencia ni scripts nuevos | HUMAN_RUNTIME_PENDING |
| Randomizer 1.0.6 | Sin cambios a flags, saves, aprendizaje o equipo | HUMAN_RUNTIME_PENDING |

## Prueba humana de aceptación

Con el juego cerrado, guardar 0.10.0 para comparación y retirar su copia activa. Instalar solo 0.10.1 del mismo ID. Rollback principal: LNK01 0.9.0. No usar 0.8.1.

1. Con los ocho mods, recibir un directo de Blue, Red y Black por separado, empezando con postura recuperada; revisar HP nativo y subida 30/35/40.
2. Repetir con Black en furia (+45), y Blue con ajuste de grupo demostrado (+5).
3. Recibir otro golpe durante invulnerabilidad: sin crédito directo extra si no hay pérdida efectiva.
4. Bloquear y hacer parry perfecto: pesos de bloqueo conservados; parry +40 enemigo/+0 Link; furia sigue no parryable y chip sin duplicación.
5. Mantener guardia y golpear varias veces al Blue bajo 100, incluyendo Shield Attack. Observar que vuelve a una ruta ofensiva y completa ataques; una animación que arranca y se cancela no basta.
6. Repetir con Red, Black y furia, y con compañeros que entran/salen.
7. Probar grupos mixtos de 2, 4 y 8 cuando la escena lo permita, incluyendo reclutamiento de Blue.
8. Completar ruptura enemiga, castigo único, Helm, Finish y levantamiento; revisar rearme y siguiente ciclo.
9. Intercalar golpes de espada que crucen100 mientras el Bokoblin está golpeando el escudo; mantener después la guardia y esperar ataques completos. Correlacionar limpieza del contacto, fin del stun y un ciclo ofensivo realmente armado.
10. Comprobar recuperación de Link por vida/guardia, pausa/menú, HUD inferior, controles y barras enemigas.
11. Enviar por chat el **log completo de la sesión**, indicar enemigo, arma, secuencia y momento del fallo, y vídeo breve si es posible. No subir logs personales a GitHub.

Revisar `LNK_S1_FIX01_INIT`; `LNK_S1_FIX01_DIRECT` debe mostrar fuente nativa y tick coincidentes, seguido por `LNK_S1_DIRECT event=CONFIRMED_DIRECT_HIT` con el peso y el antes/después del contador. `LNK_S1_SUMMARY` debe tener directos confirmados por variante y conservación 1. `LNK_S1_FIX01_AI` distingue recuperación completa de muerte/expiración/sospecha. `LNK_S1_FIX01_SUMMARY` conserva totales de exclusiones, armados reales, ciclos completos, abortos, cancelaciones, anomalías pendientes y mensajes limitados. Correlacionar con `POST05_DECISION`, `POST08_EVENT`, `POST08_AI_TRACE`, `POST06_EVENT` y los logs de Expansion.

**STOP/rollback:** crash, `ok=0`, conservación 0, crédito doble o ambiental, pérdida de HP alterada, parry roto, IA que repite ataques sin progreso, animación congelada, habilidades de variantes perdidas, ruptura/Finish/rearme incorrectos o caída marcada de FPS. Conservar el log completo y volver a 0.9.0 con el juego cerrado. Ningún cambio de ROM, EXE o save es parte de esta prueba.
