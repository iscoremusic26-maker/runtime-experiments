# CHILFOS FIX03 0.13.3: implementation

Base: CHILFOS FIX02 0.13.2, compiled source `2bea57ac9f5baffda38e01d61c33e95c806591c6` (FULL 43243150649, `.dusk` `0cd15dc3…c767`).
- **Production changes:** `src/kk_core.hpp`, `src/kk_adapter.inc`, `src/kk_bridge.inc` (clock), and two `DEFINE_HOOK` lines inside the CHILFOS hunk of `src/mod.cpp`. That hunk is the exact inverse patch of `ci/kk_policy.json`, and FIX05 still reconstructs byte for byte (`ci/kk_audit.py`).
- **Lizalfos and other shared files:** unchanged (FIX05 hash pins in `tests/test_kk_source.py`).
- **Status:** **HUMAN_RUNTIME_PENDING**, **VISUAL_RUNTIME_PENDING**, **PERF_RUNTIME_PENDING**.

## Design rule (user, FIX03)
HP and posture are two independent ways to defeat the Chilfos:
- **HP 0:** a legitimate hit that takes the last HP kills it natively at any posture.
- **Posture 100:** an immediate native stagger. The crossing contact never kills by itself; a later contact can.
- **Hidden skills:** they never instant-kill a living, unbroken Chilfos. They deal their ordinary damage, and kill only if that damage reaches HP 0.

## Evidence: user log `dusklight-20261112-103231` (0.13.2, 10 mods; filtered `CHILFOS*` lines only)
| Item | Value |
|---|---|
| Combos completed | 33 |
| `NATIVE_PRIORITY` | 0 |
| Enemy parries / counters started / counters expired | 21 / 21 / 0 |
| Throws / child duplicates | 13 / 0 |
| `blocked_spear_break` | 0 |
| Breaks: Mortal Draw-free kills | 5: 3 by `SWORD_DECISIVE`, 2 by Helm Splitter |
| Native deaths | 9 |

