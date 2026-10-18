# Resultados CP16 — TEST privado verificado

**SOURCE_IMPLEMENTED · LAB_PASS · WINDOWS_MSVC_PASS · INDEPENDENT_DOWNLOAD_PASS · HUMAN_RUNTIME_PENDING**

Fuente REAL compilada: `e364fdb1489f7e61a0e0719a62fb627b5749f730`. CI: `a5c33dcc065d6cf7861d00bbe28b40e88b7b2911`. El commit documental posterior no sustituye esta fuente. [Run final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39173568043), build117811511221 e independent-download117812394406: **SUCCESS**. [Descarga privada](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39173568043/artifacts/12153502586), artifact 12153502586, nombre `DEVF_CP16_BLUE_RECRUITER_TEST_39173568043`; requiere sesión GitHub autorizada. Caduca **17-11-2026 17:48:48 América/Panamá** (API: 2026-11-17T22:48:48Z, no expirado al verificar).

| Archivo interior | Bytes | SHA256 |
|---|---:|---|
| DEVF_CP16_BLUE_RECRUITER_TEST.zip | 1192534 | `f665bf0c9eecc3d8ff21f96fa6049719a04363dc39a6f34f6fa4c64bba6c3302` |
| BokoblinExpansion_0.13.0_CP16_TEST.dusk | 99543 | `216e19d91f67039e3ac999c38b0b8bdeb1881f445672bed01e23f959c829ef7b` |
| DLL interna (no distribuir aparte) | 229376 | `2dffc8c0eeec1c52f994d745332d0bff895f7fe3f0a60b5cc3fa46757f0b17f5` |

El ZIP exterior de Actions tiene 1192869 bytes; no confundirlo con el ZIP TEST interior de la tabla. Se entrega SOLO Expansion0.13.0; Provider/editor CP13 se usan para regresión y no se incluyen como binarios.

| Gate | Resultado ejecutado |
|---|---|
| CP16 política real compartida + port de FSM nativa | **56 PASS**, MSVC y ASan/UBSan local; LeakSanitizer no disponible bajo ptrace local, detect_leaks=0 explícito |
| CP15 histórico | 38 PASS en SU cabecera histórica; no se usa su evasión en la DLL CP16 |
| CP14 Red sobre runtime CP16 | 16 PASS de política; NO prueba física de atribución a Link |
| CP13 runtime / runtime mapas / Black / variantes / daño / daño dinámico | 26 /66 /26 /30 /22 /28 PASS |
| strokes / perf / CP12 / visual / ojos / textura | 36 /4 /7 /22 /9 /20 PASS; sin certificar píxeles ni FPS |
| Editor CP13 / app CP08 / importador CP09 / multi / nombres | 39 /42 /71 /110 /25 PASS; hay subcasos reutilizados, no se declara un total de casos únicos |
| Paridad C#→C++ | CP13 32 registros, schema1/schema2/Black PASS |
| Geometría de regresión | R03 auténtico y contraste Python/C# PASS estático; otras salas no se vuelven a acreditar por fixtures |
| ABI/PE | AMD64, ABI1,5 exports, servicios requeridos previos, único hook execute PRE/POST,20 imports game revisados; sin TLS/delay imports |
| Símbolos nativos nuevos | Source tipado + importlib oficial SHA + link MSVC + IAT PE **PASS** |
| Negativos |7 Expansion +19 Provider regresión **PASS** |
| Paquete/descarga | empaquetador oficial, DLL/manifest exactos, CRC/bytes/SHA/SourceZip/376 blobs y CI/source ledger **PASS** en runner independiente |
| Preservación |2.082 blobs históricos conservan SHA/mode/type;22 archivos runtime idénticos; fuera de adaptador Blue solo integración/versionado/telemetría explícitos |
| Movimiento/audio/golpes/FPS de CP16 en Dusklight | **HUMAN_RUNTIME_PENDING** |

Los56 casos nuevos cubren63 destinatarios en tabla64,1800/250, correa propia/margen100 y rango0 nativo, stale/contexto/generación, dos Blue, no dominó, rondas150 sin límite lógico, calma150, espera240 y fallback, progreso real del RECEPTOR (no crédito por moverse el convocante), marcha/no llamada, muro/agua/caída en mundo sintético, grito solicitado vs WATCH4/BCK7 observado, tasas/bloqueos CP15. El port de SOUND_WATCH/WATCH/FIND no es el motor ni KCL físico. ARRIVED exige movimiento receptor y proximidad actual; aproximación de Blue a receptor quieto se registra como proximidad, no como marcha del aliado.

Se preservó toda la lógica Red/Black y los filtros/bonificaciones CP10.6/CP15. Incidencia PREVIA comunicada por usuario: `LINK_LAYOUT_CANARY_FAILED_LIFESTEAL_DISABLED`; CP16 no la corrige, no certifica lifesteal runtime y no fingió leer el rawlog `dusklight-20261018-161906.log`. El reporte humano CP15 fue favorable salvo su huida defectuosa, que se elimina; no acredita universalmente nivel3 ni rendimiento.

## Trazabilidad de iteraciones

Run39172622838: **FAIL**, MSVC detectó una referencia residual de telemetría inicial a AiLine.d1/kEvadeRadius eliminados; no produjo TEST. Se conserva evidencia. Run39172880087: SUCCESS de revisión intermedia53 casos. Run39173249440: SUCCESS de revisión intermedia54 casos. Única entrega final: **39173568043 / fuente e364fdb… /56 casos**, que añade medición de progreso independiente del movimiento del convocante. No se reutilizan hashes de paquetes intermedios.

QA y rollback: [HUMAN_TEST.md](HUMAN_TEST.md), [RECOVERY.md](RECOVERY.md). El manifiesto verificable está en [VERIFIED_PACKAGE.json](VERIFIED_PACKAGE.json). No se ejecutó el juego ni se instalaron mods en la PC del usuario. PR72 y CI57 permanecen draft/open/unmerged; sin tags/releases ni CP17.
