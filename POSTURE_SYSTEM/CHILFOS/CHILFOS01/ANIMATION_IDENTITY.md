# CHILFOS01: which native clip is the diagonal slash (D) and which is the thrust (E)

Status: **not verified offline**. The identity is measured at runtime from the engine's own pose, and a human must still confirm it visually.

## What the sources prove
- `E_kk.h` (GZ2E01) has two distinct attack clips: `KK_ATTACK01 = 0x5` and `KK_ATTACK03 = 0x6`. The native `executeAttack` picks one of them 50/50.
- Both clips run through the same native code:
  - the lunge (speedF 80) and the AT opening at frame 24;
  - the AT closing at frame 33 or later.
- The only native differences are their sounds:
  - `Z2SE_EN_KK_ATTACK03` plays at frame 24 of BCK 6 (the moment of the lunge);
  - `Z2SE_EN_KK_ATTACK01` plays at frame 27 of BCK 5 (three frames later).
- **Inference, not proof:** a sound on the lunge itself fits a thrust better than a slash, which peaks a little later. Neither the clip names nor the SE timing prove the shape.
- The BCK data lives in the game archive (`E_kk.arc` inside the user's disc image). It was **not read**:
  - no path to it was authorised;
  - the project rules forbid exploring the disk for it.

## What the module does about it
- **The default:** D = BCK 5 and E = BCK 6 (`kk_core.hpp` `kBckDiagonal` / `kBckThrust`). It is marked `DEFAULT_UNVERIFIED` in every `CHILFOS event=ADMITTED` and `CHILFOS_COMBO event=START` line.
- **Runtime measurement:** `mtx_set` computes the spear tip (`field_0x68c`, weapon joint 2 plus 230 units). For every clip it plays, the adapter samples that tip in the Chilfos' own frame (origin `current.pos`, yaw `shape_angle.y`, so the lunge itself does not count) twice:
  - once between frames 18 and 23;
  - once between frames 28 and 33.
- **Classification:**
  - forward motion larger than 1.5× the lateral/vertical motion → **THRUST**;
  - lateral/vertical motion larger than 1.2× the forward motion → **DIAGONAL**;
  - otherwise **UNSURE**.
- **Settling the identity:**
  - With at least 2 consistent votes per clip and opposite classes, the identity is settled for the session.
  - If BCK 5 measures as the thrust, the mapping is swapped (`MEASURED_SWAPPED`) and every later D/E uses the measured clip.
  - Contradictory evidence (both clips classify the same way) keeps the default and logs `CONFLICT_DEFAULT_KEPT`.
- **Log:** `CHILFOS_ANIM event=TRAJECTORY bck=.. lateral=.. vertical=.. forward=.. class=.. identity=..` (WARN on the line that settles it).

Until the first two clips of each kind have been measured, the first combo of the session may use the default mapping.

## What the laboratory proves (and what it does not)
- `tests/kk_world_lab.cpp` runs the production adapter with a **model** of the tip arcs (BCK 6 thrusts and BCK 5 sweeps in one session; the reverse in the other).
  - In both sessions the identity settles.
  - After that, every D action plays the clip that sweeps and every E action the clip that thrusts.
- `clip_d_e_inverted`, `identity_settles_on_one_vote` and `identity_swap_ignored` are mutants that the laboratory kills.
- **Limit:** the model arcs are not the BCK data. Whether the real tip moves enough to classify is **HUMAN_RUNTIME_PENDING**.

## Human check
1. Spawn a Chilfos and let it attack.
2. In the log, find the line `CHILFOS_ANIM event=TRAJECTORY` that settles the identity.
3. Watch which motion the module calls D and which E.
4. If the screen and the log disagree, report the two lines. The fix is one constant.
