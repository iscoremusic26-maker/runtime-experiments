# Enemy Posture System 0.11.2 — BALANCE SESSION01

Estado de mecánicas nuevas: SOURCE_IMPLEMENTED / LAB_MODEL_PASS; WINDOWS y ARTIFACT en RESULTS.json; HUMAN_RUNTIME_PENDING. Solo se modifican pesos normalizados enemigos y destinos de rearme de pie; el detalle numérico está en BALANCE_MATRIX.md.

## Base exacta y atribución humana

Código compilado 0.11.1: `8879ea08649eccee828798f3b6767e2cd655b48f`, árbol `14d115935e13f2296cc1e035e07aaf99b94ef6b3`. Se resolvió el cierre `2f77145edfd55a7a3596ad893e234b303ccf6aae`: su diferencia es exclusivamente documental. La rama nueva parte del commit compilado, conservando intacta la rama anterior. Worktree aislado y objetos Git originales comprobados por SHA. El paquete 0.11.1 fue descargado por artifact 13194926059: 109650 bytes, SHA-256 `8325dcf92d1ad7f39b330cef55713930d4dfce39c7baba27f64c8ec7d23e93ac`.

El usuario comunica validación jugable de defensa manual, R+B/parry, ruptura y vulnerabilidad prolongada de 0.11.1. No está disponible aquí el log completo `dusklight-20261102-195749.log`; sus cifras se atribuyen al encargo:60 parries, 21 rupturas por parry,0 write_failed;9 inicios/completados/rearmes de Link con 75 ticks; una sospecha de IA inconclusa. Solo SIDEHOP_DENIED tiene observación individual entre las cuatro esquivas. No se modifica el registro histórico PENDING ni se atribuye a Codex una sesión del juego.

## Identidad y política única

`balance_adapter.hpp::capture` recibe los valores ya leídos de POST03/05 y el MISMO `lg.posture.variants` de LNK07. Comprueba slot/id/generación, ledger activo/admisión candidata y epoch actual; exige NativeAux válido y recurso reconocido. Delega en `VariantTrack::classify`, sin segunda heurística. No recibe HP, no lee otro campo del juego, no añade un hook y no sigue punteros retenidos.

La procedencia está verificada contra CP21: el registro exacto de creación y el recurso se admiten primero en Expansion, que escribe ambas esferas a la potencia base 1 Blue / 2 Red / 3 Black antes del execute nativo. Grupo Blue1→2 y furia Black3→6 se actualizan tras la pasada nativa; por ello la primera observación del Blue legado E_OC2 conserva el 1 en su historial antes del 2. E_OC siempre identifica Blue aun con potencia2; E_OC2 admite Red2, Black3/6 y Blue legado por historial1 de ESTA generación. Las tres políticas consultadas coinciden con los blobs vendorizados en la base0.11.1. La integración completa CP21 se consultó aparte en el commit original `192a7731623d69baacdd37011db60ce894d9de18` y coincide con la copia leída. Hashes en EVIDENCE/CLASSIFICATION_SOURCES.json.

Una firma desconocida o una instantánea de otra identidad/epoch NO elige Red/Black. Un contacto que siga siendo seguro según las puertas heredadas conserva la referencia0.11.1 (Sword 25 / Parry 40 / Iron 50), etiquetado UNKNOWN/VARIANT_UNAVAILABLE y motivo. No se amplía la admisión nativa para hacer pesar contactos que antes se excluían. Cambio de generación, slot reutilizado, muerte, retiro y nuevo contexto invalidan las pruebas; el estado de diagnóstico vive dentro de Entry, con el ciclo de vida existente. No hay caché de punteros de actor.

`balance_core.hpp` contiene la ÚNICA tabla nueva (25/40/50,17/27/33,13/20/25; Fury=Black) y `kStandingRearm=25`. Los pesos de ataques enemigos sobre Link siguen en su tabla original20/30,25/35,30/40,35/45; no se multiplican otra vez.

## POST04: impactos confirmados

El PRE captura una instantánea por valor después de la observación LNK07 existente. `PostureEngine::on_post` la entrega a `Posture::consume`, que conserva la clasificación y precedencia de familias, confirmación nativa, lethal exclusion, cooldown, frescura, deduplicación, prioridad de muerte, frozen y latch. Solo cambia el peso elegido para Sword e IronBall. Las otras familias siguen a cero. No se aplica un peso por giro del arma, esfera o callback repetido. Las sobrecargas de referencia mantienen los fixtures históricos; la ruta de producción está fijada explícitamente al perfil nuevo por source_audit.

Los puntos siguen siendo0..100. El peso de tabla es nominal; el crédito contable real es `after-before` tras saturar. Un Sword Red final 85→100 usa peso 17 pero acredita 15. Los logs conservan peso, antes/después y las unidades reales en los contadores. No se convierte el daño de vida en postura ni viceversa.

## POST08: preview y commit

El parry conserva su juicio y todas sus restricciones nativas. Una copia local constante de la instantánea se pasa a preview y apply. El recibo del preview vincula slot/id/generación/epoch/token, peso, antes/después/cruce y procedencia. Apply recalcula y rechaza cualquier diferencia ANTES de modificar el contador; se registra PreviewMismatch, sin crédito cruzado ni segundo latch. Un cambio de objetivo no transporta el resultado del preview.

