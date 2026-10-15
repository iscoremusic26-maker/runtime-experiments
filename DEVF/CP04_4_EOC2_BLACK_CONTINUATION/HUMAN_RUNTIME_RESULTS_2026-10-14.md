# CP04.4 — Cierre humano observado, 2026-10-14 (America/Panama)

**CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED**, limitado al flujo descrito por el usuario. Este informe es posterior al TEST y no cambia su código, configuración, logs embebidos ni binarios.

## Procedencia y categorías

| Categoría | Resultado y alcance |
| --- | --- |
| REPO_VERIFIED | Lectura GitHub en este cierre: rama de implementación en `0a2ec044cbae476c6ca8f3e5387737791875f47c`; tags históricos y PR31/PR22 comprobados. |
| CI_BUILD_PASS / PACKAGE_VERIFIED / DOWNLOAD_VERIFIED | Históricos: runs [38657297492](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492) y [38658291368](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38658291368), ambos SUCCESS releídos por API. No build, laboratorio, descarga binaria ni empaquetado nuevos en este cierre. |
| CODE_ISOLATED_OFFLINE | Evidencia técnica histórica de [CHANNEL_AND_ROUTE](CHANNEL_AND_ROUTE.md) y [TEST_RESULTS](TEST_RESULTS.md); no se repite ni se convierte en certificación universal runtime. |
| USER_SUPPLIED_LOGS_ANALYZED_IN_CHATGPT | Resumen de tres logs analizados en ChatGPT, suministrado explícitamente por el usuario para esta tarea. Codex no recibió/leyó aquí sus bytes originales. Los números de línea y hashes siguientes son atribuidos, no hashes recalculados localmente. |
| HUMAN_REPORTED | Aparición negra, combate/muerte, día/noche, reentrada/reaparición, otros enemigos observados sin alteraciones y retirada en frío: declaraciones del usuario y resumen de capturas. Codex no inspeccionó esos píxeles en este cierre. |
| HUMAN_NOT_TESTED / PENDING | Comparación inequívoca simultánea con un E_OC2 retail del mismo modelo/textura en el mismo frame; rendimiento, compatibilidad de terceros y escenarios/hardware no observados. |

Entorno reportado: Dusklight 2.0.3 win32/x86_64, D3D12, Intel UHD Graphics; fuente oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`, EXE de referencia SHA256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`. No se afirma un hash nuevo de la instalación.

Stage F_SP121 / room 3 / layer 6, E_OC2 adicional, home (-1250,-6304.00830078125,60750). HP inicial 220→150 mediante una sola escritura PRE_FIRST_EXECUTE por generación elegible; sin cambio a field_0x560.

## Índice de los logs: cinco generaciones secuenciales

Todas las filas pertenecen a USER_SUPPLIED_LOGS_ANALYZED_IN_CHATGPT. Las secuencias son diferencias NETAS observadas, no conteo físico ni potencia de golpes ni identificación del arma.

| Log / actor / generación | HP_APPLIED 220→150 | Secuencia neta posterior (líneas) | BLACK_APPLIED | BLACK_RELEASED | Shutdown de sesión |
| --- | --- | --- | --- | --- | --- |
| A / 147 / 1 | L1798 | 150→110→70→30→0 (1860,1862,1863,1866) | L1851 | L1870 | L2153–2155 |
| B / 147 / 1 | L1793 | 150→110→70→10→0 (1857,1859,1860,1862) | L1846 | L1864 | L4293–4295 |
| B / 563 / 2 | L3961 | 150→130→120→80→40→0 (3999,4000,4002,4004,4005) | L3988 | L4007 | Misma sesión B |
| C / 147 / 1 | L1796 | 150→110→50→0 (1916,1919,1920) | L1850 | L1924 | L4281–4283 |
| C / 570 / 2 | L4228 | 150→110→50→0 (4259,4261,4270) | L4255 | L4272 | Misma sesión C |

**Totales: tres sesiones; cinco generaciones secuenciales (1+2+2); HP_APPLIED=5, CP04_BLACK_APPLIED=5, CP04_BLACK_RELEASED=5; las cinco llegan a HP cero.** No son cinco actores concurrentes. Las generaciones segundas siguen a salida/reentrada según la observación humana.

En A: L61–66 carga/activación v0.4.4 y 1/1 mods activos; L1799 PREFLIGHT, L1850 READY, L1851 APPLIED con rgb_word=08080AFF; L1870 RELEASED reason=NATIVE_DESTRUCTION_NO_PRIVATE_GRAPH. El resumen examinado en ChatGPT no registra ERROR/FATAL ni CP04_BLACK_REJECTED en A/B/C. Esto no equivale a ausencia universal de fallos, fugas o corrupción. Shutdown normal sólo acredita el cierre registrado: **no prueba desinstalación**.

