# CP04.3 — Verified offline delivery

Source compiled:1cd0f30eb3c49e2ac2cebb00cc660cc4b487f084. CI:b58e6f513ef671971240d1f1f782d06e124c798d. [run38638241539](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38638241539), nativejob116106826966 / independentjob116107792723: both SUCCESS.

MSVCx64 VCTools14.51.36231 / WindowsSDK10.0.26100.0, Ninja Release. Actual cl/Bv output is compiler.log in verified TEXT; do not infer exact compiler patch version from VCTools directory. Commands/configuration/version and durations are in TEXT result.json and phase logs. Native phase excerpt is preserved in evidence/windows-success-phases.log. Official SDK40457 and Aurora3227 pins, full original private ZIP/library size/SHA/CRC checks precede build. SDK/host not built or modified, no Linux substitute, no game/DLL loading.

CMake production target devf_cp04_3_private_scent_marker: exactly mod.cpp + officialSDK game_feature.cpp; lab support JSUPtrLink fake constructors/destructor only in tests, not product.19 focalized TEST_FAKE cases pass, registration rollback old certificate reused. Four PE negative mutations failclosed, AMD64/ABI1/seven metadata records/fiveexports/typed execute PMF bound exact execute import;38 exact imports (15game+23CRT), same reviewed surface as functionalCP04. No graphics global hooks/manualdetours/custom profile callbacks.

Official SDK package DEVF_CP04_3_PRIVATE_SCENT_MARKER_windows-amd64_1cd0f30eb3c49e2ac2cebb00cc660cc4b487f084.dusk:
- .dusk 17280bytes, SHA256 097a428edf39411a7caf9e31c738f66948832fdadec6bf0ee6162b5200ef868e.
- Internal DLL 31744bytes, SHA256 bbb7779149fca7b5a54838031c42488a1f30f937676ec35acd7a86f3dd9b5981; matches loose DLL byteexactly, PE audited again after download.
- TEST ZIP18334bytes, SHA256 60fc238129d513a26258295e075fe1e8c478a768c61e6ccd6e1dde49ff98f386; only own .dusk+DOWNLOAD_MANIFEST.json.
- TEXT ZIP32362bytes, SHA256 bdcecabec0511ad843100441054f7baaf9802905d24fcbe8f652076b0732e58a; own sanitized .log/.json, no original resources/binaries/personal logs.

[TEST11928548467](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38638241539/artifacts/11928548467), [TEXT11928194657](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38638241539/artifacts/11928194657), [independent proof11929482263](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38638241539/artifacts/11929482263). TEST expires2026-11-13 16:13:03 Panama(UTC-5),21:13:03UTC; TEXT two seconds earlier; proof16:13:28Panama.

Independent fresh Windows job downloaded real compressed TEST/TEXT ZIPs from GitHub after upload. It verified GitHub digests, outer/member CRC/SHA/size, text member ledger, delivery manifest match, source/workflow provenance, compiled source ledger, official package shape and byteexact DLL/PE. Token used only API request, signed redirect retrieved with separate unauthenticated request and neither token nor signedURL stored. Cloud remained unavailable; no claim of local Cloud download/fsck. See evidence/download-verification.json.

First run38637671361 failed only lab LNK2019/1120 missing JSUPtrLink ctor/dtor; production link already succeeded, no TEST emitted. Corrected lab-only support (abort on native list membership) and LF checkout for independent verification; second run justified by affected changes. No prior CP01–03 suites or research repeated. Runtime appearance/cleanup/performance NOT_TESTED.
