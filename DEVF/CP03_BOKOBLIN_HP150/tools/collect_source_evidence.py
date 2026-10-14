"""Read-only CP03 provenance collector. No build, DLL loading, game or HP writes.

Pins Git objects and verifies checkpoint manifests; semantic conclusions remain
the reviewed Markdown report, never a regex-derived runtime PASS.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = '40457c6adb381928e4b5fef6ed459ed291edd5e2'
AURORA = '3227d76c60e1e782ca576610bce61c9e7744d8be'
CP02 = '0d2430262181bb2844f13bb8da0a628f71740998'
CI = 'd3a85769f096e2d6eb065ddf2d69847ab0b6b8e1'
FILES = {
    'src/d/actor/d_a_e_oc.cpp': [(638, 780), (2704, 2863)],
    'include/d/actor/d_a_e_oc.h': [(20, 88)],
    'include/d/d_stage.h': [(210, 225)],
    'include/f_op/f_op_actor.h': [(275, 330)],
    'include/f_op/f_op_actor_mng.h': [(61, 83), (531, 555)],
    'sdk/include/mods/svc/stage.h': [(14, 40)],
    'sdk/include/mods/svc/actor.h': [(14, 91)],
    'sdk/include/mods/svc/game.h': [(9, 29)],
    'sdk/include/mods/svc/config.h': [(24, 102)],
    'src/dusk/mods/svc/stage.cpp': [(139, 218)],
    'src/dusk/mods/svc/actor.cpp': [(56, 123), (220, 318), (359, 400)],
    'src/d/d_stage.cpp': [(1635, 1662), (2611, 2635), (2816, 2835)],
    'docs/modding.md': [(753, 800), (1237, 1353)],
    'src/f_op/f_op_actor_mng.cpp': [(258, 275)],
    'include/f_pc/f_pc_manager.h': [(45, 48), (66, 114)],
    'include/f_pc/f_pc_create_req.h': [(35, 40)],
    'src/f_pc/f_pc_create_req.cpp': [(18, 74), (84, 120)],
    'include/f_pc/f_pc_stdcreate_req.h': [(8, 12)],
    'src/f_pc/f_pc_stdcreate_req.cpp': [(67, 109), (140, 177)],
    'src/f_pc/f_pc_base.cpp': [(179, 198)],
    'src/d/d_cc_uty.cpp': [(434, 448)],
}

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def lf(raw):
    return raw.replace(b'\r\n', b'\n')

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def collect(source, main, ci):
    require(git(source, 'rev-parse', 'HEAD').decode().strip() == ROOT, 'Official root changed')
    require(git(source / 'extern/aurora', 'rev-parse', 'HEAD').decode().strip() == AURORA, 'Aurora changed')
    require(not git(source, 'status', '--porcelain'), 'Official tree dirty')
    require(git(ci, 'rev-parse', 'HEAD').decode().strip() == CI, 'CI CP02 changed')
    require(not git(ci, 'status', '--porcelain'), 'CI tree dirty')
    require(git(main, 'rev-parse', 'DEVF_CP02_EOC2_ELITE_NATIVE_PACKAGE_VERIFIED^{}').decode().strip() == CP02, 'CP02 tag changed')
    cp02 = main / 'DEVF/CP02_EOC2_ELITE_NATIVE'
    ledger = json.loads((cp02 / 'evidence/checkpoint-file-sha256.json').read_text())
    for path, expected in ledger.items():
        raw = (cp02 / path).read_bytes()
        require(len(raw) == expected['bytes'] and sha(raw) == expected['sha256'], 'CP02 ledger mismatch: ' + path)
    manifest = json.loads((cp02 / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['official_root'] == ROOT and manifest['aurora'] == AURORA, 'Manifest roots changed')
    counts = {}
    for key, base in [('sdk_lf_sha256', source), ('directed_sdk_source_sha256', source), ('reuse_lf_sha256', main / 'DEVF'), ('derivation_only_lf_sha256', main / 'DEVF')]:
        entries = manifest[key]
        for path, expected in entries.items():
            require(sha(lf((base / path).read_bytes())) == expected, key + ' mismatch: ' + path)
        counts[key] = len(entries)
    reviewed = {}
    for path, ranges in FILES.items():
        raw = (source / path).read_bytes()
        blob = git(source, 'show', ROOT + ':' + path)
        require(lf(raw) == lf(blob), 'Reviewed source differs from Git: ' + path)
        lines = lf(raw).decode().splitlines()
        reviewed[path] = {'git_blob': git(source, 'rev-parse', ROOT + ':' + path).decode().strip(), 'lf_sha256': sha(lf(raw)), 'bytes_lf': len(lf(raw)), 'lines': len(lines), 'review_ranges': ranges, 'url': 'https://github.com/TwilitRealm/dusklight/blob/' + ROOT + '/' + path}
    inventories = {}
    for name in ['stage', 'actor', 'game', 'config']:
        text = (source / ('sdk/include/mods/svc/' + name + '.h')).read_text()
        block = text.split('typedef struct ' + name.title() + 'Service {', 1)[1].split('} ' + name.title() + 'Service;', 1)[0]
        inventories[name] = re.findall(r'\(\*(\w+)\)', block)
    return {'kind': 'STATIC_PROVENANCE_ONLY', 'official_root': ROOT, 'aurora': AURORA, 'baseline_cp02': CP02, 'baseline_ci': CI, 'cp02_ledger_entries_verified': len(ledger), 'cp02_manifest_entries_verified': counts, 'reviewed_sources': reviewed, 'service_function_inventory': inventories, 'semantic_gate_automated': False, 'new_build': 'NOT_RUN_GATE_BLOCKED', 'new_fake_lab': 'NOT_RUN_NO_IMPLEMENTATION', 'game_execution': 'NOT_TESTED', 'original_resources_read_or_distributed': False}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', required=True, type=Path)
    p.add_argument('--main', required=True, type=Path)
    p.add_argument('--ci', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    result = collect(a.source, a.main, a.ci)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS static provenance: ' + str(len(result['reviewed_sources'])) + ' source files; ' + str(result['cp02_ledger_entries_verified']) + ' CP02 ledger entries; no build/game/HP operation')
