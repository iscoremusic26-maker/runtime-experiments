# CP04.4 — Canal efectivo y aislamiento por llamada de packet

Estado: implementación preparada; gate de llamada del EXE PASS; build/ABI/paquete/descarga todavía pendientes. No declarar TEST_READY hasta verificarlos. HUMAN_RUNTIME_NOT_TESTED.

## Recurso efectivo y matriz de control

E_oc2.arc real del commit privado6b32ef995814e6a20924d6b6dd3fe5886a5ef3e0: SHA256c87d7a3cb6087ff5bcb8be3abab64b2b1124fe90bba0118ab61e174349bba394,33872 bytes, CRC32ee2501dd. Yaz0→RARC47296 bytes, sin trailing bytes, índices3/4 y hashes de ambos BMD coincidentes. Contraste independiente en Windows, run38655133336; no son píxeles ni equivalencia contra overrides instalados. No se distribuyen bytes/texels.

| Modelo/shape/material | Canal nativo | Base | Candidato privado | Estado compartido |
| --- | --- | --- | --- | --- |
| index3 shape0/material0 oc_body_mat01 | COLOR0: lighting1, matSrc REG0, ambSrc REG0, mask255, diffuse CLAMP2, attenuation SPOT1 | MatColor0 RGBA255; TEX index2 | MATCOLOR0 RGB escalado por (8,8,10)/255, alpha exacta; TEV original | Sólo lectura de Material/Texture/baseDL |
| index3 shape2/material1 oc_body_mat02 | Igual al anterior | MatColor0 RGBA255; TEX index1 | Igual, sólo su packet DEVF | Sólo lectura |
| index3 shape1/material2 oc_eye_mat | COLOR0 matSrc REG, lighting0 | TEX index0 | Sin comando nuevo | Original intacto |
| index4 shape0/material0 oc2_weapon | Iluminación1 y TEX ob2_1_1 RGB56532×64 | Nativo | Modelo accesorio excluido por identidad de modelo | Original intacto |

Los tres TEX oc2_fix CMPR128×128 del cuerpo/ojos apuntan a los mismos texels. No hay CLR0/CLR1 ni arrays de color; no se crea un buffer CLR0 ni se usa TextureService.

Los cuatro materiales tienen stage0 RGB=(A=KONST K0 RGB0, B=TEXC, C=RASC, D=C0), ADD, bias0, escala4, clamp, PREV. **14 es GX_CC_KONST; ONE es12.** Alpha=(ZERO,KONST K3.a255,RASA,ZERO), ADD, escala1, clamp, PREV. La expresión RGB viva con C0=0 es4×textura×raster. Aurora calcula raster=MatColor×clamp(iluminación,0,1); multiplicar sólo MatColor RGB por(8,8,10)/255 conserva variación de textura/normales/luces y limita el valor nominal a(32,32,40)/255 antes de fog. Alpha no se cambia; C0/TEV/muerte nativos no se reescriben. El resultado estético y la influencia de fog necesitan prueba humana.

## Ruta A elegida: comandos privados en la llamada del ShapePacket elegido

HookService oficial tipado PRE/POST sobre el helper común J3DShapePacket::drawFast, sin reemplazar la función ni instalar detours manuales. El dispatcher observa las llamadas de ese helper y filtra antes de emitir. El punto de entrada de servicio es común a packets, pero la escritura de comandos sólo se admite después de resolver **el ActorId CP03 previamente autorizado**, verificar toda identidad/escena/mName/estado2, identidad de su modelo principal y dirección exacta de su packet shape0/2. No census/proximidad. Los packets de otros actores, ojos y accesorio no reciben comandos del mod.

La instancia tiene packets propios que aún apuntan a material/shape compartido. Se verifica el contrato efectivo del cuerpo/ojos/TEV/Texture sin escribirlo. ColorBlock registra getMatColorOffset dentro de la DL base; se lee su batch XF exacto de dos palabras, con bounds/header/tamaño. No se escanea memoria. mDiffFlag exacto0x11000084 no contiene MatColor: la DL diferida que ya se ejecutó no sobreescribe ese MATCOLOR0 base.

PRE emite un **array propio de9 bytes** XF0x100C; el original dibuja una vez; POST emite la restauración exacta obtenida de la DL nativa. No se cambia J3DModelData, J3DMaterial, J3DShape, TEX1, buffers DL base/diferidos, matrices ni posiciones. Se conserva el alpha y el estado TEV, y se elimina la necesidad de clonar modelos o gestionar heaps visuales. Ruta B no es necesaria y no se abre.

