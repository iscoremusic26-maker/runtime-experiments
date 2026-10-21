#!/usr/bin/env python3
"""Read-only source inventory. Writes metadata only to an explicitly separate output directory."""
import argparse,collections,csv,hashlib,json,pathlib

PIN='40457c6adb381928e4b5fef6ed459ed291edd5e2'
def classify(path):
    p=path.lower(); name=pathlib.PurePosixPath(p).name
    if p.startswith('assets/'):
        return 'resource_identifier_headers','resources_archives_overlays','regional_resource_metadata'
    if p.startswith('extern/'):
        return 'external_dependency','external_dependencies','submodule'
    if p.startswith('sdk/'):
        return 'dusklight_sdk','hooking_abi' if 'hook' in name or name in ('api.h','meta.hpp','runtime.h') else 'sdk_services','sdk'
    if p.startswith('mods/'):
        return 'upstream_mod_example','runtime_and_lifecycle','example'
    if p.startswith('platforms/'):
        return 'platform_packaging','platform_backend','platform'
    if p.startswith(('tools/','ci/','.github/','cmake/')) or name.endswith(('.cmake','.nix','.patch')) or name in ('cmakelists.txt','cmakepresets.json','cmake-variants.yaml','flake.lock','ios.toolchain.cmake'):
        return 'build_or_research_tooling','build_tooling','tooling'
    if p.startswith(('docs/','.vscode/')) or name.endswith('.md'):
        return 'documentation_or_editor','documentation','documentation'
    if p.startswith('res/'):
        return 'port_presentation_resources','hud_ui_text','resource'
    if p.startswith('src/dusk/'):
        origin='dusklight_port'; category='port'
        if '/mods/loader/' in p or name in ('mod_loader.hpp','catalog.cpp','catalog.hpp','queue.cpp','queue.hpp','manifest.cpp','manifest.hpp'):system='runtime_and_lifecycle'
        elif '/mods/svc/' in p:system='hooking_abi' if 'hook' in name else 'sdk_services'
        elif any(k in name for k in ('save','autosave')):system='save_load'
        elif any(k in name for k in ('audio','sound')) or '/audio/' in p:system='audio_particles_effects'
        elif any(k in name for k in ('camera','gyro','mouse')):system='player_and_controls' if 'camera' not in name else 'cameras_rendering'
        elif any(k in name for k in ('archive','dvd','texture','io.')):system='resources_archives_overlays'
        elif '/ui/' in p or '/imgui/' in p or any(k in name for k in ('settings','language','layout','menu_pointer')):system='hud_ui_text'
        elif any(k in name for k in ('interp','presentation','gfx')) or '/interp/' in p:system='cameras_rendering'
        elif any(k in name for k in ('input','binding','combo','hotkey','gamepad')):system='player_and_controls'
        elif 'clock' in name:system='environment_weather_time'
        else:system='port_support'
        return origin,system,category
    if p.startswith('libs/'):
        origin='bundled_engine_library' if '/jsystem/' in p else 'bundled_platform_or_third_party'
        if any(k in p for k in ('/j3d','/jstage/')):system='models_animations_materials'
        elif any(k in p for k in ('/jaudio','/jparticle/','/freeverb/','/jaudio2/')):system='audio_particles_effects'
        elif any(k in p for k in ('/j2d','/jmessage/')):system='hud_ui_text'
        elif any(k in p for k in ('/jkernel/','/jsu')):system='memory_ownership'
        elif '/jstudio/' in p:system='cutscenes_dialogue'
        elif any(k in p for k in ('/jmath/','/jgeometry/')):system='movement_physics_collision'
        else:system='platform_backend'
        return origin,system,'library'
    if p.startswith(('src/','include/')):
        origin='game_source_with_port_adaptations'
        if '/f_pc/' in p or '/f_op/' in p or '/f_ap/' in p or '/m_re/' in p:system='runtime_and_lifecycle';category='scheduler'
        elif '/z2audio' in p:system='audio_particles_effects';category='audio'
        elif '/ssystem/' in p:system='movement_physics_collision';category='math_collision'
        elif '/m_do/' in p:
            system='audio_particles_effects' if 'audio' in name else 'resources_archives_overlays' if any(k in name for k in ('dvd','memcd')) else 'player_and_controls' if 'controller' in name else 'memory_ownership' if 'ext' in name else 'runtime_and_lifecycle';category='platform_bridge'
        elif '/d/actor/' in p:
            if name.startswith(('d_a_alink','d_a_player')):system='player_and_controls';category='player'
            elif name.startswith(('d_a_horse','d_a_canoe','d_a_fish','d_a_mg_','d_a_midna','d_a_boat')):system='other_systems';category='special_actor'
            else:system='actors_ai_npcs';category='enemy' if name.startswith('d_a_e_') else 'boss' if name.startswith('d_a_b_') else 'npc' if name.startswith('d_a_npc') else 'world_actor'
        elif '/d/' in p:
            category='game_system'
            rules=[(('d_save','d_file_sel','d_mem_card'),'save_load'),(('d_stage','d_room','d_s_play','d_s_menu','d_s_logo'),'stages_rooms_layers'),(('d_event',),'flags_events_progression'),(('d_msg','d_demo'),'cutscenes_dialogue'),(('d_bg','d_path','d_jnt_col'),'movement_physics_collision'),(('d_cc','d_att'),'combat_damage'),(('d_kankyo','d_kyeff','d_vrbox','d_k_wpillar'),'environment_weather_time'),(('d_camera','d_debug_camera','d_drawlist','d_jcam'),'cameras_rendering'),(('d_res',),'resources_archives_overlays'),(('d_item','d_shop','d_tresure'),'inventory_equipment'),(('d_particle','d_envse'),'audio_particles_effects'),(('d_meter','d_menu','d_pane','d_cursor','d_select','d_map','d_font','d_kantera'),'hud_ui_text')]
            system=next((v for prefixes,v in rules if name.startswith(prefixes)),'game_support')
        else:system='platform_backend';category='platform_compatibility'
        return origin,system,category
    return 'repository_metadata','build_tooling','metadata'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=pathlib.Path);ap.add_argument('output',type=pathlib.Path);a=ap.parse_args()
    source=a.source.resolve();out=a.output.resolve()
    if source==out or source in out.parents:raise SystemExit('Output must be outside the analyzed source tree')
    out.mkdir(parents=True,exist_ok=True)
    rows=[];directories=set()
    for f in sorted(source.rglob('*')):
        if not f.is_file():continue
        rel=f.relative_to(source).as_posix();data=f.read_bytes();origin,system,category=classify(rel)
        ext=f.suffix.lower();kind='source' if ext in ('.cpp','.c','.cc','.cxx','.m','.mm') else 'header' if ext in ('.h','.hpp','.inc') else 'resource' if ext in ('.png','.jpg','.ttf','.wav','.opus','.wgsl','.rml','.rcss') else 'other'
        rows.append((rel,kind,origin,system,category,len(data),hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()))
        for d in pathlib.PurePosixPath(rel).parents:
            if str(d)!='.':directories.add(d.as_posix())
    with (out/'FILE_INVENTORY.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(('path','kind','origin','system_id','category','bytes','local_blob_sha'));w.writerows(rows)
    def counts(pos):return dict(sorted(collections.Counter(r[pos] for r in rows).items()))
    summary={'source_commit':PIN,'files':len(rows),'directories':len(directories),'by_kind':counts(1),'by_origin':counts(2),'by_system':counts(3),'by_category':counts(4),'gitlinks_not_counted_as_files':['extern/aurora','extern/borealis','mods/cosmetics','mods/randomizer'],'limits':['Path classification is a navigation aid, not proof that implementations were understood.','Local blob hashes identify inspected bytes; crosscheck SOURCE_PIN.md before citing.']}
    (out/'INVENTORY_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    # Every directory containing files is represented; aggregate descendants are explicitly separate.
    direct=collections.Counter(str(pathlib.PurePosixPath(r[0]).parent) for r in rows)
    with (out/'DIRECTORY_INDEX.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(('directory','direct_files','descendant_files','primary_systems'))
        for d in sorted(directories|{'.'}):
            matches=[r for r in rows if d=='.' or r[0].startswith(d+'/')]
            w.writerow((d,direct[d],len(matches),','.join(s for s,n in collections.Counter(r[3] for r in matches).most_common(3))))
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
