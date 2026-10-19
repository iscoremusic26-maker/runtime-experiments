# CP17 — revalidación de continuidad pendiente

66 casos locales ASan/UBSan PASS; nuevo caso de carga continua ante LOS/daño/recoil sin reroll y caso de guardia pasiva que pausa ante recoil seguro. Build/descarga del nuevo source PENDING; HUMAN_RUNTIME_PENDING. Run39184082946 fue SUCCESS del snapshot8fbaea77, pero no certifica esta revisión.

## Histórico preservado del snapshot anterior

# CP17 — cierre técnico verificado (18-10-2026 America/Panama)

**SOURCE_IMPLEMENTED / LAB_PASS / WINDOWS_MSVC_PASS / INDEPENDENT_DOWNLOAD_PASS / HUMAN_RUNTIME_PENDING**.

Fuente REAL compilada `8fbaea77df4fe547676ca2462a6db633f3788273`; CI `a14ca4e264d7b629bb6b02745510300f16bc08ae`. Este cierre documental posterior no cambia el binario. [Run39184082946](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39184082946) build117842721230 + independent-download117843631054 COMPLETED/SUCCESS.

| Gate / función | Evidencia ejecutada | Dictamen |
|---|---|---|
| Red política compartida |64 casos MSVC +64 locales ASan/UBSan |LAB_PASS; LeakSanitizer no ejecutado en ptrace |
| Tasas1.15/3, episodio70%, random12%, pasividad105, cooldowns, continuidad |Mismo header que DLL, fuente nativa y regresiones |SOURCE/LAB/MSVC_PASS; físico humano pendiente |
| Link cargas PROC/const virtual |COFF MSVC auténtico, layout/stubs/u16 y3 checks de lector |RED_LINK_CHARGE_DETECT_SOURCE_AND_MSVC_ABI_PASS_HUMAN_PENDING |
| Aproximación |Intención90, progreso≥5, FIND/obstáculos/correa nativos |NATIVE_FIND_ONLY; boost1.5 NOT_IMPLEMENTED por precedencia unsafe en PRE |
| Hitbox/contacto/SFX/escudo x3 |Port exacto de ventana/traslación/else-if; compensación nativa limitada |SOURCE_EXCERPT_LAB_ONLY; NO ATTACK_X3_HUMAN_PASS |
| FIX01/CP16/CP15 históricos |53 /56 /38 |PASS; CP15 evasion sigue solo histórica, no CP17 |
| CP14 sobre runtime CP17 |16 |PASS de policy; canario físico independiente pendiente |
| CP13/map/legacy |26 /66 /legacy exit0 |PASS |
| Black/variant/damage/dynamic |26 /30 /22 /28 |PASS |
| Strokes/perf/CP12/visual/eyes/texture |36 /4 /7 /22 /9 /20 |PASS |
| Editor CP13/CP08/CP09/multi/nombres |39 /42 /71 /110 /25 |PASS; nombres25 también dentro de multi110, no sumar como únicos |
| Schema C#→C++/C ABI/R03 auténtico vs Python |Fases exit0 |PASS estático, no juego |
| PE/ABI/manifest/exports/imports |AMD64; un execute PRE+POST; solo2 imports adicionales revisados |PASS |
| Negativos Expansion/Provider |10 /19 |PASS; Provider reconstruido solo regresión y no entregado |
| Preservación |2166 blobs fuente base +866 CI base sin cambios;24 runtimefiles iguales;462 blobs pin |PASS por path/blob/mode/type |
| Descarga independiente real |ZIP publicado/.dusk/DLL/CRC/SHA/SourceZip/ledger |PASS |
| Juego CP17/contacto/audio/interrupción/fluidez |No ejecutado por Codex |HUMAN_RUNTIME_PENDING |

523 casos C++ con conteo reportado, más legacy exit0 sin agregación de su conteo; suites UI/lectores separadas y algunas anidadas. No presentar sumas duplicadas como casos únicos.

