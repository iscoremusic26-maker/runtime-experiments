# Resultados — CP00
| Comprobación | Estado | Evidencia |
|---|---|---|
| Acceso a ambos ZIP completos | PASS | bytes, entradas y CRC en evidence/input_verification.json |
| SHA256 frente a handoff/OID LFS | PASS | coincidencia exacta de ambos |
| Fuente extraída contra ZIP | PASS | 19367 archivos, cero diferencias |
| PE Windows x64/version | PASS | AMD64, PE32+, 2.0.3.0 |
| Import library contra exports EXE | PASS | 30042 imports, cero símbolos faltantes |
| Checkpoints anteriores | NOT_AVAILABLE | repo de trabajo vacío; handoff disponible |
| Prueba Linux de configuración | PREVIOUSLY_COMPLETED | conservada; no repetida ni atribuida a DEVF |
| Guarda CMake contra build Linux | PASS | configuración rechazada explícitamente por plataforma; sin compilar el probe ni repetir smoke SDK |
| Build CP00 Windows x64 | BLOCKED | toolchain/SDK objetivo ausentes |
| Probe runtime Windows | NOT_TESTED | source preparado, sin DLL |
| Actor/Stage lifecycle, IA, colisión | NOT_TESTED | CP01/CP02 pendientes |
| Render/aislamiento DX12 | NOT_TESTED | Windows real pendiente |

Los PASS de archivos y símbolos no prueban compatibilidad runtime. CMake del probe y su código aún no verificados mediante build Windows.
