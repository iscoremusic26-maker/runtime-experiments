# G0/G4 — contexto concreto y evidencia pendiente

**Escenario de observación: F_SP121, room3, layer lógico6, Hyrule Field antes del puente hacia Kakariko. Ubicación adicional de E_OC: NOT_VERIFIED. G4 BLOCKED.** La fuente y los registros permiten seleccionar un contexto real; todavía no permiten aprobar una posición nueva para este enemigo.

Datos ya observados y conservados: entry -4; Link `(-4056.7346,-6717.1538,65135.8281)`, angle s16 -24697. Entry no es layer. El layer6 depende del progreso/override y difiere de layer0/14; no se fuerza ningún flag para obtenerlo.

El punto anterior de WRock `(-4806.7346,-6729.480961460304,65135.8281)`, yaw0, escala1, queda **solo como punto de análisis pendiente del enemigo**, no como posición validada de spawn. Se conserva soporte KCL/PLC, pendientes/altura muestreadas, caja WRock, geometrías externas, rutas y Digpl de CP01/LOCATION_ANALYSIS.md y sus JSON, sin recalcular. Los 27 puntos Digpl y mínimo565.6961 a aquella caja, y la ruta a115.6156, no excluyen la envolvente animada/persecución de E_OC. Su rango2000 no cabe dentro de la garantía de esa caja. No se traslada ningún PASS de WRock a modelo/arma/colliders/movimiento de E_OC.

Los siete `E_oc` originales en ACT6 de R03 están en selection-static.json. Dos configuran E_OC y cinco E_OC2. Sus coordenadas son emplazamientos vanilla ocupados, no espacios libres para una adición. ACTR/SCOB común y ACT6/SCO6, stage común/layer6, eventos/colisiones/triggers y límites de la revisión anterior permanecen como baseline. La cantidad live, posiciones móviles, ramas de progreso y otras cargas solo se conocerán con observación. No se sustituye ni ajusta ningún original.

## Admisión FILI y carga

Lectura incremental exclusiva de FILI del **room.dzr ya decodificado** y contrastado con su hash conservado `4404905dfa33fe90058c14a670b8a33f6236584d8db0f806f3931368d3068a6e`:

- mParameters `0x1FE07FB8`; EnemyAppear1Flag=false (`&0x20000000`).
- mBitSw `0xFF`, offset público del formato0x1B.
- `fopAc_Create` (`f_op_actor.cpp:519–538`) solo aplica el filtro genérico de grupo ENEMY si bitSw !=0xFF: **este filtro concreto está desactivado por los datos originales**. No se modifica ni falsea nada.
- Preset E_OC con switches de derrota/secundario0xFF; ausencia del filtro no prueba admisión completa, creación phase completada, progreso inalterado ni identidad de los recursos cargados en Windows.

La ruta A1 requiere una única Add antes de carga **natural** de la sala, cuya ROOM_SCENE/roomReLoader hereda CURRENT. Registrar edit no crea inmediatamente; remover edit no mata instancias; recargar puede crear de nuevo. No se invoca roomReLoader ni se escribe fpcLy_CurrentLayer. Las entradas/salidas naturales exactas y permanencia de la sala deben registrarse en G2; no se usa warp, editor, cambio de layer o flags.

## Recursos específicos faltantes

| Ruta virtual nativa | Para qué se necesita | Estado |
|---|---|---|
| `/res/Object/E_OC.arc` | Modelo3, arma4, joints/materiales y envolvente espacial del candidato normal | NOT_VERIFIED: no localizado en los recursos recuperados |
| `/res/Object/E_ocb.arc` | Animación0x1B inicial y las de Execute; envolvente de cuerpo/arma en movimiento | NOT_VERIFIED: no localizado |
| `/res/Object/E_OC2.arc` | Interpretar los cinco E_oc vanilla de variante2 y sus recursos; no necesario para el modelo del nuevo E_OC normal | Pendiente de baseline, no justifica ampliar el candidato |

El código de dRes construye esos nombres con `/res/Object/` y `.arc`. Son rutas del sistema de recursos, no una afirmación de que existan como archivos sueltos en la instalación Windows. Si se resuelven desde un contenedor, solo serían necesarias esas extracciones privadas y hashes mediante un procedimiento autorizado, nunca ROM/ZIP completos ya acreditados. No se copiaron recursos originales al repositorio de código ni a artefactos.

El observador consulta únicamente existencia de entradas por nombre con `dComIfG_getObjectResInfo`; no carga archivos ni consulta modelos/índices. `registered=true` significa referencia registrada, **no carga/phase completa ni integridad del archivo**. False tampoco prueba ausencia del archivo instalado. La consulta exacta de E_OC2 se reserva a evidencia del baseline; no se añade una lectura innecesaria del objeto.

## Qué falta para un punto seguro

1. Evidencia privada de E_OC/E_ocb: hash, estructura, índices, modelos/joints/animaciones y dimensiones. Reutilizar suelo/geometría ya calculados cuando cubran la nueva envolvente; estudiar solo superficies adicionales si la envolvente sale de lo acreditado.
2. G2 oficial: identidad host/build y DX12, lista de mods/configuración, sala/layer y owners coherentes, sin transición ni creación/destrucción, censo vanilla y recursos del caso. No se deduce DX12 por compilar un DLL.
3. Un punto adicional con yaw y suelo acreditados para E_OC, sin solapamiento original ni interferencia de arma, movimiento/aliados/eventos/rutas/Digpl, y sin necesidad de flags o bypass. **Hoy no se acredita ese punto.**
4. Condiciones de entrada/salida y progresión estables; método observacional que distinga la futura única adición de un spawn vanilla/evento. Si falta identidad, se detiene G5.

Acción mínima siguiente: autorización específica posterior para G2 sin spawn; en paralelo aportar únicamente E_OC/E_ocb privados si se quiere cerrar la envolvente estática. Esta tarea no solicita ejecutar ni entregar nuevos archivos ahora.
