# CHILFOS01 continuation implementation

This extends cf78e3a, Codex's 2adb7fd and the final-session commit; the architecture and native targets are inherited. No Lizalfos production file or shared integration hunk was changed. Runtime status: HUMAN_RUNTIME_PENDING.

## Corrections

* Sword finisher: a new sword collider still enters the native lethal path using temporary HP=2 and spear-less state. A native death is the receipt. Without it, restore the pre-call HP and do not count a finisher. The prior unconditional fallback death was reproduced with a zero-power collider and removed. Native death effects and action dispatch remain native.
* Iron Ball: preserve the original native branch, including status 0x400. Credit +30 only after an owned contact survives into native damage action with timer 8. Ignore callbacks during native invulnerability and PRE/POST pairs whose original was skipped. The transcription now includes status 0x400 in the native strong-hit branch. Ordinary lethal Iron Ball remains lethal and earns no posture.
* Defense: four aimed swings within 150 ticks reach C, without requiring two wounds. Cooldown is A/B/C 120/90/60 ticks at confirmed parry, matching the requested pressure behavior. Native rebound remains necessary. Guard baseline 30% remains provisional; no new guaranteed parries were added.
* Frame events: repeated accelerated attack event frames skip the repeated original call, preserving the visible frame and open collider while preventing duplicate native opening/sound. A production-adapter regression fails before this change. Native spawn-frame duplicate protection is retained.
* Throw: the inherited temporary eye-height sentinel is now limited to frames before 23; it is absent when the native child is created and during later recovery. POST restores it. No new native writer or hook target was added.

## Corrections after 2adb7fd (final session)

* **Crossing swing reused during the stagger (P0).** `kk_decide` returned the verdict cached for a swing before checking the stagger. The swing that raised posture to 100 keeps its cached `Damage`/`Block`/parry verdict. If that same swing contacted again after the native 8-tick `mDamageTimer` (long swings, spins), it ran the spear-less damage branch and could kill with the crossing swing. A cached `Block` would push the Chilfos from Yoroke into the native guard. During the stagger a cached verdict is now reused only when it is `Decisive` or `Ignored`; any other is decided again, and that swing becomes `Ignored`. A NEW swing still finishes. Lab: `lab_break` re-contacts with each cached verdict at 3 HP. Mutant: `stagger_reuses_crossing_verdict`.
* **Decisive contact without a native death kept the native spear-less reaction (P0).** A sword contact with zero native damage could still be decisive. Codex had already restored its HP. The native had also chosen the spear-less reaction `(7,1)` from our temporary spear-less state, and that reaction ended the 90-tick stagger early, so attacks became possible while broken. `damage_check` runs first in `action()`, so the POST now puts back the stagger action before `executeDamage` starts. It also logs `CHILFOS_BREAK event=DECISIVE_NO_RECEIPT` and counts `decisive_no_receipt` in the summary. Mutant: `decisive_no_receipt_leaves_stagger`.
* **Throw eye-height sentinel, residual risk re-measured.** The native `cc_set()` recomputes `eyePos` from the head joint in every `execute`, after `action()`. A POST skipped by another hook therefore cannot leave the sentinel past the current Execute. While the native `executeSpearThrow` is running (frames < 23 only), anything that reads `eyePos.y` sees the sentinel. No code change was needed.

## Evidence and limits

| Area | Production / tests | Evidence level |
|---|---|---|
| 4 combos, 26 melee + 1 projectile | kk_core.hpp, kk_adapter.inc / kk_lab, kk_world_lab | Pure policy and transcribed native execution; no DX12 rendering |
| HP/posture, Iron Ball | kk_adapter.inc / lab_break, identity/HP lab | Native source contract plus modeled collision receipts |
| Sword and Helm finish | kk_adapter.inc / lab_break | Native death transition in transcription; actual Link skill route needs runtime |
| Pressure/rebound/counter | kk_core.hpp, kk_adapter.inc / defense labs | Deterministic policy + scripted Link; all real animation procedures not exhaustively played |
| Frame crossing / duplicate events | kk_adapter.inc / lab_crossing | Production callbacks with native branch counters |
| C3 wall/throw/restore | kk_adapter.inc / lab_c3_tail | Transcription, not terrain/render certification |
| Lifecycle/hooks | kk_adapter.inc / lab_lifecycle, lab_install_all_or_nothing | Eight bounded slots; 17 install failure positions tested |
| D/E mapping | ANIMATION_IDENTITY.md | Unverified real BCK identity; modeled tip curves only |
| FX/HUD/Link/Lizalfos | existing bridge, inherited suites, kk_audit | Shared integration preserved; full visual/other-mod compatibility pending |

## Remaining runtime risks

The two-point tip classifier uses actor-relative samples but cannot certify the visual clip from names or synthetic curves. First episodes use the default mapping. Record actual BCK IDs and trajectory logs with video before accepting D/E.

The eye-height transaction still spans native code and any other registered callbacks. Narrowing its lifetime does not prove arbitrary third-party reentrancy or disable during PRE/POST safe. A native alternative with equivalent C3 behavior was not established. Test proximity, interruptions, walls, cliffs, pause/cutscene and scene transitions. Do not call this integration universally safe.

The Helm route preserves the host's mCutTypeCheck(2) lethal exceptions; scripted shield+Helm success does not certify every real Link procedure or eliminate native hidden-skill kills outside posture. Ordinary shield alone is tested non-lethal. Real visual guard congruence, orange-only FX and x1.22 audio require human confirmation.

## Rhythm

RHYTHM_TABLE.txt is retained: achieved means simulated native event timing, never observed gameplay. Four minimum-spacing differences remain: C1 4→5 0.260→0.333 s; C3 1→2 0.213→0.333 s; C3 3→4 0.233→0.333 s; C4 5→6 0.137→0.333 s. C3 tail 1.407→1.400 s refers to projectile emission, not arrival. Original ZIP and all four members match the requested SHA256 and CRC.

## Validation discipline

No Windows build, ABI certification or final package is claimed by local GCC labs. The Windows FAST→INTEGRATION→FULL profiles must use one final source SHA and an identical ledger; full download and hashes are separate required checks. An additional local -Wall -Wextra -Werror smoke experiment found pre-existing frozen-file warnings in Lizalfos/shared headers; those results are retained as failures, not silently passed. Existing Windows compiler flags and inherited CI suites remain unchanged.
