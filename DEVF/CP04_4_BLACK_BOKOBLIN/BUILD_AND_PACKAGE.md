# CP04.4 — Reproducción y distribución

**No BUILD_PASS, PACKAGE_VERIFIED ni TEST_READY.** No existe .dusk CP04.4, DLL, ZIP de distribución, tamaño/SHA256/caducidad de paquete nuevo. No se compiló Dawnlight/Dusklight/SDK ni CP03. No se ofreció una simulación Linux como prueba Windows.

El executor Cloud seleccionado está failed al consultar capacidades. Se usó la integración GitHub con repositorio privado y permisos de escritura. El workflow propio `.github/workflows/devf-cp04-4-recovery-tag.yml` usa `windows-latest`, checkout fijado por SHA y el head exacto del PR privado. Tiene un solo fin: recuperar Git, verificar preservación/procedencia y publicar **un tag nuevo**, sin sobrescritura. No contiene pasos MSVC, build SDK, ejecución del juego, upload de assets, DLL o artefactos. La versión de Python/Git y el SHA de CI quedan en sus logs.

Comandos de reproducción en checkout limpio propio:

```powershell
git fetch origin feature/devf-cp04-4-black-bokoblin --tags
git switch --detach origin/feature/devf-cp04-4-black-bokoblin
python DEVF/CP04_4_BLACK_BOKOBLIN/tools/verify_checkpoint.py
git fsck --full
```

El script descarga **sólo fuentes públicas en commits exactos** a memoria para comparar Git blob/SHA256 y validar rangos de referencias. No descarga ZIP/LFS/ROM/logs. Imprime metadatos derivados, no fuente ni credenciales. Su resultado es procedencia estática, nunca MSVC/ABI/render PASS.

Una futura ruta admitida deberá reutilizar el pipeline MSVC de CP03 con copia nueva del mod (sin recompilar/sobrescribir CP03), HookService tipado y políticas originales, luego auditar PE AMD64/ABI/imports/exports, paquete .dusk oficial, negativos de empaquetado y descargar el archivo real para contrastar SHA256/tamaño/CRC/manifest/DLL interna. Esto es condición futura, no trabajo realizado.

Ver [RECOVERY.md](RECOVERY.md) para refs y [TEST_RESULTS.md](TEST_RESULTS.md) para resultados. El enlace CI final se registrará tras comprobar la ejecución.
