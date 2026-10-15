# Entrega a Codex — cierre documental DEVF CP07.2C (15-10-2026)

> Encargo preparado desde ChatGPT y depositado directamente en la rama del PR #47 porque el entorno Cloud no está disponible. Este documento es una instrucción para Codex, **no una afirmación de que Codex ya haya ejecutado el cierre**.

## Objetivo

Cierra **solo documentalmente** la incidencia CP07.2C, respaldado por dos pruebas humanas reales de Dusklight 2.0.3 / Windows / D3D12. La observación textual del usuario es: **«Ya hice la prueba y ahora se comportan como los bokoblin normales».** La corrección nativa del radio de movimiento fue satisfactoria para los encuentros nuevos en el alcance de las dos sesiones. No es necesario investigar ni modificar más la IA.

## Fuente de verdad y repositorios

- Principal (privado): https://github.com/iscoremusic26-maker/Mods-Duskligh ; PR #47 https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/47 ; rama `feature/devf-cp07-2c-eoc2-native-range-5000`.
- Base pre-QA del PR47: `e2e937b060700801f04143624abd3217a3664db4` (verificar HEAD real y preservar este hito). Fuente verdaderamente compilada: `02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd`.
- Base histórica CP07.2B inmutable: `7c588d2a06d307b0288256fc2383186129430401`, PR #46. CI repo `iscoremusic26-maker/codex-cp00-inputs`, PR #33. Mantener draft/sin merge.
- Directorio documental: `DEVF/CP07_2C_EOC2_NATIVE_RANGE/` (`README.md`, `TEST_RESULTS.md`, `HUMAN_TEST.md`, `HANDOFF.md`, `RECOVERY.md`, `SOURCE_AND_DIFF.md`, `BUILD_AND_PACKAGE.md`).
- Fuente original del juego: Dusklight `40457c6adb381928e4b5fef6ed459ed291edd5e2`; archivo `src/d/actor/d_a_e_oc.cpp`. No analizarla de nuevo: el comportamiento y la parametrización ya se revisaron y la prueba humana fue positiva.

## Corrección técnica YA terminada; no editar código

- En nuevos encuentros E_OC2 de `EncounterBroker::record`, solo `angle.x` cambia de `0x0106` a `0x0132` (600 -> 5000 unidades de rango radial nativo). Registros legacy FIELD/NORTH preservan `0x0106`.
- IDs/API `dev.devf.native_placement@1.0` y `dev.devf.encounter_placement@1.0` permanecen intactos. Consumidor `Bokoblin Expansion 0.1.0` inalterado.
- Proveedor `DEVF 0.7.4` `.dusk`: 129925 bytes, SHA256 `934a0a1a5127fa994b9325a5f94a493d0df53f3b5f9af9acfce3709006379fbb`.
- Consumidor `0.1.0` `.dusk`: 24439 bytes, SHA256 `104a6c0908f498b0a833b7ed31d12e75f224bc2f232633bd921446c217d2333f`.
- Paquete proveedor, run CI `38812099184`, artifact `12009156482`, ZIP SHA256 `89258783b1d776d762f6b62c71d8bb1cefdd9086f8c3771ddec09ab137278464`. Verificación independiente run `38812605127` PASS. Laboratorio 354 PASS, 18 negativos PE/ZIP rechazados. No repetir estos gates.

## QA humana, resumen verificado a partir de DOS logs ORIGINALES

Los dos logs se revisaron localmente por ChatGPT antes de crear este documento. **No se suben los logs crudos**, pues contienen rutas locales y metadatos personales. Codex NO debe decir que leyó los logs originales si solo puede consultar este extracto. Estos hashes sirven como evidencia de identidad para el usuario.

| Sesión | Log original (NO publicado) | Bytes | SHA256 | Líneas | DEBUG/INFO/WARNING | ERROR/FATAL |
|---|---|---:|---|---:|---|---|
| A_ONLY (un encounter) | `dusklight-20261015-172414.log` | 312045 | `9d74edb7c57b1c92f41d54fe3dd75ab942ac723547ed62983d19c31b51eb0bf7` | 4041 | 3799/66/156 | 0/0 |
| BOTH (dos encounters) | `dusklight-20261015-172617.log` | 310547 | `6cd5e68f758f596fecd2d3aecb678987ce42aa63c7c14ec57283b901a173eff4` | 4024 | 3792/70/142 | 0/0 |

