"""Read-only verification against independently fetched Git objects, never a DLL loader."""
import argparse,json,hashlib,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--git-dir',type=Path,required=True);p.add_argument('--ref',required=True);a=p.parse_args()
DIR='DEVF/CP01_A2_FIRST_ACTIVE_PACKAGE_REVIEW/'
def git(*args):return subprocess.check_output(['git','--git-dir='+str(a.git_dir),*args])
def blob(rel,ref=None):return git('show',(ref or a.ref)+':'+rel)
def doc(rel):return json.loads(blob(DIR+rel))
def sha(b):return hashlib.sha256(b).hexdigest()
base='0ff1b8bf5e331fc411d6dd9e5fc70c7b3809c75e'
subprocess.run(['git','--git-dir='+str(a.git_dir),'merge-base','--is-ancestor',base,a.ref],check=True)
changes=git('diff','--name-only',base,a.ref).decode().splitlines()
if any(not f.startswith(DIR) for f in changes):raise RuntimeError('Historical path changed')
historical=doc('evidence/historical-git-blobs.json')['files_sha256']
for path,h in historical.items():
 if sha(blob(path))!=h:raise RuntimeError('Historical bytes drift '+path)
prior=json.loads(blob('DEVF/CP01_A2_FIRST_PILOT_SAFETY_AND_TRACE/evidence/historical-integrity.json'))
for path,h in prior['file_sha256'].items():
 if sha(blob(path))!=h:raise RuntimeError('Original277 drift '+path)
r=doc('evidence/windows-run-38435464736/result.json')
for path,h in r['source_ledger'].items():
 for ref in [a.ref,r['source_commit']]:
  if sha(blob(DIR+path,ref).replace(b'\r\n',b'\n'))!=h:raise RuntimeError('Compiled input drift '+path)
for run in [38434228398,38434647284,38435464736]:
 manifest=doc(f'evidence/windows-run-{run}/evidence-sha256.json')
 for path,v in manifest.items():
  b=blob(DIR+f'evidence/windows-run-{run}/'+path)
  if len(b)!=v['bytes'] or sha(b)!=v['sha256']:raise RuntimeError('CI text byte drift '+path)
d=doc('DOWNLOAD_MANIFEST.json');download=doc('evidence/download-verification.json')
if d!=download['manifest'] or d['source_commit']!=r['source_commit'] or d['workflow_commit']!=r['ci_head'] or d['execution_authorized'] or not d['creation_capable']:raise RuntimeError('Delivery provenance differs')
for k in ['dll_sha256','dll_bytes','package_sha256','package_bytes']:
 if d[k]!=r['package_verification'][k] or d[k]!=download[k]:raise RuntimeError('Delivery identity differs '+k)
refs=doc('evidence/historical-refs.json')['references']
for ref,h in refs.items():
 # Prior origin tracking refs are checked against the actual remote branches in this fetch.
 actual=ref.replace('refs/remotes/origin/','refs/heads/')
 if git('rev-parse',actual).decode().strip()!=h:raise RuntimeError('Historical reference drift '+ref)
subprocess.run(['git','--git-dir='+str(a.git_dir),'fsck','--full'],check=True,capture_output=True)
print(json.dumps({'status':'PASS_STATIC','ref':a.ref,'commit':git('rev-parse',a.ref+'^{commit}').decode().strip(),'historical_files':len(historical),'original277':len(prior['file_sha256']),'historical_refs':len(refs),'compiled_own_inputs':len(r['source_ledger']),'CI_text_manifests':3,'delivery_provenance':'PASS','git_fsck':'PASS','runtime':'NOT_TESTED'},indent=2))
