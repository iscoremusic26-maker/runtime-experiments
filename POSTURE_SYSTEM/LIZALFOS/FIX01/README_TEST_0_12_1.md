# Light Fades Twice 0.12.1: prueba humana (Windows / DX12)

Estado: **HUMAN_RUNTIME_PENDING**. Sonido, chispa, animación, colisión real y FPS solo se confirman aquí.

## Instalación (con el juego cerrado)
1. En tu carpeta de mods, quita **todos** los `.dusk` anteriores de Light Fades Twice, incluido cualquier 0.11.x que siga ahí.
2. Coloca solo `LIGHT_FADES_TWICE_LIZALFOS_FIX01_0_12_1_PRIVATE_TEST_windows-amd64_5c8ac17e75ed.dusk`, SHA-256 `08b18329128041b9b4bec99d10e2736fbd942fe58d4a1b037e7b88aef4480e23`.
3. Mantén los otros ocho mods como estaban. Debe haber exactamente un Light Fades Twice activo.

## Rollback (con el juego cerrado)
- Último Lizalfos: `.dusk` 0.12.0, SHA-256 `0565555c45f683684a60b6c796f18c474604751468b682e8596c4396136b1b99`.
- Respaldo global: `.dusk` 0.11.12, SHA-256 `82f678a8ffacf197d7828721513597fe1b4d3c6752ca07ce2d6a6c9c2797d2ed`.

## Dos pasadas
- **A, aislado:** solo Light Fades Twice (con sus dependencias si las pide), para descartar interferencias.
- **B, integración:** tus ocho mods habituales.

## Qué mirar primero en el log
- `LIZ_POSTURE event=INSTALL ... enabled=1 ... gains=9/15/30/5/25`.
- `LIZ_SUMMARY part=FIX01`: `impacts_missing` debería ser 0. `lost_ticks` mayor que 0 o `class=MISSING_FEEDBACK` son lo primero que quiero ver.
- `LIZ_CRITICAL event=POSE_PROBE_RESTORE_MISMATCH`: la cobertura se apagó esa sesión.

## Matriz

### Contacto y sonido (lo más importante)
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 1 | R mantenido contra cada combo completo, especialmente D1→D2 | **Cada** golpe suena y hace chispa. Nunca dos sonidos por golpe. El combo no se corta | `LIZ_IMPACT class=LINK_GUARD audio_native_receipt=1`; `LIZ_FEEDBACK` en D2 |
| 2 | Lo mismo, de cerca y a media distancia, moviéndote lateralmente | Ningún golpe atraviesa el escudo por delante | sin `class=LINK_BODY` con `link_proc` de guardia |
| 3 | ¿Tras D2 Link se desplaza algo más y se recupera bien? | Reacción legible, sin quedarse enganchado | juicio tuyo |
| 4 | Shield Attack a tiempo contra N, D1, D2, cola lenta, cola rápida | Parry, +15, sonido de escudo, el combo sigue | `LIZ_PARRY gain=+15`; `part=PARRY_BY_IMPACT` |
| 5 | D1 bloqueado con R y Shield Attack solo para D2 | **Ahora debe poder ser parry** | `LINK_PARRY impact` de D2 |
| 6 | D1 y D2 con dos pulsaciones | Dos parries, dos seriales | dos `LINK_PARRY` |
| 7 | Una sola pulsación manteniendo R+B | Un parry; el otro golpe es bloqueo con sonido | un `LINK_PARRY` |
| 8 | Shield Attack muy pronto o muy tarde | Bloqueo, sin crédito | `MISSED_WINDOW_GUARD` |
| 9 | Sin escudo | Daño y reacción nativos | `class=LINK_BODY` |
| 10 | Mientras parpadeas tras recibir daño | Sin daño nuevo ni sonido falso | `class=IMMUNE_VALID` |
| 11 | De espaldas con R | No bloquea, recibe daño | `LINK_BODY` |
| 12 | Fuera de alcance | Golpe al aire: sin sonido ni daño | `class=WHIFF` |
| 13 | ¿Sigue algún golpe "fantasma" que parece tocar sin reaccionar? | Dime patrón, golpe y distancia | línea `LIZ_IMPACT` de ese golpe |
| 14 | Shield Attack al cuerpo con postura <100 | Sin tambaleo, ahora con su sonido, una vez por pulsación | `bash_se` en `part=FIX01` |

