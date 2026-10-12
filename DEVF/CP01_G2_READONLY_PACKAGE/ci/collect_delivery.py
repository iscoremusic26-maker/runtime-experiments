"""Verify the actual private Actions downloads, preserve only text in Git, never load the DLL."""
import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
sys.dont_write_bytecode=True
from audit import pe_audit

p=argparse.ArgumentParser();p.add_argument('--text-zip',type=Path,required=True)
p.add_argument('--package-zip',type=Path,required=True);p.add_argument('--private-work',type=Path,required=True)
a=p.parse_args();project=Path(__file__).resolve().parents[1]
TEXT='e2c15672b693000bf29899b41268245ebc4de4868ae7850acb45956ff9eee317'
PACKAGE='a0c1533e1a2b1808df3af5b93729fd1fb733f09250e74d34d4147700758b2182'
allowed={'build.log','cmake-version.log','compiler.log','configure.log','DOWNLOAD_MANIFEST.json',
 'guard-hidden-mutation.log','guard-hidden-spawn.log','guard-mutation.log','guard-positive.log',
 'lab.log','module-exports.log','module-imports.log','package.log','result.json'}
for path,digest in [(a.text_zip,TEXT),(a.package_zip,PACKAGE)]:
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest: raise SystemExit('GitHub artifact digest mismatch')
with zipfile.ZipFile(a.text_zip) as z:
    if len(z.namelist())!=len(allowed) or set(z.namelist())!=allowed or z.testzip() is not None:
        raise SystemExit('Unexpected/nontext evidence archive or CRC failure')
    result=json.loads(z.read('result.json'));manifest=json.loads(z.read('DOWNLOAD_MANIFEST.json'))
    if result['status']!='G2_PACKAGE_READY_FOR_USER_REVIEW' or result['lab_summary']!='SUMMARY 47 PASS; synthetic observer lifecycle only; no native backend or game execution':
        raise SystemExit('Missing scoped final PASS')
    if result['game_executed'] or result['host_built'] or result['installed']:
        raise SystemExit('Unexpected execution scope')
    compared=[]
    for item in result['own_code']:
        raw=(project/item['path']).read_bytes().replace(b'\r\n',b'\n')
        if hashlib.sha256(raw).hexdigest()!=item['sha256']: raise SystemExit(f"Compiled source differs: {item['path']}")
        compared.append(item['path'])
    destination=project/'evidence/windows-pass';destination.mkdir(parents=True,exist_ok=True);files=[]
    for i in z.infolist():
        raw=z.read(i);raw.decode('utf-8');(destination/i.filename).write_bytes(raw)
        files.append({'path':i.filename,'bytes':len(raw),'crc32':f'{i.CRC:08x}',
                      'sha256':hashlib.sha256(raw).hexdigest()})
with zipfile.ZipFile(a.package_zip) as z:
    if set(z.namelist())!={manifest['name'],'DOWNLOAD_MANIFEST.json'} or len(z.namelist())!=2 or z.testzip() is not None:
        raise SystemExit('Unexpected package artifact or CRC failure')
    if json.loads(z.read('DOWNLOAD_MANIFEST.json'))!=manifest: raise SystemExit('Download manifests differ')
    data=z.read(manifest['name'])
    if len(data)!=manifest['bytes'] or hashlib.sha256(data).hexdigest()!=manifest['sha256']:
        raise SystemExit('Downloaded .dusk hash or size mismatch')
    a.private_work.mkdir(parents=True,exist_ok=True)
    package=a.private_work/manifest['name'];package.write_bytes(data)
with zipfile.ZipFile(package) as z:
    members=result['package_verification']['members']
    if z.namelist()!=[i['path'] for i in members] or z.testzip() is not None:
        raise SystemExit('Inner package layout/CRC mismatch')
    for item in members:
        raw=z.read(item['path'])
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise SystemExit('Member integrity mismatch')
    dll=a.private_work/'downloaded-own-inspection.dll';dll.write_bytes(z.read('lib/windows-amd64/mod.dll'))
    if pe_audit(dll)!=result['pe_audit']: raise SystemExit('Downloaded packaged PE differs')
verification={'status':'PASS_STATIC','run_id':38302076854,'job_id':114987154136,
 'run_url':'https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38302076854',
 'artifact_url':'https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38302076854/artifacts/11771626280',
 'text_artifact':{'id':11771686151,'bytes':a.text_zip.stat().st_size,'sha256':TEXT},
 'package_artifact':{'id':11771626280,'bytes':a.package_zip.stat().st_size,'sha256':PACKAGE,
    'name':'DEVF_CP01_G2_READ_ONLY_windows-amd64_b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2',
    'expires_utc':'2026-10-26T20:08:01Z','authenticated_github_download_verified':True},
 'github_digests_match':True,'outer_and_inner_crc_pass':True,'download_manifests_identical':True,
 'downloaded_dusk':manifest,'all_packaged_members_verified':True,'downloaded_dll_pe_audit_identical':True,
 'compiled_own_files_lf_identical':compared,'native_files_copied_to_git':False,'dll_or_game_executed':False,
 'text_files':files}
(project/'evidence/download-verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
print('PASS_STATIC: actual private download, artifact/.dusk/member SHA256+CRC, PE and source hashes verified')
