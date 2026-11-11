# Enemy Spawner (Standalone) 0.1.0: resultados de CI

Estado: **CI FULL PASS, HUMAN_RUNTIME_PENDING**. No se ha ejecutado en el juego.

| Dato | Valor |
|---|---|
| Fuente compilada | `983e1286ebd8a0f5c7dc66870e70bd0a4293ef33` (rama `feature/enemy-spawner-standalone-v0-1-0`) |
| CI | rama `ci/enemy-spawner-standalone-v0-1-0`, run FULL 42983880736 (`build` e `independent-download` en verde) |
| Artefacto | 13838413018, `ENEMY_SPAWNER_STANDALONE_0_1_0_PRIVATE_TEST_windows-amd64_983e1286ebd8.dusk`, 15 659 bytes, caduca el 2026-12-11 |
| SHA-256 `.dusk` | `6627c4a0274239371a39d0ea8d8ff20e5856aefd5eaee4b359970bbbb03647ff` (recalculado en descarga propia) |
| DLL | 32 256 bytes, SHA-256 `3f1efc13203bab93575d2be964c30137190cf06f31c145ec382dc3361e0355f9`, PE32+ AMD64 |
| Miembros | `mod.json`, `lib/windows-amd64/mod.dll` |

| Prueba | Resultado |
|---|---|
| Reglas de fuente | PASS, 20 negativos rechazados |
| Auditoría PE | PASS, 21 imports del juego, sin ganchos ni servicio de ganchos |
| Catálogo frente a Dawnlight `b5e9046` | PASS, 45 entradas |
| Código de Expansion vendorizado | PASS, hash de 0.17.0 |
| Laboratorio del núcleo | 1 247 comprobaciones, 0 fallos |
| Laboratorio del adaptador | 56 comprobaciones, 0 fallos |
| Mutantes | 34/34 detectados, 0 timeouts |
| Descarga independiente | `ARTIFACT_DOWNLOADED_VERIFIED` |

Tiempos medidos: FAST 1 min 9 s (run 42983244543), INTEGRATION 56 s (42983669911), FULL 2 min 5 s (42983880736).

Fallos encontrados y corregidos durante el trabajo:
- Las cabeceras dan offsets de GameCube: se quitaron aserciones de offsets inventados.
- El modelo de laboratorio tenía un destructor no virtual.
- El control de plan de la CI comparaba el orden de las fases.
- Dos mutantes sobrevivieron al principio, y se añadieron pruebas que los detectan.
