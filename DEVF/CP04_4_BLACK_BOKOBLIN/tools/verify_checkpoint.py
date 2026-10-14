"""CP04.4 source provenance and immutable recovery verifier. No game execution."""
import argparse
import concurrent.futures
import hashlib
import json
import platform
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f"
ROOT = "DEVF/CP04_4_BLACK_BOKOBLIN/"
WORKFLOW = ".github/workflows/devf-cp04-4-recovery-tag.yml"
HERE = Path(__file__).resolve().parents[1]
PINS = {
    "TwilitRealm/dusklight": "40457c6adb381928e4b5fef6ed459ed291edd5e2",
    "TwilitRealm/dusklight-cosmetics": "fd93491089fa95441789244f2b2fd22a451ecbcc",
    "encounter/aurora": "3227d76c60e1e782ca576610bce61c9e7744d8be",
}

def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, encoding="utf-8").stdout.strip()

def verify_git():
    git("merge-base", "--is-ancestor", BASE, "HEAD")
    changed = git("diff", "--name-status", BASE, "HEAD").splitlines()
    paths = []
    for row in changed:
        status, path = row.split("\t", 1)
        if status != "A" or not (path.startswith(ROOT) or path == WORKFLOW):
            raise RuntimeError("Change outside the new CP04.4 scope")
        if path.lower().endswith((".arc", ".dusk", ".dll", ".exe", ".bmd", ".bdl", ".iso", ".jpc", ".zip")):
            raise RuntimeError("Original resource or binary in CP04.4 diff")
        paths.append(path)
    prior = json.loads((HERE / "evidence/previous-refs.json").read_text(encoding="utf-8"))
    remote = {}
    for row in git("ls-remote", "--heads", "--tags", "origin").splitlines():
        sha, ref = row.split("\t")
        if not ref.endswith("^{}"):
            remote[ref] = sha
    for item in prior:
        if remote.get(item["ref"]) != item["sha"]:
            raise RuntimeError("Previously existing ref changed; stop without overwriting")
    git("fsck", "--full")
    return {
        "status": "PASS_STATIC",
        "base": BASE,
        "head": git("rev-parse", "HEAD"),
        "unchanged_baseline_paths": len(git("ls-tree", "-r", "--name-only", BASE).splitlines()),
        "previous_refs_preserved": len(prior),
        "added_paths": paths,
        "git_version": git("--version"),
    }

def verify_source(item):
    repo, commit, path = item["repository"], item["commit"], item["path"]
    if PINS.get(repo) != commit or path.startswith("/") or ".." in path.split("/"):
        raise RuntimeError("Unpinned or invalid source")
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{urllib.parse.quote(path, safe='/')}"
    request = urllib.request.Request(url, headers={"User-Agent": "DEVF-CP04.4-provenance"})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read(3 * 1024 * 1024 + 1)
    if len(data) > 3 * 1024 * 1024:
        raise RuntimeError("Source exceeds provenance limit")
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if blob != item["git_blob_sha"]:
        raise RuntimeError("Exact source Git blob mismatch: " + path)
    lines = len(data.decode("utf-8").split("\n"))
    for first, last in item["line_ranges"]:
        if not 1 <= first <= last <= lines:
            raise RuntimeError("Invalid source citation range")
    return {
        "repository": repo, "commit": commit, "path": path,
        "git_blob_sha": blob, "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data), "citation_ranges_valid": True,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--git-only", action="store_true", help="Seal follow-up docs; do not repeat source download")
    args = parser.parse_args()
    started = time.monotonic()
    report = {
        "schema": 1, "scope": "git/source provenance only; not MSVC, isolation or GPU proof",
        "python": sys.version.split()[0], "platform": platform.platform(),
        "git": verify_git(),
    }
    if not args.git_only:
        inventory = json.loads((HERE / "evidence/source-inventory.json").read_text(encoding="utf-8"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            report["sources"] = list(pool.map(verify_source, inventory["sources"]))
        report["source_status"] = "PASS_STATIC"
    else:
        report["source_status"] = "NOT_REPEATED"
    report["elapsed_seconds"] = round(time.monotonic() - started, 3)
    print("CP044_STATIC_RESULT=" + json.dumps(report, sort_keys=True))
    print("CP044_GIT_PROVENANCE_PASS; RUNTIME_NOT_TESTED; NO_DUSK_GENERATED")

if __name__ == "__main__":
    main()
