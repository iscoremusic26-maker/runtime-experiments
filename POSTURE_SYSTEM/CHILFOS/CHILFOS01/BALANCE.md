# CHILFOS01: balance (as requested; one provisional value marked)

## Chilfos
| Item | Value |
|---|---|
| HP | 340, written once from the exact native 140/140 of `daE_KK_c::create`. Any other value (e.g. another mod scaled it) is kept and logged `HP_FOREIGN`. |
| Posture | 0..100 |
| Link parries a Chilfos melee impact | +13 to the Chilfos, nothing to Link |
| Sword hit that removes HP | +5 |
| The Chilfos blocks a sword hit | +3 |
| The spear breaks without HP loss (native CLASH) | +5, once per real break |
| The Chilfos parries Link | +0 to the Chilfos, +25 to Link, native sword rebound, no HP on that contact |
| Iron Ball | Native lethal behavior is preserved. An owned Iron Ball contact accepted into native damage (timer 8 and damage action), surviving the call, receives +30. Player status 0x400 is the native exception; no health or lethal branch is overridden. |
| Regeneration | starts after 60 eligible ticks without a genuine gain. By current HP: 256..340 → 12/s, 171..255 → 8/s, 86..170 → 5/s, 35..85 → 2/s, 1..34 → 1/s. Never while latched or staggered, never in a damage reaction, never at 0 HP. HP never regenerates. |
| Break | at 100: a native stagger (Yoroke, held 90 ticks absolute) |

## Link
Shared LNK scale for ATP1 (the native atp of `cc_kk_at_src`):
- a normally blocked Chilfos melee impact: +20;
- a direct hit: +30, credited only with Link's native damage receipt;
- a Chilfos parry of Link: +25;
- a Link parry: +0.

At 100, LNK05's native guard break request (unchanged).

## Defense (Lizalfos FIX05 semantics, re-derived for E_KK)
- **Swings that count:** a swing counts only when aimed at the Chilfos (±45°, ≤ 320 units). One roll per swing.
- **Parry intent:**
  - A 12%;
  - B 35% (3 swings in 75 ticks);
  - C 45% (4 aimed swings in 150 ticks, no wound prerequisite);
  - after two blocks of two different swings within 45 ticks: 80% on the continuation.
- **No parry:** without the spear, while its own AT is open, from the flank (> 67.5°), during the A/B/C 120/90/60-tick cooldown after a parry, or while staggered.
- **Presenting the parry:** a prepared parry presents the body cylinder as a shield (TgShield) for that swing only. This replaces the native auto-deflect of the 4th+ cut and of spins/jumps. Link's rebound is native (`checkCutReverseAt` / `changeCutReverseProc`), and it is kept only for a real parry.
- **Guard prepared by wounds:** after 1/2/3 consecutive wounds the guard roll is 45/80/100%. It is up only 6 ticks after the wound (never retroactive) and is forgotten after 90 ticks.
- **[BALANCE_PROVISIONAL]** The guard roll of a frontal, ready Chilfos with no wound streak is **30%**. The request gives no value. Without one the native Chilfos would block 100% of sword hits while it holds the spear.
- **Counter:** only after a confirmed parry. One real D or E (50/50) at x1.25/x1.30, within 60 ticks.

## Stagger and finishers
- **The crossing contact never kills:** the swing that raised posture to 100 is ignored during the stagger. This holds even when that swing contacts again after the native 8-tick timer: its pre-stagger verdict is never reused.
- **A) Shield Attack, then Helm Splitter:**
  - another Shield Attack during the stagger gives the native HeadLock;
  - Link's native Helm Splitter then hits;
  - the native lethal branch (`mCutTypeCheck(2)`) kills the Chilfos.
  - The Shield Attack alone does not kill. It does not renew the 90 ticks.
- **B) A new sword swing:** any NEW sword swing that connects runs the native lethal branch (`health <= 1` after `cc_at_check`, then `executeDead`).
  - The module writes `health = 2` and `field_0x67d = 1` for that one call.
  - No fallback death is allowed. Without native death the temporary HP cap is rolled back; no finisher is counted. A zero-damage collision regression reproduces the old false death.
  - In that case the stagger action is also put back before the native spear-less reaction runs, so the stagger keeps its 90 ticks (`CHILFOS_BREAK event=DECISIVE_NO_RECEIPT`).
- **Timeout:** after 90 ticks without a kill: posture 0, same HP, HeadLock off, back to the fight (with its spear: the native wait; without it: the native backstep that restores it).
- **Outside the stagger:** a Shield Attack staggers natively, but the module removes the HeadLock, so Helm Splitter stays the finisher, not a shortcut.
- **Other native lethal routes stay native at any time:**
  - the Iron Ball;
  - the hidden skills that the native `mCutTypeCheck(2)` lists (great spin, jump strike, mortal draw, back slice).
  - This is a deliberate native-priority decision. If they should not kill outside the stagger, say so.

## Lizalfos (unchanged, byte-identical to FIX05)
- 370 HP, 100 posture.
- Gains: sword +6, Link parry +12, block +5, Iron Ball +30; Link +25 on an enemy parry.
- Regeneration: 10/7/4/2/1 after 2 s.
- Stagger 3 s, pitch x1.22, adaptive guard.
- `src/liz_core.hpp` and `src/liz_adapter.inc` are hash-pinned to FIX05 by `tests/test_kk_source.py`.

## FIX01 0.13.1: posture below 100 never staggers (FIX05 rule)
- **Sword hits:** a non-lethal contact removes HP and credits +5 once per swing, but never leaves the Chilfos in a native damage reaction. Its action, mode and heading are kept, in every phase including the C3 tail.
- **Link's Shield Attack on the body:** below 100 it is absorbed. No DRAWBACK, no HeadLock, no HP, no posture, the combo goes on, and one native contact SE plays per press. During the stagger it still prepares Helm Splitter.
- **At 100:** the stagger starts in the same contact.
- **Native exceptions, unchanged:**
  - arrows, boomerang, hookshot and bombs keep their native reaction (the FIX05 rule for non-sword weapons);
  - the Iron Ball keeps its native branch;
  - a strong hit that natively breaks a held spear keeps its CLASH reaction (+5 once).
- **C3 tail:** BACKSTEP / THROW / RESTORE is committed: no guard and no prepared parry.
