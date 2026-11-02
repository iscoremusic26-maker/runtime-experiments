# POST08 0.8.0: parry de precisión con Shield Attack (implementación)

## 0. Base y procedencia

| Campo | Valor |
|---|---|
| Base funcional | POST07 0.7.0, código compilado `f0e92c9f1d74d1b2d46447705fe1353cb3833eb8` (run 41392661597, artefacto 13118435513, `.dusk` SHA-256 `070533d7…3afd`) |
| Rama de la base | `feature/posture-post07-hud` en `0dad4e5` |
| Diferencia base ↔ compilado | `0dad4e5` solo añade documentos en `POSTURE_SYSTEM/POST07/`; cero cambios en `POSTURE_SYSTEM/POST05/` (`git diff f0e92c9 0dad4e5 -- POSTURE_SYSTEM/POST05` vacío) |
| Rama nueva | `feature/posture-post08-parry`, desde `0dad4e5` |
| Commit de código | `1eda39a7f603f796e18920dae73e4b12f7d0236a` |
| CI | `ci/posture-post08-parry`, desde `4ecfd42` (cabeza CI de 0.7.0), espejo `e0bd06b` con libro de control SHA-256 (48 archivos) |
| Run CI | 41397088965 (compilación e `independent-download` correctas), artefacto 13118929802 |
| ID del mod | `dev.posture.post05_selective_reactions` (sin cambios) |
| Versión | 0.8.0 |
| Nombre en el menú | "Enemy Posture System PRIVATE TEST" |

## 1. CP08-A: mapa de flujo nativo

Etiquetas: [S] fuente del host `40457c6`; [B] EXE 2.0.3 (SHA `ffa99203…0049`).

**(a) Inicio del Shield Attack**
- `daAlink_c::procGuardAttackInit` → `commonProcInit(PROC_GUARD_ATTACK)` [S guard.inc:374].
- `PROC_GUARD_ATTACK = 0x1e`, `mProcID` en `+0x4144` [B `0x14084f703`: `cmpw $0x1e,0x4144(%rbx)`].

**(b) Fotogramas**
- `ANM_SHIELD_ATTACK` con `daAlinkHIO_gAtPush_c0::m`: anim {end 14, speed 1.0, start 1.0, morf 5.0, cancel 18}, `mAttackStartFrame` 1, `mAttackEndFrame` 12, `mSlashCheckFrame` 14 [S HIO_data.inc:860].
- `procGuardAttack` activa `mGuardAtCps` con el frame en [1, 12) [S guard.inc:478-484]; a 1,0 frame por tick, son 11 ticks.
- [B `procGuardAttack` `0x1408963a0`]:
  - `movss 0x2d4c` = `mUnderFrameCtrl[0].getFrame()`;
  - `comiss 0x45d8`/`0x45dc` = frames de inicio y fin del ataque;
  - `0x45e4`/`0x45e8` = cancelación y comprobación de tajo.
- Cancelaciones: `procCutReverseInit` contra pared y `checkNextAction` al pasar el frame de cancelación.

**(c) Golpe activo del Bokoblin**
- `executeAttack`, estado 1|2 (clip B/C): `OnAtSetBit` de `mSphs_at[0|1]` con el frame del clip en [14, 22] [S e_oc.cpp:1453].
- [B `0x140e073f8`]: `orl $1,0x1038`/`0x11f0`; esferas en `0x1028`/`0x11e0`.

**(d) Confirmación del objetivo**
- `dCcS::SetAtTgGObjInf` guarda el objeto Tg golpeado en el At [S d_cc_s.cpp:541-560].
- El nativo lo resuelve con `GetAtHitAc()` (que escribe una caché). El mod compara la **dirección cruda** con `&link->mTgCyls[0..2]` [B setCollision `0x1408cb349`: `lea 0xb28` = `mTgCyls`, 3 × `0x1c0`].

