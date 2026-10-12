# CP01 — host completo con parche experimental

**PATCHED_HOST_BUILD_PASS. INTEGRATION_TEST_PASS dirigido: 17/17. Seguridad de ciclo de vida: BLOCKED; CP02 NO-GO.** DEVF sigue DISARMED_NO_REGISTRATION. No se ejecutó, instaló ni distribuyó el host; no hay TEST activo.

Base preservada: 413377f / DEVF_CP01_OFFICIAL_BASELINE_MSVC. Experimento preservado: eea4742 / DEVF_CP01_HOST_LIFETIME_EXPERIMENT. Rama experiment/devf-cp01-host-integration, [PR draft #3](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/3), sin merge. Recuperación final: **DEVF_CP01_PATCHED_HOST_INTEGRATION_MSVC**. El tag intermedio DEVF_CP01_HOST_INTEGRATION_CONFIGURED conserva el estado previo.

## Compilación y procedencia

Source oficial 40457c6adb381928e4b5fef6ed459ed291edd5e2; los cuatro gitlinks, herramientas y dependencias del baseline se conservan exactamente. No se repitió la compilación intacta ni las investigaciones anteriores. host-lifetime.patch fue aplicado mediante prepare_experiment.py con hash 3a6268135dac0d37580342dacfb429bca84428b91b2ad0beec97e88a0a7501d8 y los 12  hashes antes/después. **Ningún cambio adicional al parche ni a los archivos del host** fue necesario para compilarlo. No se modificó código DEVF.

- [Run completo38265011287](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38265011287), [job/logs 114864857848](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38265011287/job/114864857848). Snapshot 55cbce11239adb3375e6a40002dd67a331b9ac99.
- Configure85,766 s; build/enlace/install **2.413,797 s (40m13,797 s)**, exit0; vcpkg 123,063 s. UTC y comandos efectivos están en evidence/full-host/*.json.
- MSVC **19.51.36260**, Windows SDK **10.0.26100.0**, CMake 4.4.3, Ninja 1.13.2, Python 3.12.10, Git 2.55.0.windows.5, sccache 0.12.0; vcpkg 9e593bb y tool2026-07-27-98d7cb0cf1f4686a3e43aa5672b6230c1d56bce8. Todos iguales al baseline.
- Preset original x-windows-ci-msvc: Ninja/amd64, RelWithDebInfo, CRT MultiThreadedDLL, debug Embedded, Sentry original, vcpkgx64-windows. Única opción observacional adicional: CMAKE_EXPORT_COMPILE_COMMANDS=ON.
- Grafo generado2.700 entradas; los 8 CPP modificados están presentes una vez cada uno. Ninja acredita19 consumidores de f_pc_stdcreate_req.h,54 de mod_loader.hpp,7 de actor.hpp y30 de registry.hpp. Es evidencia de dependencias de compilación y reconstrucción conjunta, no garantía de ABI de terceros que usen internals.
- Staging temporal build/install/Dusklight.exe: **52.321.280 bytes**, PE AMD64, EXE, nunca ejecutado. SHA256 **d4ec7dd9ef06435d70f45c4b6654602cc95b672f5c0b7d7ce04a4afbe795c061**. No se conserva/distribuye como entregable ni se afirma equivalencia binaria con el release original.
- Después del build, raíz/gitlinks y12  hashes siguen exactos; no hay cambios rastreados ajenos al parche. Dependencias observadas idénticas al baseline:23 descargas+20 fixtures y15 repositorios Git/recursivos; mismos ports. **31 warnings originales en ambos builds**, mismos códigos/mensajes/ocurrencias; cero errores del host y cero tipos nuevos. Ver BASELINE_COMPARISON.json.

```powershell
cmake --preset x-windows-ci-msvc -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build --preset x-windows-ci-msvc --parallel 2
```

**El job completo aparece fallido por el driver inicial posterior al build (C1083 de PCH), no por el host.** Configure/build/collect y PE pasaron. Se corrigió y ejecutó exclusivamente el diagnóstico en otro job; no se reconstruyó el host por esas correcciones. Los targets oficiales asociados se construyeron por el preset install; no se ejecutaron tests del randomizer ni mods/juego.

## Validación incremental Windows

[Run 38270210787](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38270210787), [job/logs 114882321243](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38270210787/job/114882321243), [PR privado draft#4](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/4); snapshot 11b763d49810654215aa9dfcd69aa627554e0237. Tag DEVF_CP01_REAL_QUEUE_INTEGRATION_MSVC. Las copias de herramientas/parche propios se contrastaron por SHA con el checkpoint principal. Ese pipeline no lee los ZIP/ARC privados y no compila otra vez el host.

Compilación/enlace y ejecución del driver: **17 expectativas PASS**,6,328 s. Usa headers/layouts del árbol completo, siete TUs de colas/métodos originales y cuerpos efectivos extraídos del escáner, cancel/delete y recorrido de destrucción. Owner, fase, capa, heap/proceso/destructor son adaptadores explícitos; no ejecuta la factoría ni Handler completo, mounts, DLL del juego o transiciones reales.

Layout MSVC observado: pointer8, create_request144, standard_request200, mod_owner offset176, tag-data offset24. Las expectativas incluyen cola antes de callbacks, dos dueños, petición opaca, cancelación pegajosa, backlink, retirada/reencolado y diagnóstico de reentrancia. El driver confirma que el recorrido revisita un tag retirado durante un callback. Los procesos se mantienen vivos: **no se provocó UAF/doble liberación ni se ejecutó ese escenario dentro del juego**. PASS de expectativas incluye demostrar este fallo de seguridad, no aprobarlo.

Correcciones exclusivas del driver, documentadas en intentos1–4: PCH ausente; referencias gráficas no usadas que persistieron incluso con /OPT:REF; orden de escalares antes de global.h bajo DUSK_BUILDING_GAME. El driver final conserva defines de ABI y headers reales, usa types.h→global.h→headers de colas, sin PCH gráfico, /Od,/Gy,/Zc:inline,/OPT:REF propios. No se sustituyen tipos ni se simula un renderer. D9025 de /Od es del driver. Se conservaron todos los intentos y no se repitió la suite25 ni las16 pruebas anteriores.

## Bloqueos y requisitos para una prueba activa

[INTEGRATION_REVIEW.md](INTEGRATION_REVIEW.md) detalla los contratos y caminos del source; [TEST_RESULTS.md](TEST_RESULTS.md) contiene la matriz.

1. **BLOCKED — reentrancia.** El siguiente nodo guardado por finish_delete_all_actors_of_name puede retirarse durante un destructor. Desregistro de otro perfil permite un camino estático de liberación; el snapshot de handles de actor_drain_mod también puede invalidarse. El diagnóstico Windows confirma la revisita de un tag retirado bajo callback controlado. Se conserva el parche y se bloquea su adopción, según la instrucción de no forzar GO ante riesgo grave.
2. **BLOCKED — teardown global.** main llama ui::shutdown después del loader aun cuando este retiene ownership. No se acredita la vida de todos los registros, recursos ni estáticos durante el cierre restante.
3. **NOT_VERIFIED / NOT_TESTED.** Servicios legacy sin modDrained, callbacks/threads de otros mods, fases/mounts/cancelaciones reales, escenas, componentes de actores originales, DLL/contexto dentro del juego y runtime/DX12. Las condiciones de ubicación anteriores permanecen pendientes, sin reanálisis.

Siguiente paso mínimo: en una etapa CP01 posterior, resolver barrera de mutaciones/reentrancia y recorrido con revalidación, y acreditar el teardown fuera del loader; ejecutar pruebas afectadas antes de plantear una prueba controlada. **CP01 no está listo para una prueba activa Windows/DX12. No hay GO CP02.**

## Evidencia y recuperación

Artefacto host11756393337:54.467 bytes, SHA256d8760d0800404c52501099775fec8e9c197fe088290429ebb20e027998e49d49. Diagnóstico11756771324:13.815 bytes, SHA256f789724fb808b29dbb2c7a6c11a54a4b9f12a97efd9f77fee9239bfb298183a0. Ambos descargados realmente y verificados SHA/CRC/allowlist exacta,11 y9 miembros textuales. Los logs/JSON están versionados, sin EXE, source extraído, credenciales o recursos originales.

Resumen persistente: evidence/VERIFIED_INTEGRATION_SUMMARY.json. Reproducción/recuperación/reversión: [REPRODUCE.md](REPRODUCE.md). Historial previo conservado. No hay instalación que revertir; no modificar instalación, saves ni recursos del usuario.
