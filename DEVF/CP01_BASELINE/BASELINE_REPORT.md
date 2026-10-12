# CP01 — baseline oficial Windows x64 sin parche

**Conclusión: BASELINE_BUILD_PASS.** El host oficial Dusklight 2.0.3 terminó configuración, compilación/enlace y staging del preset original. No se aplicó host-lifetime.patch ni se modificó el código DEVF. El EXE no se ejecutó.

Base documental: eea4742 / DEVF_CP01_HOST_LIFETIME_EXPERIMENT. Rama independiente: checkpoint/devf-cp01-official-baseline. Snapshot de CI acreditado: 65c9b8b47f38ea966f5cb69fbc2e5b2623a785ba. Checkpoint final: **DEVF_CP01_OFFICIAL_BASELINE_MSVC**. Conserva todos los anteriores tags; sin merge.

## Evidencia Windows recibida y verificada

- [Run 38256856294](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38256856294), [job y logs 114837029572](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38256856294/job/114837029572), [PR draft #2](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/2).
- Artefacto textual 11752491649, 48.986 bytes; SHA256 `2d30d53780e8c6b57d3e1dbee3cef85b66fa7486854924e2c80891235c2747cd`. Descargado realmente y comprobado SHA, CRC y allowlist de los ocho JSON/logs. No contiene binarios, recursos ni source.
- Datos completos persistentes: [VERIFIED_BUILD_SUMMARY.json](evidence/VERIFIED_BUILD_SUMMARY.json), [baseline-result.json](evidence/final/baseline-result.json), [source-preflight.json](evidence/final/source-preflight.json), [configure.log](evidence/final/configure.log), [build.log](evidence/final/build.log). No dependen del vencimiento del artefacto de Actions.
- Root y cuatro submódulos limpios antes/después. Los 12 hashes originales del manifiesto anterior permanecen intactos. Verificación adicional del código de CI: workflow, SOURCE_LOCK y los dos scripts son idénticos al snapshot ejecutado; los commits posteriores solo añaden informes/evidencia.

| Fase | Resultado | Tiempo medido |
|---|---|---:|
| vcpkg: dos roots oficiales y transitivas | PASS | 104,734 s |
| Preflight raíz/gitlinks/hashes/toolchain | PASS | Registrado en logs |
| Configure original x-windows-ci-msvc | PASS | 83,781 s |
| Build/enlace + install original | PASS, exit 0 | 2.000,406 s (33 min 20,406 s) |
| PE AMD64 + source limpio posterior | PASS estático | Registrado en metadata |
| Ejecución del juego, render, DX12 | NOT_TESTED | No ejecutados |
| Parche experimental, seguridad del unload | NOT_TESTED por este baseline | Etapa posterior |
| DEVF activo / CP02 | NO-GO | DISARMED_NO_REGISTRATION |

El build generó sus targets oficiales asociados y 2.637 acciones Ninja, incluidos mods de ejemplo y tests del randomizer por los defaults del proyecto. No se ejecutaron esos tests ni el juego, ni se activó ningún .dusk. No se construyó DEVF ni TEST activo. Install preparó exclusivamente official/build/install dentro del runner.

El host staged se identificó como build/install/Dusklight.exe, **52.310.528 bytes**, PE AMD64 (0x8664), EXE y no DLL. SHA256 observado: `f1ab70a932a98cb551d3b40400883561f84a8f50b2dfdae00a256c4998aea628`. Solo se conserva su identidad; no se distribuye el ejecutable. No se afirma reproducibilidad bit a bit entre compilaciones ni correspondencia binaria con el ZIP Windows original.

## Procedencia del source y dependencias

Oficial TwilitRealm/dusklight, tag v2.0.3, raíz **40457c6adb381928e4b5fef6ed459ed291edd5e2**. Checkout independiente y sin modificaciones propias.

| Submódulo | Gitlink y HEAD exactos |
|---|---|
| extern/aurora | 3227d76c60e1e782ca576610bce61c9e7744d8be |
| extern/borealis | 4ac5e7052a8c49a122f8d57f626b5c75c5ca6968 |
| mods/randomizer | 1f24e81303536db4b77f49d057a8ec1f11162000 |
| mods/cosmetics | fd93491089fa95441789244f2b2fd22a451ecbcc |

Se verificaron por Git los commits facilitados; no se repitió su identificación. Relación nueva del árbol oficial con el ZIP fuente ya verificado: **19.366 blobs idénticos**, sin extras, y un único gradlew.bat equivalente tras normalizar LF/CRLF, declarado por .gitattributes. No se repitieron CRC/integridad de los inputs originales, CP00, estudios de ubicación ni auditorías. Ver source-tree-vs-zip.json.

Los cuatro submódulos no contienen gitlinks propios. CMake obtiene las transitivas bajo los pins y condiciones originales. [DEPENDENCY_PROVENANCE.md](DEPENDENCY_PROVENANCE.md) distingue **23 paquetes comprimidos descargados**, **20 fixtures ya incluidas en árboles fetched** y **15 repositorios Git incluidos los anidados**. No confundir esas 43 observaciones de archivos con 43 descargas. Las 38 declaraciones en official-dependencies.json son una enumeración del source, no una lista de ejecuciones.

La recursión automática de FetchContent también clonó submódulos de documentación/tests/otras plataformas registrados por las dependencias. No todos son necesarios para el compilador Windows. No se añadieron roots manuales ni se desactivaron partes del preset para ocultarlos; se conservó el mecanismo original y se registra esta limitación de minimización. Los parches propios del proyecto a funchook/capstone son parte del baseline de CMake, no host-lifetime.patch ni modificaciones propias al juego.

Providers auto efectivos: **Dawn package/shared v20260807.225922**, **SDL3 package/shared 3.4.10**, **nod package/shared v2.0.0-alpha.12**. No se sustituyeron por HEAD ni builds aproximadas. Se reconstruyó el host con esas dependencias prebuilt originales, sin afirmar haber reconstruido Dawn/SDL3/nod desde source. Donde el proyecto proporciona hashes se conservaron; donde solo proporciona release/tag se registra el hash observado sin inventar una validación upstream.

## Herramientas y comandos efectivos

- Windows x64 en windows-latest; Microsoft Visual Studio 18 / toolset path 14.51.36231.
- **MSVC 19.51.36260.0**, **Windows SDK 10.0.26100.0**.
- CMake **4.4.3**, Ninja **1.13.2**, Python **3.12.10**, Git **2.55.0.windows.5**, sccache **0.12.0**.
- vcpkg commit **9e593bb18ea69cc5095e012465dcd675a822ed0d**, release **2026.07.29**; tool **2026-07-27-98d7cb0cf1f4686a3e43aa5672b6230c1d56bce8**. Esta revisión fija infraestructura que el workflow oficial dejaba variable en C:\vcpkg; no cambia los pins del source.
- Ports freetype2.14.3 y zstd1.5.7, con libpng1.6.58, zlib1.3.2#1, brotli1.2.0, bzip2 1.0.8#6 y los dos helpers vcpkg-cmake/config. Todas sus versiones están fijadas por el checkout de ports y registradas en el artefacto.

Preset original: Ninja/MSVC amd64, RelWithDebInfo, CRT MultiThreadedDLL, debug Embedded, Sentry habilitado, vcpkg x64-windows, launchers sccache. No se deshabilitó funcionalidad del host ni se cambió código para hacer pasar el build.

```powershell
vcpkg install freetype:x64-windows zstd:x64-windows
cmake --preset x-windows-ci-msvc
cmake --build --preset x-windows-ci-msvc --parallel 2
```

Los wrappers en ci/run_phase.py registran comandos exactos, inicio/fin UTC, tiempo y exit code. El workflow conserva herramientas/acciones fijadas por SHA. [REPRODUCE.md](REPRODUCE.md) describe bootstrap, verificación, compilación y reversión; .github/workflows/devf-cp01-official-baseline.yml es el archivo acreditado.

## Incidencias y clasificación

Intento 1 (run38256216502): vcpkg PASS en121,468 s; preflight raw hash falló por EOL nativo Windows en un archivo con text=auto. Configure/build NO EJECUTADOS. **Error de configuración de checkout**, no error de source ni dependencia. Se resolvió fijando core.eol=lf antes de un checkout nuevo; preserva la excepción oficial .batCRLF. Se mantiene la exigencia de hashes originales, sin relajarla. Evidencia recibida en evidence/attempt1.

Intento 2: preflight/configure/build/staging PASS. Hay warnings originales, entre ellos deprecaciones de codecvt del MSVC STL; no se suprimieron ni se cambió el source. No se observaron errores de compilación/enlace. No hay bloqueo externo pendiente para este baseline.

## Recuperación y límite de esta etapa

Resolver el tag **DEVF_CP01_OFFICIAL_BASELINE_MSVC** para recuperar el checkpoint final. Su rama desciende de eea4742; DEVF/CP01 y CP01_HOST_EXPERIMENT se conservan sin cambios. El tag intermedio DEVF_CP01_BASELINE_CONFIGURED conserva el estado anterior al resultado. No se mueven tags ni se hace merge.

La compilación original queda acreditada. La integración y compilación del parche experimental será otra tarea: **no se realizó aquí**. Tampoco se acredita runtime/DX12 ni se abre GO de CP02. Mantener DISARMED_NO_REGISTRATION y detenerse al concluir este baseline.
