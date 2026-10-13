"""Independently reopen the actual Actions download; inspect only in scratch, never install/load DLL."""
import argparse,json,zipfile
from pathlib import Path
from verify_package import HERE,OBS,sha,safe_members,verify,historical_difference
p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--metadata',type=Path,required=True);p.add_argument('--runner-evidence',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
meta=json.loads(a.metadata.read_text());work=a.work;work.mkdir(parents=True,exist_ok=True)
runner=json.loads((a.runner_evidence/'package-result.json').read_text());expected=json.loads((a.runner_evidence/'DOWNLOAD_MANIFEST.json').read_text());approval=json.loads((HERE/'SOURCE_APPROVAL.json').read_text())
if runner['status']!='RUNNER_PACKAGE_VERIFIED_DOWNLOAD_PENDING':raise RuntimeError('Runner gates not passed')
if a.archive.stat().st_size!=meta['size_in_bytes'] or sha(a.archive.read_bytes())!=meta['digest'].removeprefix('sha256:'):raise RuntimeError('Outer download size/digest mismatch')
if meta['workflow_run']['head_sha']!=runner['ci_head'] or int(meta['workflow_run']['id'])!=int(runner['run_id']):raise RuntimeError('Wrong artifact provenance')
name=expected['filename'];expected_name='DEVF_CP01_G4B_READ_ONLY_windows-amd64_'+approval['approved_checkpoint']+'.dusk'
if name!=expected_name or meta['name']!=expected_name.removesuffix('.dusk'):raise RuntimeError('Wrong G4B artifact identity')
with zipfile.ZipFile(a.archive) as z:
    outer=safe_members(z,{name,'DOWNLOAD_MANIFEST.json'},set())
    manifest=z.read('DOWNLOAD_MANIFEST.json')
    if manifest!=(a.runner_evidence/'DOWNLOAD_MANIFEST.json').read_bytes():raise RuntimeError('Download manifest differs from runner evidence')
    raw=z.read(name)
if sha(raw)!=expected['package_sha256'] or len(raw)!=expected['package_bytes']:raise RuntimeError('Downloaded .dusk differs from audited runner package')
if expected['module_id']!='dev.devf.g4b_local_readonly' or expected['module_version']!='0.0.1' or expected['policy']!='DISARMED_NO_REGISTRATION' or not expected['read_only'] or expected['runtime']!='RUNTIME_NOT_TESTED' or expected['execution_authorized'] or expected['installation_authorized']:raise RuntimeError('Wrong policy/identity')
package=work/name;package.write_bytes(raw)
with zipfile.ZipFile(package) as z:
    safe_members(z);inside=z.read('lib/windows-amd64/mod.dll')
if sha(inside)!=expected['dll_sha256'] or len(inside)!=expected['dll_bytes']:raise RuntimeError('Downloaded internal DLL differs from audited runner hash/size')
dll=work/'downloaded-inspection.dll';dll.write_bytes(inside)
verification=verify(package,dll,work=work)
verification['downloaded_internal_vs_extracted_copy_identical']=verification.pop('built_and_packaged_dll_byte_identical')
if verification['pe_audit']!=runner['package_verification']['pe_audit'] or verification['exports']!=runner['package_verification']['exports']:raise RuntimeError('Independent packaged DLL audit differs')
if verification['members']!=runner['package_verification']['members']:raise RuntimeError('Downloaded members differ')
difference=historical_difference(dll,approval)
if difference!=runner['historical_difference']:raise RuntimeError('Historical comparison differs on downloaded DLL')
r={'status':'G4B_PACKAGE_DOWNLOAD_VERIFIED','artifact_id':meta['id'],'run_id':runner['run_id'],'ci_head':runner['ci_head'],'outer_bytes':a.archive.stat().st_size,'outer_sha256':sha(a.archive.read_bytes()),'outer_crc_pass':True,'outer_members':outer,'package':verification,'historical_difference':difference,'comparison_scope':'runner compared loose build DLL vs package byte-for-byte; independent download matches full package and DLL hashes and repeats complete PE/ZIP/manifest audit','artifact_expiry_utc':meta['expires_at'],'execution_authorized':False,'installation_authorized':False,'dll_executed':False,'game_executed':False}
(work/'download-verification.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['status','artifact_id','outer_bytes','outer_sha256','artifact_expiry_utc']},indent=2))
