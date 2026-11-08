# Light Fades Twice: Lizalfos Duelist FIX01 0.12.1

Estado global: **HUMAN_RUNTIME_PENDING**. Nada de este documento se ha observado en Windows/DX12. Se distingue siempre fuente, log, laboratorio, CI y prueba humana.

## Base elegida
- Fuente compilada 0.12.0 `03111c85b449da0a727b0848f1b70bb555855b60`, documentos `f72445803b7adf6aec2e05ece121fdf833e0728d`.
- Búsqueda de base posterior: `git ls-remote origin` no muestra ninguna rama Lizalfos más nueva que esa. Con los pesos antiguos +22/+15 y la caída directa en la fuente, se trabaja sobre 0.12.0 tal como pide el encargo.
- Log usado (permiso expreso, copia temporal fuera del repo, no publicado): `dusklight-20261108-132436`, 133 671 líneas, 0.12.0 con los otros ocho mods.

## Congelado y comprobado valor a valor
`lab_frozen_rhythm` compara contra la tabla compilada de 0.12.0: frame de entrada y ticks de preparación de las 20 acciones de P1 a P4.

| Contrato | Valor | Dónde se comprueba |
|---|---|---|
| Patrones | P1 N-D-C, P2 N-N-N-D-N-C, P3 D-N-D-N-N-D, P4 C-C-N-D-C | `lab_tables`, `REQUIRED_CORE` |
| Impactos y acciones | 4/7/9/6 y 3/6/6/5 | `lab_tables`, `lab_complete` |
| Velocidades | N 1,25; D 1,10; cola lenta 1,10; cola rápida 1,20 | `lab_tables`, negativo `speed_d_value` |
| Pausas entre acciones | las de 0.12.0, ±1 tick respecto a la ficha | `lab_complete`, negativo `gap_value` |
| D1→D2 | 0,367 s apertura a apertura, sin cambiar | `lab_complete` |
| Sorteo | 25/25/25/25, una tirada por combo | `lab_draw` |
| HP y regeneración | 370, 0 HP/s; postura 10/7/4/2/1 con retardo de 60 | `lab_posture` |
| Postura de Link por parry enemigo | +25 | `lab_counter` |

## Causas raíz

### 1. Golpes mudos y sin parry en D2 y golpes seguidos (P0-4)
- **Comprobado en la fuente:** `d_a_alink_damage.inc:629` es `var_r29->ChkTgHit() && mProcID != PROC_GUARD_SLIP`. Durante `GUARD_SLIP` Link ignora todo registro Tg: sin `setGuardSe` (el sonido del escudo), sin vibración y sin reacción. Tampoco nace un Shield Attack desde ese estado.
- **Duración del slip:** clip de 11 frames y velocidad 14 con frenada de 1,25 por tick, unos 12 ticks.
- **Por qué no pasa en el original:** el juego no da un segundo golpe a un Link que bloquea, porque `e_dn_attack` cancela el doble al primer contacto. 0.12.0 quitó esa cancelación, y D2 cae dentro del slip de D1.
- **Coherente con el log:** en las líneas de contacto registradas (las primeras 400 de `LIZ_SWING`), 25 de 110 parejas de contactos consecutivos del mismo actor están a ≤13 ticks, casi todas a 11 exactos (D1→D2). `link_proc` no se registraba en 0.12.0, así que la coincidencia con el estado de Link se deduce de fuente y tiempos; no se midió directamente.
- **Reproducido en laboratorio:** con el código nativo transcrito, P3 con R mantenido da 3 contactos con registro At y sin sonido en ese tick (`mute == 3`); con la corrección, 0.
- **Corrección:** en el POST de `checkDamageAction`, solo si Link ya estaba en `GUARD_SLIP` en el PRE de esa misma llamada, sigue en él, no tiene i-frames, y hay un registro de escudo real cuyo objeto At es el `at_sph` de un Lizalfos admitido (identidad por puntero), una vez por impacto: llama al `setGuardSe` nativo, al `StartShock` que usa la rama nativa, y renueva `mNormalSpeed` a su valor nativo de 14. **No** re-entra `procGuardSlipInit`, porque sumaría al contador nativo de ruptura de guardia.
- **Chispa:** sale del motor (`ProcAtTgHitmark`) y no depende de este estado. No se fabrica ni se llama.
- **Hook de recibo:** `setGuardSe` POST solo cuenta; no reproduce nada. Es la única prueba observable de audio.

