# POST00 — Traza de daño, reacción, derribo y Finish (E_OC, Dusklight 40457c6)

Rutas relativas al árbol verificado. URL: `https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/<ruta>#L<a>-L<b>`.
Etiquetas de evidencia:
- **[S]**: fuente leída.
- **[B]**: binario `dusklight.exe` (SHA `ffa99203…0049`), mediante el manifiesto `.symdb` y `objdump` (salidas en `VERIFICATION.json`).
- **[R]**: requiere ejecución humana en Windows/DX12 (HUMAN_RUNTIME_PENDING).

## 1. Identidad del actor (§4.1)

| Hecho | Evidencia |
|---|---|
| Una sola clase `daE_OC_c` sirve a los recursos `E_OC` y `E_OC2`. `create()` elige `mName` a partir del byte `(current.angle.x >> 8) & 0xFF`: 0 o 0xFF dan `"E_OC"`; cualquier otro valor, `"E_OC2"` | [S] `src/d/actor/d_a_e_oc.cpp:2734-2739` |
| Después pone a cero `current.angle.x` y `shape_angle.x`, de modo que el parámetro original deja de ser legible tras `create` | [S] `d_a_e_oc.cpp:2808` |
| Firmas que solo escribe `create()` para `E_OC` normal: `health = field_0x560 = 40` (E_OC2: 220); `mSphs_at[0/1].SetAtAtp(1)` (E_OC2: 2); `fopAcM_OnStatus(this, fopAcStts_UNK_0x10000_e)`, que E_OC2 no recibe | [S] `d_a_e_oc.cpp:2771-2779`, `2791-2802` |
| `AVOID_UB=1` en el ABI del juego, por lo que las comparaciones de `mName` usan `strcmp` | [S] `cmake/GameABIConfig.cmake:7`, `d_a_e_oc.cpp:2771-2775` |
| `mName` es `const char*` hacia un literal del propio EXE. Vive tanto como el proceso y solo es legible mientras el actor existe | [S] `include/d/actor/d_a_e_oc.h:106`, `d_a_e_oc.cpp:2736-2738` |
| El perfil (nombre de proceso) es distinto del recurso: el Delete registra `"E_OC"` para ambos | [S] `d_a_e_oc.cpp:2666` |
| Los ID de proceso son enteros monótonos crecientes que no se reutilizan dentro de una sesión | [S] `src/f_pc/f_pc_base.cpp:54-57` |
| Bars usa `fopAcM_searchActorDistance`/`fpcM_SearchByID` y HM valida `fpcEx_SearchByID(id)==actor` | [S] `bars_203_hm/mod/src/game_bars.cpp:48,147`, `hm_203/HM203_OPTIONAL_VITALS_CONTRACT.md` §2.3 |
| DEVF Blue usa el recurso `E_OC` con `atp` 1 (igual que el nativo). Red y Black usan `E_OC2`. DEVF **no publica** ningún servicio para consultar la variante de un actor; sus servicios solo atienden la colocación | [S] CP21 `CP10_5…/damage_policy.hpp:16-26`, `CP10_4…/typed_registration.hpp:46`, `devf_encounter_v11.h` |

**Clasificador propuesto (sin depender del HP):** `actor->name == fpcNm_E_OC_e`, `strcmp(mName,"E_OC")==0`, el bit de estado `0x10000` activo y `mSphs_at[0].GetAtAtp()==1`. El HP inicial 40 sirve solo como corroboración y se registra en el log. Identidad por instancia: el par (`fpcM_GetID`, puntero), revalidado con `fopAcM_SearchByID` antes de cualquier lectura diferida.

**Límite:** un E_OC nativo y un DEVF Blue no se distinguen sin la cooperación de DEVF (la atp coincide y el HP es solo heurístico). Es la decisión pendiente D1 en `ARCHITECTURE_DECISION.md`.

## 2. Flujo de daño por fotograma

