# POST01 — Evidencia

Fecha: 2026-11-01T04:5xZ (2026-10-31 America/Panama). Entorno local: WSL2/Linux, sin MSVC, sin Windows y sin juego. Todo lo de Windows salió del workflow privado.

## 1. Etiquetas
| Etiqueta | Estado | Qué lo respalda |
|---|---|---|
| `SOURCE_IMPLEMENTED` | sí | `src/mod.cpp`, `src/observer_core.hpp`; auditoría de texto `SOURCE_AUDIT_PASS` |
| `LAB_PASS` | sí (dobles, no runtime) | local g++ 20 `-fsanitize=address,undefined`: 8724 comprobaciones, 0 fallos; 4 mutaciones detectadas. En MSVC: el mismo lab, 8724 comprobaciones, `RESULT=LAB_PASS` (CI) |
| `WINDOWS_MSVC_PASS` | sí | MSVC 19.51.36260 x64 en `windows-latest`, ejecución 41274486531 |
| `ARTIFACT_DOWNLOADED_VERIFIED` | sí | descarga independiente en CI (job `independent-download`) **y** mía, con SHA-256 calculado en una carpeta nueva |
| `HUMAN_RUNTIME_PENDING` | pendiente | nadie lo ha cargado en Dusklight |
| `HUMAN_PASS` | NO | sin observación humana |
| G1 | `INSTRUMENTED_PENDING_RUNTIME` | G2 y G3 no iniciados |
| `COMPATIBILITY_PASS` | NO | sin configuraciones reales de HM/Bars/DEVF |

