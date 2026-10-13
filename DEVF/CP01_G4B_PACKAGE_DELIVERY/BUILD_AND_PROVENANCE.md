# Exact source, Windows build and official packaging

Approved observer checkpoint17bbbd288f2e17974303f98fbfcd3345f49aa11d, tagDEVF_CP01_G4B_LOCAL_READONLY_OBSERVER_VERIFIED; original equivalent compiled source9d4cba8f5e40377cf0746da6366160c147686cc8. Packaging-tools source6c788fb7d0e1245c49af473c2ecca5dc1c7f417f. Private CI head1069e2f2897b137c9ec791861eb862c832a3edcb, [draft inputs PR9](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/9). The independent download checker is additional source executed locally after the runner; its hash is in evidence/source-match.json. It is not an observer source/compile unit.

SOURCE_APPROVAL.json pins25 own/reused reviewed files and selected official SDK/packager files. Hash comparison checked them against approved main-source files and actual CI mirror before triggering, on the runner, and after download. G4B CMake/mod.json/src/tests/ci are unchanged; no second observer implementation is copied into this directory. Packaging-tools hashes also match actual executed CI sources. Final reports/checker/evidence do not change the native compilation graph.

Dependencies:

* Official TwilitRealm/dusklight40457c6adb381928e4b5fef6ed459ed291edd5e2 (v2.0.3), SDK only, no host target.
* Aurora3227d76c60e1e782ca576610bce61c9e7744d8be, headers only; no Aurora modification or other submodule build.
* Original CP00 import library9400986 bytes, SHA2564dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4; selected ZIP memberCRC70c35731. Full private ZIP56037777 bytes was available via LFS, and selected member integrity checked. CP00 original-archive audit reused, no game-resource reanalysis or EXE rebuild.
* Windows-latest imagewindows-2025-vs2026, MSVC19.51.36260.0 for x64, VS18 toolset14.51.36231, linker14.51.36260.0, Windows SDK10.0.26100.0, CMake4.4.3, Ninja. Actual commands/environment and logs preserved under evidence/runner/build-audit.

## CI isolation checked before PR creation

Base **ci/devf-cp01-g4b-readonly@7e95661bdf9f93de7ed5a532e1b37150e70fe30f**, headci/devf-cp01-g4b-package. Actual three-dot diff contains only new CP01_G4B_PACKAGE_DELIVERY files and .github/workflows/devf-cp01-g4b-package.yml. Old G2/A2/G4B workflow bytes remain identical; none of their path filters matches this diff. Existing workflows have no push or workflow_dispatch event. New PR trigger is limited to package paths and opened/synchronize/reopened; job also requires private same-repo PR, exact head/base branch names and pinned base SHA. Contents:read only; no new credential/permission. New workflow_dispatch is not available before default-branch integration, and no merge is authorized, so this guarded narrow PR event uses the proven capability.

Preflight evidence/ci-preflight.json preceded trigger. GitHub listed **only one run** for this CI head, the G4B observation-package workflow38351128600; no historical G2/A2/G4B standalone workflows were executed. The intended packaging workflow itself reuses G4B's validator to validate the newly built DLL, not a historical workflow trigger.

## Build -> audit -> package -> download

From a Windows x64 MSVC developer shell with pinned official SDK/Aurora and authorized private inputs, the dedicated CI entry is:

```powershell
python DEVF/CP01_G4B_PACKAGE_DELIVERY/ci/run_package.py --source .official --inputs . --work "$env:RUNNER_TEMP/g4b-readonly"
```

The entry deliberately verifies its guarded PR context/checkout provenance. For reproduction, use the same private PR workflow; do not edit observer guards or fake its provenance. It invokes the unchanged G4B run_windows.py, which configures Release/Ninja/cl, C++20, exact SDK/library, builds devf_g4b_readonly + existing two G4B labs, reuses92 checks,4 semantic mutants and6 compilation guards, dumps and audits the actual DLL. None of the old G2/A2 suites or SDK Linux build is repeated.

Thirteen new negative ZIP inspection fixtures are rejected: duplicate/case-alias, extra file, traversal, absolute/drive/backslash paths, symlink/special file, oversized member, nonempty directory, CRC corruption and encryption. Fixtures are in-memory test ZIPs, not installation packages. G4B lab fake code remains outside the native DLL.

Fresh DLL audit and historical-hash explanation must pass **before** this command:

```powershell
cmake --build <validated-build-dir> --target devf_g4b_readonly_package --parallel 2
```

Original official recipe cmake/ModSDK.cmake copies mod.json and audited target to lib/windows-amd64/mod.dll, creates standard directory entries and runs cmake -E tar --format=zip. The Windows path does not strip/change the DLL. Original EXCLUDE_FROM_ALL remainsTRUE; ordinary G4B lab workflow stays package-free. No alternative packager or extra resource/runtime-library argument used.

Runner package validation phase started13October2026,00:24:05 America/Panama, ended00:24:34 (UTC source records05:24:05.015152–05:24:34.972654Z). Per-command timing is in package-result.json/build-audit/result.json. New PE timestamps and ZIP timestamps mean a later build need not have the same raw file hash; every produced delivery must receive its own audit and explicit hash comparison. This task explains the actual timestamp-only DLL difference and delivers the unmodified new DLL.

Independent second-stage command (read/inspect only):

```bash
python DEVF/CP01_G4B_PACKAGE_DELIVERY/ci/verify_download.py --archive <actual-actions-download.zip> --metadata <github-artifact-metadata.json> --runner-evidence <downloaded-text-evidence> --work <private-audit-scratch>
```

It compares GitHub outer digest/size/provenance, manifest byte identity and runner package/DLL hashes, repeats ZIP/PE/metadata/import/export inspection and historical-timestamp proof. Native extraction only to scratch, never game folders. No game execution, DLL load, install or hot reload occurred.
