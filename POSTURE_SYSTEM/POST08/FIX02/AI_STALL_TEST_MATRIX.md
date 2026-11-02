# Matriz de pruebas de IA (FIX02)

**Niveles:**
- **LAB:** `parry_lab`, `run_sim2` (`LAB_MODEL_ONLY`, compilado también con MSVC en el CI).
- **SRC:** fuente.
- **HUMAN:** usuario, con `POST08_AI_TRACE`.

| ID | Caso | 0.8.1 | FIX02 | Evidencia |
|---|---|---|---|---|
| A1 | Parry 0 → 40 y Link guarda después | 1 golpe armado / 51 abortados, `SUSPECTED` | 15 / 0, `NORMAL_NEXT_ATTACK_OBSERVED` | LAB (ambos órdenes de ejecución); HUMAN pendiente |
| A2 | Parries repetidos (Shield Attack cada 23 ticks) | 7 parries falsos (residuo) | 0 falsos; 0 daño de golpes declarados parry | LAB |
| A3 | Parry que cruza 100 | bucle tras el mareo | ruptura aplazada; vuelve a atacar (≥ 8 golpes armados) | LAB + POST06 (espera, sin rearme 50) |
| A4 | Guardia normal sin Shield Attack | sin parry, sin bucle | igual | LAB (control: el rebote nativo refresca) |
| A5 | Black en furia | `FURY_CHIP_POSSIBLE` | sin cambios | LAB (T10/T37) |
| A6 | Registro de una pasada no armada, de otra identidad o de un tick viejo | — | `STALE_CONTACT` | LAB (familia 6) |
| B1 | Dos Bokoblins, bloqueo compartido | los dos atascados | los dos atacan | LAB |
| B2 | Tres Bokoblins, ritmos ×1/×1,15/×2, ambos órdenes | — | 0 abortados, 0 falsos, 0 daño en parries | LAB (familia 5) |
| B3 | Espadazos A → B → A sin parry | — | sin cambios de código en POST05 (restauración exacta [S]); monitor `cause=SUPPRESSION` | HUMAN pendiente |
| B4 | Generación reciclada | — | el monitor no mezcla generaciones | LAB (mutación `fix02_watch_any_generation` detectada) |
| C1–C7 | POST04–07, FIX01 y el HUD | — | 10 labs heredados con los mismos conteos; mutaciones FIX01 vigentes | LAB / CI |
| D1–D5 | Mutaciones | — | 130/130 detectadas | CI |

**Monitor:**
- espera nativa con temporizador → no es atasco;
- daño o caída → no es atasco;
- muerte → cierre;
- capacidad de 8 vigilancias;
- caducidad si el actor deja de ejecutarse.
