# Puerta CP01
**NO-GO para avanzar a CP02 o aprobar un TEST de juego.**

La build nativa y el laboratorio del controlador/ciclo de recursos se verifican por separado en TEST_RESULTS.md. No existe una ubicación segura acreditada para activar StageService en producción y no está demostrada la seguridad de destrucción de instancias/solicitudes pendientes antes de descargar la DLL. El host descarga aun si la limpieza devuelve error.

Las apariciones permanecen desactivadas. El actor, controlador y pruebas están implementados hasta el alcance verificable del entorno; no se declara PASS de aparición, dibujo, colisión, cambio de sala o limpieza dentro del juego. No se emite DEVF_CP01_TEST.dusk. La build diagnóstica se identifica BUILD ONLY.

Para cerrar CP01: obtener evidencia de ubicación real válida y completar allí la integración Stage sin doble spawn; demostrar creación/destrucción y recursos, cambios de sala/capa/escena, fallo temprano y salida segura del proceso/host, resolviendo el unload dentro de alcance autorizado. No parchear motor ni adoptar CP02 por defecto.
