# Verificación y prueba humana

Logs 202551 y212726 no están montados aquí: LOG_NOT_LOCALLY_AVAILABLE. 27 rupturas/17 caídas/12 sin espada adicional son datos históricos aportados, no mediciones propias. No se reutiliza el log viejo0.5.1 como evidencia0.6.0.

Baseline: nueve suites del commit a0a815, preservado. Cambios de contrato: break_lab sustituye sus expectativas de caída por tiempo y120%; compat_lab cambia únicamente expectativa de kModVersion0.6.1. Formateadores pasivos conservan versión interna0.6.0 y fixtures históricos; POST06_INIT/manifiesto identifican0.6.1.

Nuevo break_lab prueba cruces desde modos normales y BIG, no bonus en ruptura, inactividad y Shield repetidos sin caída, deadline no renovable, base1..100, redondeo, un bonus por commit, contacto ajeno rechazado, Helm sin preparación rechazado, rearme0 tras getup,60.000 identidades/generaciones, normalización Helm sin curar, CP21 POST exacto preservando bonus, transacción postura50 y conservación. Mutaciones nuevas prueban timer como Bonus,120%,Shield/ruptura bonificados, duplicación, origen ajeno, renovación de plazo, rearme incorrecto, normalización Helm y escrituras ajenas.

T01–07/T10–12/T13–15/T19/T21–25/T27–30/T34/T36 tienen cobertura de núcleo/modelo; T08/T16–18/T20/T26/T31–33/T35 necesitan además el adaptador real/observación humana. No declarar todas las36 familias gameplay PASS por las comprobaciones sintéticas. HM/Expansion se contrastan por orden fuente y función CP21 exacta; la barra y colisiones en pantalla requieren usuario.

FaseA: retirar0.6.0 e instalar únicamente nueva candidata con Zora. Tres golpes sin flinch; cruce a100 mareo sin vuelo. Esperar: pie/postura50. Repetir: Shield solo no cae; Shield+Helm CONTACTO cae con bonus; espada directa futura cae. Sin Finish: levantar completo y rearme0. Helm fuera de oportunidad no debe matar automáticamente a un actor con HP suficiente para50/100.

FaseB: ocho mods. Repetir Blue solo/grupo, Red/Black normal/furia, HMx2 y barras. Anotar número de evento, arma, HP antes/después, contacto, daño y si la oportunidad terminó por animación o90ejecuciones. Adjuntar log COMPLETO por chat, no a GitHub. Vídeo corto útil para mareo, Helm y Finish.

STOP: crash, HP inesperado/doble descuento, máscara de corte persistente, incapacidad de ejecutar Helm aprendido, caída sin contacto decisivo, Shield solo derriba, animación congelada, Finish ausente, rearme prematuro, conservación0 o pérdida fuerte de FPS/audio. Volver a0.6.0 o0.5.4 con juego cerrado; nunca versiones simultáneas.
