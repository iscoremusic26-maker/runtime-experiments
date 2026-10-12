# G4 — recursos E_OC/E_ocb

**BLOCKED para verificación de los recursos binarios y su envolvente. PARTIAL para el expediente; PASS_STATIC para referencias e índices esperados del código oficial.** Registro observado no equivale a archivo íntegro o modelo/animación inspeccionados.

## Inventario incremental

Se reutiliza la integridad CP00/CP01, sin repetir hashes/CRC de ZIP o ARC antiguos. Se consultaron nombres de directorio ZIP y, para los `.dusk` oficiales incluidos, sus directorios internos. Resultados reproducibles en [g4-aggregates.json](evidence/g4-aggregates.json).

| Fuente disponible | Inventario | E_OC/E_ocb binarios |
|---|---|---|
| `dusklight-2.0.3.zip` | 19861 entradas; fuente y encabezados de recursos | No localizados |
| `Dusklight-v2.0.3-win32-x86_64.zip` | 63 entradas | No localizados |
| `.dusk` contenidos en ese ZIP | cosmetics6, luau_runtime7, randomizer17 entradas | Ninguno contiene los ARC buscados |
| `DEVF_CP01_EVIDENCIA_F_SP121.zip` | 4 entradas: STG_00, R03_00, WRock y manifiesto | No contiene esos ARC; inventarios RARC previos sin modelos/animaciones E_OC |
| `DEVF_CP01_EXTRA_COLLISIONS.zip` | 3 entradas: @bg004d, Obj_Board y manifiesto | No contiene esos ARC; estructura previa reutilizada |
| Entradas privadas remotas | main `9f95a34d93810b55250e8b833a2e343757cf8a01`, actualizado mediante fetch | No nueva entrega de E_OC/E_ocb |
| Corpus Cloud de trabajo/entradas | Búsqueda dirigida de nombres ARC e imágenes ISO/CISO/RVZ/GCM | Sin las dos cargas binarias ni una imagen de juego disponible en este corpus |

La ausencia se limita a estos insumos; no describe los archivos de la computadora del usuario. No se revalidó el EXE, SDK, ABI, import library ni un build anterior. No se extrajo indiscriminadamente ningún contenedor. Las herramientas RARC/J3D existentes en [CP01/analysis](../CP01/analysis/README.md) permanecen disponibles; escribir otro decodificador sin los archivos no cerraría el bloqueo.

## Fuente de los recursos y nombres

