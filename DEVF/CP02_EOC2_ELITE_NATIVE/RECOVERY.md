# Recuperación CP02

Tag ANOTADO **DEVF_CP02_EOC2_ELITE_NATIVE_PACKAGE_VERIFIED**, rama feature/devf-cp02-eoc2-native-elite/[PR21](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/21) draft; el HEAD documental final se obtiene pelando el tag. Fuente compilada `13959231169aedc111c1c5b5cac747bd62e252fd` distinta del documental; CI `d3a85769f096e2d6eb065ddf2d69847ab0b6b8e1` en ci/devf-cp02-eoc2-native-elite/[PR15](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/15). Bases53ceaca4c28653bfb057ac3aaabb18b3624ea19b y09b6464343a2db0d64a643ab06714ef9f042b061 preservadas, sin merge/reset/cherry-pick/reescritura.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp02-recovery.git
git -C devf-cp02-recovery.git rev-parse DEVF_CP02_EOC2_ELITE_NATIVE_PACKAGE_VERIFIED^{commit} refs/heads/feature/devf-cp02-eoc2-native-elite
git -C devf-cp02-recovery.git cat-file -t DEVF_CP02_EOC2_ELITE_NATIVE_PACKAGE_VERIFIED
git -C devf-cp02-recovery.git fsck --full
```

Tag/HEAD deben coincidir y tipo=tag. Solo nuevo DEVF/CP02_EOC2_ELITE_NATIVE/ difiere de CP01; baseline/tag53ceaca, PR20/14/17–19/12–13 e históricos conservados. SOURCE_MANIFEST fija SDK/fuentes/derivación/hash tooling; evidence/historical-pr-status.json registra estado anterior. Reporte humano CP01 es evidencia proporcionada por usuario, no captura de Codex ni log publicado.

CI propio exclusivo privado/baseSHA/head/base exactos. Nueve workflows históricos sin cambios/filtros disjuntos. Checkout CI exacto, SDK40457c6/Aurora3227d76 y LFS Windows con.lib verificada; python ci/run_windows.py --source .official --inputs . --work <scratch> dentro del evento PR especificado. Comandos reales CMake/CL/dumpbin/package en result.json. Windows-latest puede cambiar imagen: versiones registradas, no reproducibilidad byte-a-byte universal prometida. No build del host/juego/DLL execution.

Descargar ambos artefactos de38501242719 antes de vencimiento; ci/verify_download.py --help describe inspección estática con SHA externo, scratch y output. File ledger de checkpoint/evidence persiste aunque expire Actions. Nombre/hashes/internal DLL/source vínculo en BUILD_AND_PACKAGE y download-verification. No necesidad de recuperar originales privados al repo de código.

Prueba humana: HUMAN_TEST. CP01 y CP02 mutuamente excluyentes; proceso cerrado/backups/rutas reales, aprobación explícita, DX12 y caminata normal; no hot reload/teleport/flags. EDIT_REGISTERED no es actor/HP. Render/carga/detección/combate/daño/regresiones/retiradaCP02 NOT_TESTED; CP03 no autorizado. Detener después de entregar.
