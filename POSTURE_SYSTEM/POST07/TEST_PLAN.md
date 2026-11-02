# POST07 0.7.0: plan de pruebas

**Laboratorio:** `tests/hud_lab.cpp`, lógica pura sin juego. Lo compilan con MSVC el CI y con g++ en local.

**Mutaciones:** `tests/run_mutations.py`.

**Tipo de evidencia** (cada fila indica el suyo):
- [L] laboratorio;
- [C] CI;
- [B] binario;
- [P] pendiente de humano.

| ID | Qué se comprueba | Cómo | Evidencia |
|---|---|---|---|
| H01 | Geometría | marco en sy+3,4 … +6,0, ancho total ±14, núcleo ±12,42, perfil y puntas monótonas | [L] |
| H02 | Simetría izquierda/derecha | cada primitiva tiene su espejo con colores espejados (320 estados) | [L] |
| H03 | Relleno desde el centro a los dos extremos | `E = f·12,42`, monótono, dos mitades unidas en `sx`, nada con 0 | [L] |
| H04 | Retracción hacia el centro | de 100 a 0, el tramo nunca crece | [L] |
| H05 | No pisa la barra de vida | toda primitiva, estado y fase del pulso con `y ≥ sy+2,5` | [L] |
| H06 | Color | oro → ámbar → naranja → rojo; el verde no sube; rojizo cerca de 100; valores fuera de rango acotados | [L] |
| H07 | Mezcla de J2D | alfa ≤ 254; el intercambio de esquinas inferiores de `fillBox` queda compensado | [L] |
| H08 | Pulso una vez por cruce | sin pulso por debajo de 100; uno al cruzar; ninguno en STAGGER_OPEN, FALLING, DOWN, GETTING_UP ni con escudo; otro solo tras rearme y nuevo cruce; dura 20 ticks | [L] |
| H09 | Aturdimiento perdido 100 → 50 | se retrae a 50 sin bajar de ahí ni pulsar | [L] |
| H10 | Rearme 100 → 0 | se retrae a 0 y se desvanece | [L] |
| H11 | FALLING / DOWN / GETTING_UP | lleno, aspecto roto y visible; sin 0 prematuro; respiración en la ventana de Finish; atenuado al levantarse | [L] |
| H12 | Pausa | `advance=false` congela todo y no publica | [L] |
| H13 | Suavizado y determinismo | +25 en 5 ticks o menos; regeneración de 1 punto suavizada; `visual()` constante; mismas entradas, mismo estado | [L] |
| H14 | Resoluciones | de 720p a 2160p: marco ≥ 4 px, núcleo ≥ 2,2 px, separación visible; independiente del ancho (4:3, 16:9, 21:9) | [L] |
| H15 | Entradas inválidas | NaN/inf en ancla y alfa, postura fuera de rango, id 0, slot fuera de rango, congelado, tope de primitivas | [L] |
| H16 | Identidad | slot + generación + id; reciclaje sin herencia, clave nueva, sin pulso al ligar; dos actores no se mezclan; ancla reiniciada | [L] |
| H17 | 17 actores | se pintan los 16 más cercanos, ordenados, y se cuenta el exceso | [L] |
| H18 | 64 / 65 | 64 slots ligados; el 65.º y los índices fuera de rango se ignoran; distancias NaN | [L] |
| H19 | Sin barras fantasma | desaparecido o muerto (o fase DEAD): limpiado y sin publicar en el mismo tick; si vuelve, clave nueva | [L] |
| H20 | Visibilidad | puertas de EHB (pantalla, apuntable, línea de visión, distancia 3700–4500); postura 0 oculta; opacidad 0 oculta | [L] |
| H21 | Con o sin EHB | reglas de ancla iguales a las publicadas por EHB; la colocación no depende de EHB | [L] y [P] (captura) |
| H22 | Hilos y actores obsoletos | `DrawRec`/`Frame` solo con valores, sin punteros; el pintor solo lee `hg.frame` (regla de la auditoría de fuente) | [L] y [C] |
| H23 | Lista de dibujo 2D | sin HUD nativo no se encola; encolado; rechazado (no simulación o lista llena); limpieza con compactación y cola nula; `end` falso no se toca | [L] |
| H24 | Regresión POST06 | `Breaker` da resultados idénticos con y sin observador HUD; FIX_REARM50 | [L] |
| H25 | Auditoría PE e imports | `pe_audit.py`: 5 `HOOK_MEM` con thunks de `daE_OC_c` y `dMeter2_c`, 35 imports del juego revisados (4 son ranuras de la vtable de `J2DGrafContext` que emite MSVC), `sqrtf` y `free` del CRT, `InterpService` opcional | [C] [B] |
| H26 | Rendimiento | ≤ 51 primitivas por barra, ≤ 816 por fotograma, coste de `build()` en la CPU del laboratorio | [L] (no es la GPU Intel UHD: [P]) |
| H27 | Renders de referencia | `hud_lab --render`: PNG de 720p, 1080p y 2160p rasterizados desde la lista real de primitivas (modelo GX, un muestreo por píxel). El CI los genera con MSVC | [L] [C] (no son capturas del juego) |
| H28 | Colores de roto y pulso | relleno roto rojo; pulso en brasa | [L] |

## Otros controles del CI

- `break_lab` FIX_REARM50 y los 9 laboratorios heredados.
- 64 mutaciones detectadas:
  - 21 de POST06;
  - 4 de FIX_REARM50;
  - 23 del HUD;
  - 16 negativas de la auditoría de fuente (5 heredadas y 11 del HUD).
- Auditoría de fuente.
- Auditoría PE y negativos PE.
- Muestra del formateador MSVC idéntica a g++.
- Descarga independiente por ID de artefacto.

## Pruebas humanas pendientes [P]

Ver `README_TEST_0_7_0.md`. Sin capturas del juego no hay PASS visual: alineación `LAYOUT_PARTIAL`, `HUMAN_RUNTIME_PENDING`.
