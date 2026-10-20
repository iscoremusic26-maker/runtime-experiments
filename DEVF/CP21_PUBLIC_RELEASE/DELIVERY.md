# CP21 — entrega privada verificada

Estado: **SOURCE_IMPLEMENTED · LAB_PASS · WINDOWS_MSVC_PASS · INDEPENDENT_DOWNLOAD_PASS · HUMAN_RUNTIME_PENDING**.

[Descargar TEST privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39359746319/artifacts/12237111893) · [CI y auditoría independiente](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39359746319). Caduca: **2026-11-19T02:42:15Z**. No es un release público.

## Pareja para instalar

Instalar y activar únicamente estos dos `.dusk` en Dusklight **2.0.3 Windows x64 DirectX 12**. Conservar una sola copia instalada por ID. No hace falta un editor ni configurar archivos JSON.

| Archivo | Bytes | SHA256 |
| --- | ---: | --- |
| `BokoblinExpansion_0.17.0.dusk` | 1912586 | `083de98ca6a9e5918470ebbc31f720e700bdb25dedc4b52d19f863cfc7611e2a` |
| `EnemyVariantFramework_0.15.0.dusk` | 103765 | `51f24f178969dd22d438ecfcc7336c043e7d72f05c29a91248a8f41f405ef1d5` |

Nombres visibles exactos: **Enemy Variant Framework** (0.15.0) y **Bokoblin Expansion** (0.17.0), autor **Fran**. IDs técnicos conservados: `dev.devf.cp06_native_config_dual` y `dev.bokoblin.expansion`. Los servicios nativos, V1 y V1.1 conservan sus IDs y ABI; no hay dependencia del editor.

## Fuente y referencias

- Fuente compilada: `192a7731623d69baacdd37011db60ce894d9de18` en [PR fuente #81, DRAFT](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/81).
- CI compilada: `341c7a341980c3982d2a1e2671e7852f3ef1d550` en [PR CI #66, DRAFT](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/66).
- Baseline compilado CP20: `2ce550395ff69d2c9046a2d3e0b635024307ce1e`; cierre documental `d9f83eaabff549440a10a33c002bf8e2e37945a6`. PR #80 y CI #65 permanecen intactos.
- Entradas: `inputs/devf-cp21-public-release-assets-20261019` en `16a9089c18ce17f7daf1a2ff7d37593f7b552bf1`.
- Dusklight oficial: `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Se verifica `docs/modding.md` desde su objeto Git exacto y la equivalencia de saltos de línea del checkout. Cada CMake de mod usa `RES_DIR res`.

El TEST incluye `SOURCE_COMPILED.zip`, `SOURCE_PIN.json`, `TEST_RESULTS.json`, `VERIFICATION_MANIFEST.json` y `SHA256SUMS.txt`. El ledger propio de CP21 tiene 84 blobs. El snapshot heredado de regresión corresponde por separado al CP20 compilado, sin alterar checkpoints. No se distribuye ningún ejecutable de editor.

## Datos e implementación

El Framework inicia un core aceptado y listo con cero ubicaciones legacy, conserva StageService/broker/ownership/lifecycle y no importa ni registra UiService. La ruta pública no lee `placements.json`. La Expansion pasa al parser existente `multi_config::decode` el documento integrado inmutable y no lee ni escribe `encounters.json` del jugador. Los archivos externos viejos no se suman.

Se preservan los **32/32** encuentros, **15 Blue / 7 Red / 10 Black**, Black con **HP configurado 440**, F_SP121, layer 6, rooms 0, 2, 7, 9, 10 y 12, seis recursos. IDs, orden, coordenadas a precisión float32, yaw, parámetros, autorizaciones y metadatos proceden exclusivamente del JSON congelado. No se movió ni eliminó ningún encuentro.

GitHub usa LF: 18.449 bytes, SHA256 `786afe55dfadd0811cb53012aec7417f0886d2874cab63b0f9ae87ee01487e53`. Restaurar CRLF reproduce exactamente el original: 19.164 bytes, SHA256 `67a1d7109949e9a18071ff06592f24c2cf0d54093cf76cc07efd6dad730e74aa`. La diferencia es únicamente de saltos de línea. El gate de compilación rechaza cambios de hash, identidades, cantidad, autorización, recursos, HP, posición, yaw, layer, orden y metadatos.

Los cuatro PNG originales coinciden en SHA256, dimensiones y CRC de sus chunks. Se verifican de nuevo dentro de los dos `.dusk` realmente descargados, bajo `res/icon.png` y `res/banner.png`, sin alterar sus bytes.

## Pruebas y límites

- Fuente: 42 archivos runtime idénticos a CP20; el adaptador de combate solo cambia el include de configuración, la llamada de entrada, su mensaje de error y versión. Parser compartido, client, broker, ownership, rollback y políticas de combate permanecen intactos.
- Laboratorio CP21: 11 casos, incluidos entrypoints reales del Framework con servicios simulados; cuatro combinaciones de archivos externos presentes/ausentes; cero lecturas y pares legacy; 32 ediciones de los datos del usuario; rechazo de duplicados/ownership incorrecto, detach, reinstalación lógica, Framework ausente y rollback de fallos 1/16/32. Registros nativos 0x0032 E_OC / 0x0132 E_OC2 y floats verificados.
- Regresiones completas de FIX02 y CP20 bajo MSVC, corpus parser de 85 documentos, 141 casos CP20, compatibilidad V1/V1.1, 9 casos legacy, 30 de variantes, 40 FIX02 y 16 Red; ABI C y COFF de los headers oficiales. Ninguna guarda se desactiva para obtener PASS.
- Paquetes: cuatro archivos funcionales exactos por `.dusk`; manifiesto, ID, nombre, versión, autor, PNG, CRC, SHA256, PE AMD64, exports, imports, hooks y ausencia de strings/UI de desarrollo. Negativos de binarios, manifiestos, assets faltantes/alterados y archivos extra rechazados. La auditoría independiente descarga el artifact subido y vuelve a comprobar los bytes y el ledger de fuente.

**Codex no ejecutó el juego.** El laboratorio no demuestra aparición de actores, terreno, combate, audio ni reingreso real a salas. Esas observaciones siguen en **HUMAN_RUNTIME_PENDING**, con pasos en [HUMAN_TEST.md](HUMAN_TEST.md).

Riesgo conocido: `LINK_LAYOUT_CANARY_FAILED_LIFESTEAL_DISABLED` de Red permanece pendiente si vuelve a aparecer. No se afirma que lifesteal Red esté corregido. No se amplió el trabajo a cambios de combate.

## Rollback y aprobación

Cerrar Dusklight, retirar los dos bundles CP21 y restaurar la pareja previamente respaldada fuera de la carpeta de mods; reiniciar. No conservar duplicados por ID. CP21 no modifica JSON del jugador, host, SDK, ejecutable, ROM/CISO, saves ni mods de producción. La retirada limpia ediciones propias; los actores ya cargados pueden requerir recarga de escena o reinicio. Véase [RECOVERY.md](RECOVERY.md).

Los PR siguen **DRAFT**, sin merge, tag ni release. Este cierre documental no cambia los binarios compilados ni el pin que contienen. Tras la validación humana corresponde solicitar una aprobación separada antes de cualquier release público.
