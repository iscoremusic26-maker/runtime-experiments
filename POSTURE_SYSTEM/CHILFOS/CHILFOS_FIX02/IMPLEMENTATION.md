# CHILFOS FIX02 0.13.2: implementation

Base: CHILFOS01 FIX01 0.13.1, compiled source `0a9415f4a45278fe8d584a9cd563553f13f4ec45` (FULL 43128870810, `.dusk` `c8020984…3316`).
Production changes: only `src/kk_core.hpp` and `src/kk_adapter.inc`. Shared FIX05 files and every Lizalfos file are byte-identical (`ci/kk_audit.py`, FIX05 hash pins).
No new hook target, game import or writer function.
Runtime status: **HUMAN_RUNTIME_PENDING**.

## Human evidence (user, 0.13.1, `dusklight-20261112-090632`; filtered `CHILFOS*` lines only)
| Item | Value |
|---|---|
| Summary | 38 combos completed, 0 `NATIVE_PRIORITY` (FIX01 kept) |
| Verdicts | 14 ENEMY_PARRY / 37 BLOCK / 49 DAMAGE |
| No-parry reasons | COOLDOWN 38, RNG 15, NO_SPEAR 18 |
| Spear breaks | 7 |
| Counters | 2 started, 9 expired |
| Identity | `MEASURED_DEFAULT` |

Reported by the user: repeated B wins; the spear seems to break under many hits; Link and the Chilfos slide apart in exchanges; the fast double thrusts are too fast.

## Cause matrix
| Symptom | 0.13.1 log | Code origin | Fix | Test that fails without it | Result |
|---|---|---|---|---|---|
| Spear lost on a block | 7 × `VERDICT ... verdict=BLOCK ... action=6` then `source=SPEAR_BREAK`, then `reason=NO_SPEAR`. Real cut types 0x15 FINISH_RIGHT, 0x20 FINISH_STAB, 0x21 COMBO_STAB, 0x06/0x07 FINISH_*: chain finishers | Native `damage_check`, spear in hand: `at_power_check` → `mHitStatus != 0` (or status 0x400, Midna lock) → `setActionMode(7, 0)`. `executeDamage` mode 0 = CLASH, `field_0x67d = 1`, speedF -80, then BACKWALK to regrow. 0.13.1 only credited +5. | In the damage_check POST, a contact judged BLOCK or ENEMY_PARRY with the spear in hand whose native reaction is (7,0) becomes the native guard reaction (6,0) before `executeDamage` runs. The +5 SPEAR_BREAK credit is removed (a normal block, +3). The native contact SE of that call is kept. | `lab_fix02` A1 (guarding, strong cut, BLOCK and PARRY), A2 (100/300/1000 swings of nine cut kinds, strong and normal: `field_0x67d` checked every tick). Mutants `spear_break_branch_restored`, `spear_intact_block_only` | 0 spear losses |
| Spear lost after an enemy parry (not logged in 0.13.1) | `ENEMY_PARRY` (actors 255, 311, 316) followed by `spear=0` with no SPEAR_BREAK line | Same native branch: the parry case had no check at all | Same fix; plus a runtime invariant `CHILFOS_SPEAR event=LOST after_block_or_parry=…` and the summary counters `blocked_spear_break` (must stay 0) and `other_spear_loss` | A1 (PARRY), A3 (the monitor itself). Mutant `spear_monitor_blind` | reported, never silent |
| Repeated B wins | `reason=COOLDOWN` 38 times; `block_pct` back to 30 after every block (`wounds=0`) | Cooldowns 120/90/60. `on_block` reset the wound streak, so the guard oscillated 45 → 30 → 45. | **Pressure guard:** 30/50/70/85 % by aimed swings in 150 ticks, not reset by a block.<br>**Guarantee:** after 2 ready frontal swings in a row that still wounded, the next ready frontal swing is blocked (never within the 6-tick ready delay, forgotten after 90).<br>**Cooldowns:** 45/35/25 ticks. Back and flank stay open. | `kk_lab` (pressure, guarantee, exact cooldowns); `lab_fix02` B (120 frontal swings: ≤ 1 in 5 ready wounds, ≤ 2 in a row, ≥ 10 parries; 60 back swings: no block, no parry), B2 (the guarantee through the adapter). Mutants `pressure_ignored_0_13_1`, `guarantee_ignored`, `uncovered_not_counted`, `cooldown_old_120_90_60` | lab: 120 frontal swings → 24 parries, 22 blocks, 2 ready wounds |
| Counter lost | 11 `ENEMY_PARRY`: `COUNTER` 2 times, `counter_expired` 9; the 2 started ended `cause=ADAPTIVE_DEFENSE ... counter=1` | The counter waited for the native guard clip (re-started by every block of repeated B) and the native AI to choose an attack, within a 60-tick lifetime. A block of Link's next swing ended the counter wind-up. | **Dispatch:** through the native attack entry (8,0), 6 ticks after the confirmed parry (`COUNTER_DISPATCH`). The native `executeAttack` picks the clip; the setBck PRE makes it the counter's D/E.<br>**Every opportunity ends logged:** `COUNTER` (started) or `COUNTER_CANCELLED reason=NO_SPEAR/BROKEN/DEAD/EVENT/LINK_FAR/ACTION`.<br>**Committed:** the counter never guards. | `lab_fix02` C (each confirmed parry starts a counter whose AT opens, 0 silent expiries; Link far → `reason=LINK_FAR`), C2 (a hit into the wind-up does not end it). Mutants `counter_never_dispatched`, `counter_cancel_silent`, `counter_never`, `episode_guard_allowed` | 0 silent expiries |
| A blocked swing ends a committed combo | `END cause=ADAPTIVE_DEFENSE_AT_SAFE_BOUNDARY` (4 in 0.13.1, many more with a stronger guard) | `kk_guard_ready` allowed a guard between two hits of a combo | Every offensive episode (combo, C3 tail, counter) is committed: no guard, no parry inside. Link's hits land with the FIX01 anti-stagger (HP, +5, combo goes on). The defense against repeated B is the one between episodes. | `lab_fix02` F (3000 ticks of R+B and alternating sword swings while it fights: combos complete, 0 `NATIVE_PRIORITY`, 0 spear loss). Mutant `episode_guard_allowed` | committed combos |
| Slide in exchanges (Chilfos side) | user report; no positions in the 0.13.1 log | Native `damage_check`: its spear on Link's shield → `speedF = -70`, decaying 10/frame (~280 units back).<br>Native `executeAttack` frame 24 → `speedF = 80` (~284 units forward), which against a Link already in reach only shoves him through body collision. | **The -70 shield recoil** of that call is cancelled (stops at the shield).<br>**The frame-24 lunge** is capped (`lunge_for`, the exact native decay) so the Chilfos stops 150 units from a Link in reach. The spear tip is 230 units ahead, so it still reaches; farther away the lunge is native.<br>**Not changed:** Link's own guard slip and animations, which are native Link code, unproven as a cause. | `lab_fix02` D1 (C2 against a guarding Link: no negative speed, one block receipt per impact), D2 (lunge capped at 180/300 units, native at 700; body never inside 150). Mutants `recoil_not_fixed`, `lunge_uncapped` | lab only; `CHILFOS_MOTION event=CONTACT/SETTLE` log both actors' travel over 8 ticks for the human test |
| Double thrusts too fast | user report | `kRateEBurst = 1.50` | ×1.10 (the Lizalfos FIX05 double, used as a number only; no Lizalfos code touched). The planner recomputes start frames, gaps and windows. The physical floor of two distinct whole native windows at ×1.10 is 14 ticks (0.467 s). | `lab_fix02` E (each burst opens its own native window at 1.10, ≥ 14 ticks apart); `kk_lab` rhythm (exact realizable minimum). Mutant `burst_rate_150` | see `RHYTHM_TABLE.txt` |