**(e) Bloqueo o daño a Link**
- `daAlink_c::setCollision` marca los 3 cilindros Tg como escudo frontal mientras `checkPlayerGuardAndAttack()`, que **incluye `PROC_GUARD_ATTACK`** [S alink.cpp:6783-6802; B call en `0x1408cb3b4`; bits en `0xc10`/`0xdd0`/`0xf90`].
- `dCcS::ChkShield`/`ChkShieldFrontRange` → si bloquea: `OnAtShieldHit` en el ataque, `OnTgShieldHit` en Link y **sin `PlusDmg`** [S d_cc_s.cpp:571-577].
- En Link, `TgShieldHit` → reacción de guardia (`setSmallGuard`/`procGuardSlipInit`) y **ningún `setDamagePoint`** [S damage.inc:653-690].
- **Conclusión: durante el Shield Attack el motor ya desvía de forma nativa los golpes frontales.**

**(f) Reacción del Bokoblin al Shield Attack**
- `mGuardAtCps.SetAtAtp(0)` [S alink.cpp:4534] y `AT_TYPE_SHIELD_ATTACK`.
- `damage_check` → `my_val = 3` → `cc_at_check` (potencia 0: **sin cambio de vida**, `if (mAttackPower != 0) health -= …`) → `setActionMode(DAMAGE,3)` → `executeDamage` estado 3: BCK 8 + `HeadLock` [S e_oc.cpp:690-780, d_cc_uty.cpp:440].
- **En la base 0.7.0, POST05 GENERAL ya deshace esa reacción con postura < 100** [R log 0.6.1: `SHIELD_ATTACK decision=SUPPRESS_ELIGIBLE … SUPPRESSION_APPLIED`]. Es la decisión de diseño de 0.5.4 («escudo/bumerán ya no aturden»). 0.8.0 no la cambia.

**(g) Orden de ejecución**
1. Tick N: execute de los actores; en E_OC, el `execute` PRE de Expansion → `action()` → `damage_check` (POST03–07 PRE/POST) → `executeAttack` (pone el `AtSet`) → `cc_set` (registra las 4 esferas).
2. Fin del tick: pasada `dCcS::Move` (`ChkAtTg` limpia las marcas de todos los colisionadores registrados y calcula las nuevas).
3. Tick N+1: nuestro PRE de `damage_check` lee las marcas de **esa misma pasada**, tanto en el At del Bokoblin como en su Tg.
4. El `execute` POST de Expansion (chip del Black) corre después de `action()`.

**(h) E_OC frente a E_OC2**
- Misma clase y mismo `executeAttack`.
- Expansion cambia el ritmo del clip:
  - Red: ×1,15 / ×2;
  - Black: ×1,15 normal, ×2 en furia [S Expansion `mod.cpp:1141,1320`; log `fury_rate=X2 normal_rate=X1_15`].
- El chip de escudo de Expansion afecta solo al Black en furia y se cobra sobre **cualquier** bloqueo nativo de su golpe [S `cp19f2_policy.hpp:12,97-135`].

### Alternativas descartadas
- **Devolver vida a Link:** prohibido, e innecesario porque el motor ya no aplica daño.
- **Congelar la animación o cambiar la velocidad:** escritura de animación prohibida, y Expansion es dueño del ritmo de Red/Black.
- **Proximidad, distancia, sonido o pulsación del botón:** no prueban el contacto.
- **Interceptar cualquier ataque sin identidad:** no.
- **Un hook nuevo sobre Link o sobre el motor de colisión:** innecesario. Basta leer el resultado de la pasada en el hook ya auditado de `damage_check`.

## 2. CP08-B: núcleo puro `src/parry_core.hpp`

- **Entrada (por valor, en el PRE):**
  - identidad y estado de postura;
  - modo, estado y frame/ritmo del clip del enemigo;
  - por esfera At: `AtHit` crudo, «el objeto golpeado es un `TgCyl` de la Link viva» y `AtShieldHit`;
  - Link: viva, `PROC_GUARD_ATTACK`, frame de la animación, inicio y fin del ataque;
  - evento en curso.
