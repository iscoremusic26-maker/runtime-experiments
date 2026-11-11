# CHILFOS01: rhythm analysis of the four original recordings

Status: the recordings were analysed. The in-game rhythm is **HUMAN_RUNTIME_PENDING**.

## Source and integrity
- `POSTURE_SYSTEM/CHILFOS/REFERENCES/CHILFOS_4_COMBOS_AUDIOS_ORIGINALES.zip` (branch `docs/chilfos-combo-audios`, commit `87cdd24`).
- ZIP: 497 207 bytes, SHA-256 `0513324d9629acb51bb01aa7c23b0345aef7560c16b4910701d9571306a4303e`. CRC test passed, four members.

| Member | Bytes | SHA-256 |
|---|---|---|
| Chilfos combo 1.m4a | 152 105 | `b3ea8fdd47d4e2d5096b78766a82cb6e6173e724ecea5e98c6499fe0a4e7260c` |
| Chilfos combo 2.m4a | 121 019 | `3d3b7a240463877d37e8be2a3f3ad467c66b3191ea73fc600fa6cb67a7ceddcd` |
| Chilfos combo 3 con ataque a distancia al final.m4a | 170 328 | `9e0ea754719e6dbf63b5a4a677fa1be85fd323023175a45f01a581f42ccf3574` |
| Chilfos combo 4.m4a | 183 180 | `e7101e8c19c2ba827fcacc4d884ede829a6ee0510d220812f1312e31ca155ad4` |

All four match the request. The originals were never re-encoded or rewritten, and they are not part of the `.dusk` package.

## Method (reproducible)
1. Each M4A was decoded to 48 kHz PCM **for analysis only**, with the system AAC decoder of Windows Media Foundation (`tools/m4a2wav.ps1`). This is a local temporary copy, which was then deleted. Decoded durations are 7.3839 s, 5.4799 s, 8.4985 s and 9.2880 s, within 1 ms of the request.
2. `tools/onsets.py` is pure Python. It computes a 10 ms window with a 5 ms hop over two signals: the broadband level and the high-frequency (first-difference) level.
   - **Onset strength:** the rise of the high-frequency log level over the previous 30 ms minimum.
   - **Peak picking:** a peak must reach at least 35% of the maximum and at least 12 dB above the noise floor. Peaks closer than 70 ms are merged.
   - **Precise onset:** the first sample at which the amplitude reaches 30% of the 70 ms local peak.
   - **Per-hit features:** peak level, rise, brightness (high-frequency minus broadband level), zero-crossing rate and the time to fall 20 dB.
3. **Sensitivity pass:** threshold 15% and floor +6 dB (`ONSETS_RAW.txt` keeps both outputs).

## Result
All real hits peak between -6.7 and -17.8 dB. Every other transient is at least 13 dB weaker (≤ -31 dB): handling noise, resonance or room noise. There is no ambiguity in the count.

| Combo | Onsets (s) | Intervals (s) |
|---|---|---|
| C1 | 0.6790, 1.8637, 3.0735, 4.0901, 4.3504, 5.2978 | 1.1847, 1.2098, 1.0166, **0.2603**, 0.9474 |
| C2 | 0.5882, 1.5617, 1.9325, 2.6237, 3.0129, 3.7575 | 0.9735, **0.3708**, 0.6912, **0.3892**, 0.7446 |
| C3 | 0.9966, 1.2100, 2.6556, 2.8884, 4.3105, 4.9375, 5.5415 → **6.9487** | **0.2134**, 1.4456, **0.2328**, 1.4221, 0.6270, 0.6040 → 1.4072 |
| C4 | 0.7304, 1.8575, 3.6551, 4.6174, 5.9804, 6.1171, 7.0501 | 1.1271, 1.7976, 0.9623, 1.3630, **0.1367**, 0.9330 |

- **Confidence:** ±10 ms per onset (5 ms analysis hop plus threshold placement). The previous estimates in the request are confirmed to within 0.02 s.
- **C4 5→6:** two distinct strong transients (-10.3 and -7.7 dB), 0.137 s apart. It is a real double hit, not an echo.
- **C3 final mark (6.9487 s):** it is ONE transient, the brightest of all the recordings (zcr 0.119, 205 ms decay). Above -45 dB there is no earlier, separate launch transient between 5.54 and 6.95 s. **Launch and impact cannot be separated in this recording.** The module puts the native spear release (throw frame 23) on this mark. The arrival time depends on Link's distance, and no exact arrival is promised.

## Recorded → realizable (tests/kk_lab.cpp `--table`, `RHYTHM_TABLE.txt`)
The interval is measured from one native AT opening (frame 24) to the next, at 30 Hz.

**Rules:**
- **No merged windows:** every action keeps its whole native window, frames 24..33 at its rate. At least one closed Execute separates two windows.
- **Restarted clips:** a restarted clip keeps at least 8 native wind-up frames, or 6 for the second thrust of a burst.
- **The first action** of each combo starts from frame 0.

| Transition | Recorded | Realizable | Difference | Cause |
|---|---|---|---|---|
| All non-burst transitions | — | within ±0.017 s | ≤ half a tick | — |
| C1 4→5 (E E burst) | 0.260 | 0.333 | +0.073 | 6 window ticks at ×1.50 + 4 ticks of a 6-frame wind-up |
| C2 2→3, 4→5 (E E) | 0.371, 0.389 | 0.367, 0.400 | -0.004, +0.011 | reachable |
| C3 1→2 (E E) | 0.213 | 0.333 | +0.120 | same physical floor |
| C3 3→4 (E E) | 0.233 | 0.333 | +0.101 | same physical floor |
| C4 5→6 (E E) | **0.137** | 0.333 | **+0.197** | 4.1 ticks would need two windows inside one native window |
| C3 7th → spear release | 1.407 | 1.400 | -0.007 | 19 backstep ticks, then the throw clip at ×1.45 |

**Why not shorter:**
- A second thrust 4 ticks after the first would have to open its AT while the first native window (6 ticks at ×1.50) is still open. That is ONE window. Counting it twice would be exactly the "second sound without a collider" the request forbids.
- Shortening the first window after a contact would make the rhythm depend on whether Link blocked, so it was rejected.
- The four burst intervals are therefore the realizable minimum of two physically distinct windows, each with its own parry.
