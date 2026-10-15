# DEVF CP06 — Configuración externa: TEST PARCIAL de un sitio

**CHECKPOINT_CP06_PARTIAL / PRIVATE_SINGLE_SITE_TEST_VERIFIED / HUMAN_RUNTIME_NOT_TESTED.**
MSVC/30casos/PE-ABI/7negativos/paquete/descarga real PASS. **NO es el MVP completo CP06**.

Implementado: catálogo schema1,2presets realmente distintos (black_guard150/negro/AI CP05; native_elite220/nativo/sin HPwrite/tinte/guardia), archivo externo legible placements.json leído una vez al inicio frío. Cambiar preset/yaw,activar/desactivar/quitar entrada no necesita recompilar. Un solo placement activo en el sitio humano F_SP121/3/6(-1250,-6304.00830078125,60750). Archivo inválido/ausente deja0actores,sin fallback.

**Límites reales:** moverXYZ a otra ubicación rechaza SITE_NOT_VERIFIED;2activos rechaza MULTI_ACTIVE_NOT_SUPPORTED. Dos entradas o dos presets alternativos NO significan dos actores/zonas simultáneos. No hay sceneepoch general ni vínculo StageActorHandle→ActorId; se conserva identidad exacta CP05 para1record. GateA de movimiento libre yB de2placements/2zonas todavía no cumplidos. No navegación a home corregida.

[Descarga privada PARTIAL](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831/artifacts/11951843169), ZIP83222/SHA256 `e79a0e76d3471530927ca169bbe4cbe107689b36200a63119ace012d261a10a1`. Dusk41419/SHA256 `b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2`. Caduca **2026-11-14 01:04:00 Panamá** (UTC06:04). Nuevo ID dev.devf.cp06_single_site v0.6.0; instalar sólo este DEVF. No host/ROM/saves/SDK/Aurora ni paquetesCP01–05 modificados.

[HUMAN_TEST](HUMAN_TEST.md) indica dónde poner JSON; [CP06_SCHEMA](CP06_SCHEMA.md), [SOURCE_AND_SERVICE_GATE](SOURCE_AND_SERVICE_GATE.md), [TEST_RESULTS](TEST_RESULTS.md), [BUILD_AND_PACKAGE](BUILD_AND_PACKAGE.md), [RECOVERY](RECOVERY.md). CP05 humano sellado aparte; sus pendientes no se transfieren a PASS. CP07/08/expansión no iniciados.
