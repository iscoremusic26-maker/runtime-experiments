# Guía de prueba humana — LIGHT FADES TWICE 0.13.10 DKN01 FIX01

Estado: **HUMAN_RUNTIME_PENDING**. Instala solo este `.dusk` (sustituye al 0.13.9). Invoca el **Darknut normal** del Enemy Spawner. Ten aprendidas Helm Splitter y Ending Blow. Al acabar, envía el log `dusklight-*.log` de la sesión.

## A. Bugs de 0.13.9 que deben haber desaparecido
1. **Bucle Shield Attack (fase 2)**: alterna espadazo → Shield Attack → espadazo… muchas veces. Esperado: el Darknut NO se queda en la animación de bloqueo por el Shield Attack, sigue lo que hacía y sigue atacando. Log: `SHIELD_ATTACK_REJECTED`, sin ganancias de postura por el Shield Attack.
2. **Darknut pasivo bajo presión**: en fase 2 ataca sin parar con B. Esperado: bloquea algunos, pero cada pocos segundos lanza combos o golpes por su cuenta. Log: `COMBO_SELECT ... cause=OWN_INITIATIVE` y `NATIVE_CHAIN_SUPPRESSED`.
3. **Patada automática** tras recuperarse de un tambaleo o al levantarse: no debe ocurrir (≈1,5 s sin ataques ni patada al volver).

## B. Fase 1 (armadura y maza)
4. Mira varios combos: deben verse **pesados y lentos** (cada mazazo con su preparación completa, sin saltos bruscos de la maza), con el mismo patrón rápido/lento que los audios pero estirado. Dinos si alguno sigue rápido o si alguno queda demasiado lento. Comprueba también si A = lateral y B = vertical.
5. Sin cadenas de la IA original (golpe de escudo automático solo por pasividad: escudo alzado ~1,25 s o quieto ~2,5 s).
6. Llena su postura (120): tambaleo de 3 s; puedes golpearle todas las veces que quieras (sin límite de 3). Luego vuelve a 0/120. A 0 HP: transformación nativa.

## C. Fase 2 y 3 (espada)
7. Combos rápidos: haz parry a cada corte de los dobles y a cada estocada (cada uno cuenta).
8. Defensa adaptativa: presiona con B. A veces bloquea normal (sin rebote). A veces tu espada **rebota de verdad** (parry del Darknut) y él responde con **un** contraataque (estocada o doble). Log: `ADAPTIVE_GUARD`, `ENEMY_PARRY_REAL`, `SWORD_REBOUND`, `COUNTER_START`.
9. Llena su postura (F2 160, F3 180): **primer tambaleo** (agachado). No cae solo.
   - **Ruta A**: acércate y pulsa B → **Mortal Draw** nativo; al tocarle, cae (TN2B_DIE).
   - **Ruta B**: Shield Attack → **segundo tambaleo distinto** (echado hacia atrás con la espada alzada) → fíjale (Z) y salta con **Helm Splitter**; al tocarle, cae.
   - Sin hacer nada: a los ~3 s se recupera sin caer.
10. En el suelo, **sin Finish**: cuenta ~6 s desde que termina de caer → se levanta (caída al revés + guardia), **misma vida**, postura 0. Fase 2 sigue en fase 2; fase 3 sigue en fase 3. **No** debe sonar/verse la resurrección FIX02 ni morir.
11. En el suelo, **con Finish** (Ending Blow):
    - Fase 2 → resurrección FIX02 una vez → fase 3 (postura 0/180).
    - Fase 3 → muerte definitiva (oscurece y desaparece tras tu Finish), sin segunda resurrección.
12. Empieza el Finish justo antes de los 6 s: no debe levantarse a mitad del salto.
13. Vida a 0 por golpes normales: fase 2 → caída/Finish/FIX02 como en 0.13.9; fase 3 → muerte nativa.

## D. Regresiones
14. Bokoblins, Lizalfos, Chilfos y otros Darknut (Templo del Tiempo, "Darknut (Sword)"): sin cambios.
15. Rendimiento normal; HUD de postura del Darknut sobre su cabeza (oculto mientras está caído).

Qué reportar: número del punto, qué viste, y el log.
