# CP04.4 — Evidencia mínima y prueba futura condicionada

**No hay TEST CP04.4 admitido. No instalar ni activar un archivo de esta revisión.** No se ha ejecutado el juego. El protocolo visual siguiente no desbloquea por sí mismo los contratos técnicos.

## Obtener el dato faltante sin iniciar el juego

Usar el mismo método de extracción **de sólo lectura** empleado en CP01 para los archivos Object, sobre una copia de la imagen de la instalación correspondiente, nunca sobre un recurso que se vaya a sobrescribir. Localizar `res/Object/E_OC2.arc` (variante exacta seleccionada por mName == E_OC2). El nombre físico/ruta debe confirmarse en el listado de esa imagen; no sustituirlo por E_oc.arc si no aparece. Exportar el ARC a un directorio separado; no reinsertar nada en ISO/instalación ni cambiar flags/saves.

En PowerShell, sobre el archivo exportado:

```powershell
$eliteResource = '.\E_OC2.arc'
(Get-Item -LiteralPath $eliteResource).Length
(Get-FileHash -LiteralPath $eliteResource -Algorithm SHA256).Hash
```

Enviar por la rama/repo **privado de inputs** y un manifiesto con nombre, tamaño, SHA256 y procedencia de versión (sin rutas personales). No enviar ROM completa, saves, credenciales, direcciones de memoria, ni archivo al repositorio Mods-Duskligh o artefactos públicos. Si no puedes exportarlo sin alterar la instalación, detener esta obtención y describir el impedimento. No necesitas arrancar el juego para esta extracción.

Alternativa técnicamente suficiente: evidencia derivada completa y verificable del modelo realmente index3 e index4 de E_OC2, incluyendo atributos de vértice, formatos/arrays/índices CLR0, mapa shape→material, canales GX material/ambient/vertex, stages/inputs/ops/outputs/konst de TEV, alpha/blend, texel formats/nombres/mapeos y separación cuerpo/ojos/accesorio. Una lista de bounding boxes, el modelo de E_OC normal o sólo un screenshot no acredita estos contratos.

## Futura prueba DX12 — sólo después de admitir build y paquete

1. Cerrar completamente Dusklight; respaldar saves por el usuario. Confirmar EXE oficial SHA256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049` y D3D12.
2. Instalar **sólo** el futuro .dusk CP04.4 verificado, con ID/versión propios. No combinar CP03/CP04.x que añadan otra instancia. Sin hot reload.
3. Entrar F_SP121/3/6. Capturar el E_OC2 adicional negro **y un E_OC2 original del mismo modelo/recurso**, preferiblemente ambos visibles en el mismo frame. E_OC normal de 40 HP no sirve como control. Si esa escena no ofrece dicho original, registrar ese control como pendiente; no inventarlo ni provocar aparición/modificar flags.
4. El negro debe mostrar volumen/detalle con iluminación, sin auras; ojos/arma respetan el límite material documentado. Un log APPLIED/readback privado nunca es VISUAL_PASS.
5. Si hay contaminación de original, fallo o crash: cerrar, no continuar combate, preservar log anonimizado privado y captura. Si estable: combate/daño/HP150 write PRE único, muerte, salir/reentrar una instancia nueva y reconstrucción visual una vez.
6. Reversión con juego cerrado: retirar **sólo** nuevo .dusk CP04.4, reabrir, comprobar ausencia del añadido y originales intactos. No restaurar por editar archivos/flags.

La aceptación final requiere log y evidencia visual humana. Todo el protocolo runtime permanece NOT_TESTED en este checkpoint.
