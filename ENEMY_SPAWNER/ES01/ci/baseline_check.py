"""Enemy Spawner 0.1.2: the 45 entries of 0.1.1 FIX01 are untouched (test A of the 0.1.2 brief).
Compares src/catalog.hpp, row by row, with the frozen inventory ci/baseline_0_1_1.json (taken from 4330ec68acff51bb8bd2d323d2784cc9bcedf480): index, label,
profile, parameters, argument, angle.x, angle.z, flying, route and adaptation of rows 0..44 must be identical, and every later row must be one of the
appended variants listed below, in that order. Proven by its own negatives. Usage: baseline_check.py <project>"""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
BASE = json.loads((root / 'ci/baseline_0_1_1.json').read_text())
ROW = re.compile(r'\{"([^"]+)", Profile::(\w+), (0x[0-9a-f]+)u, (-?\d+), (0x[0-9a-f]+|0), (0x[0-9a-f]+|0), (true|false), Route::(\w+), Adapt::(\w+)\}')
# The only rows 0.1.2 may add, after index 44, exactly (docs/VARIANTS_0_1_2.md).
APPENDED = [
    {'label': 'Stalfos (Alternate Attack)', 'profile': 'E_SF', 'parameters': '0x0100ff00', 'argument': -1, 'angle_x': 0, 'angle_z': 0xff, 'flying': False, 'route': 'Native', 'adapt': 'None'},
    {'label': 'Darknut (Sword)', 'profile': 'B_TN', 'parameters': '0x010001ff', 'argument': -1, 'angle_x': 0, 'angle_z': 0, 'flying': False, 'route': 'Native', 'adapt': 'None'},
    {'label': 'Stalfos (Breakable Shield)', 'profile': 'E_SF', 'parameters': '0x1000ff00', 'argument': -1, 'angle_x': 0, 'angle_z': 0xff, 'flying': False, 'route': 'Native', 'adapt': 'None'},
    {'label': 'Bulblin (Bow)', 'profile': 'E_RD', 'parameters': '0xff000200', 'argument': -1, 'angle_x': 0, 'angle_z': 0, 'flying': False, 'route': 'Native', 'adapt': 'None'},
    {'label': 'Bulblin (Fire Bow)', 'profile': 'E_RD', 'parameters': '0xff000300', 'argument': -1, 'angle_x': 0, 'angle_z': 0, 'flying': False, 'route': 'Native', 'adapt': 'None'},
]

def rows(txt):
    out = []
    for i, r in enumerate(ROW.findall(txt)):
        out.append({'index': i, 'label': r[0], 'profile': r[1], 'parameters': '0x%08x' % int(r[2], 16), 'argument': int(r[3]), 'angle_x': int(r[4], 0), 'angle_z': int(r[5], 0),
                    'flying': r[6] == 'true', 'route': r[7], 'adapt': r[8]})
    return out

def check(txt):
    e = []
    got = rows(txt)
    base = BASE['entries']
    if BASE['count'] != 45 or len(base) != 45:
        e.append('the frozen inventory is not the 45 entries of 0.1.1')
    for b in base:
        i = b['index']
        if i >= len(got):
            e.append('row %d missing' % i)
        elif got[i] != b:
            diff = sorted(k for k in b if got[i].get(k) != b[k])
            e.append('row %d (%s) changed: %s' % (i, b['label'], diff))
    extra = got[45:]
    want = [dict(a, index=45 + k) for k, a in enumerate(APPENDED)]
    if extra != want:
        e.append('appended rows differ from the reviewed list: %s' % [x['label'] for x in extra])
    labels = [x['label'] for x in got]
    if len(set(labels)) != len(labels):
        e.append('duplicate labels')
    # The mace Darknut is the 0.1.1 "Darknut" and is offered once; no B_TN row may decode to mType 0 (Temple of Time).
    tn = [x for x in got if x['profile'] == 'B_TN']
    if any(((int(x['parameters'], 16) >> 8) & 0xFF) != 1 for x in tn):
        e.append('a B_TN row decodes to mType 0 (Temple of Time Darknut)')
    if sum(1 for x in tn if (int(x['parameters'], 16) >> 24) != 1) != 1:
        e.append('the mace Darknut must be offered exactly once')
    return e, got

def main():
    txt = (root / 'src/catalog.hpp').read_text(encoding='utf-8')
    errors, got = check(txt)
    negs = [
        ('{"Stalfos", Profile::E_SF, 0x0000ff00u', '{"Stalfos", Profile::E_SF, 0x0100ff00u'),                 # a 0.1.1 row changed in place
        ('    {"Darknut", Profile::B_TN, 0x000001ffu, -1, 0, 0, false, Route::Native, Adapt::None},\n', ''),    # a 0.1.1 row removed
        ('    {"Stalfos (Alternate Attack)",', '    {"Stalfos (Alternate Attack) ",'),                            # an appended row renamed
        ('    {"Lizalfos",', '    {"Stalfos (Alternate Attack)", Profile::E_SF, 0x0100ff00u, -1, 0, 0xff, false, Route::Native, Adapt::None},\n    {"Lizalfos",'),  # inserted above 45
        ('{"Darknut (Sword)", Profile::B_TN, 0x010001ffu', '{"Darknut (Sword)", Profile::B_TN, 0x000000ffu'),      # Temple of Time Darknut
        ('{"Darknut (Sword)", Profile::B_TN, 0x010001ffu', '{"Darknut (Sword)", Profile::B_TN, 0x000001ffu'),      # a duplicated mace Darknut
        ('{"Gibdo", Profile::E_GI, 0x00ff01ffu, -1, 0, 0, false', '{"Gibdo", Profile::E_GI, 0x00ff01ffu, -1, 0, 0, true'),  # a flag changed
        ('{"Water Toadpoli", Profile::E_TK, 0x00ff0000u, -1, 0, 0, false, Route::Native, Adapt::ToadpoliWater}', '{"Water Toadpoli", Profile::E_TK, 0x00ff0000u, -1, 0, 0, false, Route::Native, Adapt::None}'),
        ('{"Bokoblin Red (Expansion)", Profile::E_OC, 0x00ff0000u, -1, 0x0100', '{"Bokoblin Red (Expansion)", Profile::E_OC, 0x00ff0000u, -1, 0x0000'),
        ('    {"Bulblin (Fire Bow)", Profile::E_RD, 0xff000300u, -1, 0, 0, false, Route::Native, Adapt::None},\n', '    {"Bulblin (Fire Bow)", Profile::E_RD, 0xff000300u, -1, 0, 0, false, Route::Native, Adapt::None},\n    {"Bulblin (Bomb Arrows)", Profile::E_RD, 0xff000400u, -1, 0, 0, false, Route::Native, Adapt::None},\n'),
    ]
    rejected = 0
    for old, new in negs:
        if txt.count(old) != 1:
            errors.append('negative anchor missing: %r' % old[:60])
            continue
        if check(txt.replace(old, new, 1))[0]:
            rejected += 1
        else:
            errors.append('negative accepted: %r' % new[:60])
    out = {'status': 'BASELINE_FAIL' if errors else 'BASELINE_PASS', 'frozen_rows': 45, 'rows': len(got), 'appended': [x['label'] for x in got[45:]],
           'negatives_rejected': rejected, 'errors': errors}
    print(json.dumps(out, indent=1))
    sys.exit(1 if errors else 0)

main()
