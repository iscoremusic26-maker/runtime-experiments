# G0 — selección condicional de E_OC

**Resultado: PARTIAL. Se recomienda únicamente E_OC normal (`E_oc`), sin autorizar aparición.** El expediente nativo está fundamentado; los recursos completos, la posición adicional y su contexto runtime siguen pendientes. DISARMED_NO_REGISTRATION; G5 y CP02 NO_GO.

Base DEVF `60ffb08ea1337592d3e05216f3f3d97f37426e18`. Fuente oficial Dusklight 2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Se reutilizan los seis informes de CP01_DAWNLIGHT_AUDIT y la evidencia CP00/CP01. No se compiló Dawnlight ni el host, ni se repitieron sus auditorías o suites.

| Candidato | Contrato acreditado | Decisión para este escenario |
|---|---|---|
| E_OC / `E_oc`, `fpcNm_E_OC_e` = `0x1FE`, argumento -1 | Tabla oficial `d_stage.cpp:975`; perfil CURRENT y callbacks Create/Execute/Delete nativos en `d_a_e_oc.cpp:2836–2863`. **Siete** registros ACT6 en F_SP121/R3: cinco variantes E_OC2 y dos E_OC normales, según angle.x. | Mejor evidencia de presencia natural. Selección condicional de modo normal; no se trasladan posiciones ocupadas. |
| E_SB / `E_SB`, `fpcNm_E_SB_e` = `0x1C1`, argumento -1 | Expediente previo: CURRENT; un archivo E_SB, modelo 0xF y animación inicial 0xC; cilindro 80/130, Acch 100/30, tamaño nativo 1.4. Switch bajo 0xFF omite ese filtro. Puede crear explosión de bomba y DISAPPEAR. | Menos archivos, pero no presencia natural acreditada en ACT6 de esta sala y riesgo de explosión. No seleccionado; no se declara incompatible en todas las escenas. |
| E_RD / `E_rd`, `fpcNm_E_RD_e` = `0x1D4`, argumento -1 | Reutiliza ENEMY_PARAMETERS/SCENE_OWNERSHIP previos: CURRENT; E_RD/E_rdb, modos y parámetros especiales, proyectiles/montura y migración condicionada. Un preset Dawnlight no acredita admisión local. | No presencia natural acreditada aquí; mayor dependencia de modo/descendientes. No seleccionado. |

La evidencia completa está en [selection-static.json](evidence/selection-static.json): registros, parámetros, transformaciones, hash del inventario conservado, hash de room.dzr y referencias de fuente. La lectura preliminar enumeró seis; la extracción completa incorporó ACT6 índice21. El baseline correcto es siete registros authored, **no siete actores vivos garantizados**. No se decodificaron de nuevo los ARC/KCL.

## Preset exclusivamente documental

Se toma la configuración original de ACT6 índice11 como referencia del tipo normal: `parameters=0xFFFFFFFF`, angle.x s16 **-236** (`0xFF14`), yaw **0**, angle.z **0**, setID `0xFFFF`, ACTR con escala implícita `(1,1,1)`, argumento -1. Es el menor rango nativo documentado de los dos E_OC normales de ACT6, sin inventar una configuración para reducirlo. No hay definición de spawn ni encoder nuevo en el observador.

`daE_OC_c::create` (`2704–2750`) interpreta byte bajo 0xFF como modo0; byte siguiente 0xFF selecciona búsqueda S (1200 por HIO), no M (5000). Switch de derrota y secundario son 0xFF: sus consultas/escrituras están condicionadas por ese sentinel. El byte alto de angle.x 0xFF elige **E_OC**, el bajo 0x14 configura **mMoveRange=2000**. El otro normal, índice10, usa 0xFF28/rango4000; no se cambia al azar el rango para declarar segura otra posición. Los modos2/3/4 y variantes E_OC2 quedan fuera del caso propuesto.

Recursos de Create: **E_OC** y **E_ocb**, dos solicitudes phase; heap `0x2E40`; modelo principal índice3 y arma índice4 de E_OC; animación inicial índice0x1B de E_ocb, más las animaciones referidas por Execute/setBck. La selección E_OC2 de los cinco originales debe distinguirse en el censo; no convierte E_OC2 en el candidato.

El tamaño nativo del modelo es **1.5** (`HIO`, `mtx_set:2542`), incluso con escala ACTR1. Cull ±200 no es AABB del modelo. Execute actualiza dos esferas de cuerpo (50/45) y dos de arma (45/30), ligadas a joints (`cc_set:2551–2584`); Acch usa radio100, altura70 fuera de D_MN05/R12. Faltan modelo y animaciones para obtener su envolvente real.

El rango de movimiento no es confinamiento duro: decisiones de regreso usan rango±200/300 (`2333–2430`), con ataque, persecución, huida, aliados y eventos. No se demuestra ausencia de interferencia por tener el centro fuera de un trigger. Modo2 tiene dependencia de Obj_RotBridge (`346–367`); modos3/4 inicializan las demos de la jaula del mono con control de cámara/Link (`2811–2826`). Ninguno corresponde al modo0 escogido. No se detectó setter explícito setStageLayer/setRoomLayer en este consumidor; **no equivale a probar ausencia de migración indirecta/runtime**. No se impone agua, lava, techo u horario para admitir este preset en Create. Execute sí comprueba agua (`2397–2440`: nivel >Y-140 sin GroundHit puede entrar WATER_DEATH), caídas y obstáculos; radio Acch pasa a60 en FIND/WALK y100 en otros estados. Se necesita suelo seco/contacto y espacio de movimiento, no solo una altura estática. Aliados/eventos y comportamiento real siguen pendientes.

Hay descendientes/efectos: las rutas de muerte llaman `fopAcM_createDisappear`; el helper oficial (`f_op_actor_mng.cpp:2019`) crea perfil DISAPPEAR y puede derivar efectos/recompensas nativos. No se exige combate o muerte en la primera observación. `_delete:2650–2662` libera las dos solicitudes de recursos y sonido, y retira su HIO cuando corresponde; la destrucción del heap/actor pertenece al motor. Esto acredita el contrato de fuente, **no PASS de limpieza dentro del juego**.

La especie es compatible estáticamente con la ruta A1 CURRENT→flujo normal de sala ya auditado, sin código DLL DEVF dentro del actor. No se registra su perfil, no se altera HIO, no se deshabilitan switches ni se utiliza A2. La descarga de perfiles personalizados continúa BLOCKED de forma independiente.
