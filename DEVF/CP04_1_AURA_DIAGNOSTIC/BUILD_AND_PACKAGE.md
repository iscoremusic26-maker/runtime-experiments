# Windows y paquete CP04.1

Fuente nueva en feature/devf-cp04-1-aura-diagnostic, contra CP04 histórico080f8e4. CI privada ci/devf-cp04-1-aura-diagnostic, contra CI histórica4bea35d. Workflow nuevo devf-cp04-1-aura-diagnostic.yml, solamente PR del mismo repo privado/baseSHA exacto; workflows históricos intactos. actionscheckout/upload y MSVCsetup fijados a los SHAs del pipelineCP04. SDK40457c6, Aurora 3227d76 e importlibSHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4.

Comando de runner: python DEVF/CP04_1_AURA_DIAGNOSTIC/ci/run_windows.py --source .official --inputs . --work <RUNNER_TEMP>/cp04-1-aura-diagnostic. MSVC x64/Windows SDK, CMakeNinja Release; build propio devf_cp04_1_aura_diagnostic + cp04_1_visual_lab, package oficialSDK. Nunca host/juego/DLLload. CI comprueba dependencia/archivooriginalCP00 intactos, ledger propio, 14 casos, PEAMD64/ABI1/cincoexports/serviciosHostLogGameStageHook/únicoHookexecute/imports exactos, negativosPE y DLL internaequaloose. TEST privado separado de evidenciaTEXT sanitizada, retención30días. Ningún recurso original o binariohost se publica.

**BUILD_PASS / PACKAGE_VERIFIED / DOWNLOAD_VERIFIED** en [run 38593704059](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38593704059), MSVC 19.51.36260/SDK 10.0.26100.0/CMake 4.4.3. Fuente compilada`554c31a3e10906c50dd18a05fe0b55737bf5a3a8`; CI`da07f77fddd13ca1664997e5373f3dfe988cf7e1`. Un solo build verificable.

[TEST privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38593704059/artifacts/11908437726) y [TEXT privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38593704059/artifacts/11908358056). TESTvence13-11-2026,15:57:15 UTC (10:57:15 Panamá); TEXT15:57:13 UTC. Descarga verificadareal. Extraer del ZIP deActions:

`DEVF_CP04_1_AURA_DIAGNOSTIC_windows-amd64_554c31a3e10906c50dd18a05fe0b55737bf5a3a8.dusk`

- .dusk:16017 bytes, SHA256`da4aa72faa2148238c9e6ef879b372647c3c976fe57140d1a4484decd3109d60`.
- DLL interna:29696 bytes, SHA256`e6d91eaf93201dbede491084c869f2c3cae6aad2f299aca4d5040f4f357e7553`. No se entregaDLL suelta.
- ZIPTEST:17017 bytes / SHA256`c91d96f418e1ed097f22b93e0eb703e9f47d492c008f24bebd9974dcc55c2e47`.
- ZIPTEXT:30026 bytes / SHA256`906d2038478f1e72195761d888d6d282e899abc600c34ed6755831faa8d5a141`.

Contenidooficial:.dusk contiene mod.json,lib/,lib/windows-amd64/,mod.dll interno. ZIPTEST únicamenteese.dusk+DOWNLOAD_MANIFEST; TEXTsolo.log/.json propios sanitizados. Metadata módulo `dev.devf.cp04_native_aura`v0.4.1, DIAGNOSTIC_ONLY; originalCP03/CP04.dusk guardados íntegros fuera deGit.

```powershell
Get-FileHash -Algorithm SHA256 '.\DEVF_CP04_1_AURA_DIAGNOSTIC_windows-amd64_554c31a3e10906c50dd18a05fe0b55737bf5a3a8.dusk'
```

Para reproducir con acceso aGitHubprivado: checkoutCI`da07f77fddd13ca1664997e5373f3dfe988cf7e1`, SDKroot 40457c6 y Aurora 3227d76; abrirPRsobrebase CI 4bea35d como indica workflow. Ejecutar con MSVC x64 + SDK; los comandos concretos deCMake, cl/dumpbin y packaging están en evidence/windows-run-38593704059/result.json, con exitcodes/timing. No usar Linux, compilarhost o cargarDLL.

Auditor de descarga con ambos ZIPs:ci/verify_download.py --delivery TEST.zip --text TEXT.zip --work <SCRATCH> --delivery-sha256 c91d96f418e1ed097f22b93e0eb703e9f47d492c008f24bebd9974dcc55c2e47 --text-sha256 906d2038478f1e72195761d888d6d282e899abc600c34ed6755831faa8d5a141 --output <SCRATCH>/verification.json. Comprueba digestsGitHub, CRC, manifiestos/ledgers, PE y coincidenciaDLL. Los 18 archivospropios medidos en source ledger se conservan tras cierre documental; mismoIDimpide dosCP04activos, retirarCP03 sigue obligatorio. Se entrega un único DIAGNOSTIC_ONLYv0.4.1, nunca una variante especulativa. [HUMAN_TEST](HUMAN_TEST.md) exige instalación única y cierre total.
