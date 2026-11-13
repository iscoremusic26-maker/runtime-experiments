# 0.13.6 FIX06 — Matrices

Laboratorios locales (g++ con ASan/UBSan) sobre el código de producción. El CI público ejecuta los mismos con MSVC. Que un laboratorio pase no es una prueba en el juego.

## P0 Jump Strike (`kk_world_lab` `lab_fix06`, `liz_world_lab` `w_fix06`, `balance_lab`)

| Caso | 0.13.5 | 0.13.6 |
|---|---|---|
| Chilfos HP 280, postura 0, corte 19 a 400 | muerte `HP_ZERO` 280→0 (log) | vivo, 245, +8 |
| Misma fase repetida y fase 20 del mismo salto | daño nativo cada vez | sin HP ni postura (`js_dupes`) |
| Jump Strike nuevo | — | otro crédito de −35 / +8 |
| Fases 18/19/20 × HP {340, 300, 36, 30, 3, 2, 1} | muerte con HP bajo | nunca por debajo de 2 (E_KK); con HP 1 el motor no procesa |
| En el suelo + tajo ordinario | — | el tajo mata (`HP_ZERO`) |
| Chilfos roto + Jump Strike | muerte instantánea nativa | vivo, tambaleo mantenido (`js_breaks_kept`) |
| Bloqueo o parry de un Jump Strike | HP intacto | HP intacto |
| Lizalfos HP 350, postura 6, corte 20 a 400 | 350→0 (log) | 315, +10 una vez |
| Lizalfos HP 20 + Jump Strike / luego tajo | muerte | 1 / el tajo mata |
| Bokoblin, peso del Jump Strike | 25/17/13/13 por fase | 40/27/21/21 una vez, 0 en las demás fases |

## P1 / P2 defensa del salto (`kk_world_lab`)

| Matriz | Resultado |
|---|---|
| 100 saltos, racha 4 (FIX05 + FIX06) | 76 parries (59 en el aire + 17 al aterrizar), 21 bloqueos, 3 daños; ningún bloqueo o parry pierde HP |
| Retroceso al aterrizar (P2) | 59 parries aéreos → 59 retrocesos nativos `ANM_CUT_RECOIL_B`, uno por salto, ningún otro salto |
| Lizalfos, matriz de saltos | 50/50 parries aéreos y 50/50 al aterrizar, 0 HP perdido |
| Spam de saltos de frente, 60 s | 0.13.5: 30 saltos, 9 parries, 17 daños, 68 HP, Link golpeado 19 veces · 0.13.6: 21 saltos, 6 parries, 14 daños, 56 HP, Link golpeado 27 veces |
| Spam de saltos en el borde, 60 s | 0.13.5: 27 saltos, 8 parries, 15 daños, 60 HP · 0.13.6: 23 saltos, 4 parries, 17 daños, 68 HP, Link golpeado 27 veces |

Lectura honesta de la tabla:
- En el escenario de frente, el Chilfos pierde menos HP y golpea más a Link.
- En el borde, el Chilfos pierde 8 HP más y Link recibe más golpes.
- El laboratorio no interrumpe el spam de Link cuando recibe golpes. En el juego, esos golpes cortarían su ritmo.

## P3 cadena (núcleo, 4000 contraataques completados)

| Medida | Resultado |
|---|---|
| Cadenas | 65,7 % (2628 de 4000) |
| Patrones 1/2/3/4 | 645 / 658 / 700 / 625 |
| Hueco | 4–9 ticks |
| Cadenas dobles | 0 |
| Cadenas tras contraataque cortado | 0 |

Integración: un C3 encadenado (retroceso y lanzamiento) es legítimo dentro de su fase. La lanza nunca se pierde tras un bloqueo.

## P4 Back Slice

| Caso | Resultado |
|---|---|
| Parry preparado | `PARRY_WITHOUT_LINK_RECOIL`, Link +25, contraataque, 0 rebotes, proc 35 intacto |
| Racha | primero sin seguimiento; suelos 35/55/70 y 50/70/85; giro 0x0A00, 0x1000 y 0x1400 por tick |

## P6 chispa (núcleo)

- Golpe dentro de Link (proyección 5) → se dibuja en la cara del escudo (28), a altura 90.
- Golpe delante (60) → punto nativo.
- Golpe bajo → altura 55.

## Mutantes nuevos (todos muertos en local)

**Chilfos (20):**
- `js_no_headroom`, `js_native_loss_kept`, `js_no_floor`, `js_credit_every_phase`, `js_cut_gain`, `js_broken_instant_kill`, `js_native_power`, `js_ordinary_cut_damage`, `js_phases_unbounded`;
- `land_recoil_never`, `land_recoil_not_armed`;
- `twirl_parry_needs_rebound`, `twirl_parry_waits_rebound`;
- `chain_always`, `chain_pattern_bias`, `chain_twice`, `chain_after_cut_counter`;
- `spark_never_moved`, `spark_inside_link`, `spark_height_unclamped`.

**Lizalfos (4):** `js_no_raise`, `js_no_settle_before_reaction`, `js_cut_gain`, `js_credit_every_phase`.

**Suites completas:** las ejecuta el FULL público. El recuento final está en el informe.

## Pruebas existentes ajustadas por cambio de diseño (no debilitadas)

- **`kk_world_lab` FIX03 A1/A2:** para las fases del Jump Strike espera el daño acotado y el suelo, y después la muerte por un tajo ordinario.
- **Matriz de saltos:** separa los retrocesos de aterrizaje FIX06 de los parries de contacto al aterrizar.
- **Estrés de 1000 tajos:** la lanza fuera solo se admite dentro de las fases propias de un C3 encadenado. La proporción de defensas se calcula sobre los tajos defendibles; los que llegan durante un ataque comprometido se descuentan.
- **Guardia garantizada:** se aísla de la tirada de parry del 12 %.
- **`liz_lab`:** tras un contraataque, o cadena rápida o el descanso de siempre.
