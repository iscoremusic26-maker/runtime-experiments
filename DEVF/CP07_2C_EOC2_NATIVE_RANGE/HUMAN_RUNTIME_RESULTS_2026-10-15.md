# CP07.2C — cierre humano observado, 15-10-2026
Fecha de referencia: 15 de octubre de 2026, America/Panama. Dictamen acotado: **CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12**.

## Procedencia y alcance
**USER_OBSERVED_RUNTIME_PASS:** el usuario declaró: **«Ya hice la prueba y ahora se comportan como los bokoblin normales».** La corrección del radio nativo resultó satisfactoria en el alcance de las dos sesiones A_ONLY y BOTH comunicadas. No se necesita más investigación ni modificación de IA para cerrar esta incidencia.

**USER_LOG_ANALYZED_IN_CHATGPT / EXTRACTOS_COMUNICADOS:** ChatGPT revisó localmente los dos logs originales antes de depositar el [encargo](CODEX_CIERRE_HUMANO_2026-10-15.md), blob `12f667e4be03ba957a308da1da4b42eda5efe872`, en commit `684d027c1c73be5d083dfa6754e10fe3fc2ae066`. Codex leyó ese documento mediante GitHub; **no recibió ni leyó los bytes originales de los logs, no recalculó sus hashes y no ejecutó el juego ni inspeccionó imágenes**. Los datos siguientes se transcriben del handoff autorizado, sin convertirlos en verificación local de Codex. No se publican logs crudos ni rutas o metadatos personales.

**REPO_VERIFIED:** PR47 estaba draft/open/sin merge, HEAD literal `684d027c1c73be5d083dfa6754e10fe3fc2ae066`, hijo de `e2e937b060700801f04143624abd3217a3664db4`; ese commit añadió sólo el encargo Markdown. El cierre se añade por fast-forward a esa misma rama, sin otro PR ni CI.

## Dos sesiones humanas
En ambas, según los extractos: Dusklight 2.0.3 revisión `40457c6adb381928e4b5fef6ed459ed291edd5e2`, Windows/D3D12; proveedor DEVF 0.7.4 (fuente `02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd`), Bokoblin Expansion 0.1.0 (fuente `5446365ed343905ff59bf7e6bc4929c5e395e6b1`), **Zora Swim 1.3.0** y **3/3 mods activos**. No fue un ensayo aislado de otros mods. Slots legacy FIELD/NORTH: `configured=0 edits=0`.

| Sesión | Archivo original no publicado | Bytes | Líneas | DEBUG / INFO / WARNING | ERROR / FATAL |
|---|---|---:|---:|---|---|
| A_ONLY | dusklight-20261015-172414.log | 312045 | 4041 | 3799 / 66 / 156 | 0 / 0 |
| BOTH | dusklight-20261015-172617.log | 310547 | 4024 | 3792 / 70 / 142 | 0 / 0 |

SHA256 aportados, no recalculados por Codex:

- A_ONLY: `9d74edb7c57b1c92f41d54fe3dd75ab942ac723547ed62983d19c31b51eb0bf7`.
- BOTH: `6cd5e68f758f596fecd2d3aecb678987ce42aa63c7c14ec57283b901a173eff4`.

| Sesión | Solicitudes aceptadas | Retiro de ediciones | Cierre |
|---|---|---|---|
| A_ONLY | encounter-1, token 1, result=0 | token 1, result=0 | limpieza consumidor/proveedor y all mods unloaded |
| BOTH | encounter-1 token 1 y encounter-2 token 2; result=0 en ambas | orden inverso 2 y 1, result=0 | limpieza consumidor/proveedor y all mods unloaded |

Los mensajes `actor_id=NOT_OBSERVED` y `evidence=STAGE_EDIT_ONLY` prueban registro de ediciones según el extracto, **no identidad de actor vivo ni estados internos de IA**. La normalidad del comportamiento procede exclusivamente de la observación humana. Retirar una edición no demuestra destrucción inmediata de un actor vivo ni hot unload.

## Advertencias y límites
- A_ONLY: 122 advertencias de aurora::texture y 34 de dusk/CalcDivideInfo; total 156.
- BOTH: 112 de aurora::texture y 30 de dusk/CalcDivideInfo; total 142.
No se atribuyen causalmente a este cambio con la evidencia disponible; tampoco se afirma que fueran preexistentes o globalmente irrelevantes. Los recuentos ERROR/FATAL=0 se atribuyen al análisis comunicado, no a lectura propia de Codex.

No se acreditan distancias medidas, video, radio visible de 5000, paridad completa de IA retail, todos los estados de executeWalk/home, cooperación universal, navegación general, rendimiento/FPS, compatibilidad universal ni release estable. Haber ejecutado junto con Zora Swim no certifica todas las interacciones entre mods. Este PASS no significa eliminación de toda conducta nativa de retorno/patrullaje.

## Identidad técnica preservada y cronología
- **SOURCE_VERIFIED:** sólo records nuevos encounter_placement@1.0 cambian angle.x de 0106 a 0132 (rango radial nativo 600→5000); legacy FIELD/NORTH mantiene 0106. No se alteran APIs ni consumidor.
- **BUILD_PASS histórico:** run [38812099184](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812099184), 354 PASS y18 negativos rechazados.
- **DOWNLOAD_VERIFIED histórico:** run [38812605127](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812605127). No se repiten build, laboratorio ni descarga para editar Markdown.
- **USER_OBSERVED_RUNTIME_PASS posterior:** declaración humana y dos sesiones anteriores, con los límites expresos de este acta.
- Proveedor 0.7.4: .dusk **129925 bytes**, SHA256 `934a0a1a5127fa994b9325a5f94a493d0df53f3b5f9af9acfce3709006379fbb`.
- Consumidor 0.1.0 inalterado: .dusk **24439 bytes**, SHA256 `104a6c0908f498b0a833b7ed31d12e75f224bc2f232633bd921446c217d2333f`.
- ZIP proveedor histórico: **280547 bytes**, SHA256 `89258783b1d776d762f6b62c71d8bb1cefdd9086f8c3771ddec09ab137278464`.
- Pre-QA documental: `e2e937b060700801f04143624abd3217a3664db4`; encargo posterior: `684d027c1c73be5d083dfa6754e10fe3fc2ae066`. La fuente compilada sigue siendo `02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd`, distinta del commit de cierre humano.

Los metadatos congelados y textos internos HUMAN_PENDING describen el momento del build; no se reescriben paquetes, manifiestos ni evidencias JSON para aparentar que el resultado humano existía entonces. [Build y hashes](BUILD_AND_PACKAGE.md), [recuperación](RECOVERY.md).

## Veredicto
**CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12**, limitado a las dos sesiones y al reporte humano: incidencia cerrada documentalmente. Continuar con la próxima funcionalidad cuando se autorice, sin reabrir esta corrección de IA ni exigir repetir las pruebas. No se implementa otra funcionalidad en este cierre.
