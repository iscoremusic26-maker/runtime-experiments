"""Verify downloaded *text-only* CI evidence and account explicitly for Windows CRLF."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from verify_sources import verify

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--pass-zip", type=Path, required=True)
parser.add_argument("--failure-zip", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
allowed = {"compiler.log", "cmake-version.log", "configure.log", "build.log", "lab.log",
           "module-exports.log", "module-imports.log", "result.json", "source-references.json"}
items = [
    ("windows-pass", args.pass_zip, "09dcc93a116682146c3b4dfffea02c6f4d7a8998ce83e9987544988ac590bd83", 38277234930, 11759173058),
    ("windows-first-failure", args.failure_zip, "2fab3e4646518e843c50b532a24437694174faefd8dcb40bfb6a7ece678b0dd1", 38276827345, 11758848796),
]
args.output.mkdir(parents=True, exist_ok=True)
verification = []
for name, path, digest, run, artifact in items:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != digest: raise SystemExit(f"Artifact SHA256 mismatch: {name}")
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None: raise SystemExit(f"CRC failure: {name}")
        members = archive.infolist()
        if not all(i.filename in allowed and not i.is_dir() for i in members):
            raise SystemExit(f"Unexpected/nontext member: {name}")
        if len({i.filename for i in members}) != len(members): raise SystemExit("Duplicate member")
        dest = args.output / name
        dest.mkdir(parents=True, exist_ok=True)
        files = []
        for info in members:
            data = archive.read(info.filename)
            data.decode("utf-8")
            (dest / info.filename).write_bytes(data)
            files.append({"path": info.filename, "bytes": len(data), "crc32": f"{info.CRC:08x}",
                          "sha256": hashlib.sha256(data).hexdigest()})
        result = json.loads(archive.read("result.json"))
        if name == "windows-pass" and (result["status"] != "PASS" or
                result["lab_summary"] != "SUMMARY 26 PASS; no host/game/runtime test"):
            raise SystemExit("Missing lab PASS evidence")
    verification.append({"run_id": run, "artifact_id": artifact, "zip_bytes": path.stat().st_size,
                         "zip_sha256": actual, "github_digest_match": True, "crc_all_pass": True,
                         "text_only_allowlist_pass": True, "files": files})

local = verify(args.source.resolve())
windows = json.loads((args.output / "windows-pass/source-references.json").read_text())
if windows["official_root"] != local["official_root"]: raise SystemExit("Wrong Windows official root")
by_path = {item["path"]: item for item in windows["references"]}
if set(by_path) != {item["path"] for item in local["references"]}:
    raise SystemExit("Wrong Windows reference set")
compared = []
for item in local["references"]:
    relative = item["path"]
    data = (args.source / relative).read_bytes().replace(b"\r\n", b"\n")
    windows_bytes = data.replace(b"\n", b"\r\n")
    expected = hashlib.sha256(windows_bytes).hexdigest()
    recorded = by_path[relative]
    if expected != recorded["sha256"] or len(windows_bytes) != recorded["bytes"]:
        raise SystemExit(f"Windows source differs beyond CRLF: {relative}")
    if item["anchor_lines"] != recorded["anchor_lines"]: raise SystemExit(f"Line anchors differ: {relative}")
    compared.append({"path": relative, "git_blob_sha256": item["git_blob_sha256"],
                     "lf_sha256": item["lf_sha256"], "windows_raw_sha256": expected,
                     "windows_raw_bytes": len(windows_bytes), "eol_only_difference": True})
(args.output / "source-references.json").write_text(json.dumps(local, indent=2) + "\n", encoding="utf-8")
(args.output / "artifact-download-verification.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
(args.output / "windows-source-comparison.json").write_text(json.dumps({"official_root": local["official_root"],
    "status": "PASS", "method": "local checkout equals pinned Git blob after CRLF normalization; re-expanded CRLF hashes and sizes equal all 37 Windows evidence entries; no source rewrite",
    "references": compared}, indent=2) + "\n", encoding="utf-8")
print("PASS artifact hashes/CRC/text allowlist, 26 checks and 37 Windows-source comparisons (CRLF accounted)")
