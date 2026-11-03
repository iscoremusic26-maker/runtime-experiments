# HUD FIX03 — Enemy Posture System 0.11.5 PRIVATE TEST

La corrección restringe la supresión al propietario nativo del prompt contextual inferior. Raíces, corazones, minimapa, ITEMS/MAP, rupias, objetivo, barras enemigas y HUD superior continúan su dibujo nativo aunque crucen la banda de Link. No se reubican elementos ni se cambian acciones.

## Base y causa demostrada

Base compilada: `061e1793d687c958d10e9d0c63ae898c369bda24` (0.11.4). Su descendiente documental `b39cccbd3403543c5acb398c88fa6812c4cf128c` se consultó sin usarlo como base del binario nuevo. Rama nueva: `feature/posture-hud-fix03-0-11-5`.

Se inspeccionaron ambas capturas visibles en la conversación: con barra faltaban elementos generales; sin barra aparecían dos instancias de Shield attack/B, inferior y superior derecha. No se publican las capturas ni el log personal. El resumen saneado del log `dusklight-20261103-114656.log`, SHA-256 `ed86073768987359a9016d0b7a07d8dc5fb30f5b8bd7c9c8ff229287c9c7b259`, registra 61.696 pantallas, 61.696 candidatos y 61.696 supresiones/restauraciones de pane. Eso era una pista, no una medición de píxeles.

