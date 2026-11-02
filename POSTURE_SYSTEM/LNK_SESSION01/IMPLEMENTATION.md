# LNK SESSION01 0.10.0: LNK02 + LNK03 + LNK04 + LNK07

| Campo | Valor |
|---|---|
| Base | LNK01 0.9.0, commit compilado `10dff331f2013965cee41e4890a8585489478a92` (validado por el usuario: `LNK01_HUMAN_PASS_ACOTADO`) |
| Rama fuente | `feature/posture-lnk02-03-04-07-player-posture` |
| Commit de código | `9453e603c3db5b37c90affec5c619e89ae267cec` |
| Rama CI | `ci/posture-lnk02-03-04-07-player-posture` (desde `eff2eb0`, la base CI de LNK01) |
| ID del mod | `dev.posture.post05_selective_reactions` (sin cambios) |

**Etiquetas de evidencia:**
- **[S]** fuente del host `40457c6`;
- **[B]** EXE oficial 2.0.3 o la DLL compilada;
- **[X]** fuente exacta de Bokoblin Expansion 0.17.0 (`192a773`);
- **[L]** laboratorio (`LAB_MODEL_ONLY`);
- **[H]** humano (pendiente).

## 1. Un único contador

`lnk01::Posture` sigue siendo el **único** contador. Los eventos, en el orden obligatorio, son:

1. Identidad de Link (`observe_link`; Link nueva o ausente ⇒ reinicio a 0 y pendientes descartados).
2. Identidad y generación del atacante (ledger de 64 slots; una identidad nueva no hereda nada).
3. Frescura del contacto (`ArmTrack` de FIX02, a través del veredicto POST08).
4. Clasificación: parry ⇒ bloqueo ⇒ golpe directo, decidida por la marca nativa `AtShieldHit`.
5. Atribución (solo golpe directo).
6. Duplicados: **un resultado por token de ataque**, bloqueo **o** directo, nunca los dos; un parry excluye ambos.
7. Variante y tipo de golpe.
8. Peso (tabla única).
9. Una sola modificación del contador (`apply`).
10. Reinicio del retraso de recuperación.
11. Publicación a la barra (copia por valor; el HUD de LNK01 no cambia).

## 2. LNK02: golpes directos

**Ruta nativa** [S] (`d_a_alink_damage.inc`):
- `daAlink_c::checkDamageAction` (l. 505–780):
  - con `mDamageTimer != 0` no hay daño (invulnerabilidad);
  - si no, toma el **primer** `mTgCyls[i]` con `ChkTgHit` (l. 526–531);
  - con `TgShieldHit` hay guardia;
  - en `PROC_GUARD_SLIP` no hay daño;
  - en otro caso llama a `setDamagePoint(dmg = potencia At, …, TRUE)`.
- `setDamagePoint` (l. 177–229): resta en `ItemLifeCount` (armadura mágica: rupias) y `mDamageTimer = tiempo de invulnerabilidad`. Con `dmg ≤ 0` no arma el temporizador.
- `dMeter2_c::moveLife` (`d_meter2.cpp:599–640`) aplica `ItemLifeCount` a la vida en el `_execute` del medidor.

**Detección en el mod** (sin hook nuevo ni lectura nueva del colisionador del enemigo):

1. **Contacto (PRE de `damage_check`):** veredicto POST08 `NOT_BLOCKED` de un contacto fresco (golpe activo, Link con instantánea de pasada válida, sin `AtShieldHit`).
2. **Atribución (`lnk_pre`, mismo PRE):**
   - se lee el registro Tg de la última pasada de los 3 cilindros de Link (`cCcD_ObjHitInf::ChkTgHit`/`GetTgHitObj` crudos; comparación de direcciones, sin seguir punteros);
   - solo si el **primer** cilindro con impacto registró una esfera de **este** atacante (`tg_match`) queda pendiente. Es el cilindro del que el juego toma el daño.
   - Si no: `REJECTED_DIRECT_NOT_ATTRIBUTED`.
3. **Confirmación (`mod_update` siguiente):**
   - flanco de subida de `mDamageTimer` entre el `mod_update` del tick del contacto y este (Link procesa el impacto en su `execute` de ese mismo tick, antes o después del Bokoblin);
   - y pérdida real de vida: vida actual menor que la del tick anterior, o resta pendiente `ItemLifeCount < 0` aún sin aplicar.

**Rechazos:**

