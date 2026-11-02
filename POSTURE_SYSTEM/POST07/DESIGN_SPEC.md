# POST07 0.7.0: especificación visual de la barra de postura

**Ámbito:** solo visualización. La barra lee copias de la postura (POST04) y de la fase de POST06. Nunca escribe en el actor, la postura, POST05 ni POST06.

**Fuente:** `POSTURE_SYSTEM/POST05/src/hud_core.hpp` (núcleo puro) y el bloque `POST07` de `src/mod.cpp` (pegamento con el juego).

**Etiquetas de evidencia:**
- [S] fuente leída;
- [B] binario/EXE;
- [L] laboratorio;
- [C] CI;
- [R] log real;
- [P] pendiente de humano.

## 1. Lenguaje visual

Barra **fina, oscura y estilizada**, de inspiración Sekiro. Es una paleta y una geometría **originales**: no se copia ninguna imagen, textura ni código de Sekiro.

- **Cuerpo:** plano, con **puntas afiladas**. Cada punta tiene 4 escalones que se estrechan linealmente de 1,3 a 0,15 unidades de semialtura.
- **Doble borde sutil:**
  - marco exterior bronce, de `0x8C6A36` (arriba) a `0x4A361C` (abajo);
  - línea oscura de 0,2 entre el bronce y el núcleo;
  - pista oscura con degradado vertical, de `0x241C14` a `0x0C0906`.
- **Halo:** suave y oscuro detrás, para dar contraste sobre fondos claros, con desvanecido horizontal en las puntas.
- **Muescas:** dos pequeñas, en el centro (arriba y abajo). Marcan el origen del relleno.
- **Sin texto:** ni números, ni "75/100", ni etiquetas, ni porcentajes.

## 2. Posición (respecto a Enemy Health Bars CP06)

La unidad es la del espacio ortho del pintor 2D: alto lógico 448. Por tanto:
- 1080p: 2,41 px por unidad;
- 2160p: 4,82 px por unidad.

**Ancla:** `(sx, sy)` es la proyección del **mismo ancla** que usa EHB CP06 [S `tracker.cpp`/`normal_runtime.h`], reimplementada de forma independiente:
- altura estable de cabeza:
  - `attention.y - pos.y`;
  - si no vale, `eye.y - pos.y`;
  - si tampoco, 55;
  - solo sube, como mucho 3 por tick;
- más 8.

**Barra de vida de EHB** [S `normal_renderer.h`]: `x ∈ [sx−14, sx+14]`, `y ∈ [sy−2, sy+2]`.

| Elemento | y (relativo a sy) | x (relativo a sx) |
|---|---|---|
| Barra de vida EHB (referencia, no la dibuja este mod) | −2,0 … +2,0 | ±14 |
| Franja libre mínima | +2,0 … +2,5 | — |
| Halo | +2,8 … +6,6 | ±14,6 (desvanecido) |
| Marco | +3,4 … +6,0 (centro +4,7) | ±14 (cuerpo ±11,5 + puntas 2,5) |
| Núcleo, donde va el relleno | +4,0 … +5,4 | ±12,42 (incluye la parte afilada) |
| Pulso de ruptura (máximo) | ≥ +2,7 | hasta ±17 |

**Garantías del laboratorio:**
- `H05`: ninguna primitiva, en ningún estado ni fase del pulso, sube por encima de `sy+2,5`.
- `H21`: la colocación no depende de que EHB esté cargado.

**Sin EHB:** se usa la misma posición. La barra flota justo encima de la cabeza, donde iría la barra de vida. Es contextual porque sigue al actor con la misma regla de ancla.

**Alineación exacta:** `LAYOUT_PARTIAL`. Solo una captura humana con EHB activo puede confirmar el píxel exacto (`PIXEL_ALIGNMENT_PASS` no se declara).

## 3. Relleno

- **Fracción:** `f = clamp(P/100)`.
- **Extensión:** `E = f · 12,42`. Crece **desde el centro hacia los dos extremos** a la vez y se retrae de los extremos hacia el centro.
- **Forma:** dos mitades que se tocan en `sx` y entran en las puntas afiladas siguiendo su perfil.
- **Brillo:**
  - centro un 22 % más oscuro y extremos un 10 % más claros;
  - parte superior iluminada y parte inferior sombreada;
  - línea de brillo en el tercio superior.
