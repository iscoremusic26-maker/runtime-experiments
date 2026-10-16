# Recuperación
Baseline source CP08 9b44c40e12f108d1b585f15e1c17bc2c621ccffe; CI92e877a44b392e75bc9dc819f4932c43deb5e0a0.
CP09 se construye únicamente desde app/DEVF.MapEditor.csproj en rama nueva; no se compilan los .dusk.

Rollback usuario: cerrar CP09 y abrir DEVF Map Editor0.8.0 histórico. Conservar proveedor0.8.0 y Expansion0.2.0. Configuración schema1 y backups históricos no se convierten. Para reconstruir catálogo, con CP09 cerrado retirar solo archivos catalog-v1-*.json bajo LocalAppData/DEVF/MapEditor/CP09; la imagen original no se modifica. last-image.txt es referencia privada local y puede eliminarse.

Build reproducible: Windows .NET8 SDK, dotnet publish app/DEVF.MapEditor.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true. La CI aislada registra SHA fuente e inputs en SOURCE_CI.json, verifica ledger y ejecuta --self-test contra el R03 privado existente. Nunca agregue ese ARC a Git ni al ZIP.

No merges, force, amend, retag ni cambios a PR48/34. Una falla requiere corregir solo CP09 y repetir su CI, manteniendo evidencias anteriores.

## Checkpoint entregado
Fuente compilada b9ea7518684126b733532cb0a99a0e3b98d4d74e; CI 04e87f713f1d96301d7ede29cda9628ba8fa84f9; [PR fuente49](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/49), [PR CI35](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/35), ambas draft/sin merge. [Run final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38918182460) y [descarga](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38918182460/artifacts/12053167316). No reconstruir CP08 ni instalar mods nuevos para esta prueba.

## Hotfix CISO +576 B entregado
Fuente compilada 3b45f2f50c65f98f0f9b880bc8d1ec7cc9829416; CI c6e20919e0f0d9ae3139879974c4e50220b1e429. [Run final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38954973078) y [ZIP privado nuevo](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38954973078/artifacts/12069682536). La corrección funcional cambia solo Disc.cs; ImporterTests.cs añade regresiones. Mismo workflow y pipeline, una actualización del ledger/checkout de fuentes. No modificar ni convertir el CISO; no desactivar validaciones de FST si surge un segundo error.

Para QA: conserve .dusk CP08, encounters.json y editor anterior; abra el EXE del ZIP nuevo y seleccione el mismo CISO. Compruebe GZ2E01 rev0, cifras reales y salas según HUMAN_TEST.md. Si falla, guarde solo el texto exacto del nuevo error. Rollback del editor: cierre el hotfix y use la entrega CP09 anterior o CP08 para importar ARC manualmente. La entrega anterior rechaza esta cola conocida y no sirve como control positivo del CISO. Ningún cambio de mods ni prueba de juego es necesario para este diagnóstico.
