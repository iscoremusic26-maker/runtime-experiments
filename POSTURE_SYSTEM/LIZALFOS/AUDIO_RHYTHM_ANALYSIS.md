# Referencias de ritmo del Lizalfos: análisis de los cuatro audios

Fuente: `docs/lizalfos-audio-refs` @ `7caf6a50a0c8c7e4f308608884ce3903cc0f4e78`, `POSTURE_SYSTEM/LIZALFOS/AUDIO_REFERENCES/LIZALFOS_4_PATRONES_AUDIO_ORIGINALES.zip`. Este informe no incluye audio crudo ni rutas personales.

## Método y límite
No se decodificó la forma de onda: el entorno bloqueó ejecutar un decodificador externo y no se sorteó ese bloqueo. Se usó un analizador de Python estándar que lee la tabla de muestras MP4 y la cabecera de cada bloque AAC-LC (44,1 kHz, 23,2 ms por bloque). Mide el tamaño en bits por bloque y `window_sequence`, y usa los picos como aproximación a los transitorios.

Es una **corroboración parcial, no una medición de forma de onda**. La resolución es de un bloque y el codificador genera picos adicionales. La autoridad es la ficha aprobada por el usuario (sección 05 del encargo); no se reabrió el número de impactos.

## Resultado (picos de tamaño de bloque con el umbral que da exactamente N impactos)
| Patrón | Duración | Intervalos medidos (s) | Ficha (s) | Lectura |
|---|---|---|---|---|
| P1 (4) | 3,90 | 0,88 / 0,51 / 0,12 | 0,50 / 0,13 / 0,63 | se reconocen 0,51 y la pareja 0,12 |
| P2 (7) | 5,67 | 0,53 / 1,21 / 0,53 / 0,09 / 1,32 / 0,49 | 0,58 / 0,60 / 0,54 / 0,10 / 0,66 / 0,67 | 0,53, la pareja 0,09 y 1,21 ≈ 0,60+0,60 (pico perdido) |
| P3 (9) | 5,11 | 0,95 / 0,14 / 1,04 / 0,09 / 0,56 / 0,60 / 0,51 / 0,12 | 0,12 / 0,52 / 0,53 / 0,10 / 0,54 / 0,61 / 0,52 / 0,11 | los últimos cinco coinciden (±0,02); 1,04 ≈ 0,52+0,53 |
| P4 (6) | 6,20 | 0,56 / 1,37 / 0,42 / 0,84 / 1,25 | 1,34 / 1,26 / 0,52 / 0,11 / 0,63 | 1,37 y 1,25: las dos pausas largas de cola |

Coincide lo que define la identidad de cada patrón: parejas de unos 0,09–0,14 s, normales de unos 0,5–0,6 s y pausas de cola de unos 1,3 s. Los valores que no encajan con la ficha son picos perdidos o de más por el método, no una nueva lectura de los impactos.

## Ritmo programado en el juego
Lo calcula el laboratorio de producción (`tests/liz_lab.cpp`, líneas `LIZ_RHYTHM`) y lo registra el CI en `run-lab26.log`. Se mide de apertura a apertura de ventana AT, a 30 ticks/s. Todos los intervalos entre acciones quedan a ±1 tick de la ficha.

La pareja D1→D2 **no alcanza** los 0,10–0,13 s grabados. Las dos ventanas son del mismo clip, separadas 12 frames, y el encargo fija una sola velocidad x1,10 para el clip completo: 0,367 s de apertura a apertura y 0,18 s como mínimo entre cierre y apertura. Esta desviación es física y queda registrada. Se conserva lo que el encargo prioriza: dos ventanas reales, dos parries físicos independientes y que la pareja siga siendo el intervalo más corto de cada patrón.
