# CP07.2C — rango nativo finito E_OC2
Proveedor TEST privado 0.7.4, mismo ID y data_dir. Sólo los registros de encounter_placement@1.0 cambian angle.x de 0x0106 a 0x0132. Cada ACTR de 32 bytes difiere del anterior únicamente en byte 25: 06 → 32. Legacy FIELD/NORTH y native_placement@1.0 conservan 0x0106. Consumidor Bokoblin Expansion 0.1.0 intacto; no instalar otro consumidor.

## Evidencia histórica anterior a la prueba humana
USER_REPORTED: el usuario probó A_ONLY, BOTH, combate y retirada en frío del consumidor; apariciones y ausencia posterior funcionaron. También observó regreso caminando a spawn. No se recibieron rawlogs aquí y no se atribuye su lectura a Codex.
SOURCE_VERIFIED: el código oficial interpreta el byte bajo como rango finito multiplicado por 100; el alto conserva E_OC2. No se cambia IA ni HIO.
HUMAN_RUNTIME_PENDING (al build): determinar si aumenta el movimiento útil y evita la retirada prematura. executeWalk conserva regreso/patrullaje hacia home.pos. 5000 es un parámetro nativo, no persecución visual certificada.

[Fuente y alcance](SOURCE_AND_DIFF.md) · [QA](HUMAN_TEST.md) · [Recuperación](RECOVERY.md) · [Resultados](TEST_RESULTS.md).

Estado posterior al build: **PRIVATE_TEST_READY**, 354 casos y18 negativos, paquete/descarga verificados. [Descarga y hashes](BUILD_AND_PACKAGE.md), [evidencia](evidence/independent-download.json). Fuente compilada 02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd; el checkpoint posterior sólo agrega documentación/evidencia. Ese checkpoint no era un release estable ni contenía aún confirmación del fix en gameplay.

## Cierre humano posterior — 15-10-2026
**CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12**, acotado a A_ONLY/BOTH. El usuario confirmó «Ya hice la prueba y ahora se comportan como los bokoblin normales». Dos logs analizados en ChatGPT y comunicados en el encargo respaldan activación, solicitudes y limpieza; Codex no leyó los originales. Zora Swim 1.3.0 también estaba activo. Véase [acta humana del 15-10-2026](HUMAN_RUNTIME_RESULTS_2026-10-15.md) para hashes, advertencias y límites.
No se acreditan distancias medidas, paridad completa de IA, todos los estados home, cooperación o rendimiento universales. Paquetes, código y fuente compilada permanecen intactos; no se repite QA.
