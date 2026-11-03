# Enemy Posture System CP02+CP03 — 0.11.6 PRIVATE TEST

Ambos checkpoints se implementan en un único mod acumulativo. Base compilada obligatoria: `2d0e59329f14d822c1905ee7953d337959932f1f`. El descendiente documental `3202a09bd5af89a58789e33921985279d89bce62` se consultó sin atribuirle el binario anterior. El encargo actual confirma que el usuario probó 0.11.5 con ocho mods y «Todo funcionó perfectamente». Esa aprobación pertenece a 0.11.5;0.11.6 permanece HUMAN_RUNTIME_PENDING.

## CP02: cambio de regeneración, no de HP

| Vida restante respecto al máximo observado válido | Antes | Candidato |
|---|---:|---:|
| HP >75% | 5/s | 10/s |
| 50% < HP ≤75% | 4/s | 7/s |
| 25% < HP ≤50% | 3/s | 4/s |
| 10% < HP ≤25% | 2/s | 2/s |
| 0% < HP ≤10% | 1/s | 1/s |
| HP/max inválido o slot sin máximo válido | fallback 5/s | fallback 5/s conservado |

`post06::policy::regen_rate_for` conserva comparaciones estrictas y productos `long long`. Los bordes 75/50/25/10 producen 7/4/2/1 respectivamente. `Breaker::step` mantiene exactamente la observación de máximos de pre_hp/native_hp por id/generación; ni daño ni cambio de banda reducen ese máximo, y una generación nueva lo reinicia.

**Límite conocido:** OBSERVED_MAX_THIS_GENERATION es el mayor HP visto, un límite inferior del máximo verdadero. Un actor observado por primera vez con 50 HP se clasifica inicialmente al 100% del máximo observado 50, aunque su máximo verdadero pudiera ser 100. No se inventó un máximo, no se leyó memoria privada de otro mod ni se sustituyó esta política por una API distinta. El fallback inválido permanece 5, las identidades inseguras siguen congeladas y la telemetría declara `OBSERVED_LOWER_BOUND_NOT_TRUE_MAX`. La prueba cubre ese caso y la elevación posterior del máximo observado al curarse. La fidelidad al porcentaje verdadero requiere observar a la instancia con su máximo real; no se certifica donde ese dato falta.

`post04::policy::kRecoverDelayTicks` pasa de 120 a 60 ticks **elegibles**, a reloj nominal 30 Hz. `set_regen_rate` y el clamp dentro de `advance` admiten 1..10; ambos eran 1..5. Se mantiene el acumulador entero: +rate créditos/tick después de los 60; cada 30 créditos descuenta un punto. El resto sobrevive al cambiar de banda y se reinicia con golpe/parry válido según la política anterior. Con rate 10, el primer decremento ocurre en el tick 63; con 7 en 65; con 4 en 68; con 2 en 75; con 1 en 90. El tick 60 todavía no acumula recuperación. `kRecoverPeriodTicks=6` se conserva y se identifica como período del **fallback 5**, no como cadencia de todas las tasas.

El acumulador uint 8 permanece seguro: antes de sumar contiene 0..29 y la suma máxima es 39. Un assert comprueba el rango y que la tasa máxima es menor que 30; sigue bastando un decremento por tick. No se usa tiempo de presentación/interpolación ni coma flotante para regenerar.

Se audita la ruta real completa: `mod_update → do_update → PostureEngine::on_update → Posture::advance`; la tasa se selecciona en `post06_step → Breaker::regen_rate → set_regen_rate`. El SDK oficial ejecuta `ModLoader::tick` desde `duskExecute/fapGm_Execute`, antes de `fpcM_Management`, no desde el callback de presentación. Se reutiliza **solo en lectura** `lg.sim_active`, ya calculado por `lnk01_update` con identidad válida, vida de Link positiva, sin pausa/evento/menú. `on_update(false)` sincroniza el ledger pero no avanza el reloj numérico; el barrido y el orden de llamadas de Link se conservan. No se altera el algoritmo ni las constantes de Link.

Se conservan los descartes por muerte, generación caducada, admisión insegura, golpe letal, familia de peso 0, reporte duplicado y latch 100. Un golpe rechazado no reinicia la demora; un golpe ponderado o parry confirmado sí. Durante el ciclo de ruptura el latch impide recuperación; rearme 25/0 inicia la demora nueva. La máquina nativa de stun/caída/levantamiento/Finish no cambia.

## CP03: precisión y recompensas separadas

