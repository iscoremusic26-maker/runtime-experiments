# Light Fades Twice 0.13.4 CHILFOS FIX04: implementation

- **Base:** CHILFOS FIX03 0.13.3, source `f77969e0286ba9777f2b8a6a32d16554abf17393` (FULL 43260499707, artifact 13964029612, `.dusk` SHA-256 `7348ce11d0256f58e1ebd3fff3c559d1ce4417b0c915b5794828ed96a47b9006`, kept as rollback).
- **Evidence:** the user's `dusklight-20261112-115957.log` (0.13.3, Dusklight 2.0.3 rev 40457c6, D3D12, Intel UHD, 1920x1080 at 1.25, 10 mods). Only the relevant lines were extracted and counted locally.
- **Scope:** Chilfos files only (`kk_core.hpp`, `kk_adapter.inc`, `kk_bridge.inc`). `mod.cpp`, `parry_fx_adapter.inc`, `parry_fx_core.hpp` and every Lizalfos file are byte-identical to 0.13.3 (`ci/kk_audit.py` and the FIX05 pins still pass).
- **Status:** `HUMAN_RUNTIME_PENDING`, `PERF_RUNTIME_PENDING`, `VISUAL_RUNTIME_PENDING`. Nothing here was run in Dusklight DX12.

## P0: the C3 throw frame drop

| Step | Evidence |
|---|---|
| Human symptom | 60 -> ~45 FPS during the C3 throw, unchanged from 0.13.2. |
| Log | Bokoblin Expansion's `DEVF_CP12 PERF_WINDOW` (wall clock between 30 Hz sim ticks) shows **exactly 15 ticks over 40 ms (p99 44-45 ms)** in the 7 windows that contain the 7 `THROW_SPAWN` ticks (3255, 4547, 5730, 17705, 18654, 19967, 26286), and in no other window with that signature. 15 ticks = `THROW_START` (frame 2.5) to the spawn (frame 23) at rate 1.45. ~44 ms per tick = ~11 ms extra CPU per tick = ~45 FPS. |
| Why 0.13.3's telemetry misled | `CHILFOS_PERF THROW_WINDOW` opened at the **release**; the wind-up was in its `pre` ring (pre p95 43-46 ms, which is the drop) while the report read `post` (~19 ms). `mod_hooks_ms` only ran after the release. `dMeter2_c::_draw` is a HUD draw, not a Present. |
| Root cause (code + EXE) | To stop the native melee cancel (`eyePos.y + 50 > Link.y`, frame < 23) the adapter parked `eyePos.y` at **-1e9** for each wind-up `executeSpearThrow`. The same native call first runs `fopAcM_otherBgCheck` (EXE `0x14076a110`), whose `dBgS_LinChk` starts at `(pos.x, [actor+0x630] = eyePos.y, pos.z)`. `cBgS::LineCross` calls `dBgWKCol::LineCheck` (EXE `0x14080b150`) on every BG element, and LineCheck walks the segment in **500-unit strides** (`500.0f` at `0x141e4e718`) with out-of-line `C_VECSubtract/C_VECScale/C_VECAdd` per stride. A 1e9-unit segment = **~2 000 000 strides per KCL per wind-up Execute**. |
| Fix | `kk::throw_eye`: the eye is lowered only to `Link.y - 60` (never raised). `eyePos.y + 50 <= Link.y`, so the cancel still never fires, and the native segment is as short as vanilla. Restored in the POST as before. |
| Lab (fails on 0.13.3) | `kk_world_lab` transcribes the native cancel with its two BG lines: Link close / far edge / on a step / below / 8 KCL / out of range: the spear always flies, at most 3 strides per KCL per call. Mutants `fix04_eye_at_minus_1e9`, `fix04_throw_eye_core_1e9`, `fix04_eye_raised_not_lowered` are killed. |
| CPU benchmark | `tests/kk_los_bench.cpp` (transcribed stride loop, SYNTHETIC KCL, run by CI on MSVC): eye -1e9 = **1 968 956 strides, ~10.5 ms per call per KCL (~157 ms per wind-up)**; eye Link-60 = 1 stride, ~0.06 us; vanilla eye = 1 stride. The ~10.5 ms matches the ~11 ms the log shows per tick. |
| Throw unchanged | BCK 0x18, `kRateThrow` 1.45, spawn frame 23, one native child, restore 1.60. |
| Runtime telemetry | `CHILFOS_PERF event=THROW_WINDUP calls native_ms_max native_ms_avg los_len_max los_strides_per_kcl`: QPC around each native wind-up call in your game (expected well under 1 ms). `THROW_WINDOW` now opens at `THROW_START` (`anchor=THROW_START sampler=METER_DRAW_NOT_PRESENT gpu=GPU_NOT_MEASURED`). |
| Still pending | DX12 frame pacing and GPU time cannot be measured here: **PERF_RUNTIME_PENDING** until your FPS-counter video. |

