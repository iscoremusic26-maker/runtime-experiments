# Recuperación de la decisión CP03

Revisión documental en `feature/devf-cp03-hp150-feasibility`, descendiente directa de `0d2430262181bb2844f13bb8da0a628f71740998`. No se crea tag CP03 de PASS: el pedido reserva ese checkpoint/tag de implementación para un PASS offline. El commit documental publicado y su rama permiten recuperar la evidencia sin afirmar implementación.

```bash
git clone --single-branch --branch feature/devf-cp03-hp150-feasibility https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp03-review
git -C devf-cp03-review log -1 --format='%H %s'
git -C devf-cp03-review fsck --full
git -C devf-cp03-review diff --name-only 0d2430262181bb2844f13bb8da0a628f71740998 HEAD
```

El diff debe contener exclusivamente `DEVF/CP03_BOKOBLIN_HP150/`. La PR documental es DRAFT y no se hace merge. CP02 branch/tag deben continuar resolviendo 0d243026..., tag anotado 453ef09e8f6551313af8261f0e96fa7a6e160d95; el tag CP01 continúa en 53ceaca4c28653bfb057ac3aaabb18b3624ea19b. CI CP02 sigue en `d3a85769f096e2d6eb065ddf2d69847ab0b6b8e1` (rama `ci/devf-cp02-eoc2-native-elite`); no se creó rama, workflow o PR de CI CP03.

Reproducción de procedencia, utilizando checkout oficial exacto y CI histórico limpio existentes:

```bash
python DEVF/CP03_BOKOBLIN_HP150/tools/collect_source_evidence.py --source /ruta/dusklight-v2.0.3 --main /ruta/devf-cp03-review --ci /ruta/ci-cp02 --output /tmp/cp03-source-provenance.json
```

La herramienta lee 21 fuentes acotadas, compara objetos Git con checkout, comprueba 52 entradas del ledger CP02 y hashes de SOURCE_MANIFEST; inventaría funciones de cuatro servicios. No configura CMake, carga DLL, ejecuta el juego ni automatiza un PASS semántico. Las conclusiones se revisan en FEASIBILITY_GATE y BLOCKER_REPORT. No precisa ARC ni logs del usuario. Para recuperar el tag base en un clone single-branch sin sobrescribir refs:

```bash
git -C devf-cp03-review fetch origin tag DEVF_CP02_EOC2_ELITE_NATIVE_PACKAGE_VERIFIED
```

CI histórico 38501242719 está completed/success; no se vuelven a ejecutar compilaciones, suites ni descargas. SHA de la .lib histórica `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4` se conserva como pin documentado, sin extraer o redistribuir originales otra vez.

Continuar únicamente tras decisión explícita sobre el contrato de 150 HP. No reutilizar CP02 DLL renombrándola, instalar un CP03 inexistente, editar el histórico, activar G5 ni avanzar a CP04.
