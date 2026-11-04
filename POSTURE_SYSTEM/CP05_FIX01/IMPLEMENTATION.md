# Light Fades Twice — CP05 FIX01 / 0.11.9 PRIVATE TEST

Fuente compilada: `785f7044a09588ea9f570f09b4b74580e4f7ee93`. Base defectuosa: `e226415ebb4c5ad1d488898357072dc7c503a57d` (0.11.8, HUMAN_RUNTIME_REJECTED). Respaldo aprobado: CP04 `2d103c5562f7199b875d5c4c7de7f00a32922a61` (0.11.7). El commit documental que contiene este informe es posterior; no es la fuente del binario.

## Diagnóstico comprobado

El log humano completo tiene 35.532 líneas, 7.948.481 bytes y SHA-256 `7c6855428160a432544ebec12cf26d33e50835fc6240e3be718f7df9c0fd2242`. Se procesó entero, usando únicamente los resúmenes acumulativos SHUTDOWN para los totales. Los derivados publicados omiten rutas privadas; no se publica el log crudo.

| Patrón 0.11.8 | Seleccionados | Completados | Cancelados | NATIVE_PRIORITY |
| --- | ---: | ---: | ---: | ---: |
| Red4 | 82 | 0 | 82 | 70 |
| Black8 | 62 | 1 | 61 | 58 |
| Black7 | 53 | 0 | 53 | 51 |

Solo 1/197 completó. Las probabilidades no explican esta falta de continuidad: Red tuvo 138 oportunidades y 56 normales/82 Red4; Black 181 y 66 normales/62 Black8/53 Black7; sin sorteos duplicados o reentrantes registrados. No se cambió el RNG.

El presupuesto antiguo agotó 800 detalles y descartó 1.829. De los **61 NATIVE_PRIORITY con detalle disponible**, 43 preceden a un Shield Attack, 17 a una espada y uno corresponde a pasividad/especial Red confirmado por Expansion. No extrapolamos estas proporciones a los 179 totales. Entre esos 43 de escudo, **21 tienen POST08 COMMITTED_NATIVE posterior**, del mismo actor/generación, en las siguientes 14 líneas. El contador CP05 ya había cerrado el episodio y omitía esos parries. Esto explica un subconteo, no invalida los atravesamientos físicos reportados por el usuario.

Cronología real de la revisión SDK: `action` desactiva AT, ejecuta `damage_check` y su transacción POST05, llama Attack/Find, avanza la animación y ejecuta matrices/`cc_set`; después ocurre execute POST. 0.11.8 cancelaba ante Tg crudo en execute PRE, antes de saber si el contacto produjo daño/reacción o fue suprimido correctamente. Ejemplos verificables por número de línea del log:

- Red, cancelación 2322 → contacto nativo de escudo 2323 → supresión POST05 → parry POST08 confirmado 2330 (+27).
- Black7: cancelación 7849; Black8: 8025; ambas preceden al contacto/supresión.
- Espada con daño en 2894–2895 y prioridad Red legítima en 2226: deben seguir cancelando.

`EVIDENCE/HUMAN_0_11_8_ANALYSIS.json` conserva los contadores y las correlaciones limitadas por actor/generación/combo.

Los demás diagnósticos del log se contaron por separado: 187 líneas ERROR son DEVF_CP12 PERF_WINDOW; 5.056 WARNING se reparten en 199 avisos mip, uno LNK01_INIT, uno de hook inlined y 4.855 CalcDivideInfo. No se atribuyen causalmente a CP05 ni se modifican esos sistemas. No aparecen tokens FATAL, Unhandled exception o access violation; esto no demuestra ausencia universal de fallos. El detalle está en `EVIDENCE/LOG_DIAGNOSTIC_CATEGORIES.json`.

## Corrección de continuidad y propiedad

Solo se cambian los dos módulos CP05 de producción y la versión global. Los callbacks esperan la resolución nativa/POST05: pérdida real de HP, un nuevo reporte ponderado confirmado de nuestro slot/generación, o un modo nativo prioritario cancelan. Un Shield Attack de peso cero suprimido y con continuación nativa válida ya no cancela por la mera presencia previa de Tg. El reporte requiere evento nuevo, generación correcta, applied y weight>0; un reporte antiguo, no confirmado o de otro actor no sirve.

Find0/1/2/3 conserva su recuperación; Find4 permite un lease de timer de 16 bits con comparación. El valor temporal 2 permite el decremento nativo a 1 y se restaura al valor nativo decrementado **antes de Expansion POST**, únicamente si modo/state/valor siguen siendo nuestros. Si el motor cambia el modo, su timer gana incluso si también vale 1. Un cambio externo entre ejecuciones se detecta antes de tomar el lease. La continuación Attack0 se publica en POST para que Expansion PRE de la ejecución siguiente vea su entrada y valide su propio recibo de arranque.

