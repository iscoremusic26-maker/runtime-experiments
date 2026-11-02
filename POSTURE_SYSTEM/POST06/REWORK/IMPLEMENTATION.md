# POST06 REWORK 0.6.1 — candidata privada

Base EXACTA compilada a0a81535639459275702371324448e96a5d17575. Snapshot local 9614648 tiene contenido verificado por SHA de blobs, pero NO es el ancestro Git upstream. La rama remota nueva se crea desde a0a815. No se alteran 0.5.4, 0.6.0, Expansion, EVF, HM ni Bars.

## Comportamiento

Bajo100: núcleo GENERAL de POST05 sin cambios de política. Cruce no letal confirmado: DAMAGE3 (Shield Attack nativo), no BIG_DAMAGE y sin bonus. Los cortes fuertes también entran a mareo si PRE era modo normal seguro. Muerte, agua, caída física y perfiles no verificados conservan precedencia nativa.

STAGGER_OPEN: Shield Attack REAL de Link prepara Helm, no da bonus, no derriba ni renueva plazo. Una espada directa futura o Helm legítimo preparado produce un bonus único: extra=(base+1)/2, redondeo half-up por contacto, sin acumulación fraccional. Base10→15,20→30,3→5. Base0 no consume. La caída usa el vector de ESE contacto; BIG nativo ya seleccionado no se reinicia.

Timeout: recuperación de PIE y transacción postura100→50. No existe Act::Drop ni temporizador de inactividad que genere BIG. Tras caída real, DOWN5 y getup6 nativos; rearme0 solo al salir a FIND5 tras GETTING_UP. Finish y muerte nativos. Contabilidad units_rearmed cuenta100−target (50 o100), no HP.

## Mareo y disponibilidad de Helm

[S] executeDamage3 elige BCK8, voz nativa, retroceso y HeadLock; state5 sale a FIND/MOVE_OUT cuando termina el clip. [S][B] checkCutHeadState exige aprendizaje/evento o entrenamiento, equipo apropiado, objetivo enemigo y HeadLock. Por sí solo el mareo concedería la disponibilidad; un POST adicional sobre executeDamage retira SOLO HeadLock durante oportunidad aún no preparada. Tras Shield Attack confirmado se permite el flag nativo. No se concede habilidad no aprendida.

**Ventana provisional**: máximo90 ejecuciones propias; si la animación nativa termina antes, cierre de pie anticipado. No se congela frame ni se repite clip/audio para fingir tres segundos. La duración visual exacta y suficiencia de tiempo para Shield→Helm requieren prueba humana. No afirmar ventana visual fija3s. El reloj de regeneración sigue teniendo el límite histórico TIMEBASE_PAUSE_UNVERIFIED; el de oportunidad solo avanza al ejecutar ese actor.

## Helm independiente y compatible con Expansion

[S] CP21 cp19_policy.hpp helm_pre/post: Master100/Ordon50, Wood fuera; mascara HEAD_JUMP5→TURN_RIGHT8; no cura una pérdida nativa/HM mayor. Si health≤daño, CP21 deja muerte original. El adaptador independiente normaliza a max(pérdida nativa efectiva,100|50), exclusivamente en contacto de collider de Link y PROC_CUT_HEAD0x2d, sin Finish, con firma procesada. Se evita health=0 original ANTES del original; nunca se resucita HP después. Native HP0 ya ocurrido se conserva. Fuera de oportunidad también funciona esta adaptación, sin bonus.

Con Expansion, su PRE ya puede haber puesto cut8: no se adquiere ni restaura una máscara ajena. Su POST helm_post es un mínimo monotónico de HP: si el consumidor ya descontó el daño equivalente y el +50%, CP21 no lo vuelve a descontar ni eleva HP. El laboratorio ejecuta ESA función exacta. No se multiplica otra vez HM: su cc_at_check ya terminó antes de observar pérdida. El mínimo50/100 reproduce la propia regla CP21, que puede superar daño nativo escalado por HM.

Se limita un impacto por episodio Helm y generación; repetición procesa cooldown1 equivalente al bloqueo nativo antes de observar PRE. No se permite inferir Helm de un botón o de pasar cerca. Cuando el actor no observa el fin del procedimiento (p.ej. culling), puede conservar exclusión conservadora hasta observar una fase no-Helm, como la política CP21.

## ABI y escrituras

[B] EXE SHA ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049. setCutType cuerpo0x1408cd980 escribe byte+0x668; procCutHeadInit lee procedimiento+0x4144; checkCutHeadState lee HeadLock+0x69a. static_assert de offsets y enum. Se escribe cut type directamente para NO tocar el flag adicional que setCutType borra. No se llama ese setter.

Dos hooks: damage_check PRE/POST; executeDamage POST. PRE siempre HOOK_CONTINUE. Escritores acotados: restore_reaction (campos históricos); write_vitality (HP y attention flags solo letal); helm_set_cut (5/8); helm_guard_duplicate (cooldown1). No frame/rate, collider de ataque, potencia, HUD, audio ni saves. Se mantiene identidad slot/gen/id. Reentrada cierra escrituras de reacción y evita contabilizar el contexto anidado; máscara propia se devuelve. Rutas de error no generan caída por temporizador.

La presencia de SDK/CI no constituye prueba de gameplay. Versión nueva siempre HUMAN_RUNTIME_PENDING; fallos de las auditorías bloquean distribución.

## Resultado binario y revisión final [B][C]

DLL real MSVC extraída del artefacto: dos metadatos HOOK_MEM sobre los objetivos declarados, cuatro imports de servicios, siete imports del juego. Cero imports CRT nuevos frente a0.6.0. GetLinkPlayer y GetSelectEquipSword en el EXE son una carga de memoria seguida de ret: getters de lectura, no una importación de estado global escribible. Las escrituras de HP son word+0x656; attention letal dword+0x650; máscara Link byte+0x668; bloqueo duplicado word+0x8ec. El compilador desenrolló8sitios del bloqueo en el bucle acotado; no son ocho contactos. Las escrituras indexadas de inicialización de tablas internas no deben confundirse con offsets del actor. Modos/timers/flags conservan el escritor auditado; no hay llamadas a setActionMode/executeDamage ni setCutType: executeDamage solo es objetivo del POST adicional.

El rastreador Helm conserva seen durante frames sin contacto mientras PROC_CUT_HEAD siga activo; solo libera el episodio al observar su final, cambio de Link o generación. No confunde ausencia de TG con fin del ataque. Reentrada cierra el escritor de HeadLock. Contactos no decisivos no letales mantienen el mareo sin preparar Helm ni renovar plazo; transiciones físicas/de muerte ajenas conservan prioridad.

## Verificación final del contacto de escudo [S][B][L]

Shield Attack usa **mGuardAtCps**, no mAtCps/mAtCyl de la espada. Fuente setAtCollision, PROC_GUARD_ATTACK0x1e. En EXE cuerpo0x1408c3b40, rama0x1408c3ef1: registro en Ccsp de actor+0x1e78; static_assert fija ese offset. El clasificador de direcciones separa Shield y Sword, rechaza cero/ajeno y se prueba conectado a la preparación de la máquina. El tipo AT confirmado sigue siendo obligatorio. La normalización Helm requiere actor vivo, token válido, firma de procesamiento, el MISMO collider seleccionado en PRE y POST y tipo Sword; se comparte una única lectura AT con el observador para no desreferenciar un collider antiguo de escudo. Dos mutaciones eliminan o confunden el collider de escudo y deben fallar.
