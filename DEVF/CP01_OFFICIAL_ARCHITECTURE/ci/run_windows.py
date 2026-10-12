"""Only new disarmed prototype/lab/type-surface builds; no game, packaging or install target."""
import argparse
import datetime
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from verify_sources import verify

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--build", type=Path, required=True)
parser.add_argument("--evidence", type=Path, required=True)
args = parser.parse_args()
evidence = args.evidence.resolve()
evidence.mkdir(parents=True, exist_ok=True)
project = Path(__file__).resolve().parents[1]
source = args.source.resolve()
build = args.build.resolve()
result = {"started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "platform": platform.platform(), "workflow_sha": os.getenv("GITHUB_SHA"),
          "run_id": os.getenv("GITHUB_RUN_ID"), "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
          "toolchain_env": {key: os.getenv(key) for key in
                            ("VCToolsVersion", "WindowsSDKVersion", "VSCMD_ARG_TGT_ARCH")},
          "policy": "DISARMED_NO_REGISTRATION", "game_executed": False,
          "original_host_built": False, "packaged_or_installed": False,
          "phases": [], "status": "BLOCKED"}

def run(label, command):
    start = time.monotonic()
    with (evidence / f"{label}.log").open("w", encoding="utf-8") as log:
        completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, text=True)
    result["phases"].append({"label": label, "command": command,
                             "seconds": round(time.monotonic() - start, 3), "exit": completed.returncode})
    print(f"{label}: exit={completed.returncode}", flush=True)
    if completed.returncode:
        print((evidence / f"{label}.log").read_text(encoding="utf-8")[-16000:], flush=True)
        raise RuntimeError(f"{label} failed")

try:
    if os.name != "nt": raise RuntimeError("Windows MSVC runner required")
    (evidence / "source-references.json").write_text(json.dumps(verify(source), indent=2) + "\n", encoding="utf-8")
    build.mkdir(parents=True, exist_ok=True)
    version_source = build / "compiler-version.cpp"
    version_source.write_text("int devf_architecture_compiler_version_only;\n", encoding="utf-8")
    run("compiler", ["cl", "/Bv", "/c", str(version_source), f"/Fo{build / 'compiler-version.obj'}"])
    run("cmake-version", ["cmake", "--version"])
    run("configure", ["cmake", "-S", str(project), "-B", str(build), "-G", "Ninja",
                       "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_C_COMPILER=cl", "-DCMAKE_CXX_COMPILER=cl",
                       f"-DDUSK_SOURCE={source}"])
    run("build", ["cmake", "--build", str(build), "--target", "devf_official_disarmed",
                  "official_placement_lab", "game_abi_surface", "--parallel", "2"])
    run("lab", [str(build / "official_placement_lab.exe")])
    run("module-exports", ["dumpbin", "/exports", str(build / "devf_official_disarmed.dll")])
    run("module-imports", ["dumpbin", "/imports", str(build / "devf_official_disarmed.dll")])
    exports = (evidence / "module-exports.log").read_text(encoding="utf-8")
    for entry in ("mod_initialize", "mod_update", "mod_shutdown", "mod_ctx"):
        if entry not in exports: raise RuntimeError(f"Missing export {entry}")
    imports = (evidence / "module-imports.log").read_text(encoding="utf-8").lower()
    if "dusklight" in imports: raise RuntimeError("Service-only prototype unexpectedly imports game binary")
    dll = build / "devf_official_disarmed.dll"
    result["own_disarmed_dll"] = {"bytes": dll.stat().st_size, "sha256": hashlib.sha256(dll.read_bytes()).hexdigest(),
                                  "uploaded": False, "executed_in_game": False}
    if list(build.rglob("*.dusk")): raise RuntimeError("Unexpected package output")
    result["source_after"] = verify(source)["tracked_source_clean"]
    result["lab_summary"] = (evidence / "lab.log").read_text(encoding="utf-8").splitlines()[-1]
    result["status"] = "PASS"
finally:
    result["ended_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (evidence / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
