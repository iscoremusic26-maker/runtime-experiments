"""Verify and preserve only textual Windows evidence; compare compiled own source to this tree."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--zip',type=Path,required=True)
p.add_argument('--output',type=Path,required=True);p.add_argument('--project',type=Path,required=True)
a=p.parse_args()
EXPECTED='abc8050097518c7f621ff99af93d790f181bf1861e1a664d40ccde27f4e4daca'
allowed={'build.log','cmake-version.log','compiler.log','configure.log','guard-hidden-mutation.log',
         'guard-hidden-spawn.log','guard-mutation.log','guard-positive.log','lab.log',
         'module-exports.log','module-imports.log','result.json'}
blob=a.zip.read_bytes()
if hashlib.sha256(blob).hexdigest()!=EXPECTED: raise SystemExit('GitHub artifact digest mismatch')
with zipfile.ZipFile(a.zip) as z:
    if z.testzip() is not None: raise SystemExit('Artifact CRC failure')
    if set(z.namelist())!=allowed or len(z.namelist())!=len(allowed): raise SystemExit('Unexpected artifact members')
    result=json.loads(z.read('result.json'))
    if result['status']!='PASS' or result['lab_summary']!='SUMMARY 36 PASS; synthetic observer lifecycle only; no native backend or game execution':
        raise SystemExit('Missing scoped PASS')
    if result['game_executed'] or result['host_built'] or result['packaged_or_installed']:
        raise SystemExit('Unexpected execution scope')
    comparison=[]
    for item in result['own_code']:
        raw=(a.project/item['path']).read_bytes().replace(b'\r\n',b'\n')
        if hashlib.sha256(raw).hexdigest()!=item['sha256']: raise SystemExit(f"Own code changed: {item['path']}")
        comparison.append(item['path'])
    a.output.mkdir(parents=True,exist_ok=True);files=[]
    for i in z.infolist():
        raw=z.read(i.filename);raw.decode('utf-8')
        (a.output/i.filename).write_bytes(raw)
        files.append({'path':i.filename,'bytes':len(raw),'crc32':f'{i.CRC:08x}',
                      'sha256':hashlib.sha256(raw).hexdigest()})
verification={'run_id':38297058072,'job_id':114970558041,'artifact_id':11768783927,
    'run_url':'https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38297058072',
    'private_ci_head':'988bafed31e93674082cc926086e56d92728c175',
    'main_compiled_source_commit':'57a167a6c650ab9473db31c4eac531dba8e6a127',
    'zip_sha256':EXPECTED,'zip_bytes':len(blob),'github_digest_match':True,'crc_all_pass':True,
    'text_only_members_pass':True,'own_compiled_code_lf_identical':comparison,
    'additional_collection_tools':'Post-build read-only evidence extraction, not part of the module/lab',
    'files':files}
(a.output.parent/'windows-verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
print('PASS_STATIC: artifact digest/CRC/text allowlist and all compiled own-code hashes match')
