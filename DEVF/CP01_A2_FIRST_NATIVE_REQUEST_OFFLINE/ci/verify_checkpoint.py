"""Read-only verification of independently fetched own Git blobs; no builds or game inputs."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--git-dir',required=True);p.add_argument('--ref',required=True);a=p.parse_args()
prefix='DEVF/CP01_A2_FIRST_NATIVE_REQUEST_OFFLINE/'
def blob(name):return subprocess.check_output(['git','--git-dir='+a.git_dir,'show',a.ref+':'+name])
def load(name):return json.loads(blob(prefix+name))
def sha(b):return hashlib.sha256(b).hexdigest()
r=load('evidence/windows-run-38414957463/result.json');counts={}
for label,ledger,path,lf in [
 ('compiled_own_source',r['source_ledger'],prefix,True),
 ('reused_source',r['reused_source_ledger'],'DEVF/',True),
 ('historical',load('evidence/historical-unchanged.json')['file_sha256'],'DEVF/',False)]:
 for name,h in ledger.items():
  b=blob(path+name)
  if lf:b=b.replace(b'\r\n',b'\n')
  if sha(b)!=h:raise RuntimeError('Hash mismatch: '+path+name)
 counts[label]=len(ledger)
manifest=load('evidence/windows-run-38414957463/evidence-sha256.json')
for name,d in manifest.items():
 if Path(name).name!=name or Path(name).suffix not in ['.json','.log']:raise RuntimeError('Unreviewed evidence path')
 b=blob(prefix+'evidence/windows-run-38414957463/'+name)
 if len(b)!=d['bytes'] or sha(b)!=d['sha256']:raise RuntimeError('Evidence mismatch: '+name)
counts['evidence']=len(manifest)
subprocess.run(['git','--git-dir='+a.git_dir,'fsck','--full'],check=True,capture_output=True)
print(json.dumps({'status':'PASS_STATIC','ref':a.ref,'verified':counts,'fsck':'PASS','game_run':False},indent=2))