- **Episodio:** cada golpe (ATTACK 1|2) recibe un token; se reinicia al entrar al golpe o si el clip retrocede. Dos esferas, callbacks repetidos y los frames siguientes del mismo golpe dan `DUPLICATE`.
- **Orden del veredicto:**
  1. identidad segura;
  2. evento;
  3. golpe activo;
  4. Link válida;
  5. **bloqueo nativo**;
  6. **Shield Attack**;
  7. ya parado;
  8. ya resuelto (tardío);
  9. **ventana**;
  10. latched;
  11. Black en furia;
  12. `CONFIRMED`.
- **Ventana:** `delta = frame_link − inicio ∈ [−1, +5]` frames de `ANM_SHIELD_ATTACK` [TIMING_PROVISIONAL_POST08].
  - 1 frame = 1 tick a velocidad 1,0, así que son 0,17–0,20 s más la holgura de orden.
  - Link puede ejecutarse antes o después del Bokoblin en el tick; esa holgura (−1) cubre la diferencia de lectura.
  - Está ligada al frame real de la animación de Link, no al botón ni a un temporizador propio.
- **Black en furia:** E_OC2 no-Red con ritmo ≥ 1,5 o desconocido → `FURY_CHIP_POSSIBLE`, sin parry; ese golpe se comporta como en 0.7.0.

## 3. CP08-C: postura (`posture_core.hpp`)

- `kParryPostureGain = 40` [BALANCE_PROVISIONAL_POST08], junto a los pesos de espada y bola.
- `preview_parry` (sin efectos) y `apply_parry(slot, generation, id, token, ledger)`:
  - validan la identidad contra el ledger;
  - rechazan muerto, congelado, latched, token 0 o duplicado;
  - suman +40 saturado a 100;
  - reinician el retardo de recuperación (`k=0`, acumulador 0), como un golpe ponderado;
  - un cruce pone el mismo latch y una línea `POST04_BREAK_READY cause=PARRY`.
- **No se fabrica ningún `HitReport`:** `consume()` queda intacto.
- **Contabilidad:**
  - `units_added` incluye las unidades de parry;
  - `e4`: `crossings ≤ weighted + parries`, `parry_crossings ≤ parries` y `crossings = latched + retirados latched + rearms`;
  - `e6` nuevo: `parry_calls = parries + rechazos`, `parry_units ≤ units_added` y `parry_units ≤ 40·parries`;
  - `ok` exige `e6`.
- Los formateadores de POST04 no cambian (la muestra versionada del CI sigue byte a byte).

## 4. CP08-D: adaptador en tiempo real (`mod.cpp`)

**`post08_judge` (PRE, solo lectura)**
- Lee del enemigo `cCcD_ObjHitInf::ChkAtHit`/`GetAtHitObj` crudos y `dCcD_GObjInf::ChkAtShieldHit` de `mSphs_at[0|1]`.
- Lee de la Link viva de esta llamada:
  - `mProcID`;
  - `mUnderFrameCtrl[0].getFrame()`;
  - `field_0x3478`/`0x347c`;
  - las direcciones de `mTgCyls`.
- Lee el evento en curso y guarda el `LiveMode` PRE.
- Comprobación de layout una vez por sesión: `&mSphs_at[0|1].GetObjAt()` = `0x1038`/`0x11f0` como en el EXE; si no coincide, parry OFF.

**`post08_step` (POST, tras POST05 y antes de POST06)**, solo con `CONFIRMED`:
1. Exige:
   - escritor abierto, sin reentrada y layout verificado;
   - identidad intacta;
   - **vida idéntica a la del PRE y mayor que 1**;
   - forma permitida: el PRE intacto (sin contacto del escudo, o POST05 ya lo deshizo) o exactamente la reacción nativa del Shield Attack (`DAMAGE 3`, previo = ATTACK).
