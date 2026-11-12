# 0.1.2: native variants

Status: **HUMAN_RUNTIME_PENDING**. Everything below was read in the native source of Dusklight 2.0.3 (`TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`, the commit the mod is built against) and checked by the laboratories and CI scripts. Nothing here was observed in the game.

## Rules

- Entries 0..44 are the 0.1.1 FIX01 catalog, unchanged: same labels, order, indices, profiles, parameters, arguments, angles, flags, routes and adaptations (`ci/baseline_0_1_1.json`, `ci/baseline_check.py`). The persisted chooser index keeps naming the same enemy.
- New entries are appended at 45..49 (`ci/variants_0_1_2.json` lists them as explicit exceptions of the Dawnlight comparison).
- A variant is offered only when a native parameter bit, read by the actor's own `create()`, changes what the actor is or does, and when that path needs no event, camera, room, stage or save state.

## Added

| Index | Label | Profile | Parameters | What the native code does with it |
|---|---|---|---|---|
| 45 | Stalfos (Alternate Attack) | E_SF | `0x0100FF00` | `mType = (p >> 24) & 0xF = 1` (`d_a_e_sf.cpp` L1774). `e_sf_fight_run` chooses `ACTION_ATTACK_0` for mType 1 and `ACTION_ATTACK` for mType 0 (L515-519). `e_sf_attack_0` plays `BCK_SF_ATTACK02` and sets the hit flag on frames 15..22 (L556, L561); the base attack plays `BCK_SF_ATTACK01`, hit frames 81..86. Weapon `BMDR_SF_SWORDB` instead of `SWORDA` (L1716), attack sphere offset -30 instead of -60 along the sword (L1581-1585). Wait/walk animations `WAIT02`/`WALK03` instead of `WAIT01`/`WALK02`. HP 200, guard, crash, get-up and death code are shared with the base Stalfos. |
| 46 | Darknut (Sword) | B_TN | `0x010001FF` | The 0.1.1 **Darknut** (`0x000001FF`: `mType 1`, archive `B_tnp2`) with `mType2 = 1` (`d_a_b_tn.cpp` L5062). `mType2` has exactly one use: `CreateHeap` part 13 loads `BMDR_TN2_SWORD_A` instead of `BMDR_TN2_MACE` (L4967). |
| 47 | Stalfos (Breakable Shield) | E_SF | `0x1000FF00` | `arg3 = p >> 28 = 1` (L1775): shield model `BMDR_SF_SHIELDB` (L1732). Only arg3 1 loses durability (`field_0x5c0`, 30) on blocked hits; at 0 the shield breaks (`arg3 = 0xFF`, L1626-1637) and the Stalfos no longer guards (L1126). mType 0: the base attack. |
| 48 | Bulblin (Bow) | E_RD | `0xFF000200` | `weapon_type = (p & 0xF00) >> 8 = 2` (`d_a_e_rd.cpp` L7375). Bow model and arrow model (L7267-7290), `ACTION_BOW_RUN` when it sees Link (L1252), arrows created as `E_ARROW` children (L6910). |
| 49 | Bulblin (Fire Bow) | E_RD | `0xFF000300` | `weapon_type = 3`: the same, with fire arrows (`E_ARROW` parameter bit 1, fire sound, fire effect; L6833-6904). |

Shared by all: switch byte as in the base entry (no defeated-switch), spawned in Link's layer facing him, the 12 limit, every 0.1.1 guard.

### Darknut: the existing entry is the mace Darknut

`{"Darknut", Profile::B_TN, 0x000001FF, ...}` decodes to `mType 1`, `mType2 0`: archive `B_tnp2`, part 13 = `BMDR_TN2_MACE`. It is not duplicated. 0.1.2 adds only the sword model of the same Darknut.

What the sword variant does NOT change (read, not assumed): the AI, the attacks, the phases (armour break, `executeZakoChangeDemo`), the hitboxes (`mSwordSphs` follow the part-13 matrix, radius 45, the same for both models, L4774), the HP (`0x50`), the sounds and the throw of part 13. No new combo or pattern is claimed. `mBrkAnmFrame = (p >> 16) & 0xFFFF = 0x0100` is stored in a `u8`, so it is 0 as for `0x000001FF`: the same armour colour frame.

The label is "Sword", not "Greatsword": the native code names the model `BMDR_TN2_SWORD_A` and nothing in it says the sword is larger.

## Not added