- **Color por postura:**

| P | Color |
|---|---|
| 0 | oro `0xF2C85A` |
| 50 | ámbar `0xF09E2A` |
| 80 | naranja `0xF0661E` |
| 100 | rojo `0xD82E14` |

  El canal verde nunca sube (`H06`).
- **Resplandor:** un resplandor cálido del tramo lleno asoma por los bordes del marco.

## 4. Señales

| Señal | Disparador | Efecto | Duración |
|---|---|---|---|
| Golpe | la postura objetivo sube | relleno aclarado un 35 %, extremos blancos y calientes, más resplandor | 6 ticks |
| Recuperación | la postura objetivo baja | extremos pálidos y fríos (`0xFFE8B0`) mientras el relleno se retrae | 15 ticks |
| Ruptura | flanco `latched` de falso a verdadero (cruce a 100) | anillo de brasa `0xFF6A24` que se expande tras el marco y destello blanco sobre el relleno; **una vez por cruce** | 20 ticks |
| Rota | `latched` = 100 | relleno rojo profundo `0xC0200E` que respira hacia `0xFF5A26`; marco teñido | mientras dure |

**Ritmo de la respiración:**
- STAGGER_OPEN: periodo de 40 ticks.
- FALLING y DOWN_FINISH (ventana de Finish): 24 ticks.
- GETTING_UP: fija y atenuada al 80 %.

**Suavizado en tiempo de simulación** (30 Hz):
- **Subida:** `max(50 % de la diferencia, 2 puntos)` por tick. Llega en 5 ticks o menos para un golpe de +25.
- **Bajada:** `max(12–16 % de la diferencia, 0,2 puntos)` por tick. La regeneración de 1 punto se ve continua.
- **Determinista:** los fotogramas de presentación no hacen avanzar nada.
- **Pausa y menú:** congelan todo.

## 5. Política por estado de POST06 0.6.1

| Estado | HUD |
|---|---|
| TRACKING 0..99 | normal. Oculta con postura 0 y sin animación (alfa a 0). |
| Cruce a 100 | se llena y lanza **un** pulso |
| STAGGER_OPEN | aspecto roto, respiración lenta |
| Escudo preparatorio | sigue `latched`: **sin segundo pulso** |
| Golpe decisivo de espada o Helm, y paso a FALLING | sigue rota |
| FALLING / DOWN_FINISH / GETTING_UP | sigue rota (100) y **nunca baja a 0 antes de tiempo**. Respira rápido en la ventana de Finish y se atenúa al levantarse. No se oculta. |
| Rearme | se retrae a 0 y luego se desvanece |
| Aturdimiento perdido (100 → 50) | se retrae a 50, sin pulso |
| Muerte, retiro o identidad nueva | se **oculta en el mismo tick** (sin barra fantasma ni desvanecido sobre un ancla que ya no existe) |
| Congelado (POST04 no verificado) | se oculta, conservando la identidad |

## 6. Visibilidad

Mismas reglas que EHB:
- en pantalla, dentro de un margen de ±80;
- apuntable (`attention_info.flags & 7`);
- con línea de visión: `dCamera_c::lineBGCheck` hasta 45 unidades antes del ancla, con banderas `0x40b7`;
- distancia menor de 4500, con desvanecido entre 3700 y 4500;
- se excluyen `actor_status & 0x1000000` y `actor_condition & 4`.

**Además:**
- Solo se ve si hay contenido: postura > 0, animación activa o estado roto.
- **Presupuesto:** se pintan como mucho 16 barras, las más cercanas primero. El resto se sigue animando pero no se pinta.
- **Coste:** 51 primitivas como máximo por barra, así que 816 por fotograma como máximo.

## 7. Restricciones de render

- El alfa se limita a 254. `J2DGrafContext::setColor` desactiva la mezcla cuando las esquinas TL y BR tienen alfa 255 [S `J2DGrafContext.cpp:113-123`].
- `fillBox` intercambia los colores de las esquinas inferiores [S `:147-156`]. `j2d_args()` lo compensa (`H07`, `H27`).
- **Sin anti-aliasing:** el renderizado de referencia muestrea un punto por píxel, como GX. A 720p la línea oscura de 0,2 unidades mide unos 0,3 px y puede no verse. El marco (≥ 4 px) y el núcleo (≥ 2,2 px) sí se ven (`H14`).