## Identidad de la evidencia suministrada

Hashes y tamaños declarados para los archivos exactos aportados en ChatGPT; **no verificados de nuevo por Codex**. No se almacenan logs raw, capturas raw, texels ni rutas personales en Git.

| Archivo | Bytes suministrados | SHA256 suministrado |
| --- | ---: | --- |
| dusklight-20261014-192606.log (A) | 165829 | 110c4bdbc5c6dd04fe16bdf5f0adc4ae95c10365a04559d7101b2f265e3ad14c |
| dusklight-20261014-194506.log (B) | 332304 | 2d16a555920ddb29b8761e1efc051e3864ab207946479c2aa13ba3a60a857e8d |
| dusklight-20261014-194725.log (C) | 330821 | d7f91410a937fbae010f130cff21478f53b552dd75566d8dc9e2dce27c77953f |
| image(20261015-002719).png | No suministrado | ead7b89f63783cede313f4b2bd38b62af3225a5932c653902d16996bf1c61641 |
| image(20261015-004949).png | No suministrado | 005d268b8ec14e70ff254398b15ba20471cc7bbd9be6d7bf24c56bb25491bfa4 |
| image(20261015-005029).png | No suministrado | 2d213f4548a6526fd6ecfa7939ce1554c11fea65702ea5f91b63fe0416f89da7 |

La fecha del cierre usa America/Panama; los nombres de las capturas conservan literalmente su fecha original. Este índice no pretende ser evidencia raw ni un análisis independiente de los archivos.

## Observaciones humanas y dictamen limitado

Declaraciones expresas del usuario:

> "APARECIO. LO LOGRAMOS."

> "Todo funciono perfectamente. El enemigo reaparecio pero sigue negro incluso de dia. Ahi estan los dos logs de las dos pruebas".

> "Si, los demas enemigos mantienen el color original".

> "El enemigo desaparece al desinstalar. No hay problema con eso".

| Comprobación | Estado posterior a la build |
| --- | --- |
| Bokoblin adicional negro visible, día/noche | HUMAN_REPORTED / observado en las capturas según resumen suministrado |
| Silueta y arma reconocibles | HUMAN_REPORTED; Codex no inspeccionó los píxeles |
| Ojos | Excluidos por el mecanismo técnico; no se eleva la visibilidad de las capturas a una comprobación visual detallada independiente |
| Combate hasta cero y muerte | USER_SUPPLIED_LOGS_ANALYZED_IN_CHATGPT + HUMAN_REPORTED en estas sesiones |
| Reentrada y reaparición negra | HUMAN_REPORTED, compatible con las generaciones secuenciales B/C |
| Otros enemigos observados conservan colores | HUMAN_REPORTED; no comparación equivalente universal |
| Retirada con juego cerrado y ausencia del adicional | HUMAN_REPORTED por declaración expresa; no inferido del shutdown |
| Original E_OC2 idéntico, simultáneo en mismo frame | PENDING; la imagen de otro enemigo rojizo no satisface ese control |
| FPS/frametime, compatibilidad con terceros, otros hardware/escenarios | HUMAN_NOT_TESTED |

El tinte es muy oscuro y atenúa detalle superficial según el resumen humano: observación estética, **no corrección autorizada**. Se conserva exactamente la paleta y compilación probadas.

Hay advertencias de texturas y CalcDivideInfo en el entorno; el juego reporta 1.867 registros de reemplazos de textura. No se ocultan, no se adjudican automáticamente a DEVF y tampoco se usan como prueba de compatibilidad universal.

## Mecanismo conservado, sin nueva auditoría

Se reutiliza el diseño sellado: comandos XF MATCOLOR0 de nueve bytes propios, emitidos alrededor del packet de cuerpo shapes 0/2 de la instancia admitida, con restauración exacta en el stream; ojos shape 1 y arma/modelo accesorio excluidos. No se modifica TextureService, texturas, J3DModelData/MaterialData, baseDL ni recursos compartidos. ActorId/generación/escena/modelo/packet delimitan la selección. La evidencia de propiedad/FIFO y los tests offline permanecen en CHANNEL_AND_ROUTE y los registros históricos; este cierre no extiende su alcance a UNIVERSAL_ISOLATION.

Los eventos READY/APPLIED y PRE/POST son evidencia lógica de comandos, no imágenes GPU. El literal embebido `visual=HUMAN_RUNTIME_NOT_TESTED` se conserva sin reescribir código ni logs: era correcto al producir el TEST. La evidencia posterior actualiza este dictamen documental.

