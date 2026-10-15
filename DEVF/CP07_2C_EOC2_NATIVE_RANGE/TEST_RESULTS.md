# Resultados — CP07.2C
Dictamen técnico: **CP07_2C_NATIVE_RANGE_5000_PRIVATE_TEST_READY**. Dictamen de gameplay **al build**: HUMAN_RUNTIME_PENDING. Dictamen posterior: **CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12** (acotado); véase [acta humana del 15-10-2026](HUMAN_RUNTIME_RESULTS_2026-10-15.md).

| Gate | Estado | Evidencia |
|---|---|---|
| Interpretación nativa de angle.x | SOURCE_VERIFIED | create L2728–2738, blob 57828ccb7c987757929835da38623d8a6b04ebbd del host oficial fijado |
| A/B sólo byte25 06→32, alto01 | LAB_PASS | C++ real compartido + comparación independiente Python, 32 bytes por record |
| Legacy FIELD/NORTH/probe 0106 intactos | LAB_PASS / BINARY_ABI_VERIFIED | comparación completa, cliente histórico descargado sin recompilar |
| 0/1/2 solicitudes, límites, rollback/detach | LAB_PASS | 70 expansión +50 API existentes y 8 focales; dobles de servicios, no gameplay |
| Core/editor/captura/colección | LAB_PASS | 109+55+62 regresiones; ninguna implementación de esas rutas cambió |
| Windows/MSVC x64, C11/C++20, PE/ABI | BUILD_PASS | run 38812099184, 18 negativos rechazados |
| .dusk/manifest/DLL oficial | PACKAGE_VERIFIED | identidad 0.7.4, dos servicios 1.0, hooks0, sin imports nuevos |
| Runner independiente descarga real | DOWNLOAD_VERIFIED | run 38812605127; SHA/bytes/CRC/70 fuentes/PE |
| Consumidor 0.1.0, probe y proveedor 0.7.3 originales | DOWNLOAD_ABI_VERIFIED | ZIP/DLL/source originales; sin ejecución ni reempaquetado |
| Rango útil/persecución/retirada, al build | HUMAN_RUNTIME_PENDING histórico | posteriormente cerrado por observación del usuario |
| Comportamiento comparable a Bokoblins normales en A_ONLY/BOTH | USER_OBSERVED_RUNTIME_PASS acotado | declaración humana y dos extractos de logs; ver acta |
| Patrullaje/home de executeWalk, cooperación general | NOT_CERTIFIED | se conservan rutas nativas; no eliminación de todo retorno |

USER_REPORTED (fase previa CP07.2B): A_ONLY, BOTH, combate y ausencia de adicionales tras retirar consumidor funcionaron. También se observó regreso caminando hacia spawn. No se recibieron los rawlogs de esa prueba aquí; no se atribuye su análisis a Codex ni se repiten los gates de aparición como pendientes.

- A anterior: `455f6f6300000000ffff010045a896c7c5af1d974748f24e0106f68b0000ffff`; nuevo: `455f6f6300000000ffff010045a896c7c5af1d974748f24e0132f68b0000ffff`.
- B anterior: `455f6f6300000000ffff0100455c8c84c5b6d70a474801180106b81e0000ffff`; nuevo: `455f6f6300000000ffff0100455c8c84c5b6d70a474801180132b81e0000ffff`.
Legacy: FIELD `455f6f6300000000ffff0100c49c4000c5c50011476d4e00010600000000ffff`; NORTH `455f6f6300000000ffff0100c49c4000c5c594ce4771fe00010600000000ffff`.

Primer verificador falló por orden físico de modmeta, no por contenido ABI; corrección y run fallido conservados en [BUILD_AND_PACKAGE](BUILD_AND_PACKAGE.md). No se ocultó el fallo ni se regeneró el paquete.
Codex y los runners no ejecutaron el juego/DLL/GPU. El usuario sí ejecutó las dos sesiones Windows/DX12 posteriores documentadas en el acta. No se midieron FPS, KCL/navegación ni cooperación universal. No se asigna ActorId a un placement ni se certifica aislamiento universal.

Cierre exclusivamente documental desde el encargo 684d027c1c73be5d083dfa6754e10fe3fc2ae066; sin nuevas compilaciones ni cambios de binarios. Los recuentos de los logs son datos comunicados por ChatGPT, no recalculados aquí.
