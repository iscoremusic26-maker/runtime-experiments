# Enemy Posture System 0.11.5 — HUD FIX03 PRIVATE TEST

Candidato acumulativo Windows x64 / DX12 para Dusklight 2.0.3. FIX03 restringe el dibujo que puede ocultarse al clúster contextual **inferior**, certificado por propietario y slot nativos, cuando invade la barra visible de Link. Raíces y HUD ajeno se conservan, aunque crucen la banda. No se reubica el prompt y sus acciones no cambian.

La alineación EHB CP06, Scoop y la presentación independiente de Link se conservan de 0.11.4, donde el usuario confirmó su corrección. La fuente del combate permanece congelada en 0.11.2. El laboratorio reproduce el borrado de HUD de 0.11.4 y lo rechaza con los callbacks nuevos. Esto sigue siendo **HUMAN_RUNTIME_PENDING**: ni CI ni las comprobaciones estáticas ejecutan Dusklight/DX12.

## Paquete verificado

[Descargar PRIVATE TEST 13255667942](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41687970224/artifacts/13255667942) · [CI 41687970224](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41687970224).

`POSTURE_HUD_FIX03_0_11_5_PRIVATE_TEST_windows-amd64_2d0e59329f14.dusk`

137446 bytes; SHA-256:

`1dbf22a4c985e2ff334bd774faba86ac6bef717e55d135dbca7755103cd2f660`

ID `dev.posture.post05_selective_reactions`; versión `0.11.5`. Expiración informada por GitHub: **2026-12-03T13:04:19-05:00 (Panamá, UTC−5)**.

Fuente compilada `2d0e59329f14d822c1905ee7953d337959932f1f`; CI `29230b450e0b77bdab7aa3edc1f272e17e2a168b`. El commit documental es un descendiente separado; no se recompiló por añadir estos informes.

MSVC x64, auditoría PE, 2,829,095 comprobaciones en 18 labs, 67,218 del adaptador FIX03, 412 mutaciones detectadas, 126 negativos semánticos de fuente, 20 negativos PE, dos negativos de instrucciones y ambas descargas verificados. Juego nativo: **HUMAN_RUNTIME_PENDING**.



## Instalación y prueba humana breve

Con el juego cerrado, guarda el `.dusk` de postura 0.11.4 **fuera de la carpeta mods** y sustituye solamente ese mod por el `.dusk` 0.11.5 del artefacto TEST. Conserva los otros siete mods sin modificarlos. No cargues dos versiones del ID `dev.posture.post05_selective_reactions`. Arranca en frío con DirectX12.

A. Provoca barra de Link visible y Shield attack/B inferior como en la captura. Deben conservarse corazones, minimapa, ITEMS/MAP, rupias y botones superiores; solo desaparece el clúster inferior que invade la barra. La barra debe verse completa. Guarda una captura.

B. Espera a que la barra termine hold/fade y desaparezca: Shield attack/B inferior debe reaparecer en su posición nativa, sin movimiento ni residuos; todo el HUD restante sigue intacto. Guarda otra captura.

C. Repite con Jump/Jump Attack, Helm Splitter y cambios rápidos R/B, con y sin barra. Las indicaciones superiores, aunque tengan el mismo texto, deben conservarse y las acciones funcionar. Comprueba también Open/Talk/Pick Up disponibles y parries, defensa manual y rearme soltando R.

D. Prueba Scoop con botella y un combate corto con Blue/Red/Black, incluyendo 10–20 golpes de espada seguidos. Confirma ausencia de parpadeo de Link, alineación vida/postura enemiga durante movimiento/caídas/cámara, y HUD general intacto al aparecer la barra. Comprueba guard-break de Link y su penalización/rearme. Si es posible repite a 30/60 FPS; esos FPS no se han certificado en el laboratorio.

E. Pausa, menú, cambio de sala y regreso; prueba lobo/humano cuando proceda. No debe quedar supresión residual ni aparecer la barra en estados donde el juego deba ocultarla. Conserva el log completo para revisión privada.

**FAIL inmediato** si desaparecen corazones, minimapa, rupias o un botón superior por la aparición de la barra. Si aparece un halo/texto inferior residual o una ruta no clasificada, también requiere revisión: no se declara que todos los píxeles nativos hayan sido medidos. La telemetría `POST_HUD_FIX03_INIT/SUMMARY` cuenta rutas, propietarios, raíces conservadas, leases y cobertura; no reemplaza las capturas humanas.

## Rollback

Cierra el juego, retira 0.11.5 y devuelve únicamente el backup 0.11.4. SHA-256 esperado del `.dusk` 0.11.4:

`c63d436e8a475ef5b19732ac1006fad14599921232eca5545c33fb477d415fa4`

[Artefacto 0.11.4 verificado, CI 41673271040](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41673271040/artifacts/13248769855). Su fallo conocido es la supresión excesiva del HUD; el retorno sirve para recuperar el estado anterior. Como segunda referencia, 0.11.2: SHA-256 `2aa715980bc81af0db13622fc9e210100bcd973cd1255044d570a91f092eba0a`, [artefacto 13201587185](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41570019310/artifacts/13201587185). No se alteran partidas ni otros mods.

[Implementación y causa](IMPLEMENTATION.md) · [Resultados verificables](RESULTS.json) · [Evidencias](EVIDENCE/)