Este bracketing NO es una escritura temporal al TEV compartido. Es una secuencia explícita en el stream: [MatColor privado][geometría del packet elegido][MatColor anterior]. Las buffers del comando son propios; el registro es estado de dibujo GX transitorio. No se alega que el registro GX sea un recurso privado. Se restaura para no dejar estado persistente a ojos/originales.

## Captura, reconstrucción y lifetime

- J3DMatPacket::draw ejecuta diffDL **por shape** antes de drawFast; POST ocurre antes de tomar el siguiente packet de la cadena, incluidos originales agrupados por el mismo MaterialID.
- No se parchea una diffDL susceptible de regeneración: cada entrada efectiva a geometría se vuelve a acotar después de calcMaterial/diff/interpolación. prepare_presentation_view sólo combina matrices y no altera MATCOLOR0.
- GXCallDisplayList copia los9 bytes a FIFO **antes de retornar**; no guarda la dirección del array del mod. Las geometrías nativas siguen su propiedad habitual.
- Aurora consume en orden. XF0x100C actualiza MatColor y marca DirtyUniform; genera un uniformRange por draw. Prefix y restore invalidan el merge de draws con distinto uniform. Restaurar no modifica los uniforms ya copiados ni captura futuros colores retroactivamente.
- POST no desreferencia packet/actor/modelo: usa sólo palabras e identidad de llamada guardadas. Tras retornar no queda puntero a recurso o modelo en estado del mod; sólo ActorId/generación.
- Sin allocations de recursos del mod, calculadores virtuales, texturas privadas, vtables del mod en actores, ni callbacks de render almacenados en escena. HostService/HookService conservan sólo los callbacks registrados y los retiran al detach según el contrato oficial ya usado por CP03. No hot reload.
- PRE/POST usan prioridad última/primera respectivamente para acotar la función nativa. El método original revisado no invoca otros ShapePacket::drawFast recursivamente. Nested/out-of-order/missing POST activa rechazo y restauración fail-closed; no se afirma compatibilidad con un tercer mod que reimplemente o haga recursiva esta función.
- Fallo parcial/modelo no creado/cambios de escena/identidad errónea no emiten. Scope cerrado antes de destrucción normal; nueva generación requiere la admisión CP03. Se liberan sólo escalares propios. El OOM fatal interno del host/FIFO no es una garantía de recuperación de este mod y no se probó.
- El recurso instalado puede tener overrides; guardas MAT3-like, texturas/canales/shape y contrato de DL rechazan discrepancias. No se afirma hash del recurso ya transformado en memoria ni píxeles correctos sólo por APPLIED.

## Evidencia de código exacto, sólo funciones pendientes

Dusklight40457c6adb381928e4b5fef6ed459ed291edd5e2:
- libs/JSystem/include/JSystem/J3DGraphLoader/J3DMaterialFactory.h:15–49, layout MAT3; J3DModelLoader.h:106–145, tablas.
- libs/JSystem/include/JSystem/J3DGraphBase/J3DTevs.h:88–94, mapping semántico de stage; J3DMatBlock.h:102–143, canales.
- libs/JSystem/src/J3DGraphBase/J3DMatBlock.cpp:10–19 y329–346, batch MatColor y offset; J3DMaterial.cpp:199–209/253–268, DL base/diferida.
- libs/JSystem/src/J3DGraphBase/J3DPacket.cpp:213–245/342–413, orden por packet; J3DShape.cpp:311–349, geometrías sin modificar color; J3DShapeDraw.cpp:174–176, envío de geometría.
- libs/JSystem/src/J3DGraphAnimator/J3DModel.cpp:115–122, presentación sólo matrices.
Aurora3227d76c60e1e782ca576610bce61c9e7744d8be:
- lib/dolphin/gx/GXDispList.cpp:48–62, copia/publicación; lib/gx/fifo.cpp:149–169, copia.
- lib/gx/regs.cpp:717–727/839–845, registro MatColor y DirtyUniform; lib/gx/shader.cpp:779–867, iluminación.
- lib/gx/command_processor.cpp:382–472/491–506, uniforms y merge. La revisión sellada de32 fuentes se conserva, no se ejecuta de nuevo.

Gate binario focalizado run38655854048: EXE oficial SHAffa992…049, AMD64, llamada efectiva MatPacket.draw→ShapePacket.drawFast, sin inline sites. MULTI_NAME indica exactamente nombre MSVC, display y source-qualified de la MISMA función, sin nombre ajeno; se verificó el allowlist exacto. Se publica sólo metadata, no direcciones/bytes del EXE.
