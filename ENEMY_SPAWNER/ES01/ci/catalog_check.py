"""Enemy Spawner 0.1.2: every catalog entry is either Dawnlight's (same profile, parameters, argument, angle.z, flying) or a documented change.
Reads src/catalog.hpp as text against ci/dawnlight_reference.json (extracted from Dawnlight b5e9046). Usage: catalog_check.py <project>
0.1.2: the 0.1.1 rule is unchanged for rows 0..44. The appended native variants are NOT Dawnlight entries: each one is an explicit exception of
ci/variants_0_1_2.json (label, profile, parameters, argument, angle.z, flying, the Dawnlight entry it derives from and the native evidence), and it
must sit after every Dawnlight-derived row. Any other label, or a variant that drifts from its exception, still fails."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
ref = json.loads((root / 'ci/dawnlight_reference.json').read_text())
variants = json.loads((root / 'ci/variants_0_1_2.json').read_text())
exceptions = {v['label']: v for v in variants['appended']}
txt = (root / 'src/catalog.hpp').read_text()
rows = re.findall(r'\{"([^"]+)", Profile::(\w+), (0x[0-9a-f]+)u, (-?\d+), (0x[0-9a-f]+|0), (0x[0-9a-f]+|0), (true|false), Route::(\w+), Adapt::(\w+)\}', txt)
errors = []
byname = {e['label']: e for e in ref['entries']}
alias = {}
seen = set()
first_variant = None
for i, (label, prof, par, arg, ax, az, fly, route, adapt) in enumerate(rows):
    if label in exceptions:
        v = exceptions[label]
        if first_variant is None:
            first_variant = i
        base = byname.get(v['derives_from'])
        same = prof == v['profile'] == (base or {}).get('profile') and int(par, 16) == int(v['parameters'], 16) and int(arg) == v['argument'] and int(az, 0) == v['angle_z'] \
            and (fly == 'true') == v['flying'] and route == 'Native' and adapt == 'None'
        if not same:
            errors.append('appended variant differs from its exception: ' + label)
        if base is None or int(arg) != base['argument'] or int(az, 0) != base['angle_z'] or (fly == 'true') != base['flying']:
            errors.append('appended variant does not keep its Dawnlight base placement fields: ' + label)
        continue
    if first_variant is not None:
        errors.append('a Dawnlight-derived row after the appended variants: ' + label)
    if label.startswith('Bokoblin'):
        e = byname['Bokoblin']
        if prof != 'E_OC' or int(par, 16) != int(e['parameters'], 16):
            errors.append('Bokoblin entry differs: ' + label)
        seen.add('Bokoblin')
        continue
    key = alias.get(label, label)
    if key not in byname:
        errors.append('not a Dawnlight entry: ' + label)
        continue
    e = byname[key]
    seen.add(key)
    same = prof == e['profile'] and int(par, 16) == int(e['parameters'], 16) and int(arg) == e['argument'] and int(az, 0) == e['angle_z'] and (fly == 'true') == e['flying']
    if not same and key not in ref['changed']:
        errors.append('undocumented change: ' + label)
    if same and key in ref['changed']:
        errors.append('documented change not present: ' + label)
missing = [e['label'] for e in ref['entries'] if e['label'] not in seen and e['label'] not in ref['not_offered']]
if missing:
    errors.append('Dawnlight entries dropped without a reason: %s' % missing)
for name in ref['not_offered']:
    if name in seen:
        errors.append('not offered but present: ' + name)
present = [r[0] for r in rows if r[0] in exceptions]
if present != [v['label'] for v in variants['appended']]:
    errors.append('appended variants missing or out of order: %s' % present)
for name in variants['not_offered']:
    if any(r[0] == name for r in rows):
        errors.append('variant ruled out in 0.1.2 but present: ' + name)
out = {'status': 'CATALOG_FAIL' if errors else 'CATALOG_PASS', 'rows': len(rows), 'dawnlight_rows': len(rows) - len(present), 'appended_exceptions': present, 'errors': errors}
print(json.dumps(out, indent=1))
sys.exit(1 if errors else 0)
