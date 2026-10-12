# Recuperación y límites de continuación

Rama independiente: `architecture/devf-official-sdk-only`, desde `765e16dcd86c1eeda45bad80a2c1380129565429` / `DEVF_CP01_PATCHED_HOST_INTEGRATION_MSVC`.

Tag nuevo: **`DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE`**. PR draft [#4](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/4), base `experiment/devf-cp01-host-integration` en 765e16d, sin merge. La base se eligió para preservar historia y que los workflows de baseline/host experimental no se disparasen por diferencias heredadas.

Recuperar en un directorio nuevo; no resetear una copia con cambios propios:

```bash
git clone --no-checkout https://github.com/iscoremusic26-maker/Mods-Duskligh.git work/devf-official-recovered
git -C work/devf-official-recovered fetch origin refs/tags/DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE:refs/tags/DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE
git -C work/devf-official-recovered switch --detach DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE
git -C work/devf-official-recovered rev-parse HEAD
git -C work/devf-official-recovered status --short
```

Leer primero README, ARCHITECTURE_DECISION, FEASIBILITY_MATRIX, ROUTES_AND_CONTRACTS, OFFICIAL_HOST_RISKS y TEST_RESULTS de **esta carpeta**. Los informes anteriores describen checkpoints históricos y la investigación del parche; la decisión actual excluye el host modificado como dependencia del producto.

Compilación incremental recibida: snapshot **20efbbf563ad1ec7edb7e22a27128ba07b77c7c7**, run **38277234930**, **26 PASS**. Los archivos C++/CMake/workflow no cambian tras ese snapshot; logs preservados en Git. `evidence/checkpoint-integrity.json` documenta los árboles anteriores intactos y los hashes de entrada del laboratorio. El checkpoint final añade informes y verificación explícita de EOL/procedencia, sin exigir otra build.

Si hace falta reproducir una comprobación afectada futura, checkout oficial limpio 40457c6, `git submodule update --init --depth 1 extern/aurora` para los headers exactos y Developer PowerShell x64 con MSVC/Windows SDK. Ejecutar `ci/run_windows.py` con build/evidence fuera del árbol oficial, o los comandos explícitos de TEST_RESULTS. No compilar host, otros mods o targets package/install. El workflow solo publica textos propios y no necesita los ZIP privados.

Los artefactos de CI se validaron contra digest/CRC y se guardaron como logs/JSON. Para revalidar sus ZIP descargados, usar `ci/collect_evidence.py --source <official> --pass-zip <ZIP11759173058> --failure-zip <ZIP11758848796> --output <directorio-propio>`; identifica explícitamente la diferencia LF/CRLF de las 37 fuentes. No copiar ZIP ni fuentes/recursos originales al repositorio DEVF.

**DETENERSE al concluir esta evaluación.** Mantener DISARMED_NO_REGISTRATION, CP02 NO-GO, bloqueo independiente de perfiles/DLL y ausencia de instalación/ejecución. No habilitar el closure del prototipo por configuración: no existe tal opción. Cualquier prueba real necesita nueva autorización, enemigo/ubicación/recursos verificados y un paquete de prueba separado revisado. No continuar el parche experimental ni convertir este laboratorio en un TEST activo.
