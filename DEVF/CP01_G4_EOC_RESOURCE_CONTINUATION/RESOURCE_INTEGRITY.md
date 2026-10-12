# G4 — dos recursos recuperados y verificados

**PASS_STATIC para identidad, lectura y estructuras/índices necesarios de los bytes aportados.** El bloqueo anterior de disponibilidad queda resuelto. No es una prueba del loader, renderer, memoria o recursos efectivos de una sesión futura.

Base documental intacta: `3e0792e90b6ebc764b421e56ab63a36df3157893` / `DEVF_CP01_G4_EOC_SAFETY_REVIEW`. Continuación exclusiva G4; sin modificar los seis informes históricos.

## Procedencia y comprobación independiente

Repositorio de entradas privado `iscoremusic26-maker/codex-cp00-inputs`; rama `inputs/devf-cp01-g4-eoc-resources`; commit exacto **`91884d5932377e15a96a9f1c8df48348751f37a5`**. Se leyó únicamente el directorio `DEVF/CP01_G4_EOC_RESOURCE_INPUTS/`, con tres archivos. El fetch coincide con el HEAD indicado. Ambos ARC son bytes reales almacenados como blobs Git, no punteros LFS; no fue necesario LFS pull ni descargar ZIP históricos.

| Archivo | Bytes comprobados | SHA256 recalculado |
|---|---:|---|
| E_oc.arc | 30837 | `ed7031096583a3a5a62e8ebbadb7c74dff29a8f77bf738222389ab99a39131f4` |
| E_ocb.arc | 137250 | `156bbd9d030a28885b6989ea53a4cffa965c152c29c24e37505844a0d76b8a09` |
| DEVF_G4_MANIFEST.json | 839 | `87211983294b1829f55d0be18765b1e49d3fccb8c0653a5ce3e2ad2db958a96f` |

Se cotejaron además los nombres, tamaños y hashes declarados dentro del manifiesto. Resultado PASS, sin modificar los originales ni sus copias de análisis. Identificación **GZ2E01, Twilight Princess USA** y exportación individual Dolphin Filesystem de solo lectura son procedencia **reportada por el usuario**; no se presenció la exportación ni se recibió la imagen completa. Esta región coincide con el dato conservado de G2.

El manifiesto declara `effective_game_override_status=NOT_VERIFIED`. Los hashes acreditan exactamente los recursos recibidos del disco; **no prueban que Randomizer/overlays/reemplazos de la sesión G2 usaran estos mismos bytes**. No se falsea esa procedencia ni se piden de nuevo los ARC.

## Compresión, contenedor e índices

| Recurso | Lectura real | Resultado |
|---|---|---|
| E_oc | Yaz0→RARC,43488 bytes descomprimidos,2 archivos | Índice/id3 `bmdr/oc.bmd`,39520 bytes; índice/id4 `bmdr/oc_wepon.bmd`,3648 bytes |
| E_ocb | Yaz0→RARC,177792 bytes descomprimidos,28 archivos | Índices/id3…30, todos BCK;0x1B corresponde a `bck/oc_wait.bck` |
| Ambos BMD | J3D2bmd3, longitud y secciones coherentes | INF1,VTX1,EVP1,DRW1,JNT1,SHP1,MAT3,TEX1 |
| Las28 BCK | J3D1bck1, ANK1,29 joints cada una | Tablas/offsets/canales/tangentes/tiempos y valores finitos comprobados; rango de índices acorde al header GZ2E01 |

Los decodificadores previos Yaz0/RARC/VTX1 se reutilizaron. La herramienta nueva valida únicamente la jerarquía, skinning, referencias primitivas/matrices y curvas requeridas para esta envolvente. No se invocó un loader nativo ni se construyó un ejecutable.

Yaz0/RARC **no proporcionan aquí un CRC de integridad embebido comparable**: CRC contra manifiesto es NOT_APPLICABLE, no un PASS inventado. Se registra CRC32 calculado sobre cada ARC solo como dato adicional; la comprobación de identidad es SHA256+tamaño, y la de estructura exige descompresión, longitudes y referencias válidas. No hay ZIP nuevo al que aplicar test de CRC de miembros.

## Modelos y dependencias realmente presentes

Modelo principal:566 posiciones F32,29 joints,3 shapes,11 grupos de matrices,3 materiales,3 texturas CMPR128×128 de un mip embebidas. Arma:17 posiciones F32,1 joint raíz identidad,1 shape/grupo/material y1 textura CMPR32×64 de un mip embebida. Todos los payloads de textura necesarios por estos headers quedan dentro de TEX1; no se localizaron referencias de textura externas en estos modelos.

DRW1 del cuerpo guarda85 entradas; el loader usa55 (`mMtxNum - mWEvlpMtxNum`), con25 rígidas y30 envelopes. Se resolvieron las55 mediante SHP1, incluyendo palettes heredadas65535. Los1500 registros de vértice primitivo remiten a las566 posiciones; el arma44 registros a sus17 posiciones. Los30 envelopes usan29 matrices inversas de bind, con pesos no negativos y sumas[0.9999999776482582,1.0000000298023224]. Se conservan los pesos reales, sin normalizarlos para facilitar una cota.

La enumeración BCK esperada del informe anterior ahora está respaldada por28 archivos reales. Su inventario con índice, tamaño y hash individual figura en [resources-envelope.json](evidence/resources-envelope.json). No se copian modelos, texturas, curvas ni ARC a Git. El sound bank/efectos/servicios del juego conservan los contratos previos; disponer de estos dos ARC no prueba por sí solo todos los subsistemas de creación.

Fuentes exactas: raíz oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`, `d_a_e_oc.cpp:2670–2750`, loaders J3D y headers GZ2E01 ya acreditados. Comparación de nombres virtuales E_OC/E_oc resuelta por la semántica FST previamente documentada. No se solicita E_OC2 ni se modifica el preset normal.

**Conclusión:** recursos aportados verificados y aptos para este análisis offline; disponibilidad/resolución de índices ya no BLOCKED. Correspondencia con recursos efectivos de G2/futuro host y funcionamiento nativo completo: **NOT_VERIFIED / NOT_TESTED**.
