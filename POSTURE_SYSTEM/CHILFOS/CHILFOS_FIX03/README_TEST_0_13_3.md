# Light Fades Twice 0.13.3 CHILFOS FIX03: private test

Status: **HUMAN_RUNTIME_PENDING** (also visual and performance). Install only the `.dusk` of a FULL run whose `independent-download` passed. Check its SHA-256 first.

## Install and rollback
1. Close Dusklight.
2. Back up and remove the active Light Fades Twice `.dusk` (0.13.2).
3. Put **only** `LIGHT_FADES_TWICE_CHILFOS_FIX03_0_13_3_PRIVATE_TEST_windows-amd64_<sha12>.dusk`.
   - Same ID `dev.posture.post05_selective_reactions`.
   - Do not touch other mods.
4. To roll back, remove 0.13.3 and restore 0.13.2 (SHA-256 `0cd15dc3046fb1ae4cefe1045bc1e5b6dc995e9af95084e34777979fc23bc767`).

## A and B
- **A:** one Chilfos alone (or with Enemy Spawner, labelled `LFT+Spawner`).
- **B:** your usual collection.

## Priority checks (log lines that prove each one)
1. **A raised guard never bleeds.** While it is visibly guarding, hit its front repeatedly: no HP loss and no damage particles.
   - **Log:** `VERDICT verdict=BLOCK ... guard_state=ACTIVE`.
   - **Expected:** side and back hits still land.
2. **HP 0 before posture 100 kills.** Wear it down with ordinary hits.
   - **Log:** `NATIVE_DEATH ... cause=HP_ZERO broken=0`.
3. **Back Slice (and the other hidden skills) never instant-kill at high HP.** They deal damage only.
   - **Log:** `CHILFOS_HP event=SKILL_INSTANT_SUPPRESSED`; never `cause=NATIVE_SKILL_INSTANT`.
4. **Stagger without any guard.** Break its posture, then Shield Attack and Helm Splitter. It must keep staggering (no blocking pose) and die on the Helm hit.
   - **Log:** `CHILFOS_BREAK event=TRACE what=STAGGER_CLIP_KEPT asked_bck=15 ... tgshield=0`, then `cause=HELM_SPLITTER`.
5. **Mortal Draw.** Break its posture, face it and press **B** (no R).
   - **Expected:** Link performs his native Mortal Draw. It dies only when the blade connects.
   - **Log:** `CHILFOS_EXEC event=B_REQUEST` → `START_NATIVE ... cut=31` → `KILL`, `cause=MORTAL_DRAW`.
   - **Also check:** B out of reach must not kill (`CANCELLED`); R+B must stay a Shield Attack.
6. **Four combos and C3.** The throw speed and look are unchanged.
   - **Log:** one `CHILFOS_PERF event=THROW_WINDOW` per throw (pre/post frame times, slow frames, `mod_hooks_ms`, `gpu=GPU_NOT_MEASURED`).
   - **Report:** a short video with an FPS counter, plus those lines.
7. **Kept from 0.13.2.** Spear never breaks on a block (`blocked_spear_break=0`), parries, counters, no slide, ×1.10 bursts, FIX01 behaviour, HUD, Lizalfos.

Share only the filtered `CHILFOS*` lines, the final `CHILFOS_SUMMARY` and short videos.
