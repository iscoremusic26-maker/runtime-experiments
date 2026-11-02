# Evidencia de FIX01

El paquete final fue descargado por artifact ID y verificado localmente; el job independiente de CI también descargó el archivo publicado. Los dos JSON de verificación tienen el mismo SHA-256. MSVC_RESULT_SANITIZED conserva resultados, versiones, dependencias y fases sin comandos, rutas del runner o logs de entorno. GXX_LABS y GXX_MUTATIONS son ejecuciones locales ASAN+UBSAN y mutaciones de modelo. SOURCE_COMPARE corresponde al commit compilado, antes del commit documental.

DOWNLOAD_METADATA_NEGATIVE contiene ARTIFACT_VERIFY_FAIL de forma intencional: prueba que el verificador rechaza la declaración obsoleta del artefacto intermedio. PE_NEGATIVES y PMF_STATIC_TESTS también son casos negativos deliberados. Ningún DLL ni materializador nativo fue cargado/ejecutado. Las direcciones en NATIVE_COLLISION_ABI y NEW_WRITER_BINARY_REVIEW son constantes del binario auditado, no direcciones de una sesión del usuario.

No se publica un log humano ni se afirma haber leído el log de0.10.0 no disponible. Renders de laboratorio, ejecución sintética y compilación no prueban compatibilidad jugable o rendimiento: HUMAN_RUNTIME_PENDING.
