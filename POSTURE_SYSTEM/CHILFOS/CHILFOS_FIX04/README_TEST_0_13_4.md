# Light Fades Twice 0.13.4 CHILFOS FIX04: private test

Status: **HUMAN_RUNTIME_PENDING**, **PERF_RUNTIME_PENDING**, **VISUAL_RUNTIME_PENDING**. Install only the `.dusk` of a FULL run whose `independent-download` passed; check its SHA-256 first.

## Install and rollback
1. Close Dusklight.
2. Back up and remove the active Light Fades Twice `.dusk` (0.13.3).
3. Put **only** `LIGHT_FADES_TWICE_CHILFOS_FIX04_0_13_4_PRIVATE_TEST_windows-amd64_<sha12>.dusk` (same ID `dev.posture.post05_selective_reactions`). Do not touch other mods.
4. Rollback: remove 0.13.4, restore 0.13.3 (SHA-256 `7348ce11d0256f58e1ebd3fff3c559d1ce4417b0c915b5794828ed96a47b9006`).

## Priority checks
1. **C3 throw at 60 FPS.** Turn on an FPS counter and record from before the backstep until after the rearm: the first throw of the session and at least 5 more.
   - **Expected:** no dip during the wind-up. Speed, look and timing of the throw unchanged.
   - **Log:** `CHILFOS_PERF event=THROW_WINDUP ... native_ms_max=<well under 1> los_strides_per_kcl=<1-3>` and `THROW_WINDOW anchor=THROW_START`.
2. **One clash per spear attack.** Block single D and E attacks and the fast E-E bursts with the shield.
   - **Expected:** one sound and one spark per thrust, each burst thrust counted, no echo about a quarter second later.
   - **Log:** one `CHILFOS_CONTACT event=ATTACK ... native_rounds=1` per attack; `native_rounds=2` must never appear.
3. **Sparks.** Make 20+ parries of both kinds and 20+ normal blocks, including strong cuts and finishers into its guard.
   - **Expected:** an orange spark on every parry, a blue spark on every block, never both.
   - **Log:** `PARRY_FX event=FX_PAIR ... emitters>=1`; `CHILFOS_CONTACT_SUMMARY guard_marks=` counts the sparks added on strong hits.
4. **Repeated B, frontal and with side-steps.**
   - **Expected:** it keeps facing you while it waits and raises its guard when it covers a swing (`CHILFOS_DEFENSE event=GUARD_RAISED`). Pressing B without a plan should not win cheaply. Its own attacks, real flanks (rolls behind it) and HP wear-down must still work.
5. **Kept from 0.13.3.**
   - Mortal Draw with B on a broken Chilfos, killing on contact.
   - Shield Attack + Helm Splitter.
   - `cause=HP_ZERO` below posture 100.
   - Back Slice without instant kill.
   - The spear never breaks on a block.
   - Counters, x1.10 bursts, HUD, Lizalfos.

Share only the filtered `CHILFOS*` and `PARRY_FX` lines, the final `CHILFOS_SUMMARY` + `CHILFOS_CONTACT_SUMMARY`, and short videos.
