#!/usr/bin/env python3
"""G4 read-only resource analysis. Stdlib; no game/native code or raw asset output.

Reuses CP01 Yaz0/RARC and F32 BMD/VTX1 readers. Adds only required JNT1,
EVP1/DRW1/SHP1 metadata, ANK1 curves and conservative skeletal bounds.
Bernstein hull subdivision bounds whole Hermite intervals, not sampled frames.
Bounds apply to ideal-real resource transforms; no runtime/FP certificate.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import zlib

HERE = Path(__file__).resolve().parents[1]
CP01 = HERE.parent / "CP01"
sys.path.insert(0, str(CP01 / "analysis"))
HOST = "40457c6adb381928e4b5fef6ed459ed291edd5e2"
INPUT_COMMIT = "91884d5932377e15a96a9f1c8df48348751f37a5"
EXPECTED = {
    "E_oc.arc": (30837, "ed7031096583a3a5a62e8ebbadb7c74dff29a8f77bf738222389ab99a39131f4"),
    "E_ocb.arc": (137250, "156bbd9d030a28885b6989ea53a4cffa965c152c29c24e37505844a0d76b8a09"),
}


def check(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ceil_sqrt(value):
    check(value >= 0, "Negative squared norm")
    integer = math.isqrt(value.numerator // value.denominator)
    return integer if F(integer * integer) >= value else integer + 1


def norm_bound(ranges):
    return ceil_sqrt(sum(max(abs(a), abs(b)) ** 2 for a, b in ranges))


def split_bezier(p):
    a, b, c, d = p
    e, f, g = (a + b) / 2, (b + c) / 2, (c + d) / 2
    h, i = (e + f) / 2, (f + g) / 2
    j = (h + i) / 2
    return (a, e, h, j), (j, i, g, d)


def hermite_hull(t0, v0, outgoing, t1, v1, incoming):
    """Exact rational convex hull of 16 subcurves over the whole interval."""
    dt = t1 - t0
    check(dt > 0, "Non-increasing key times")
    pieces = [(v0, v0 + dt * outgoing / 3, v1 - dt * incoming / 3, v1)]
    for _ in range(4):
        pieces = [child for piece in pieces for child in split_bezier(piece)]
    return min(min(p) for p in pieces), max(max(p) for p in pieces)


def curve(table, count, offset, tangent_type, default):
    check(tangent_type in (0, 1), "Unsupported tangent encoding")
    if count == 0:
        return (F(default), F(default)), 0, False
    check(0 <= offset < len(table), "Channel offset out of table")
    if count == 1:
        return (table[offset], table[offset]), 0, False
    stride = 3 if tangent_type == 0 else 4
    check(offset + count * stride <= len(table), "Channel exceeds table")
    keys = [table[offset + i * stride:offset + (i + 1) * stride] for i in range(count)]
    low, high = min(k[1] for k in keys), max(k[1] for k in keys)
    key_low, key_high = low, high
    for a, b in zip(keys, keys[1:]):
        lo, hi = hermite_hull(a[0], a[1], a[2] if stride == 3 else a[3], b[0], b[1], b[2])
        low, high = min(low, lo), max(high, hi)
    return (low, high), count - 1, low < key_low or high > key_high


def j3d_sections(data, magic, u, span):
    check(data[:8] == magic, "Unexpected J3D version")
    length, count = u(data, 8, "II")
    check(length == len(data) and 0 < count < 100, "J3D size/count mismatch")
    sections, cursor = {}, 32
    for _ in range(count):
        tag, size = span(data, cursor, 4).decode("ascii"), u(data, cursor + 4, "I")[0]
        check(size >= 8 and tag not in sections, "Duplicate/invalid J3D section")
        sections[tag] = span(data, cursor, size)
        cursor += size
    check(cursor == len(data), "J3D trailing section mismatch")
    return sections


def bck(data, u, span):
    sections = j3d_sections(data, b"J3D1bck1", u, span)
    check(set(sections) == {"ANK1"}, "Unexpected BCK section")
    a = sections["ANK1"]
    loop, shift, frames, joints, ns, nr, nt = u(a, 8, "BBHHHHH")
    ao, so, ro, to = u(a, 20, "IIII")
    check(joints == 29 and shift < 16 and loop < 5, "BCK model/loop/rotation mismatch")
    span(a, ao, joints * 54)
    tables = []
    for offset, count, fmt in [(so, ns, "f"), (ro, nr, "h"), (to, nt, "f")]:
        values = u(a, offset, str(count) + fmt)
        check(all(math.isfinite(v) for v in values), "Non-finite animation value")
        tables.append([F(v) for v in values])
    ranges, channels, segments, overshoot, animated_channels = [], [], 0, 0, 0
    for joint in range(joints):
        transform = {"scale": [], "rotation": [], "translation": []}
        channel = {"scale": [], "rotation": [], "translation": []}
        for axis in range(3):
            for kind, table_index, delta, default in [("scale", 0, 0, 1), ("rotation", 1, 6, 0), ("translation", 2, 12, 0)]:
                count, offset, tangent_type = u(a, ao + joint * 54 + axis * 18 + delta, "HHH")
                bounds, n, exceeds = curve(tables[table_index], count, offset, tangent_type, default)
                if kind == "rotation":
                    bounds = tuple(v * (1 << shift) for v in bounds)
                transform[kind].append(bounds)
                channel[kind].append((tables[table_index], count, offset, tangent_type, default))
                segments += n
                overshoot += int(exceeds)
                animated_channels += int(count > 1)
        ranges.append(transform)
        channels.append(channel)
    summary = {"frames": frames, "loop": loop, "joints": joints, "rotation_shift": shift,
               "table_lengths": [ns, nr, nt], "animated_channels": animated_channels,
               "hermite_segments": segments, "channels_with_hull_beyond_key_values": overshoot,
               "scale_range_all_joints": [float(min(r[0] for j in ranges for r in j["scale"])), float(max(r[1] for j in ranges for r in j["scale"]))],
               "max_joint_local_translation_norm_ceil": max(norm_bound(j["translation"]) for j in ranges)}
    return summary, ranges, (channels, shift)


def hierarchy(inf, n, u):
    cursor = u(inf, 20, "I")[0]
    parents = {}
    def walk(parent):
        nonlocal cursor
        current = parent
        while True:
            kind, value = u(inf, cursor, "HH")
            cursor += 4
            if kind == 0:
                return
            if kind == 2:
                check(parent is not None, "Unbalanced hierarchy")
                return
            if kind == 1:
                check(current is not None, "Missing hierarchy parent")
                walk(current)
            elif kind == 0x10:
                check(value < n and value not in parents, "Invalid hierarchy joint")
                parents[value] = parent
                current = value
            else:
                check(kind in (0x11, 0x12), "Unknown hierarchy node")
    walk(None)
    check(set(parents) == set(range(n)), "Incomplete joint hierarchy")
    return [parents[i] for i in range(n)]


def model(data, u, span, bmd):
    # Preserve the established decoder; these new models use the F32 it supports.
    meta, sections = bmd(data)
    check(set(sections) == {"INF1", "VTX1", "EVP1", "DRW1", "JNT1", "SHP1", "MAT3", "TEX1"}, "Unexpected model sections")
    j = sections["JNT1"]
    n = u(j, 8, "H")[0]
    jo, remap = u(j, 12, "II")
    indices = u(j, remap, str(n) + "H")
    parents = hierarchy(sections["INF1"], n, u)
    joints = []
    for index in indices:
        pos = jo + index * 64
        span(j, pos, 64)
        scale, rot, trans = u(j, pos + 4, "fff"), u(j, pos + 16, "hhh"), u(j, pos + 24, "fff")
        check(all(math.isfinite(v) for v in scale + trans), "Non-finite bind joint")
        check(j[pos + 2] in (0, 1, 255), "Unknown scale compensation")
        joints.append({"scale": [F(v) for v in scale], "rotation": list(rot), "translation": [F(v) for v in trans],
                       "ssc": int(j[pos + 2] == 1)})
    v = sections["VTX1"]
    vp = u(v, 12, "I")[0]
    vertices = [u(v, vp + 12 * i, "fff") for i in range(meta["vertices"])]
    check(all(math.isfinite(x) for p in vertices for x in p), "Non-finite model position")
    e = sections["EVP1"]
    ne = u(e, 8, "H")[0]
    co, io, wo, mo = u(e, 12, "IIII")
    envelopes, inverses = [], []
    if ne:
        counts = span(e, co, ne)
        total = sum(counts)
        check(all(c > 0 for c in counts), "Empty skin envelope")
        js, weights = u(e, io, str(total) + "H"), u(e, wo, str(total) + "f")
        check(all(i < n for i in js) and all(math.isfinite(w) for w in weights), "Invalid skin input")
        check(all(w >= 0 for w in weights), "Negative skin weight")
        cursor = 0
        for count in counts:
            envelopes.append([(js[k], F(weights[k])) for k in range(cursor, cursor + count)])
            cursor += count
        inverses = [u(e, mo + i * 48, "12f") for i in range(n)]
        check(all(math.isfinite(v) for m in inverses for v in m), "Non-finite inverse bind matrix")
    d = sections["DRW1"]
    nd = u(d, 8, "H")[0]
    fo, ix = u(d, 12, "II")
    draw = list(zip(span(d, fo, nd), u(d, ix, str(nd) + "H")))
    check(all((f == 0 and i < n) or (f == 1 and i < ne) for f, i in draw), "Invalid DRW joint/envelope reference")
    check(nd >= ne, "Invalid runtime draw matrix count")
    usable_draw = nd - ne  # J3DModelLoader::readDraw, not the whole stored array
    sh = sections["SHP1"]
    nsh = u(sh, 8, "H")[0]
    si, sr, _, vd, mt, dl, mi, di = u(sh, 12, "8I")
    groups, primitive_vertices, references = 0, 0, {}
    for index in u(sh, sr, str(nsh) + "H"):
        entry = si + index * 40
        span(sh, entry, 40)
        ng, vo, mg, dg = u(sh, entry + 2, "HHHH")
        check(sh[entry] in (0, 3), "Billboard/unknown shape needs separate analysis")
        attr, descriptors = vd + vo, []
        while True:
            attribute, kind = u(sh, attr, "II"); attr += 8
            if attribute == 255:
                break
            check(kind in (0, 1, 2, 3), "Invalid shape vertex descriptor")
            if kind:
                check(kind != 1 or attribute <= 8, "Unsupported direct non-matrix vertex attribute")
                descriptors.append((attribute, kind, 1 if kind in (1, 2) else 2))
        palette_state = {}
        for group in range(ng):
            use, count, first = u(sh, mi + (mg + group) * 8, "HHI")
            if sh[entry] == 3:
                palette = u(sh, mt + first * 2, str(count) + "H")
                check(all(i == 65535 or i < usable_draw for i in palette), "Invalid shape matrix palette")
                for slot, value in enumerate(palette):
                    if value != 65535:
                        palette_state[slot] = value
            else:
                check(use < usable_draw, "Invalid rigid shape matrix")
                palette_state[0] = use
            length, offset = u(sh, di + (dg + group) * 8, "II")
            display = span(sh, dl + offset, length)
            cursor = 0
            while cursor < len(display):
                command = display[cursor]; cursor += 1
                if command == 0:
                    continue  # padding NOP
                check(command & 7 == 0 and command in (0x80, 0x90, 0x98, 0xa0, 0xa8, 0xb0, 0xb8), "Unsupported display-list command/VAT")
                count = u(display, cursor, "H")[0]; cursor += 2
                for _ in range(count):
                    values = {}
                    for attribute, kind, width in descriptors:
                        values[attribute] = span(display, cursor, 1)[0] if width == 1 else u(display, cursor, "H")[0]
                        cursor += width
                    check(9 in values and values[9] < len(vertices), "Position index out of VTX1")
                    matrix_index = values.get(0, 0)
                    check(matrix_index % 3 == 0 and matrix_index // 3 in palette_state, "Unresolved carried matrix slot")
                    draw_index = palette_state[matrix_index // 3]
                    references.setdefault(draw_index, set()).add(values[9])
                    primitive_vertices += 1
            check(cursor == len(display), "Display list length mismatch")
        groups += ng
    t = sections["TEX1"]
    nt = u(t, 8, "H")[0]
    texo = u(t, 12, "I")[0]
    textures = []
    for i in range(nt):
        start = texo + i * 32
        span(t, start, 32)
        width, height = u(t, start + 2, "HH")
        mipmaps, image = t[start + 24], u(t, start + 28, "I")[0]
        check(t[start] == 14 and width > 0 and height > 0 and 0 < mipmaps < 16, "Unexpected texture encoding")
        check(image > 0, "External texture payload requires separate evidence")
        size = sum(((max(1, width >> level) + 7) // 8) * ((max(1, height >> level) + 7) // 8) * 32 for level in range(mipmaps))
        span(t, start + image, size)
        textures.append({"width": width, "height": height, "mipmaps": mipmaps, "format": "CMPR", "embedded_image": True})
    meta.update({"joints": n, "shapes": nsh, "matrix_groups": groups, "draw_table_entries": nd,
                 "usable_draw_matrices": usable_draw, "referenced_draw_matrices": len(references),
                 "primitive_vertex_references": primitive_vertices, "referenced_position_count": len(set().union(*references.values())),
                 "skin_envelopes": ne, "materials": u(sections["MAT3"], 8, "H")[0], "textures": textures,
                 "inverse_bind_count": len(inverses), "parent_chains": {str(k): chain(parents, k) for k in (1, 12, 17, 22, 25, 28) if k < n},
                 "skin_weight_sums": [float(min(sum(w for _, w in e) for e in envelopes)), float(max(sum(w for _, w in e) for e in envelopes))] if envelopes else None})
    return meta, {"parents": parents, "joints": joints, "vertices": vertices, "bounds": meta["position_bounds"], "envelopes": envelopes, "inverses": inverses, "draw": draw, "references": references}


def chain(parents, index):
    result = []
    while index is not None:
        check(index not in result, "Hierarchy cycle")
        result.append(index)
        index = parents[index]
    return list(reversed(result))


def transformed_box_radius(matrix, box):
    # Exact interval image of the raw vertex AABB: contains every stored position.
    ranges = []
    for axis in range(3):
        low = high = F(matrix[axis * 4 + 3])
        for i in range(3):
            a, b = F(matrix[axis * 4 + i]) * F(box[0][i]), F(matrix[axis * 4 + i]) * F(box[1][i])
            low, high = low + min(a, b), high + max(a, b)
        ranges.append((low, high))
    return norm_bound(ranges)


def skeletal_bounds(body, weapon, animation_ranges):
    n = len(body["joints"])
    combined = []
    for j in range(n):
        r = {}
        for kind in ("scale", "translation"):
            sources = [a[j][kind] for a in animation_ranges]
            bind = body["joints"][j][kind]
            r[kind] = [(min([v[axis][0] for v in sources] + [bind[axis]]), max([v[axis][1] for v in sources] + [bind[axis]])) for axis in range(3)]
        combined.append(r)
    # Resolve in hierarchy order, independent of numeric joint order.
    pending = set(range(n))
    origin, norm = {}, {}
    while pending:
        ready = [j for j in pending if body["parents"][j] is None or body["parents"][j] in origin]
        check(bool(ready), "Unresolvable hierarchy")
        for j in ready:
            p = body["parents"][j]
            parent_norm, parent_origin = (F(1), F(0)) if p is None else (norm[p], origin[p])
            compensation = F(1)
            if body["joints"][j]["ssc"] and p is not None:
                minimum = min(min(abs(a), abs(b)) if a * b > 0 else F(0) for a, b in combined[p]["scale"])
                check(minimum > 0, "Parent scale interval contains zero; no finite SSC bound")
                compensation = max(F(1), 1 / minimum)
            local_scale = max(max(abs(a), abs(b)) for a, b in combined[j]["scale"])
            norm[j] = parent_norm * compensation * local_scale
            origin[j] = parent_origin + parent_norm * norm_bound(combined[j]["translation"])
            pending.remove(j)
    hio = F(3, 2)
    drw_bounds = []
    for draw_index, vertex_indices in body["references"].items():
        flag, index = body["draw"][draw_index]
        points = [body["vertices"][i] for i in vertex_indices]
        box = [[min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)]]
        if flag == 0:
            radius = norm_bound([(F(a), F(b)) for a, b in zip(*box)])
            bound = origin[index] + norm[index] * radius
        else:
            bound = sum(w * (origin[j] + norm[j] * transformed_box_radius(body["inverses"][j], box)) for j, w in body["envelopes"][index])
        drw_bounds.append(bound)
    body_radius = math.ceil(hio * max(drw_bounds))
    check(len(weapon["joints"]) == 1 and weapon["joints"][0]["scale"] == [1, 1, 1] and weapon["joints"][0]["translation"] == [0, 0, 0], "Weapon root assumptions unmet")
    weapon_local_radius = norm_bound([(F(a), F(b)) for a, b in zip(*weapon["bounds"])])
    weapon_radius = math.ceil(hio * (origin[12] + norm[12] * weapon_local_radius))
    colliders = {}
    for name, j, offset, radius in [("backbone", 1, (10, 10, 0), 50), ("head", 17, (10, 0, 0), 45), ("weapon70", 12, (0, 0, 70), 45), ("weapon20", 12, (0, 0, 20), 30)]:
        offset_norm = ceil_sqrt(sum(F(v) ** 2 for v in offset))
        colliders[name] = math.ceil(hio * (origin[j] + norm[j] * offset_norm) + radius)
    return {"domain": "Ideal-real resource transforms; arbitrary rotations and joint callbacks; all28 BCK plus bind and convex morphs; NOT engine FP/runtime proof",
            "method": "exact-rational Hermite Bernstein hulls, per-joint norm propagation, SSC reciprocal exclusion of zero, EVP abs-weight sum, integer upper rounding",
            "draw_association": "SHP1 primitives/palette carry resolve position-to-DRW; per-DRW vertex AABB enclosure, not exact posed mesh",
            "hio_assumption": 1.5, "body_radius_upper": body_radius, "weapon_radius_upper": weapon_radius,
            "collider_radius_uppers": colliders, "combined_radius_upper": max(body_radius, weapon_radius, *colliders.values(), 100),
            "joint_origin_radius_uppers_hio": {str(j): math.ceil(hio * origin[j]) for j in (1, 12, 17, 22, 25, 28)},
            "nonunit_scale_joints": [j for j in range(n) if combined[j]["scale"] != [(F(1), F(1))] * 3],
            "scale_compensation_zero_parent": False}


def evaluate_channel(channel, frame):
    table, count, offset, kind, default = channel
    if count == 0:
        return float(default)
    if count == 1:
        return float(table[offset])
    step = 3 if kind == 0 else 4
    keys = [table[offset + i * step:offset + (i + 1) * step] for i in range(count)]
    if frame <= keys[0][0]:
        return float(keys[0][1])
    if frame >= keys[-1][0]:
        return float(keys[-1][1])
    a, b = next((a, b) for a, b in zip(keys, keys[1:]) if a[0] <= frame < b[0])
    t0, v0, m0, t1, v1, m1 = map(float, (a[0], a[1], a[2] if kind == 0 else a[3], b[0], b[1], b[2]))
    t = (frame - t0) / (t1 - t0)
    return (2*t**3-3*t**2+1)*v0 + (t**3-2*t**2+t)*(t1-t0)*m0 + (-2*t**3+3*t**2)*v1 + (t**3-t**2)*(t1-t0)*m1


def concat(a, b):
    return [sum(a[r*4+k] * b[k*4+c] for k in range(3)) + (a[r*4+3] if c == 3 else 0) for r in range(3) for c in range(4)]


def point(matrix, p):
    return tuple(sum(matrix[r*4+k]*p[k] for k in range(3)) + matrix[r*4+3] for r in range(3))


def sampled_pose(body, weapon, channels, frame):
    """Diagnostic only: double trig, callbacks zero, no morph/root attitude."""
    transforms = []
    for j, bind in enumerate(body["joints"]):
        if channels is None:
            transforms.append({"scale": list(map(float, bind["scale"])), "translation": list(map(float, bind["translation"])), "rotation": bind["rotation"]})
        else:
            table, shift = channels
            t = {kind: [evaluate_channel(c, frame) for c in table[j][kind]] for kind in ("scale", "translation", "rotation")}
            t["rotation"] = [((int(v) << shift) + 32768) % 65536 - 32768 for v in t["rotation"]]
            transforms.append(t)
    worlds, pending = {}, set(range(len(transforms)))
    while pending:
        ready = [j for j in pending if body["parents"][j] is None or body["parents"][j] in worlds]
        check(bool(ready), "Unresolvable sampled pose")
        for j in ready:
            p, tr = body["parents"][j], transforms[j]
            x, y, z = [v*math.pi/32768 for v in tr["rotation"]]
            sx, cx, sy, cy, sz, cz = math.sin(x), math.cos(x), math.sin(y), math.cos(y), math.sin(z), math.cos(z)
            rotation = [[cz*cy, cz*sy*sx-sz*cx, cz*sy*cx+sz*sx], [sz*cy, sz*sy*sx+cz*cx, sz*sy*cx-cz*sx], [-sy, cy*sx, cy*cx]]
            local = [rotation[r][c]*tr["scale"][c] if c < 3 else tr["translation"][r] for r in range(3) for c in range(4)]
            if body["joints"][j]["ssc"] and p is not None:
                for r in range(3):
                    check(transforms[p]["scale"][r] != 0, "Sampled SSC singularity")
                    for c in range(3):
                        local[r*4+c] /= transforms[p]["scale"][r]
            parent = [1.5,0,0,0, 0,1.5,0,0, 0,0,1.5,0] if p is None else worlds[p]
            worlds[j] = concat(parent, local)
            pending.remove(j)
    positions = []
    for draw_index, indices in body["references"].items():
        flag, index = body["draw"][draw_index]
        if flag == 0:
            matrix = worlds[index]
        else:
            terms = [(concat(worlds[j], body["inverses"][j]), float(w)) for j, w in body["envelopes"][index]]
            matrix = [sum(m[k]*w for m,w in terms) for k in range(12)]
        positions.extend(point(matrix, body["vertices"][i]) for i in indices)
    wp = [point(worlds[12], p) for p in weapon["vertices"]]
    bounds = lambda ps: [[min(p[i] for p in ps) for i in range(3)], [max(p[i] for p in ps) for i in range(3)]]
    return {"body_bounds": bounds(positions), "weapon_bounds": bounds(wp),
            "body_radius_sample": max(math.sqrt(sum(v*v for v in p)) for p in positions),
            "weapon_radius_sample": max(math.sqrt(sum(v*v for v in p)) for p in wp),
            "leg_end25_y": point(worlds[25], (0,0,0))[1], "leg_end28_y": point(worlds[28], (0,0,0))[1]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", required=True, type=Path)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--private-work", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    code = HERE.parents[1]
    work = args.private_work.resolve()
    check(work != code and code not in work.parents, "Private scratch must be outside repository")
    check(args.output.resolve().suffix == ".json", "Derived JSON output only")
    os.environ["DEVF_CP01_LOCATION_WORK"] = str(work)
    from analyze_location import rarc, u, span
    from location_geometry import bmd
    manifest_data = (args.inputs / "DEVF_G4_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_data)
    check(manifest["disc_id"] == "GZ2E01", "Unexpected disc ID")
    declared = {f["filename"]: (f["bytes"], f["sha256"]) for f in manifest["files"]}
    check(declared == EXPECTED, "Manifest resource identity mismatch")
    inventories, payloads = {}, {}
    for arc, (size, expected_hash) in EXPECTED.items():
        blob = (args.inputs / arc).read_bytes()
        check(len(blob) == size and digest(blob) == expected_hash, "ARC identity mismatch")
        check(blob[:4] == b"Yaz0", "Unexpected ARC compression")
        raw, entries, files = rarc(blob)
        records = []
        for f in files:
            content = f["raw"]
            payloads[(arc, f["index"])] = content
            records.append({k: f[k] for k in ("index", "id", "path", "size")})
            records[-1]["sha256"] = digest(content)
        inventories[arc] = {"bytes": len(blob), "sha256": digest(blob), "crc32_computed_not_embedded": f"{zlib.crc32(blob) & 0xffffffff:08x}",
                            "compression": "Yaz0", "container": "RARC", "decoded_bytes": len(raw),
                            "table_entries": len(entries), "file_count": len(files), "files": records}
    check(set(k[1] for k in payloads if k[0] == "E_oc.arc") == {3, 4}, "Model indices mismatch")
    check(set(k[1] for k in payloads if k[0] == "E_ocb.arc") == set(range(3, 31)), "Animation indices mismatch")
    body_meta, body = model(payloads[("E_oc.arc", 3)], u, span, bmd)
    weapon_meta, weapon = model(payloads[("E_oc.arc", 4)], u, span, bmd)
    check(body_meta["joints"] == 29 and weapon_meta["joints"] == 1, "Model skeleton mismatch")
    animations, all_ranges, diagnostic_samples = [], [], {}
    for file in inventories["E_ocb.arc"]["files"]:
        summary, ranges, channels = bck(payloads[("E_ocb.arc", file["index"])], u, span)
        summary.update(index=file["index"], name=Path(file["path"]).name)
        animations.append(summary)
        all_ranges.append(ranges)
        if file["index"] in (5, 6, 27):
            frames = [0] if file["index"] == 27 else [i/2 for i in range(2*summary["frames"]+1)]
            samples = [sampled_pose(body, weapon, channels, t) for t in frames]
            result_sample = {"sample_count": len(samples), "sample_spacing_frames": 0.5 if len(samples) > 1 else None,
                             "body_bounds": [[min(s["body_bounds"][0][i] for s in samples) for i in range(3)], [max(s["body_bounds"][1][i] for s in samples) for i in range(3)]],
                             "weapon_bounds": [[min(s["weapon_bounds"][0][i] for s in samples) for i in range(3)], [max(s["weapon_bounds"][1][i] for s in samples) for i in range(3)]],
                             "max_body_radius_sample": max(s["body_radius_sample"] for s in samples), "max_weapon_radius_sample": max(s["weapon_radius_sample"] for s in samples)}
            if file["index"] == 27:
                result_sample.update(leg_end25_y=samples[0]["leg_end25_y"], leg_end28_y=samples[0]["leg_end28_y"])
            diagnostic_samples[summary["name"]] = result_sample
    root = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.source, text=True).strip()
    check(root == HOST, "Wrong official source")
    subprocess.run(["git", "diff", "--quiet", "HEAD"], cwd=args.source, check=True)
    source_paths = ["src/d/actor/d_a_e_oc.cpp", "src/m_Do/m_Do_ext.cpp", "libs/JSystem/src/J3DGraphAnimator/J3DAnimation.cpp",
                    "libs/JSystem/src/J3DGraphAnimator/J3DJoint.cpp", "libs/JSystem/src/J3DGraphAnimator/J3DJointTree.cpp",
                    "libs/JSystem/src/J3DGraphAnimator/J3DMtxBuffer.cpp", "libs/JSystem/src/J3DGraphLoader/J3DAnmLoader.cpp",
                    "libs/JSystem/src/J3DGraphLoader/J3DModelLoader.cpp", "libs/JSystem/include/JSystem/JMath/JMath.h"]
    bounds = skeletal_bounds(body, weapon, all_ranges)
    bind_pose = sampled_pose(body, weapon, None, 0)
    check(all(s["max_body_radius_sample"] <= bounds["body_radius_upper"] and s["max_weapon_radius_sample"] <= bounds["weapon_radius_upper"] for s in diagnostic_samples.values()), "Sample escapes resource enclosure")
    result = {"input_commit": INPUT_COMMIT, "official_root": HOST, "manifest_sha256": digest(manifest_data),
              "provenance": {"disc_id": manifest["disc_id"], "extraction_method": manifest["extraction_method"], "effective_game_override_status": manifest["effective_game_override_status"],
                             "extraction_witness": "USER_REPORTED; bytes/hashes independently verified"},
              "arc_integrity": inventories, "models": {"body3": body_meta, "weapon4": weapon_meta}, "animations": animations,
              "all28_included": True, "animation_exclusions": [], "resource_skeletal_bound": bounds,
              "pose_diagnostics_only": {"status": "APPROXIMATE_SAMPLES; double trig, callback angles0, actor attitude0, no morph; NOT a continuous bound or engine execution",
                                        "bind": bind_pose, "animations": diagnostic_samples},
              "engine_arithmetic_and_render": "NOT_VERIFIED; not run", "movement_confinement": "NOT_VERIFIED; native2000 is soft",
              "source_sha256": {p: digest((args.source / p).read_bytes()) for p in source_paths},
              "reused_decoders": ["CP01/analysis/analyze_location.py:yaz/rarc", "CP01/analysis/location_geometry.py:bmd"],
              "reused_g2_aggregate_sha256": digest((HERE.parent / "CP01_G4_EOC_SAFETY/evidence/g4-aggregates.json").read_bytes()),
              "status": "G4_RESOURCE_VERIFIED_POSITION_BLOCKED", "policy": "DISARMED_NO_REGISTRATION", "g5": "NO-GO", "cp02": "NO-GO"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS_OFFLINE: exact ARC hashes/containers/models/28 BCK; conditional continuous resource bounds; position remains BLOCKED")
    print(json.dumps(bounds, indent=2))


if __name__ == "__main__":
    main()
