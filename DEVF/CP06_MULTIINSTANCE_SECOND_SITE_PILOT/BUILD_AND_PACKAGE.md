# Build y paquete

**NO NEW BUILD / NO NEW PACKAGE / NO NEW DOWNLOAD.** No fuente de DLL multiinstancia compilada, mod_id nuevo, .dusk, ZIP, DLL ni artifact TEST. Runner Python Windows no es BUILD_PASS MSVC.

| Operación nueva | CI / run |
| --- | --- |
| Sello fijo del cierre anterior | db254b9fa7d2714e4bb647b1880cac11b18fa5ba / [38744256177](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38744256177), SUCCESS |
| Consultas estáticas de dos puntos | inputs98bbb027c91e4cabc9629f370971345c887a958c / [38744954662](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38744954662), SUCCESS; sin artifacts |

Comandos del estudio: `git lfs pull --include=DEVF_CP01_EVIDENCIA_F_SP121.zip`; `python DEVF/CP06_MULTIINSTANCE_SECOND_SITE_PILOT/ci/review_sites.py`. El runner llama site_query.py dos veces, X=-1250,Z61950/59550, cache en RUNNER_TEMP; no juego. Logs privados leídos realmente; sólo metadata derivada preservada. Fuentes oficiales leídas por API en40457c6…, no EXE ni host compilado.

## Rollback histórico intacto

Fuente compilada original107c79987b0d3d1d28319654739a72bd498271bb, dev.devf.cp06_single_site v0.6.0:

| Objeto | Bytes | SHA256 histórico |
| --- | ---: | --- |
| .dusk CP06 PARTIAL SINGLE SITE | 41419 | b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2 |
| DLL interna | 77824 | 45effe8a0ac9d56c3921c2cd6d0a27e9ea7017821559ef96b94b21ff390214e0 |
| ZIP TEST | 83222 | e79a0e76d3471530927ca169bbe4cbe107689b36200a63119ace012d261a10a1 |

[Artifact histórico11951843169](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831/artifacts/11951843169), caduca2026-11-14 01:04 Panamá/06:04Z. [Build38690126831](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831) y [descarga38690375002](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690375002) históricos, sin nueva ejecución, recálculo binario ni reempaquetado. No se atribuyen al commit presente.
