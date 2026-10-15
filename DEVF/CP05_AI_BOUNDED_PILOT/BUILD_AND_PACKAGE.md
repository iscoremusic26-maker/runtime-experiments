# CP05 — Build y descarga verificados

Fuente realmente compilada: `ec61daa3ed7d539989028cd26b22fa529896de11`.
CI build: `efd8a49ec7b4bcb444bf510c5a9173a92386ce97`, [run38672691356](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356) /job116219222220.
CI verificación: `41396f1fe17120b0f95e2ae0da4abc9c2866821e`, [run38672879974](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672879974) /job116219818583.
Host fuente40457c6adb381928e4b5fef6ed459ed291edd5e2, Aurora3227d76c60e1e782ca576610bce61c9e7744d8be y librería SDK original verificados en runner; no host build ni cambios. MSVC19.51.36260, VCTools14.51.36231, SDK10.0.26100.0, AMD64.
Configure5.891s/build5.344s/lab resolución0s/package0.297s; tiempos CI, no medición de FPS.

Comandos reales parametrizados, completos en evidence/build-result.json:

```powershell
cmake -S DEVF/CP05_AI_BOUNDED_PILOT -B work/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DDUSK_SOURCE=.official -DDUSK_GAME_EXE=work/windows-amd64.lib -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build work/build --target devf_cp05_ai_guard cp05_ai_lab --parallel 2
work/build/cp05_ai_lab.exe
dumpbin /headers work/build/devf_cp05_ai_guard.dll
dumpbin /imports work/build/devf_cp05_ai_guard.dll
dumpbin /exports work/build/devf_cp05_ai_guard.dll
cmake --build work/build --target devf_cp05_ai_guard_package
```

| Elemento | Bytes | SHA256 |
| --- | ---: | --- |
| ZIP TEST artifact11945045896 | 52452 | c5df6dcbd0f440e096c5c4048f2c3c97476ed6cb1234c9587e2df0a6317914bc |
| DEVF_CP05_AI_GUARD_windows-amd64_ec61daa3ed7d539989028cd26b22fa529896de11.dusk | 18929 | 23f81ad131082a03fcd66068ccd926ecf878182a5afce06244898cf663248ddb |
| DLL interna lib/windows-amd64/mod.dll | 34816 | 830577e71543301f5ca672094caeb5c54103d61e85a23f01e2ba39074565f509 |
| SOURCE_COMPILED.zip | 34777 | 1e3fa8a08908b5781d00427f398c2ba48346a0cfab9971261f4450a401f75fb0 |

[ZIP privado TEST](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356/artifacts/11945045896). Caduca2026-11-14T02:46:49Z = **2026-11-13 21:46:49 Panamá**. No promesa después de vencimiento.
Artifact TEXT11945170843:9265bytes/SHA cbbda0d6c15ef5d1fce440406d7c42aed14babf06933f81259af8cd0a73366f8; logs de compilador/lab/PE y result.json, sin raw logs del usuario.
ZIP contiene sólo .dusk, MANIFEST.json, SHA256SUMS.txt y fuentes propias compiladas (incluye3 headers CP03 inmutables). Dusk sólo mod.json y DLL en directorios oficiales. No ARC/BMD/EXE/importlib/SDK original/texturas/assets.
SourceZip conserva docs anteriores a validación; la documentación posterior del checkpoint actualiza los resultados sin reempaquetar.

Descarga independiente REAL en otro runner: hashes/bytes artifacts, CRC de todas las capas, ledger fuente, manifiesto, checksum, dusk y DLL reanalizada PE/ABI. No sólo checksum de workflow. Token sólo enviado a api.github.com; redirect firmado sin auth y sin publicar URL firmada. Ver evidence/download-verification.json.

El workflow CI en rama actual quedó en modo download-only y no construye por cambios documentales. Para una futura corrección autorizada usar el workflow de build del CI SHA efd8a49ec7b4bcb444bf510c5a9173a92386ce97 y pin nuevo; nunca recompilar/reemplazar CP04.4 histórico. No Linux/Vulkan como prueba de entrega Windows.
