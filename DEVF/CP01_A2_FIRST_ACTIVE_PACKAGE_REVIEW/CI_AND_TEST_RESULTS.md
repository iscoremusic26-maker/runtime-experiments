# Pruebas incrementales y Windows CI

**ACTIVE-CAPABLE / NOT INSTALLED / NOT RUN / SESSION NOT AUTHORIZED.**

Dusklight **2.0.3 Windows x64/DX12**; paquete ID`dev.devf.cp01_eoc_first_active_pilot` versión`0.0.1`; fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`.

| Run | Resultado real |
|---|---|
|38434228398|Build/link PASS. 46 checks, 1 fallo del fixture de saturación de trazas; no paquete activo publicado.|
|38434647284|46/46 checks PASS, 4/4 mutantes compilados y detectados, 23 negativos ZIP y 3 negativos de digest PASS. Luego falló la comparación ordenada de imports; los conjuntos eran idénticos. No paquete activo publicado.|
|38435464736|DLL Windows, auditoría PE/map/disasm/provider/slot32, paquete SDK e inspección interna PASS. Reutiliza las pruebas del run anterior tras verificar hashes idénticos; no vuelve a ejecutarlas. Descarga independiente posterior: DOWNLOAD_VERIFIED.|

[Run final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38435464736), job115428153522: único job `active-package`, success. Fuente compilada `a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`; CI `245c9eec99f7ff0186aac4174f04811cb9918b76`. [PR12 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/12), base exacta0b7b517ff2fdce5a0964cbc1dbd91d4a27525b28. Seis workflows históricos intactos con filtros disjuntos. Sin merge.

Los46 checks usan el proveedor real: grant/denied; tres capturas frescas; preset C/perfil/params/angle/scale; live Key y stage/room/layer; XZ1599.999/1600/1600.001 y deltaY; movimiento de Link, actor global desconocido y censo truncado; cambios de Key/freshness/reentrada A/B/C; latch, setter, previous y restore; MOD_OK distinto de READY; timeout, error y shutdown sin retry; trazas, sink y presupuestos; contratos reales de servicios y nulos. Los static_assert de headers oficiales comprueban tamaños48/80/8 y offsets create32/room64. Solo se ejecuta EXE fake de laboratorio; nunca DLL ni host.

Cuatro mutantes nuevos ejecutados con MSVC: provider NONE accidental; umbral1600→1200; omisión del check C; omisión del latch. Los cuatro compilaron y terminaron por assertions con exit1. Ningún crash ni error de compilación se contó como kill. Fuentes/resultados en REUSE_LAB_EVIDENCE.json y logs del run38434647284. La suite histórica104 y sus7 mutantes se conserva como evidencia anterior; no se reejecutó.

Los23 negativos ZIP cubren manifest/DLL ausentes o sustituidos, identidad/manifest drift, duplicados/case aliases, extras, rutas inseguras, symlink/especial, tamaños, directorios falsos/no vacíos, CRC, cifrado, ratio anómalo, ZIP malformado/truncado. Tres fixtures adicionales comprueban rechazo por digest distinto de manifest/SDK/importlib, sin modificar originales. Los mismos validadores y fixtures mantienen sus hashes; el run final reutiliza esos PASS. Tras descargar el archivo real, tres negativos adicionales en Codex rechazaron digest externo falso, workflow manifest distinto y DLL hash esperado falso; sin extraer/cargar DLL. Esa inspección Linux de datos no es una compilación simulada Windows ni un ensayo runtime.

MSVC**19.51.36260.0**, toolset**14.51.36231**, WindowsSDK**10.0.26100.0**, CMake**4.4.3**. Imagen `windows-2025-vs2026@20260925.250.1` en windows-latest. SDK40457c6.../Aurora3227d76.../.lib SHA4dc4a511... exactos; fuentes y hashes completos en SOURCE_AUTHORITY y result.json. No vcpkg/host build ni repetición SDK Linux.

```powershell
python DEVF/CP01_A2_FIRST_ACTIVE_PACKAGE_REVIEW/ci/run_windows.py --source .official --inputs . --work "$env:RUNNER_TEMP/first-active-package"
```

Último run: configure Ninja Release8.360s; build DLL11.640s; target SDK package0.297s. Fases desde2026-10-13T17:03:28.585634Z hasta17:03:53.499604Z (12:03:28→12:03:53 Panama UTC−5). Comandos completos y15 unidades de producción en result.json/compile-commands.json. Los23 archivos textuales y22 hashes del run final están preservados en Git; los16 inputs propios se contrastaron con el commit compilado y con el checkpoint. CI_SOURCE es procedencia externa excluida del propio ledger para evitar autoreferencia. Herramientas documentales agregadas después no alteran el binario.

REQUEST/CREATION/RENDER/COLLISION/CLEANUP y DX12 de esta DLL: **NOT_TESTED**. G5/CP02 NO-GO; G6 NOT_VERIFIED; ubicación no certificada y unloading custom BLOCKED.

Integridad histórica:658 archivos de worktree sin cambios y658 blobs Git del baseline sin cambios;46 textos históricos tienen solo diferencia CRLF(worktree)/LF(Git). Se preservan ambos ledgers y no se reescribe ningún histórico. El verificador de fetch usa los hashes de los blobs del baseline; el subset277 conserva su ledger exacto anterior.

Referencias:las50 referencias locales previas conservan su valor. De ellas,45 son ramas/tags de GitHub contrastados exactamente mediante fetch;5 son referencias locales/tracking (incluidas dos tracking ya obsoletas) cuyos objetos originales siguen recuperables en la historia descargada. No se publican ni actualizan esas referencias locales para simular igualdad con la punta remota. El tag base0ff1b8b también se verifica por separado.