### Ruptura
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 15 | Llevar a 100 por parry, por espada y por bloqueo propio | Se tambalea **de pie**, no cae | `event=BREAK_STANDING native_knockdown=0` |
| 16 | Iron Ball que realmente cruza 100 | También de pie | `BREAK_STANDING` |
| 17 | Iron Ball con postura baja | Reacción nativa, sin rearmar | `source=IRON_BALL` |
| 18 | Un Shield Attack **nuevo** en el tambaleo | Aparece el aviso de Helm Splitter | `event=HELM_PREPARED` |
| 19 | El mismo Shield Attack que hizo el parry | No prepara nada | sin `HELM_PREPARED` |
| 20 | Helm Splitter | Golpe real, cae, Finish disponible | `DECISIVE_HIT kind=HELM_SPLITTER`, `DOWN_FINISH` |
| 21 | Espadazo nuevo durante el tambaleo | Cae, Finish disponible | `DECISIVE_HIT kind=SWORD` |
| 22 | No hacer nada 3 s | Vuelve a luchar con postura 0 | `event=REARM` |
| 23 | Caído sin rematar | Se levanta y postura 0 | `GETUP`, `REARM` |
| 24 | ¿Se lee bien el tambaleo? ¿La parte final aturdido queda natural? | Juicio tuyo; la duración real del clip no se pudo leer | |

### Balance
| # | Prueba | Esperado |
|---|---|---|
| 25 | Solo parries | 7 para romper |
| 26 | Solo espadazos | +9, baja la vida; con vida baja regenera menos postura |
| 27 | Espada y parry combinados | Claramente mejor que solo una cosa |
| 28 | 370 HP y cero regeneración de HP | Sin cambios frente a 0.12.0 |

### IA
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 29 | Machacar B de frente | Sube a B y C de verdad | `event=ROLL level=C pct=45` |
| 30 | Dos golpes bloqueados seguidos | Suele salir de guardia y contraatacar con normal o doble | `LIZ_COUNTER COUNTER_SELECTED`, `ATTACK_COMMITTED` |
| 31 | ¿Sigue valiendo spamear B sin mirar? | No de forma fiable | juicio tuyo |
| 32 | Parry del Lizalfos | +25 a tu postura, contraataca corto | `ENEMY_PARRY`, `source=ENEMY_PARRY` |
| 33 | Parry al contraataque, incluido D1 y D2 | No cancela, sigues teniendo aperturas | `LIZ_COUNTER CONTACT` |
| 34 | Alejarte tras preparar un contraataque | Se cancela sin forzarlo | `EXPIRED cancel_reason=LINK_FAR` |
| 35 | Colocarte a su espalda | Sin giro mágico: se gira de forma natural o caduca | sin `ATTACK_COMMITTED` desde atrás |
| 36 | Guardia prolongada | Nunca se queda bloqueado | sin `code=3` en `LIZ_CRITICAL` |

### Combos (no deben haber cambiado)
| # | Prueba | Esperado |
|---|---|---|
| 37 | P1–P4 | Mismos ritmos y velocidades que tu versión aprobada; 25 % cada uno en `selected` |

### Regresión
| # | Prueba | Esperado |
|---|---|---|
| 38 | Bokoblins Blue/Red/Black, furia, especial, CP04 | Igual que 0.12.0, sin falso rojo |
| 39 | Grupos: 3 Lizalfos y Bokoblins a la vez | Sin atascos, sonido por golpe, barras correctas |
| 40 | FPS con varios Lizalfos en combate | Sin caídas; `probes` en `part=FIX01` indica cuánto trabajó la cobertura |
| 41 | Cerrar el juego | Sin bloqueo; `LIZ_SUMMARY` final |

## Si algo falla
Compárteme el log con el número de prueba. Si es un golpe sin sonido, dime patrón y posición del golpe si la recuerdas.