## P1: one contact per spear attack

| Step | Evidence |
|---|---|
| Human symptom | A single spear attack sometimes gives two clashes / two sparks on the shield. |
| Log | 10 impacts with a second native shield round **exactly 8 ticks** after the first (489/497, 560/568, 734/742, ...); 11 rounds outside any impact window (`action=8 mode=3`); `motion_recoil_fixed=430` native rounds for ~330 real receipts (197 parries + 133 blocks). |
| Root cause (code) | `cc_set` registers `mSph` and arms the six shaft spheres' AT only while `field_0x67d == 0 && field_0x67e == 0` (frames 24-33). `cCcS::ClrAtHitInf` clears only **registered** AT objects, so a contact still held when the window closes leaves stale AT-hit flags; `damage_check` replays them when its 8-tick `mDamageTimer` expires. FIX02 cancels the -70 recoil, so the spear stays on the shield and the stale case became common. `damage_check` also plays one `Z2SE_HIT_SWORD` per sphere of the same pass, and `dCcS` emits one hit mark per sphere (each sphere has its own effect counter). |
| Fix | One token per native AT window (`field_0x67e` 1 -> 0 seen after `cc_set`). In this Chilfos' `damage_check` PRE (`kk::spear_round`): stale flags cleared (no clash, no recoil, no receipt); the echo of an attack that already had its round cleared; a new contact keeps **one** sphere (the tip first) for the native round; a new attack muted by an older timer plays its one clash at once. Clears use the native virtual `dCcD_GObjInf::ClrAtHit` (no import). A PRE on the existing `dCcS::ProcAtTgHitmark` hook (after the parry FX PRE) lets only the first hit mark of this spear on Link per attack through. Geometry, radii and windows are native. |
| Lab | 7 spheres modelled (tip + 0/2/6 shaft spheres), stale flags as `cCcS` leaves them, native effect counters: **exactly one clash, one spark and one receipt per attack** over 8-13 attacks (bursts included), body hits too, two Chilfos on one Link, out of reach = nothing (no false positive), in reach = every attack counted (no false negative). |
| Telemetry | `CHILFOS_CONTACT event=ATTACK` (one line per attack that touched Link: spheres, native rounds, echoes, stale, marks) and `CHILFOS_CONTACT_SUMMARY`. |

## P2: missing orange / blue sparks

