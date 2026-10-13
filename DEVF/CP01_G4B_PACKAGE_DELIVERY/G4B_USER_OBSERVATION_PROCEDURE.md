# G4B user review and future observation procedure

**Current authorization ends at private package delivery/review. Do not install, launch Dusklight, load this DLL or collect a runtime capture yet.** Installation and observation require separate explicit authorization. No instruction below is executed automatically. Windows/Dusklight2.0.3/DX12 availability and the prior observed Hyrule Field context are retained; no general setup or geometry investigation is required again.

## Package identity and download/review

Download with the GitHub account authorized for the private inputs repository:

[Actual G4B artifact11790942278](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600/artifacts/11790942278).

GitHub reports expiration12November2026,00:24:36 Panama (UTC−5); availability is not permanent. Extract only the **outer Actions ZIP** to an ordinary review/download folder, not a game/mod folder. Keep the .dusk intact as a file; do not extract/install its internal DLL manually. Outer ZIP contains the following .dusk and DOWNLOAD_MANIFEST.json, no installer.

* Filename: `DEVF_CP01_G4B_READ_ONLY_windows-amd64_17bbbd288f2e17974303f98fbfcd3345f49aa11d.dusk`
* Size20818 bytes; SHA256 `45822a197690e0995c30f1f42febd023db43f68154e3aab109a6070a995acc78`.
* ID `dev.devf.g4b_local_readonly`; version `0.0.1`; name `DEVF CP01 G4-B local READ_ONLY observer`.
* Internal DLL50688 bytes; SHA256 `2ac673d7e5980b8c7c9e62a3150097830b3be6b438600455fa67a022ea0f5006`.

Read-only PowerShell checks, without assuming a personal path:

```powershell
$g4bPackagePath = Read-Host 'Ruta real al .dusk descargado, fuera de las carpetas del juego'
$g4bPackageHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $g4bPackagePath).Hash
$g4bPackageBytes = (Get-Item -LiteralPath $g4bPackagePath).Length
if ($g4bPackageHash -ne '45822a197690e0995c30f1f42febd023db43f68154e3aab109a6070a995acc78' -or $g4bPackageBytes -ne 20818) {
    throw 'Identidad del paquete distinta: detener la revisión y conservar el archivo.'
}
$g4bHostPath = Read-Host 'Ruta real al dusklight.exe oficial existente'
$g4bHostHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $g4bHostPath).Hash
$g4bHostBytes = (Get-Item -LiteralPath $g4bHostPath).Length
if ($g4bHostHash -ne 'ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049' -or $g4bHostBytes -ne 52309504) {
    throw 'Ejecutable distinto del CP00 oficial: detenerse; no reemplazarlo ni parchearlo.'
}
```

These commands hash local files only. Match DOWNLOAD_MANIFEST.json to package version, source, new DLL hash and runtime/authorization flags; do not substitute an old G2 package or the historical G4B DLL hash.

## Preparation only after separate installation/observation authorization

1. Preserve the current installation state and existing mods/list/settings. Identify the real configured data folder, save/card/GCI storage, autosaves, configuration and package-search locations; do not invent C:\ paths. In a separately authorized future host session, official Settings -> Data Folder -> Open Data Folder and Saves -> Open Save Folder identify them; do not use Change Data Folder, Replace/Import saves or Uninstall. Opening the game to inspect these settings is not authorized by this delivery task.
2. Close the game fully. Copy existing saves/autosaves, configuration/data as appropriate, package list and mods to a separate backup without overwriting other backups. Record the storage mode and original configuration. The game/loader may write ordinary config/log/cache/autosave data; the observer's read-only nature does not make a game session write-free.
3. Plan an isolated official2.0.3/DX12 session: preserve but exclude conflicting actor/spawn/scene/layer/ABI/enemy-resource/hook mods and other experimental DEVF modules through official settings while respecting the agreed cold-session plan. Do not delete packages or overwrite their configuration blindly. If isolation cannot be established, stop before installation/startup.
4. With the game fully closed, copy only the reviewed .dusk to **one** previously identified official mod-search directory. Loader paths are configuration-dependent (ConfigPath/mods or --mods override, and application-adjacent mods as documented in prior G2 procedure). Do not extract DLL, copy to res/ROM/save or replace EXE/SDK. If the filename or ID already exists in any searched folder, stop and preserve both copies; do not overwrite or load duplicate IDs. No hot reload or install/uninstall while the process runs.