La fuente oficial `libs/JSystem/src/J2DGraph/J2DScreen.cpp` define `u16 J2DScreen::getTypeID() const` con retorno **8**. La inspección estática del EXE oficial, SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`, resuelve la exportación `?getTypeID@J2DScreen@@UEBAGXZ` a RVA `0x166dd10`: `b8 08 00 00 00 c3` (`mov eax,8; ret`). No se ejecutó ni modificó el EXE.

En 0.11.4, `hudfix_collect` excluía tipos16/17 pero aceptaba la pantalla8 como primitiva de rectángulo completo. `on_screen_pre_fix02` construía máscaras geométricas sin una autorización estricta de propietario; `on_pane_pre_fix02` podía pasar `drawEnabled=false` a esa raíz. `J2DPane::draw` propaga ese argumento a los hijos: se perdía todo el subárbol. Los fallbacks de Picture/Font por coordenadas tampoco probaban pertenencia. El adaptador anterior modelaba incorrectamente Screen17 y aceptaba ciertas supresiones ajenas como comportamiento esperado.

El nuevo fixture ejecuta los callbacks auténticos congelados de 0.11.4 y los nuevos sobre la misma escena. La base suprime la raíz y pierde diez identidades protegidas; la corrección conserva sus cantidades e identidades. También se prueba una pantalla general separada, igual que la separación nativa mpMeterDraw/mpEmpButton. El fixture es un modelo de interfaces y propagación de dibujo; los offsets y la ABI reales se comprueban separadamente al compilar contra el SDK oficial y auditar el PE.

## Procedencia nativa y selección

`src/d/d_meter2.cpp::_draw` encola separadamente `mpMeterDraw` (HUD general/superior) y `mpEmpButton` (paquete contextual inferior). La pertenencia se lee dentro de PRE/POST de `dMeterButton_c::draw`, aceptando únicamente `self == dMeter2Info_getMeterClass()->mpEmpButton`. No se seleccionan palabras.

Dentro de ese propietario vivo, solo `mpButtonScreen` permite construir certificados de los dos slots `field_0x4be[0/1]`. Se verifican los campos `mpText[slot]`, su pertenencia al árbol y tags `text_n`/`text2_n`; para los botones se verifican las subramas específicas creadas por `d_meter_button.cpp::createButtonScreen`:

| Enumeración | Tag nativo PC |
|---|---|
| A/B/R/Z | abtn_n / bbtn_n / rbtn_n / zbtn_n |
| 3D/C/S/X/Y | asbtn_n / cbtn_n / sbtn_n / xbtn_n / ybtn_n |
| 3DB | as_b_n |
| Bin | bottl_n |
| Nun/Remo/Remo2/AR/NURE/Reel/Reel2/AB/Tate/NunZ/NunC | campos NULL en constructor PC; solo texto certificado, sin inventar widgets Wii |

La raíz, un tag incorrecto, una subrama compartida inválida o un propietario ajeno nunca autorizan borrado. Solo después de certificar propiedad se agrega la geometría visible de texto y botón y se compara con la banda de Link. Se suprimen las primitivas del clúster certificado invasor, incluidos sus hijos de texto/sombra/glifo; no un ancestro de HUD múltiple. Pantallas8 y contenedores16 siempre continúan. Al no estar visible la barra, la política no suprime nada.

Picture requiere identidad exacta certificada; OutFont requiere el textbox certificado del slot. Font no se clasifica por palabras ni por coordenadas: solo se aplica una lease de sus cuatro colores dentro de la llamada de pane certificada. Una emisión ajena que cruza la banda permanece nativa. Las colisiones de Picture ajena se cuentan sin borrarla. No se afirma que esos contadores detecten todos los píxeles de todas las rutas desconocidas.

El Pikari inferior usa la misma función del renderizador general. Se añade un único target visual `dMeter2Draw_c::drawPikari` PRE/POST, con firma exacta y observación del argumento3: debe ser `&mpEmpButton->field_0x2e8[slot]` del propietario vivo y slot certificado invasor. Dentro de esa llamada solo los descendientes de `mpPikariParent`, tag `pika_n`, quedan autorizados para supresión. Una llamada del HUD superior con otro contador o un hermano ajeno en esa pantalla se conserva. **El cuerpo original de drawPikari siempre se ejecuta**, incluidos avance de animación y audio; no se modifican sus argumentos ni contadores.

## Escrituras y conservación

Únicas escrituras nativas nuevas/activas en la política: argumento por valor `J2DPane::draw` número5, restaurado en POST; cuatro colores de JUTFont en una lease síncrona restaurada exactamente. La predicción geométrica existente `hudfix_root` conserva su lease temporal de scale/translation/matrices y su restauración fijada. No hay escrituras de mVisible, códigos de acción, estados de contexto, entradas ni coordenadas persistentes; no reflow. `hudfix_collect` excluye explícitamente el índice raíz y tipo8 de la geometría propia.

Los certificados y punteros prestados se limitan al draw del propietario; se borran en POST. Límites: 4 propietarios/pantallas/Font/Pikari anidados, 512 nodos, 48 de profundidad de colección, 64 Pane calls, 128 identidades de pantalla por presentación. Árbol desconocido, contexto no ortográfico o viewport inesperado y overflow dejan HUD nativo y cuentan falta de cobertura. No se usa memoria de EHB ni un servicio privado nuevo.

El bloque desde `namespace align02native` hasta la presentación por frame, `alignment_core.hpp`, el inventario CP06 auténtico y los callbacks `hudfix_before/hudfix_after` se mantienen iguales a 0.11.4. El nuevo gate verifica el bloque de alineación/paquete byte por byte y las funciones preservadas. Scoop, interpolación y parpadeo no se reimplementaron. El usuario confirmó su corrección en 0.11.4; la regresión visual en este binario sigue pendiente.

Combate congelado de 0.11.2: 107 funciones y 15 encabezados con los mismos hashes; solo se normaliza la cadena de versión en lifecycle para comparar. Blue25/40/50, Red17/27/33, Black/Fury13/20/25; rearme25/0, decisivo×1.5, R+B, L+R, 75 ticks, regeneración y comportamiento de otros mods intactos.

## Laboratorios y límites

El adaptador compara cantidades/identidades protegidas con una traversía nativa independiente y obtiene la geometría esperada de las matrices calculadas por esa traversía, no de la decisión del mod. Cubre ambas instancias de Shield attack/B por identidad de widget; 22 códigos; dos slots simultáneos; sombras/glifos; Pikari inferior y ajeno; Picture/Font/OutFont ajenos dentro de la banda; lease Font propia y su restauración; viewport4:3/ancho; alpha0/1/.2/.005; propietario recreado cada escenario; tags/owner/pantalla inválidos. Los laboratorios heredados cubren presentación sin tick, hold/fade/pulso y transformaciones. Eso no ejecuta menú, lobo, cámara, cambio de sala o raster DX12 nativos: esos casos están en la prueba humana.

La entrada heredada `test_hudfix02_adapter.py` se conserva y delega al fixture corregido. Se sustituyen explícitamente las dos premisas incorrectas (Screen17 y borrado geométrico de emisiones ajenas); no se conserva una expectativa que constituía el bug del usuario. Las once identidades de mutación FIX02 se mantienen con anclas del código actual y control positivo; el oráculo auténtico CP06 no se edita. Nuevas mutaciones verifican que se detecte ocultación ajena, invasión forzada/ignorada, cookie obsoleta y fallo de aislamiento Pikari/Picture/OutFont. Compilación fallida o TIMEOUT es FAIL, nunca detección válida.

Telemetría `POST_HUD_FIX03_INIT/SUMMARY`: frames activos/inactivos, raíces vistas/conservadas, slots certificados/invasores/no invasores, dibujos suprimidos por ruta, restauraciones, Pikari, dibujos protegidos conservados, rechazos, colisiones ajenas observadas, overflow/unpaired/uncovered y reaparición. Son eventos de rutas observadas, no conteos de píxeles por elemento ni una certificación visual. Un nuevo borrado global se rechaza por el fixture/gates y requiere FAIL humano inmediato si aparece en el host.

Los resultados finales, commit fuente compilado, CI, hashes y descarga independiente constan en `RESULTS.json` y `EVIDENCE/`. No se abrió PR, merge, tag ni release; no se avanzó al checkpoint de regeneración.

## Resultado de Windows y advertencias

CI `41687970224`: build e independent-download SUCCESS. Fuente compilada `2d0e59329f14d822c1905ee7953d337959932f1f`, CI `29230b450e0b77bdab7aa3edc1f272e17e2a168b`. MSVC 14.51.36231 x64, Windows SDK 10.0.26100.0. Ambos verificadores del artefacto publicado coinciden en nombre, tamaño, SHA-256, ID, versión y PE; ningún juego ni DLL se ejecutó.

18 labs: 2.829.095 comprobaciones. Adaptador FIX03: 67.218; reproducción negativa de la base: 32; adaptador heredado: 47.702. Mutaciones: 393 heredadas + 11 FIX02 conservadas + 8 FIX03 = 412/412, sin TIMEOUT. Negativos semánticos: 114 heredados + 12 nuevos; PE: 20; instrucciones nativas extraídas: 2. Barrera de combate: 107 funciones/15 encabezados. Alineación: 716.386 presentaciones comparadas contra la fuente CP06 auténtica, 2.875.378 comprobaciones del comparador; error lógico máximo 4,577636718572364e−6. Eso no es una medición de píxeles DX12.

PE: 14 hooks compactos + 8 extendidos, 55 imports de juego y los mismos siete contratos de servicio. Única adición respecto de 0.11.4: drawPikari visual con ejecución original preservada. Nueve warnings proceden de encabezados oficiales: C4805/C4806 por operaciones bool/int y C4068 por pragmas push/pop. No se editó el SDK para eliminarlos. El inventario y las líneas saneadas están en EVIDENCE/MSVC_WARNINGS.json.

El run anterior `41687415617` falló antes de la compilación nativa por la importación del auditor en Python aislado. El commit final corrige esa ruta; el run fallido no produjo un .dusk candidato. El resultado publicado y verificable es únicamente el run exitoso indicado arriba.
