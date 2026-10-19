# CP19 FIX02 — sonidos universales + chip de escudo · Expansion 0.16.2 TEST privado

Sustituye a la 0.16.1. Windows x64, Dusklight 2.0.3@40457c6, DX12. Una sola Expansion; Provider/editor 0.13.0 y JSON intactos.

- **Audio:** los Bokoblin de DEVF cargan su grupo de sonidos nativo en un bloque de memoria de audio propio, fuera del que llena la sala. Vale en cualquier sala, escenario y capa. No se borra nunca, para no quitar sonidos de la sala.
- **Escudo:** un golpe de Black en furia que el motor confirma como bloqueado por el escudo quita exactamente 1/4 de corazón (sin multiplicador ni armadura) y pone a Link rojo un instante, sin romper la guardia.
- FIX01 (arranque sin crash) y las correcciones A–G de CP19 no cambian.

Descarga (privada): [artifact 12217026541](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39312607981/artifacts/12217026541) del run 39312607981, caduca 18-11-2026 14:40:37 America/Panama. Dentro del ZIP: `BokoblinExpansion_0.16.2_CP19_FIX02_TEST.dusk`, 151 985 B, SHA-256 `2e11259916504da2bf127d0ab20f9b3db4776e3d2e10c9d05f0c752bc4053fea`.

Ver IMPLEMENTATION, SOURCE_AUDIT, HUMAN_TEST, RECOVERY y TEST_RESULTS. Estado: SOURCE_IMPLEMENTED / LAB_PASS / WINDOWS_MSVC_PASS / INDEPENDENT_DOWNLOAD_PASS / HUMAN_RUNTIME_PENDING (audio y escudo).