Solo cambian `kWindowFrames:9→7` y `kWindowTicksCap:11→9`. El slack anterior permanece 1: **delta[-1,+7] y edad≤9 simultáneamente**. Es una condición del contacto bloqueado en la pasada correcta, no invulnerabilidad ni una modificación de la animación. Snapshot, cilindros Tg, esferas At armadas, token, generación, STALE_CONTACT, duplicados y orden FIX02 permanecen iguales. Red y Black normal conservan sus reglas; la posibilidad de chip de Black Fury sigue rechazando el parry.

Un contacto fuera de la nueva ventana deja de recibir crédito de parry y sigue su resultado nativo. Si ese resultado era un bloqueo válido, el sistema de postura de Link aplica su regla de bloqueo ya existente. No se añadió un coste de parry, castigo artificial, HP, cooldown, nueva animación o estado. Parry confirmado sigue costando 0 a Link.

Las ganancias por parry permanecen Blue 40/Red 27/Black 20, y los pesos de espada/iron ball siguen 25/50,17/33,13/25. Sin regeneración entre contactos, hacen falta 3/4/5 parries desde 0 para alcanzar 100; desde el rearme de pie 25,2/3/4. Esta comparación cuantifica las recompensas sin aplicarlas de nuevo ni aumentarlas para compensar la ventana más estricta. El balance percibido depende de la cadencia real y requiere la prueba humana.

## Evaluación sin aplicar: decisivo y propuesta 5–8

El bonus sigue siendo `extra=(base+1)/2`, aplicado una vez a un contacto decisivo verificado: por ejemplo, base 13 añade 7, pérdida total 20; base 40 añade 20, total 60; base 100 añade 50, total 150. El redondeo hace que pérdidas impares pequeñas superen ligeramente 1,5; base 1 produce 2. Eso ya existía y no se modifica.

Las observaciones numéricas anteriores, saneadas y enlazadas por generación, muestran Blue 40+20=60, Red 40+20=60 y Black 100+50=150 en el log humano 0.11.4. No son daños universales de cada variante ni evidencia de ejecución 0.11.6. El cuerpo de `post06_bonus` y la máquina de oportunidad/commit se conservan desde 0.11.5. Los laboratorios recorren bases 1..150 con espada/Helm y verifican bonus único, rearme, muerte/Finish, contacto no decisivo y caducidad. Pasar a×2 añadiría aproximadamente otro 50% del daño base a ese golpe y alteraría umbrales letales: **evaluado, no aplicado**. No se considera probado que×1,5 sea el balance definitivo; se conserva para comparar exclusivamente CP02/CP03.

La propuesta de 5–8 puntos para Link no define evento, signo ni unidades. Añadirlos al parry confirmado, hoy 0, castigaría una acción más exigente y cambiaría guard-break/regen; podría evaluarse como política separada con una definición y autorización futuras. **No aprobada, no aplicada.** Ningún campo ni constante de los núcleos de Link cambió.

## Auditorías y congelación granular

El archivo original `ci/baseline_0_11_2_barrier.json` permanece intacto. `ci/cp0203_policy.json` registra hashes antes/después y justificación exacta de 2 funciones (`post06_step`: diagnóstico; `do_update`: elegibilidad de regen) y 3 encabezados (`posture_core`, `break_core`, `parry_core`). Los demás 105 cuerpos conservan su pin original. De 15 encabezados auditados,3 tienen cambios CP; lifecycle solo cambia la cadena de versión mediante la normalización acotada existente; los otros 11 son idénticos. Ninguna exención de escritor nativo se amplía.

La auditoría adicional compara byte por byte 27.883 bytes de HUD FIX03/leases,59.566 de Link/contactos nativos y 42.684 de alineación/presentación. También se conservan los inventarios CP06, hudfix_core, alignment_core, los pines FIX03, SDK, imports y targets. El PE esperado sigue en 22 hooks (14 compactos+8 extendidos),55 imports de juego y 7 contratos; no hay nuevas entradas nativas ni servicios obligatorios.

## Pruebas y alcance

Los 19 laboratorios compilan los núcleos reales. El nuevo CP0203 usa una referencia de tokens independiente por tick, fronteras racionales alternativas, secuencias largas, restos al cambiar tasa, pausa, conservación, cero/latch/muerte, generaciones, múltiples máximos y matrices frame/edad/variante. Las pruebas heredadas mantienen sus escenarios: solo se actualizan expectativas de las políticas autorizadas. En el estrés de reacción se añadió el reloj independiente que faltaba al reducir la demora; el trace humano original no se edita y se proyecta con la política nueva. Su fila 505/event 14 pasa de 43 histórico a 33 previsto por el nuevo retardo, no se presenta como una observación humana nueva.