| Resultado | Cuándo |
|---|---|
| `REJECTED_NO_NATIVE_DAMAGE` | Sin flanco: invulnerable, `GUARD_SLIP`, daño 0, estado especial |
| `REJECTED_NO_LIFE_LOSS` | Flanco sin vida (armadura mágica) |
| `REJECTED_AMBIGUOUS` | Dos candidatos del mismo tick para un daño |
| `REJECTED_LINK_CHANGED` | Link cambió o desapareció antes de confirmar |
| `REJECTED_SUPERSEDED` | El slot cambió de identidad o el ataque fue desviado |

- Un flanco sin candidato (lava, caída, objeto) se cuenta como `unattributed_damage_edges` y **nunca** se acredita.
- **Shield chip de Black** [X]: `dComIfGp_setItemLifeCount(-1)` sobre un bloqueo nativo, sin `mDamageTimer`. Es un bloqueo (`AtShieldHit`), no puede ser candidato directo y no produce flanco.

**Offsets medidos en el EXE** [B], con `static_assert` en `mod.cpp`:

| Campo | Offset Win64 | Dónde se midió |
|---|---|---|
| `daPy_py_c::mDamageTimer` | `+0x66c` (s16) | `damageTimerCount` 0x14085e580, `dec word [rcx+0x66c]` |
| `mNoResetFlg0` / `mNoResetFlg1` / `mNoResetFlg2` | `+0x670` / `+0x674` / `+0x678` | — |
| vida máxima / vida | `g_dComIfG_gameInfo+0x48` / `+0x4a` (big-endian `BE(u16)`) | Envoltorios del host con `ror ax,8`; nuestra DLL lee lo mismo con `rol ax,8` |
| `ItemLifeCount` | `+0x98f0` (f32) | Mismos offsets en el desensamblado de `moveLife` y de nuestra DLL |

**Riesgo residual** (documentado): si en el mismo tick Link recibe daño de suelo (lava) **y** un Bokoblin le da en el primer cilindro, `checkDamageAction` aplica el daño de suelo (va antes) y el mod acreditaría el golpe. Es muy improbable y no se puede distinguir sin leer el polígono.

## 3. LNK03: parries

- `CONFIRMED`/`DUPLICATE` de POST08 ⇒ `REJECTED_PARRY`, con **+0** para Link (`kParryCostPoints = 0`).
- El token queda marcado como desviado: ningún contacto posterior de ese ataque puede ser bloqueo ni golpe directo.
- El +40 del enemigo sigue saliendo solo de `post08_step`/`apply_parry`. POST08 no se ha tocado: `parry_core.hpp` es idéntico al de 0.8.2 y 0.9.0.
- **Telemetría:** `LNK_S1_PARRY event=PARRY_CONFIRMED_POST08 enemy_credit=… link_credit=+0 excluded=BLOCK+DIRECT_FOR_THIS_ATTACK`.
- Black en furia en la ventana del Shield Attack (`FURY_CHIP_POSSIBLE`): sin parry y con bloqueo ordinario con peso de furia (+35). El chip de Expansion no cambia.

## 4. LNK04: recuperación por vida y guardia

- **Vida:** `getLife()` y `(getMaxLife()/5)*4`, en las mismas unidades que usa el medidor (`moveLife`). Proporción en milésimas.
- **Bandas** (`kBandPointsPerSecond`, provisional, nunca crece al bajar la vida):

  | Vida | Recuperación | Con guardia segura (×1,5) |
  |---|---|---|
  | 75–100 % | 10 pts/s | 15 pts/s |
  | 50–75 % | 8 pts/s | 12 pts/s |
  | 25–50 % | 5 pts/s | 7,5 pts/s |
  | menos de 25 % | 2 pts/s | 3 pts/s |

  Sin vida máxima válida se usa la banda más lenta.
- **Guardia segura** (réplica de lectura de `daAlink_c::checkUpperGuardAnime`, `d_a_alink_guard.inc:156-163`, medida en el EXE). Exige a la vez:
  - flag de guardia superior `FLG2_UNK_8000000` sin `FLG0_UNK_2`;
  - simulación activa y Link humana;
  - `mDamageTimer == 0`;
  - `mProcID` distinto de `GUARD_SLIP`, `GUARD_ATTACK`, `GUARD_BREAK` y `CUT_REVERSE`.

  No se lee ninguna entrada de mando. La guardia no acorta el retraso de 30 ticks, y cada impacto válido (bloqueo o directo) lo reinicia.
- **Aritmética:**
  - enteros en milésimas por segundo × 2, con resto exacto por tick;
  - un tick por `mod_update`, nunca por FPS;
  - congelada en pausa, eventos, menús, muerte y con Link ausente;
  - el cambio de banda conserva el resto;
  - siempre en `[0, 100]`.

## 5. LNK07: variantes y pesos

