# Light Fades Twice 0.13.1 CHILFOS01 FIX01: private test

Status: **HUMAN_RUNTIME_PENDING**. Install only the `.dusk` of a FULL run whose `independent-download` job passed. Check its SHA-256 before installing.

## Install and rollback
1. Close the game.
2. Back up the active Light Fades Twice `.dusk` (0.13.0 or FIX05 0.12.5). Then remove it from the mods folder.
3. Put **only** `LIGHT_FADES_TWICE_CHILFOS01_FIX01_0_13_1_PRIVATE_TEST_windows-amd64_<sha12>.dusk`.
   - Same ID `dev.posture.post05_selective_reactions`.
   - Never two packages with that ID.
   - Do not touch any other mod.
4. To roll back, remove 0.13.1 and restore one of these (verify the hash before you install it):

| Version | SHA-256 |
|---|---|
| 0.13.0 | `84613cc9beebc9014a9c5b9c43cf34ca90068ef19b3af4be9410cc89b050bede` |
| FIX05 0.12.5 | `8d62780bc0782ce68dc88cd86b930915933892eb2f25919791a9edfed21c6775` |

## A and B
- **A:** one Chilfos alone (native, or spawned with Enemy Spawner 0.1.1; label that session `LFT+Spawner`).
- **B:** the same with your usual mod collection.
- Record version, scene/room and active mods.

## Priority checks (each with the log lines that prove it)
1. **No stagger below 100.** Hit it from the front, side and back while it waits, walks, guards, attacks, and during the C3 backstep, throw and restore.
   - **Expected:** it loses HP and keeps fighting, with no flinch, no backward slide and no retreat.
   - **Log:** `CHILFOS_POISE event=RESUMED ... native=7/<mode> kept=<action>/<mode>` for each hit.
   - **Report:** a hit followed by a flinch or retreat with no `RESUMED` line.
2. **Shield Attack (R+B) below 100.** Press R+B at its body and against its thrusts.
   - **Expected:** no knockback, no HeadLock, combo continues, one hit sound per press.
   - **Log:** `CHILFOS_POISE event=SHIELD_ATTACK_ABSORBED`.
   - **Report:** a `CHILFOS_COMBO event=END ... cause=NATIVE_PRIORITY` right after it.
3. **Four combos without your intervention.** Stay just inside its range and only guard.
   - C1 DDDEED, C2 DEEEED, C3 EEEEDED + backstep + one throw + regeneration, C4 DDEDEEE.
   - **Expected:** `END cause=COMPLETED`.
   - **Report:** any other cause, which now names its `origin=`, `phase=`, `last_link=`.
4. **C3 tail visual.** Video of backstep → throw → disarmed → regeneration ×1.60 → fighting again.
   - **Log:** `CHILFOS_SPEAR event=BACKSTEP`, `THROW_START`, `THROW_SPAWN count=1`, `RESTORE`, `REARMED`.
   - Also test near walls/cliffs and with Link closing in.
   - **Report:** any pose pop, foot sliding, frozen frame, missing spear, two spears.
5. **D/E identity.** Watch which clip is the diagonal slash and which the thrust.
   - **Log:** `CHILFOS_ANIM event=TRAJECTORY ... identity=` should settle on `MEASURED_DEFAULT` (BCK5 = D, BCK6 = E).
   - **Report:** a video if the screen disagrees.
6. **Parries.**
   - Parry each burst hit (C1 4–5, C3 1–2 / 3–4, C4 5–6): `CHILFOS_LINK event=PARRY` (+13) or `POSTURE_GAIN kind=BLOCK` (+20) once per hit.
   - Swing repeatedly at its front to make it parry: `CHILFOS_DEFENSE event=ENEMY_PARRY`, a real sword rebound, then `event=COUNTER`.
7. **Break.**
   - **Reach 100:** `CHILFOS_BREAK event=STAGGER` (immediately). The crossing swing never kills.
   - **New sword hit:** `SWORD_DECISIVE` + `NATIVE_DEATH`.
   - **Alternative:** a new Shield Attack (`SHIELD_PREP`) then Helm Splitter (`route=HELM_SPLITTER`).
   - **No finisher:** after 3 s `event=RECOVERED`, posture 0, same HP.
   - **Report:** if `DECISIVE_NO_RECEIPT` appears.
8. **Regressions.** Compare the Lizalfos and other enemies with FIX05.
   - Check the HUD bars (none on a thrown spear), orange parry sparks, the ×1.22 parry sound, multiple Chilfos, room changes and FPS.

Share only the filtered `CHILFOS*` lines and the final `CHILFOS_SUMMARY`, plus short videos; never the whole raw log. Lab and CI results are not a visual or DX12 certificate.
