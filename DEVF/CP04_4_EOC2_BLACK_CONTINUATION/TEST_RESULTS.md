# CP04.4 — Resultados finales de la continuación

**CP04_4_EOC2_BLACK_PRIVATE_TEST_READY / CODE_ISOLATED_OFFLINE. HUMAN_RUNTIME_NOT_TESTED.**

| Gate | Resultado | Evidencia real |
| --- | --- | --- |
| E_oc2.arc bytes/SHA256/Git blob/CRC/Yaz0/RARC/modelos index3/4 | PASS estático | Lectura de bytes base64 + contraste Windows Node, run38655133336; effective-materials.json. Arc33872, SHA c87d…394, CRCee2501dd; hashes BMD coinciden. |
| MAT3/SHP1/INF1/VTX1/TEX1 y cuerpos/ojos/arma | PASS estático | Remap0/1/2; shape0→mat0, shape2→mat1, shape1→mat2; CLR ausente; tres oc2_fix comparten imagen. TEV y fuente de raster registrados íntegros en evidencia derivada. |
| Llamada real del helper en el EXE oficial, sin inline/unrelated ICF | PASS estático PE | Run38655854048; una llamada directa MatPacket.draw→ShapePacket.drawFast. Los3 nombres son alias exactos de la misma función; no se publica RVA/disassembly. |
| Selección/additional0/2/eyes/weapon/normal E_OC/original E_OC2/identidad/escena/estado/generación/packet | PASS OFFLINE_ONLY | Laboratorio C++ propio usa core real y datos compartidos explícitos; callback nativo de la DLL no ejecutado. |
| Dos originales y DEVF intercalados / mismo frame / FIFO diferido / snapshot de comandos / ausencia de writes shared | PASS OFFLINE_ONLY | Cinco geometrías comprobadas una a una; dos actores usan el mismo puntero de recurso. Cmd arrays se copian al queue y restores comprobados. |
| Out-of-order/nested/missing POST/reentrada/reconstrucción/draw null/model-allocation failure/shutdown/bounds/alpha/charcoal bound | PASS OFFLINE_ONLY | 20 casos totales. Scope no tiene allocator/model pointer; fallo de modelo no emite. OOM fatal interno del host/FIFO no probado. |
| Compilación/enlace nuevo Windows AMD64 MSVC | BUILD_PASS | Run38657297492; cl19.51.36260, VCTools14.51.36231, WindowsSDK10.0.26100.0; CMake/Ninja; DLL28672 bytes. Nunca build host/SDK Linux/CP03. |
| PE/ABI/metadata/export/import/PMF↔IAT exactos | PASS |8 records,5 services/versiones,2 hooks MEM8bytes y sus imports precisos,5 exports oficiales; TLS/delay imports ausentes; whitelist exacta. |
| Negativos | PASS,6 rechazos | x86, target packet erróneo, servicio hook erróneo, export erróneo, miembro ARC extra, traversalZIP. Ninguna DLL mutada se cargó. |
| .dusk oficial/manifest/DLL idéntica/CRC/contents | PACKAGE_VERIFIED | SDK target devf_cp04_eoc2_black_package;15.287 bytes; sin resources originales. |
| Descarga REAL de2 artifacts privados / ZIP exterior / SourceZip / dusk / DLL / source ledger / PE repetido en DLL descargada | DOWNLOAD_VERIFIED | Nuevo runner Windows, run38658291368, job116173195779; SHA256 de artifacts, CRC y manifiesto/strings/bytes internos comprobados; no recompilación. |
| CP03 y cierre anterior: archivos/refs recuperables | PASS del baseline conservado; sellado final remoto al cerrar | Comparación Git completa contra0b2216ee; tag final y destino se verifican por API al publicar. No se modifica el tag antiguo. |
| Píxeles negro/volumen/ojos/arma/contraste con E_OC2 original/combate/muerte/reentrada/rollback | HUMAN_RUNTIME_NOT_TESTED | Sólo el usuario puede confirmar esta versión mediante log+captura. El PASS humano CP03 no se hereda como PASS visual CP04.4. |
| Overrides de la instalación / convivencia con otro mod que reemplace o recurse este helper / rendimiento GPU | NOT_VERIFIED / NOT_TESTED | Guardas runtime comprueban contrato efectivo; instalación/hardware no accesibles. Instalar sólo este DEVF y retirar conflictos. |

## Laboratorio y límites

El laboratorio ejecutó el código real de xf_scope.hpp con20 casos, no la DLL/Game/HookService backend. Las pruebas de shared pointer/material/texture/DL usan el mismo objeto para original y DEVF y comprueban inmutabilidad; las pruebas de FIFO son un modelo explícito de captura por valor. No se presentan como GPU fake equivalente. El bracketing del callback y las guardas nativas se justifican adicionalmente por fuente y PE; su eficacia runtime se validará por humano.

No hay allocation visual propia que deba sobrevivir a escena: nada de cloned model/shapes/texture buffers ni vtables en actores. Source/draw closure comprueban retirada de palabras/keys del scope. Las APIs del host tienen su límite habitual: abort/OOM fatal no son recuperados por esta DLL.

## Incidencias corregidas, sin modificar host

- Run38655001894: checkout shallow sin padre; antes de analizar recursos. Se corrigió fetch-depth0.
- Runs38655133336/38655334008: procedencia PASS; gate conservador bloqueó MULTI_NAME hasta enumerar co-addressed nombres. El tercero era el alias source-qualified del mismo método, no ICF ajeno; allowlist exacto comprobado en38655854048.
- Run38656791697: error C++ del wrapper (getVertexData devuelve referencia). Corrección local.
- Run38657033655: DLL compila; fixture del laboratorio esperaba6 geometrías pero encolaba5. Se corrigió el conteo; se siguen comprobando los5 colores, no se omitió el control negativo. Se añadió readback de la palabra del comando privado.
- Run38657297492: build/lab20/PE/negativos/package SUCCESS.
- Run38657956298: descarga real con hashes de artifact correctos, checksum textual Windows CRLF no aceptado por verificador. Se normalizó sólo el texto SHA256SUMS y se fijó checkoutLF; dusk/manifest/DLL/CRC y hashes quedan estrictos.
- Run38658291368: DOWNLOAD_VERIFIED, no build repetido.

Evidencia: build-result.json y download-verification.json contienen comandos/tiempos/versiones/hash/ledger, sin credenciales, texels ni log privado del juego. Los informes sellados de0b2216ee siguen intactos.
