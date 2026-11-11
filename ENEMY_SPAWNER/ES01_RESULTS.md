# Enemy Spawner (Standalone): CI results

## 0.1.1 FIX01 (current)

Status: **CI FULL PASS, HUMAN_RUNTIME_PENDING**. Not executed in the game.

FIX01 fixes the Mods panel that failed to build in 0.1.0 (log `dusklight-20261111-091855`: `SELECT controls need a help pane (mod window tabs)` → `mod UI panel build failed`). The chooser is now `UI_CONTROL_DROPDOWN`, and every user-visible text is English. See `ES01/docs/FIX01.md`.

| Item | Value |
|---|---|
| Compiled source | `2365018403d52fc70dd6a1b2971d3d1bc76ed531` (branch `feature/enemy-spawner-standalone-v0-1-1-fix01`) |
| CI | branch `ci/enemy-spawner-standalone-v0-1-1`, FULL run 43041748974 at CI head `d60414bb6f55b02124393f602ca3c4af1f13da88` (`build` and `independent-download` green) |
| Artifact | 13866460257 `ES_TEST_43041748974_1`, expires 2026-12-11 |
| Package | `ENEMY_SPAWNER_STANDALONE_FIX01_0_1_1_PRIVATE_TEST_windows-amd64_2365018403d5.dusk`, 16 030 bytes |
| Package SHA-256 | `1b331d46b2426c85947331a20b6cf507579ceecd5b85868c6315e74a82346207` (recomputed from an own download through the API) |
| DLL | 33 280 bytes, SHA-256 `7310f07d0326dce8277decabff11c0bc57b4262cb6d390d6e3350930e2588e38`, PE32+ AMD64 |
| Files | `mod.json`, `lib/windows-amd64/mod.dll` (plus the two directory entries of the archive) |

| Check | Result |
|---|---|
| Source rules | PASS, 38 negatives rejected (18 new for the panel and the version) |
| English audit | PASS, 166 production literals, manifest and 8 documents; 10 negatives rejected |
| PE audit | PASS, 21 game imports (unchanged from 0.1.0), no hook, no hook service |
| Catalog against Dawnlight `b5e9046` | PASS, 45 entries, same order |
| Vendored Expansion code | PASS, 0.17.0 hash |
| Core laboratory | 1 248 checks, 0 failures |
| Adapter laboratory | 56 checks, 0 failures |
| Panel laboratory (new) | 1 878 checks, 0 failures; real SDK UI header, host control model |
| Mutants | 58/58 detected (34 previous + 24 panel/English), 0 timeouts |
| Independent download | `ARTIFACT_DOWNLOADED_VERIFIED` (CI job and own download); the DLL contains the English texts and none of the 0.1.0 Spanish ones |

Measured times: FAST 1 min 19 s (run 43040959596), INTEGRATION 2 min 4 s (43041289307), FULL 3 min 19 s (43041748974; mutants 62 s).

Locally (WSL, not CI): the three laboratories also pass under ASan/UBSan, and the clang-cl cross-build passes the same PE audit.

Limit: the panel laboratory models the host's `pane_add_control` as read in `TwilitRealm/dusklight@40457c6`. It does not run the RmlUi window. Only the game shows the real menu.

## 0.1.0 (superseded: its panel fails to build in the game)

| Item | Value |
|---|---|
| Compiled source | `983e1286ebd8a0f5c7dc66870e70bd0a4293ef33` (branch `feature/enemy-spawner-standalone-v0-1-0`) |
| CI | branch `ci/enemy-spawner-standalone-v0-1-0`, FULL run 42983880736 |
| Package | `ENEMY_SPAWNER_STANDALONE_0_1_0_PRIVATE_TEST_windows-amd64_983e1286ebd8.dusk`, 15 659 bytes, SHA-256 `6627c4a0274239371a39d0ea8d8ff20e5856aefd5eaee4b359970bbbb03647ff` |
| Human result | FAILED: the Mods panel was refused by the host (SELECT without a help pane) |

Problems found and fixed while building 0.1.0: header offsets are GameCube offsets (invented offset assertions removed), a non-virtual destructor in the lab model, the CI plan check compared phase order, and two surviving mutants (tests added).
