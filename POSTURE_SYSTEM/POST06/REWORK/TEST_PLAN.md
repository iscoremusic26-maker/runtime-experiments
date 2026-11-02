# Verificación y prueba humana

Logs 202551 y212726 no están montados aquí: LOG_NOT_LOCALLY_AVAILABLE. 27 rupturas/17 caídas/12 sin espada adicional son datos históricos aportados, no mediciones propias. No se reutiliza el log viejo0.5.1 como evidencia0.6.0.

Baseline: nueve suites del commit a0a815, preservado. Cambios de contrato: break_lab sustituye sus expectativas de caída por tiempo y120%; compat_lab cambia únicamente expectativa de kModVersion0.6.1. Formateadores pasivos conservan versión interna0.6.0 y fixtures históricos; POST06_INIT/manifiesto identifican0.6.1.

Nuevo break_lab prueba cruces desde modos normales y BIG, no bonus en ruptura, inactividad y Shield repetidos sin caída, deadline no renovable, base1..100, redondeo, un bonus por commit, contacto ajeno rechazado, Helm sin preparación rechazado, rearme0 tras getup,60.000 identidades/generaciones, normalización Helm sin curar, CP21 POST exacto preservando bonus, transacción postura50 y conservación. Mutaciones nuevas prueban timer como Bonus,120%,Shield/ruptura bonificados, duplicación, origen ajeno, renovación de plazo, rearme incorrecto, normalización Helm y escrituras ajenas.

T01–07/T10–12/T13–15/T19/T21–25/T27–30/T34/T36 tienen cobertura de núcleo/modelo; T08/T16–18/T20/T26/T31–33/T35 necesitan además el adaptador real/observación humana. No declarar todas las36 familias gameplay PASS por las comprobaciones sintéticas. HM/Expansion se contrastan por orden fuente y función CP21 exacta; la barra y colisiones en pantalla requieren usuario.

FaseA: retirar0.6.0 e instalar únicamente nueva candidata con Zora. Tres golpes sin flinch; cruce a100 mareo sin vuelo. Esperar: pie/postura50. Repetir: Shield solo no cae; Shield+Helm CONTACTO cae con bonus; espada directa futura cae. Sin Finish: levantar completo y rearme0. Helm fuera de oportunidad no debe matar automáticamente a un actor con HP suficiente para50/100.

FaseB: ocho mods. Repetir Blue solo/grupo, Red/Black normal/furia, HMx2 y barras. Anotar número de evento, arma, HP antes/después, contacto, daño y si la oportunidad terminó por animación o90ejecuciones. Adjuntar log COMPLETO por chat, no a GitHub. Vídeo corto útil para mareo, Helm y Finish.

STOP: crash, HP inesperado/doble descuento, máscara de corte persistente, incapacidad de ejecutar Helm aprendido, caída sin contacto decisivo, Shield solo derriba, animación congelada, Finish ausente, rearme prematuro, conservación0 o pérdida fuerte de FPS/audio. Volver a0.6.0 o0.5.4 con juego cerrado; nunca versiones simultáneas.

## Matriz de las 36 familias

`CORE_PASS` acredita únicamente la aserción indicada en laboratorio; ninguna fila acredita una pelea ejecutada por el agente. `SOURCE` indica trazado de fuente/ABI. Toda observación jugable queda `HUMAN_PENDING`. `PARTIAL` señala una limitación conocida.

