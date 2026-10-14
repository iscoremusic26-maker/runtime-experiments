# Pruebas CP02 focalizadas

| Gate | Estado y evidencia |
|---|---|
| MSVC Windows x64 compile/link | PASS, [run38501242719](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38501242719)/job115648464135; MSVC19.51.36260, VCTools14.51.36231, SDK10.0.26100.0, CMake4.4.3/Ninja Release |
| Fake StageService del código real |11/11 PASS ejecutados ahora: success/reentry/reject/zero-handle/throw/missing/wrong-host/small-stage/null-add/wrong-stage-major/null-context |
| Campos nuevos y BE32 | PASS: aliasE_oc, room3/layer6/XYZ/setID; wordFFFF0100 = bytesFF FF 01 00; angle0106 = bytes01 06; logID/v0.2.0/expectativaE_OC2 |
| Exactamente un add, fallos/reentry/handle0 | PASS según cada escenario;1000 updates no agregan llamadas y shutdown idempotente; no retries |
| Grafo producción | PASS: solo src/mod.cpp + SDKgame_feature.cpp; ningún test/tripwire en DLL |
| PE ABI/máquina/services/export/import | PASS_STATIC: AMD64, ABI1, Host2.2/Log1/Stage1/Game2; cinco exports oficiales;20 CRT/system por identidad, cero imports dusklight.exe/GX |
| Negativos PE |3/3 PASS, x86 machine, ActorService metadata, export name alterado; DLL propia solo inspeccionada, nunca cargada |
| Paquete oficial `.dusk` | PASS: miembros/rutas únicos, no traversal/alias/symlink/cifrado/extras, CRC/SHA/tamaños/manifest/DLL interna==suelta |
| Descarga verdadera desde CI privado | DOWNLOAD_VERIFIED: digest GitHub de ambos ZIP, external manifest byte-idéntico al texto del run, source ledger, PE/exports y CRC/SHA comprobados |
| CP01 humano | USER_REPORTED_PASS para aparición/aspecto/vida/animación y ausencia tras retiro; original log no adjunto a esta tarea, no nuevo juego ejecutado |
| CP02 carga/modelo/vida real/detección/combate/daño exacto/retirada/regresiones/DX12 | NOT_TESTED; espera aprobación y sesión humana |

La fuente CP02 y las expectativas de bytes/telemetría difieren de CP01, por lo que sus hashes no son equivalentes: se ejecutaron11 casos cortos derivados, no se presentó el lab CP01 como prueba del nuevo payload. No reejecución de CP00/CP01, KCL/WRock/Digpl, suites100/104/46 o matrices antiguas. Inspección ZIP reutiliza herramientas/hash-contracts intactos; no nuevas suites masivas.

El tripwire GX de aborto, establecido en CP01, resuelve exclusivamente un COMDAT de header sin uso en el laboratorio y hace fallar el proceso si se invoca incluso al salir. Once procesos terminaron0. No fallback de GPU, no producción ni prueba render. La variante no usa memoria de actores existentes, ActorService/patch/delete/profile/hook/overlay; solo add de ACTR propio.

Source/commands/versiones/map/imports/exports/metadata/CRC/hashes en evidence/windows-run-38501242719. Fases 2026-10-14T02:29:47.844224+00:00→2026-10-14T02:30:03.239988+00:00 (~15,40s, aparte de setup/uploads); comandos/exits/segundos reales en result.json. Un run, sin fallos/reintentos. No host build/juego/DLL cargado en CI o workspace.
