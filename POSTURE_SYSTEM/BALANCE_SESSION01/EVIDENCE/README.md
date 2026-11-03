# Evidencias0.11.2

SOURCE_COMPARISON y CI_SOURCE_LEDGER corresponden al commit compilado, anterior al cierre documental. GXX_LABS/GXX_MUTATIONS son modelos compilados contra producción; MSVC_RESULT_SANITIZED recoge fases/contadores/versiones sin comandos o rutas del runner. Su estado de build precede a la descarga: los veredictos finales están en CI_DOWNLOAD_VERIFICATION y LOCAL_DOWNLOAD_VERIFICATION, con el mismo hash. Ambos jobs figuran SUCCESS en CI_JOBS.

STORE_AUDIT_BASELINE_DLL y STORE_AUDIT_FINAL_DLL verifican las escrituras acotadas de defensa manual/R+B; SOURCE_NUMERIC_SCOPE y los32pins de funciones/10cabeceras comprueban el alcance heredado. PE_NEGATIVES y los dos negativos de stores son rechazos deliberados de mutaciones estáticas, sin cargar código nativo. CLASSIFICATION_SOURCES distingue políticas vendorizadas de la integración original CP21 consultada por separado.

No hay logs humanos ni capturas del juego; no se afirma haber leído el log0.11.1 no disponible. Las nuevas mecánicas siguen HUMAN_RUNTIME_PENDING. Los demás mods, DEVF CP10, host/SDK/EXE y partidas no se modificaron.
