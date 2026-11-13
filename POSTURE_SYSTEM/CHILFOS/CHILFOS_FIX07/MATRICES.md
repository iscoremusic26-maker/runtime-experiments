# 0.13.7 FIX07 — Matrices

Laboratorios locales (g++ con ASan/UBSan) sobre el código de producción: el adaptador se incluye literal y el `damage_check` nativo de E_KK y E_DN está transcrito. El CI público ejecuta los mismos laboratorios con MSVC. Que un laboratorio pase no es una prueba en el juego: el laboratorio no simula que los ataques del enemigo golpeen a Link ni interrumpan su spam.

## Cobertura por técnica y enemigo

| Técnica (corte) | Chilfos | Lizalfos | Bokoblin |
|---|---|---|---|
| Back Slice (30) | Guardia efectiva de frente: 105/105 defendidos, 0 HP, un crédito por swing. Espalda o fuera de arco: entra (60). Atacando o roto: sin defensa falsa. Anticipación: guardia sostenida tras el primer Back Slice | Guardia que sube (modo 6, f0–f2) × escudo con/sin cuerpo × ±35°: BLOQUEO, 0 HP. Espalda: entra. Preguardia 65/80 con el primer especial, 80/80 con el tercero, 0/80 de espaldas | HP nativa (sin número acordado) |
| Giro normal (8/22) | 340 → 310, +8; con HP baja muere (HP_ZERO); bloqueo 0 HP, +5; parry sin rebote, +25 a Link | 370 → 340, +10; con HP baja muere por `big_damage` (también desde `small_damage`); bloqueo en `mAtSph`, +9 | Acotado a 30, +40/27/21 (pesos); suelo 2 |
| Giro fuerte (23/24) | 340 → 295, +10 (log: 340 → 0); bloqueo +8; parry sin rebote | 370 → 325, +12 (log: 370 → 0); bloqueo +13 | 45, +50/34/26; suelo 2 |
| Mortal Draw común (26/31) | 340 → 290, +11 (log: 340 → 0); bloqueo +8; un Chilfos no roto vecino de un remate: acotado | 370 → 320, +14 (log: 370 → 0); bloqueo +14; roto: ruta decisiva nativa | 50, +56/38/29; suelo 2 |
| Mortal Draw de remate | Petición B sobre un Chilfos roto: recibo, muerte por la rama letal nativa (`authorized_finisher=1`, `route=MORTAL_DRAW`) | Sin remate propio del Posture System (su ruptura es la caída) | — |
| Jump Strike (18/19/20), Jump Attack (10), Helm Splitter (5) | Sin cambios: pruebas FIX06/FIX05/FIX03 en verde | Sin cambios | Sin cambios |

## P0 Back Slice (`kk_world_lab` `lab_fix07`, `liz_world_lab` `w_fix07`)

| Caso | Resultado |
|---|---|
| Chilfos con guardia nativa efectiva: 7 ángulos (0, ±0x1000, ±0x2000, ±0x2E00 en el borde del arco) × 3 distancias (110/170/230) × 5 | 105/105 defendidos, 0 HP, segundo contacto del mismo swing sin crédito |
| Chilfos con guardia, Link detrás o a ±0x5000 | El Back Slice entra (60), razón `FLANK` |
| Chilfos atacando / roto | Daño `COMMITTED_ATTACK` / estocada decisiva; nunca un bloqueo |
| Chilfos listo en espera, primer Back Slice | Guardia sostenida al tick siguiente (`GUARD_HOLD`), descanso ≥ `kHold`, ningún ataque durante 55 ticks; el siguiente Back Slice de frente: 0 HP |
| Chilfos sin lanza con racha activa | Nunca levanta una guardia que no tiene |
| Lizalfos, 7 técnicas × cuerpo sí/no × fotogramas 0/1/2 × 0°/+35°/−35° | 126/126 BLOQUEO, 0 HP, postura de bloqueo (especial), nunca parry |
| Lizalfos, racha de 5 especiales a 60 ticks (más que el *watchdog* de 180) | Guardia efectiva (modo 5–7) en cada llegada, nunca bajando |

### Spam de 60 s (30 Back Slices, uno cada 60 ticks, contacto 2 ticks después del inicio)

Chilfos (24 de frente, 6 por la espalda), cuatro semillas:

| Semilla | Cubiertos por guardia sostenida | Defendidos de esos | Espalda que entra | Bloqueos | Parries | Daño: comprometido / flanco / sin guardia | Contraataques | Cadenas |
|---|---|---|---|---|---|---|---|---|
| 0 | 8 | 8 | 6/6 | 2 | 6 | 20 / 2 / 0 | 6 | 4 |
| 1 | 5 | 5 | 6/6 | 2 | 5 | 23 / 0 / 0 | 5 | 5 |
| 2 | 4 | 4 | 6/6 | 0 | 6 | 23 / 1 / 0 | 6 | 4 |
| 3 | 9 | 9 | 6/6 | 3 | 7 | 18 / 2 / 0 | 7 | 4 |

Lectura honesta:
- **Guardia sostenida:** el 100 % de los contactos que encuentran la guardia sostenida y de frente se defienden, y ninguno es «guardia batida».
- **De dónde viene el daño:** casi todo el daño restante llega mientras el Chilfos ejecuta su contraataque o el combo encadenado (65 %, política de FIX06), incluida la cola del C3. En el juego esos ataques golpearían a Link; el laboratorio no lo modela.
- **Parry frente a bloqueo:** el Back Slice conserva los suelos de parry de FIX06 (35/55/70 %), así que los parries dominan. Los suelos nuevos de FIX07 para giros y Mortal Draw son menores que los de bloqueo.

