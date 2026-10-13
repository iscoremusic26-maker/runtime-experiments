# Recovery checkpoint

Main private repository iscoremusic26-maker/Mods-Duskligh. Independent branch **implementation/devf-cp01-g4b-readonly**, base8911403f2432b7117fa9e6009d809a5c3501cd7c, draft[PR14](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/14), no merge or force push. Recovery tag **DEVF_CP01_G4B_LOCAL_READONLY_OBSERVER_VERIFIED** points to the documentary/evidence checkpoint preserving all implementation corrections. Resolve its commit via Git; a self-referential hash is intentionally not embedded in the tagged tree. Exact final checkpoint/ref verification will be in the PR body and user delivery.

**Compiled own source commit:**9d4cba8f5e40377cf0746da6366160c147686cc8. All production/test/CI sources in the recovery tag must retain matching SHA256 ledgers in evidence/result.json. Later checkpoint changes are reports/derived text evidence only. Source-authoritative host40457c6adb381928e4b5fef6ed459ed291edd5e2, Aurora3227d76c60e1e782ca576610bce61c9e7744d8be; no experimental host patch applied. Historical G2 and A2 sources remain byte-identical to the inherited checkpoint.

Private inputs CI branch **ci/devf-cp01-g4b-readonly**, head7e95661bdf9f93de7ed5a532e1b37150e70fe30f, base6ba5533ec4d32f0c7c3735481d300544a50a92f9; draft[PR8](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/8). Source provenance CI_SOURCE.json. Final [Windows run38348951106](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38348951106) PASS; artifact11790120981 is text-only and preserved under evidence. Original ZIP stays only in private inputs; no library/originals/binaries in main.

```bash
git clone https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-recovery
git -C devf-recovery fetch origin refs/heads/implementation/devf-cp01-g4b-readonly refs/tags/DEVF_CP01_G4B_LOCAL_READONLY_OBSERVER_VERIFIED
git -C devf-recovery switch --detach DEVF_CP01_G4B_LOCAL_READONLY_OBSERVER_VERIFIED
git -C devf-recovery merge-base --is-ancestor 8911403f2432b7117fa9e6009d809a5c3501cd7c HEAD
git -C devf-recovery status --short
```

Use independently cloned official SDK/Aurora at exact commits and the same authorized private CP00 ZIP/library for reproduction; follow TEST_RESULTS.md. Only new G4B targets, not the historic SDKLinux example or old suites. Do not build *_package, run DLL/host, install, generate .dusk or touch saves on recovery.

Manifest evidence/TEXT_EVIDENCE_MANIFEST.json records SHA256 and sizes; actual artifact ZIP digest and all member CRC verified on download. Evidence/mirror-check.json checks24 own/reused implementation/CI files equal to CI source, binary-call-review.json ties imports/map/disassembly to final DLL hash. Source and SDK provenance plus tool versions/commands/durations are in result.json. Files are scalar own analysis and newly built observer text audit only; no user's private raw logs.

**Next minimum step:** obtain distinct authorization for packaging and a cold observation-only runtime session with unchanged official host. Then gather the actual correlated evidence the observer safely supports and explicitly retain unsupported physical/water-volume uncertainty. No native spawn authorization, hot reload, G5/G6/CP02 or re-audit of the independent custom-DLL blocker follows from this checkpoint.
