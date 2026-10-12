"""Compare received integration metadata to the established baseline, without rerunning it."""
import argparse,collections,hashlib,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--integration',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
b=json.loads((a.baseline/'baseline-result.json').read_text());n=json.loads((a.integration/'integration-result.json').read_text())
def archives(x):return {(v['root'],v['path'].replace('\\','/')):(v['sha256'],v['bytes'])for v in x['archives']}
def repos(x):return {v['path'].replace('\\','/'):(v['commit'],v['recursive_gitlinks'].replace('\\','/'))for v in x['fetched_git_dependencies']}
def diff(old,new):return {'added':sorted(set(new)-set(old)),'removed':sorted(set(old)-set(new)),'changed':sorted(k for k in set(old)&set(new)if old[k]!=new[k])}
dep={'archives_and_embedded_fixtures':diff(archives(b),archives(n)),'git_and_recursive_gitlinks':diff(repos(b),repos(n)),'vcpkg_versions_equal':json.loads(b['vcpkg_installed'])==json.loads(n['vcpkg_installed'])}
# Preserve warnings by code/message; ignore runner absolute directories and shifted line positions.
def warnings(folder):
 text=(folder/'build.log').read_text(errors='replace');matches=re.findall(r'\bwarning ((?:C|LNK)\d+):\s*(.*)',text)
 return collections.Counter((code,re.sub(r'[\r\n]+','',message).strip())for code,message in matches)
bw=warnings(a.baseline);nw=warnings(a.integration)
changes=[{'code':k[0],'message':k[1],'baseline_occurrences':bw[k],'integration_occurrences':nw[k]}for k in sorted(set(bw)|set(nw))if bw[k]!=nw[k]]
new_kinds=[{'code':k[0],'message':k[1],'occurrences':nw[k]}for k in sorted(set(nw)-set(bw))]
errors=re.findall(r'\b(?:fatal )?error (?:C|LNK)\d+:.*',(a.integration/'build.log').read_text(errors='replace'))
result={'baseline_run':38256856294,'integration_run':38265011287,'baseline_status':b['status'],'integration_status':n['status'],'dependencies':dep,'dependency_comparison_status':'PASS'if not any(v['added']or v['removed']or v['changed']for k,v in dep.items()if isinstance(v,dict))and dep['vcpkg_versions_equal']else 'BLOCKED','warnings':{'baseline_occurrences':sum(bw.values()),'integration_occurrences':sum(nw.values()),'new_code_message_pairs':new_kinds,'occurrence_changes':changes,'scope':'host build.log only; diagnostic driver and Actions infrastructure warnings excluded; not a source-location correspondence proof'},'compiler_linker_errors':errors,'game_runtime':'NOT_TESTED'}
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'dependency_status':result['dependency_comparison_status'],'new_warning_kinds':len(new_kinds),'compiler_linker_errors':len(errors)}))
