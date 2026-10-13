#!/usr/bin/env python3
"""Read-only G4 delta: overlay records, RTBL/SCLS and cached candidate screening.

No ARC/BCK/BMD/KCL decode, game/native calls, raw log or capture publication.
Private saved numerical captures are used only for new distances to OLD points.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess

HERE = Path(__file__).resolve().parents[1]
BASE = "dc2f65ab5d1423ce74d78661dbbea5e14a692409"
HOST = "40457c6adb381928e4b5fef6ed459ed291edd5e2"
LOG_HASH = "d19f2760e695f48f4df59706b791de121ffe77806bdafde8a7539b2cdc2b78b4"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(data, offset, fmt):
    length = struct.calcsize(">" + fmt)
    assert 0 <= offset <= len(data) - length
    return struct.unpack_from(">" + fmt, data, offset)


def chunk_index(data):
    count = read(data, 0, "I")[0]
    assert 0 < count < 1000
    chunks = [(read(data, 4+i*12, "4s")[0].decode("ascii"), *read(data, 8+i*12, "II")) for i in range(count)]
    result = {}
    for tag, size, offset in chunks:
        assert offset >= 4 + 12*count and offset <= len(data) and tag not in result
        end = min([o for _,_,o in chunks if o > offset] + [len(data)])
        result[tag] = (size, offset, end)
    return result


def scls(data, chunk):
    count, offset, end = chunk
    assert offset + count * 13 <= end  # exact stage_scls_info_class, not old12
    result = []
    for index in range(count):
        stage, point, room, a, b, wipe = read(data, offset+index*13, "8sBbBBB")
        stage = stage.split(b"\0",1)[0].decode("ascii")
        assert re.fullmatch(r"[A-Z]_[A-Z0-9]{4,6}",stage)
        layer = b & 15
        result.append({"index":index,"destination_stage":stage,"point":point,"room":room,
                       "layer":-1 if layer==15 else layer,"wipe":wipe,"time_h":((a>>4)&15)|(b&16)})
    return result


def rtbl(data, chunk):
    count, offset, end = chunk
    assert offset + count*4 <= end
    result = []
    for room in range(count):
        p = read(data,offset+room*4,"I")[0]
        size, _, _, _, entries = read(data,p,"BBBBI")
        assert entries+size <= len(data)
        values = list(data[entries:entries+size])
        result.append({"room":room,"loaded_rooms":[v&63 for v in values],"bg_flags":[bool(v&128) for v in values]})
    return result


def summarize_log(data):
    assert sha(data)==LOG_HASH
    lines = data.decode("utf-8").splitlines()
    matches = []
    module_lines = []
    for number,line in enumerate(lines,1):
        if "dusk::mods::overlay]" in line:
            module_lines.append(number)
        m = re.match(r"^\[DEBUG\s*\| dusk::mods::overlay\] Registering (\d+) overlay file\(s\)\.$",line)
        if m:
            matches.append({"line":number,"count":int(m[1])})
    assert matches==[{"line":70,"count":0}]
    assert module_lines==[70]
    return {"primary_log_sha256":LOG_HASH,"lines":len(lines),"overlay_sync_records":matches,
            "other_overlay_module_records":[],"capture_interval_reused":[1846,1897],
            "later_applied_service_overlays":"PASS_RUNTIME_LOG: no later sync recorded through end of complete provided log",
            "dynamic_unapplied_slots":"NOT_VERIFIED; pending registrations would not yet be effective",
            "arc_filename_load_records_count":sum(bool(re.search(r"E_ocb?\.arc",l,re.I)) for l in lines),
            "byte_identity_in_runtime":"NOT_VERIFIED; no per-resource load hash"}


def screen(pool, points, position_key, slope_key):
    ranked=[]
    for item in pool:
        p=item[position_key]
        dxz=min(math.hypot(q[0]-p[0],q[2]-p[2]) for q in points)
        d3=min(math.dist(q,p) for q in points)
        ranked.append((d3,dxz,item))
    d3,dxz,item=max(ranked,key=lambda row:row[0])
    return {"existing_points":len(pool),"best_min_recorded_Link_3d":d3,"best_min_recorded_Link_xz":dxz,
            "screen_point_not_candidate":item[position_key],"prior_slope_WRock":item[slope_key],
            "all_have_a_recorded_Link_position_within_default_search_S":all(row[0]<1200 for row in ranked),
            "limits":"Past Link points only; not future route/LOS/detection or E_OC ground guarantee; cached WRock points not promoted"}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--private-log",type=Path,required=True)
    ap.add_argument("--private-captures",type=Path,required=True)
    ap.add_argument("--location-cache",type=Path,required=True)
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--output-dir",type=Path,required=True)
    args=ap.parse_args()
    root=subprocess.check_output(["git","rev-parse","HEAD"],cwd=args.source,text=True).strip()
    assert root==HOST
    subprocess.run(["git","diff","--quiet","HEAD"],cwd=args.source,check=True)
    overlays=summarize_log(args.private_log.read_bytes())
    inventory=json.loads((args.location_cache/"inventory.json").read_text())
    context={}
    for arc in ["STG_00.arc","R03_00.arc"]:
        file=next(f for f in inventory["archives"][arc]["files"] if f["path"].endswith((".dzs",".dzr")))
        data=(args.location_cache/arc/file["path"]).read_bytes()
        assert sha(data)==file["sha256"]  # small targeted file, no ARC integrity repeat
        chunks=chunk_index(data)
        context[arc]={"data_sha256":file["sha256"],"scls_stride":13,"scls":scls(data,chunks["SCLS"])}
        if "RTBL" in chunks:
            table=rtbl(data,chunks["RTBL"])
            context[arc]["rtbl"]=table
            context[arc]["rooms_retaining_room3"]=[r["room"] for r in table if 3 in r["loaded_rooms"]]
        if "PLYR" in chunks:
            previous=next(c for c in file["chunks"] if c["tag"]=="PLYR")
            context[arc]["player_entry_ids_reused"]=[r["angle"][2]&255 for r in previous["records"]]
            context[arc]["scene_exit_actors_reused"]=[{"chunk":c["tag"],"index":r["index"],"exit_id":int(r["parameters"],16)&255,
                "switch":int(r["parameters"],16)>>24,"arg1":(int(r["parameters"],16)>>8)&255,
                "event_on_label":r["angle"][0]&4095,"event_off_label":r["angle"][2]&4095}
                for c in file["chunks"] if c["tag"] in ("ACTR","SCOB","ACT6","SCO6") for r in c["records"] if r["name"]=="scnChg"]
    captures=json.loads(args.private_captures.read_text())
    assert len(captures)==28
    points=[[float(v) for v in c["fields"]["link"].strip("()").split(",")] for c in captures]
    broad=json.loads((args.location_cache/"geometry.json").read_text())["evaluations"]
    refined=json.loads((args.location_cache/"refined-candidates.json").read_text())
    screening={"purpose":"New comparisons to existing cached points; no new geometry/search grid or original G2 census analysis",
               "broad16":screen(broad,points,"position","max_slope_degrees"),
               "refined98":screen(refined,points,"position","max_slope_degrees")}
    sources=["src/dusk/mods/svc/overlay.cpp","src/dusk/mods/svc/registry.cpp","src/dusk/mods/loader/loader.cpp",
             "extern/aurora/lib/dolphin/dvd/fst.cpp","libs/JSystem/src/JKernel/JKRArchivePri.cpp","src/dusk/texture_replacements.cpp",
             "src/d/actor/d_a_e_oc.cpp","src/SSystem/SComponent/c_math.cpp","src/SSystem/SStandard/s_basic.cpp",
             "src/f_pc/f_pc_base.cpp","src/f_op/f_op_actor_mng.cpp","src/d/d_bg_s_gnd_chk.cpp",
             "src/d/d_com_inf_game.cpp","src/d/d_stage.cpp","src/d/d_s_room.cpp","include/d/d_stage.h",
             "src/d/actor/d_a_scene_exit.cpp","include/d/actor/d_a_scene_exit.h"]
    prior=HERE.parent/"CP01_G4_EOC_RESOURCE_CONTINUATION/evidence"
    result={"base":BASE,"host":HOST,"overlay_log_review":overlays,"stage_context_delta":context,"cached_sector_screening":screening,
            "movement_delta":{"initial_mode0":"WAIT from zeroed actor memory; Create calls Execute; prior checks can immediately switch state",
                              "first_wait_min_timer":10,"first_walk_timer_upper":200,"walk_speed_target":4,
                              "first_walk_voluntary_xz_distance_upper_ideal_conditional":800,
                              "bound_conditions":"Single first WALK episode only; no detections/sound/ally/damage/event/water/fall; ideal trig; no extra CCMove or horizontal Acch corrections",
                              "full_origin_displacement_domain":"NOT_VERIFIED; voluntary bound does not cover excluded effects, repetition or pursuit",
                              "safe_observation_domain":"NOT_VERIFIED; no static candidate admitted"},
            "source_sha256":{p:sha((args.source/p).read_bytes()) for p in sources},
            "reused_evidence_sha256":{n:sha((prior/n).read_bytes()) for n in ["resources-envelope.json","position-query.json","offline-validation.json"]},
            "position":"NO_SAFE_POSITION_VERIFIED","g4":"G4_RESOURCE_VERIFIED_POSITION_BLOCKED","policy":"DISARMED_NO_REGISTRATION","g5":"NO-GO","cp02":"NO-GO"}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"focused-review.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS_OFFLINE: targeted overlay log, RTBL/SCLS13, old sector screening; no ARC/BCK/KCL reprocessing")
    print(json.dumps({"overlay_sync":overlays["overlay_sync_records"],"room3_retained_by":context["STG_00.arc"]["rooms_retaining_room3"],"best_3d_cached16":screening["broad16"]["best_min_recorded_Link_3d"],"best_3d_cached98":screening["refined98"]["best_min_recorded_Link_3d"]},indent=2))


if __name__=="__main__":
    main()
