# Light Fades Twice 0.13.5 CHILFOS FIX05: implementation

- **Base:** CHILFOS FIX04 0.13.4, source `1d443df9fbe9dd8cc2006fce3845140289d8410e` (FULL 43299000991, artifact 13981542981, `.dusk` SHA-256 `28e8097b12a79f2b291f31913b777069c359912e2cc6a36ed759acd916c66b20`, kept as rollback).
- **Evidence:** the user's `dusklight-20261112-155149.log` (0.13.4). Only the relevant lines were extracted and counted locally. The user confirmed that the C3 frame drop is gone and that contacts, sparks and the defense improved; none of that was touched.
- **Scope:**
  - Chilfos files: `kk_core.hpp`, `kk_adapter.inc`.
  - Lizalfos: `liz_adapter.inc`, for the Jump Attack defense only: 6 hunks, +19/-1 lines. `ci/kk_policy.json` holds them as an exact counted inverse patch; removing them gives the FIX05 0.12.5 file byte for byte, which `kk_audit`, `liz_audit`, `source_audit` and `test_kk_source` check.
  - `liz_core.hpp`, `mod.cpp`, `parry_fx_*`, `lnk_core.hpp`, `parry_core.hpp`, `shield_chain_core.hpp` and `link_break_core.hpp` are unchanged.
- **Hooks / imports:** no new `DEFINE_HOOK`, no new install record, no new game import. HOOK_MEM 29 / EXT 15; 102 imports with MSVC (98 with the local clang-cl preflight, the same list as 0.13.4).
- **Status:** `HUMAN_RUNTIME_PENDING`, `VISUAL_RUNTIME_PENDING`, `PERF_RUNTIME_PENDING`. Nothing here was run in Dusklight DX12.

## P0: the stagger seen twice at the end of an unfinished break

| Step | Evidence |
|---|---|
| Log | Actor 491, generation 5: `STAGGER` at tick 6679 (`STAGGER_CLIP asked_bck=9`), `RECOVERED` at 6769, the next combo at 6772. No other `setBck` of that actor in between (no `STAGGER_CLIP_KEPT`). Its real second break is at 7160. The only natural recovery of the session (`recovered=1`). |
| Native (d_a_e_kk.cpp) | `executeYoroke` mode 0 asks `setBck(9 or 0xB, attr 0)`: ONE play of DAMAGE_BOW, the bow and then the return to the stance. At `isStop` it calls `nextActionCheck`. |
| Cause (code + J3D) | 0.13.3/0.13.4 forced `attr = 2` (`EMode_LOOP`, loop frame 0) for the 90-tick window. In the 0.13.4 log the clip reads frame 40 at age 40, so it is shorter than the window. The Chilfos straightened up at the end of the clip, `J3DFrameCtrl::update` jumped back to frame 0 (`mFrame -= mEnd - mLoop`), and it bowed again before `RECOVERED` morphed it into the wait. That jump is the stagger the user saw "a second time". |
| Fix | The clip stays `EMode_LOOP`, because that mode never sets the stop state and the native Yoroke never leaves early. It is played ONCE: the first `min(10, end/3)` frames at the native rate, then stretched so its own last frame (the upright stance) is reached when the window ends. The loop frame is the last frame, so a Mortal Draw extension holds the stance instead of jumping back. A Shield Attack restart (DRAWBACK -> DAMAGE_BOW) is planned again over what is left. Writer: `kk_native_bow` (`mRate`, `mLoop`, inline fields). |
| Lab (fails on 0.13.4) | 30 natural recoveries in a row on the same actor: 0 jumps back, still staggering 10 ticks before the end, `RECOVERED` at 90 ticks at the clip's last frame, action 5 throughout, no Yoroke afterwards. 30 real new breaks: a new stagger with its own plan each time. Shield Attack restart and Mortal Draw extension: 0 jumps back. Mutants: `stagger_not_held`, `fix05_bow_not_stretched`, `fix05_bow_loop_frame_zero`, `fix05_bow_rate_native`, `fix05_bow_no_replan`, `fix05_bow_off_by_one`. |
| Unchanged | Threshold 100, window 90 ticks, HP and posture paths, both finishers, rearm, regeneration. |
| Telemetry | `CHILFOS_STAGGER event=PLAN` (clip, end, jolt, ticks left, loop frame); `CHILFOS_BREAK event=RECOVERED ... clip_frame clip_end at_end wraps bow_rate`. |

## P1: repeated Jump Attacks

