# Revisión focalizada del piloto

Fuente oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`, Aurora `3227d76c60e1e782ca576610bce61c9e7744d8be`. Import library original SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`. [SOURCE_MANIFEST](SOURCE_MANIFEST.json) y [referencias](evidence/source-references.json) fijan procedencia, hashes y líneas. No se modifican esas fuentes.

## Target y momento

`src/d/actor/d_a_e_oc.cpp`: create establece `field_0x560 = health = 40/220` en 2771–2779, borra current/shape.angle.x en 2808 y llama al wrapper en 2829. El wrapper 2642–2644 llama a execute; execute llama a action en 2631, y action llama a damage_check en 2418. El pre-hook se sitúa después de fijar 220 y antes de estas acciones. No reconstruye el parámetro original a partir de current.angle.x.

La inspección estática del EXE Windows original, SHA256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`, confirma create→wrapper→execute y execute→action, sin flags de inlining crítico en su manifest. [host-target.json](evidence/host-target.json) conserva nombres, RVAs derivados y llamadas; no bytes originales ni disassembly. No se ejecutó el EXE ni se compiló el host.

`DEFINE_HOOK(&daE_OC_c::execute, NativeEocExecute)` y `mods::hook::add_pre` usan el SDK oficial. El compilador verifica firma `int(daE_OC_c::*)()`, health s16 y PMF de 8 bytes. La auditoría PE comprueba metadata Hook MEM, target, PMF unido al thunk/import exacto y versiones de servicios. La referencia importada no es una llamada manual a execute. El callback siempre devuelve HOOK_CONTINUE, sin alterar argumentos, resultado ni ejecución original.

## Identidad y una sola escritura

Lecturas tipadas: perfil 510, sala 3, parameters FFFF0100, setID FFFF, home.pos con **igualdad float32 exacta**, home.angle `(262,0,0)`, stage F_SP121 y capa efectiva 6 mediante getter nativo. La Y efectiva float32 es `-6304.00830078125`; tolerancia cero. Además exige recurso E_OC2, health 220, current.angle.x cero, IsCreating(ID) e init_state 0/1. HP 220 por sí solo nunca autoriza la escritura.

El inventario ya decodificado tiene 40 registros E_oc originales entre los datos disponibles, 7 en ACT6 y cero coincidencias con home.pos del piloto. [identity-uniqueness.json](evidence/identity-uniqueness.json) acredita procedencia sin repetir geometría. **Es identidad por atributos, no una API de ownership de StageService.** Requiere solo CP03, sin mods que editen enemigos, stages o hooks de E_OC. No garantiza aislamiento frente a un tercero que copie exactamente el registro.

Solo se conserva el último ActorId aceptado, nunca un puntero de actor. La consulta por SDK de ese ID anterior rechaza otra instancia coincidente concurrente viva; no hace censo ni busca por perfil o proximidad. Una nueva instancia necesita ID mayor y anterior ausente o en estado de destrucción 3. ID repetido durante create, reciclado o desbordado se rechaza. El ID ya procesado fuera de creación ignora llamadas posteriores, incluso tras daño o si la lógica nativa devuelve HP a 220. Solo una nueva creación válida recibe otra asignación.

La única escritura al actor es `a->health = devf::kHp` (150). `field_0x560` conserva el valor nativo. HP_APPLIED lee el campo tras escribir; esa evidencia aún no existe en el juego. No se promete HP máximo, daño multiplicado o equivalencia a golpes.

## Registro, errores y descarga

Inicialización: valida servicios/versiones, instala hook antes de añadir una única entrada StageService y arma tras recibir handle válido. Sin reintentos o registro por frame. Un fallo desarma, retira el hook por API oficial cuando corresponde y devuelve error; el detach del loader limpia registros propios incluso tras inicialización parcial. Identidad ambigua, fase tardía o HP inesperado producen HP_REJECTED sin escritura y error consumido por mod_update fuera del callback.

SDK declara callbacks en el stack e hilo del juego. HookService, hook.cpp 888–927, elimina callbacks/candidatos y restaura backend o transfiere trampoline; 1057 conecta modDetached. Loader 296–338 hace detach antes de unload; natives.cpp 563–583 difiere FreeLibrary al drenaje posterior. StageService elimina su edición en 214–218 y conecta modDetached en 314. No hay solicitudes ActorService pendientes.

Si retirar un backend vivo falla, hook.cpp 914 invoca fatal. Borealis exacto `4ac5e7052a8c49a122f8d57f626b5c75c5ca6968`, src/log.cpp 637–655, termina con `std::abort()` tras el handler opcional. No continúa descargando como si un hook vivo fuese seguro. Esto es evidencia de fuente; no se ha provocado ni probado ese fallo real.

Shutdown desarma; no borra actores materializados ni implementa hot-unload manual. La retirada humana exige cerrar por completo, quitar el `.dusk` y reiniciar: quitar la edición no elimina un actor vivo.

## Límites

Quince casos TEST_FAKE compilan política/registro reales con SDK y servicios simulados. Simulan 220→pre-hook→150→action, daño y generaciones; no construyen un actor real ni ejecutan la DLL o backend. El bridge tipado se compila y audita, pero llamada real, HP, combate y retirada siguen HUMAN_RUNTIME_NOT_TESTED. Tripwire GX heredado solo en EXE de laboratorio. No se reabren A0/A1 ni auditorías anteriores.
