"""Read-only own Git-blob evidence recovery; does not compile, load a DLL or read game inputs."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--git-dir',required=True);p.add_argument('--ref',required=True);a=p.parse_args()
prefix='DEVF/CP01_A2_FIRST_PILOT_SAFETY_AND_TRACE/'
def blob(n):return subprocess.check_output(['git','--git-dir='+a.git_dir,'show',a.ref+':'+n])
def load(n):return json.loads(blob(prefix+n))
def sha(b):return hashlib.sha256(b).hexdigest()
r=load('evidence/windows-run-38425038752/result.json');counts={}
for label,ledger,base,lf in [('own',r['source_ledger'],prefix,True),('reused',r['reused_source_ledger'],'DEVF/',True),('historical',load('evidence/historical-integrity.json')['file_sha256'],'',False)]:
 for n,h in ledger.items():
  b=blob(base+n)
  if lf:b=b.replace(b'\r\n',b'\n')
  if sha(b)!=h:raise RuntimeError('Hash mismatch: '+base+n)
 counts[label]=len(ledger)
manifest=load('evidence/windows-run-38425038752/evidence-sha256.json')
for n,d in manifest.items():
 if Path(n).name!=n or Path(n).suffix not in ['.json','.log']:raise RuntimeError('Unreviewed path')
 b=blob(prefix+'evidence/windows-run-38425038752/'+n)
 if len(b)!=d['bytes'] or sha(b)!=d['sha256']:raise RuntimeError('Evidence mismatch: '+n)
counts['final_evidence']=len(manifest)
subprocess.run(['git','--git-dir='+a.git_dir,'fsck','--full'],capture_output=True,check=True)
print(json.dumps({'status':'PASS_STATIC','ref':a.ref,'verified':counts,'fsck':'PASS','runtime':'NOT_TESTED'},indent=2))
