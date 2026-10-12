# G4 — cuerpo, arma, animación y colisión

**PASS_STATIC de lectura y de una cota matemática conservadora de recursos, bajo sus condiciones explícitas.** No es PASS del cálculo de matrices Windows, render DX12, contacto con suelo ni desplazamiento del actor. Los datos completos derivados y hashes están en [resources-envelope.json](evidence/resources-envelope.json).

## Geometría estática y jerarquía real

| Datos VTX1 sin posar | Cuerpo, modelo3 | Arma, modelo4 |
|---|---|---|
| Posiciones F32 | 566 | 17 |
| X mínimo/máximo | -97.552879 /97.552879 | -13.457222 /23.653517 |
| Y mínimo/máximo | -12.688277 /137.963608 | -5.420070 /10.224586 |
| Z mínimo/máximo | -42.500854 /42.500854 | -19.075724 /90.813782 |
| Joints | 29 | 1 raíz identidad |

Estos son límites del buffer de posiciones, **no dimensiones del enemigo posado**: posiciones rígidas y skinned requieren las matrices correctas. Se inspeccionaron INF1/JNT1/EVP1/DRW1 y referencias SHP1 a esas posiciones. No se usa un AABB crudo, cull±200 ni heap como envolvente animada.

Cadenas reales: backbone1 `[0,1]`; mano derecha12 `[0,1,2,9,10,11,12]`; cabeza17 `[0,1,2,15,16,17]`; extremos de piernas25/28 `[0,20,23,24,25]` / `[0,20,26,27,28]`; joint22 `[0,20,22]`, sin descendientes. Escalas bind1 en todos los joints, con flags Maya de compensación de escala0/1; remap JNT1 leído, no asumido por orden.

Native `mtx_set` aplica traslación del actor, rotaciones de actitud/shape/otra Y y HIO por defecto1.5. El arma hereda la matriz animada de mano12. Callbacks de cabeza17/mano12 añaden Yrot y afectan también descendientes; se incluyen como rotaciones arbitrarias en la cota, aunque los diagnósticos de poses siguientes las fijan a0.

## Todas las animaciones, sin exclusiones convenientes

Se analizaron las28 BCK/29 joints de E_ocb: escala, rotación y traslación por eje, tipos de tangente0/1, rotation shift, loop/frame máximo. **18975 segmentos Hermite** en total. El clip LEAP_SPIN de frame máximo0 sigue incluido como pose válida; no se rechaza por no tener duración positiva.

No se excluye ninguna animación por supuesta inaccesibilidad del modo0: la biblioteca completa, bind y mezclas forman una sobreaproximación. ATTACK_B/C5/6 y WAIT0x1B quedan explícitamente cubiertas. Los estados de daño, muerte, agua y demos no se omiten para reducir dimensiones. Esta inclusión no afirma que todos se disparen en el preset/contexto elegido.

Hallazgos que invalidan medir solo keyframes:

- ANGRY_A/B tienen escala variable en joint22, con keys negativos. Intervalos continuos conservadores de escala global: A[-0.226976746,2.388904147], B[-0.414888170,1.692899857]. Son hulls, no extremos exactos alcanzados.
- FINISH tiene escala1 en sus keys, pero tangentes no nulas: hull global[0.023145622,1.961046138]. Suponer escala constante1 omitiría interpolación.
- Solo joint22 presenta escala no unitaria en la unión de clips; no tiene hijos. Ningún padre utilizado por SSC posee un intervalo que contenga0. Los valores negativos de22 no se sustituyen por1 ni se ignoran.

## Límite continuo y propagación

En aritmética racional exacta, cada segmento Hermite con extremos `(t0,v0,mout)` y `(t1,v1,min)` se convierte en controles Bézier:

`[v0, v0 + (t1-t0)*mout/3, v1 - (t1-t0)*min/3, v1]`.

Cuatro subdivisiones de Casteljau producen16 subcurvas; el mínimo/máximo de sus controles encierra **todos** los valores continuos. Se incluyen los extremos que usa el clamp nativo fuera del dominio de keys. Se verifica el orden de tiempos y ambos tipos de tangente; no se emplea un muestreo de frames como demostración del límite. Los floats F32 e índices S16 recibidos se convierten a fracciones exactas para este cálculo.