```
fpcM execute handler
 └─ daE_OC_Execute → daE_OC_c::execute()                       [S] 2586-2640, 2642-2644
     ├─ decrementa los temporizadores, incluido field_0x6cc     [S] 2599-2601
     │     (en Win64 está en +0x8ec, NO en 0x6cc)               [B] `movw $0x3,0x8ec(%rbx)` @0x140e06785
     ├─ action()                                                [S] 2415
     │   ├─ mSphs_at[0/1].OffAtSetBit()                         [S] 2416-2417
     │   ├─ damage_check()   ← llamada real, sin inline          [B] call 0x14006c4ae → 0x140e06390
     │   │   ├─(1) checkCutDownHitFlg → health=0, DEATH(1), offTgSph, return     [S] 639-647
     │   │   ├─(2) field_0x6cc≠0 → return (invulnerabilidad de 10/20/3 ticks)    [S] 649-651
     │   │   ├─ mStts.Move()                                                     [S] 653
     │   │   ├─(3) TG de las esferas cc[0] y cc[1]: si ambas, gana cc[1]; sin TG → return   [S] 656-670
     │   │   ├─ field_0x6cc = 20 (AT_TYPE_UNK) / 10; con atp ≤1 → 10              [S] 673-681
     │   │   ├─(4) tabla de reacción my_val por tipo de AT (ver §3)              [S] 683-754
     │   │   ├─(5) cc_at_check(this,&mAtInfo) ← llamada real                     [B] →0x8186d0
     │   │   │     at_power_check, mHitDirection, health -= power (piso 0),
     │   │   │     SE de colisión, hit-stop                                      [S] d_cc_uty.cpp:372-500
     │   │   ├─ GetAtSpl()==1 (salvo espada de madera) → my_val=5                 [S] 757-762
     │   │   ├─ health ≤ 1 → attention_info.flags=0; my_val=max(my_val,5)         [S] 764-769
     │   │   ├─(6) CUT_TYPE_JUMP + cancel-turn → DAMAGE(my_val), 0x6cc=3, return  [S] 771-776
     │   │   └─(7) my_val≥5 → setActionMode(BIG_DAMAGE,my_val-5)+offTgSph
     │   │         else  → setActionMode(DAMAGE,my_val); FIN                      [S] 779-785
     │   │         Tras el último setActionMode solo queda el epílogo
     │   │         (comprobación de cookie y ret)                                 [B] 0x140e067a5…0x140e067e3
     │   ├─ leash/field_0x6e3, searchOtherOc, mBattleOn=false                    [S] 2420-2437
     │   ├─ checkWaterSurface → WATER_DEATH (anula cualquier modo previo)         [S] 2439-2441
     │   ├─ checkFall → FALL / FALL_DEAD (salvo BIG_DAMAGE en FALL)               [S] 2449, 2151-2179
     │   ├─ switch(mActionMode) → executeXXX()                                   [S] 2451-2509
     │   └─ posMove, CrrPos, setHeadLockPos, morf play                           [S] 2528-2534
     ├─ mtx_set, cc_set (reposiciona cc[0] R50 torso, cc[1] R45 cabeza, at[0/1]) [S] 2632-2633, 2551-2584
     └─ setMidnaBindEffect                                                       [S] 2638
```

Enumeración de acciones, confirmada en los inmediatos del binario: WAIT 0, WALK 1, TALK 2, FIND 3, ATTACK 4, **DAMAGE 5**, **BIG_DAMAGE 6**, WATCH 7, SOUND_WATCH 8, **DEATH 9**, WATER_DEATH 10, DEMO_MASTER 11, DEMO_CHILD 12, FALL_DEAD 13, FALL 14, FIND_STAY 15, MOVE_OUT 16. [S] `d_a_e_oc.cpp:20-38`; [B] `mov $0x9,%edx`, `mov $0x6,%edx`, `cmp %bpl,%sil` con ebp=5.

**Golpe único:** cada llamada procesa como máximo un collider (cc[1] sustituye a cc[0], líneas 662-666), y el bloqueo `field_0x6cc` impide reprocesar durante 10, 20 o 3 ticks. Por eso, para Posture, «impacto aceptado» significa: en PRE de `damage_check`, `field_0x6cc==0`, no hay CutDownHit y existe TG en alguna esfera. El contacto sin aceptación (con el bloqueo activo) no cuenta.

## 3. Tabla de reacción nativa (`my_val`) y escrituras