| Candidate | Status | Reason |
|---|---|---|
| Darknut (Temple of Time), B_TN mType 0 (`0x000000FF`) | **Ruled out** | See below. A compile-time guard (`no_temple_of_time_darknut`) and CI rules refuse any B_TN entry that decodes to mType 0. |
| Darknut (Mace) | Ruled out | It is the existing "Darknut". |
| Bulblin (Bomb Arrows), weapon type 4 | Ruled out | The native create returns `cPhs_ERROR_e` for weapon type 4 or more (`d_a_e_rd.cpp` L7380). |
| Bulblin weapon type 0 (unarmed) | Not added | No attack of its own; it only wanders (`e_rd_fight_run` L1288-1296). |
| Bokoblin low-byte types 1..4 | Not added | 1: return-home behaviour only; 2: needs a bridge actor; 3/4: Forest Temple monkey-cage demo actions (`d_a_e_oc.cpp` L2810-2826). Bokoblin also interacts with Bokoblin Expansion; out of scope. |
| Lizalfos arg1 1 (skull helmet, `0xFF0001FF`) | Pending | Native (`d_a_e_dn.cpp` L3364, L1257-1270, L752): skull model, cliff tail attack and jump, bomb reaction, longer stun. Its differences show only near ledges and bombs, and Light Fades Twice's handling of it was not reviewed in this release. |
| Stalfos alternate attack + breakable shield (`0x1100FF00`) | Not added | A combination of two added variants; no new behaviour. |
| Chilfos types | Not added | Type 2 checks the Ball and Chain item; type 1 changes Snowpeak-specific behaviour (`d_a_e_kk.cpp` L114-120). |
| Aeralfos (City in the Sky) | Excluded | Excluded by the brief for this release. The regular Aeralfos stays. |
| Other catalog actors | Not added | No native selector with an independent gameplay difference was found that does not depend on a room, a path, a switch or an event. |

### Why the Temple of Time Darknut is not offered

Read in `d_a_b_tn.cpp` (mType 0 paths):

1. `create()` sets `ACT_ROOMDEMO` (L5140) and then calls `daB_TN_Execute` itself (L5160). The first Execute runs **inside the engine's create**, before any `mod_update` of this mod: `executeRoomDemo` orders an event (`fopAcM_orderPotentialEvent`), then stops the camera, sets trim bars and puts Link in demo mode, moving him (L1676-1822).
2. `create()` refuses to exist when `dComIfGs_isStageMiddleBoss()` is set for the current stage (L5042).
3. Every frame of its life, mType 0 calls `player->onBossRoomWait()` and `dKy_custom_colset` (environment colours) (L4535-4553).
4. Phase change: `executeChangeDemo` (event, camera, Link demo mode and position, L2678-2928). Opening: `dComIfGs_onOneZoneSwitch(14, room)` and stage BGM (L1857-1864).
5. Death: `executeEnding` orders an event, stops the sub-BGM, sets switch `mSwitchNo`, moves Link to fixed coordinates `(-100, -400, 550)` and calls **`dComIfGs_onStageMiddleBoss()`**: a persistent save bit of the current stage (L4181-4351). Spawned inside a dungeon, it would mark that dungeon's middle boss as defeated.
6. Its demo coordinates (`2250`, `-350`, room 2 of `D_MN09`) are the Temple of Time arena's.

Making it fight normally would mean redirecting its action state on every frame of its life (including the first Execute, which a mod cannot reach without a hook), and replacing its phase change and its death, which are themselves cutscenes that also perform the armour drop and the deletion. That is a reimplementation of the boss behind private state, not a spawn. 0.1.2 therefore does not offer it, and the guards above keep it from appearing by accident.

## Read-only telemetry (new in 0.1.2)

For entries of E_SF, B_TN and E_RD, once the actor exists and its create has finished, the mod reads (never writes) the fields the actor decoded and logs one line:

`ENEMY_SPAWNER event=NATIVE_SELECTOR ... expected=mType:1,arg3:0 observed=mType:1,arg3:0 match=YES`

For Stalfos it also logs, once per actor and kind, when a native attack action is running:

`ENEMY_SPAWNER event=NATIVE_ATTACK_OBSERVED ... action=ACTION_ATTACK_0(4) anm=BCK_SF_ATTACK02(5) expected_bck=5 mType=1 match=YES`

The fields are read by name through the SDK headers (`e_sf_class::mType`, `arg3`, `mAction`, `mAnm`; `daB_TN_c::mType`, `mType2`; `e_rd_class::weapon_type`), only after `fopAcM_GetName` confirms the profile. These lines are evidence for the human test. A line in a lab or in CI is not a game observation. `ENEMY_SPAWNER_SUMMARY` adds `selector_match`, `selector_mismatch`, `stalfos_attack0_seen`, `stalfos_attack_seen` and `stalfos_attack_unexpected`.
