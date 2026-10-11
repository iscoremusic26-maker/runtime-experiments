# Resultados — CP00 Windows
| Comprobación | Estado | Evidencia |
|---|---|---|
| ZIP exactos, SHA256/CRC, fuente extraída | PASS | input_verification.json; repetición solo en nuevos runners Windows |
| EXE AMD64 2.0.3.0 e import library | PASS | 30042 imports presentes en EXE |
| Original checkpoint recuperable de GitHub | PASS | fetch en repo temporal vacío, objeto 8a14628 y tag original intactos |
| Acceso runner a ZIP privados por LFS | PASS | checkout mismo repositorio, GITHUB_TOKEN contents:read; sin secretos nuevos |
| Run 38183814814 | FAIL | generador VS2022 no instalado en windows-latest actual |
| Run 38183965513 | FAIL | configuración MSVC/SDK PASS; C2440 por __cplusplus antiguo y macro nullptr de Aurora |
| Run 38184111122 | PASS | build/package/enlace, PE, exports e imports |
| Run 38184306482 | PASS | resultado final; añade versiones/flags exactos de registros de servicios y hashes en logs |
| DLL y .dusk nativos | PASS | AMD64, exports lifecycle/mod_meta, import dusklight.exe/fopAcM_SearchByID |
| Versión de registros requeridos | PASS estático | Actor 1.0, Stage 1.0, Resource 1.1, Host 2.2, Log 1.0, Game 2.0; records Win64 de 80 bytes |
| Resolución real del loader / guardas de host | NOT_TESTED | no se ejecutó el juego |
| Actor/Stage lifecycle, IA, colisión, apariencia y DX12 | NOT_TESTED | etapas posteriores; CP01 NOT_STARTED |
| Smoke Linux previo | PREVIOUSLY_COMPLETED | preservado; no se repitió ni se atribuyó a Windows |

MSVC 19.51.36260.0, Windows SDK 10.0.26100.0, Windows Server 2025, Visual Studio 2026, RelWithDebInfo x64. Build: 4 advertencias C4805 en JSUIosBase (referencia SDK), 0 errores; no ocultadas. Ver evidence/run-4-build-excerpt.log y windows-verification.json. Build reproducible por commits/inputs fijados; no se afirma determinismo binario (PE/ZIP llevan metadatos temporales).

El artefacto generado es un probe de compilación, sin autorización de instalación, sin prueba real del host y sin acreditación del mod DEVF final.
