"""Incremental Python-only inspection fixtures; never execute our own downloaded DLL."""
import io,json,stat,zipfile
from pathlib import Path
from audit import safe_members,sha,verify_package
from verify_download import verify

def run(delivery,text,project,work):
 with zipfile.ZipFile(delivery) as z:files={n:z.read(n) for n in z.namelist()}
 original=json.loads(files['DOWNLOAD_MANIFEST.json']);name=original['filename'];results=[]
 def rejected(name,action):
  try:action()
  except (RuntimeError,zipfile.BadZipFile):results.append({'case':name,'rejected':True,'execution':'OFFLINE_PYTHON_INSPECTION_ONLY','dll_loaded':False})
  else:raise RuntimeError('Surviving download/package fixture '+name)
 for case in ['external-manifest-changed','external-source-changed','wrong-artifact-digest']:
  changed=dict(files)
  if case!='wrong-artifact-digest':
   meta=json.loads(changed['DOWNLOAD_MANIFEST.json']);key='dll_sha256' if case=='external-manifest-changed' else 'source_commit';meta[key]='0'*len(meta[key]);changed['DOWNLOAD_MANIFEST.json']=json.dumps(meta).encode()
  f=work/(case+'.zip')
  with zipfile.ZipFile(f,'w') as z:
   for k,v in changed.items():z.writestr(k,v)
  digest='0'*64 if case=='wrong-artifact-digest' else sha(f.read_bytes())
  rejected(case,lambda:verify(f,text,project,work/('inspection-'+case),digest,sha(text.read_bytes())))
 own=work/'original.dusk';own.write_bytes(files[name])
 with zipfile.ZipFile(own) as z:inner={n:z.read(n) for n in z.namelist()}
 dll=work/'own.dll';dll.write_bytes(inner['lib/windows-amd64/mod.dll'])
 for case in ['manifest-id-changed','internal-DLL-changed']:
  altered=dict(inner)
  if case=='manifest-id-changed':
   meta=json.loads(altered['mod.json']);meta['id']='dev.other';altered['mod.json']=json.dumps(meta).encode()
  else:altered['lib/windows-amd64/mod.dll']=altered['lib/windows-amd64/mod.dll'][:-1]+b'X'
  f=work/(case+'.dusk')
  with zipfile.ZipFile(f,'w') as z:
   for k,v in altered.items():z.writestr(k,v)
  rejected(case,lambda:verify_package(f,dll,project,work))
 for case in ['directory-marked-regular','file-marked-directory']:
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w') as z:
   for k,v in inner.items():
    info=zipfile.ZipInfo(k);info.external_attr=((stat.S_IFDIR if k.endswith('/') else stat.S_IFREG)|0o755)<<16
    if case=='directory-marked-regular' and k=='lib/':info.external_attr=(stat.S_IFREG|0o644)<<16
    if case=='file-marked-directory' and k=='mod.json':info.external_attr=(stat.S_IFDIR|0o755)<<16
    z.writestr(info,v)
  with zipfile.ZipFile(io.BytesIO(stream.getvalue())) as z:rejected(case,lambda:safe_members(z))
 return results

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--delivery',type=Path,required=True);p.add_argument('--text',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
 result=run(a.delivery,a.text,Path(__file__).resolve().parents[1],a.work);a.output.write_text(json.dumps(result,indent=2)+'\n');print(len(result),'download/package negatives PASS; DLL/game NOT_EXECUTED')