**Identidad** [X], según CP10.4, CP10.5 y CP10.6 de Expansion:
- recurso `E_OC` o `E_OC2`;
- potencia At de las dos esferas en la pasada del contacto, que es la que se lee en el PRE: Expansion la cambia en el POST de `execute`, antes de la pasada.

| Firma | Variante | Método |
|---|---|---|
| E_OC, potencia 1 o 2 | Blue (con potencia 2: grupo) | `E_OC_RESOURCE` |
| E_OC2 con potencia 1 en esta generación | Blue normal o legado de DEVF (con 2 después: grupo) | `E_OC2_ATP1_LEGACY_BLUE` |
| E_OC2, potencia 2 y nunca 1, 3 ni 6 | Red | `E_OC2_ATP2_RED` |
| E_OC2, potencia 3 | Black | `E_OC2_ATP3_BLACK` |
| E_OC2, potencia 6 (300 ticks tras perder vida) | Black en furia | `E_OC2_ATP6_BLACK_FURY` |
| Potencia transitoria en un Black conocido | Black | `E_OC2_BLACK_HISTORY` |
| Cualquier otra firma | Unknown (fila mínima, nunca Black) | `UNKNOWN_ATP` |

La historia de potencias es por slot, id y generación: un reciclaje no la hereda.

**Limitación:** un Blue legado de DEVF que nace ya en grupo (potencia 2 sin haber tenido nunca 1) es indistinguible de un Red. Se clasifica como Red (+5 sobre Blue en grupo) y queda registrado por su método.

**Pesos** (tabla única `kWeights`, provisional):

| Variante | Bloqueo | Golpe directo |
|---|---|---|
| Blue | 20 | 30 |
| Red | 25 | 35 |
| Black | 30 | 40 |
| Black en furia | 35 | 45 |
| Unknown | 20 | 30 |

**Ataques especiales:**
- E_OC tiene un único ataque nativo (`ATTACK`, clips B/C, `AtSpl = 0`, misma esfera; `d_a_e_oc.cpp:83-93`). No hay ataques grandes ni enormes demostrables.
- La única diferencia de potencia demostrable fuera de la variante es el **buff de grupo Blue** de CP10.6 (potencia ×2): `kGroupPowerAdjust = +5/+5`.
- No hay multiplicador por velocidad de ataque: un Black más rápido acumula más por tener más contactos.

## 6. Escrituras, hooks e imports

- **Ningún hook nuevo:** siguen siendo 6 `HOOK_MEM`.
- **Ningún import nuevo:** la vida, los flags y el temporizador son lecturas inline.
- **Ninguna escritura nueva:** las únicas escrituras siguen siendo las de 0.9.0 (actor POST05/06/08 y las dos visuales de LNK01).
- **Lo que la auditoría de fuente prohíbe:** `setItemLifeCount`, `setDamagePoint`, `setLife`, `ClrTgHit`, `procGuard*`, `field_0x2fd5` y cualquier escritura a través de un puntero fuera de los escritores auditados.
- **Lo que no se toca:** `procGuardBreakInit`, `field_0x2fd5` y la vida de Link. A 100 no hay ruptura física (LNK05/06).

## 7. Telemetría

- **Arranque:** `LNK_S1_INIT` (versión, commit, host y `build_id`, componentes, pesos, coste de parry 0, bandas, guardia y estado ABI).
- **Eventos:**
  - `LNK_S1_DIRECT`, hasta 150;
  - `LNK_S1_PARRY`, hasta 80;
  - `LNK_S1_REGEN` (inicio, cero, pausa, cambio de banda o de guardia), hasta 120;
  - `LNK_S1_BALANCE`, hasta 120.
- **Resumen:** `LNK_S1_SUMMARY tag=… part=1/2 y 2/2`.
- **Se conservan:** `LNK01_*`, `POST08_SUMMARY`, `POST06_SUMMARY`, `POST05_*` y `POST07_HUD_SUMMARY`.

## 8. Resultados del CI (run 41506630106, MSVC 14.51)

- Compilación e `independent-download` correctas.
- 13 laboratorios sin fallos: los 12 heredados con los mismos conteos que 0.9.0, más `lnks1_lab` con 178 comprobaciones.
- 194/194 mutaciones detectadas: 168 heredadas (4 reapuntadas a la tabla nueva) + 26 nuevas.
- `SOURCE_AUDIT_PASS`, y `PE_AUDIT_PASS` con el pin de LNK01 sin cambios; 14/14 negativos rechazados.
- **Auditoría del binario descargado:** las funciones nuevas solo escriben en datos propios del mod. Sobre Link solo hay `cmp`/`test`.

Datos del artefacto en `RESULTS.json`; evidencia en `EVIDENCE/ci_41506630106/`.