| AT / caso | `my_val` | Escrituras antes de `cc_at_check` | Resultado nativo |
|---|---|---|---|
| Espada: corte ordinario | `getCutType()` 0/1/2 (alternancia con `field_0x6d6/6dc`) | `field_0x6d6=30`, `field_0x6dc` | DAMAGE 0/1/2 → `executeDamage` (anim 8/9/10, voz, `speedF=0`) → FIND/MOVE_OUT |
| Espada: combo ≥4, salto, twirl, mortal draw | 5 | — | BIG_DAMAGE 0 |
| Espada: giro / giro grande / head jump | 6 / 7 | Head jump: `health=0` | BIG_DAMAGE 1/2. Head jump: muerte |
| Espada de madera | 2 | — | DAMAGE 2 |
| Escudo (AT_TYPE_SHIELD_ATTACK) | 3 | — | DAMAGE 3 (`speedF ±20`, `onHeadLockFlg`) |
| Flecha | 0/1 (`cM_rnd`) | — | DAMAGE 0/1 |
| Bomba | 5 | `health=0` | BIG_DAMAGE 0 → DEATH |
| Bola de hierro | 5 | `health += 80/140` (literal de la fuente; el `cc_at_check` posterior resta la potencia) | BIG_DAMAGE 0 |
| Bumerán | 4 | — | DAMAGE 4 (anim gale, estado 6) |
| AT_TYPE_40 | 2 | `health += 10` | DAMAGE 2 |
| Tirachinas E_OC | 2 | `health -= 5`; si queda <0: hit mark, BIG_DAMAGE 0, offTgSph, **return sin `cc_at_check`** | DAMAGE 2 (con `cc_at_check`) |
| Tirachinas E_OC2 | — | SE; WAIT/WALK/TALK→FIND; **return** | Sin daño |
| Ataque especial (`GetAtSpl()==1`) | ≥5 | — | BIG_DAMAGE |
| `health ≤ 1` tras `cc_at_check` | ≥5 | `attention_info.flags=0` | BIG_DAMAGE → DEATH si `health<1`; con `health==1` sobrevive derribado (bug que DEVF documenta en `cp19_policy.hpp:11-12`) |

Fuente: [S] `d_a_e_oc.cpp:596-629`, `683-785`, `1534-1601`; `d_cc_uty.cpp:372-500`.

**Efectos que ya han ocurrido cuando vuelve `cc_at_check`:** resta de HP, `mHitDirection`, SE de colisión, hit-stop (`pause_time`), señal de logro `enemy_killed`. Los produce la ruta común, no la reacción.
**Efectos que dependen de la reacción:** animación, voz de daño (`Z2SE_EN_OC_V_DAMAGE*`), `speedF`, `onHeadLockFlg` (escudo) y la transición a FIND/MOVE_OUT. Los produce `executeDamage` en el **mismo** `action()`, después de que `damage_check` retorne.

`setActionMode` (fuente `d_a_e_oc.cpp:584-594`) solo escribe: `mOldActionMode`, `mActionMode`, `mOcState`, `field_0x6c0=field_0x6c2=0`, los bits CoSet/TgSet de `mSphs_cc[0/1]`, y `offHeadLockFlg()` sobre `mFlags`.

## 4. Derribo (BIG_DAMAGE) y Finish