| Step | Evidence |
|---|---|
| Log | 39 `FX_PAIR kind=CHILFOS_PARRY_LINK emitters=0`. In 35 the native spark was created and captured right after (`EMITTER_CAPTURED` res 0x0117/0x0118, same pass tick). The other 4 (ticks 3996, 16198, 16920, 19046) are all next to a `BLOCK_INTACT` line. There are 16 `BLOCK_INTACT` in the log: 8 blocks and 8 parries. |
| Root cause (code) | `damage_check` plays the guard spark `setHitMark(2, this, ...)` only in its **weak** branch. A strong sword hit (`at_power_check` AtSpl 1, Link status 0x400, Midna lock) takes the clash branch `def_se_set(.., 0x1F)` + `(7,0)`, with **no spark**. FIX02 turns that into the guard (6,0) to keep the spear, so the block or parry kept no spark at all. The 35 others were only a premature log: the settle ran in the PRE, before the native spark existed. |
| Fix | `kkb_guard_mark`: the native weak-branch call for exactly that converted contact (blue for a block; the parry FX book claims it and makes it orange for a parry). The parry record is settled in the damage_check POST, after its spark exists. For that call only, the parry pitch accepts the strong branch's map 0x1F. No shared file changed. |
| Lab | Strong and weak x block / parry / damage: exactly one spark per block or parry, none on damage, never two. Order `MOD_MARK`/`NATIVE_MARK` before `SETTLE_ENEMY_PARRY`. 200 alternating contacts: 200 sparks. |

## P3: defense, lateral steps, repeated B

| Step | Evidence |
|---|---|
| Log | Damage verdicts: 17 frontal + ready in WAIT (roll failed), 4 flank in WAIT, 1 flank in GUARD (tick 17987, `frontal=0`: an authentic flank, kept), 20 inside its own attacks (trades). |
| Root cause (code) | The native WAIT never turns (only the native guard does: `cLib_addCalcAngleS2(.., 8, 0x500)`), so a short side-step reached the 67.5 degree flank. The block was rolled at contact, so its "alert" stance looked like a guard that sometimes failed. |
| Fix | A ready Chilfos in its native wait turns toward Link with the native guard's own rule. The pressure/wound roll of a swing is taken when Link starts it (`setCutType`) and, if it covers, raises the native guard (6,0) before the blade. There is one roll per swing (a failed raise is a hit). A wound outside its own attacks raises the native guard. It never guards inside its committed attacks. A raised guard still covers only its front. Percentages, HP 340, posture 100 and gains are unchanged. |
| Lab, 60 s of repeated B (Link interrupted by spear hits) | **Slow lateral circle:** 0.13.3 defense = 27 hits by flank/opening, 0 blocks; 0.13.4 = 0 by flank, 22 blocks, 19 parries, 19 counters. **Frontal:** 0.13.4 = 2 wounds in 40 contacts on its covered front, 19 blocks, 19 parries, 19 counters (0.13.3: 2 in 48). **Fast flank** (0x1200 per tick): still lands (37 by flank/opening). |

## Unchanged (regression labs)

FIX01/FIX02/FIX03 labs are green: combos and rhythm, C3 and rearm, anti-stagger, the spear never breaking on a block, counters, x1.10 bursts, a raised guard blocking 100 %, hidden skills without instant kill, HP_ZERO deaths below posture 100, the stagger without guard, Mortal Draw by B on contact only, Shield Attack + Helm Splitter.

One FIX01 contract changed on purpose: a wound **outside** its own attack now raises the guard instead of returning to the wait. It is still not a stagger or knockback. Inside its attacks, action, mode and heading are resumed exactly, as before.

## Hooks, imports, writers

| Item | 0.13.3 | 0.13.4 |
|---|---|---|
| HOOK_MEM / HOOK_MEM_EXT / HOOK_NAME | 29 / 15 / 13 | Same: no new `DEFINE_HOOK` |
| Install records | 20 | 21: one PRE on the existing `dCcS::ProcAtTgHitmark` |
| Game imports | 102 | Same, checked with clang locally and MSVC in CI |
| New writers | — | `kk_native_at_clear`, `kk_native_face` |

`kkb_guard_mark` calls the already-imported `dPa_control_c::setHitMark`.

## Limitations

- GPU and Present timing are not measured; the benchmark KCL is synthetic.
- The labs are a transcription plus a scripted Link, not the renderer: whether an FX is visible and whether one sound is heard as one can only be confirmed by you.
