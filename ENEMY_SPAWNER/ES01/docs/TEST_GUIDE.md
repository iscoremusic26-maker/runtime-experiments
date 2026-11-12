# Human test (Windows / DX12)

Status: **HUMAN_RUNTIME_PENDING**. CI checks the code, the host API contract with a model and the native parameter decoding; only the game shows the real menu, the real enemies and their attacks.

## Install (game closed)
Replace **only** the Enemy Spawner `.dusk` 0.1.1 in your mods folder with the 0.1.2 one. Never keep both. Do not touch the other mods.

## 1. The panel
1. Start the game, open the Mods window, then the Enemy Spawner tab. No `Failed` and no `mod UI panel build failed`.
2. Open the **Enemy** dropdown: 50 entries, all in English. The first 45 are those of 0.1.1 in the same order; the last five are Stalfos (Alternate Attack), Darknut (Sword), Stalfos (Breakable Shield), Bulblin (Bow), Bulblin (Fire Bow).
3. Your previous choice is still selected (the index did not move). Choose another entry, close and reopen the tab: the choice is kept.
4. In the log: `ENEMY_SPAWNER event=INSTALL version=0.1.2 entries=50 original_entries=45`, and no `UI_BUILD_FAILED`.

## 2. Stalfos: base vs Alternate Attack (main goal)
Use an open, flat area, ideally at night-independent places (any field).
1. Spawn **Stalfos**. Let it attack several times without blocking. Expected: the long wind-up attack (`BCK_SF_ATTACK01`). In the log: `NATIVE_SELECTOR ... observed=mType:0,arg3:0 match=YES`, then `NATIVE_ATTACK_OBSERVED ... action=ACTION_ATTACK(5) anm=BCK_SF_ATTACK01(4) ... match=YES`.
2. Spawn **Stalfos (Alternate Attack)**. Expected: a different, shorter sword and a quicker attack (`BCK_SF_ATTACK02`). In the log: `observed=mType:1,arg3:0 match=YES`, then `action=ACTION_ATTACK_0(4) anm=BCK_SF_ATTACK02(5) expected_bck=5 mType=1 match=YES`.
3. For each: does the attack **hit** Link (damage), and does your shield **block** it? Does the Stalfos guard, crumble, reassemble, and die to a bomb or after crumbling? Note anything that differs from the base Stalfos.
4. Report: visible attack, real hit, block, death. A log line alone is not a pass.

## 3. Darknut: mace vs sword
1. Spawn **Darknut**: the mace Darknut of 0.1.1. Expected unchanged.
2. Spawn **Darknut (Sword)**: the same Darknut with a sword model. Log: `observed=mType:1,mType2:1 match=YES`.
3. Fight both through the armour break and the second phase, until death. Check that the sword hits, that the armour falls, and that nothing else happens (no cutscene, no camera change, no music change you would not get with the mace one).
4. The **Temple of Time Darknut is not in the list**: by design (see `docs/VARIANTS_0_1_2.md`).

## 4. Stalfos (Breakable Shield)
Block its attacks and hit its shield repeatedly. Expected: the shield breaks, then the Stalfos no longer guards. Log: `observed=mType:0,arg3:1 match=YES`.

## 5. Bulblin (Bow) and (Fire Bow)
At a distance, the Bulblin should shoot arrows (fire arrows for the second). Log: `weapon_type:2` / `weapon_type:3`, `match=YES`. The base **Bulblin** (club) must be unchanged.

## 6. Regression of 0.1.1
1. Lizalfos, Keese, a Chu, Bokoblin (E_OC, native): spawned in front of Link, facing him, fighting.
2. Spawn 12 enemies: the 13th press shows "Maximum of 12 active spawned enemies reached". Kill some and spawn again.
3. Kill one, change room and come back, reload, close the game: no crash and no duplicated enemies.
4. Refusals: at a cliff edge, in water, against a wall, during a cutscene: an English notice, nothing spawned.
5. Expansion entries without Expansion: "Bokoblin Expansion is not loaded". Black: "Bokoblin Black integration is unavailable".

## 7. With and without the optional mods
- **Enemy Spawner alone**: sections 1 to 6.
- **With Bokoblin Expansion 0.17.0 + Enemy Variant Framework 0.15.0**: Blue → "classified ... as BLUE" (220 HP), Red → "as RED" (330 HP), Black refused. If a Red attacks but does not regenerate health, note it: regeneration belongs to Expansion, not to this mod.
- **With Light Fades Twice 0.12.5**: a spawned Lizalfos logs `LIZ_POSTURE event=ADMITTED`; blocks, parries and posture behave like a placed Lizalfos.
- **With all your mods**: repeat 2, 3 and 6.

In the log, look for `ENEMY_SPAWNER` and, at shutdown, `ENEMY_SPAWNER_SUMMARY` (it now counts `selector_match`, `selector_mismatch`, `stalfos_attack0_seen`, `stalfos_attack_seen`, `stalfos_attack_unexpected`).

## Rollback
Close the game, remove the 0.1.2 `.dusk` and put back the 0.1.1 FIX01 `.dusk`. If an entry above 44 was chosen, 0.1.1 does not know that index: its dropdown may show no selection, and **Spawn Enemy** answers "Invalid enemy selection" until another entry is chosen.
