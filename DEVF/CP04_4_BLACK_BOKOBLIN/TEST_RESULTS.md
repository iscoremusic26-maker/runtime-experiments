# CP04.4 — Resultados y límites

Dictamen **CP04_4_BLOCKED_WITH_EVIDENCE**. PASS_STATIC indica lectura de fuente exacta y relaciones del código, no ejecución C++ ni GPU.

| Comprobación | Resultado | Evidencia / alcance |
| --- | --- | --- |
| Acceso repositorio privado / base CP03 / nuevo checkpoint temprano | PASS_STATIC | Rama nueva y commit a3c6b934e27c40c2044dfc6c83eb835c0b0a1c95 recuperados mediante GitHub. PR30 draft. |
| Cosmetics: copia texels y registro SOURCE sin ActorId | PASS_STATIC | Referencias en ROOT_CAUSE; contrato SDK y registro contrastados. |
| Model de instancia frente a ModelData/material/shape/texture compartidos | PASS_STATIC | Model.cpp/create packets y CreateHeap nativo. |
| DiffDL por shape privada, incluso en batching | PASS_STATIC | MatPacket.draw ejecuta diffDL de cada ShapePacket. No confundir “material compartido” con “no existe nada privado”. |
| VertexBuffer/current color pointer de instancia | PASS_STATIC | Datos base prestados; frameInit reinicia; setter y calculador nativo existen. |
| Interpolación captura y vuelve a calcular materiales/diff | PASS_STATIC | material.cpp y mDoExt; snapshots no constituyen un owner de copia visual del mod. |
| FIFO copia comandos; streaming de frame copia arrays/uniforms; backend D3D12 | PASS_STATIC | Aurora exacta. Se distinguen los puntos de consumo. |
| Canales/TEV/CLR0 y cobertura cuerpo/ojos/arma de E_OC2 efectivo | NOT_VERIFIED | Evidencia de archivos anterior corresponde a E_oc normal; E_OC2 efectivo no examinado. |
| Modelo/material privado completamente attachado y retirado | NOT_VERIFIED | Loader/fábricas existen; no se acreditó grafo propietario ni fence/retiro. |
| Cambio temporal shared TEV + restore | BLOCKED como solución | No se demostraron todas las fases/caches/intercalaciones. No se implementó. |
| Dos E_OC2 mismo modelo/frame, sólo DEVF negro | NOT_TESTED | Sin implementación admitida; no hay fake test presentado como prueba. |
| Reentrada/muerte/partial allocation/ActorId reciclado/out-of-order draw/shutdown/release visual | NOT_TESTED | Se exige cobertura una vez elegido mecanismo válido; no se repiten suites CP01–03. |
| Build CP04.4 MSVC/Windows SDK | NOT_RUN | No hay fuente de mod admitida; Cloud failed. Verificación Git en Windows no es build MSVC. |
| PE/AMD64/ABI/imports/exports/hook nuevo | NOT_RUN | Ninguna DLL CP04.4 generada. No reutilizar los PASS del binario CP03 como auditoría de CP04.4. |
| Paquete .dusk, CRC/manifest/DLL interna/descarga real | NOT_RUN | Sin paquete, hashes, tamaño o caducidad nuevos. |
| Visual negro / iluminación / combate / limpieza runtime / reversión CP04.4 | NOT_TESTED | No se ejecutó juego; requiere evidencia humana. |
| Preservación Git / procedencia / tag nuevo en runner Windows | PENDING hasta CI | Workflow de evidencia, sin compilación ni paquete; se registrará su resultado y logs al terminar. |

El script propio `tools/verify_checkpoint.py` verifica el alcance del diff desde CP03, hashes Git de las fuentes referenciadas y rangos de citas. No demuestra aislamiento, GPU, ABI, alloc/free ni material effectiveness. No genera un artefacto funcional.

La referencia HP150 humana CP03 conserva su PASS anterior; no se reejecutó ni se adjudica a un recoloreado nuevo. El NO-GO runtime de partículas CP04.3 se tomó del relato explícito del usuario; no se publicó/reanalizó un log privado. No se modificó instalación, ejecutable, ISO, SDK, Aurora ni partidas.
