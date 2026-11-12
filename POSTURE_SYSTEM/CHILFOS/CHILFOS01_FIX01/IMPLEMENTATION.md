# CHILFOS01 FIX01 0.13.1: implementation

Base: CHILFOS01 0.13.0, compiled source `1ee6660d644b8a31cc984ec8f3a7931a7c7af7d2` (FULL 43101477049, `.dusk` `84613cc9…bede`).
Shared FIX05 files (`mod.cpp`, `parry_fx_core.hpp`, `parry_fx_adapter.inc`) and every Lizalfos file are byte-identical. `ci/kk_audit.py` and the FIX05 hash pins of `tests/test_kk_source.py` prove it.
Runtime status: **HUMAN_RUNTIME_PENDING**.

## Human evidence that drove this fix

Source: the user's 0.13.0 session log `dusklight-20261111-170440` (Dusklight 2.0.3, usual mod collection). Only filtered event lines were read.

| Observation | Count |
|---|---|
| Combos selected / completed | 21 / 3 |
| `END cause=NATIVE_PRIORITY` | 17 |
| Breaks / finishers | 0 / 0 |
| Native deaths by HP | 3 |
| BCK5 trajectories | 14, 13 of them UNSURE |
| BCK6 trajectories | 27, all THRUST |

## Root causes (proven, not assumed)

1. **Link's Shield Attack staggered the Chilfos below 100 and cut its combo.** Proven: 16 of the 17 `NATIVE_PRIORITY` ends.
   - Each one is 1–3 ticks after `LNK_FIX01_SHIELD_ATTACK event=R_B_ACCEPTED` / `POST08_SHIELD_ATTACK_START`, with posture 0 and HP 340.
   - `damage_check` takes the `AT_TYPE_SHIELD_ATTACK` branch: `onHeadLockFlg(); setActionMode(5, 1)`, the native DRAWBACK stagger.
   - The 0.13.0 adapter ended the episode in that PRE, which is why the log shows `action=8`.
   - Every attempted R+B parry whose shield also touched the body knocked the Chilfos back.
2. **A non-lethal sword hit outside the melee combo kept its native reaction.** Proven: the 17th end (C3 backstep, `action=7`) and the user's report of repeated flinching.
   - The spear-less damage branch runs `setActionMode(7, 1)`, then `executeDamage`: a flinch clip, then the native BACKWALK.
   - 0.13.0 restored only "melee combo, ATTACK mode 3".
   - WAIT, WALK, GUARD, the counter, the rest wait and the whole C3 tail flinched.
   - Every later PARRY_PREPARED in the log met `action=7` (`ready=0`), so the enemy parry could never be presented (`enemy_parry=0`).
3. **The D/E classifier rejected a real sweep.** Proven by the engine's own spear-tip trajectories in the same log:
   - BCK5 tip: 320..357 units sideways for 325..441 forward.
   - BCK6 tip: 0..23 sideways for 60..169 forward.
   - The 0.13.0 diagonal rule demanded sideways > 1.2 × forward, so BCK5 stayed UNSURE and the identity never settled.

## Corrections (production: `src/kk_core.hpp`, `src/kk_adapter.inc` only)

### Anti-stagger below posture 100 (the FIX05 contract, re-derived for E_KK)
- **Sword hits:** a non-lethal contact keeps the Chilfos in what it was doing.
  - In the damage_check POST, its action, mode and heading are put back with `kk_native_resume`, only when the native picked the damage reaction 7 for that contact.
  - `damage_check` is the first call of `action()`, so `executeDamage` (the flinch clip, then the native BACKWALK) never starts.
  - HP loss, hit mark, damage SE, the native 8-tick `mDamageTimer` and the posture credit stay as they were.
  - This covers WAIT, WALK, GUARD, ATTACK (window open or closed), the counter, the rest wait and the C3 BACKSTEP / THROW / RESTORE.
- **Link's Shield Attack:** below the stagger, its Tg mark is cleared before the native reads it (`kk_native_tg_clear`).
  - No native DRAWBACK and no HeadLock. No HP and no posture are gained (FIX05 rule).
  - The combo goes on.
  - The native contact SE (`startCollisionSE(Z2SE_HIT_SWORD, 0x28)`, the same call the native branch makes) plays once per press. It is a virtual call: no new import.
  - During the stagger the native branch runs untouched (HeadLock, then Helm Splitter).
- **Posture 100 breaks immediately:** in the same damage_check POST (`kk_try_break`, `origin=DAMAGE_POST`). There is never one tick of another native reaction first.
- **One posture credit per swing:** the same swing contacting again after the native timer keeps its native HP loss, with no second +5 and no second wound (`sword_dupes`).
- **Receipt of the Chilfos' own impact on Link** (Link parry +13, block +20, direct offer): resolved before the Chilfos' damage-timer gate, still once per AT window. A hit Link landed a few ticks earlier can no longer swallow the receipt of the next thrust.
- **Native exceptions kept (FIX05 rule for non-sword weapons; agreed balance):**
  - arrows, boomerang, hookshot and bombs keep their native reaction;
  - the Iron Ball keeps its native branch (+30 when non-lethal);
  - a strong hit that natively breaks a held spear (CLASH, +5 once) keeps its native reaction.
  - Each such end is logged with its origin.

