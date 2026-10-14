# CP03 — piloto privado E_OC2 con salud inicial de 150

**SOURCE_VERIFIED · BUILD_PASS · PACKAGE_VERIFIED · DOWNLOAD_VERIFIED · HUMAN_RUNTIME_NOT_TESTED.** Listo para una prueba humana controlada en Windows x64/DX12; todavía no es CP03 PASS_RUNTIME ni una versión estable. CP04 no está autorizado.

StageService 1.0 añade una entrada nativa. HookService oficial 1.1 permite escribir una sola vez `health=150` en la primera creación de la instancia identificada. Se conserva la IA, recursos y combate nativos de CP02. No usa ActorService, callbacks de solicitud, hooks manuales, cambios de perfil, `field_0x560` ni modificaciones del host o SDK.

Registro conservado: E_oc, F_SP121, sala 3, capa 6, XYZ `(-1250, -6304.0083, 60750)`, parameters `0xFFFF0100`, angle `(262,0,0)`, setID `0xFFFF`. La identidad exige coincidencia exacta del registro y fase de creación; no selecciona por proximidad. No se afirma que 150 HP equivalgan a una cantidad de golpes.

- [Descargar TEST privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38513406897/artifacts/11870393231): `.dusk` de **8953 bytes**, SHA256 `5754a47e84d56563cfb4143139aa0f4660b6852ce409e30b84fd398b0cfe3229`.
- [CI Windows aprobado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38513406897): MSVC 19.51.36260 x64 y Windows SDK 10.0.26100.0.
- Fuente compilada: `b39e010d1a25168dee8de0c2c7740957d76dd853`; CI: `4f84a7137011a35f0500dc7ae1104420e58fbb30`.
- Recuperación: tag `DEVF_CP03_STAGE_HOOK_HP150_OFFLINE_TEST`, rama `feature/devf-cp03-stage-hook-hp150`, [PR24](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/24). CI independiente en [PR16](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/16). Ambos draft, sin merge.

El checkpoint documental final añade evidencia sin cambiar el código compilado. Conserva CP01, CP02 y las revisiones CP03 anteriores. Base funcional: `0d2430262181bb2844f13bb8da0a628f71740998`.

[Fuente](SOURCE_REVIEW.md), [compilación y descarga](BUILD_AND_PACKAGE.md), [matriz de pruebas](TEST_RESULTS.md), [recuperación](RECOVERY.md) y [prueba humana/reversión](HUMAN_TEST.md). No se ha instalado el paquete, cargado su DLL ni ejecutado el juego desde Codex.