En **ambas** sesiones se registraron Dusklight 2.0.3 (revisión citada), D3D12, DEVF Provider `0.7.4` (fuente `02e907...`), consumidor Bokoblin Expansion `0.1.0` (fuente `5446365...`), otro mod Zora Swim `1.3.0`, y `3/3` mods activos. Proveedor indicó `configured=0 edits=0` para los slots FIELD/NORTH legacy. No presentar el test como aislado de todo otro mod.

- **A_ONLY**: una solicitud aceptada de `encounter-1`, token 1, `result=0`; retiro de token 1 con `result=0`, limpieza del consumidor/proveedor y `all mods unloaded`.
- **BOTH**: dos solicitudes aceptadas de `encounter-1` token 1 y `encounter-2` token 2, todas con `result=0`; retiro en orden inverso 2 y 1, limpieza y `all mods unloaded`.
- Los mensajes `actor_id=NOT_OBSERVED` y `evidence=STAGE_EDIT_ONLY` no verifican un enemigo vivo ni estados internos de IA. La normalidad de comportamiento viene **solo de la observación del usuario**, no de los registros.
- Advertencias no atribuibles causalmente a este cambio según estos logs: A_ONLY 122 de `aurora::texture` y 34 de `dusk` (CalcDivideInfo); BOTH 112 y 30 respectivamente. No ocultarlas, tampoco afirmar que ya existían antes de esta prueba o que son globalmente irrelevantes.

## Dictamen autorizado

**`CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12` (acotado)**: el usuario confirma gameplay con comportamiento comparable al de Bokoblins normales, junto con evidencia de activación, una/dos solicitudes de encuentro y limpieza correctas en logs Windows/DX12. No alegar distancias medidas, video, medición del radio visible, paridad completa de IA del juego original, todos los estados de `executeWalk/home`, cooperación universal, desempeño general ni release estable. No afirmar que Codex ejecutó el juego.

## Trabajo preciso que debe hacer Codex

1. Consultar PR47 y el HEAD real. Si se añadió este documento al PR47, trabajar desde el HEAD actualizado sin sobrescribir la base ni los cambios ajenos. Identificar que este archivo es un **encargo pendiente**, no el acta final.
2. Crear acta `DEVF/CP07_2C_EOC2_NATIVE_RANGE/HUMAN_RUNTIME_RESULTS_2026-10-15.md`: fecha, dictamen textual exacto, observación humana, correlación A_ONLY/BOTH, fuentes/log-hashes y métricas de esta tabla, advertencias, límites, y veredicto acotado. **No añadir rutas del usuario, logs crudos ni información privada**.
3. Ajustar exclusivamente los documentos de CP07.2C que hoy dicen `HUMAN_RUNTIME_PENDING` como estado actual (`README.md`, `TEST_RESULTS.md`, `HANDOFF.md`, `HUMAN_TEST.md`, `RECOVERY.md` si corresponde). Conservar marcas históricas y manifiestos congelados sin falsear la cronología; diferenciar `SOURCE_VERIFIED`, `BUILD_PASS`, `DOWNLOAD_VERIFIED` y `USER_OBSERVED_RUNTIME_PASS`.
4. Actualizar la descripción de PR47 (o publicar comentario final con enlace al acta) manteniéndolo **draft/sin merge**. No modificar PR33 ni PR46 ni sus HEAD salvo una justificación estrictamente necesaria; no iniciar otro PR, CI o release por este cierre.
5. Verificar diff acotado a Markdown/documentación. Ningún cambio C/C++, headers, JSON operativo, scripts/CI, DLL/.dusk, host, SDK, ROM, assets ni tags; no reset/rebase/amend/force-push/merge/retag.
6. Entregar en español: enlace al acta y commit de cierre, listado de archivos modificados, PR47 actualizado/draft, hashes de logs y `.dusk`, diferencia entre HEAD documental y fuente compilada, y recomendación de seguir con la próxima funcionalidad sin reabrir la incidencia resuelta.

**No recompilar, no crear nuevos mods, no pedir nuevas pruebas y no declarar que los logs originales están subidos.** Si no puedes ejecutar cambios en GitHub, explica el bloqueo concreto y presenta un diff honesto. No reportes una acción como realizada hasta comprobarla.

## Procedencia y privacidad

Este handoff fue elaborado a partir del reporte directo del usuario, de sus dos logs originales revisados localmente y de la fuente/PR47 existente. Solo se publica una descripción depurada, hashes y resultados de registro. Los originales siguen fuera del repositorio. Esta publicación NO supone por sí sola que Codex haya trabajado o que el cierre documental final esté hecho.
