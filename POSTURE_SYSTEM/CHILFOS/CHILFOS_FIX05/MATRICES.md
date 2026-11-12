# 0.13.5 CHILFOS FIX05: matrices

Lab = `tests/kk_world_lab.cpp` / `tests/liz_world_lab.cpp` (production adapters over the transcribed native code, scripted Link). Runtime = your test (pending).

## Stagger (posture 100, 90-tick window)

| Situation | 0.13.4 | 0.13.5 | Lab |
|---|---|---|---|
| No finisher, window runs out | Clip loops: upright, then a new bow, then cut to the wait | One play: bow, slow sway, its own upright end at RECOVERED, then the native wait | 30/30, 0 jumps back |
| Real new break later | New stagger | New stagger, planned anew | 30/30 |
| Shield Attack during the break (Helm prep) | Clip restarts | Clip restarts, planned over the time left | Yes |
| Mortal Draw extends the window | Loop could wrap | Holds its last frame | Yes |
| Death by HP / finishers | Unchanged | Unchanged | Yes |

## Jump Attack (CUT_TYPE_JUMP 0x0A)

| Phase / case | Chilfos 0.13.4 | Chilfos 0.13.5 | Lizalfos 0.13.4 | Lizalfos 0.13.5 |
|---|---|---|---|---|
| Takeoff + landing setCutType | 2 swings | 1 swing | 2 swings | 1 swing |
| Prepared parry, aerial contact | Block, no rebound | Parry, native aerial rebound (heading reversed, speed 27) | Block (0/50) | Parry (50/50) |
| Prepared parry, landing contact | Block | Parry, `ANM_CUT_RECOIL_B` -> `PROC_CUT_REVERSE` | Parry (new serial) | Parry (50/50), same serial |
| Raised guard | Block, 0 HP | Block, 0 HP, one gain per jump | Native | Native |
| Jump streak (2nd/3rd/4th+ in 6 s) | — | Parry floor 40/60/75 %, guard floor 60/80/90 % | — | Unchanged rolls |
| From behind | Damage | Damage | Native | Native |
| Out of reach / no contact | Nothing | Nothing | Nothing | Nothing |
| During its own combo | Trade | Trade, no parry | Native | Native |
| Helm Splitter (HEAD_JUMP 0x05) on a broken enemy | Finisher | Finisher | Finisher | Finisher |
| Jump Strike (LARGE_JUMP 0x12-0x14) | No rebound route: guard/damage | Same | Same | Same |

## 60 s of repeated Jump Attacks (Link interrupted ~20 ticks by every spear hit)

| Scenario | Version | Jumps | Enemy parries | Blocks | Damage verdicts | Posture gained | Counters |
|---|---|---|---|---|---|---|---|
| Front (200 u) | 0.13.4 | 21 | 0 | 9 | 33 | +182 | 0 |
| Front (200 u) | 0.13.5 | 27 | 13 | 8 | 6 | +39 | 13 |
| Edge (230 u) | 0.13.4 | 23 | 0 | 12 | 34 | +179 | 0 |
| Edge (230 u) | 0.13.5 | 30 | 10 | 3 | 17 | +69 | 10 |

It is still winnable: wounds, blocks with posture, flanks and its committed attacks remain.

## Fast bursts (E-E at x1.10)

| Pattern | Real pairs | Gap fed (0.13.4 / 0.13.5) | Second thrust parried in the lab | 0.13.4 log, second thrusts |
|---|---|---|---|---|
| C1 (acts 4-5) | 1 | gap 0: no / yes | Yes | 0 parries of 5 |
| C2 (2-3, 4-5) | 2 | no / yes | Yes | 0 of 8 |
| C3 (1-2, 3-4) | 2 | no / yes (0.13.4 also fed the long gap before act 3) | Yes | 0 of 5 |
| C4 (5-6) | 1 | no / yes | Yes | 0 of 3 |

## Helm Splitter aim (procCutHeadInit)

| State | Aim point | Jump height (lab model, Link on the same floor) |
|---|---|---|
| 0.13.4, broken (bowed head) | Bowed eye (55) | 55 |
| 0.13.5, broken + Shield Attack | Its own upright eye (150), never lower than native | 150 |
| Not broken | Native | Native |

## Mortal Draw finisher

| | 0.13.4 | 0.13.5 |
|---|---|---|
| Link's torso after the kill (lab, s16 units) | Dips 1454 toward the falling body | 0 |
| Clip, sound, kill on contact, camera | Native | Native |
| Other deaths / other enemies | — | No hold |
