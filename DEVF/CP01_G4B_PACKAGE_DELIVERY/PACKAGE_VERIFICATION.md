# G4B observation package: verified private delivery

**G4B_PACKAGE_READY_FOR_USER_REVIEW. Installation and execution are not authorized by this checkpoint.** Native module is READ_ONLY / DISARMED_NO_REGISTRATION; runtime is NOT_TESTED. This is an actual SDK-generated package, not a renamed hand-built ZIP.

Private [package artifact11790942278](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600/artifacts/11790942278), [Windows run38351128600](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600), attempt1, SUCCESS. URLs are actual download links reported by GitHub upload step logs; access requires the repository's authorized GitHub account. Expiration reported by GitHub: **12November2026,00:24:36 America/Panama (UTC−5)**, equivalent2026-11-12T05:24:36Z. Availability is not permanent; deletion or repository policy may end it earlier.

Filename:

`DEVF_CP01_G4B_READ_ONLY_windows-amd64_17bbbd288f2e17974303f98fbfcd3345f49aa11d.dusk`

| Object | Bytes | SHA256 |
|---|---:|---|
| Actual `.dusk` |20818|`45822a197690e0995c30f1f42febd023db43f68154e3aab109a6070a995acc78`|
| Internal `lib/windows-amd64/mod.dll` |50688|`2ac673d7e5980b8c7c9e62a3150097830b3be6b438600455fa67a022ea0f5006`|
| Outer Actions download ZIP |21984|`036812d6e6a5fb220d3714ec62c93f75962d671820d9a7510b61fb863c144977`|
| Packaged `mod.json` |268|`70e96371ac93206509732839e77e56936b52867cce66f146db06f2f27859dc2f`|

## Complete inner structure

Exactly two functional files and two SDK directory entries:

```text
mod.json
lib/
lib/windows-amd64/
lib/windows-amd64/mod.dll
```

Manifest is byte-identical to the approved G4B mod.json, with only id/name/version/description:

```json
{"id":"dev.devf.g4b_local_readonly","name":"DEVF CP01 G4-B local READ_ONLY observer","version":"0.0.1","description":"DISARMED_NO_REGISTRATION. Bounded local C observations only; partial safe API coverage; no actors, hooks, setters or install/runtime authorization."}
```

File CRC32 values: manifest3429485d; DLL6237e38d; directory entries00000000. All member CRC, SHA256 and sizes verified on runner and again after real artifact download. No duplicate/case-alias entries, encryption, symlink/special file, absolute/drive/traversal/backslash/noncanonical path or extra files. No EXE, host DLL, original resources, import library, saves, private logs, lab binaries, debug files or install script. Outer artifact contains only the named .dusk and external DOWNLOAD_MANIFEST.json; the external manifest is not embedded in the .dusk.

## Same-run identity and second inspection

1. Approved source hashes were checked before native build; original G4B/G2/A2 and SDK sources remained unchanged.
2. New loose DLL passed the existing exact G4B audit and exports inspection, eight-unit compile/map graph, labs and guards. Native hash was recorded before packaging.
3. Only then the official `devf_g4b_readonly_package` target ran; it did not rebuild/change the loose DLL.
4. DLL extracted from runner package was compared **byte-for-byte** and by SHA256 with that audited loose DLL. PE metadata/imports/exports were repeated on the extracted copy.
5. GitHub private artifact was actually downloaded into Codex scratch. Outer size/GitHub digest, exact members and CRC were checked. .dusk/DLL hashes and sizes were recalculated, manifest byte identity checked, full PE/import/export audit repeated, and historical-timestamp analysis repeated on downloaded DLL. These match the same-run package and runner record. No DLL was loaded or executed; scratch extraction was not installation.

Evidence: `evidence/runner/package-result.json`, `package-verification.json`, `DOWNLOAD_MANIFEST.json`; `evidence/download-verification.json`, `actions-artifacts.json`, `delivery-links.json`, `source-match.json`. Separate [text artifact11790457787](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600/artifacts/11790457787) was also downloaded:97499 bytes, SHA256b5253dd6bf0998ab387caa5df14e41224d58ff8e90b460af77b1f53feec5d603, all CRC passed. Texts are preserved in Git without native binaries.

## Historical DLL hash difference explained

Prior DLL SHA256d5693c904b0706a04d37ca4eac7403cbb14a4bdccf3fd37650c058de94296fde is **not** the new DLL hash. New size is still50688 bytes. The precise changes are COFF.TimeDateStamp at file offset264 and Debug[0].TimeDateStamp at37700: new1791869065, historical1791867502. Replacing just these two documented timestamp fields in a temporary in-memory copy reproduces the **exact historical whole-file SHA256**. Thus all bytes outside those timestamp fields match the prior DLL; no unexplained code/ABI difference is inferred harmless. Same proof succeeded independently on downloaded DLL. Actual build, package and delivered DLL were never normalized/rewritten.

## Results

| Requirement | Result |
|---|---|
| Exact native Windows build/link |G4B_PACKAGE_MSVC_BUILD_PASS|
| Fresh loose/internal/downloaded DLL audit |G4B_PACKAGE_DLL_AUDIT_PASS|
| Official SDK package structure/integrity |G4B_PACKAGE_STRUCTURE_PASS|
| Actual private download independently reopened |G4B_PACKAGE_DOWNLOAD_VERIFIED|
| Package for private user review |G4B_PACKAGE_READY_FOR_USER_REVIEW|

No result here is a game/DX12 execution PASS or admission of C. ZIP and SHA identity establish delivery integrity, not runtime medium/collision/lifetime validation.
