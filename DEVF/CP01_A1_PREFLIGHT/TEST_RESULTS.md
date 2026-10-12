# Resultados incrementales ejecutados

**G1 build/enlace y laboratorio PASS; juego/Windows DX12 runtime NOT_VERIFIED.** No se repitieron CP00, las26 comprobaciones anteriores, suites del host, Dawnlight ni análisis KCL/ARC/WRock/Digpl.

CI privada [run38297058072](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38297058072), [job114970558041](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38297058072/job/114970558041), primer intento, success. [PR de CI #5](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/5) draft sin merge; rama ci/devf-cp01-a1-g0-g4, head `988bafed31e93674082cc926086e56d92728c175`. GITHUB_SHA `770f0d18daf5b5a53cb01336029795850eeb7cba` corresponde a la referencia de evento PR; checkout explícito usa el **head**, no ese merge sintético. Fuente propia compilada del repo principal `57a167a6c650ab9473db31c4eac531dba8e6a127`.

MSVC **19.51.36260.0**, linker14.51.36260.0, Visual Studio18 Enterprise, toolset14.51.36231, Windows SDK **10.0.26100.0**, CMake4.4.3, Ninja. Fuente oficial40457c6 intacta; Aurora3227d76 para headers; SDK FEATURES game/epoch2; import lib AMD649,400,986bytes SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`. Se reutiliza la acreditación CP00 del original; checkout LFS real y CRC/hash del miembro de lib comprobados, sin extraer EXE ni repetir auditoría completa ZIP/host.

Intervalo de ejecución propia **18.101s** (suma de comandos17.203s), UTC19:21:50.900796–19:22:09.002284 del12oct2026. Configuración5.875s, build6.625s, lab0.016s. Comandos/tiempos/versiones completos en [result.json](evidence/windows-pass/result.json), logs preservados en evidence/windows-pass.

```powershell
cmake -S DEVF/CP01_A1_PREFLIGHT -B <work>/build -G Ninja `
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=cl `
  -DDUSK_SOURCE=<clean-40457c6> -DDUSK_GAME_EXE=<exact-windows-amd64.lib>
cmake --build <work>/build --target devf_a1_observer a1_observer_lab --parallel 2
<work>/build/a1_observer_lab.exe
dumpbin /imports <work>/build/devf_a1_observer.dll
dumpbin /exports <work>/build/devf_a1_observer.dll
```

| Comprobación ejecutada | Resultado | Alcance |
|---|---|---|
| Configuración/compilación/link DLL+lab AMD64 MSVC | PASS_LAB | Lector nativo real compilado y enlazado; sin construir/ejecutar host |
|12 imports game realmente utilizados | PASS_STATIC | PE importa dusklight.exe;10 funciones y2 datos públicos (mStayNo/mStatus); allowlist completa en result.json |
| Metadata oficial | PASS_STATIC | HeaderABI1; exclusivamente imports requeridos Host2.2, Log1.0, Game2.0; sin hooks/exports de servicios |
| Laboratorio incremental | PASS_LAB **36 comprobaciones** | Misma implementación mod/core; lector nativo sustituido por fixture explícito. Versiones, headers, errores, logs, reset/idempotencia, snapshots inválidos, layer opaco/ciclo/límite |
| Guardas de compilación | PASS_LAB | Configuración positiva exit0; READ_ONLY0, ENABLE_SPAWN y ENABLE_MUTATION fallan exit2 como esperado |
| Presupuesto log/lecturas | PASS_LAB |100000updates sintéticos:62capturas,63líneas antes de shutdown,64total; ninguna lectura después del límite/shutdown |
| Fuente propia y host | PASS_STATIC | Hashes LF del código compilado coinciden con árbol principal; fuente oficial tracked intacta |
| Siete registros naturales/FILI | PASS_STATIC | Herramienta incremental lee caché ya decodificada; FILIbitSwFF; no reanálisis geométrico |
| Ejecución del lector nativo/descarga en host | NOT_VERIFIED | Laboratorio no invoca Game ABI ni engine real; no aporta garantía runtime de préstamos/transiciones |
| Renderer/colisión/spawn/cleanup de enemigo | NOT_VERIFIED, NOT_TESTED | Sin ejecución del juego, actor nuevo ni TEST activo |

DLL propia compilada18,432bytes, SHA256 `ba78e5da935cbb1815993c2fc3ad377360ccc23cfe1fa01c259c629375134b4e`; **no subida ni distribuida**. No .dusk, install, host build ni arranque del juego. Las advertencias C4805/C4806/C4068 proceden de headers originales; no se editaron para ocultarlas. No error de compilación ni reintento necesario.

Artefacto textual id11768783927,7,686bytes, SHA256 GitHub `abc8050097518c7f621ff99af93d790f181bf1861e1a664d40ccde27f4e4daca`. Digest, CRC de12miembros, lista exclusiva .log/.json, UTF8 y hashes propios contrastados por ci/collect_windows.py; [windows-verification.json](evidence/windows-verification.json). Logs/resultados conservados en Git para que la caducidad del artefacto (26oct) no pierda evidencia. Las herramientas posteriores de extracción no cambian el módulo/lab, por lo que no se repitió la build aprobada.