### 2. D2 no admitía parry tras un bloqueo ordinario de D1
El re-armado rápido existía solo tras un parry. Ahora un bloqueo ordinario también arma la cadena de escudo si el combo debe más impactos. Sigue exigiendo una **pulsación nueva real**, el `procGuardAttackInit` nativo y un serial nuevo, y solo mientras la AT está cerrada. Mantener R+B no paga dos veces (`w_double_pair`).

### 3. Trayectoria saltada (colisión entre ticks)
El motor comprueba discos, no barridos. Pasos de centro medidos en el log: N 70–79, D 158–211, cola 134–159 por tick. Con radio 55 + 35 de Link, un paso de D1 puede superar los 180 de cuerda y atravesar a Link sin tocarlo.

Corrección, con el mismo método que CP06 FIX01 en Bokoblins: cuando ningún registro toca y el arma está al alcance, se evalúan **poses nativas exactas** cada medio frame con el `modelCalc` del motor. La pose se restaura y se verifica matriz a matriz; ante un desajuste, la cobertura se apaga en esa sesión y queda en el log. Solo si una de esas poses alcanza un cilindro Tg **activo** de Link con 0,5 de margen, se coloca allí la esfera, con su radio nativo. El motor sigue decidiendo guardia, parry, daño, i-frames y sin-contacto-continuo.

Laboratorio con trayectorias de arco ajustadas al log (no BCK real): 8 de 154 caminos que tocan se perdían sin cobertura, 0 con ella. Ninguno de los 242 caminos limpios genera contacto.

### 4. Bloqueo decidido por la velocidad de la esfera
`ChkShieldFrontRange` usa `AtVec` si no es cero. Un barrido lateral delante de un escudo alzado puede leerse "de lado" y pasar a daño. En el primer tick armado (`StartCAt`) el vector es cero y el motor usa la posición real. Corrección: mientras el Tg de Link tiene el escudo activo, se deja el vector en cero, que es ese mismo estado nativo. La espalda sigue sin bloquear (`w_front_range`).

Es una causa **posible** de golpes que atraviesan el escudo; el log de 0.12.0 no registraba la guardia de Link en cada `DIRECT`, por lo que no se puede cuantificar. `LIZ_IMPACT` ahora registra `link_proc`.

### 5. Shield Attack sin sonido por debajo de 100
0.12.0 limpiaba el registro Tg para evitar el tambaleo, y con él `cc_at_check`, que es quien toca ese sonido. Ahora se llama al `def_se_set` nativo una vez por pulsación.

### 6. Caída automática al cruzar 100
`deliver_break` llamaba directamente a `big_damage`. Ver "Ruptura".

### 7. El nivel C nunca se alcanzaba
Log: `rolls=74/8/0`. Exigía 6 golpes en 150 ticks más 2 impactos no defendidos, la memoria caducaba a 6 ticks, y cada parry de Link la borraba (1 077 parries). Ver "IA".

### 8. Los 356 "watchdogs" no eran fallos
`LIZ_CRITICAL event=STATE code=4` salía en el último tick de los clips de cola y doble: `J3DFrameCtrl::update` escribe `mRate = 0` él mismo al final de un clip `EMode_NONE`, un tick antes de la salida `isStop` nativa. Las líneas registradas (29, porque el resto se quedó sin cupo) están 20–22 ticks antes del fin de combo o sin combo cerca (3). La comprobación era errónea y además reescribía la velocidad en ese tick; se retira. Un clip parado a medias sale por la ruta nativa y el combo sigue (`lab_mid_clip_stop`).

### 9. Los 693 AT_SAMPLE_GAP
Es un diagnóstico de geometría, no un recuento de golpes perdidos. Se conserva. La cifra útil ahora es `collision_gap_fixed` y `impacts_missing`.

## `on_at_hit_post`: auditoría
Devuelve NULL solo en `ACTION_ATTACK`. El único consumidor del retorno en esa función es la rama que cancela (`setPlaySpeed(0)`, `FIGHT_RUN`). Los registros At/Tg, la chispa y la reacción de Link ocurren en la pasada de colisión y en Link, antes y por otra ruta. **No era la causa del silencio**; la causa es el punto 1. En `ACTION_ATTACK_0` no toca nada, y la vibración original de ese ataque sigue.

