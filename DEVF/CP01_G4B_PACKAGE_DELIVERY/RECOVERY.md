# Package recovery checkpoint

Main private repository iscoremusic26-maker/Mods-Duskligh. Branch **package/devf-cp01-g4b-observation**, exact base17bbbd288f2e17974303f98fbfcd3345f49aa11d. [Draft PR15](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/15), no merge/force push/tag replacement. New recovery tag **DEVF_CP01_G4B_OBSERVATION_PACKAGE_VERIFIED** points to the final reports/tools/text-evidence checkpoint; resolve the final commit using Git/tag or PR body. A self-referential commit hash is not embedded in the tagged tree. Prior observer checkpoint/tag remain untouched.

Native observer source checkpoint17bbbd2, equivalent compiled source9d4cba8; packaging-run source6c788fb7d0e1245c49af473c2ecca5dc1c7f417f. All original G4B and reused G2/A2/approved review files remain identical to SOURCE_APPROVAL.json; final additions are packaging inspection, the locally executed independent download checker, reports and text evidence. Checker hash and actual package-tool/observer source equality in evidence/source-match.json.

Inputs private branch **ci/devf-cp01-g4b-package**, head1069e2f2897b137c9ec791861eb862c832a3edcb, base7e95661bdf9f93de7ed5a532e1b37150e70fe30f on ci/devf-cp01-g4b-readonly. [Draft inputs PR9](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/9). Dedicated workflow .github/workflows/devf-cp01-g4b-package.yml corresponds to ci/windows.yml here. Pre-trigger isolation proof in evidence/ci-preflight.json; old workflows untouched and not triggered. Exactly one Windows run for this head: [38351128600](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600), attempt1, SUCCESS.

Official host source40457c6adb381928e4b5fef6ed459ed291edd5e2; Aurora3227d76c60e1e782ca576610bce61c9e7744d8be; selected CP00 import library9400986 bytes/SHA2564dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4. No host or original resource rebuilt/modified. Reproduction uses same guarded PR workflow, exact reviewed files and original SDK package target; see BUILD_AND_PROVENANCE.md.

## Recover the source/reports independently

```bash
git clone https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-g4b-package-recovery
git -C devf-g4b-package-recovery fetch origin refs/heads/package/devf-cp01-g4b-observation refs/tags/DEVF_CP01_G4B_OBSERVATION_PACKAGE_VERIFIED
git -C devf-g4b-package-recovery switch --detach DEVF_CP01_G4B_OBSERVATION_PACKAGE_VERIFIED
git -C devf-g4b-package-recovery merge-base --is-ancestor 17bbbd288f2e17974303f98fbfcd3345f49aa11d HEAD
git -C devf-g4b-package-recovery status --short
```

Final independent bare fetch, branch/tag/commit/blob comparison, fsck and unchanged-old-ref count are reported in PR15 body and delivery; they are performed after publishing the final tag. Text manifest hashes persist under evidence/TEXT_EVIDENCE_MANIFEST.json. The compiled observer snapshot is separately preserved by its prior tag/commit and exact approval ledger.

## Recover the private artifact before expiration

* [Package artifact11790942278](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600/artifacts/11790942278): actual outer ZIP21984 bytes, SHA256036812d6e6a5fb220d3714ec62c93f75962d671820d9a7510b61fb863c144977. Contains one .dusk plus DOWNLOAD_MANIFEST.json.
* Named .dusk `DEVF_CP01_G4B_READ_ONLY_windows-amd64_17bbbd288f2e17974303f98fbfcd3345f49aa11d.dusk`:20818 bytes, SHA25645822a197690e0995c30f1f42febd023db43f68154e3aab109a6070a995acc78.
* Internal DLL50688 bytes, SHA2562ac673d7e5980b8c7c9e62a3150097830b3be6b438600455fa67a022ea0f5006; no standalone DLL in artifact/Git.
* [Separate text artifact11790457787](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38351128600/artifacts/11790457787):97499 bytes, SHA256b5253dd6bf0998ab387caa5df14e41224d58ff8e90b460af77b1f53feec5d603, reproduced as text evidence in this checkpoint.

GitHub expiry for package2026-11-12T05:24:36Z =12November2026,00:24:36 Panama. No permanent download availability promised; preserve original downloaded package privately if reviewed before expiry. If expired, source/report recovery still works, but the exact binary is not stored in Git: a separately authorized reproduction must have new build/package/hash/download verification, never substitute the old hash automatically.

To repeat independent inspection of an actual authorized download:

```bash
python DEVF/CP01_G4B_PACKAGE_DELIVERY/ci/verify_download.py --archive <actual-actions-zip> --metadata <saved-artifact-metadata> --runner-evidence <downloaded-runner-text> --work <private-scratch>
```

Download only the exact artifact from the authorized private repo. Check GitHub digest/CRC, reopen inner package, retain exact manifest ID/version and repeat PE/import/export inspection; never install or load the extracted DLL. DLL hash differs from historical DLL by exactly two documented timestamps; see PACKAGE_VERIFICATION.md, including whole-file normalized historical-SHA equality proof.

## Stop boundary

G4B_PACKAGE_READY_FOR_USER_REVIEW only. No installation/game/DLL execution or hot reload. Runtime capture/owner/creation/render NOT_TESTED or NOT_VERIFIED; first test location blocked, G5/CP02 NO_GO, G6 NOT_VERIFIED, independent custom-DLL blocker unchanged. Next minimum step is a separate explicit authorization for the cold observation-only session documented in G4B_USER_OBSERVATION_PROCEDURE.md; do not begin it during recovery.