Se unen por joint los intervalos de todos los clips y bind. Un morph convexo de traslación/escala permanece en esos intervalos. Las llamadas E_OC usan morph0/5; el flujo McaMorfSO interpola trans/scale y quaternion, con ratio entre0/1 bajo su contrato normal. La cota permite rotación arbitraria, incluidas callbacks y actitud del actor.

Propagación: norma lineal del hijo ≤ norma del padre × compensación SSC × máximo absoluto de escala local. La distancia del origen del hijo ≤ distancia del origen padre + norma del padre × cota de norma de traslación local. Los recíprocos SSC exigen intervalos del padre separados de0; si no se cumple, la herramienta falla sin inventar una cota finita.

SHP1 identifica posiciones realmente usadas por cada DRW, con carry de slots65535. Para cada grupo se encierra su AABB local; EVP aplica las inversas bind reales y la suma ponderada real de matrices. Las desigualdades de norma y de triángulo incluyen todos los puntos de esa caja. No se presupone que los pesos sumen exactamente1. Los cálculos de norma se redondean hacia arriba a enteros mediante comparaciones de cuadrados racionales; el último radio también se redondea hacia arriba.

| Dominio relativo a current.pos | Radio superior matemático, HIO1.5 |
|---|---:|
| Cuerpo animado/skinned | 401 |
| Geometría del arma anclada | 494 |
| Esfera corporal backbone R50 | 238 |
| Esfera corporal cabeza R45 | 357 |
| Esfera del arma offset70,R45 | 501 |
| Esfera del arma offset20,R30 | 411 |
| Unión cuerpo/arma/colliders/Acch | **501** |

Son esferas que contienen sobreaproximaciones, **no** tamaños exactos ni radios de ataque nativos. Los centros de colisión se obtienen de joints1/17/12 y offsets(10,10,0)/(10,0,0)/(0,0,70)/(0,0,20); el radio nativo se suma después, no se escala1.5 automáticamente. Acch R60/100,H70 es otro componente, incluido conservadoramente en501.

## Diagnósticos de poses: separados de la prueba continua

Se reconstruyeron bind, WAIT frame0 y ataques5/6 con pasos0.5,182 poses en total contando bind. Usan trigonometría double, callback0, actitud0, HIO1.5 y sin morph. No reproducen tablas JMath/F32 exactas del host. Todas las muestras quedan dentro de las cotas anteriores.

| Pose/clip diagnóstico | Máximo radio corporal observado | Máximo radio de arma observado |
|---|---:|---:|
| Bind,1 pose | 256.574 | 270.302 |
| WAIT0,1 pose | 198.545 | 114.614 |
| ATTACK_B,85 poses | 249.277 | 283.490 |
| ATTACK_C,95 poses | 245.324 | 300.140 |

WAIT0 aproxima AABB corporal X[-88.514,54.038],Y[-0.124,180.759],Z[-16.104,143.291]. Extremos de piernas25/28 Y~8.952; son joints, no el punto inferior del pie. ATTACK_B alcanza arma Y[-15.297,254.517] y Z[-226.671,252.399] en esas muestras; ATTACK_C llega a radio de arma300.140. El muestreo muestra por qué el arma no puede sustituirse por el centro del actor. No demuestra ausencia de contacto con suelo o geometría entre frames.

## Límites indispensables

La cota continua es rigurosa para el **modelo matemático de recursos** declarado; **no es un certificado de aritmética F32/JMath/render-interpolation/driver del engine**. No se reproducen todos esos redondeos ni se inventa un epsilon como garantía. Rotaciones ideales y morph convexo son condiciones explícitas, contrastadas con la ruta nativa; HIO efectivo1.5 y ausencia de overrides aún deben acreditarse en el entorno pertinente. Números decimales en resúmenes son presentación; los radios enteros se calcularon desde fracciones.

Tampoco acota el desplazamiento de current.pos, correcciones de colisión, persecución, daño/caída o transiciones. Rango2000 no equivale a un disco duro de confinamiento. No se afirma una envolvente mundial permanente de radio2501/2801. Contacto de pies con pendientes, recurso efectivo/runtime y ausencia de interferencia siguen pendientes, como explica [POSITION_REASSESSMENT](POSITION_REASSESSMENT.md).
