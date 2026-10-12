# Parámetros: ejemplos seleccionados, no catálogo de seguridad

Referencias D/S y commits exactos: [COMPARATIVE_AUDIT](COMPARATIVE_AUDIT.md). Se revisaron como ejemplos **E_SB**, **E_RD** y **Darknut B_TN**. No se auditó cada una de las 43 opciones ni se seleccionó automáticamente un enemigo o una ubicación para TEST.

## Patrones transferibles

| Patrón Dawnlight | Fuente y contrato / límite en el objetivo |
|---|---|
| Parámetros por tipo, no cero universal | D1 tablas27–119/D2:79–84. Tipo, arma, ruta, switches, variantes e incluso color se empaquetan de forma diferente. **PASS_STATIC** de su definición; no setters universales de salud/daño/IA. |
| Sentinel de switch en distintos bits | D1:76–118: Darknut low byte FF; E_RD high byte FF; Stalfos/Kargarok también angle.z (321–323). Estos dos últimos significados se consignan como evidencia Dawnlight, **NOT_VERIFIED** en el native 2.0.3 por esta revisión acotada. |
| Argumento no intercambiable con parámetros | D1:61–62/121–122/326 y D4:65: Helmasaurus usa argument1. S9 name table990–991 tiene `E_mm`/-1 y `E_mm2`/1. A2 por número conserva argument, por nombre lo sustituye con el canónico; A1 obtiene argumento del nombre, no de bytes ACTR. **PASS_STATIC** de esa distinción; variante runtime no validada. |
| Ángulos con significados especiales | D1:321–331; Cave normaliza X y Z preservando yaw (D4:265–269). No tratar todos los s16 como rotación visual libre ni aplicar esa normalización a cualquier enemigo. **PARTIAL**. |
| Suelo/probe y altura de vuelo | D1:302–320 usa 300 delante de Link, probe+500 y GroundCross; sube ciertos perfiles 200. Solo rechaza -1e9: no comprueba aquí finite/room/material/envolvente. Es heuristic de testing, **NOT_VERIFIED** para coordenadas específicas DEVF. D5 es más defensivo y específico de Cave. |
| Agua, lava, techo, noche, rutas | D1/D4 comentarios de catálogo; D1 fuerza estado/timer de E_TK/E_TK2 y owner de E_ZS, D4 fuerza daytime Stalhound. Sus hooks son **INCOMPATIBLE**. Alternativa: seleccionar entorno, horario y variante nativos cuyo contrato esté probado; no copiar esas adaptaciones ni declarar que un piso basta. |
| Hijos/owners/eventos | D2:55–58/94–100, D4:194–199 y ejemplos S16. ID o parent ID no garantiza admisión, resources ni cleanup de toda descendencia. Coordinadores que esperan un tipo concreto de hijo no se randomizan arbitrariamente. **PARTIAL**. |

El catálogo incluye una opción rotulada Goron/NPC_GRA y distintos presets del mismo perfil (D9:11–20/D1:27–71); las 43 etiquetas no acreditan 43 enemigos seguros ni una whitelist de perfiles ENEMY. E_SB **no aparece** en las tablas D1/D4: las pruebas reportadas del spawner no certifican ese prototipo DEVF.

## E_SB — conservar la referencia anterior

S15 daE_SB_c::Create1097–1155 y su perfil1171–1186, ya revisados en CP01, respaldan nombre `E_SB`, perfil `0x1C1`, argumento -1, layer CURRENT y archivo nativo `E_SB`. El parámetro `0x000000FF` alimenta el campo u8 de switch y evita sus consultas/escrituras guardadas cuando es FF. Recursos/heap/suelo/colisión todavía precisan Create completo. La escala del prototipo no demuestra tamaño independiente; usa HIO global en setBaseMtx (evidencia anterior).

**PASS_STATIC** del contrato de bytes/params nativos; ubicación, recursos de instalación, apariencia, ataque, colisión y ausencia de otros efectos **NOT_VERIFIED**. El suelo/WRock/F_SP121 analizado antes no demuestra aptitud de E_SB y no se reestudia aquí. E_SB permanece una referencia de formato, no candidato definitivo de prueba.

## E_RD — preset de club/arco contrastado

D1:100 y D4:59–60 usan `0xFF000100` (club) y `0xFF000200` (bow). S16:208–209 define los valores de arma1/2. Su Create7316–7495 muestra:

