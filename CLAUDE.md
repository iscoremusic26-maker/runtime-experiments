# DEVF (Mods-Duskligh) — instrucciones operativas

Este archivo se creó en la rama `docs/devf-transfer-01`; otras ramas históricas (incluida `feature/devf-cp10-multi-room`) pueden no tenerlo hasta que el usuario decida integrarlo. Una vez integrado sigue siendo válido en cualquier rama de desarrollo. Complementa, sin contradecir, el `CLAUDE.md` de la carpeta superior de trabajo.

Referencia: `DEVF/TRANSFER_01_HANDOFF_2026-10-17.md`. Es una instantánea histórica de esa fecha: comprueba si existen actualizaciones posteriores antes de tomarla como el estado más reciente.

## Antes de trabajar
- Verifica rama, `HEAD` y `git status --short`, e informa cambios relevantes. La base validada del código CP10 `42fc87455624bde8b898a26a0512f708f02a3b26` es **referencia histórica**, no un HEAD obligatorio: los commits nuevos y legítimos no bloquean trabajo autorizado. Ante cambios imprevistos, conflictos o riesgo de perder trabajo, pausa esa operación y pide instrucciones (nunca reset/clean/force).
- La CI compila el espejo del repo privado `codex-cp00-inputs`, no este checkout. Un cambio aquí no llega a la CI hasta actualizar el espejo y `SOURCE_CI.json` (107 blobs fijados). No los modifiques sin encargo explícito; una etapa autorizada puede requerir sincronizarlos conservando la procedencia.

## Invariantes (no romper)
- Mod IDs `dev.devf.cp06_native_config_dual` y `dev.bokoblin.expansion`; servicios @1.0 y structs de 80 y 24 bytes; no mezclar versiones del mismo ID.
- E_OC2 nativo, perfil 510; capacidad global 8 (los legacy ocupan slots); separación 300 en el mismo room/layer.
- Paridad schema1/schema2 entre C# (`MultiConfig.cs`) y C++ (`shared/config.hpp`).
- Migración legacy `CP08_OBSERVED` (F_SP121/R03/L6) solo con su validador histórico (`PlacementGeometry.Check`); jamás para puntos QA nuevos (regresión `FLOOR_AMBIGUOUS`).
- Capa explícita 0–14; el sufijo `_00` del ARC no es capa. Sin wildcard de capa en DEVF.
- Cambios de JSON solo con arranque frío; sin hot reload. Rollback: restaurar la pareja anterior y los JSON de respaldo.

## Procedimiento
- Compilación: solo Windows GitHub Actions. Pruebas de juego: solo el usuario (Windows/DX12).
- Ticket, handle o `REQUEST_ACCEPTED` registran una edición, no un actor vivo.
- Estados: CI, SOURCE (código), USER_TESTIMONY, PENDING. Nunca "PASS universal".
- Datos locales: por defecto no leas AppData, partidas, logs, CISO/ISO, ROM, ARC/KCL/PLC, otros mods ni credenciales. Si el usuario lo autoriza para una tarea concreta, inspecciona solo lo necesario; esa autorización no es permanente. Los datos comerciales y las partidas no van a Git, PR, artifacts ni servicios externos; de los logs cita solo líneas relevantes y redacta lo sensible. Sin credenciales en documentación o Git.
