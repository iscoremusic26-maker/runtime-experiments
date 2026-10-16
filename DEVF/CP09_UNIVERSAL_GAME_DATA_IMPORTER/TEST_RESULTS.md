# CP09 — Windows build y descarga verificados
Dictamen técnico: **WINDOWS_BUILD_VERIFIED + PRIVATE_TEST_READY**.
Dictamen humano: **CISO_REAL_IMPORT_HUMAN_PENDING**; Codex no ejecutó Dusklight.

- Fuente realmente compilada: `b9ea7518684126b733532cb0a99a0e3b98d4d74e`.
- CI exacta: `04e87f713f1d96301d7ede29cda9628ba8fa84f9`; .NET SDK 8.0.426, net8.0-windows, self-contained win-x64.
- [Run final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38918182460): build SUCCESS, independent-download SUCCESS.
- [Paquete privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38918182460/artifacts/12053167316), artifact 12053167316, DEVF_CP09_IMPORTER_TEST_38918182460.
- Caduca 2026-11-15 09:46:03 America/Panama (2026-11-15T14:46:03Z).

| Gate | Evidencia real | Resultado |
|---|---|---|
| Aplicación WinForms / lector CISO sparse e ISO / FST / catálogo / caché / cancelación | 54 casos importador ejecutados Windows, fixtures sintéticos legales | PASS de laboratorio |
| Regresión modo CP08 | 42 casos, ARC auténtico por hash, controles reales add/enable/yaw/drag/paint, guardado/backups, mapa↔mundo | PASS |
| Geometría real | R03_00.arc F_SP121/room3; 5326 triángulos completos, 100 en subconjunto histórico | PASS de lectura |
| Contraste independiente | Lector Python CP01 vs C#: alturas .002 unidades; tres referencias humanas redondeadas tolerancia .02 | PASS |
| Seguridad de formato | FST/rangos/traversal/duplicados, Yaz0 excesivo/truncado, RARC ciclos/alias, KCL/PLC corruptos, NaN, pisos superpuestos, caché manipulada/interrumpida | PASS de laboratorio |
| PE | AMD64/PE32+, 2 negativos de cabecera/truncado | PASS |
| Paquete / descarga independiente | Segundo runner descargó artifact; SHA256, bytes, CRC, PE y todos los blobs de SourceZip contra ledger | PASS |
| CISO comercial GZ2E01 completo | No disponible en CI ni leído por Codex | HUMAN_PENDING |
| Dos salas auténticas adicionales | No disponibles en inputs utilizados | NOT_TESTED |
| Exportar nuevas salas / runtime CP10 | Bloqueado; no implementado | OUT_OF_SCOPE |

Resumen de catálogo **sintético**: 1 stage T_TEST, 3 recursos de sala distintos; 2 mallas legales sintéticas disponibles, 1 recurso corrupto aislado. No representa cifras del juego.
Recursos auténticos procesados: **1 sala** (R03_00.arc), SHA256 dc53106667811c4cde18b35edb5279357f00ebecaef2f9de546aea9a5a2b06af. No se distribuyen ARC, KCL, PLC, mallas ni ROM.

Historial CI: run 38917466456 compiló y pasó 92 casos, pero falló empaquetado por KeyError source_ledger; no fue TEST_READY. Se corrigió el ledger y fijó SDK .NET8. Run38918110915 pasó build/descarga; el run final añade rechazo de alias RARC y su negativo. No se reutilizan hashes de builds previas.

CP08 humano histórico sigue limitado a tres Bokoblins reportados por el usuario. Esta CI no vuelve a ejecutar el juego ni amplía ese dictamen. Los .dusk proveedor0.8.0/Expansion0.2.0 y sus fuentes permanecen sin cambios.

## Hotfix CISO_PHYSICAL_LENGTH (+576 B) — 16-10-2026
**WINDOWS_BUILD_VERIFIED + PRIVATE_TEST_READY; CISO_REAL_IMPORT_HUMAN_PENDING.**
Fuente compilada: `3b45f2f50c65f98f0f9b880bc8d1ec7cc9829416`. CI: `c6e20919e0f0d9ae3139879974c4e50220b1e429`. SDK .NET8.0.426, net8.0-windows self-contained AMD64. [Run 38954973078](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38954973078): build SUCCESS e independent-download SUCCESS. [ZIP privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38954973078/artifacts/12069682536).

Resultados nuevos ejecutados: **113 casos de aplicación PASS** (42 compatibilidad CP08 +71 importador), **2 negativos PE PASS**. Se conservaron las 54 pruebas originales del importador y añadieron17; el truncamiento CISO existente exige ahora el código CISO_PHYSICAL_LENGTH exacto. El límite4096 acepta el sufijo576 no nulo, rechaza4097 y nunca lo expone en el espacio lógico. La aritmética real comunicada se comprobó sin generar un archivo de1GB.

Casos nuevos, nombres reales del runner:
- `CISO-no-tail-policy-unchanged`
- `GCM-logical-match`
- `CISO-user-diagnostic-mapped-end-arithmetic`
- `CISO-user-diagnostic-tail-arithmetic`
- `CISO-tail-576-nonzero-accepted`
- `CISO-tail-logical-space-unchanged`
- `CISO-tail-never-exposed-through-absent-block`
- `CISO-tail-FST-resources-unchanged`
- `CISO-tail-logical-end-rejected`
- `CISO-tail-policy-boundary-accepted`
- `CISO-tail-policy-excess-rejected`
- `CISO-physical-policy-overflow-rejected`
- `CISO-block-size-uint-overflow`
- `CISO-tail-does-not-extend-FST-range`
- `ISO-FST-truncated-rejected`
- `CISO-truncated-header-rejected`
- `CISO-tail-catalog-resource-regression`

Regresiones PASS: CISO estándar, huecos/cruces, ISO/GCM, FST, catálogo/cache, guardado/restauración de marcadores, ARC R03 auténtico por hash, 5326 triángulos completos, alturas y tres referencias CP08; contraste independiente Python. No se modifica ninguno de esos algoritmos. La descarga independiente verificó tamaño/SHA256/CRC, PE AMD64 y SourceZip/ledger contra fuente fijada.

Procedencia: los números502/2MiB/+576 son diagnóstico humano comunicado; Codex no recibió ni leyó el CISO comercial ni su cola. Los tests de cola usan datos sintéticos no nulos. La aceptación de este contenedor no demuestra todavía FST/catálogo comercial completo ni geometría de dos salas auténticas adicionales; estos gates continúan HUMAN_PENDING. Los dos mods CP08 no se reconstruyeron ni empaquetaron. CP10 no iniciado.
