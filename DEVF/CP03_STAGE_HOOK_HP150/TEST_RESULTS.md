# Resultados CP03

| Comprobación | Estado | Evidencia y límite |
|---|---|---|
| Target create→execute→action; sin inlining crítico | SOURCE_VERIFIED | host-target.json: Windows oficial, inspección estática |
| Identidad en inventario disponible | SOURCE_VERIFIED | 40 E_oc originales, cero coincidencias; requiere solo CP03 |
| 15 casos nuevos de política/registro | PASS TEST_FAKE | Run 38511192326; snapshots, no actor/DLL/backend real |
| Reutilización de esos 15 casos | PASS | Hashes de CPP/hpp/tests/CMake/SDK/lib/toolchain iguales |
| DLL MSVC y binding tipado | BUILD_PASS / PE_PASS | Run 38513406897; cinco exports, siete records, 28 imports |
| Cuatro negativos PE | PASS | x86, servicio Hook, target y export alterados rechazados; copias propias no cargadas |
| Paquete oficial e igualdad de DLL | PACKAGE_VERIFIED | .dusk 8953 bytes, DLL 16896; CRC/SHA/manifests |
| Descarga real de TEST y TEXT | DOWNLOAD_VERIFIED | Git/CI/manifest/source ledger/PE/ZIPs contrastados |
| Hook instalado y primera llamada real | HUMAN_RUNTIME_NOT_TESTED | Requiere log sin warnings y HP_APPLIED |
| HP150 efectivo y ausencia de reset tras daño | HUMAN_RUNTIME_NOT_TESTED | Lectura dentro del juego pendiente |
| Aparición, render, recursos, DX12, combate y originales | HUMAN_RUNTIME_NOT_TESTED | No ejecución del juego ni DLL de producción |
| Retirada tras cierre y reentrada | HUMAN_RUNTIME_NOT_TESTED | No prometer borrado caliente del actor vivo |
| CP03 estable / CP04 | NO-GO hasta evidencia humana / NOT_AUTHORIZED | Piloto offline únicamente |

Casos nuevos: registration_success, reentry, stage_fail, zero_handle, install_fail, install_throw, missing_hook, hook_minor0, bad_host, timing_and_damage, originals, room_reload, ambiguous_or_recycled, incomplete_and_late y detach_disarm. Cada uno se ejecutó como proceso separado y terminó con exit 0.

Cobertura: payload32 BE exacto, una adición/handle, errores de servicio, orden 220→pre150→action150, daño posterior 115 sin reset, originales no coincidentes, recarga/nueva instancia, concurrente/ID repetido, HP inesperado, recurso incompleto, llamada tardía y desarmado. La política y registro reales se compilan en el laboratorio. El bridge tipado se compila/audita en producción, pero no se invoca en CI. Detach simulado no prueba el backend: su contrato real se revisa en la fuente oficial.

Intentos conservados; no se publicó TEST mientras fallaban:

1. 38510945734: E_OC requiere mDoExt_McaMorfSO. Se añadió include oficial en nuestro módulo, sin editar SDK.
2. 38511192326: BUILD y 15/15 TEST_FAKE PASS; auditoría exacta detectó strcmp fuera de la lista nueva. Se revisaron los 28 imports completos.
3. 38512608035: BUILD y PE positivo PASS; nombre temporal con `::` inválido en Windows. Corrección exclusiva de tooling.
4. 38513406897: SUCCESS; build, PE, cuatro negativos y package PASS; descarga posterior verificada. CPP/headers de producto y laboratorio sin cambios desde el segundo intento.

CP01/CP02 humano PASS es antecedente de aparición/comportamiento/retirada, no prueba CP03 ni medición de 220 HP. No se repiten A0/A1, G5, KCL/WRock/Digpl, CP00, host o SDK Linux. Logs Windows conservados byte a byte, incluidos CRLF; sus ledgers no se normalizan. [gates.json](evidence/gates.json) registra estados finales.
