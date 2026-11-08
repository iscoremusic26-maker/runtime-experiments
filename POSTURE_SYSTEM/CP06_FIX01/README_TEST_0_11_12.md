# Prueba en juego — Light Fades Twice 0.11.12 (CP06 FIX01) · HUMAN_RUNTIME_PENDING

## A. Instalación (juego cerrado)
1. Cierra Dusklight por completo.
2. Sustituye **solo** el `.dusk` de Light Fades Twice por `LIGHT_FADES_TWICE_CP06_FIX01_0_11_12_PRIVATE_TEST_windows-amd64_<sha12>.dusk` (mismo ID `dev.posture.post05_selective_reactions`; nunca dos versiones a la vez).
3. Mantén los otros siete mods, la misma sala y la misma configuración.
4. Rollback inmediato: 0.11.11 (`7bcebf6f…5be3`, mejores ritmos, con los dos defectos) o 0.11.10 (`9c8f0074…bb4f`, última aprobada).

## B–F. Qué probar (anota variante, ataque/índice, si R estaba sostenido, si pulsaste R+B, si había i-frames y el color de Link)
| Bloque | Pruebas |
|---|---|
| B. Blue normal y 2+2 | sin escudo, con R, parry individual y 3→4; chispa/sonido; vida/postura |
| C. Red normal y Red4 | sobre todo la pareja ×1.35; sin escudo, guardia y R+B en varios ángulos/distancias |
| D. Red especial ×2 | bloquear, parry con R+B **antes** del contacto, dejar que golpee el cuerpo; ¿alguna espada atraviesa sin resultado? |
| E. Black normal | Black8 y Black7, cada índice; bloqueo y parry; ruptura a 100 cancela |
| F. Black furia ×2 | cadenas largas: golpe al cuerpo, bloqueo normal (¼ de corazón y rojo), parry (**0 chip y sin rojo**); prueba también un golpe real o un bloqueo normal **justo después** de un parry: ese rojo sí debe verse |

Atención especial: un espadazo que **atraviese** a Link sin daño/bloqueo/chispa/sonido. Ojo: tras recibir un golpe real Link es invulnerable 1 s (parpadea en rojo propio del juego): ahí atravesar es normal.

## G–I. Regresiones
- G. Mantén R 20–30 s ante Blue/Red/Black: la IA sigue atacando, sin rebotes prematuros.
- H. Golpea Bokoblins con postura < 100 en finales/recoil: sin tambaleo anticipado; rompe a 100 y ejecuta castigo/Finish.
- I. Varios Bokoblins, cambios de habitación, pausa, muerte, HUD/barras/prompts; compara estabilidad/FPS con 0.11.11 en una sala parecida (`PERF_WINDOW` no es FPS).

## J. Log
Sal del juego con normalidad (SHUTDOWN) y aporta el log. Líneas nuevas útiles:
- `CP06F1_SWING` (un golpe: tipo, clip, tasa, ticks, resultado; `anomaly=1` si algo no cuadra),
- `CP06F1_BACKFILL` (una esfera colocada en una pose nativa saltada),
- `CP06F1_FLASH` (reinicio del flash de Expansion por parry o por chip legítimo),
- `CP06F1_SUMMARY` (histogramas y contadores; `CP06F1_CRITICAL` si la sonda de pose se desactivó).
El campo `tick` coincide con el de `POST08_EVENT`/`CP05_*`, así que un golpe concreto se puede correlacionar sin adivinar frames.