`test_cp0203_adapter.py` extrae y compila los cuerpos reales de `post06_step` y `do_update`, integrados con PostureEngine/Breaker reales y E/S nativa modelada; comprueba tasas desde la ruta de producción,8 enemigos simultáneos, pausa, Red curándose, generación caducada y presentación 30/60 sin avance extra. Las escrituras nativas se modelan: no es ejecución del juego.

`test_cp0203_reference.py` usa `fractions.Fraction` como referencia independiente; compila también los 3 encabezados auténticos de la base 0.11.5, preservados con SHA-256. Ambos ejecutables modelo deben compilar y correr: el anterior incumple las expectativas nuevas y el actual coincide. Un error de compilación no cuenta como detección. Las 22 mutaciones nuevas verifican ambos clamps, tabla, fronteras, demora/remainders, ventana, generación, ruta real de tasa/pausa y cambios prohibidos de pesos, Link o bonus. Se repiten las 412 mutaciones heredadas y los negativos, sin admitir TIMEOUT como PASS.

CI, PE, descargas, conteos finales y correlación exacta fuente/binario constan en RESULTS.json y EVIDENCE. No se ejecuta Dusklight ni se carga la DLL. Ni los modelos 30/60 ni la aprobación humana 0.11.5 certifican el nuevo binario DX12. Las pruebas A y B están pendientes; HUD regresivo es bloqueante.

## Muestra del formateador y procedencia del candidato

El primer run `41700811384`, fuente `e8050042c4e0ad012a2eb563b0af08aaae02bd9a`, pasó MSVC, PE, los 19 labs y 434 mutaciones; el gate final rechazó correctamente la muestra sintética comprometida, que todavía correspondía al retardo anterior. No publicó un paquete TEST. La salida real de GCC y la salida de MSVC son idénticas tras normalizar LF: SHA-256 `73ebb848f2c62fe27745e4fd9ed0ba5c8cbb75e5f2dacc139041ab7776b2707a`.

El commit `8c72aec291a7473f1752c702137229cc2224c998` actualiza exclusivamente `tests/data/sample_post04_formatter_output.log`:16 líneas sustituidas, sin cambios en src ni en gates. Los 12 tests de herramientas pasan con la muestra fresca, sin skip. Se repite el CI completo y se empaqueta desde ese commit nuevo; el resultado y artefacto finales se identifican en RESULTS.json.

GRANULAR_SOURCE_DIFF.json comprueba además que post 06_step solo cambia cadenas diagnósticas, do_update solo añade el argumento de elegibilidad, break_core solo cambia su tabla y parry_core solo cambia las dos constantes aprobadas. Las funciones de consumo, rearme, preview/apply_parry, sync_slot y close_run permanecen iguales. La inicialización actualiza los textos numéricos para reflejar las políticas nuevas.

## Resultado verificado del candidato

Fuente compilada `8c72aec291a7473f1752c702137229cc2224c998`, CI `505cd3fd053011e6dc7f78dfa73d7d039c57c23a`; run `41703645193` con build e independent-download SUCCESS. Ambos verificadores coinciden en ID, versión, nombre, bytes, SHA-256 y PE del artefacto publicado. MSVC14.51.36231 x 64, Windows SDK10.0.26100.0.

19 labs: 2,881,551 comprobaciones; CP0203 puro 52.432, adaptador de producción 4,325, referencia racional 2.908 casos por ejecutable (base con 2.694 discrepancias esperadas, actual 0), adaptador HUD67.218. Mutaciones 434/434 (412 heredadas +22 nuevas), cero timeout. Negativos semánticos 114 +12 HUD; PE20; instrucciones nativas 2. Los mismos 22 targets/55 imports de juego/7 contratos de servicio. El build del módulo emite 9 warnings de encabezados oficiales; líneas saneadas en MSVC_WARNINGS.json, sin editar el SDK para eliminarlos.

La aprobación humana de 0.11.5 no se atribuye a este binario. Estado final técnico: PRIVATE_TEST_CP02_CP03_TECHNICAL_IMPLEMENTED_HUMAN_RUNTIME_PENDING. No hubo PR, merge, tag, release, instalación ni cambio de los otros siete mods.