## 2. Fuente y SDK
- SDK oficial: `TwilitRealm/dusklight` @ `40457c6adb381928e4b5fef6ed459ed291edd5e2`; Aurora @ `3227d76c60e1e782ca576610bce61c9e7744d8be` (coincide con el submódulo del árbol oficial, `gh api …/contents/extern/aurora`).
- ZIP de Windows (LFS, repo de CI @ `9f95a34`): 56037777 bytes, SHA-256 `ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf`. `sdk/windows-amd64.lib`: 9400986 bytes, SHA-256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`, CRC `70c35731`. `dusklight.exe` `ffa99203…0049`. Todos fijados en `ci/build_windows.py` y verificados en cada ejecución.
- POST00: rama `docs/posture-post00-audit-20261031` @ `7fa57ef6b6513ae8a841c4ff0d75bb5332698b8e` (HEAD remoto verificado con `ls-remote` antes de empezar). Se usó como referencia; su numeración POST01–POST07 comprimida **no** se usa.

## 3. Git (todo en ramas nuevas y aisladas; sin PR, merge, tag ni release)
| Repo | Rama | Commits |
|---|---|---|
| `iscoremusic26-maker/Mods-Duskligh` | `feature/posture-post01-passive-observer` (desde `7fa57ef`) | `00c5e55` → `72232a0` → `6a80ebe` → `b4a0196` → **`ba7b7ac`** (código compilado por la ejecución final) → commit documental posterior (este archivo) |
| `iscoremusic26-maker/codex-cp00-inputs` | `ci/posture-post01-passive-observer` (desde `main` @ `9f95a34`) | `dd4bcf0`, `a95221a`, `996aec4`, `e4c7590`, **`037f29a`** (espejo de `ba7b7ac`, ejecución final) |
El espejo de CI contiene solo archivos nuevos: `POSTURE_SYSTEM/POST01/**` (CMake, mod.json, src, tests, ci), `POSTURE_SYSTEM/POST01_CI_SOURCE.json` (commit fuente + SHA-256 de cada archivo) y `.github/workflows/posture-post01-passive-observer.yml` (disparo `push` solo en esa rama; condición por repo privado y `GITHUB_REF`). Ningún workflow, rama, ejecución ni artefacto previo se tocó. El `build_windows.py` aborta si un archivo compilado difiere del ledger.

## 4. Ejecuciones de CI (todas en el repo de CI, rama `ci/posture-post01-passive-observer`)
| Run | Espejo de | Resultado | Motivo |
|---|---|---|---|
| 41273872316 | `00c5e55` | fallo | tipo `Frame` ambiguo con `Frame` de Aurora (`dolphin/perf.h`); el lab MSVC sí pasó |
| 41274001710 | `72232a0` | fallo (PE sin fijar) | compila; los imports reales incluían `dCcD_GAtTgCoCommonBase::GetAc`, getter con caché ⇒ se **retiró** (§HOOK_ABI_PASSIVITY 3) |
| 41274204620 | `6a80ebe` | fallo | solo discrepancia de la fijación (`__std_terminate` ya no se importa) |
| 41274352210 | `b4a0196` | build OK, descarga fallida | el job de verificación leyó `mod.json` con CRLF (autocrlf); error de CI, no del artefacto |
| **41274486531** | **`ba7b7ac`** | **éxito (build + descarga)** | https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41274486531 |

## 5. Ejecución final (41274486531, CI head `037f29a1ee7f53b6b36919dde3d4e675fb4a9329`)
- Toolchain: MSVC 19.51.36260 (VCTools 14.51.36231), Windows SDK 10.0.26100.0, CMake 4.4.4, Ninja 1.13.2, `-std:c++20 /O2 /Zc:inline- /GL-`.
- Todos los `static_assert` de ABI (firma, PMF de 8 bytes, tipos, 5 offsets) compilaron: la compilación del módulo terminó sin error. Los avisos del módulo (9) vienen de cabeceras del juego; ninguno de `src/`.
- Unidades de producción: `mod.cpp` y `sdk/src/game_feature.cpp`; el lab no entra en el módulo.
- DLL suelta: 24064 bytes, SHA-256 `7a6dafa50a0c33fa6036348115032517e7953b64d60e78b72a27013fddefd361`.
- Paquete `.dusk`: 12693 bytes, SHA-256 `adfe9f1884a7bb05fa4607b6814da48b670bc73be4060cbaf7df7eaac3ec9766`; miembros `mod.json` (idéntico a la fuente) y `lib/windows-amd64/mod.dll` (idéntica a la suelta). ID `dev.posture.post01_passive_observer`, versión `0.1.0`.
- PE: AMD64, sin TLS ni delay-import; exports `mod_ctx, mod_initialize, mod_meta, mod_shutdown, mod_update`; metadata: 1 HEADER, 4 IMPORT (`game 2.0`, `hook 1.1`, `host 2.2`, `log 1.0`), 1 HOOK_MEM; thunk ligado a `?damage_check@daE_OC_c@@QEAAXXZ`; imports de `dusklight.exe` = solo ese símbolo; el resto es arranque CRT/EH. `PE_AUDIT_PASS`.
- Artefactos (30 días, expiran 2026-12-01): `POST01_TEST_41274486531_1` (digest `41f889ad…186e`, 13503 bytes), `POST01_TEXT_41274486531_1` (`52304b3e…edc4`), `POST01_DOWNLOAD_VERIFIED_41274486531_1` (`964611ae…85fb`). Evidencia de texto: `result.json` SHA-256 prefijo `5cf03001…` y manifiesto `evidence-sha256.json` dentro del artefacto.

## 6. Verificación independiente en local
Descarga con `gh run download` a carpetas nuevas; `sha256sum -c SHA256SUMS.txt` OK; `unzip` a una carpeta vacía; DLL `7a6dafa5…d361`; `mod.json` idéntico a la fuente; `pe_audit.py -I --expected ci/expected_pe.json` = `PE_AUDIT_PASS`; `objdump -p` (herramienta distinta) confirma el único import de `dusklight.exe`: `?damage_check@daE_OC_c@@QEAAXXZ`. La DLL **no se cargó ni se ejecutó**.

## 7. Desviaciones respecto a POST00 y límites
- POST00 proponía leer el tipo de AT y el actor del impacto: se omitieron por no ser pasivos o seguros (ver HOOK_ABI_PASSIVITY §3). El POST01 real solo registra bit TG crudo.
- Las fuentes de HM/Bars siguen sin demostración de reconstrucción byte a byte (heredado de POST00); no bloquea POST01. La coexistencia con ellos y con DEVF/Expansion **no se ha probado**: solo se sabe que ninguno hookea `damage_check` (POST00).
- No hay medición de coste en el juego. El hook corre una vez por ejecución de cada E_OC, con trabajo O(1) (ledger de 16 entradas).
- Un warning de inline en el log del host invalida G1 aunque el hook se haya instalado.
- La pasividad del binario no se demuestra solo con imports: se apoya en revisión de fuente, auditoría de texto, build y, sobre todo, la prueba humana pendiente.
- Bloqueos: ninguno de acceso. No se usó `SOURCE_CI.json` ni el espejo CP10 de DEVF.