64 casos: clasificación Red/Blue/Black; tasas B/C frescas/foráneas/clip/stop/recoil/restore; generación/contexto/64slots/semillas; PROC29/2A/2F vs28/30/virtuales; canario negativo;70%/12% reproducibles; cooldowns/anti-rachas;105 pasivo/guardia frente a ataque/dodge/daño/exploración; prioridad de carga, cancelación90, contexto/radio/Y/leash/LOS/pared; recepción SOUND_WATCH; contactos de fuente/ventana14–22; SFX B/C y compensación; presupuesto de logs.

El port usa duración40 como fixture legal, NO como duración medida de BCK. No incluye esqueleto/contacto físico/audio real ni prueba de1.5 de marcha (no implementado). No emitir ATTACK_X3_PASS humano por readback3.

Baseline humana FIX01 comunicada en el encargo: «Mejor. Ahora sí se nota», log185830 identificado por el usuario;47 calls,3 ofertas/consumos/inicios,2 arrived,10 recalls sin LOS actual,61 tasas y54 lockouts Blue. Se atribuye a confirmación humana+extractos comunicados, NO lectura directa del rawlog ausente. No prueba alcance exitoso>1800 ni Red CP17. Canary CP14 lifesteal sigue pendiente.

Primer run39182819992 FAILURE antes de configure/MSVC: source_gate usaba lectura Windows predeterminada y una cabecera UTF-8 produjo charmap. Se fija encoding UTF-8 explícito; no hubo paquete y descarga fue SKIPPED. La telemetría CP17 distingue además lectura PRE actual de NOT_SAMPLED_POST para no interpretar datos no capturados como ausencia de Link. No cambia gameplay.

Segundo run39183207051: configure y compilación/enlace de Expansion DLL correctos, pero msvc global FAILURE al enlazar el helper ABI EXE por GXDestroyTexObj arrastrado por cabeceras. Se reemplaza SOLO ese helper por un target OBJECT y auditoría del COFF real MSVC: sin juego/DLL cargados, sin stubs falsos ni SDK modificado. No paquete, independent-download SKIPPED.

Tercer run39183741446: MSVC SUCCESS y CP17 64/FIX01 53/CP16 56/CP15 38 PASS. Falló el lector COFF por off-by-one: el stub virtual auténtico de10 bytes (JMP indirecto en sus6 bytes finales) no se examinaba en el último índice permitido. Se corrige el límite manteniendo todas las verificaciones de slots/u16/layout y se agregan3 checks de lector (stub real/truncado/no-op). No se generó paquete, independent-download SKIPPED.


## TEST descargado y verificado

[Artifact12157032798 DEVF_CP17_RED_AGGRESSIVE_AI_TEST_39184082946](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39184082946/artifacts/12157032798). Caducidad API2026-11-18T01:13:35Z =17-11-2026 20:13:35 America/Panama. [Verificación descargable12157457479](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39184082946/artifacts/12157457479).

| Archivo | Bytes | SHA256 |
|---|---:|---|
| DEVF_CP17_RED_AGGRESSIVE_AI_TEST.zip interior |1509884 |f70d8df32659bbc1d0d80cd80400462c010fd87974daba36403ebe9b05a58166 |
| BokoblinExpansion_0.14.0_CP17_RED_AGGRESSIVE_AI_TEST.dusk |113055 |d3b888d13c6ca23c91761337e7a2cbbf43794e6ea78f5d9f6f497f9c48fcc461 |
| DLL interna (no suelta) |263680 |886e7cb4260a80e8ca30f47ac8beae5d44ab82f7794c12211d0ee3286d874664 |

El ZIP solo contiene Expansion, documentación, manifiesto/hashes/resultados y fuentes. No Provider/editor/binarios auxiliares ni recursos del juego. El manifest y docs en el SourceZip son snapshots anteriores a independent-download; este cierre y download-result.json registran el resultado final sin alterar el paquete.