## Ruptura
| Fase | Qué ocurre |
|---|---|
| Cruce de 100 (parry, espada, bloqueo propio, Iron Ball) | `ACTION_DRAWBACK` nativo, con sus campos de retroceso. Sin caída, sin bandera Down, sin vida fabricada |
| Ventana | 90 ticks absolutos, como `kPunishMaxExec` de Bokoblins. Si el clip de tambaleo termina antes, sigue aturdido en `ACTION_S_DAMAGE`, sostenido por su `timer[0]` |
| HeadLock | Se apaga cada tick mientras no haya preparación: el cruce solo no ofrece Helm Splitter |
| Shield Attack nuevo (serial distinto al del cruce) | Corre la rama nativa `mHitType 16`: sin HP, `DRAWBACK` nativo, HeadLock real. Una vez; no renueva nada |
| Espadazo decisivo (corte nuevo con pérdida real de HP) o Helm Splitter | `big_damage` nativo, `onDownFlg`, Finish nativo. Daño normal, sin multiplicador |
| Sin golpe decisivo | Termina de pie y rearma a 0 |
| Tras caer sin Finish | Levantada nativa y rearme a 0 |

- El corte que cruzó 100 no puede castigarse a sí mismo.
- Iron Ball sin cruzar 100 mantiene su reacción nativa; bombas y demás, también. Esos derribos no rearman la barra.
- Las muertes siempre son nativas.

Depende del juego: Helm Splitter exige que Link tenga esa técnica aprendida y al enemigo fijado (`checkCutHeadState`).

## Balance
+9 espada, +15 parry (uniforme en todo impacto de combo y contraataque), +5 bloqueo, +30 Iron Ball, +25 a Link. Con parries solos hacen falta 7: P1 y P4 pueden terminar sin romperse, P2 y P3 se rompen en el séptimo.

## IA
- **Niveles:** A 12 %, B 35 % (3 cortes reales en 75 ticks), C 45 % (4 en 150). Se quitó la condición de impactos no defendidos, y un parry de Link ya no borra la memoria.
- **Corte real:** una vez por `setCutType`, excluido el Shield Attack, dirigido a ±45° y a menos de 320. Otro Lizalfos no cuenta.
- **Lease:** el mismo corte conserva su única tirada 6 ticks en nivel A y 30 en B/C, para decidir al salir de un estado comprometido. Las fronteras de combo solo usan cortes frescos, para no romper combos.
- **Dos bloqueos reales** de cortes distintos en menos de 90 ticks: una tirada al 80 %. Si sale, se prepara **Normal x1,25 o Doble x1,10 al 50/50**.
- **Parry enemigo:** prepara lo mismo al 100 %. Enfriamiento A 120, B 90, C 60 según el nivel en ese momento.
- **Salida:** desde mode 6/7 con la salida nativa (mode 8). Nunca desde mode 5, porque `ANM_GUARD` aún no ha empezado y ese clip no terminaría.
- **Inicio del contraataque:** primer tick legal en `FIGHT_RUN`, sin depender de `timer[2]`. Exige suelo, sin retroceso, de frente (±67,5°), misma altura, menos de 350 y línea de visión nativa. Gana a una entrada de guardia nativa en ese mismo tick y anula su invulnerabilidad de 15.
- **Fin de la intención:** 120 ticks, más de 600 de distancia, daño de espada, ruptura, evento, muerte, Link ausente. Cada motivo se registra.
- **Después:** el descanso normal y cualquiera de los cuatro combos al 25 %. Los contraataques no cuentan en `selected`.

## Instrumentación
- `LIZ_IMPACT`: clase por ventana (`WHIFF`, `LINK_GUARD`, `LINK_PARRY`, `LINK_BODY`, `IMMUNE_VALID`, `MISSING_FEEDBACK`), `link_proc`, recibos de audio, `event=CANDIDATE_INTERSECTION`. `effect=ENGINE_NOT_OBSERVED`: la chispa no se puede leer.
- `LIZ_COUNTER`: `PRIORITY_ROLL`, `COUNTER_SELECTED`, `GUARD_EXIT`, `ATTACK_COMMITTED`, `AT_OPEN`, `CONTACT`, `EXPIRED cancel_reason`.
- `LIZ_BREAK`: `BREAK_STANDING`, `HELM_PREPARED`, `DECISIVE_HIT`, `DOWN_FINISH`, `GETUP`, `REARM`.
- `LIZ_FEEDBACK`: cada sonido restaurado durante el slip.
- `LIZ_SUMMARY part=FIX01` y `part=PARRY_BY_IMPACT`.
- Todo con cupo; nada por frame.

## ABI y riesgo
- **Nuevo objetivo de hook:** `daAlink_c::setGuardSe` POST (solo recibo). Además, un PRE sobre `checkDamageAction`, que ya estaba enganchada. Ninguno en rutas E_OC.
- **Imports nuevos del juego (4):** `setGuardSe`, `StartShock`, `dComIfGp_getVibration`, `def_se_set`. Total 73.
- **Escritores nativos (12, 6 nuevos):** `stagger`, `hold`, `pose_frame`, `at_place`, `bash_se`, `link_feedback`. Auditados por fuente y por binario.
