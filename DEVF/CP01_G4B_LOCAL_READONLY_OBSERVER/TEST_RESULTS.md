# Targeted Windows validation

Final [CI run38348951106](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38348951106), attempt1, SUCCESS. Private inputs draft[PR8](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/8), base ci/devf-cp01-a2-disarmed. CI head7e95661bdf9f93de7ed5a532e1b37150e70fe30f mirrors own source **9d4cba8f5e40377cf0746da6366160c147686cc8**. Final documentary checkpoint changes no tested implementation/lab/CI files. Exact own/reused source ledgers were checked against recovered CI text and final local files; see evidence/mirror-check.json and binary-call-review.json.

Toolchain: windows-latest x64, MSVC19.51.36260.0, linker14.51.36260.0, VS18 Enterprise toolset14.51.36231; Windows SDK10.0.26100.0, CMake4.4.3, Ninja. SDK source40457c6adb381928e4b5fef6ed459ed291edd5e2, Aurora3227d76c60e1e782ca576610bce61c9e7744d8be. Selected exact CP00 import library9400986 bytes, SHA2564dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4, memberCRC32=70c35731. Original archive integrity reused; no ARC/resource re-analysis or host build. Official tracked source remained unchanged.

| Check | Result | Evidence |
|---|---|---|
| New scalar/context/medium/occupancy capture lab | PASS50 checks /0FAIL | capture-lab.log |
| Actual lifecycle with fake capture/log, cadence/budget/reentry | PASS31 /0FAIL | adapter-lab.log |
| Capture C++ exception, fail-closed budget | PASS5 /0FAIL | capture-error.log |
| Log C++ exception, fail-closed budget | PASS6 /0FAIL | log-error.log |
| Three occupancy/context/ID mutants plus unavailable-water mutant | PASS4/4 compiled mutants killed | mutation build/test logs; result.json |
| Permanent read-only configuration | PASS1 valid build and5 negative guard builds rejected | guard-*.log |
| New native observer compile/link vs exact SDK/import library | PASS | configure.log, build.log, compiler.log |
| Eight native compile units, no lab backend or historical controller/request path in map | PASS_STATIC | compile-commands.json, module-map.log, binary-call-review.json |
| PE AMD64, ABI1, only Host2.2/Log1/Game2, exact30 decorated host imports plus reviewed CRT/system imports, five exports | PASS_STATIC | result.json, module-imports/exports/headers.log |
| Entry/virtual call source + disassembly review | PASS_STATIC | binary-call-review.json, module-disassembly.log; READ_API_CONTRACTS.md |
| Runtime ground/water/BG/Link/event/resources or actual owner lifetime | NOT_TESTED / NOT_VERIFIED | no game execution |
| Spawn/render/collision/cleanup/DX12 | NOT_TESTED | no package, activation or host execution |

Total **92 successful checks** in the new labs, including repeated bounded line assertions; these are not92 independent game tests. No previous99-check A2 suite is included in this total. Four mutants each return test exit1 after successful compilation. Negative compile guards return2 as expected. Query API safety derives from exact official source review and native compile/link, not fake proof of host geometry.

Native DLL SHA256 **d5693c904b0706a04d37ca4eac7403cbb14a4bdccf3fd37650c058de94296fde**,50688 bytes. Lab EXE hashes/bytes in result.json. This hash was computed/audited on the runner for the final DLL; binaries were not downloaded or distributed. It is not the historical A2/G2 DLL hash. No .dusk target built by G4B.

Final runner validation phase began2026-10-13T04:57:59.625233Z, ended04:58:34.015450Z; per-command durations and actual compiler commands are in result.json. Minimal reproduction from an MSVC x64 developer shell with exact SDK/Aurora checkout and authorized private input ZIP:

```powershell
python DEVF/CP01_G4B_LOCAL_READONLY_OBSERVER/ci/run_windows.py --source <official-v203> --inputs <private-inputs> --work <ephemeral-work>
```

Runner configures Release with Ninja/cl, DUSK_SOURCE and DUSK_GAME_EXE pointing to exact extracted **import library**, builds only devf_g4b_readonly/g4b_capture_lab/g4b_adapter_lab, executes the four lab modes, four mutants and six compile guards, then dumpbin headers/imports/exports/disasm and source/PE checks. SDK *_package target is explicitly excluded and never invoked. Runner/API uploads text only; do not interpret build binaries as installation deliverables. windows-latest is a moving image; record actual versions on reproduction, and re-review any different native import surface.

## Failed iterations retained in Git/CI history

| Run | Finding | Correction |
|---|---|---|
|38348059115|Own namespace/type and missing resolver declaration compile errors|Qualified Id/include only, no official source edit|
|38348243381|Official deleting-message API accepts non-const layer pointer|Use the actual non-const lookup result, with read-only callee already reviewed|
|38348387229|DLL/labs passed; expected import bases did not match inline vs exported SDK methods|Review actual base constructors/dtor, SetObj, exported Bgsp and exact signatures|
|38348720363 /38348827258|Exact import-list preparation included dumpbin section-summary rows|Remove non-symbol summary rows, retaining exact decorated imports; add independent Link copy and retest final source|
|38348951106|Final code/tests/import auditor|SUCCESS|

No binary PASS from a failed/earlier run is reused. See SAFETY_AUDIT.md for unintended historical workflow trigger/cancellation403; those outputs are outside this evidence set.

Final text artifact11790120981,85559 bytes, GitHub digest SHA256a8a759a15e0f97bf9befc6bf94711fb475d136a048351050486e8ead9e74f786. Downloaded digest/size verified, ZIP CRC passed all members; contains only .log/.json. Evidence persisted in this source checkpoint; GitHub ephemeral artifact expires2026-11-12. TEXT_EVIDENCE_MANIFEST.json hashes every persisted evidence file. Original game archives, import library, private G2 user log and native binaries are excluded.
