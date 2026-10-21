# Uso y mantenimiento de este atlas

Estas instrucciones son locales a `DUSKLIGHT_RESEARCH/`. No garantizan carga automática desde otra carpeta, otro repositorio ni una ejecución nueva. En un encargo nuevo, indicar explícitamente: «Lee primero DUSKLIGHT_RESEARCH/AGENTS.md, README.md, SOURCE_PIN.md y CONTINUATION.md de la rama research/dusklight-203-dusk-atlas».

1. Consultar el atlas antes de repetir búsquedas; comprobar el SHA upstream `40457c6adb381928e4b5fef6ed459ed291edd5e2`. No combinar HEAD/tag móvil con evidencia del pin.
2. Leer CONTINUATION.md y RESEARCH_COVERAGE.md. Inventariado, localizado, examinado y contrastado son niveles distintos; localizar una ruta no implica comprenderla.
3. Usar SYSTEM_INDEX.json para localizar proveedores/consumidores y SYMBOL_INDEX.json para firmas y condiciones; seguir siempre sus evidence_ids hasta EVIDENCE_LEDGER.json.
4. Leer implementación y usos antes de promover una hipótesis. Incluir repo, SHA, ruta, líneas reales y enlace permanente. No inventar offsets ni disponibilidad Windows. Las entradas API se documentan como metadatos, sin líneas ficticias.
5. Preferir un servicio oficial cuando cubra el contrato. TYPED_HOOK/SYMBOL_HOOK requieren firma, resolución real y ciclo de vida propios; la clasificación del mecanismo no certifica una instalación runtime.
6. Mantener explícitas las incógnitas de SDK, callbacks, unload, saves, escenarios y backends. No convertir CI o laboratorio en observación del juego. No usar PASS como etiqueta global.
7. Este encargo es investigación: solo documentos, índices y utilidades auxiliares de lectura/análisis. No modificar fuente, SDK, assets, host, ejecutables, saves ni configuración del jugador; no producir ni compilar mods.
8. En la rama aislada, versionar exclusivamente resultados bajo `DUSKLIGHT_RESEARCH/`. No versionar el prompt ni copiar archivos fuente o assets protegidos. Conservar ramas y PR previos; sin merge, release, tag o force-push.
9. Cada bloque actualiza ledger, índices, cobertura, preguntas y CONTINUATION; ejecutar `tools/validate_atlas.py` cuando esté disponible. Revisar diff y asegurar que todos los cambios permanecen bajo esta carpeta.
10. Los scripts deben escribir fuera de la fuente analizada y emitir metadatos. No ejecutar descargas o builds como efecto colateral de un índice.

Los archivos históricos del repositorio tienen contexto y permisos de sus propios encargos. En este atlas se reutilizan solamente descubrimientos generales con procedencia precisa, sin reabrir proyectos ni modificar checkpoints cerrados.
