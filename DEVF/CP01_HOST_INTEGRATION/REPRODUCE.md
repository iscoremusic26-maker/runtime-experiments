# Recuperación y reproducción de la integración CP01

El tag final de esta etapa se consignará al recibir/verificar la evidencia. Recuperar siempre en un checkout independiente, sin reset/clean sobre trabajo ajeno. No mover tags anteriores ni hacer merge. Baseline 413377f y experimento eea4742 permanecen en el historial.

## Source y aplicación

Usar el source oficial 40457c6 y los cuatro gitlinks de ../CP01_BASELINE/SOURCE_LOCK.json. Los requisitos de EOL, toolchain, vcpkg y preset son los del baseline acreditado. No repetir su compilación intacta. Los comandos de clone/submodule/bootstrap están en ../CP01_BASELINE/REPRODUCE.md; reutilizarlos para una copia nueva.

Desde el checkout de orquestación y Developer Prompt MSVC amd64, con sccache0.12.0, Ninja, CMake y Python disponibles:

```powershell
# Preflight intacto, no build del baseline.
python DEVF/CP01_BASELINE/ci/baseline_evidence.py preflight --source official --vcpkg baseline-vcpkg --evidence evidence --lock DEVF/CP01_BASELINE/SOURCE_LOCK.json
python DEVF/CP01_HOST_EXPERIMENT/ci/prepare_experiment.py --source official --out private-extracted
python DEVF/CP01_HOST_INTEGRATION/ci/integration_evidence.py preflight --source official --vcpkg baseline-vcpkg --evidence evidence --lock DEVF/CP01_BASELINE/SOURCE_LOCK.json
python DEVF/CP01_BASELINE/ci/run_phase.py --phase configure --source official --evidence evidence -- cmake --preset x-windows-ci-msvc -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
python DEVF/CP01_BASELINE/ci/run_phase.py --phase build --source official --evidence evidence -- cmake --build --preset x-windows-ci-msvc --parallel 2
python DEVF/CP01_HOST_INTEGRATION/ci/run_directed.py --source official --evidence evidence --temp private-directed
python DEVF/CP01_HOST_INTEGRATION/ci/integration_evidence.py collect --source official --vcpkg baseline-vcpkg --evidence evidence --lock DEVF/CP01_BASELINE/SOURCE_LOCK.json
```

Detenerse si falla un comando y clasificar el error. No cambiar hashes, source o dependencias para ocultarlo. El preset install escribe únicamente official/build/install. El host EXE no debe ejecutarse, instalarse, publicarse ni incluirse en artefactos. private-extracted/private-directed contienen source efectivo y binarios de diagnóstico temporales; tampoco son entregables.

## CI y pruebas incrementales

.github/workflows/devf-cp01-host-integration.yml ejecuta el build completo en Mods-Duskligh. El snapshot iniciado es 55cbce11239adb3375e6a40002dd67a331b9ac99; cambios posteriores del driver/informes no cambian ese resultado. Las versiones finales del driver requieren su propia evidencia de ejecución.

El laboratorio privado establecido en codex-cp00-inputs utiliza la rama experiment/devf-cp01-host-integration-directed, PR draft #4 y .github/workflows/devf-cp01-host-directed.yml. Solo contiene copias de herramientas/parche propios, con hashes en CI_SOURCE.json. No lee los ZIP/ARC existentes en ese repositorio. Configura el mismo source y compila exclusivamente las siete TUs/driver para evitar repetir el host por cambios de la prueba. Las funciones/layouts extraídos permanecen en RUNNER_TEMP, mientras el artefacto contiene solo JSON/logs.

Para repetir únicamente el diagnóstico en una copia ya configurada, usar run_directed.py, sin repetir build/install. El script obtiene flags del compile_commands.json efectivo y usa cl.exe directamente para el driver; /Od afecta solo el diagnóstico. Sus adaptadores son explícitos y no autorizan una declaración de seguridad global.

GitHub puede restringir workflow_dispatch a workflows presentes en default. No hacer merge para habilitarlo. Una reproducción autorizada puede usar un PR draft nuevo con el snapshot correspondiente o los comandos Windows anteriores. No ejecutar otra etapa baseline intacta.

## Reversión y bloqueo

No hay instalación que revertir. Conservar los checkouts originales; descartar solamente los árboles experimentales propios cuando deje de ser necesaria su evidencia. No modificar EXE, saves, flags, recursos o instalación del usuario. Mantener DISARMED_NO_REGISTRATION.

INTEGRATION_REVIEW.md describe los riesgos graves de reentrancia y teardown global. Antes de una prueba activa se requiere resolverlos mediante una etapa específica, pruebas afectadas y evidencia runtime/ubicación ya pendiente. Este checkpoint no autoriza activación, prueba DX12 ni CP02.
