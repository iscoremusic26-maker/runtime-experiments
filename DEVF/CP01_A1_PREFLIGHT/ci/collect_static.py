"""Extract only E_OC authored placements/FILI from the preserved decoded location cache.
Never decompress ARC/KCL or publish resource bytes. Reuses prior integrity/geometry analysis.
"""
import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--cache',type=Path,required=True); p.add_argument('--source',type=Path,required=True)
p.add_argument('--output',type=Path,required=True); a=p.parse_args()
root = '40457c6adb381928e4b5fef6ed459ed291edd5e2'
if subprocess.check_output(['git','-C',str(a.source),'rev-parse','HEAD'],text=True).strip() != root:
    raise SystemExit('Wrong official source')
inventory = a.cache/'inventory.json'; raw=inventory.read_bytes(); data=json.loads(raw)
room = next(f for f in data['archives']['R03_00.arc']['files'] if f['path']=='dzr/room.dzr')
records = []
for chunk in room['chunks']:
    if chunk['tag'] != 'ACT6': continue
    for r in chunk['records']:
        if r['name'] == 'E_oc': records.append({'chunk':'ACT6',**r})
if len(records)!=7: raise SystemExit('Preserved baseline no longer contains seven E_oc records')
dzr = (a.cache/'R03_00.arc/dzr/room.dzr').read_bytes()
if hashlib.sha256(dzr).hexdigest()!=room['sha256']: raise SystemExit('Decoded room bytes differ from verified cache')
fili=next(c for c in room['chunks'] if c['tag']=='FILI')
if fili['count']!=1: raise SystemExit('Unexpected FILI count')
n=fili['offset']; parameters=struct.unpack_from('>I',dzr,n)[0]; sw=dzr[n+0x1b]
selected=next(r for r in records if r['index']==11)
x=selected['angle'][0]&65535; params=int(selected['parameters'],16)
references={
 'src/d/actor/d_a_e_oc.cpp':[98,350,787,1868,2333,2397,2420,2542,2563,2650,2670,2704,2733,2741,2811,2848],
 'src/d/d_stage.cpp':[975], 'include/f_pc/f_pc_name.h':[524],
 'src/f_op/f_op_actor.cpp':[519], 'include/d/d_stage.h':[1215,1547],
 'src/f_pc/f_pc_layer.cpp':[91,105,137], 'src/f_pc/f_pc_executor.cpp':[55,68],
 'src/f_op/f_op_actor_iter.cpp':[28], 'src/SSystem/SComponent/c_tag_iter.cpp':[13],
 'src/d/d_com_inf_game.cpp':[890], 'src/dusk/mods/loader/loader.cpp':[1237],
 'sdk/include/mods/svc/host.h':[34], 'sdk/include/mods/svc/log.h':[28],
 'sdk/include/mods/svc/game.h':[17], 'sdk/src/game_feature.cpp':[5],
 'cmake/GameABIConfig.cmake':[36], 'cmake/ModSDK.cmake':[201],
}
source_refs=[]
for path,lines in references.items():
    content=(a.source/path).read_bytes()
    source_refs.append({'path':path,'lf_sha256':hashlib.sha256(content.replace(b'\r\n',b'\n')).hexdigest(),'anchor_lines':lines})
result={'official_root':root,'analysis_scope':'incremental E_OC/FILI only; prior ARC/KCL/WRock/Digpl evidence reused',
 'preserved_inventory_sha256':hashlib.sha256(raw).hexdigest(),'room_dzr_sha256':room['sha256'],
 'stage':'F_SP121','room':3,'logical_layer':6,'authored_records':records,
 'fili':{'parameters':hex(parameters),'enemy_appear1':bool(parameters&0x20000000),'bit_sw':sw,
         'appearance_switch_gate_disabled_statically':sw==255},
 'conditional_preset':{'canonical_name':'E_oc','profile':'fpcNm_E_OC_e','profile_id':'0x1fe','argument':-1,
    'authored_preset_index':11,
    'parameters':hex(params),'angle_x_s16':selected['angle'][0],'angle_x_u16':hex(x),
    'yaw_s16':0,'angle_z_s16':0,'scale':'ACTR implicit (1,1,1); native HIO basic_size 1.5',
    'native_mode':0 if params&255==255 else params&255,
    'defeated_switch':(params>>16)&255,'secondary_switch':(params>>24)&255,
    'model_archive':'E_OC' if (x>>8) in (0,255) else 'E_OC2',
    'animation_archive':'E_ocb','move_range':100*(0 if x&255==255 else x&255),
    'placement':'NOT_VERIFIED; authored coordinates occupied by vanilla actors, not available spawn slots'},
 'source_references':source_refs}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS_STATIC: seven authored E_oc placements and targeted FILI; no runtime or new-position claim')
