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

Ver [RECOVERY.md](RECOVERY.md) para refs y [TEST_RESULTS.md](TEST_RESULTS.md) para resultados. CI de procedencia ejecutado: [run 38649308109](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38649308109); resultado SUCCESS. El sellado posterior se verifica en su propia ejecución y ref remota.

## Resultado de procedencia ejecutado

[Actions Windows #38649308109](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38649308109), job 116143874314: **SUCCESS / PASS_STATIC** sobre `fac19a9ead3771185f6b977e4be238652b79e2c8`. Python 3.12.10, git version 2.55.0.windows.5, Windows-2025Server-10.0.26100-SP0; verificación 2.672 s (no tiempo de compilación). 32 fuentes con blob Git esperado/SHA256 y rangos válidos; 1249 rutas de la base intactas; 71 refs antiguas intactas; git fsck completo. Evidencia derivada: [evidence/static-audit-result.json](evidence/static-audit-result.json). No contiene recursos originales ni logs privados del juego.

El cierre documental conserva sin cambios verificador, inventario y snapshot validados. La segunda ejecución comprueba únicamente Git y publica el tag final; no vuelve a descargar fuentes ni repite tests/compilaciones de etapas anteriores. El runner Windows está disponible; el executor Cloud permanece failed. El bloqueo del recoloreado es técnico, no falta de compilador demostrada.
