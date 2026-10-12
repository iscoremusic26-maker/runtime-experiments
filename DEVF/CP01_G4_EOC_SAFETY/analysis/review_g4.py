#!/usr/bin/env python3
"""Read private G2 evidence; emit aggregates only, never log lines or resources.

Uses existing CP01 evidence for ARC/KCL/PLC/Digpl. Does not decode those again,
load a native library, run a game, write inputs, or extract game resources.
Python standard library only. Fixed identity checks fail closed on other input.
"""
import argparse
import collections
import hashlib
import io
import json
import math
from pathlib import Path
import re
import subprocess
import zipfile

LOG_HASH = "d19f2760e695f48f4df59706b791de121ffe77806bdafde8a7539b2cdc2b78b4"
HOST = "40457c6adb381928e4b5fef6ed459ed291edd5e2"
REFERENCE = [-4806.7346, -6729.480961460304, 65135.8281]
EXPECTED = {158: 296, 159: 296, 160: 296, 161: -216, 162: -236, 163: 296, 172: 281}
CONTEXT = dict(stage="F_SP121", room="3", logical="6", current="0", link_owner="5",
               room_node="102", room_owner="5", room_child_layer="6", room_creates="0",
               room_deletes="0", E_OC_registered="1", E_ocb_registered="1",
               loaded="NOT_VERIFIED", renderer="NOT_VERIFIED", census="7", truncated="0")
ACTOR = re.compile(r"E_OC id=(\d+) rm=(-?\d+) owner=(\d+) p=([0-9a-f]+) hx=(-?\d+) xyz=\(([^)]+)\)")
ARC_NAME = re.compile(r"(?:^|/)e_ocb?\.arc$", re.IGNORECASE)


def require(value, message):
    if not value:
        raise ValueError(message)  # messages contain no private input text


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xyz(value):
    result = [float(v) for v in value.strip("()").split(",")]
    require(len(result) == 3 and all(math.isfinite(v) for v in result), "Invalid XYZ")
    return result


