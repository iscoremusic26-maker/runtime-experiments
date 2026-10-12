"""CP01 incremental external ARC analysis. Original map/WRock results are reused.

Private extracted resources stay under DEVF_CP01_LOCATION_WORK, outside the code repo.
No host calls, actor registration, game execution or modification of original resources.
"""
import argparse
import hashlib
import itertools
import math
import struct
import zipfile
import zlib
from analyze_location import ROOT, span, u, yaz, rarc, dzb, bbox
from location_spatial import triangle_box, point_rect_distance
import json
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bmd_extra(data):
    """Decode only the supplied models; supports their packed S16 positions."""
    assert data[:8] == b"J3D2bmd3"
    length, count = u(data, 8, "II")
    assert length == len(data) and count < 100
    sections = {}
    offset = 32
    for _ in range(count):
        tag = span(data, offset, 4).decode("ascii")
        size = u(data, offset + 4, "I")[0]
        assert size >= 8 and tag not in sections
        sections[tag] = span(data, offset, size)
        offset += size
    assert offset == len(data)
    vertex_count = u(sections["INF1"], 16, "I")[0]
    vertex = sections["VTX1"]
    fmt, position = u(vertex, 8, "II")
    formats = {}
    while True:
        attribute, components, kind = u(vertex, fmt, "III")
        fraction = span(vertex, fmt + 12, 1)[0]
        if attribute == 255:
            break
        assert attribute not in formats
        formats[attribute] = (components, kind, fraction)
        fmt += 16
    components, kind, fraction = formats[9]
    assert components == 1 and kind in (3, 4) and fraction < 32
    stride = 6 if kind == 3 else 12
    span(vertex, position, vertex_count * stride)
    vertices = [u(vertex, position + i * stride, "hhh" if kind == 3 else "fff")
                for i in range(vertex_count)]
    if kind == 3:
        vertices = [tuple(x / (1 << fraction) for x in v) for v in vertices]
    assert all(math.isfinite(x) for v in vertices for x in v)
    joint = sections["JNT1"]
    nj = u(joint, 8, "H")[0]
    jo = u(joint, 12, "I")[0]
    span(joint, jo, nj * 64)
    assert nj == 1, "Nontrivial joint hierarchy requires separate analysis"
    scale = u(joint, jo + 4, "fff")
    rotation = u(joint, jo + 16, "hhh")
    translation = u(joint, jo + 24, "fff")
    assert scale == (1, 1, 1) and rotation == (0, 0, 0) and translation == (0, 0, 0)
    bounds = [u(joint, jo + 40, "fff"), u(joint, jo + 52, "fff")]
    assert all(bounds[0][i] <= bounds[1][i] for i in range(3))
    textures = []
    tex = sections["TEX1"]
    nt = u(tex, 8, "H")[0]
    to = u(tex, 12, "I")[0]
    names = u(tex, 16, "I")[0]
    assert u(tex, names, "H")[0] == nt
    span(tex, names + 4, nt * 4)
    span(tex, to, nt * 32)
    for i in range(nt):
        o = to + 32 * i
        image = u(tex, o + 28, "I")[0]
        width, height = u(tex, o + 2, "HH")
        mipmaps = span(tex, o + 24, 1)[0]
        assert tex[o] == 14 and width == 128 and height == 128 and mipmaps == 1
        if image:
            # GX_TF_CMPR: 8x8 tiles, 32 bytes/tile; supplied images have one level.
            span(tex, o + image, ((width + 7)//8) * ((height + 7)//8) * 32)
        name_offset = names + u(tex, names + 4 + i * 4 + 2, "H")[0]
        name_end = tex.index(0, name_offset)
        texture_name = span(tex, name_offset, name_end - name_offset).decode("ascii")
        textures.append(dict(name=texture_name,width=width,height=height,
                             format="GX_TF_CMPR",mipmap_count=mipmaps,
                             image_offset=image, embedded_image=image != 0))
    return dict(vertex_count=vertex_count, position_type="S16" if kind == 3 else "F32",
                fractional_bits=fraction, position_bounds=bbox(vertices),
                joint_count=nj, joint_identity=True, joint_bounds=bounds,
                textures=textures, sections={k:len(v) for k,v in sections.items()}), vertices


def spec_extra(data):
    """Follow spec_data_c::Set and its block cursor, including texture sharing."""
    kind, flags = u(data, 0, "HH")
    assert kind == 1
    report = dict(type=kind, flags=hex(flags),target_shape=flags & 15,
                  attention_fields=[(flags >> 14) & 3, (flags >> 12) & 3,
                                    (flags >> 9) & 7],
                  extra_target_flag=(flags >> 8) & 1,
                  particle_ids=[], particle_model_numbers=[], sound_ids=[],
                  texture_shares=[], blocks=[])
    offset = 4
    while True:
        block = span(data, offset, 1)[0]
        if block == 0:
            assert all(x == 0 for x in data[offset:])
            report["terminator_offset"] = offset
            break
        start = offset
        if block in (1, 2):
            length = u(data, offset, "I")[0] & 0xffffff
            span(data, offset + 4, length)
            stride = 16 if block == 1 else 4
            assert length % stride == 0
            for i in range(length // stride):
                o = offset + 4 + i * stride
                if block == 1:
                    flag, resource = u(data, o, "II")
                    report["particle_ids"].append(hex(resource & 0xffff))
                    report["particle_model_numbers"].append((flag >> 20) & 15)
                else:
                    report["sound_ids"].append(hex(u(data, o, "I")[0]))
            offset += length + 4
        elif block == 3:
            number = span(data, offset + 4, 1)[0]
            cursor = offset + 8
            for _ in range(number):
                end = data.index(0, cursor)
                target = span(data, cursor, end - cursor).decode("ascii")
                cursor = end + 1
                if data[cursor] == 0:
                    assert span(data, cursor, 2) == b"\0\1"
                    source = "STAGE_TEXTURES"
                    cursor += 2
                else:
                    end = data.index(0, cursor)
                    source = span(data, cursor, end - cursor).decode("ascii")
                    cursor = end + 1
                report["texture_shares"].append(dict(target=target, source=source))
            offset = cursor
        elif block == 4:
            report["far_info"] = u(data, offset + 4, "f")[0]
            offset += 8
        else:
            raise ValueError(f"Unsupported or invalid spec block {block}")
        report["blocks"].append(dict(type=block,offset=start,decoded_length=offset-start))
    assert report["target_shape"] == 2
    assert all(x == 0 for x in report["particle_model_numbers"])
    return report


def engine_trig(angle):
    # JMath::TSinCosTable<13,f32> truncates unsigned s16 to 8192 samples.
    quantized = ((angle & 0xffff) >> 3) << 3
    radians = quantized * 2 * math.pi / 65536
    f32 = lambda x: struct.unpack("f", struct.pack("f", x))[0]
    return f32(math.cos(radians)), f32(math.sin(radians))


def transform(vertex, position, angles, scale):
    # Exact axis order in mDoMtx_ZXYrotM: T * Ry * Rx * Rz * S.
    x, y, z = [v * s for v, s in zip(vertex, scale)]
    co, si = engine_trig(angles[2]);x,y=co*x-si*y,si*x+co*y
    co, si = engine_trig(angles[0]);y,z=co*y-si*z,si*y+co*z
    co, si = engine_trig(angles[1]);x,z=co*x+si*z,-si*x+co*z
    return tuple(v+p for v,p in zip((x,y,z),position))


def box_vertices(bounds):
    return list(itertools.product(*zip(bounds[0], bounds[1])))


def spatial_test(vertices, triangles, candidate_low, candidate_high):
    bounds = bbox(vertices)
    gaps = [max(candidate_low[i]-bounds[1][i], bounds[0][i]-candidate_high[i], 0)
            for i in range(3)]
    overlaps = [i for i,t in enumerate(triangles)
                if triangle_box([vertices[j] for j in t[:3]], candidate_low, candidate_high)]
    return dict(world_bounds=bounds,axis_gaps_xyz=gaps,
                aabb_distance_lower_bound=math.sqrt(sum(x*x for x in gaps)),
                triangle_box_intersections=len(overlaps))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--prior", required=True, type=Path)
    args = parser.parse_args()
    zip_path = args.inputs / "DEVF_CP01_EXTRA_COLLISIONS.zip"
    raw = zip_path.read_bytes()
    assert not raw.startswith(b"version https://git-lfs.github.com/spec/v1")
    manifest = (args.inputs / "CP01_EXTRA_ZIP_SHA256SUMS.txt").read_text().splitlines()
    assert len(manifest) == 1
    expected, filename = manifest[0].split()
    assert filename.lstrip("*") == zip_path.name and digest(raw) == expected
    report = dict(zip_size=len(raw),zip_sha256=digest(raw),integrity="PASS",
                  input_commit="9f95a34d93810b55250e8b833a2e343757cf8a01",
                  members=[],archives={},instances=[],policy="DISARMED_NO_REGISTRATION",
                  runtime_game="NOT_TESTED",safe_location="NOT_VERIFIED",
                  host_unload_barrier="BLOCKED_UNCHANGED",cp02="NO_GO")
    payloads = {}
    with zipfile.ZipFile(zip_path) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == 3 and set(archive.namelist()) == {
            "@bg004d.arc", "Obj_Board.arc", "CP01_EXTRA_SHA256SUMS.txt"}
        lines = archive.read("CP01_EXTRA_SHA256SUMS.txt").decode().splitlines()
        sums = dict((line.split()[1].lstrip("*"),line.split()[0])
                    for line in lines if line.strip())
        assert set(sums) == {"@bg004d.arc","Obj_Board.arc"}
        for entry in archive.infolist():
            data = archive.read(entry)
            assert len(data)==entry.file_size and zlib.crc32(data)==entry.CRC
            if entry.filename in sums:
                assert digest(data)==sums[entry.filename]
                assert len(data)=={"@bg004d.arc":19385,"Obj_Board.arc":440}[entry.filename]
            report["members"].append(dict(name=entry.filename,size=len(data),
                compressed_size=entry.compress_size,crc32=f"{entry.CRC:08x}",sha256=digest(data)))
            if not entry.filename.endswith(".arc"):
                continue
            decoded, entries, files = rarc(data)
            info = dict(compression=data[:4].decode(),decoded_size=len(decoded),files=[])
            for f in files:
                content = yaz(f["raw"])
                destination = ROOT / entry.filename / f["path"]
                destination.parent.mkdir(parents=True,exist_ok=True)
                destination.write_bytes(content)
                payloads[(entry.filename, f["name"].lower())] = content
                record = {k:f[k] for k in ("index","id","path","size")}
                record["sha256"] = digest(content)
                if f["name"].endswith(".dzb"):
                    collision,vertices,triangles,_=dzb(content)
                    assert all(math.isfinite(x) for v in vertices for x in v)
                    assert all(g["scale"]==(1,1,1) and g["angle"]==(0,0,0)
                               and g["translation"]==(0,0,0) for g in collision["groups"])
                    record["collision"]=collision
                elif f["name"].endswith(".bmd"):
                    record["model"]=bmd_extra(content)[0]
                elif f["name"]=="spec.dat":
                    record["spec"]=spec_extra(content)
                info["files"].append(record)
            report["archives"][entry.filename]=info
    spec=spec_extra(payloads[("@bg004d.arc","spec.dat")])
    model0,_=bmd_extra(payloads[("@bg004d.arc","model0.bmd")])
    model1,_=bmd_extra(payloads[("@bg004d.arc","model1.bmd")])
    for share in spec["texture_shares"]:
        assert ("@bg004d.arc",share["target"].lower()) in payloads
        assert ("@bg004d.arc",share["source"].lower()) in payloads
    assert model1["textures"][0]["name"] == model0["textures"][0]["name"]
    assert model0["textures"][0]["embedded_image"] and not model1["textures"][0]["embedded_image"]
    report["dependencies"]=dict(texture_sharing=spec["texture_shares"],
        texture_name_match=model0["textures"][0]["name"],
        missing_optional_broken_collision="model1.dzb",
        broken_collision_is_absent_not_external_reference=True,
        external_geometry_references=[],
        global_particle_ids=spec["particle_ids"],global_sound_ids=spec["sound_ids"],
        particle_model_dependency=False,
        global_effects_extent="NOT_VERIFIED")
    # Reuse prior JSON, never reopen original game ARC or recalculate KCL/WRock/Digpl.
    prior=json.loads((args.prior/"inventory.json").read_text())
    footprint=json.loads((args.prior/"footprint-verification.json").read_text())
    dig=json.loads((args.prior/"digpoints-verification.json").read_text())
    assert abs(dig["nearest_dig_point"]["distance_to_model_rectangle_xz"]-565.6960562988279)<1e-7
    report["reused_digpl_distance"]=dig["nearest_dig_point"]["distance_to_model_rectangle_xz"]
    position=footprint["candidate"];poly=footprint["footprints"]["model_and_collision"]["rectangle"]
    assert position==[-4806.7346,-6729.480961460304,65135.8281]
    low=(poly[0][0],position[1],poly[0][1])
    high=(poly[2][0],position[1]+429.4033508300781,poly[2][1])
    report["candidate_box"]=[low,high]
    chunks=next(f["chunks"] for f in prior["archives"]["R03_00.arc"]["files"] if "chunks" in f)
    for chunk in chunks:
        if chunk["tag"] not in ("ACTR","ACT6","SCOB","SCO6"):
            continue
        for actor in chunk["records"]:
            if actor["name"] not in ("mmvbg","ClearB"):
                continue
            param=int(actor["parameters"],16)
            result=dict(chunk=chunk["tag"],index=actor["index"],name=actor["name"],
                parameters=actor["parameters"],position=actor["position"],stored_angles=actor["angle"])
            if actor["name"]=="mmvbg":
                assert param==0x1fe0004d and chunk["tag"]=="ACTR"
                angles=(0,actor["angle"][1],0);scale=(1,1,1)
                _,verts,triangles,_=dzb(payloads[("@bg004d.arc","model0.dzb")])
                result["switch"]=(actor["angle"][2]&0xffff)&255
                result["secondary_switch"]=(actor["angle"][2]&0xffff)>>8
                result["object_arg0"]=(actor["angle"][0]&0xffff)&255
                result["event_id"]=(param>>21)&255
                result["state0_collision"]="model0.dzb"
                result["state1_collision"]="NONE: optional model1.dzb absent"
                result["physics"]=spatial_test(
                    [transform(v,actor["position"],angles,scale) for v in verts],
                    triangles,low,high)
                radius=max(model0["joint_bounds"][1][0],model0["joint_bounds"][1][2])
                result["target_cylinder"]=dict(radius=radius,height=model0["joint_bounds"][1][1],
                    gap_xz=point_rect_distance(actor["position"],poly)-radius)
                result["attention_helper"]="Tag_Attp; arg0=3 and arg1=3 disable lock-on flags"
                result["render_state_boxes"]=[]
                for model in (model0,model1):
                    transformed=[transform(v,actor["position"],angles,scale)
                                 for v in box_vertices(model["joint_bounds"])]
                    b=bbox(transformed)
                    gaps=[max(low[i]-b[1][i],b[0][i]-high[i],0) for i in range(3)]
                    result["render_state_boxes"].append(dict(world_bounds=b,axis_gaps_xyz=gaps))
            else:
                assert param==0xff41 and chunk["tag"]=="SCO6"
                angles=actor["angle"]
                scale=[x/10 for x in actor["scale_bytes"]]
                if param&15==1:
                    scale[0]*=10;scale[2]*=10
                _,verts,triangles,_=dzb(payloads[("Obj_Board.arc","clearb02.dzb")])
                result["variant"]="clearb02.dzb"
                result["switch"]=(param>>8)&255
                result["condition"]="arg0=4, switch255: dSv_info_c::isSwitch returns FALSE; registered"
                result["physics"]=spatial_test(
                    [transform(v,actor["position"],angles,scale) for v in verts],
                    triangles,low,high)
                result["initial_load_physics"]=spatial_test(
                    [transform(v,actor["position"],(0,angles[1],0),
                               [x/10 for x in actor["scale_bytes"]]) for v in verts],
                    triangles,low,high)
                assert result["initial_load_physics"]["triangle_box_intersections"]==0
                assert result["initial_load_physics"]["aabb_distance_lower_bound"]>1000
                # Independent witness: a horizontal local plane tilted by pitch90 has
                # world Y endpoints ±300, and the source scale remains X10/Z6.
                assert scale == [10,1,6] and angles[0] == 16384 and angles[2] == 0
                assert abs(result["physics"]["world_bounds"][0][1]+6700)<1e-4
                assert abs(result["physics"]["world_bounds"][1][1]+6100)<1e-4
            result["effective_angles"]=angles;result["effective_scale"]=scale
            assert result["physics"]["triangle_box_intersections"]==0
            assert result["physics"]["aabb_distance_lower_bound"]>1000
            report["instances"].append(result)
    assert len(report["instances"])==4
    report["static_collision_separation"]="PASS four placements, all modeled switch states"
    report["numeric_scope"]="double calculations; quantized JMath angle grid and rounded sin/cos; not engine execution"
    report["numeric_margin_units"]=1
    assert all(max(e["physics"]["axis_gaps_xyz"])>report["numeric_margin_units"]
               for e in report["instances"])
    (ROOT/"extra-collisions-verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PASS new ZIP integrity/structures, dependencies and static separation for four placements.")
    print("Private derived report:",ROOT/"extra-collisions-verification.json")


if __name__=="__main__":
    main()