## Cause matrix
| Symptom | 0.13.2 log | Code origin | Fix | Test that fails without it | Result |
|---|---|---|---|---|---|
| Hits through a raised guard | `VERDICT verdict=DAMAGE ... ready=1 action=6 frontal=1` at ticks 8184 (HP 60→20), 13282 (260→200), 14331 (160→120) | `kk_decide`: even with the native GUARD action up, a frontal swing rolled `block_pct` and could fail | A GUARD action that is up, with the spear in hand and a frontal swing, is a **block, no roll** (`guard_state=ACTIVE`). The roll only decides whether a ready Chilfos guards. Back and flank stay open. | `lab_fix03` B1 (the three log cases exactly), B2 (300 normal/strong swings into a raised guard: 0 HP; one from the back: damage). Mutants `guard_active_roll_restored`, `guard_active_from_back` | 0 leaks in the lab |
| Back Slice kills at full HP | `NATIVE_DEATH route=NATIVE hp_before=340 broken=0` at 10915 and 11242, `cut=30` (0x1E TWIRL) | Native `damage_check`: `(IRON_BALL && !0x400) \|\| mCutTypeCheck(2)` → `health = 0; setActionMode(10, 0)` before any damage. `mCutTypeCheck(2)` is true for LARGE_JUMP(+FINISH), LARGE_TURN_L/R, MORTAL_DRAW_A/B, HEAD_JUMP, TWIRL. | A PRE hook on the exported `daE_KK_c::mCutTypeCheck` answers **false for param 2** inside an admitted, unbroken Chilfos' own `damage_check` (`in_dc`). The EXE calls it for real three times from `damage_check` (`0x140dc789f/7a38/7b9b`). The hit then takes the ordinary branch (hit mark, cc_at_check, our verdict). Before the instant-kill branch nothing has been emitted (no pause timer, hammer SE or death). The Iron Ball's own lethal operand is untouched. | `lab_fix03` A1 (each of the 8 skills at HP 340: HP 338, no death). Mutant `skill_instant_kill_restored` | `CHILFOS_HP event=SKILL_INSTANT_SUPPRESSED` |
| (kept) HP 0 at posture 98/99 | `hp_before=20` at 8236 and 12860, normal cut: legitimate deaths | — | Kept native. Classified `cause=HP_ZERO`. | A2 (each skill takes the last HP → dies, HP_ZERO), A3 (HP 20, posture 99/98, a cut of 20: dies, no break). Mutant `hp_zero_death_blocked` | deaths keep working |
| Guard-like clip during the stagger (Shield Attack → Helm Splitter) | `SHIELD_PREP` → `HELM_HIT` at 6931 / 14439; no clip data in 0.13.2 | The native Shield Attack branch puts Yoroke mode 1 = `setBck(KK_DRAWBACK 0xF)`, a raised-spear recoil the 0.13.2 setBck PRE only looped. Also, `mCutTypeCheck(0)` (auto-deflect) is true for HEAD_JUMP/MORTAL_DRAW, so the native raised `TgShield` inside `damage_check`; it was closed in our POST. | While broken, the setBck PRE turns DRAWBACK and the guard clips into the stagger clip (with or without spear). HeadLock stays native. `mCutTypeCheck(0)` answers false while broken, so `TgShield` is never raised. A guard action would be undone. `CHILFOS_BREAK event=TRACE` records bck/asked/action/mode/frame/TgShield/HeadLock. | C (DRAWBACK replaced, TgShield never raised and never asked, Helm kills, no GUARD action). Mutants `stagger_drawback_shown`, `stagger_shield_reopened` | VISUAL_RUNTIME_PENDING |
| B finisher should be Mortal Draw | design | Native: `checkCutAction` → `procCutFinishInit(CUT_FINISH_PARAM_MORTAL_DRAW_A/B)` only from the sheathed quick draw (`checkCutFastReady`: sword sheathed, skill learnt, lock-on within 400) | A POST hook on Link's `checkCutAction` runs only when the native just chose an ordinary cut (PROC_CUT_NORMAL/FINISH, not a hidden skill). If a broken, admitted Chilfos without a prepared Helm Splitter stands in front of Link (±60°) within 350, it calls Link's own `procCutFinishInit(CUT_FINISH_PARAM_MORTAL_DRAW_B)`, the native choice when R is not held. That gives `PROC_CUT_FINISH`, `ANM_CUT_MORTAL_DRAW_B`, cut type 0x1F, its AT and sound, in the same call. **The kill is the native `mCutTypeCheck(2)` branch on contact**, allowed only while broken. B without contact does not kill; B while not broken is untouched; R+B stays a Shield Attack. The 90-tick window may extend at most 30 ticks while a started Mortal Draw really runs. | D1–D7 (press ≠ kill, contact kills, B again = no second request, not broken = ordinary cut, out of reach = cancelled, then recovery, Helm prepared = no takeover, facing away = none, two broken = nearest only, extension bounded). Mutants `md_not_started`, `md_index_swapped`, `md_steals_helm`, `md_any_actor`, `md_double_request`, `md_kill_on_press`, `md_from_behind`, `md_no_extension`, `md_never_cancelled` | `CHILFOS_EXEC event=B_REQUEST/START_NATIVE/KILL/CANCELLED/WINDOW_EXTENDED` |
| FPS drop at the C3 throw | user report (60→45); not measurable from the 0.13.2 log | Not proven. Mod-owned work at the release: each spear child took a slot, ran the admission path and logged an `EXCLUDED` line (synchronous log I/O in the release frame). | Spear children take no slot: a `field_0x679 == 1` fast path, unique-counted, one log line per session. A **`CHILFOS_PERF event=THROW_WINDOW`** line per release measures presented frames (POST record on the existing `dMeter2_c::_draw` target, one QPC read per frame): 90 frames before and after, avg/p50/p95/p99/max ms, frames over 1.5 × the pre-release median, and the module's own hook time in the window. QPC is calibrated against the file-time clock (no new import). `gpu=GPU_NOT_MEASURED`. Throw rate 1.45, spawn frame 23, one child, rearm: unchanged. | E (13 releases with real child actors: 13 children, 0 slots, ≤ 1 log line, 13 windows, an injected 10 ms spike measured exactly). Mutants `spear_child_takes_slot`, `spear_child_logged_each`, `perf_window_never_opens`, `perf_slow_frames_wrong` | **PERF_RUNTIME_PENDING**: no FPS gain is claimed |

## Death causes (`CHILFOS_BREAK event=NATIVE_DEATH ... cause=`)
`HP_ZERO`, `SWORD_DECISIVE`, `HELM_SPLITTER`, `MORTAL_DRAW`, `POSTURE_FINISHER_SKILL`, `IRON_BALL`, `NATIVE_SKILL_INSTANT` (must stay 0), `OTHER`. The summary counts them in `deaths=…`.

## Hooks and imports (deltas over FIX02; confirmed by the gate's PE audit)
| Item | Change |
|---|---|
| `HOOK_MEM` | +1, `daE_KK_c::mCutTypeCheck` |
| `HOOK_MEM_EXT` | +1, `daAlink_c::checkCutAction` |
| Game imports | +3: those two and `daAlink_c::procCutFinishInit` |
| New writer | `kk_native_mortal_draw` |
| Extra hook records on existing targets | 1, the `dMeter2_c::_draw` POST |

Prologues are checked by `ci/hook_prologue_audit.py`. Locally, neither prologue has a rel8 branch in its first 5 bytes.

## Kept from FIX01/FIX02
- **Combat:** anti-stagger, absorbed Shield Attack, immediate break, the spear never breaks on a block or parry, pressure guard and cooldowns, committed episodes, counters, no recoil slide or lunge shove, ×1.10 bursts.
- **Combos and identity:** four combos, C3 throw/rearm, D = BCK5 / E = BCK6.
- **Balance:** unchanged.
