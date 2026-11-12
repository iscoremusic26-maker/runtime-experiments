# 0.13.4 CHILFOS FIX04: collision, FX, guard and performance matrices

Lab = `tests/kk_world_lab.cpp` (production adapter over the transcribed native code, scripted Link). Runtime = your test (pending).

## Collision: per spear attack (one native AT window = one token)

| Situation | Native rounds (clash SE) | Hit marks on Link | Receipt | Lab |
|---|---|---|---|---|
| Tip only on the shield | 1 | 1 | 1 block or parry | Yes |
| Tip + 2 or 6 shaft spheres in one pass | 1 (tip kept) | 1 | 1 | Yes |
| Contact held past the window close (stale flags) | 0 extra (0.13.3: +1 eight ticks later) | 0 extra | 0 extra | Yes |
| Contact continuing inside the window | 0 extra (echo cleared) | 0 extra | 0 extra | Yes |
| New attack while an older 8-tick timer runs | 1, played by the module at once | 1 | 1 | Yes |
| E-E burst (x1.10) | 1 per thrust | 1 per thrust | 1 per thrust | Yes |
| Body hit (no shield) | 0 (native) | 1 | 1 direct offer, credited by Link's own damage receipt | Yes |
| Link out of reach | 0 | 0 | 0 | Yes |
| Two Chilfos on one Link | 1 per attack each | 1 per attack each | — | Yes |
| C3 thrown spear (child E_KK) | Native, untouched | Native | — | — |

## FX

| Contact | Native branch | Spark | Colour | Sound |
|---|---|---|---|---|
| Link blocks its spear | dCcS shield mark | 1 per attack | Blue (native) | Link guard SE + 1 native clash |
| Link parries its spear (Shield Attack) | dCcS shield mark | 1 per attack | Orange (parry FX book) | Clash x1.22 |
| It blocks Link, weak cut | `damage_check` weak: `setHitMark(2,this)` | 1 native | Blue | Map 7 |
| It blocks Link, strong cut | strong `def_se_set` (no mark) -> guard | 1 (module, the same native call) | Blue | Map 0x1F (native) |
| It parries Link, weak cut | weak | 1 native | Orange | Map 7 x1.22 |
| It parries Link, strong cut | strong -> guard | 1 (module) | Orange | Map 0x1F x1.22 |
| Damage | Native | Native damage spark | — | Native |

## Guard (ready = not in its own attack, spear in hand, not broken)

| State when Link swings | 0.13.3 | 0.13.4 |
|---|---|---|
| Native wait, Link in front | Roll at contact; the alert stance did not change | Roll at swing start; the guard goes up if it covers |
| Native wait, Link side-steps slowly | No turn: a flank after ~68 degrees | Turns like the native guard (max 0x500 per tick) |
| Raised guard, front | Block 100 % | Block 100 % |
| Raised guard, flank or back | Hit | Hit (not 360) |
| Wounded outside its attack | Back to wait | Native guard raised |
| Inside its own attack | Hit (trade) | Hit (trade) |
| Fast flank (rolls behind it) | Hit | Hit |

## Performance (P0)

| Measure | 0.13.3 | 0.13.4 |
|---|---|---|
| Wind-up eye height | -1e9 | Link.y - 60 |
| BG strides per wind-up call per KCL | ~2 000 000 | 1-3 (vanilla) |
| Bench, CPU per call per KCL (synthetic KCL) | ~10.5 ms | ~0.06 us |
| Your log: sim ticks over 40 ms per throw | 15 (p99 44-45 ms) | PERF_RUNTIME_PENDING |
| GPU / Present | Not measured | Not measured |
