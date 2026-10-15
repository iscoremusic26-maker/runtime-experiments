# CP05 — Piloto acotado de guardia E_OC2

Estado inicial: SOURCE_GATE_IN_PROGRESS; ningún TEST CP05 publicado. Base exacta f7a6623f6d931bacef6f2c8e54f46f7476780ade; no cambiar CP04.4 ni sus binarios.

Sello humano CP04.4 completado por run38671493020: tag anotado DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14, objeto f21d0d95e0fc7d5fcbca15ae17ba6b50cdee564e, destino f7a6623f6d931bacef6f2c8e54f46f7476780ade, leído por API. Workflow separado/tag-only en PR33; PR31/32 intactos.

Hallazgo fuente40457c6: parámetros CP03 FFFF0100 y home.angle.x=0106 producen mPlayerRange=5000 y mMoveRange=600, no 1200/0. Guardar esta diferencia antes de implementar. Diseño candidato: guardia selectiva con percepción1200, retención1400 y ventana30 updates, reutilizando movimiento/retorno nativos y cambiando sólo mPlayerRange durante execute de la instancia autorizada, restaurado en POST. Sin nuevas acciones/teleport/timers nativos; dos umbrales provienen de constantes nativas, no offsets inventados. Pendiente demostrar core, adapter, MSVC/PE/package y descarga independiente. No se hereda PASS humano CP04 a IA CP05.

CP04.4 .dusk15287 SHA a1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9 permanece inmutable; CP03 y refs anteriores intactos. CP06 fuera del alcance. Cloud offline; GitHub y Windows Actions disponibles.
