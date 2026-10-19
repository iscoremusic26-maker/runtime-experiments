# CP19 FIX02 — resultados

**A y B: SOURCE_IMPLEMENTED / LAB_PASS / WINDOWS_MSVC_PASS / INDEPENDENT_DOWNLOAD_PASS / HUMAN_RUNTIME_PENDING**

El juego no se ha ejecutado: que se oigan los Bokoblin, que se vea el destello y que la guardia continúe solo lo confirma la prueba humana.

## Local (WSL2, g++ 15.2, C++20, ASan+UBSan)

| Gate | Resultado | Clase |
|---|---|---|
| `cp19f2_lab`: 40 casos contra puertos del motor (loader/heap ARAM/wave table, escena, colisión con escudo, medidor, `setDamagePoint` como control negativo, calendario de color de `draw`) | 40/40 | LAB |
| Mutaciones de `cp19f2_policy.hpp` y de la puerta FIX01 | 35/35 eliminadas | LAB |
| `mod.cpp` y `cp19f2_abi.cpp` con g++ contra cabeceras oficiales | 0 errores, 0 avisos propios | COMPILADOR NO-MSVC |
| `source_gate.py` contra FIX01 y 52 blobs oficiales | PASS | INSPECCIÓN |

## Windows MSVC y descarga independiente (CI)

[Run 39312607981](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39312607981): build 118265815741 + independent-download 118267110919 **SUCCESS**. Fuente `a0dd9e5a780c413a27fd165c9d3133b14d1e8613`, CI `db30418c6e97eecd1a6dcf45a80d8839483ddc48`. MSVC 14.51.36231 x64; 0 avisos printf, 0 avisos en ficheros propios (los 27 avisos son de cabeceras oficiales, igual que en FIX01).

Intentos previos (fallos de CI reales, corregidos antes de entregar):
- 39310447670: mi `static_assert` detectó que el puntero a miembro de `daAlink_c` mide 24 B en MSVC (herencia no especificada, `daAlink_procFunc` se forma antes de la clase). Ahora se usa el registro extendido del SDK y el auditor lo valida.
- 39311127095: la lista revisada aún incluía `eraseSeWave`, que ya no se importa porque no hay ruta de borrado.
- 39311847821: error en el script de auditoría (variable del bucle reutilizada).

| Gate | Resultado CI |
|---|---|
| Blobs fijados / UTF-8 / puerta de fuente vs FIX01 (27 idénticos, sin borrado de ondas, una sola escritura de vida, render de Link restaurado, 52 blobs oficiales) | 708 / PASS / PASS |
| CP19 FIX02 / CP19 FIX01 / CP19 / CP18 / CP17 FIX01 / CP17 / CP16 FIX01 / CP16 / CP15 / CP14 | 40 / 73 / 65 / 43 / 53 / 64 / 53 / 56 / 38 / 16 |
| CP13 runtime / map / Black / variant / damage / dynamic / visual / eyes / strokes / perf / CP12 / texture | 26 / 66 / 26 / 30 / 22 / 28 / 22 / 9 / 36 / 4 / 7 / 20 |
| Editor CP13 / CP08 / CP09 / multi / nombres | 39 / 42 / 71 / 110 / 25 |
| COFF MSVC (6 215 B, `a0688a0b43bdd3a9b761e551ad15bdecd5f53836f980ea0a77342602db891906`): `tevStr` 0x1f0, `TevKColor` +0x360 (= 0x550), modelos de Link 0x770/0x778/0x780/0x788/0x7d8/0x7e0/0x810/0x820, `JASHeap` mBase 0x70 / mSize 0x78, `JKRAram::mAramHeap` 0xf8, `JKRAramHeap::mHeap` 0x60, `JKRAramBlock` 0x28/0x2c: **iguales a los del `dusklight.exe` 2.0.3 oficial** | CP19F2_MSVC_COFF_SOURCE_ABI_PASS |
| PE/ZIP: hooks `daE_OC_c::execute` (registro compacto) y `daAlink_c::modelDraw` (registro extendido), ambos unidos a su import; imports = FIX01 − `eraseSeWave` + 13 revisados (45); 27 negativos rechazados | CP19F2_PE_ABI_PASS |
| Descarga independiente + re-descarga local (bytes y SHA-256 iguales, CRC) | DOWNLOAD_VERIFIED |

## Comprobación en la DLL compilada (inspección binaria local, `cdc69498…5733`)

- `audio_pass` (0x47f0): la puerta FIX01 está intacta. Cada condición fallida pone `dil` = 1..7; `dil` = 0 solo en 0x48c2, tras las 8 comprobaciones. `test dil,dil; je 0x4958`: el bloque listo contiene la **única** llamada a `resident_pass` (0xa470, en 0x4966) y la lectura BGM.
- Todas las referencias a audio/ARAM de la DLL están dentro de `resident_pass`: `getWaveLoadStatus`, `loadSeWave`, `sAramHeap`, `sAramObject`, `JKRHeap::alloc`, `JKRAramHeap::alloc`, `initRootHeap`, `getAramFreeSize` y `mAudioMgrPtr`.
- `sAramHeap`:
  - 0xa8fe: si ya tiene valor, se rechaza;
  - 0xa90f: se fija;
  - 0xa92f: `loadSeWave(0x5e)`;
  - 0xa93e: vuelve a 0.

  Solo hay 2 referencias a ese slot.
- No hay imports de `eraseSeWave`/`eraseBgmWave`. Única llamada a `dComIfGp_setItemLifeCount`: 0x168b3, en la función del chip.

## Paquete

`BokoblinExpansion_0.16.2_CP19_FIX02_TEST.dusk` 151 985 B, SHA-256 `2e11259916504da2bf127d0ab20f9b3db4776e3d2e10c9d05f0c752bc4053fea`; DLL 401 408 B `cdc694989ae83401ea7459c7920ae86a6875b1d426cfc6b8917662976cd45733`; ZIP 2 611 409 B `dd6b107630ee6f3250ccf14822ea6ea6fedebaf735a13aee02d0f36e03cf96a0`. Artifact 12217026541, caduca 18-11-2026 14:40:37 America/Panama.