| Step | Evidence |
|---|---|
| Native rebound (d_a_alink_cut.inc) | `procCutJumpInit` -> `setCutType(CUT_TYPE_JUMP)` in `PROC_CUT_JUMP`. `procCutJump` calls `changeCutReverseProc(ANM_CUT_JUMP)`; `procCutReverseInit(ANM_CUT_JUMP)` plays its sound and returns 1 **without** changing proc or clip. `procCutJump` then reverses the heading (`+0x8000`), sets `mNormalSpeed = 27` and a POWER5 shock. This is the aerial rebound: gravity, height and landing stay Link's own. `procCutJumpLandInit` calls `setCutType(CUT_TYPE_JUMP)` **again** in `PROC_CUT_JUMP_LAND`. `procCutJumpLand` calls `changeCutReverseProc(ANM_CUT_RECOIL_B)`, which is `PROC_CUT_REVERSE` with the native ground recoil clip `ANM_CUT_RECOIL_B`. No other rebound clip exists for the jump. The aerial reaction has no clip of its own. |
| Jump data | `daAlinkHIO_cutJump_c0::m` (d_a_alink_HIO_data.inc): ANM_CUT_JUMP at 1.1, aerial AT from frame 13 (`mStartAttackFrame`) until the landing; landing AT until frame 1. |
| Cause, Chilfos | `kk_link_has_rebound` accepted only `PROC_CUT_NORMAL/FINISH`: a prepared parry against a jump became an ordinary block. Every jump also gave **two** swing serials (two rolls, two verdicts, two gains). In the 0.13.4-source metrics run, 21 jumps produced 33 damage verdicts. |
| Cause, Lizalfos (measured before changing) | Prepared parry, 50 jumps meeting the shield in the air: **0 parries, 50 ordinary blocks**. `liz_link_frame` set `can_rebound=false` for `PROC_CUT_JUMP`. 50 landing contacts parried only because the landing was a NEW serial. 100 serials for 50 jumps. |
| Fix, Chilfos | Jump procs are rebound procs. The landing is the same swing: one serial, one roll, one verdict, one gain (`block_dupes`). A jump streak within 6 s raises the prepared-parry floor to 40/60/75 % and the guard floor to 60/80/90 % (2nd/3rd/4th+ jump, never 100 %). The prepared parry lasts 30 ticks for a jump (airtime). Cooldowns, flank, committed attacks and the Helm Splitter (`HEAD_JUMP`) are untouched. Jump Strike (`LARGE_JUMP`) has no rebound route and stays an ordinary guard/damage contact. |
| Fix, Lizalfos | `PROC_CUT_JUMP` keeps `can_rebound`. Its shield is presented from the jump's native AT start (frame 13, +1 tick so the 5-tick window covers the aerial contact and the landing). The landing `setCutType` is the same swing. Its rolls, posture, combos and windows are unchanged. |
| Lab | Chilfos, 100 jumps at a 4-jump streak: 76 parries (59 aerial rebounds, 17 landing `PROC_CUT_REVERSE`), 21 blocks, 3 wounds; exactly one result per jump; 0 HP through a block or parry; a counter after every parry. Behind: damage, no guard. Out of reach: nothing. During its combo: no parry. Helm Splitter: finishes. Lizalfos: 50/50 aerial parries with the aerial rebound, 50/50 landing parries with `PROC_CUT_REVERSE`, one serial per jump, 0 HP lost. |
| 60 s of jump spam (same scenario, 0.13.4 sources vs 0.13.5) | Front, 0.13.4: 21 jumps, 0 parries, 33 damage verdicts, +182 posture, 1 break. Front, 0.13.5: 27 jumps, 13 parries with rebound, 13 counters, 6 damage, +39 posture. Edge (230 u), 0.13.4: 0 parries, 34 damage, +179 posture. Edge, 0.13.5: 10 parries, 17 damage, +69 posture. |
| Telemetry | `CHILFOS_JUMP event=VERDICT` (swing, cut, link_proc, AIR/LAND, front, guard, parry, verdict, hp, posture, streak); `CHILFOS_FIX05_SUMMARY jump_*`; `LIZ_SUMMARY part=FIX05_CUTS ... jump_land_merged=`. |

## P2: both thrusts of a fast burst

