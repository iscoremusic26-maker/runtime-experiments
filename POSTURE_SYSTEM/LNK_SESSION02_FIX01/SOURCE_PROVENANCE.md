# LNK SESSION02 FIX01 (0.11.1): procedencia del código y créditos

## 1. Base propia

| Elemento | Valor |
|---|---|
| Mod | Enemy Posture System, ID `dev.posture.post05_selective_reactions` (sin cambios) |
| Base | 0.11.0 LNK SESSION02 |
| Commit compilado de la base | `b68b3ff3c941cca8446f1d36d984170f7eb8b316` (rama `feature/posture-lnk05-lnk06-native-link-guard-break`) |
| `.dusk` base | SHA-256 `6f880aff5d589931e0100879685b6c1efad9b76bb7478a8b1b891b48daecbcc2` |
| CI de la base | run 41534362043, artefacto 13183756914 |
| Rama de esta versión | `feature/posture-lnks2-fix01-manual-shield-extended-vulnerability` |

La rama nace del commit documental `a503461`, hijo directo de `b68b3ff` que solo añade documentación. `git diff b68b3ff a503461 -- POSTURE_SYSTEM/POST05` da 0 líneas: el código de partida es exactamente el compilado en 0.11.0.

**Host:** Dusklight 2.0.3, fuente `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Lo fija `ci/build_windows.py`, y el CI compila contra ese SDK y su biblioteca de importación.

## 2. Origen externo: Lazy Shield Rework 1.0.0 (Kamilink)

| Elemento | Valor |
|---|---|
| Repositorio | https://github.com/kamilink7/lazytweaks-modapi |
| Página | https://twilitrealm.dev/mods/com.kamilink.lazytweaks/ |
| `mod.json` | `com.kamilink.lazytweaks`, «Lazy Shield Rework» 1.0.0, autor «Kamilink» |
| Commit examinado | `62620e726cc0803008408427abe701e42f1b5e33` («updated mod.json and icon») |
| Blob de `src/hooks.cpp` | `a0c7a320f2cd1ced216c69ea7bd73d7b4aa2e271`, verificado con `git rev-parse 62620e7:src/hooks.cpp` |
| Host fijado por LazyTweaks | `DUSKLIGHT_VERSION a775418c667f748724c24283b9bad62ebe2dc48b` |

**Licencia.** El repositorio no contiene ningún fichero LICENSE en ese commit.
- Según el usuario, el autor autorizó públicamente el uso libre de su código en un vídeo.
- **No** he podido comprobar ese permiso ni el vídeo, y no se indica ninguna URL.
- Antes de cualquier publicación definitiva hay que conservar la evidencia del permiso.
- Esta versión es solo PRIVATE TEST.

**Créditos:**
- La lógica de la defensa manual (R para guardar, R+B para el Shield Attack) está adaptada de Lazy Shield Rework, de Kamilink.
- El crédito aparece en `mod.json`, en `LNK_FIX01_INIT` y en este documento.
- No se ha copiado el repositorio de LazyTweaks a nuestros repos ni se empaqueta su `.dusk`.

## 3. Qué se ha adaptado (y cómo difiere)

Los 15 callbacks de LazyTweaks se reparten así:

| Callback LazyTweaks | En 0.11.1 | Diferencia |
|---|---|---|
| `setShieldGuard` POST (recalcula y añade `getHoldLockR(PAD_1)` a la rama de fijación) | **Sí**, `on_shield_post_fx` | Solo **apaga** la bandera cuando la encendió la rama de fijación y la defensa no la admite: sin R, en penalización o sin rearme. Es equivalente al recálculo de LazyTweaks, porque el estado no cambia entre el original y el POST, pero nunca enciende nada. `GUARD_SLIP` y la guardia pequeña nunca se tocan. |
| `swordSwingTrigger` POST (FALSE con R pulsado) | **No** | Redundante: `swordTrigger` lee `mItemTrigger & BTN_B`, que ya controla `setStickData`. Además, quitar la espada con solo pulsar R es demasiado amplio. |
| `setStickData` POST (quita BTN_B si R está pulsado) | **Sí**, `on_stick_post_fx` | El consumo es **contextual**. Solo se quita B si R está pulsado, la defensa está en READY **y** el juego ofreció el Shield Attack en el execute anterior, lo que implica que todas sus condiciones nativas se cumplen (técnica aprendida, fijación, escudo, suelo). En cualquier otro caso B sigue siendo la espada. Además se muestrea R desde `mItemButton & BTN_R`, que el propio juego pone a 0 en pausa, eventos y muerte. |
| `procGuardAttackInit` PRE (salta si no hay R+B) | **No** | En el EXE 2.0.3, `procGuardAttackInit` solo se alcanza desde el sitio del Shield Attack (0 llamadas directas; un salto de cola desde ese sitio). Ese sitio ya lo controla `spActionTrigger`. |
| `dComIfGp_setRStatus` PRE (función global) | **Sustituido** por `daAlink_c::setRStatus(u8)` PRE | Mismo efecto con menos superficie. En el EXE, el sitio llama al **miembro** de Link, que salta al global. Enganchar el miembro afecta solo a las llamadas de Link, no a las de otros actores. |
| `spActionTrigger` POST (R+B, `setBStatus`) | **Sí**, `on_spaction_post_fx` | Solo la llamada inmediatamente posterior a la oferta, y FALSE durante la penalización o el rearme. |
| `procWait` / `procMove` PRE (defensa agachada) | **No** | Excluido: defensa agachada. |
| `setSmallGuard` REPLACE | **No** | Excluido: animación de defensa agachada. |
| `procGuardSlipInit` PRE/POST, `setSingleAnimeParam` PRE, `setSingleAnime` PRE | **No** | Excluido: reescritura de animaciones agachadas. |
| `handleQuickTransform` PRE/POST (alfa Z del HUD) | **No** | Excluido: transformación rápida en defensa agachada. |

`checkShieldGet()` (lectura de la partida) no hace falta. La guardia nativa ya exige `checkGuardAccept()`, que comprueba el escudo equipado.

Las rutas añadidas, que no vienen de LazyTweaks y son propias de 0.11.1:
- `checkMoveDoAction` PRE: veto de la admisión de esquivas voluntarias.
- `setCollision` PRE: cierra la bandera residual del frame de salida de `GUARD_BREAK`.

## 4. Revalidación en 2.0.3 frente a `a775418`

Toda la revalidación se hizo sobre la fuente de referencia 2.0.3 (`d_a_alink*.cpp/.inc`, idéntica a la extraída en el pin del SDK) y el EXE 2.0.3 (SHA-256 `ffa992038d042906…`; copia local de referencia, solo lectura).

**Exportaciones:**
- Los seis objetivos y las dos llamadas se exportan con el nombre decorado esperado.
- `getDirectionFromShapeAngle` es inline: se replica solo para clasificar el registro.

**Llamadas reales en el EXE (no inlinadas):**

| Objetivo | Llamadas |
|---|---|
| `spActionTrigger` | 1 directa: el sitio del Shield Attack, precedida de `setRStatus@daAlink_c(0x3a)` |
| `setShieldGuard` | 1, desde `execute` |
| `setStickData` | 1, desde `execute` |
| `checkMoveDoAction` | Desde `checkNextActionFromButton` |
| `setCollision` | Desde `execute` |

**Offsets Win64 medidos en el código máquina** (fijados con `static_assert` en `mod.cpp`):

| Campo | Offset | Dónde se midió |
|---|---|---|
| `mItemTrigger` / `mItemButton` | +0x40e9 / +0x40ea | `setStickData` |
| `mEquipItem` | +0x4138 | `setShieldGuard`; bola de hierro 0x42 |
| `mNoResetFlg2` | +0x678, bit 0x8000000 | `setShieldGuard` |
| `mMoveAngle` | +0x413e | `checkMoveDoAction` |
| `shape_angle.y` | +0x5ca | `checkMoveDoAction` |
| `field_0x2fb0` | +0x410c | `checkMoveDoAction` |

**Resolución de hooks:** en Windows, el host resuelve un miembro no virtual directamente desde la PMF (`resolve_member_record`). El nombre visible del registro `setRStatus`, el texto del `static_cast` que elige la sobrecarga `(u8)`, no interviene.
