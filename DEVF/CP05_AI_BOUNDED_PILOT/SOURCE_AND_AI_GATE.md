# CP05 — Fuente y gate de integración

Fuente exacta [Dusklight40457c6](https://github.com/TwilitRealm/dusklight/tree/40457c6adb381928e4b5fef6ed459ed291edd5e2). Referencias siguientes en src/d/actor/d_a_e_oc.cpp:

- [20–38](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_e_oc.cpp#L20): WAIT0/WALK1/FIND3/ATTACK4/DAMAGE5/BIG_DAMAGE6/DEATH9/etc.; no enum inventado.
- 95–105: HIO nativo percepción S1200/M5000, standby1400, demo70. HIO nunca escrito.
- 307–329 y388–407: searchPlayer/searchPlayerShakeHead consumen mPlayerRange junto con FOV/LOS; no basta distancia para entrar. searchPlayer2 344–385 permite sonido/pares/puente nativos: no se suprimen. El record DEVF es tipo0, sin ruta de switch tipo2.
- 897–1059: WAIT/WALK nativos invocan searchPlayer2 y pasan FIND1, animan/colisionan; WALK apunta home cuando distancia>=500 y conserva evasión de obstáculos local.
- 1138–1343: FIND maneja animación, persecución, ataques200–400, timer0x1e y pérdida de percepción a WAIT; el mod no fuerza transiciones ni timers.
- 2304–2394 y2420–2431: MOVE_OUT/leash600 nativo con márgenes100/200/300 y standby1400. No se promete locomoción de navegación general.
- 638–785 /2415–2449: daño primero, agua/caída antes de dispatch. POST observa/cancela interés por pérdida HP o daño/muerte; PRE evita hit pendiente/iframes/event/estados no permitidos. No escribe daño, stun, colisiones ni animación.
- 2528–2534: movimiento, corrección de suelo y play nativos;2586–2639 decrementa timers, action, matrices, cc. Se ejecutan originales una vez.
- 2642–2643 y create(): execute es el mismo target tipado CP03/CP04 humano, no hook nuevo ni API de búsqueda de otro actor.
- 2706–2738: record FFFF0100 + home.angle.x0106 => tipo0, percepción5000 y mMoveRange600 (6×100). Encabezado include/d/actor/d_a_e_oc.h:101–109 define campos propios mMoveRange/mPlayerRange/mActionMode. Comentarios de offsets originales contienen duplicación0x690; se accede por miembro C++ compilado/ABI, jamás por offsets.

HookService oficial sdk/include/mods/svc/hook.hpp: HookImpl::trampoline ejecuta PRE, original y POST tipados; se reutilizan los dos hooks execute/render del baseline, sin replace/skip/recursión manual. La prueba PE anterior del mismo execute y runtime CP03/04 sustenta el punto real; CP05 verifica otra vez PMF/import/export de su propia DLL.

Gate de fuente: GO para un piloto de percepción por instancia, condicionado a MSVC/lab/PE/paquete/descarga y prueba humana. No es GO de gameplay. No se cambia FSM ni se promete retorno a home sin obstáculos. Consultas nuevas dComIfGp_getPlayer(int), dComIfGp_event_runCheck() y ChkTgHit (detallada abajo) declaradas DUSK_NOINLINE en include/d/d_com_inf_game.h1625/1847; ABI/import exactos se comprobarán en nueva DLL.

Ownership: mPlayerRange pertenece al actor concreto; materiales/HIO/texturas compartidos sólo lectura. Scope guarda escalares y key opaco durante PRE/POST; al salir restaura el valor exacto si identidad/key/generación y expected range coinciden. No guarda puntero dereferenciable tras el scope. Callback incompleto: mod_update/shutdown busca sólo ActorId admitido, revalida record/key y restaura si coincide; si actor desapareció o hay otro writer, no toca memoria ajena, registra error fail-closed. Stack8 + overflow contabilizado evita perder scope exterior. El límite de callbacks del host ya documentado se mantiene: no hot reload ni recuperación de abort/OOM fatal.

No se reauditó ARC/32 fuentes/render. CP04.4 .dusk y refs históricos permanecen intactos.

## Validación posterior al gate

Tres imports nuevos exactos en la DLL final, revisados y unidos al importlib oficial:
`?dComIfGp_getPlayer@@YAPEAVfopAc_ac_c@@H@Z`,
`?dComIfGp_event_runCheck@@YAHXZ`,
`?ChkTgHit@dCcD_GObjInf@@QEAAIXZ`.
La última consulta está declarada en include/d/d_cc_d.h295 y definida en src/d/d_cc_d.cpp221–229, wrapper del hit real con comprobación de actor. No se sustituye por la firma de su clase base. PE/ABI del build final verifica el owner exacto y no amplía indiscriminadamente imports. Las dos queries citadas arriba más esta consulta de daño son la superficie nueva; no un nuevo hook.

El primer execute de create ocurre antes del estado2; la inicialización nativa se conserva. La guardia no pretende impedir FIND inicial en esa llamada. El bloque visual y xf_scope son idénticos al CP04, salvo identidad/versionado en mensajes.
