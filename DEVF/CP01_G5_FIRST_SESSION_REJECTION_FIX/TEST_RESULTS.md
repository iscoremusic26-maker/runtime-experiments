# Evidencia de pruebas y fallos conservados

## Ejecuciones Windows reales

| Run / job | Resultado y causa | Evidencia |
|---|---|---|
| 38444298710 | SKIPPED: filtro base_ref propio incorrecto; ningún build | skipped-ci-run.json |
| 38444485831 / 115459196190 | FAIL: headers propios duplicados C2086/C2374/C2011, luego tipos incompletos por cascada | windows-run-38444485831; artifact 11836564862 |
| 38445082050 / 115461238858 | Compile/link PASS, 100 checks PASS, 8 mutantes compilados/killed; FAIL posterior al comparar la whitelist antigua completa | windows-run-38445082050; artifact 11837853851 |
| 38465614811 / 115531527064 | Compile/link/dumpbin/map PASS; BLOCKED intencional por review pendiente, sin paquete | windows-run-38465614811; artifact 11848837315 |
| [38466822325](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325) / 115535637388 | SUCCESS: MSVC build, auditor nuevo, 20 negativos PE, 13 ZIP y target oficial/package | windows-run-38466822325 |

La corrección de forwarding headers a una definición canónica permanece en `ci/prepare.py`; no se rehízo. La segunda falla exigió capturar/revisar imports reales, no desactivar el auditor. Se preservaron logs completos propios y ledgers; no el log privado del usuario.

## Incrementales, reutilización y límites

| Comprobación | Estado | Ejecución/evidencia |
|---|---|---|
| 100 checks nuevos/afectados (scope686, negaciones, coherencia A/B/C, speed/delta, presupuestos/identidades, latch) | PASS_LAB_REUSED_BY_HASH | Run 38445082050, SUMMARY failures=0; 20 hashes idénticos en REUSE_WINDOWS_LAB.json |
| 8 mutantes any_invalid_room, ky_without_owner, far_unknown_profile, d3_replaces_XZ, movement_admitted, C_freshness_missing, reject_consumes_latch, critical_shares_normal | PASS_LAB_REUSED_BY_HASH | Los ocho compilaron MSVC; cada ejecutable devolvió 1 por aserciones, no compile errors |
| 20 negativos PE semánticos | PASS, ejecutados Windows en este run | Decoración exacta, setter, create, file API, CRT, DLL, ActorService, ABI, tamaño, x86, TLS/delay, exports nombre/ordinal/forward/alias y manifiesto incompleto/duplicado/esquema/ausente |
| 13 negativos ZIP | PASS, reejecutados Windows | Duplicado/case alias, extra/traversal/absolute/drive/backslash, symlink/special/oversize, directory nonempty, CRC, cifrado; wrapper refuerza tipo directory/name |
| 7 negativos de descarga/paquete propios | PASS, inspección Python offline | External manifest/DLL hash/procedencia, artifact digest, internal mod ID/DLL bytes y dos inconsistencias de directory/file; download-negative-results.json. No compilación ni ejecución de DLL |
| Identidad de 30 imports de juego + 24 CRT/system actuales | PASS_STATIC | Nueve DLLs, 54 símbolos exactos, sin wildcard |
| Única llamada memcmp y bytes F_SP121 NUL | PASS_STATIC | R8D=8, buffer stack/constante, caller context_valid; memcmp-review.json |
| Grafo 6 unidades nativas + 8 bridge readonly, mapa/servicios/exports | PASS_STATIC | compile-commands.json, module-map.log, result.json |
| Target oficial SDK y DLL interna byte-idéntica a suelta | PASS | package_verification del run |
| Descarga real, CRC/SHA/tamaños/manifest/PE/exports/source ledger | PASS | download-verification.json; DLL solo leída, nunca cargada |
| 104+7 y 46+4 anteriores | HISTORICAL_NOT_RERUN | No presentados como ejecutados en esta tarea |
| Velocidad nueva real, nueva aparición/render/colisión/limpieza/DX12 | NOT_TESTED | Ningún juego/DLL ejecutado |

MSVC 19.51.36260 x64, linker 14.51.36260, VCTools14.51.36231, WindowsSDK10.0.26100.0, CMake4.4.3/Ninja Release. El runner windows-latest no garantiza eternamente la misma imagen: versiones efectivas se registran por ejecución. Fuente/SDK/importlib/hashes están fijados; no se afirma reproducibilidad byte-a-byte entre toolchains o timestamps distintos.

Runner propio: 2026-10-13T20:57:31.880993+00:00 → 2026-10-13T20:57:55.934750+00:00 (≈24,05 s; 15:57:31→15:57:55 Panamá), sin incluir checkout/setup/upload. Comandos, exits y segundos de cada fase: result.json. No se compiló ni ejecutó el host, no Linux SDK test ni loader harness.
