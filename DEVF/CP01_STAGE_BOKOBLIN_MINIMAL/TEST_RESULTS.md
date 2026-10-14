# Pruebas focalizadas

| Comprobación | Resultado |
|---|---|
| MSVC19.51.36260 x64, Windows SDK10.0.26100.0, VCTools14.51.36231, CMake4.4.3/Ninja Release | PASS compile/link, run38496922708/job115634702685 |
| Once-only payload/failure/reentry/no retries/1000 updates sin add/shutdown idempotente | 11 escenarios PASS en run38496356945, reutilizados por hashes y toolchain idénticos, no repetidos en run final |
| Payload32 BE: E_oc/FFFF0000/posición/angle(6,0,0)/FFFF, room3/layer6 concretos | PASS_FAKE; código real mod.cpp compilado en EXE aislado, no DLL ni juego cargado |
| Máquina AMD64, ABI1, metadata Host2.2/Log1/Stage1/Game2, cinco exports | PASS_STATIC final; metadata presente completa |
| Identidad de imports | PASS_STATIC:20 CRT/system exactos y ningún import dusklight.exe/Aurora/GX; StageService indirecto permitido |
| Negativos x86, metadata ActorService y nombre export alterado | 3 PASS final; solo bytes de DLL propia, sin cargarla |
| Target oficial `.dusk`, miembros/rutas/CRC/SHA/manifest y DLL interna==suelta | PASS |
| Descarga real de Actions y verificación independiente | DOWNLOAD_VERIFIED; external manifest byte-idéntico al texto del run, source ledger/PE/exports/hashes/CRC PASS |
| Localización | PASS_STATIC_LOCAL; suelo/cobertura y separación de registros/volúmenes modelados; seguridad efectiva/visibilidad NOT_VERIFIED |
| Aparición/render/IA/combate/muerte/retirada al recargar/DX12 runtime | NOT_TESTED; usuario ejecutará tras aprobación |
| SDK Linux, suites104/46/100 y mutantes anteriores | NOT_RERUN; no necesarios para este contrato |

Once escenarios: success, reentry, reject, zero-handle, throw, missing-service, wrong-host-version, short-stage-header, null-add, wrong-stage-major, null-context. Test de excepción deliberada solo en callback fake. Lab incluye un símbolo GXDestroyTexObj de aborto exclusivo de test para resolver una referencia emitida por headers amplios: si se alcanza incluso al cerrar el EXE, falla el proceso. Los once EXE devolvieron0; ninguna ejecución lo alcanzó. No es stub de producción ni prueba de gráficos. La DLL no contiene tests/GX imports.

Fallos conservados, ningún paquete fallido publicado:

| Run / job | Causa y corrección |
|---|---|
|38495478715 /115630155032|DLL enlazó; lab falló por GXDestroyTexObj y conversión BE→csXyz/constructor. Lectura directa de componentes BE eliminó csXyz; sin game linked/loaded.|
|38495925831 /115631540566|GX header COMDAT seguía sin resolver. Tripwire abort-only exclusivo del laboratorio; no producción.|
|38496356945 /115632895155|Build/lab11 PASS, auditor detuvo por metadata ausente: /Zc:inline en producción eliminó registros MOD_META_RECORD; secciónmodmeta16bytes. Fue configuración propia, no defecto corregido en host.|
|[38496922708](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38496922708) /115634702685|SUCCESS. /Zc:inline- conserva metadata oficial en producción; auditor completo y tres negativos/SDK package PASS. Lab previo intacto reutilizado por hashes.|

Logs sanitizados completos, exits/tiempos, mapas y manifests en evidence/windows-run-*. Textos de laboratorio están etiquetados fake y no son logs de juego. Runner final 2026-10-14T01:40:40.791963+00:00→2026-10-14T01:40:56.604721+00:00 (≈15,81s, aparte de setup/uploads); todos los comandos en result.json. No se cargó ningún DLL ni ejecutó el host/juego.
