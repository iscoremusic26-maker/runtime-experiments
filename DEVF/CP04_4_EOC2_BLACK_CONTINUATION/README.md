# DEVF CP04.4 — E_OC2 negro por instancia, TEST privado

> **Nota documental posterior (2026-10-14 Panamá).** Estado posterior a la build: **CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED** en el flujo reportado; tres logs/cinco generaciones y observaciones humanas. Comparador simultáneo E_OC2 idéntico pendiente. El tag documental nuevo sigue bloqueado por la interfaz disponible. Ver [cierre humano y límites](HUMAN_RUNTIME_RESULTS_2026-10-14.md). Las menciones siguientes a HUMAN_RUNTIME_NOT_TESTED/pendientes describen el estado histórico **en el momento de la build**; se conservan sin reescribir historia.

**CP04_4_EOC2_BLACK_PRIVATE_TEST_READY**. Aislamiento de código **CODE_ISOLATED_OFFLINE**; apariencia/combate/limpieza en esta versión **HUMAN_RUNTIME_NOT_TESTED**. No se ejecutó juego ni se cargó la DLL en CI.

Mod nuevo: `dev.devf.cp04_eoc2_black` versión0.4.4. Un E_OC2 adicional nativo en F_SP121/3/6, home(-1250,-6304.00830078125,60750), HP220→150 mediante la misma escritura única PRE_FIRST_EXECUTE de CP03, sin cambiar field_0x560. Incluye la telemetría y las políticas CP03 necesarias; se instala **solo**, nunca junto al .dusk CP03/CP04 anterior.

El cuerpo de su modelo principal (shapes0/2) recibe color de material oscuro durante su propia llamada de packet, mediante un comando XF privado de9 bytes y su restauración exacta. Se mantienen texturas/TEV/normales/luces/alpha nativos. Ojos shape1, accesorio y modelos/packets originales quedan excluidos. No hay textura reemplazada por hash, buffer CLR0 ficticio, material/DL compartido modificado, clon de modelo, heap visual nuevo, partícula ni callback guardado en un actor.

La entrada HookService es el helper común J3DShapePacket::drawFast: **observa llamadas comunes y filtra ActorId+generación/identidad/escena/modelo/packet antes de emitir**. Sólo la instancia CP03 admitida puede entrar. No se reemplaza el método original ni se hacen detours manuales. Ver [CHANNEL_AND_ROUTE.md](CHANNEL_AND_ROUTE.md), incluidos límites de convivencia con otros hooks.

[Descarga privada de Actions](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492/artifacts/11936739368) — artifact11936739368, ZIP45231 bytes, SHA256 `e7b05803b687324c6f5eace8d3e2954b7e5b26d819f05e7de7d03bf5c2a8ca49`. Contiene un .dusk nuevo, MANIFEST.json, SHA256SUMS.txt y SOURCE_COMPILED.zip; sin recursos originales.
- .dusk:15287 bytes, SHA256 `a1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9`.
- DLL interna:28672 bytes, SHA256 `b61e47ed9cc1ee461469fab1f8fa7df38cca9045e17f14e12341657d9cb07f06`.
- Caducidad actual del artifact: 2026-11-13 18:59:41 (Panamá, UTC−05:00); UTC 2026-11-13T23:59:41Z. No se publicó release ni se promete disponibilidad posterior.

Fuente compilada: `ee42f62d2bd2bbbfae9e61affb10c066fd0588af`. CI build `565b16f44a9eb338e4d2018c27f2c1bad8caf4f9`, [run38657297492](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492). [Descarga real independiente38658291368](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38658291368), sin recompilar. Ver TEST_RESULTS y BUILD_AND_PACKAGE.

Se mantienen íntegros CP03 humano y su paquete11975 bytes/SHA0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344, y todos los archivos del cierre CP04.4 `0b2216eec658402aec2470e0df0080e399294225`. El ARC real permanece sólo en inputs privado. No se repitieron CP01–03, el estudio de32 fuentes, ubicación ni partículas. No host/SDK/Aurora/ISO/saves modificados; CP05/06 no iniciados.

[HUMAN_TEST.md](HUMAN_TEST.md) contiene instalación, control del mismo E_OC2 y rollback. APPLIED significa readback del comando privado, no píxeles ni VISUAL_PASS.