2. `preview_parry`. Si **no cruza 100**: `post08_deflect` = `restore_reaction(PRE con mOcState = 3)`.
   - Es el estado nativo de «golpe rechazado» de `executeAttack`: sin esferas At activas, el clip termina y vuelve a FIND por la ruta nativa.
   - Sin BCK 8, sin `HeadLock`, sin BIG ni DOWN, sin tocar vida, cooldown, animación ni velocidad.
   - Se verifica con `same_live`.
3. `apply_parry`. Si **cruza 100**: no hay escritura de desvío y se entrega `parry_crossed` a POST06.
4. `commit` del episodio (falle o no, sin reintentos).
5. `POST08_EVENT`. Un `mod_update` después: `POST08_LINK_LIFE_CHECK` (diagnóstico de cualquier fuente).

**Escrituras nuevas:** **ninguna**.
- El desvío reutiliza el escritor auditado `restore_reaction`: los mismos 10 campos, ahora en un tercer sitio, `post08_deflect`.
- Link, vida, cooldown, animación, velocidad, colisiones y Expansion no se escriben.
- La auditoría de fuente lo exige (sección 6).

## 5. CP08-E: ruptura y HUD

- **Ruptura:** `break_core` añade `View::parry_crossed` y `Why::BreakByParry`.
  - En TRACKING, un cruce por parry con modo seguro escribe el **mismo aturdimiento de pie** (`post06_stun` = `DAMAGE 3`) y pasa a STAGGER_OPEN con `shield_prepared=false`.
  - Sin bonus, sin caída y sin preparar Helm.
  - Después siguen valiendo la espada decisiva ×1,50, el Escudo real → Helm, el tiempo agotado → 50 y FIX_REARM50.
  - Un latched sin ruptura escrita (escritor cerrado) se recupera a 50 en la llamada siguiente.
- **HUD:** POST07 no cambia (`hud_core.hpp` idéntico a 0.7.0). Lee la misma `Entry`, así que el +40 se ve al instante desde el centro, con destello de golpe; el cruce produce un solo pulso.

## 6. Auditorías y pruebas

- **Auditoría de fuente** (nuevas reglas):
  - las lecturas At crudas, solo en `post08_judge`;
  - `ChkAtShieldHit` una sola vez;
  - `post08_judge` sin escritores;
  - `post08_deflect` definido una vez y llamado una vez desde `post08_step`;
  - el objetivo debe ser el PRE con `kDeflectState`;
  - comprobaciones obligatorias de forma y vida;
  - `apply_parry`/`preview_parry` una vez cada uno;
  - `parry.enabled` fijado una vez;
  - `restore_reaction`: 8 llamadas en anfitriones permitidos.
- **Laboratorios:** los 10 heredados más `parry_lab`.
- **Mutaciones:** 99 (lógica de parry, postura, entrega a POST06, HUD y negativos de fuente).
- **PE:** el mismo conjunto de imports de 0.7.0 (`PE_AUDIT_PASS` con el pin sin tocar). Las escrituras y lecturas del DLL se comparan en `EVIDENCE/BINARY_AUDIT.md`.

## 7. Límites conocidos

- **Black en furia:** **no se ofrece parry**. Expansion le cobraría a Link 1 unidad de vida por el bloqueo y no se puede impedir sin tocar Expansion.
- **Visual del desvío:** con postura < 100, el clip del Bokoblin termina hacia delante sin colisión (no hay rebote al revés). El rebote nativo invierte la velocidad del clip, una escritura de animación no permitida que además chocaría con Expansion.
- **Reacción de Link:** el deslizamiento o la guardia pequeña nativos de Link al bloquear se conservan, porque son la física nativa de la defensa.
- **Shield Attack ordinario:** su aturdimiento por debajo de 100 ya estaba suprimido en 0.7.0 por POST05 GENERAL (tu decisión de 0.5.4). 0.8.0 no lo cambia y no añade otra supresión.
- **Ventana, timing real y protección de Link en el juego:** HUMAN_PENDING.