### Combos
- **0.13.0 cause of the premature ends:** causes 1 and 2 above. The policy, rhythm and window code were correct.
- **Disambiguated ends:** every `CHILFOS_COMBO event=END` now carries:
  - `origin=` (the hook and branch that ended it);
  - `phase=`, `mode=`, `bck=`, `frame=`;
  - `last_link=` (`SWORD`, `SHIELD_ATTACK`, `IRON_BALL`, `OTHER_WEAPON`) with its tick.
  - Unexpected causes are WARN lines.
- **The C3 tail is committed:** no guard and no prepared parry during BACKSTEP, THROW and RESTORE. A hit lands, and with the anti-stagger the tail goes on.

### C3 tail
- **Backstep speed:** BCK7 plays at ×1.25, and the native 15 that `executeBackWalk` writes is now scaled by the same factor (18.75). Otherwise the legs would stride 25% faster than the body moves.
- **Eye-height sentinel (unchanged, residual risk re-measured):**
  - Native `cc_set()` recomputes `eyePos` every Execute, after `action()`.
  - Creature sounds are positioned on `current.pos` (`mSoundObjAnime`), not on `eyePos`.
  - The POST now restores the sentinel even if the episode ended inside the native call.
- **New telemetry:** `CHILFOS_SPEAR event=THROW_START` and `event=REARMED`.
- **Visual coherence of throw → restore:** not observable offline. **HUMAN_RUNTIME_PENDING.**

### D/E identity
- `classify_tip`: a sweep is a sideways/vertical motion of at least 100 units and at least 0.6 × the forward one. The thrust rule is unchanged.
- With the user's real vectors the identity settles as `MEASURED_DEFAULT` (D = BCK5, E = BCK6). No constant was flipped.
- Visual confirmation is still required.

### New native writers (E_KK, this actor only)
| Writer | Writes |
|---|---|
| `kk_native_resume` | action, mode and heading of before one damage_check call |
| `kk_native_tg_clear` | mCyl Tg-hit clear (Shield Attack below the stagger, crossing-swing re-contact) |
| `kk_native_bash_se` | the native contact SE of that Shield Attack |
| `kk_native_speed` | speedF of the C3 backstep |

No new hook target and no new game import: 28 HOOK_MEM / 99 imports, as in 0.13.0. A local clang-cl preflight showed no new import; the MSVC gate audits it again.

## Requirement matrix (sections 3–7 of the FIX01 request)

| Requirement | Implementation | Automated proof | Human |
|---|---|---|---|
| Below 100, no flinch, backwalk or stagger from a non-lethal sword hit, in every phase | `kk_resume` | `lab_poise` (2): WAIT, back hit, posture 0/50, heading kept, no backward travel. (4): every combo, a hit in every open window. (5): C3 BACKSTEP / THROW / RESTORE. Mutants `resume_lost`, `resume_heading_lost`, `resume_melee_only_0_13_0` | PENDING |
| HP lost, +5 once per swing, hit mark/SE native | unchanged native path + `sword_credit_serial` | `lab_poise` (2), (9); mutant `sword_credit_every_contact` | PENDING |
| Shield Attack below 100: no stagger, no HeadLock, no combo cut | `kk_native_tg_clear` | `lab_poise` (7) every pattern, (8) the user's session shape (3000 ticks of R+B presses: 0 `NATIVE_PRIORITY`); `lab_break` FIX01 case. Mutants `shield_attack_staggers`, `bash_se_every_contact` | PENDING |
| At 100, immediate native stagger; the crossing swing never kills | `kk_try_break` in POST; 0.13.0 fix of the cached verdict | `lab_poise` (3); `lab_break`. Mutants `break_deferred_one_tick`, `stagger_reuses_crossing_verdict`, `same_swing_kills` | PENDING |
| Finishers (new sword swing / Shield Attack + Helm), 90-tick timeout | unchanged | `lab_break` | PENDING (0 breaks in the 0.13.0 log) |
| Four combos complete, no unexplained `NATIVE_PRIORITY` | causes removed; `origin=` on every end | `lab_patterns_and_rhythm`, `lab_poise` (4), (7), (8) | PENDING |
| One AT, one SE, independent block/parry per hit; bursts | unchanged | `lab_crossing`, `lab_link_side`, rhythm table | PENDING |
| C3 tail: one spear, x1.60 restore, rearm, no spear after a cancel | committed tail, speed fix, logs | `lab_c3_tail`; `lab_poise` (5), (6). Mutants `tail_guard_allowed`, `back_speed_native`, `rearm_not_logged` | PENDING (visual) |
| Link block/parry receipts in fast pairs | contact before the timer gate | `lab_poise` (10); mutant `link_contact_gated_by_timer` | PENDING |
| Enemy parry: real rebound, +25 Link, counter | unchanged; now reachable (no flinch state) | `lab_defense` | PENDING (0 in the 0.13.0 log) |
| Balance 340 / gains / regen / break 90 | unchanged | `kk_lab`, `test_kk_source` | PENDING |
| D/E identity | classifier from real data | `lab_poise` (1) with the user's vectors; mutant `tip_sweep_strict_0_13_0` | PENDING (visual) |
| Lizalfos FIX05 and shared files unchanged | — | `kk_audit`, FIX05 hash pins, every inherited suite in FULL | PENDING |
| Non-sword weapons: native reaction kept, end logged | unchanged + `origin=` | `lab_poise` (11) | PENDING |

Rhythm: unchanged from 0.13.0 (`../CHILFOS01/RHYTHM_TABLE.txt`). The four burst intervals stay at the physical floor of separate native AT windows: C1 4→5, C3 1→2, C3 3→4 and C4 5→6 at 0.333 s.