| Caso | Evidencia disponible | Pendiente humano o límite |
|---|---|---|
| T01 tres golpes bajo100 | GENERAL heredado y suites de postura/reacción PASS | Confirmar Blue/Red/Black en pantalla |
| T02 cuarto golpe rompe | CORE_PASS Stun sin Bonus, no Drop | Mareo nativo visible |
| T03 giro/salto rompen | CORE_PASS POST BIG desde PRE seguro convertido a Stun | Cada técnica real |
| T04 FIND/ATTACK/WAIT/DAMAGE | CORE_PASS modos seguros parametrizados | Transición real en combate |
| T05 Blue solo/grupo | Generación/id por actor; labs de identidad PASS | IA grupal y separación visual |
| T06 Red | GENERAL/RB heredados PASS; no cambios a Expansion | Habilidades y E_OC2 en combate |
| T07 Black/furia | GENERAL/RB heredados PASS | Furia/chip en combate |
| T08 animación nativa | SOURCE DAMAGE3→BCK8, sin escritor de frame/rate | Deslizamiento/voz/tiempo visual |
| T09 inactividad | CORE_PASS90 ejecuciones sin Bonus/Drop | PARTIAL: clip puede terminar antes de90; no3s garantizados |
| T10 postura50 | CORE_PASS transacción/liberación/audit conservación | Contador del log y siguiente golpe |
| T11 nueva ruptura | API target50 y núcleo acumulación heredado PASS | Ciclo completo mismo actor |
| T12 ciclos tras timeout | Identidad/commit/rearme cubiertos parcialmente | Dos rupturas completas mismo actor |
| T13 Shield preparatorio | CORE_PASS collider Shield→Stun/preparación, sin Bonus | Escudazo real y HeadLock |
| T14 Shield repetido | CORE_PASS plazo absoluto no renovable | Animación/contactos repetidos |
| T15 Shield sin Helm | CORE_PASS plazo termina Recover50 | Recuperación de pie visible |
| T16 Helm fallado | CORE_PASS requiere hit fresco Sword; truth table32 | Animación que falla collider |
| T17 Shield+Helm | CORE_PASS preparación→Bonus único; SOURCE adaptador | CONTACTO real, caída y Finish |
| T18 HEAD_JUMP | SOURCE máscara PRE5→8; CORE_PASS floor/letal/CP21 POST exacto | HP real con/sin Expansion; Wood mantiene excepción |
| T19 espada directa | CORE_PASS Bonus sin escudo | Caída al contacto y vector |
| T20 espadas especiales | CORE_PASS no reinicia BIG existente; SOURCE Family::Sword | Mortal Draw/giro/salto/4.º corte reales |
| T21 base10/20 | CORE_PASS10→15,20→30; mutación120% detectada | Comparación de HP real |
| T22 impares/único | CORE_PASS bases1..100, half-up, commit duplicado | HP entero en combate |
| T23 base0 | SOURCE base>0 y normalización no aumenta HP; cobertura parcial | Contacto sin daño real |
| T24 ruptura sin bonus | CORE_PASS apertura/Stun y bonus solo futuro | Ver log por evento |
| T25 otras familias | CORE_PASS no Sword sin Bonus; SOURCE clasificación estricta | Flecha/bola/bomba/bumerán/muerte reales |
| T26 suelo/Finish | SOURCE BIG5 usa Down/Finish original | Prompt y Finish real |
| T27 levantarse/rearme0 | CORE_PASS Down5→Getup6→FIND5→0 | Clip completo sin rearme prematuro |
| T28 muerte/Finish | Núcleo heredado congelación por muerte; SOURCE prioridad nativa | Muerte real y limpieza |
| T29 bonus letal | SOURCE HP0+attention0 y BIG original; cobertura parcial | Animación/limpieza letal |
| T30 HM | CORE_PASS pérdida efectiva parametrizada; CP21 POST exacto monotónico | HM ausente/x2 y barras reales |
| T31 barras | SOURCE mismas HP/attention, sin cambios a Bars | Visualización y limpieza |
| T32 habilidades | GENERAL/RB/CP21 modelos PASS; fuentes de otros mods intactas | Black/Red/Blue completos |
| T33 ocho mods/aislado | SOURCE contratos y orden; no dependencia nueva | Fases A/B enteras |
| T34 simultáneos/reciclaje | Núcleos lifecycle/posture;60.000 generaciones en nuevo lab PASS | Cambio de sala real |
| T35 pausa/FPS | Actor exec como reloj; regen histórica sin cambio | TIMEBASE_PAUSE_UNVERIFIED; PARTIAL duración~3s |
| T36 fail-safe | CORE_PASS fallo writer/abort50/identidad; auditoría escrituras | Nunca afirmar seguridad universal sin juego |

## Compatibilidad de los ocho mods

| Mod | Revisión y alcance | Estado jugable |
|---|---|---|
| Posture0.6.1 | Dos hooks E_OC; mismo ID, una versión cargada | HUMAN_PENDING |
| EVF0.15 / Bokoblin Expansion0.17 | CP21 exacto; no cambian sus binarios, IA ni servicios. Normalización independiente y CP21 POST monotónico; la máscara ajena no se restaura por este mod | HUMAN_PENDING |
| Enemy Health Multiplier2.0.3 CP11 | Bonus sobre pérdida efectiva tras cc_at_check; floor50/100 conforme Expansion | HUMAN_PENDING |
| Enemy Health Bars2.0.3 CP06 | HP/attention nativos; sin servicio/HUD nuevo | HUMAN_PENDING |
| Zora Swim1.3 | Sin ruta de escritura compartida identificada | HUMAN_PENDING |
| Luau Support1.0 | Sin dependencia nueva ni cambio de scripts | HUMAN_PENDING |
| Randomizer1.0.6 | Sin cambios a flags de aprendizaje/equipo/eventos | HUMAN_PENDING |

La tabla agrupa EVF+Expansion en una fila: son dos mods, ocho en total incluyendo Posture. No equivale a validar órdenes arbitrarios de hooks o todas las variantes del usuario.
