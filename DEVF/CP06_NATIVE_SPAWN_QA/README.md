# CP06 — QA de apariciones nativas: norte y dos sitios

**A: NORTH_NATIVE_QA_BUILD_READY.**  
**B: DUAL_NATIVE_QA_BUILT / HUMAN_TEST_BLOCKED_UNTIL_NORTH_PASS.**

Dos paquetes privados distintos, versión 0.6.1, compilados con MSVC para Dusklight oficial 2.0.3 Windows x64/DX12. A registra una entrada nativa en el candidato norte; B registra dos: sitio 1 y norte. No requieren JSON. Instalar **un solo .dusk DEVF a la vez**.

Los dos usan registros E_oc nativos de 0x20 bytes, sin hooks ni intervención en HP, color o IA. StageActorHandle identifica una edición, no un ActorId. El número de altas aceptadas **no demuestra enemigos aparecidos**.

| Paquete | Mod ID | Entradas |
| --- | --- | --- |
| A | `dev.devf.cp06_qa_north_native` | Norte solamente |
| B | `dev.devf.cp06_qa_dual_native` | Sitio 1 + norte; probar sólo después de A satisfactorio |

Escenario fijo: F_SP121, sala 3, capa 6. Sitio 1 conserva (-1250, -6304.00830078125, 60750). Norte usa X=-1250, Z=61950: suelo KCL calculado Y=-6327.600450915229 y margen inicial +5, serializado como float32 **Y=-6322.6005859375**. El asentamiento real está pendiente de QA humano.

- [Control estático incremental del norte](NORTH_QA_SCREEN.md): permite un ensayo controlado; no acredita SITE2 como seguro.
- [Implementación](IMPLEMENTATION.md): conteo fijo, rollback de handles propios y límites de limpieza.
- [Resultados](TEST_RESULTS.md): 24 casos de laboratorio, PE/ABI, seis negativos por DLL y descarga independiente.
- [Paquetes, hashes y CI](BUILD_AND_PACKAGE.md).
- [Prueba humana y rollback](HUMAN_TEST.md).
- [Recuperación exacta](RECOVERY.md).

Fuente realmente compilada: **689f79c1c785bea31715d814f7d03818a7f0dd72**. Los informes posteriores y el verificador de descarga no cambian ese snapshot ni sus paquetes.

El CP06 v0.6.0 humano probado y todos sus checkpoints permanecen intactos. La personalización multiinstancia y el CP06 general siguen pendientes; estos QA sólo prueban altas nativas. No se ejecutó el juego. No se inició CP07/CP08, postura ni Bokoblin Expansion.