| Paso | Evidencia |
|---|---|
| BIG_DAMAGE 0/1/2: anim 0x13/0x15, voz, `offTgSph`, salto (`speed.y=40`, `speedF=20`), orientación según `mHitDirection` | [S] `d_a_e_oc.cpp:1607-1640` |
| Estado 3: en el aire, `checkDamageBg`; al tocar suelo, anim 0x14, SE y paso al estado 4 | [S] `1641-1669` |
| Estado 4: al terminar la anim, `health<1` → DEATH(0). Si no, `onDownFlg()`, `setStabPos()` (que llama a `setDownPos`) y `field_0x6c0 = 45±10` ticks | [S] `1670-1694`, `818-825` |
| Estado 5: derribado. Si Link está en `CUT_TYPE_DOWN`, se quitan los CoSet y el tiempo pasa a 30. Al expirar: `offDownFlg()` y se levanta | [S] `1695-1714` |
| Estado 6: termina la anim → FIND(5) | [S] `1715-1720` |
| `onDownFlg`/`offDownFlg` son inline en las cabeceras; `offDownFlg` también borra CutDownHit/WolfDown* | [S] `include/f_op/f_op_actor.h:376-399`; [B] manifiesto: `fopEn_enemy_c::onDownFlg` INLINE |
| Link `checkDownAttackState()`: objetivo fijado de grupo ENEMY, `checkDownFlg()`, y además (humano con F_0339 o entrenamiento, distancia a `mDownPos` < 800) o (lobo, solo E_PO/E_HP) | [S] `src/d/actor/d_a_alink_cut.inc:799-822` |
| Origen del botón «Finish»: `checkDoCutAction` → `procCutDownInit`; indicador del botón A con espada (`mEquipItem==0x103`) y bloqueo de atención | [S] `d_a_alink_cut.inc:767-778, 1955, 2370`; `d_a_alink.cpp:10405-10425` |
| `procCutDownInit`: salto hacia `getDownPos`, `CUT_TYPE_DOWN` | [S] `d_a_alink_cut.inc:2058-2134` |
| `procCutDownLandInit`: solo hay acierto si el enemigo **sigue** con `checkDownFlg`, la punta de la espada está a menos de 100 XZ de `mDownPos` y la diferencia en Y es < 100. Entonces `onCutDownHitFlg()` y hit mark. Si no, fallo | [S] `d_a_alink_cut.inc:2151-2193` |
| En el siguiente `damage_check`: CutDownHit → `health=0`, DEATH(1), `offTgSph` (prioridad absoluta, antes del bloqueo) | [S] `d_a_e_oc.cpp:639-647` |
| Una muerte por HP≤1 vacía `attention_info.flags`: no se puede fijar y no hay Finish | [S] `764-766` |

**Respuesta a la pregunta de §4.3:** sí. Si la ruptura de postura entra en el `BIG_DAMAGE` nativo llamando a la función nativa `setActionMode(6, k)` seguida de `offTgSph()` (la misma secuencia que la línea 780-781, sin escribir `mFlags`), el down flag lo pone después el propio `executeBigDamage` estado 4, y solo si el Bokoblin sigue vivo y ya está en el suelo. Como Link vuelve a comprobar el down flag y la geometría al aterrizar, no puede producirse un Finish sobre un actor de pie. Queda **[R]** lo siguiente:
- la ruptura no puede coincidir con un golpe letal, porque eso es DEATH nativa;
- con `health==1` el estado nativo ya es anómalo (ver §3);
- la llamada desde el POST debe hacerse con el actor en un modo «vivo» (ver los vetos en ARCHITECTURE_DECISION §3).

## 5. Ciclo de vida

- `daE_OC_Delete` → `_delete()`: libera recursos y el objeto de sonido. [S] `d_a_e_oc.cpp:2650-2668`. No hay un hook necesario: basta con validar el ID de forma diferida.
- Muertes: DEATH, WATER_DEATH y FALL_DEAD llaman a `fopAcM_delete` (DEVF CP03 SOURCE_REVIEW, citado en `fe47c8b:DEVF/CP03_HP_DIAGNOSTIC/SOURCE_REVIEW.md:9`, líneas 1873/1951/2206).
- Si el actor no ejecuta (pausa, evento que congela, sala descargada), `damage_check` no se llama. Por tanto, un reloj de postura que avance dentro de `damage_check` mide **tiempo de simulación del propio actor**, no tiempo de reloj. [S] `d_a_e_oc.cpp:2418` es incondicional dentro de `action()`.

## 6. Pendiente de runtime [R]

1. Que el detour de `daE_OC_c::damage_check` se instale sin aviso de inline en el host real. El manifiesto no tiene el flag, pero falta el log de Windows.
2. Que el `mOcState` de ATTACK restaurado continúe la animación de ataque sin artefactos (CP02 de Posture).
3. Que el BIG_DAMAGE forzado reproduzca el derribo, la ventana de Finish y el levantamiento nativos.
4. El orden real de los PRE/POST con DEVF y HM activos (log de POST01).