## Future limited observation

5. Start a cold process with the verified original EXE and ordinary DX12 configuration. Confirm module ID/name/version and successful service/epoch binding, with no other active DEVF test. Do not change ABI checks/runtime or add hooks to remedy load failure.
6. Reach the previously observed **F_SP121 / room3 / logical6** before the Kakariko bridge through normal play from an existing suitable state. No teleport, forced layer, story/flags/save editing, actor request, roomReLoader or enemy creation. If the existing state does not naturally supply logical6, record that limitation and stop; do not progress the story to satisfy a numeric requirement.
7. Diagnostics are at most16 slots, one every120 mod_update calls, **updates rather than seconds**. Slots are consumed even for rejected/incomplete contexts; they may run out before reaching the room. Plan around an existing suitable save/context under the later authorization. Do not create/edit a save, extend the code budget, reactivate or hot reload to compensate. If no useful valid-context capture remains, preserve what happened and review the session plan before another attempt; this task promises no timing/runtime performance.
8. Keep the observation brief, stable and free of event/transition/combats when possible, without moving other actors or altering AI/progress. C is only the observer's fixed query point, **not an approved spawn location**. No request to stand on C or use center distance as physical clearance. End after the agreed brief sample or exhaustion.

## Records to preserve privately

Keep full `G4B DISARMED_NO_REGISTRATION id=...` lines with their timestamps and capture IDs, plus module-load/service errors and a short note of route/context/DX12 and conflicting-mod isolation. Official module Logs -> Copy or the actual configured log folder provides output; do not assume a personal log path. Preserve the original log privately and make a reviewed anonymous copy if requested. Do not share saves, original assets, personal paths, tokens or full unrelated log contents.

A record correlates host/build, stage/room/logical layer, room/play IDs/profiles/init and owner/binding/counters/status2e, context/event signals, support/water-group surface, moving BG candidate AABBs and owner matches, Link/local actor positions/distances and registered resources. See inherited LOCAL_CAPTURE_SCHEMA.md for numeric enums. Engine layer IDs are observed, not required to equal5/6; actor room and process owner are different concepts.

`stable=0`, `session=0/2`, `valid=0`, truncation flags, incomplete census/process, unknown owner/index/room, unavailable/invalid surface or `CAPTURE_INCOMPLETE=LOG_TRUNCATION` prevent favorable interpretation. Keep rejected captures; do not combine different IDs/instants to fabricate completeness. Even `valid=1` is basic scalar coherence, not location admission. `no_location_admission=1`, `READY=NOT_VERIFIED`, `water_volume=UNAVAILABLE_WITH_SAFE_API`, `bg_exact=UNAVAILABLE_WITH_SAFE_API` and physical-overlap uncertainty remain. A water-group no-hit, AABB or far actor center never proves universal absence/clearance.

## Stop and recover

Stop the future session immediately on crash, freeze, module-load/version/epoch failure, abnormal performance, render/Link visibility problems, incompatible scene/event/transition, persistent invalid/incomplete data, C++ exception/error, unexpected actors or progression changes. Preserve logs/notes; do not fix by warping, flags, deleting an actor, loading resources, hot reload or loosening checks. A legitimate difference between owner IDs alone is not corruption.

Exit/close the game completely before removing only the newly copied observer file from the identified mod folder. Do not rely on unloading a DLL while the game continues. Preserve other packages and restore configuration intentionally from the recorded state; do not automatically overwrite saves/backups. **Closing the process or removing the observer does not revert an autosave or other saved progress.** Review any unexpected state against backups before deciding recovery actions. A recovery relaunch or save restoration also follows the later agreed authorization, not this delivery task.
