"""Incremental analysis of the previously unresolved room-3 route-7 consumer.

Reads existing private inventory/footprint results; does not redo KCL/WRock analysis.
"""
from location_spatial import ROOT, json, math, paths, point_rect_distance

if __name__ == "__main__":
    inventory = json.loads((ROOT / "inventory.json").read_text())
    footprint = json.loads((ROOT / "footprint-verification.json").read_text())
    room = inventory["archives"]["R03_00.arc"]
    chunks = next(f["chunks"] for f in room["files"] if "chunks" in f)
    common = next(c for c in chunks if c["tag"] == "ACTR")
    consumer = next(e for e in common["records"] if e["name"] == "Digpl"
                    and ((int(e["parameters"], 16) >> 8) & 15) == 5)
    parameter = int(consumer["parameters"], 16)
    route_index = (parameter >> 20) & 255
    assert consumer["index"] == 5 and parameter == 0xf07ff5ff and route_index == 7
    route = paths((ROOT / "R03_00.arc/dzr/room.dzr").read_bytes())[route_index]
    assert route["count"] == 27
    position = footprint["candidate"]
    poly = footprint["footprints"]["model_and_collision"]["rectangle"]
    distances = []
    for index, point in enumerate(route["points"]):
        distances.append(dict(index=index, position=point,
                              center_distance_xz=math.hypot(point[0] - position[0],
                                                           point[2] - position[2]),
                              distance_to_model_rectangle_xz=point_rect_distance(point, poly)))
    nearest = min(distances, key=lambda e: e["distance_to_model_rectangle_xz"])
    assert nearest["index"] == 8
    assert nearest["distance_to_model_rectangle_xz"] > 500
    report = dict(
        consumer=dict(chunk="ACTR", index=5, name="Digpl", parameters=hex(parameter),
                      initial_type=5, path_index=7, switch=parameter & 255,
                      engine_class="daObjDigpl_c"),
        route_semantics="discrete wolf digging positions, not a continuous actor trajectory",
        scope="one verified consumer; not an exhaustive exclusion of all other consumers",
        candidate=position, nearest_dig_point=nearest,
        all_27_points_outside_model_rectangle=True,
        all_27_points_distance_to_rectangle_above_500=True,
        look_position_radius=500, look_position_y_tolerance=200,
        particle_emission_distance_3d=1000,
        separation_above_look_radius=nearest["distance_to_model_rectangle_xz"] - 500,
        previous_polyline_distance=115.61556516274018,
        previous_polyline_distance_is_swept_actor_clearance=False,
        runtime_point_used_flags="NOT_VERIFIED",
        runtime_game="NOT_TESTED",
        safe_location="NOT_APPROVED",
        policy="DISARMED_NO_REGISTRATION",
    )
    (ROOT / "digpoints-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