Furia sigue sin parry en los casos vetados por POST08/chip; el valor20 solo es su perfil numérico si una regla ya vigente admite realmente el parry. No se cambia la ventana [-1,+9] frames / 11 ticks, el desvío, el aplazamiento de BREAK_BY_PARRY, el crédito +0 a Link ni su daño nativo.

## POST06: destinos de salida

Todos los productores que antes entregaban 50 usan ahora la misma constante 25: fin de stun, timeout de pie y abortos técnicos ya seguros. La validación de `Posture::rearm` acepta exclusivamente 0 o 25. Las puertas de transición, native priority, muerte, Finish y levantamiento no se amplían. El rearme se hace por la salida que ya verificaba POST06, nunca al iniciar STAGGER_OPEN. La ruta completa BIG/getup y su salida redirigida conservan 0.

El consumo contable es 100-target: 75 para pie25 y 100 para getup 0. Los contadores/motivos dicen rearms25/ON_FEET_25, sin etiquetar 25 como 50. El archivo break_core completo es idéntico a la base al normalizar SOLO esos destinos y etiquetas; evidencia SOURCE_NUMERIC_SCOPE.json.

## Recuperación, HP y controles sin cambios

`Posture::advance`, `regen_rate_for`, el acumulador30Hz, el retraso120 y las tasas 5/4/3/2/1 están conservados. Se observa el HP real del actor para la tasa; el máximo continúa siendo OBSERVED_MAX_THIS_GENERATION del código heredado, no un220/330/440 inventado ni una lectura nueva de un offset supuesto. Se imprime UNKNOWN cuando no hay un máximo observado fiable. El ejemplo Red239→322 con máximo previamente observado330 cambia tasa 4→5, sin alterar su identidad ni los 83 HP de curación.

Los220/330/440 HP, regeneraciones2/3/4 HP/s y HM x2 son contexto de Expansion suministrado por el usuario, no multiplicadores de esta política. No se duplica HP, no se normaliza lifesteal y no se tocan ventanas de curación de aliados. Helm decisivo conserva 100+50 HP; su familia Sword no se convierte en Iron Ball. Las diez cabeceras y 32 funciones heredadas fijadas por hash protegen defensa manual, 75 ticks, R+B, LNK01–07, daño, IA, parry, HUD y escrituras nativas. No se importó código nuevo de Lazy Shield Rework ni se añadió una dependencia; se conserva el crédito a Kamilink y no se inventa una licencia.

## Auditorías, regresiones y límites

Source audit, barrera heredada,17 laboratorios reales y 380 mutaciones se ejecutan contra las funciones de producción. La nueva auditoría de variante verifica también que sus totales de unidades/eventos/rearmes coincidan con las ecuaciones globales anteriores. Un nuevo caso de conservación independiente de llamadas de parry mantiene detectable el mutante histórico que elimina e6; no se debilita ninguna expectativa. Los mutantes tienen preflight de anclas, timeout externo de compilación/ejecución y estados KILLED/SURVIVED/TIMEOUT/ERROR; un bloqueo no es detección.

El auditor de stores usa el PE y el MAP para acotar los tres callbacks heredados de guardia/R+B; verifica dos BTR del bit27 con sus dos stores+0x678 y un AND para consumir B+0x40e9. Dos negativos cambian instrucciones extraídas del DLL real. Es una auditoría de ese ámbito, no una prueba formal de todos los efectos x64. Se completa con la barrera de fuente, 16 hooks / 48 imports fijados y auditoría PE. Los primeros intentos internos corrigieron carga de módulos con Python-I, lectura explícita UTF-8 en Windows y anclas/fixtures contables; no son entregas de gameplay distintas.

Sin asignaciones por frame, hilos ni búsqueda global por contacto. Captura O(1), arrays fijos de 64, detalle limitado a 180 líneas y resumen periódico acotado con cierre final. No se midieron FPS/CPU dentro del juego. La aproximación de resistencia100/150/200 NO es equivalencia completa de recuperación: conservar tasas normalizadas implica distinta equivalencia absoluta conceptual. El ajuste de recuperación/retardo se reserva para 0.11.3.

No hay cambios a otros enemigos, otros mods, DEVF CP10, encuentros, EXE, host, SDK, ROM, saves o instalación del usuario. La compilación usa el SDK/ABI2.0.3 y los pins heredados. Nada se instala automáticamente. No PR, merge, tag o release. Las mecánicas nuevas y la coexistencia de 0.11.2 siguen HUMAN_RUNTIME_PENDING.

La ejecución final mantuvo también las dependencias CRT/sistema: se eliminó una comparación de etiquetas de diagnóstico que había materializado un import strcmp adicional. La muestra del formateador cambió únicamente su policy_id aprobado; g++ y MSVC produjeron el mismo archivo. La compilación y auditoría del módulo se ejecutan antes de las mutaciones para detectar fallos del binario pronto. No se amplió ningún pin para aceptar diferencias.