def distance(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--log", required=True, type=Path)
    ap.add_argument("--inputs", required=True, type=Path)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    require(args.output.resolve() != args.log.resolve(), "Output must differ from input")
    blob = args.log.read_bytes()
    require(hashlib.sha256(blob).hexdigest() == LOG_HASH, "Anonymized log SHA256 mismatch")
    require(len(blob) == 183907, "Anonymized log size mismatch")
    lines = blob.decode("utf-8").splitlines()
    require(len(lines) == 2182, "Anonymized log line count mismatch")
    captures = []
    levels = collections.Counter()
    warnings = []
    creates = collections.defaultdict(list)
    for number, line in enumerate(lines, 1):
        level = re.match(r"^\[(\w+)\s*\|", line)
        if level:
            levels[level[1]] += 1
            if level[1] == "WARNING":
                warnings.append(line)
        create = re.search(r"fpcBs_Create: pid=(\d+) profname=fpcNm_(E_OC|ROOM_SCENE)_e", line)
        if create:
            creates[create[2]].append({"id": int(create[1]), "line": number})
        if "DISARMED stage=" not in line:
            continue
        fields = dict(re.findall(r"(\w+)=(\([^)]*\)|[^ |]+)", line.split(" | E_OC", 1)[0]))
        require(all(fields.get(k) == v for k, v in CONTEXT.items()), "Capture context mismatch")
        records = {}
        for match in ACTOR.finditer(line):
            actor_id, room, owner, param, home_x, position = match.groups()
            actor_id = int(actor_id)
            require(actor_id not in records, "Duplicate actor in a capture")
            require(actor_id in EXPECTED and int(home_x) == EXPECTED[actor_id], "Preset mismatch")
            require(int(room) == 3 and int(owner) == 6 and param == "ffffffff", "Actor context mismatch")
            records[actor_id] = xyz(position)
        require(set(records) == set(EXPECTED), "Incomplete actor census")
        captures.append({"line": number, "link": xyz(fields["link"]), "actors": records})
    require(len(captures) == 28, "Expected all 28 captures")
    require(dict(levels) == {"INFO": 89, "DEBUG": 1990, "WARNING": 83}, "Severity totals mismatch")
    require(all("dds" in w.lower() and "mip" in w.lower() for w in warnings), "Unexpected warning category")
    require(HOST in lines[1], "Official host revision missing")
    require("DISARMED_NO_REGISTRATION" in lines[65], "Observer guard missing")
    require("D3D12" in lines[13] and "D3D12" in lines[17], "D3D12 markers missing")
    require("shutdown" in lines[2180] and "all mods unloaded" in lines[2181], "Shutdown markers missing")
    require("Loaded 1867 texture replacement" in lines[45], "Texture count marker missing")
    require("dev.twilitrealm.luau" in lines[66] and "activating mod" in lines[66], "Luau activation missing")
    require("dev.twilitrealm.randomizer" in lines[67] and "activating mod" in lines[67], "Randomizer activation missing")
    require(any("GZ2E01" in line for line in lines), "Disc ID marker missing")
    require(all("SKIP" in lines[n - 1] for n in (82, 717, 810, 2179)), "SKIP markers missing")
    nearest_link = min(enumerate(captures, 1), key=lambda v: distance(v[1]["link"], REFERENCE))
    aggregates = []
    for actor_id in EXPECTED:
        positions = [c["actors"][actor_id] for c in captures]
        sample, near = min(enumerate(captures, 1), key=lambda v: distance(v[1]["actors"][actor_id], REFERENCE))
        aggregates.append({"id": actor_id, "home_x": EXPECTED[actor_id],
                           "sampled_xyz_bounds": [[min(p[i] for p in positions), max(p[i] for p in positions)] for i in range(3)],
                           "min_sampled_center_xz_to_reference": distance(near["actors"][actor_id], REFERENCE),
                           "nearest_sample": sample, "nearest_line": near["line"],
                           "max_sampled_displacement_3d_from_first": max(math.dist(positions[0], p) for p in positions)})
    inventories = []
    for name in ["dusklight-2.0.3.zip", "Dusklight-v2.0.3-win32-x86_64.zip",
                 "DEVF_CP01_EVIDENCIA_F_SP121.zip", "DEVF_CP01_EXTRA_COLLISIONS.zip"]:
        with zipfile.ZipFile(args.inputs / name) as archive:
            members = archive.namelist()
            nested = []
            for member in members:
                if member.lower().endswith(".dusk"):
                    with zipfile.ZipFile(io.BytesIO(archive.read(member))) as mod:
                        nested.append({"name": Path(member).name, "member_count": len(mod.namelist()),
                                       "eoc_arc_entries": [m for m in mod.namelist() if ARC_NAME.search(m)]})
            inventories.append({"name": name, "member_count": len(members),
                                "eoc_arc_entries": [m for m in members if ARC_NAME.search(m)], "nested_mods": nested})
    root = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.source, text=True).strip()
    require(root == HOST, "Source revision mismatch")
    subprocess.run(["git", "diff", "--quiet", "HEAD"], cwd=args.source, check=True)
    aurora = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.source / "extern/aurora", text=True).strip()
    require(aurora == "3227d76c60e1e782ca576610bce61c9e7744d8be", "Aurora source revision mismatch")
    source_paths = ["assets/GZ2E01/res/Object/E_oc.h", "assets/GZ2E01/res/Object/E_ocb.h",
                    "src/d/actor/d_a_e_oc.cpp", "src/dusk/mods/svc/stage.cpp", "src/d/d_stage.cpp",
                    "src/d/d_s_room.cpp", "src/f_pc/f_pc_node.cpp", "include/f_pc/f_pc_manager.h",
                    "src/f_pc/f_pc_stdcreate_req.cpp", "src/d/d_resorce.cpp", "include/d/d_resorce.h",
                    "extern/aurora/lib/dolphin/dvd/dvd.cpp"]
    here = Path(__file__).resolve().parent.parent
    previous = here.parent / "CP01/evidence"
    summary = json.loads((previous / "location-f-sp121-summary.json").read_text())
    result = {"schema": 1, "scope": "G4 offline aggregates only; no game or creation",
              "primary_log": {"sha256": LOG_HASH, "bytes": len(blob), "lines": len(lines),
                              "original_unredacted_hash_status": "USER_REPORTED_ONLY; different file not received",
                              "severity_counts": dict(levels), "ERROR": levels["ERROR"], "FATAL": levels["FATAL"],
                              "dds_mipmap_warnings": len(warnings)},
              "g2": {"status": "PASS_RUNTIME_OBSERVED; observer scope only", "host_commit": HOST,
                     "disc_id": "GZ2E01", "d3d12_marker_lines": [14, 18, 21, 23],
                     "valid_capture_count": len(captures), "census_records": len(captures) * 7,
                     "capture_lines": [c["line"] for c in captures], "capture_invariants": CONTEXT,
                     "outside_context_skip_lines": [82, 717, 810, 2179], "startup_line": 66,
                     "shutdown_lines": [2181, 2182], "mod_activation_lines": [67, 68],
                     "texture_replacement_count": 1867, "texture_count_line": 46,
                     "create_request_messages": dict(creates),
                     "ids_220_221_origin": "NOT_VERIFIED; create message is not a room/live census"},
              "reference_only": {"xyz": REFERENCE, "yaw_s16": 0, "status": "NOT_APPROVED_FOR_E_OC",
                                 "min_sampled_link_center_xz": distance(nearest_link[1]["link"], REFERENCE),
                                 "nearest_link_sample": nearest_link[0], "nearest_link_line": nearest_link[1]["line"]},
              "actor_sample_aggregates": aggregates,
              "distance_limits": "XZ center samples only; no swept envelopes, continuous trajectories, hard movement bounds, or clearance proof",
              "resource_inventories": inventories, "resource_inventory_scope": "Central-directory names; nested .dusk member names. Prior ZIP integrity reused, not repeated.",
              "native_resource_payloads": "NOT_VERIFIED; two ARC absent from available inputs",
              "aurora_commit": aurora, "source_sha256": {p: sha(args.source / p) for p in source_paths},
              "reused_evidence_sha256": {n: sha(previous / n) for n in ["location-f-sp121-summary.json", "location-f-sp121-digpoints.json", "extra-collisions-verification.json"]},
              "reused_wrock_footprint": summary["candidate"],
              "position_decision": "NO_SAFE_POSITION_VERIFIED", "g4_decision": "G4_BLOCKED_WITH_EXACT_NEXT_INPUT",
              "policy": "DISARMED_NO_REGISTRATION", "cp02": "NO-GO"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS_OFFLINE: private hash/2182 lines/28 captures, aggregates, inventories, source identity; G4 remains BLOCKED")


if __name__ == "__main__":
    main()
