# DEVF_CP00 — checkpoint Windows actualizado
Fecha: 2026-10-11. **GO técnico CP00: build MSVC/Windows SDK y verificación estática PASS. CP01 no iniciado. Juego/DX12 NOT_TESTED.**

Se conserva el análisis e inventario previo. Original commit 8a146281e236e715b94c173b8cb9f309396bb75b y tag DEVF_CP00 publicados intactos en GitHub, recuperados por fetch en repo temporal vacío. Desarrollo solo CP00 en rama checkpoint/devf-cp00-windows-20261011 de iscoremusic26-maker/Mods-Duskligh. Tag actualizado adicional: DEVF_CP00_WINDOWS, sin mover el original ni force push.

CI corre en una rama nueva de codex-cp00-inputs para leer sus ZIP privados con token del mismo repositorio. PR #1 en borrador, sin merge automático. Sus ZIP y main no cambiaron. Mirror del probe/scripts documentado por commit y SHA256 en DEVF/CP00_SOURCE.json. La autoridad principal sigue siendo fuente ZIP exacta 2.0.3.

Dos fallos corregidos de alcance CP00: selección de VS instalado en windows-latest y /Zc:__cplusplus para Aurora. Encabezados Aurora fijados al gitlink exacto de v2.0.3, externos al ZIP; no se modificó ni recompiló el juego. La build final usa MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0, x64 RelWithDebInfo. Run 38184306482 PASS, incluyendo paquete, PE, exports, import real del EXE y versiones de servicios. Historial de runs y logs en evidence/ y BUILD_ENV.md.

Se produjo únicamente probe de compilación. No se probó loader/servicios dentro del host, rechazo runtime de versión, actors/lifecycle/escenarios, IA, colisión, render ni DX12. No instalado en PC. No framework DEVF ni CP01 implementados. Ver GO_NO_GO.md para alcance exacto de la puerta original y TEST_RESULTS.md para limitaciones.

Las rutas A/B y propuesta CP02 previas se preservan, sin reabrir 2.0.2 ni resolver prematuramente IA/apariencia. No se repitió smoke Linux. Leer RESUME_INSTRUCTIONS.md; no iniciar CP01 sin un nuevo encargo.