Fuente limpia: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`. `include/d/d_resorce.h:94–96` usa `/res/Object/`; `src/d/d_resorce.cpp:53–61` concatena nombre y `.arc` y solicita montar el archivo. El actor solicita `E_OC` y `E_ocb`; estas son **rutas virtuales**, no rutas que necesariamente existan sueltas bajo Windows.

Aurora exacto `3227d76c60e1e782ca576610bce61c9e7744d8be`, `lib/dolphin/dvd/dvd.cpp:167–179,992,1102`: resuelve archivos mediante el FST del disco montado, con comparación de nombres insensible a mayúsculas. El host también admite overlays. El contenedor acreditado que falta en Cloud es la fuente de juego configurada en la instalación —imagen de disco y, si corresponde, un overlay que la sustituya—. El log informa **GZ2E01**, consistente con los encabezados regionales consultados; eso no demuestra los bytes de un ARC.

Conservar nombre/capitalización real: el archivo del disco puede aparecer como `E_oc.arc` para la solicitud `E_OC`. No renombrar ni crear un archivo para ajustarlo al nombre del código. No se necesita descargar una ROM ni recibir su contenedor completo.

## Referencias esperadas; no confundir encabezados con geometría

| Recurso | Fuente oficial / contrato | Comprobación |
|---|---|---|
| E_OC modelo principal | `CreateHeap`, d_a_e_oc.cpp:2670; índice3, tipo BMDR en `assets/GZ2E01/res/Object/E_oc.h` | PASS_STATIC referencia; archivo/índice real NOT_VERIFIED |
| E_OC arma | Índice4, OC_WEPON, mismo header y CreateHeap | PASS_STATIC referencia; dimensiones/materiales reales NOT_VERIFIED |
| Joints | Header enumera29, backbone1=1, mano derecha=0xC, cabeza=0x11; callbacks de actor en12/17 | Nombres/índices esperados PASS_STATIC; JNT1, transformaciones y vértices reales NOT_VERIFIED |
| E_ocb inicial | Índice0x1B WAIT en CreateHeap | PASS_STATIC referencia; BCK y curvas reales NOT_VERIFIED |
| E_ocb adicional | Header lista28 BCK, índices3…0x1E | Inventario esperado PASS_STATIC; integridad/compatibilidad/poses NOT_VERIFIED |

Animaciones esperadas: angry_a/b, attack_b/c, cry, damage/l/r, dash, drowned, find, finish, gale, jump_a/b/c, leap_a/b/spin, **serch** (nombre oficial), stand/stand_wait, talk/talk_b, wait/wait_st, walk/walk_st. Son enumeraciones del fuente, no un inventario de archivos recibidos. Para una envolvente futura deben considerarse todas las poses alcanzables del modo0, callbacks de cabeza/mano, interpolación y transformaciones del arma; no basta medir el frame inicial de WAIT.

Hashes de los dos encabezados y de las funciones oficiales consultadas están en `source_sha256` del JSON. Los hashes de **E_OC.arc y E_ocb.arc son NOT_VERIFIED/ausentes**; no se sustituyen por hashes de headers. No se solicita E_OC2: los cinco originales de esa variante ya están explicados y no define el modelo de la nueva instancia normal.

## Colliders que sí permite identificar el fuente

Se conserva la auditoría de [ENEMY_SELECTION](../CP01_A1_PREFLIGHT/ENEMY_SELECTION.md). Consulta focalizada d_a_e_oc.cpp:2542–2584/2670–2770:

- Escala HIO por defecto1.5 aplicada a la matriz; ACTR implícita1 no anula esa escala. No se cambia ni se afirma que el HIO efectivo de la sesión se haya medido.
- Esferas corporales R50/R45: centros obtenidos de matrices animadas de backbone1/cabeza, offsets locales(10,10,0)/(10,0,0).
- Esferas del arma R45/R30: centros de mano derecha animada con offsets locales(0,0,70)/(0,0,20); el modelo de arma hereda esa matriz.
- Acch pared R60 en FIND/WALK, R100 en otros estados; altura70 en este contexto. No es una esfera que contenga el actor y su arma.
- Cull box±200 y heap0x2E40 son contratos distintos; ninguno ofrece una cota geométrica de las poses/ataques.

Sin BMD/BCK reales no se conocen posiciones/escala de joints, geometría del arma ni máximos animados. No existe una envolvente superior finita justificada por esos radios solos. Los dos E_OC normales observados en G2 y el testimonio visual respaldan funcionamiento de recursos en **esa sesión**, pero no dan identidad, estructura, dimensiones o integridad de los archivos que G4 necesita.

## Entrada mínima exacta para continuar

**Solo dos ARC completos**, correspondientes al disco **GZ2E01** usado en G2 y conservando los nombres que muestre su explorador:

1. `/res/Object/E_OC.arc` (posible nombre físico `E_oc.arc`).
2. `/res/Object/E_ocb.arc`.

Procedimiento de lectura, sin iniciar el juego: con el mismo explorador de imagen de disco ya utilizado para STG/R03/WRock, abrir **en modo lectura** la imagen configurada para esa sesión; exportar únicamente esas dos entradas a una carpeta de evidencia externa a la instalación. No guardar modificaciones de la imagen, editar ARC ni reemplazar originales. Si existe un overlay para cualquiera de esas rutas, identificarlo y copiar también el archivo efectivo correspondiente, indicando que es un override; no asumir que el disco base fue la fuente efectiva.

Anotar en un manifiesto: ID/región GZ2E01, nombres virtuales y reales, tamaño en bytes, herramienta/versión, extracción de solo lectura, y si hubo override de esas dos rutas. Omitir rutas personales, claves y la ruta de la imagen. Si no se puede identificar la fuente efectiva, indicar UNKNOWN; no afirmar equivalencia con G2.

PowerShell, sobre las **copias** y adaptando sus nombres reales:

```powershell
Get-Item 'C:\evidencia\E_oc.arc','C:\evidencia\E_ocb.arc' | Select-Object Name,Length
Get-FileHash -Algorithm SHA256 'C:\evidencia\E_oc.arc'
Get-FileHash -Algorithm SHA256 'C:\evidencia\E_ocb.arc'
```

Empaquetar solo esas copias y el manifiesto en un ZIP, calcular también SHA256 del ZIP y subirlo al repositorio **privado de entradas**; usar Git LFS si corresponde. No subir al repositorio de código ni a una release/artefacto público. Si el explorador existente no permite la exportación, aportar únicamente esa limitación y un listado sanitizado de las dos entradas; esta guía no autoriza instalar herramientas, arrancar el juego o descargar una ROM.

No reenviar EXE, SDK, ROM, STG/R03/WRock, colisiones adicionales ni el log G2. Con esos dos ARC, la siguiente revisión sería exclusivamente offline: SHA/CRC/estructura/índices, reutilizar decodificadores existentes para modelo y arma, después BCK/joints y cota de envolvente. Recibirlos **no garantiza** cerrar ubicación o autoriza G5.