| Step | Evidence |
|---|---|
| Log | Burst pairs by pattern/act. Second thrusts: **0 parries in 21 shield contacts**, all blocks. First thrusts of the same pairs: 15 parries. |
| Cause (code) | The shared D1->D2 fast shield re-arm (`liz_adapter.inc` `on_link_damage_post_liz`, the same mechanism as the Lizalfos double) restarts Link's native Shield Attack from `GUARD_SLIP` only while `double_gap_tick` is fresh. The Chilfos fed it (`kkb_burst_gap`) only on SKIPPED gap ticks. A burst whose second clip restarts in the closing Execute (gap 0) never had one, so the second press could not start a Shield Attack. It also fed the long gap before the first thrust of a pair (P3 act 3). |
| Fix | Every tick between the first thrust's close and the second thrust's open of a REAL pair (recorded < 0.40 s) feeds it, and nothing else does. It still needs a parry of the first thrust (`d1_parry_id`) and a NEW real press of R+B. x1.10 and the rhythm are unchanged. |
| Lab | All four patterns: every burst gap fed (6 pairs), 0 feeds outside, every second thrust accepts its own parry. Mutants `fix05_burst_gap_not_fed`, `fix05_burst_any_e_pair`. |

## P3: Helm Splitter too low

| Step | Evidence |
|---|---|
| Native | `procCutHeadInit`: `sp2C = enemy->getHeadLockPos() - current.pos`, height `clamp(sp2C.y, 30, mMaxHeight)`. E_KK `cc_set`: `eyePos = joint 4 - 50; setHeadLockPos(&eyePos)`. |
| Cause | The aim point follows the head, and the stagger clip bows it. The Lizalfos head stays up, so its Helm Splitter looked right. |
| Fix | While broken with the native HeadLock on (Shield Attack), the head-lock point is lifted to this actor's own upright height, sampled every Execute in its wait/walk/guard. It is never lowered. `cc_set` rewrites it every Execute: nothing to restore, nothing persists. The real position, collision, gravity and Link are untouched. Writer: `kk_native_head`. |
| Lab | Aim 55 (bowed) -> 150 (upright model): jump height 55 -> 150; never lower than a higher native point; the kill on contact intact; not broken: native. |
| Telemetry | `CHILFOS_HELM event=AIM_LIFTED native_rel lifted_rel upright_rel link_rel`; `HELM_HIT ... aim_native_rel aim_rel link_peak` (Link's real highest point over his takeoff). |

## P4: Link's torso after the Mortal Draw kill

| Step | Evidence |
|---|---|
| Native | `procCutFinish` calls `setBodyAngleXReadyAnime(1)` every frame. It aims the torso at `mTargetedActor->eyePos - 40`. During `PROC_CUT_FINISH` the target is the Mortal Draw's own (`field_0x280c`, `setAtnList`), even after it dies. The dead clip lays the head on the ground. |
| Cause | After the kill, Link's torso follows the falling eye down for the rest of the Mortal Draw, then straightens when the target is released. |
| Fix | The eye of the Chilfos the Mortal Draw killed keeps its kill height while Link is still in THAT Mortal Draw (`PROC_CUT_FINISH`, cut 0x1A/0x1F, target = this actor), at most 60 ticks. `cc_set` rewrites it every Execute. Link's clip, sound, collision, camera and other enemies are untouched. |
| Lab | Torso dip after the kill 1454 s16 units (0.13.4 model) -> 0; `POSE_HOLD_END` once; the native eye back afterwards; no hold for a Helm Splitter death. |
| Telemetry | `CHILFOS_EXEC event=POSE_HOLD_END held_ticks eye_kill_rel native_eye_drop link_body_x`. |

## Tests

- `kk_world_lab`: 26,203 checks; `liz_world_lab`: 290,546 checks; `kk_lab`, `liz_lab`, `kk_los_bench`. All pass with ASan/UBSan, 0 reports.
- Mutants: Chilfos 170 (20 FIX05), 170/170 locally. Lizalfos +5 jump mutants, 5/5 locally.
- Source rules: `test_kk_source` 36 negatives.
- Native contract: `kk_native_audit` 91 pinned lines (19 new: Yoroke, J3D loop/stop, isStop, HeadLock = eye, jump rebounds, jump AT frame 13, Helm aim, finish torso aim, MD target).

## Limitations

- The labs are a transcription plus a scripted Link, not the renderer. Whether the stretched stagger, the aerial rebound, the Helm jump and the torso look natural can only be confirmed by you in DX12.
- The real length of DAMAGE_BOW is read at runtime (`mEnd`) and logged. The lab uses 40 frames.
