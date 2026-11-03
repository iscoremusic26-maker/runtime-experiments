"""Only the two exact reviewed native transitions escape the mutator ban."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'ci'))
import pe_audit
checks=0
for symbol in pe_audit.CP04_NATIVE_TRANSITIONS:
 bad=symbol.split('@')[0][1:]
 for raw,want in [(symbol.encode()+b'\0',False),(symbol.replace('@daE_OC_c@','@daE_DB_c@').replace('@daAlink_c@','@daOther_c@').encode()+b'\0',True),(symbol.encode()+b'EXTRA\0',True),(symbol.encode()+b'\0?'+bad.encode()+b'@WrongClass@@QEAAXXZ\0',True)]:
  assert pe_audit.forbidden_decorated(raw,bad)==want,(bad,raw);checks+=1
for bad in ('setDamagePoint','procGuardSlipInit','commonProcInit','VirtualProtect','WriteProcessMemory'):
 assert pe_audit.forbidden_decorated(b'?'+bad.encode()+b'@Wrong@@\0',bad);checks+=1
print(json.dumps({'status':'PE_NAME_POLICY_PASS','checks':checks,'authorized_exact_transitions':sorted(pe_audit.CP04_NATIVE_TRANSITIONS),'native_runtime':False},indent=2))
