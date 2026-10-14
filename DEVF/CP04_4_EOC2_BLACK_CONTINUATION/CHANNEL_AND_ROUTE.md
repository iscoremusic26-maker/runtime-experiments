# CP04.4 — Canal efectivo y ruta candidata

Estado: RESOURCE_STATIC_VERIFIED; mecanismo aún pendiente de gate PE/calls y tests, sin TEST admitido. El ARC real coincide con SHA256/tamaños/índices del prompt. Ausencia CLR0/CLR1 confirmada; tres entradas TEX1 oc2_fix apuntan a la misma imagen. Sólo se publica metadata derivada.

MAT3 cuerpo: shapes0/2 → oc_body_mat01/02, COLOR0 de GX_SRC_REG, lighting enabled, ambient GX_SRC_REG, light mask255, diffuse CLAMP, attn SPOT; MatColor0 blanco. Ojos shape1 → oc_eye_mat, misma textura compartida, lighting disabled. Arma oc2_weapon en modelo4 queda intacta. Stage0 RGB: A=KONST(K0 RGB0), B=TEXC, C=RASC, D=C0; ADD, bias0, scale4, clamp, PREV. Alpha: A=ZERO, B=KONST(K3.a255), C=RASA, D=ZERO; ADD, scale1/clamp/PREV. No confundir GX_CC_KONST14 con ONE12.

Ruta A candidata: emitir un comando XF MATCOLOR0 propio de 9 bytes justo antes de drawFast del ShapePacket **de la instancia elegida**, RGB(8,8,10) conservando alpha; después emitir la restauración exacta del registro activo, obtenida de las DL base/diferida leídas sin modificarlas. Mantener TEV, iluminación, texels y matrices nativos. El bound nominal con C0 RGB0 es salida <=(32,32,40); resultado visual pendiente humano. No queda un recurso/callback del mod almacenado en actor/modelo.

Este punto final de geometría sucede después de diffDL y sus regeneraciones/interpolación. Aurora copia comandos FIFO por valor; registra uniforms por draw, de modo que la restauración posterior no altera el draw ya capturado. Un hook tipado de ShapePacket drawFast debe ser único/no inlined y tener una llamada efectiva desde MatPacket.draw en el EXE oficial. Si hay inline sites, no asumir cobertura. Se prepara gate PE focalizado antes de implementar; no se repite auditoría general ni build histórico.

La ruta no escribe ModelData/Material/TEX1 ni modifica los display lists de originales. No se admite aún: falta gate binario, parser/binding guards, pruebas de aliasing/reconstrucción y bracketing. No aplicar TEV temporal sobre Material compartido. No nueva ruta de partículas; CP05/06 fuera de alcance.
