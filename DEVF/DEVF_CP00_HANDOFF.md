# DEVF_CP00 — Handoff de reanudación
Fecha: 2026-10-11. **CP00 documentado; puerta NO-GO por build Win64 pendiente.** Framework DEVF no implementado ni probado.

Se recuperó el handoff maestro adjunto y su encargo original CP00. La petición del usuario autoriza esta etapa; las instrucciones históricas de esperar prompt ya están satisfechas. Se verificaron ambos ZIP completos disponibles en Git LFS, CRC y SHA256 exactos. El bloqueo de transferencia de 32 MiB está superado.

Repositorio de trabajo: /workspace/Mods-Duskligh, rama work; checkpoint aislado en DEVF/, tag DEVF_CP00. Insumos: /workspace/codex-cp00-inputs, revisión 72b61382d8518a9f727a974e18fae97ec44887fc. Sin push. Fuente de implementación única: ZIP 2.0.3, copia extraída de setup-support contrastada sin diferencias. Handoff maestro copiado en references/ para recuperación.

Se contrastó EXE AMD64 2.0.3.0 con import library exacta (30042 símbolos, cero faltantes), APIs y epoch del SDK, límites de Actor/Stage/Resource y posibles rutas A/B. No se decide herencia de IA ni aislamiento visual. Se preparó un probe mínimo Win64 de imports sin creación de actores, con comando de build SDK standalone sin reconstruir juego.

El Cloud tiene toolchain Linux, sin MSVC/clang-cl/Windows SDK. No se compiló probe Win64; prueba Linux previa conservada sin repetir. **No hay .dusk TEST Windows ni prueba final Windows/DX12.** No instalar ni iniciar CP01.

Leer SOURCES_AND_VERSIONS.md, SERVICE_CAPABILITIES.md, FEASIBILITY_DECISIONS.md, BUILD_ENV.md, TEST_RESULTS.md, GO_NO_GO.md y RESUME_INSTRUCTIONS.md para siguiente acción exclusivamente CP00. CHANGES.md y diff Git delimitan cambios; evidence/input_verification.json conserva datos concretos.
