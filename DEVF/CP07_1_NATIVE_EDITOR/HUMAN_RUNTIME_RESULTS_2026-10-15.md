# CP07.1 — observación humana posterior al TEST

**CP07_1_HUMAN_RUNTIME_OBSERVED**, limitado al reporte de dos sesiones Windows x64/D3D12 del usuario. Versión0.7.0, ID dev.devf.cp06_native_config_dual; fuente compilada c084729a36661cc6992843baca99f40b3c8211e2, cierre build/descarga f11006f73e84f3aed0427773c5e185aa5345fe42.

| Sesión | Fuente de evidencia | Hechos reportados |
| --- | --- | --- |
| dusklight-20261015-115005.log | USER_LOG_SUMMARY_ANALYZED_IN_CHATGPT | UI_MENU_REGISTERED; CONFIG_ACCEPTED_STAGE_EDITS_REGISTERED; configured=1, edits=1; D3D12; cierre normal |
| dusklight-20261015-115119.log | USER_LOG_SUMMARY_ANALYZED_IN_CHATGPT | UI_MENU_REGISTERED; CONFIG_ACCEPTED_STAGE_EDITS_REGISTERED; configured=2, edits=2; D3D12; cierre normal |

USER_HUMAN_REPORTED: el editor funcionó perfectamente sin anomalías observadas; el usuario confirmó visualmente interfaz, opciones y apariciones esperadas. El resumen no informa error crítico atribuible a DEVF. Codex no recibió bytes de estos logs ni capturas: no calculó hashes ni inspeccionó píxeles. No se atribuye ActorId a placement, ni se infieren ensayos de FPS, compatibilidad universal, fallos de energía o pruebas adversariales.

REPO/CI_VERIFIED al recuperar: [build38770105933](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933) SUCCESS,109+55casos y11negativos; [descarga38770449006](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770449006) SUCCESS. Ya documentados en el checkpoint f11006…; no se repiten ni se reempaqueta0.7.0.
.dusk39591bytes/SHA256c1070b6e4fa53f6cfa5e6f77640c30383351dc3dae10964f06edbb77e962cd46; ZIP87947bytes/SHA2569033029e6c4fef90d29ff24d42943910072204b31285946f3e1dfda44f31dc14. Paquete histórico y refs intactos.
La nueva API de mods dependientes es un trabajo separado, aún sin prueba humana; estos PASS no se transfieren al proveedor/consumidor nuevo.