La admisión exige un PRE de la misma ejecución, E_OC2 clasificado, generación/contexto válidos, dos perfiles ATP normales auténticos y B/C recién iniciado: frame 1/rate1 temprano seguido de frame 1/rate1.15 normal tras Expansion. No se adquiere propiedad a mitad de una llamada recién reenlazada. Una cancelación impide volver a sortear en esa misma ejecución. Sin el protocolo exacto de Expansion no se fuerzan estos combos: degradación segura conservando el comportamiento previo. El protocolo observable 0.17.0 no es una API privada que autentique criptográficamente a un escritor desconocido.

El clip completo, su duración leída realmente y el recoil nativo negativo siguen siendo autoritativos. El log antiguo sí contiene 44 arranques BCK5 con end 42 y 37 BCK6 con end 47: los fixtures 42/47 coinciden con esas lecturas disponibles. Esto no proporciona las poses articulares originales ni certifica otros assets. No se recorta una animación para cumplir un plazo ni se fuerza un golpe tras postura100, muerte, agua, daño prioritario, escena, furia o especial Red. No se restauran modos antiguos después de una prioridad.

## Ritmos y velocidades por posición

Los números son plazos entre **aperturas AT**, en ticks del actor (30Hz como referencia), no tiempos garantizados de contacto. La recuperación, duración real de B/C y frenado nativo pueden extenderlos. Se mide el exceso; nunca se inventa una ventana.

| Patrón | Estructura | Tasa por swing | AT objetivo, ticks | Referencia segundos a 30Hz |
| --- | --- | --- | --- | --- |
| Red4 | 1—2-3—4 | 1 / 1.15 / 1.15 / 1 | 68 / 46 / 72 | 2.27 / 1.53 / 2.40 |
| Black8 | 1—2—3-4-5-6-7—8 | 1 / 1 / 1.15 / 1.15 / 1.15 / 1.15 / 1.15 / 1 | 65 / 67 / 46 / 46 / 46 / 46 / 70 | 2.17 / 2.23 / 1.53 / 1.53 / 1.53 / 1.53 / 2.33 |
| Black7 | 1-2—3—4–5–6–7 | 1.15 / 1.15 / 1 / 1 / 1 / 1 / 1 | 46 / 68 / 70 / 56 / 56 / 56 | 1.53 / 2.27 / 2.33 / 1.87 / 1.87 / 1.87 |

Referencias temporales del encargo, sin análisis de audio nuevo: Red `[0.694,1.893,2.133,3.452]` s; Black8 `[0.777,1.662,2.639,2.898,3.150,3.391,3.651,4.522]` s; Black7 `[0.873,1.126,2.169,3.224,3.704,4.197,4.677]` s. Sus ráfagas de0.24–0.26s no se reproducen literalmente a costa de perder muestras o recortar los clips nativos E_OC2. El tramo rápido de46 ticks respeta esos clips al máximo normal1.15; los tramos separados se compactan a65–72 y el cierre Black7 a56.

No hay una escala uniforme aplicada al audio: se comprimen especialmente sus separaciones largas y se ralentizan sus ráfagas para conservar clips, contactos y tiempo de repetición del escudo. No se dispuso de archivos m4a montados en esta sesión; se usaron las marcas temporales autorizadas del encargo. La fidelidad perceptiva queda HUMAN_RUNTIME_PENDING. Los arrays viejos 180/36/198, 134/147/39/38/36/39/131 y 38/156/159/72/74/72 se conservan solo como control histórico, no como programa activo.

La animación CP05 pasa de tasas uniformes 1.50/1.45 a tasas individuales 1 y 1.15. El inicio de la siguiente ventana usa la progresión real de frames de Attack: comprueba 14 antes de play, frame 1 POST recién iniciado, 14 ticks a tasa1 y 13 a 1.15. La programación descuenta ese retraso por swing y exige un margen mínimo tras el final real.

## Colisión, bloqueo y parry: alcance real

Se contrastaron Attack, Find, damage_check, SetActionMode, offTgSph, cc_set, colisión cilindro/esfera y la ruta ChkShieldFront/Shield de la revisión `40457c6adb381928e4b5fef6ed459ed291edd5e2`, además de las políticas exactas de Expansion 0.17.0. Las referencias están fijadas por hash y auditadas contra el SDK.

El especial Red tiene su propia política de barrido; no se atribuye automáticamente a B/C E_OC2 de CP05 acelerado. La ventana nativa muestreada ofrece 9 muestras a 1, 7 a 1.15 y 6 a 1.45/1.50 en el port de Attack usado. La reducción del máximo elimina esa aceleración añadida por CP05. Es una medida conservadora fundada en la fuente, **no una demostración de que todos los fallos visuales fueran causados por ese único factor**.

