"""Focused official-source provenance. Never copies upstream sources or game assets."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = "40457c6adb381928e4b5fef6ed459ed291edd5e2"
AURORA = "3227d76c60e1e782ca576610bce61c9e7744d8be"
REFERENCES = {
    "sdk/include/mods/svc/actor.h": r"ACTOR_SERVICE_MAJOR|create_function|create_actor_from_name|delete_actor",
    "src/dusk/mods/svc/actor.cpp": r"finish_delete_all|ModResult create_actor|copy.argument|actor_remove_mod|forceDelete|modDeactivating",
    "sdk/include/mods/svc/stage.h": r"STAGE_SERVICE_MAJOR|add_actor|removed|out_handle",
    "src/dusk/mods/svc/stage.cpp": r"kActrEntrySize|kTgscEntrySize|stage_create_new_actors|record.mod->active|stage_add_actor|stage_remove_actor_edit|stage_remove_mod|record =|modDetached",
    "src/d/d_stage.cpp": r'OBJNAME\("E_SB"|OBJNAME\("E_rd"|dStage_actorCreate|dusk_stage_svc_new_actor_create|dStage_dt_c_roomReLoader|fopAcM_Create\(actorInf|object.scale|object.base|objectNameInf|dStage_searchName',
    "include/d/d_stage.h": r"class stage_actor_data|class stage_tgsc_data|sizeof\(stage_|mStatus\[",
    "include/f_pc/f_pc_name.h": r"fpcNm_E_SB_e|fpcNm_E_RD_e",
    "include/f_op/f_op_actor_mng.h": r"BE\(u32\) parameters|BE\(cXyz\)|BE\(csXyz\)|BE\(u16\) setID|fopAcM_prmScale|SearchByID|SetSpeed|GetScale|GetModel",
    "src/f_op/f_op_actor_mng.cpp": r"fopAcM_CreateAppend|createAppend\(|fopAcM_createDisappear|fopAcM_createItemFromEnemyID|fopAcM_createItemFromTable|append->scale|append->argument",
    "include/f_op/f_op_actor.h": r"cXyz scale|cXyz speed|J3DModel\* model|f32 speedF|s16 health",
    "include/SSystem/SComponent/c_cc_d.h": r"SetAtp|GetAtAtp|SetAtAtp|SetAtType",
    "include/d/d_cc_d.h": r"SetAtHitCallback|SetTgShieldFrontRangeYAngle|OnTgShield|OffTgShield|SetAtMtrl|SetAtSpl",
    "include/d/d_cc_uty.h": r"mAttackPower|cc_at_check|at_power_check",
    "include/d/actor/d_a_e_rd.h": r"public:|action|mode|timer|at_info|dCcD_Sph|dCcD_Cyl",
    "src/f_op/f_op_actor.cpp": r"fopAc_Create\(|ToActorQ|sub_method =|actor->scale.set|dStage_FileList_dt_GetEnemyAppear|fpcMtd_Create",
    "src/d/actor/d_a_e_sb.cpp": r"daE_SB_c::Create|daE_SB_c::Delete|daE_SB_c::setBaseMtx|l_HIO|field_0x61a|dComIfG_resLoad|health|field_0x5e6|createDisappear|g_profile_E_SB",
    "include/d/actor/d_a_e_sb.h": r"field_0x61a|field_0x5e6",
    "src/d/actor/d_a_e_rd.cpp": r"static daE_RD_HIO|l_HIO.model_size|i_this->scale.x|health =|health <=|scene_no =|weapon_type =|swBit =|int daE_RD_Create|dComIfG_resLoad|0xFF|coachGameActorSet",
    "src/d/actor/d_a_disappear.cpp": r"daDisappear_Create|createItemFromEnemyID|enemy_id|particle_set",
    "sdk/include/mods/svc/game.h": r"FEATURES|ABI|GAME_SERVICE_MAJOR",
    "cmake/GameABIConfig.cmake": r"_game_compile_defs|Public game|dusklight_mod_feature_game|game_feature|global.h",
    "cmake/ModSDK.cmake": r"_needs_host_link|_feature STREQUAL|Game.*import|_package_target",
    "sdk/include/mods/svc/resource.h": r"RESOURCE_SERVICE_MAJOR|RESOURCE_SERVICE_MINOR|Read-only|reclaimed|data_dir|load\)|free\)",
    "src/dusk/mods/svc/resource.cpp": r"s_buffers|resource_remove_mod|resource_free|modDetached",
    "sdk/include/mods/svc/host.h": r"HOST_SERVICE_MAJOR|HOST_SERVICE_MINOR|data_dir|mod_dir|fail|Lifecycle|Detached|DETACHED",
    "sdk/include/mods/svc/file.h": r"FILE_SERVICE_MAJOR|callback|thread|ModResult|read|write",
    "src/dusk/mods/svc/file.cpp": r"file_remove_mod|s_pendingPick->owner|s_pendingPick->callback|modDetached",
    "src/dusk/mods/loader/loader.cpp": r"ModLoader::deactivate_mod|modules_mod_deactivating|fn_shutdown|modules_mod_detached|unload_native|mod.active = false",
    "src/dusk/mods/loader/natives.cpp": r"Deferred dlclose|unload_native|drain_retired_natives|retired.native.reset",
    "sdk/include/mods/svc/texture.h": r"TEXTURE_SERVICE_MAJOR|TEXTURE_KEY_POINTER|TEXTURE_KEY_SOURCE|copied|Actor|register_|unregister",
    "libs/JSystem/include/JSystem/J3DGraphAnimator/J3DModel.h": r"getModelData|mModelData|mMatPacket",
    "libs/JSystem/src/J3DGraphAnimator/J3DModel.cpp": r"mModelData = pModelData|setMaterial\(materialNode\)|getMaterialNodePointer|getMaterialAnm|newDisplayList",
    "sdk/include/mods/svc/gfx.h": r"GFX_SERVICE_MAJOR|GFX_SERVICE_MINOR|callback|borrowed|thread|register|unregister",
    "src/dusk/mods/svc/gfx.cpp": r"gfx_mod_deactivating|take_mod_types_locked|unregister_aurora_types|synchronize|modDeactivating",
    "sdk/include/mods/svc/item.h": r"ITEM_SERVICE_MAJOR|ITEM_SERVICE_MINOR|giver_actor|set_check_resolver|set_check_override|give_item|observe_gives|FIFO",
    "sdk/include/mods/svc/ui.h": r"UI_SERVICE_MAJOR|UI_SERVICE_MINOR|thread|unregister|register|callback",
    "src/dusk/mods/svc/ui.cpp": r"ui_remove_mod|modDetached|invalidates every callback",
}

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

def verify(root):
    head = git(root, "rev-parse", "HEAD")
    if head != ROOT:
        raise SystemExit(f"Wrong official root: {head}")
    # Tracked-tree equality only. Build outputs must stay outside the source tree.
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise SystemExit("Official tracked sources changed")
    if git(root, "rev-parse", "HEAD:extern/aurora") != AURORA:
        raise SystemExit("Wrong aurora gitlink")
    if git(root / "extern/aurora", "rev-parse", "HEAD") != AURORA:
        raise SystemExit("Wrong aurora checkout")
    if git(root / "extern/aurora", "status", "--porcelain", "--untracked-files=no"):
        raise SystemExit("Aurora tracked sources changed")
    entries = []
    for relative, pattern in REFERENCES.items():
        path = root / relative
        data = path.read_bytes()
        entries.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(),
                        "bytes": len(data), "upstream_url": f"https://github.com/TwilitRealm/dusklight/blob/{ROOT}/{relative}",
                        "anchor_lines": [i for i, line in enumerate(data.decode("utf-8").splitlines(), 1)
                                         if re.search(pattern, line)]})
    return {"official_root": head, "aurora": AURORA, "tracked_source_clean": True,
            "scope": "focused architecture source references; no ARC/location/dependency reinvestigation",
            "references": entries}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.source.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"PASS exact official root, aurora and {len(result['references'])} source references; tracked trees clean")