| Campo | Decodificación de esos dos presets / conclusión |
|---|---|
| low byte arg0 | 0: no selecciona los modos4/5/11/12 que cambian actor_set a boss o archivo `E_rdb`; arg0=10 tiene rechazo coach-game y no se propone. |
| bits8–11 weapon | 1 club, 2 bow; otros valores tienen rangos/rechazos propios. |
| bits12–15 arg2 | 0: no es uno de los estados especiales/one-hit-kill/commander de3–7. |
| bits16–23 scene_no | 0: evita específicamente scene_no=2/setStageLayer en Create. No supone inmunidad a toda migración posterior. |
| high byte switch | FF: no consulta switch de room en7358–7363. |
| Recursos | `E_RD` en7341/resLoad7344 para esos arg0. Modelos/armas/animaciones son requisitos del native Create, no solo que exista el perfil. |
| Descendientes | Bow puede crear E_ARROW por createChild6909; otras rutas crean E_RD4963/E_WB7140. Exigen revisar el modo que vaya a activarse. |

**PASS_STATIC** del significado acotado del preset en 2.0.3; recursos/contexto/admisión/timing/combat runtime **NOT_VERIFIED**. Es selección de equipamiento/estado nativo, no configuración universal de stats. Se conservan las limitaciones previas de health sobrescrito, escala visual y colliders por separado. No se propone activar todavía esos presets ni auditar toda su IA.

## Darknut — type1 y FF tienen efectos concretos

D1:73–76/D4:77 proponen `0x000001FF`. S18 daB_TN_c::create5030–5054 confirma low byte switchFF y type bits8–15=1. Type0 usa `B_tnp` y consulta stage middle-boss; type1 usa `B_tnp2` y consulta isSwitch. S18 dSv_info_c::isSwitch1621–1641 devuelve FALSE para255/-1, de modo que FF sí neutraliza esa consulta. Siempre carga `B_tn` y después el archivo secundario: **dos recursos/phase requests**, más heap/modelo/animación.

Create5139–5151 elige ACT_ROOMDEMO para type0 y ACT_WAITH para type1. El dispatcher4526–4531 usa executeEnding para type0 y executeZakoEnding para type1. ZakoEnding4359–4429 evita sus escrituras de mSwitchNo cuando FF, mientras executeEnding4179–4223 contiene lógica de boss/evento. Esto respalda una variante nativa separable de la intro; **no prueba que sea independiente de todos los eventos/escenas**.

Create5154–5157 distingue `D_MN09` room2 con mStayNo2Flag; mType2 y frame de BRK también se decodifican en5057–5065. Campos altos distintos, scene específica y rutas de muerte pueden cambiar comportamiento. El nombre canónico A1 es `B_tn` (S9:1064), perfil `0x213`, argumento -1, CURRENT (S18:5177–5192). No convertir ese perfil de grupo ENEMY en un simple actor libre en cualquier room.

**PARTIAL** para variante sin opening demo y sin ese defeated switch; recursos, geometría, interacción/eventos/loot y limpieza de un ensayo concreto **NOT_VERIFIED**. La arena propia de Dawnlight usa hooks de admisión/estado y no es evidencia de que type1/FF elimine por sí solo restricciones FILI o de escenario en DEVF.

## Admisión y restricciones que no resuelve el catálogo

S17 fopAc_Create517–536 consulta FILI/EnemyAppear1Flag/BitSw de room antes de terminar la creación específica; si el grupo es ENEMY y el switch no satisface el sentido configurado, retorna ERROR. FF del enemigo no sustituye el bit FILI. Una clase puede cargar recursos, fallar por owner/entorno o iniciar un evento aunque su switch propio esté deshabilitado.

D6:719–751 devuelve cleared dungeon/switch state para la arena, exceptuando procesos tracked por D1. Ese bypass modifica el comportamiento de funciones por HookService y es **INCOMPATIBLE** incluso sin escribir saves. Su tracking temprano atiende el problema real de rechazar un proceso antes de inicializar componentes; copiar solo el preset, sin ese contexto, no hereda esa protección.

La alternativa compatible **A / PASS_STATIC como política**, con admisión concreta **NOT_VERIFIED**, es respetar los gates: room/estado/hora/evento compatibles, parámetros sin switches propios cuando el native admite ese sentinel y recursos disponibles. Si para una colocación concreta hace falta falsificar consultas o forzar globals/estados cada Execute mediante hook, esa combinación queda **BLOCKED**; escoger otro contexto/tipo demostrado, sin modificar flags, ROM o recursos originales.

## Contradicción puntual del checkpoint base: layer lógico15

El prototipo anterior acepta0–15 como validación de encoding. S9 dStage_setLayerTagName2298–2300 exige `0 <= layer < 15`; layerTableLoader2694–2698 dispone de índices0–14. Por tanto **15 no es una capa de escenario acreditada para una aparición**, aunque quepa en int8 y el validador de datos desarmado la acepte. Es una corrección documental concreta, no una razón para repetir 26 tests ni modificar el prototipo en esta tarea. Los gates futuros exigirán0–14 o una regla más restrictiva de la escena; -1 del servicio es wildcard, no una capa nueva. La capa efectiva6 previamente observada no cambia.
