# Safety review of the actual delivered package

The approved observer sources, CMake and manifest remain unchanged; packaging code is outside the native module graph. The fresh build reproduces all non-timestamp bytes of the historically audited DLL, and independently passes exact current G4B source/PE checks. Package/download checks operate on scratch data, never load the DLL or call the game.

## DLL inspected in three forms

Fresh loose Windows DLL, same-run SDK-packaged DLL and DLL extracted from actual private Actions download all have SHA2562ac673d7e5980b8c7c9e62a3150097830b3be6b438600455fa67a022ea0f5006,50688 bytes. Runner establishes byte-for-byte loose/internal equality; independent download matches entire package hash and DLL hash, then repeats full PE audit/exports and historical-timestamp proof. No normalization or patch is applied to the delivered DLL. See PACKAGE_VERIFICATION.md for precise differences from the earlier DLL.

* PE32+ AMD64, official ABI1 metadata.
* Exactly HostService2.2, LogService1.0 and GameService2.0 required imports; four metadata records total, no optional service/hook/export-service record.
* Exactly30 reviewed decorated dusklight.exe imports and unchanged reviewed CRT/system imports, checked against original G4B ci/reviewed-imports.json.
* Exactly five exports: mod_ctx, mod_meta, mod_initialize, mod_update, mod_shutdown. No additional ordinal-only or forwarded export.
* Eight production compile units: unchanged four G4B sources, historical G2 core.cpp, A2 controller_core.cpp/room_owner_resolver.cpp, original SDK game_feature.cpp. No lab/fake source in native DLL or Controller/fake/request backend symbol in map.
* Fresh compiler logs, imports/exports/headers, linker map and disassembly preserved. Whole-file timestamp-normalized equality to historical SHA also proves code bytes and approved call paths remain identical.

## Read paths and permanent desarme

Source and exact IAT preserve the explicitly qualified **cBgS::GroundCross**. No dBgS DEBUG GroundCross wrapper or SphChk. Read-API contracts are inherited unchanged from CP01_G4B_LOCAL_READONLY_OBSERVER/READ_API_CONTRACTS.md; this task neither reopens geometry analysis nor fills its partial coverage. SetObj/SetPos imports write only caller-owned query objects, not actors/gameplay. LogService is the bounded diagnostic output path, no own DLL file writer/worker.

No ActorService/StageService/HookService, create/register/delete/request backend, layer setter, HIO/save/flag/scene/resource/BG write, forced load/reload, teleport, hook/detour/host patch or arming configuration. No persistent native loans or own deferred callbacks. Six compile guards preserve permanent READ_ONLY/DISARMED definitions. Budget remains16 diagnostic slots/cadence120 updates; reentry is blocked and exception exhausts the budget. Shutdown/reinitialization in the same loaded image cannot reset it. No telemetry option or additional runtime control is added.

Manifest IDdev.devf.g4b_local_readonly, version0.0.1. Original manifest is byte-identical; no second manifest/options/version bump. Package contains only manifest + G4B native module (standard directories aside), no other mods, original assets, EXE/library, user logs, saves, debug/lab binaries or installer. Outer artifact adds only external DOWNLOAD_MANIFEST.json, explicitly READ_ONLY/DISARMED/RUNTIME_NOT_TESTED and installation/execution_authorized=false.

## Scope boundaries preserved

The package is ready **for private review only**. MSVC/package/ZIP/PE PASS does not establish runtime capture, Link/actor overlap, water volume, render, collision, owner lifetime, location admission or DX12 behavior. G4B safe coverage remains partial; first location blocked, G5/CP02 NO_GO, G6 NOT_VERIFIED. Independent custom-profile DLL unloading blocker remains BLOCKED and was not reinvestigated. A future procedure uses cold start and full process exit, without representing dynamic DLL unloading as safe or process exit as save rollback.

No original host/SDK/Aurora/game resource was modified or built. Original .lib stays only in private ephemeral runner; .dusk is not committed to any Git repository. Artifact is private and expires. No game launch, DLL loading, installation, runtime capture or save/progress change was performed. Main PR remains draft without merge; old branches/tags preserved.

CI isolation preflight proves historical workflows unchanged and nonmatching. GitHub confirmed only the new package run for head1069e2f; no fallback to a risky default main-base PR and no reliance on cancellation. The prior G2 artifact is not used as this delivery.