No se agrandan radios, no se escriben centros, AT/TG, frames, HP ni acciones de Link, ni se fabrican chispas/sonidos/parries. La telemetría solo lee centros/radios nativos, procedimiento Link, distancia, guardia, fase, frame/rate/end, modo/state/timer y flags. `engine_spark_event=NOT_OBSERVED` evita certificar efectos que el mod no observa.

El laboratorio geométrico ejecuta cuerpos nativos originales cc_set, cilindro/esfera y Shield; las matrices articulares y cilindros de Link son sintéticos. El laboratorio de continuidad ejecuta las callbacks completas de producción y los cuerpos nativos de daño/Attack/Find, y la transacción POST05 real; sus entradas SDK y colisión mundial están modeladas. Los ensayos de parry usan el juez real y tokens/seriales de escudo con I/O modelado. Ninguno ejecuta el juego, su DLL ni su renderer. No certifican trayectoria visual, dos movimientos físicos reales de escudo, chispa/sonido, FPS o coexistencia jugable de ocho mods.

## Guardia sostenida: causalidad delimitada

El antiguo programador añadía pausas largas que también se observaban sin depender de soltar R. El control del laboratorio compara nativo+Expansion, CP04+Expansion, CP05 viejo y FIX01, con R sostenido y liberado en tick 50. En Black8 el primer intervalo CP05 pasa de134 a65 ticks; en Black7 de38 a46, idéntico al mantener o soltar R en cada versión. Los controles sin CP05 conservan sus 31 ticks en ese escenario. Esto demuestra una demora propia del programa antiguo y ejercita su lease, no demuestra que toda espera de la partida proviniera de R o que el NPC deba atacar instantáneamente. Los detalles por fila se entregan en VALIDATION.json; la escena humana con rango/aggro/guardia reales sigue pendiente.

## Diagnóstico nuevo, acotado

Siete presupuestos independientes por clase de evento y actor; reserva adicional por submotivo crítico; resúmenes periódicos cada 1.800 ticks y SHUTDOWN completos, fuera de esos presupuestos. Las cancelaciones distinguen sitio PRE/AttackPRE/EARLYPOST/LATEPOST/contacto, causa, esperado/observado, HP comprometido, modo/state, timer, recoil, tasa/propietario, postura y contexto. Totales separados de cancelación legítima e inesperada. Histogramas de intervalo AT/contacto/gap posclip; lease adquirido/restaurado/cedido, ticks de gap con R y observaciones Tg diferidas. No se confunde blocked, parry elegible, rechazo y transacción confirmada. Los centros/radios pertenecen a la última captura de ejecución indicada por el sitio; no certifican por sí solos la pareja física en el instante de colisión.

## Preservación y límites

RNG bind/decide/reduce3 es idéntico byte a byte al de 0.11.8: Red normal/Red4 1/2 cada uno; Black normal/Black8/Black7 1/3 cada uno mediante rechazo imparcial uint64. Una oportunidad por actor/generación/contexto; sin sorteo por swing/frame.

Los 32 archivos previos de producción conservan sus hashes CP04 tras retirar únicamente las inserciones CP05 ya existentes y el cambio global de versión. Se mantienen las barreras de 107 funciones y 15 encabezados. Blue2+2, shieldchain físico aprobado, Link, HUD FIX03/alineación, Scoop, pesos, regeneración CP02 y ventana POST08 no se modifican. CP02 tasas10/7/4/2/1 y retraso60; POST08 [−1,+7], edad≤9; pesos Blue25/40/50, Red17/27/33, Black/Fury13/20/25; rearme 25/0; decisivo 1.5; penalización Link 75 ticks. Especial aleatorio Red×2 y BlackFury×2/chip y sus exclusiones de parry quedan intactos. Tampoco se corrige regeneración futura fuera de este checkpoint.

No se agregan targets de hooks; se usan las cuatro callbacks CP05 en los dos targets existentes. Los dos escritores CP05 conservan el float de velocidad y el lease16bit, con readback y ámbito auditado en el PE. Se reutiliza el escritor de modo nativo CP04 existente. No se modifica ningún otro mod, SDK, host, EXE, ROM o save; no hay PR, merge, tag ni release.

El resultado de MSVC, todos los laboratorios, mutaciones, negativos, imports PE y descarga independiente se incorpora desde los artefactos reales a `RESULTS.json` y `EVIDENCE/VALIDATION.json`. El estado jugable final de los tres patrones es **HUMAN_RUNTIME_PENDING**.
