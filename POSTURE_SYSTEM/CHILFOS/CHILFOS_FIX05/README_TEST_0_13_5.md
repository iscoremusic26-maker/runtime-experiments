# Light Fades Twice 0.13.5 CHILFOS FIX05: private test

Status: **HUMAN_RUNTIME_PENDING**, **VISUAL_RUNTIME_PENDING**, **PERF_RUNTIME_PENDING**. Install only the `.dusk` of a FULL run whose `independent-download` passed. Check its SHA-256 first.

## Install and rollback
1. Close Dusklight.
2. Back up and remove the active Light Fades Twice `.dusk` (0.13.4).
3. Put **only** `LIGHT_FADES_TWICE_CHILFOS_FIX05_0_13_5_PRIVATE_TEST_windows-amd64_<sha12>.dusk` in its place (same ID `dev.posture.post05_selective_reactions`). Never two versions at once; do not touch other mods.
4. Rollback: remove 0.13.5 and restore 0.13.4 (SHA-256 `28e8097b12a79f2b291f31913b777069c359912e2cc6a36ed759acd916c66b20`).

## Profiles
- **A, isolated:** only Light Fades Twice, plus Enemy Spawner if you use it to place enemies (say so).
- **B, your usual set:** Enemy Spawner, Bokoblin Expansion, Enemy Variant Framework, Enemy Health Bars, HM203 and the rest you normally load.

## Priority checks
1. **Recovery without a finisher (P0).** Break a Chilfos to 100 and do nothing for 3 s; repeat 5+ times.
   - **Expected:** one continuous stagger that ends upright, then it fights. No second bow, no pose jump.
   - **Log:** `CHILFOS_BREAK event=RECOVERED ... at_end=1 wraps=0`, and `CHILFOS_STAGGER event=PLAN end=<real clip length>`.
2. **Jump Attacks (P1), against both enemies.** From the front, repeat jump attacks for ~60 s; also from behind, and with jumps that land short.
   - **Expected:** it guards often and sometimes parries. On a parry in the air Link is thrown back mid-jump (heading reversed, he lands normally); on a parry at the landing he plays his ground recoil. Then a counter follows. Behind it, hits land.
   - **Log:** `CHILFOS_JUMP event=VERDICT ... phase=AIR|LAND verdict=...`, `CHILFOS_DEFENSE event=SWORD_REBOUND_NATIVE`, `LIZ_DEFLECT event=SWORD_REBOUND_NATIVE`. The summary `jump_land_merged` should be about one per jump.
3. **Both thrusts of a fast double (P2).** R+B on the first thrust, then R+B again on the second.
   - **Expected:** two independent parries, each with an orange spark and the parry sound; a blue spark on a block.
   - **Log:** two `CHILFOS_LINK event=PARRY` in the same pair; `CHILFOS_FIX05_SUMMARY burst_gap_ticks>0`.
4. **Helm Splitter height (P3).** Shield Attack a broken Chilfos, then the Helm Splitter. Compare with a Lizalfos; try flat floor, a step and a low ceiling.
   - **Expected:** a jump proportioned to its height, the kill on contact.
   - **Log:** `CHILFOS_HELM event=AIM_LIFTED native_rel lifted_rel` and `HELM_HIT ... link_peak`.
5. **Mortal Draw (P4).** B on a broken Chilfos, with and without Z-targeting.
   - **Expected:** a smooth finish, no brief downward bend of Link's torso as it falls.
   - **Log:** `CHILFOS_EXEC event=POSE_HOLD_END held_ticks native_eye_drop`.
6. **Kept from 0.13.4.**
   - The C3 throw at 60 FPS (`CHILFOS_PERF event=THROW_WINDUP`).
   - One clash and one spark per spear attack.
   - Blue blocks, orange parries; the spear never breaks.
   - HP 0 kills below posture 100.
   - Hidden skills without instant kill.
   - Lizalfos: its four patterns, double hits, tail, parry, HUD.

Share the filtered `CHILFOS*`, `LIZ_*` and `PARRY_FX` lines, the final `CHILFOS_SUMMARY`, `CHILFOS_CONTACT_SUMMARY`, `CHILFOS_FIX05_SUMMARY` and `LIZ_SUMMARY` lines, and short videos of points 1, 2, 4 and 5.
