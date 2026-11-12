# Catalog

50 entries. Entries 0..44 are the 45 entries of 0.1.1 FIX01, unchanged (`ci/baseline_0_1_1.json`). Their parameters, profiles and sentinels come from Dawnlight `b5e9046`, checked by `ci/catalog_check.py` against `ci/dawnlight_reference.json`. Entries 45..49 are the native variants of 0.1.2, explicit exceptions listed in `ci/variants_0_1_2.json` (evidence in `docs/VARIANTS_0_1_2.md`).

| Group | Entries |
|---|---|
| Bokoblin | E_OC native, E_OC2 native, Blue (Expansion), Red (Expansion), **Black (Expansion): integration unavailable** |
| Humanoids | Darknut (the mace Darknut), Lizalfos, Dynalfos, Bulblin, Stalfos, Stalchild, Stalhound (night only), Gibdo, Puppet |
| Animals and others | White Wolfos, Rat, Bomskit, Tektite, Dodongo, Skulltula, Helmasaur, Helmasaurus, Armos |
| Ice | Chilfos, Freezard, Mini Freezard |
| Flying (+200) | Keese (normal, fire, ice), Bubble (normal, fire, ice), Aeralfos, Kargarok, Guay |
| Plants | Baba Serpent, Big Baba, Deku Baba |
| Toadpoli | Water and fire, with Dawnlight's adaptation to stay on the chosen ground |
| Chu | Red, blue, yellow, purple, black |
| 0.1.2 variants (at the end) | Stalfos (Alternate Attack), Darknut (Sword), Stalfos (Breakable Shield), Bulblin (Bow), Bulblin (Fire Bow) |

**Not offered:** Goron (an NPC), Staltroop (it removes itself without Stallord, and Dawnlight replaces its AI), the Temple of Time Darknut (cutscenes, camera, Link teleport and a stage save bit; see `docs/VARIANTS_0_1_2.md`), Bulblin bomb arrows (refused by the native create).

**Depends on the environment, no guarantee:**
- Stalhound only appears at night.
- Outside its dungeon, Dodongo's fire may not be visible: the game creates no particle when the scene lacks it, and the native code tolerates that.
- Aeralfos, Armos and Big Baba belong to special rooms: they are created with Dawnlight's no-arena parameters.
- Stalfos (both attacks) in room 7 of any stage starts sitting (native rule of `d_a_e_sf.cpp`, as for the 0.1.1 Stalfos).
- Fire arrows can set burnable things on fire, as in the game.