## Rhythm at ×1.10 (`RHYTHM_TABLE.txt`)
Each burst pair is now 0.467 s apart (a whole 8-tick window plus the 6-frame wind-up kept). The difference from the recordings is shown, not hidden:

| Pair | Recorded | Now |
|---|---|---|
| C1 4→5 | 0.260 s | 0.467 s |
| C2 2→3 | 0.371 s | 0.467 s |
| C2 4→5 | 0.389 s | 0.467 s |
| C3 1→2 | 0.213 s | 0.467 s |
| C3 3→4 | 0.233 s | 0.467 s |
| C4 5→6 | 0.137 s | 0.467 s |

Every other interval stays within one tick. The C3 backstep, throw and restore are unchanged.

## Kept
- **FIX01:** anti-stagger, absorbed Shield Attack, immediate break, one +5 per swing.
- **Combos and identity:** four combos, 25 % each; C3 one throw and rearm; D = BCK5 / E = BCK6.
- **Balance:** 340 HP, posture gains 13/5/3/30, Link 20/30/25, regeneration 12/8/5/2/1, break 90 ticks, both finishers.
- **Native exceptions:** arrows, boomerang, hookshot, bombs and the Iron Ball (including its native spear break under status 0x400) are unchanged. They are not sword blocks.

## Limits
- **Link's slide:** whether Link's own slide disappears in the real game is not proven offline. Only the Chilfos-side causes were changed; `CHILFOS_MOTION` lines record both actors.
- **Lab Link:** the lab's scripted Link keeps swinging during his native parry recoil, so the lab's frontal-damage total includes trades with counters that the real recoil may prevent.
- **Not observable offline:** visual coherence, audio and FX.