## Artefacto funcional inmutable y procedencia

Fuente compilada: `ee42f62d2bd2bbbfae9e61affb10c066fd0588af`.
CI compilación: `565b16f44a9eb338e4d2018c27f2c1bad8caf4f9`.
Checkpoint documental previo: `0a2ec044cbae476c6ca8f3e5387737791875f47c`.
ID/versión: `dev.devf.cp04_eoc2_black` / `0.4.4`.

| Elemento preservado | Bytes | SHA256 histórico |
| --- | ---: | --- |
| DEVF_CP04_4_EOC2_BLACK_windows-amd64_ee42f62d2bd2bbbfae9e61affb10c066fd0588af.dusk | 15287 | a1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9 |
| ZIP TEST | 45231 | e7b05803b687324c6f5eace8d3e2954b7e5b26d819f05e7de7d03bf5c2a8ca49 |
| DLL interna | 28672 | b61e47ed9cc1ee461469fab1f8fa7df38cca9045e17f14e12341657d9cb07f06 |

[Artifact histórico 11936739368](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492/artifacts/11936739368): API releída, expired=false, tamaño/digest ZIP coinciden con el registro. Caduca **2026-11-13 18:59:41 Panamá**, UTC 2026-11-13T23:59:41Z; no promesa de disponibilidad posterior. No se vuelve a descargar ni se reconstruye. Ver [BUILD_AND_PACKAGE](BUILD_AND_PACKAGE.md) para la auditoría histórica de las capas internas.

## Recuperación y límite del sello actual

Nueva rama exclusivamente documental: `feature/devf-cp04-4-eoc2-black-human-runtime-closure`, hija exacta de 0a2ec044. El SHA literal del commit publicado se entrega en PR/chat y se verifica por lectura GitHub. El diff sólo permite Markdown dentro de esta carpeta; el código funcional, workflows y paquete permanecen intactos.

Refs históricos releídos y preservados:

- `DEVF_CP04_4_EOC2_BLACK_PRIVATE_TEST_READY`: objeto anotado `21f9abb6b8dec176cc8b56d2652fb56a797ba45b` → commit `0a2ec044cbae476c6ca8f3e5387737791875f47c`.
- `DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14`: objeto anotado `08ffbae5e5da73658df77b3763de2fe6851f7a45` → `139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f`.
- CP04.4 BLOCKED `0b2216eec658402aec2470e0df0080e399294225` permanece en la ascendencia. CP01–CP03 y CP04 anteriores no reciben modificaciones.

**Sello por tag nuevo: BLOCKED en esta sesión**, no PASS DOCUMENTAL completo. Cloud informa environment_startup_failed/offline, sin shell disponible. La integración GitHub permite publicar árbol/commit/rama/PR, pero no expone creación de objetos tag anotados ni refs de tags. Los dos workflows de recuperación existentes fijan nombres y ramas históricos y no son compatibles con este nuevo cierre; reutilizarlos no crearía el tag solicitado. No se modifican workflows ni se intenta mover tags.

Nombre reservado, **no publicado por Codex**: `DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14`. Para completar únicamente el sello desde un clon autorizado nuevo cuando haya shell, sin compilar ni tocar binarios:

```powershell
git fetch origin feature/devf-cp04-4-eoc2-black-human-runtime-closure --tags
git rev-parse origin/feature/devf-cp04-4-eoc2-black-human-runtime-closure
# Contrastar el SHA con el commit documental publicado en PR/chat.
git show-ref --verify refs/tags/DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14
# Si ya existe, DETENER y verificar su destino; no sobrescribir.
# Sólo si no existe:
git tag -a DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14 origin/feature/devf-cp04-4-eoc2-black-human-runtime-closure -m "CP04.4 human runtime observed; three reported logs, five sequential generations; documentation only; identical EOC2 simultaneous control pending"
git push origin refs/tags/DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14
```

Después leer por GitHub API la ref y su objeto anotado, comprobar destino igual al SHA documental y volver a contrastar los dos tags históricos. No usar force/amend/reset/merge. Para recuperar el funcional se conserva el tag PRIVATE_TEST_READY y el artifact original; para retirar el mod, cierre completo, quitar sólo su .dusk y arranque frío, reversión ya reportada por el usuario.

No se solicita repetir el gameplay. No GENERAL_STABLE, FULL_RELEASE, PERFORMANCE_PASS ni UNIVERSAL_ISOLATION. **CP05 (comportamiento/IA nativa) y CP06 NO INICIADOS**; ninguna implementación nueva queda autorizada por este cierre.
