# Light Fades Twice 0.13.0 CHILFOS01 private test

Status: HUMAN_RUNTIME_PENDING. Install only an artifact explicitly backed by final FULL and independent-download evidence; a FAST internal build is not installable delivery.

With the game closed, back up FIX05 0.12.5 and replace only Light Fades Twice. Never activate two packages with ID dev.posture.post05_selective_reactions. Do not change other mods. Roll back by removing only 0.13.0 and restoring FIX05 (SHA256 8d62780bc0782ce68dc88cd86b930915933892eb2f25919791a9edfed21c6775).

A: use a native Chilfos encounter, or explicitly label the run LFT+Enemy Spawner 0.1.1. B: repeat with the usual mod collection. Record version, source SHA, scene/room and which other mods were active.

1. Verify a fresh combatant has 340 HP and a 0..100 posture bar; thrown child spears have neither. Verify externally modified HP is preserved.
2. Record BCK5/6 video and CHILFOS_ANIM trajectory lines. Check D/E visually and all combos: C1 DDD EED; C2 D EEEE D; C3 EEEE DED then backstep/one throw/regeneration; C4 DD E D EEE. Each episode chooses once, approximately 25% each.
3. Block and parry every burst hit, especially C1 4–5, C3 1–2/3–4, C4 5–6. Each needs an independent collision. Whiffs grant nothing.
4. Spam aimed sword chains from front, side and back. Confirm real rebound, +25 Link, no simultaneous enemy HP loss, and a real counter after parry; ordinary blocks have no false parry FX. No spear means no weapon parry.
5. Reach posture100: crossing hit does not finish, even if that same long swing or spin touches the Chilfos again; a NEW connecting sword hit kills. If `CHILFOS_BREAK event=DECISIVE_NO_RECEIPT` ever appears, report it: the Chilfos must keep staggering and keep its HP. Separately test Shield Attack then connecting Helm; shield alone and a missed Helm do not finish. At 90 ticks, posture resets and HP is preserved.
6. C3 must backstep safely, emit exactly one spear, stay disarmed until visible fast regeneration, then fight again. Test close approach, walls/cliffs and damage/death before/at/after frame23 and during restore; pause, cutscene and room change.
7. Verify orange particles at both objects and one native parry sound at pitch1.22, only on real parry. Preserve ordinary ice, Z-target, Manual Shielding, R+B, Link posture and unobstructed HUD.
8. Compare Lizalfos and other enemies with FIX05. Test multiple Chilfos, external spawning, slot exhaustion, room/stage changes, FPS and clean exit.
9. Report filtered CHILFOS events/summaries and relevant errors with short video. Do not upload raw private logs. Geometric lab success is not a visual or DX12 certificate.