Lizalfos: 30 Back Slices de frente, 23 al escudo (17 bloqueos, 6 parries) y 7 al cuerpo, los 7 durante su propio contraataque o combo encadenado. 0 sin guardia, 0 fugas con guardia efectiva.

Referencia humana 0.13.6 [LOG]: Chilfos con `twirl=47/156/1/5/23` y Lizalfos `cut30=59/0/0` (30/30 con `BODY_DAMAGE` en la traza).

## P1 especiales

| Caso | Chilfos | Lizalfos |
|---|---|---|
| Descubierto, HP llena, 6 cortes | −30/−45/−50, +8/+10/+11, un crédito; el mismo swing otra vez: nada; un swing nuevo: otra vez | −30/−45/−50, +10/+12/+14, sin reacción (regla de postura < 100); duplicado: nada |
| HP = daño acotado, +1, +2, 3 | Letal exactamente cuando el resto ≤ 1 (muerte E_KK); `cause=HP_ZERO`, nunca `NATIVE_SKILL_INSTANT` | HP = daño: muere por `big_damage` (golpe fuerte y normal) |
| Guardia efectiva | 0 HP, +5/+8/+8 una vez, lanza intacta, sin reacción | 0 HP, +9/+13/+14 una vez |
| Parry de giro preparado | Sin rebote, +25 a Link, contraataque, proc de Link intacto | 49/120 parries y 71 bloqueos (suelo 40 %), 0 HP, contraataque, sin rebote |
| Postura 95 + giro fuerte | Ruptura a 100 (`LATCH_100`, tambaleo) | — |
| Remate MD autorizado + vecino no roto | Muere el autorizado; el vecino −50 | — |
| MD común sobre Chilfos roto | Estocada decisiva, `BROKEN_DECISIVE_SWORD`, sin recibo | Lizalfos roto: ruta decisiva nativa, sin ruta acotada |

## Bokoblin (`balance_lab`)

- Pesos del especial por variante: Blue 40/50/56, Red 27/34/38, Black y Black Fury 21/26/29.
- El mismo especial otra vez: 0. Un tajo normal conserva su peso.
- Ningún especial rompe a un Blue por sí solo.

## Mutantes nuevos

**Chilfos (20, `test_kk_mutations.py`):**
- `fix07_sk_no_headroom`, `fix07_sk_native_loss_kept`, `fix07_sk_credit_every_phase`, `fix07_sk_never_lethal`, `fix07_sk_lethal_without_death_action`;
- `fix07_hp_native_power`, `fix07_hit_gain_ordinary`, `fix07_block_gain_ordinary`, `fix07_sk_block_plain_credit`, `fix07_block_then_body_damage`;
- `fix07_spin_parry_needs_rebound`, `fix07_spin_parry_waits_rebound`;
- `fix07_md_receipt_missing`, `fix07_md_receipt_any_actor`, `fix07_md_finisher_bounded`;
- `fix07_no_guard_hold`, `fix07_hold_without_rest`, `fix07_hold_forever`, `fix07_no_special_streak`, `fix07_hold_any_state`.

**Lizalfos (15, `test_liz_world_mutations.py`):**
- `lft137_entry_clause_needs_ut2`, `lft137_entry_frames_open`, `lft137_spin_not_link_sword`;
- `lft137_no_pre_guard`, `lft137_pre_guard_any_facing`, `lft137_pre_guard_always`, `lft137_watchdog_not_renewed`;
- `lft137_sk_no_raise`, `lft137_sk_small_dies_in_s_damage`, `lft137_sk_credit_every_contact`, `lft137_sk_gain_ordinary`, `lft137_sk_block_gain_ordinary`;
- `lft137_special_parry_needs_rebound`, `lft137_special_parry_always`, `lft137_broken_bounded`.

## Pruebas existentes ajustadas por cambio de contrato (no debilitadas)

| Prueba | Antes | Ahora | Mutante que cubre el contrato nuevo |
|---|---|---|---|
| `kk_world_lab` FIX03 (A1/A2) | Giro fuerte y Mortal Draw con daño nativo | Daño acotado y muerte cuando el acotado agota la HP | `fix07_sk_no_headroom`, `fix07_sk_never_lethal` |
| `liz_world_lab` `w_fix05_early` | Modo 6 fotograma 1 con escudo y cuerpo tocados (el caso del log de FIX05): exigía `BODY_DAMAGE` | Es la fuga que el encargo manda corregir: ahora BLOQUEO, 0 HP, +5 y sigue sin parry | `lft137_entry_clause_needs_ut2` |
| `liz_world_lab` «guardia que sube no cubre» y regla del cuerpo | La guardia que sube no cubría ni de frente | El caso frontal pasa a la matriz de entrada de `w_fix07`; los de guardia bajando, espalda y lado abierto siguen exigiendo daño, y se añadió «subiendo con Link detrás → daño» | `lft137_entry_frames_open` |
| `liz_lab` `lab_shield` | Igual que la anterior | De frente: invulnerable, 0 HP; detrás: daño | `lft137_entry_frames_open` |
| `liz_lab` ventana de parry (edad 3–4) | Ni parry ni bloqueo | Bloqueo (+5), sin parry | `lft137_entry_frames_open` |
| `liz_world_lab` `kCutSpecs` | `FINISH_STAB` con el número 8, que en el SDK es `TURN_RIGHT` | Valor real del SDK, 0x20 | — |
