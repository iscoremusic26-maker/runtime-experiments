# Light Fades Twice 0.13.2 CHILFOS FIX02: private test

Status: **HUMAN_RUNTIME_PENDING**. Install only the `.dusk` of a FULL run whose `independent-download` passed. Check its SHA-256 first.

## Install and rollback
1. Close the game.
2. Back up and remove the active Light Fades Twice `.dusk` (0.13.1).
3. Put **only** `LIGHT_FADES_TWICE_CHILFOS_FIX02_0_13_2_PRIVATE_TEST_windows-amd64_<sha12>.dusk`.
   - Same ID `dev.posture.post05_selective_reactions`.
   - Never two packages with that ID.
   - Do not touch any other mod.
4. To roll back, remove 0.13.2 and restore 0.13.1 (SHA-256 `c802098433eb7bbd69dce98375d455a5121389ba4280cc4bdbe60f7927153316`). Verify that hash before installing it.

## A and B
- **A:** one Chilfos alone (native, or with Enemy Spawner; label it `LFT+Spawner`).
- **B:** your usual collection.

## Priority checks (log lines that prove each one)
1. **Spear never breaks on a block or parry.** Mash B from the front with full sword chains, including finishers. The spear must stay in its hands.
   - **Log:** `CHILFOS_SPEAR event=BLOCK_INTACT` where 0.13.1 broke it.
   - **Summary:** `blocked_spear_break=0`.
   - **Report:** any `CHILFOS_SPEAR event=LOST after_block_or_parry=1`.
2. **Defense under repeated B.** Expect many blocks and parries: `CHILFOS_DEFENSE event=VERDICT ... pressure=… guarantee=…`.
   - Hitting from the side or back must still work.
   - During its own combos it does not guard: a trade.
3. **Counter after every parry.**
   - `ENEMY_PARRY` → `COUNTER_DISPATCH` → `COUNTER` → `IMPACT_OPEN`, or `COUNTER_CANCELLED reason=…`.
   - The summary `counter_cancelled=` splits the reasons.
   - Block or parry the counter.
4. **No slide.** Trade blows at close range, blocking its thrusts and being parried.
   - **Log:** `CHILFOS_MOTION event=CONTACT kind=SPEAR_ON_LINK_SHIELD|LUNGE_CAPPED` and `event=SETTLE moved_chilfos=… moved_link=…`.
   - **Report:** video plus those lines if Link still slides (Link's own guard slip is native and was not touched).
5. **Double thrusts at ×1.10.** C1 4–5, C2 2–3 and 4–5, C3 1–2 and 3–4, C4 5–6: slower than 0.13.1, each one separately blockable/parryable.
   - **Log:** `CHILFOS_COMBO event=IMPACT_OPEN ... rate=1.10` for each.
6. **Kept from FIX01.**
   - **Below 100:** no stagger (`CHILFOS_POISE event=RESUMED`); R+B absorbed.
   - **At 100:** immediate break, with both finishers.
   - **Combos:** four combos, the C3 throw and `REARMED`.
7. **Regressions.** Lizalfos, HUD, FX, several Chilfos, room changes, FPS.

Share only the filtered `CHILFOS*` lines, the final `CHILFOS_SUMMARY` and short videos.
