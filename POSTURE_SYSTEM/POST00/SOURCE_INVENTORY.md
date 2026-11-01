# POST00 — Inventario de fuentes y procedencia

Enemy Posture System, auditoría de arquitectura. Fecha: 2026-10-31 (America/Panama), 2026-11-01T04:05Z UTC.
Todo se hizo en solo lectura. No se compiló ni se ejecutó nada en Windows.

## 1. Dusklight v2.0.3 oficial (autoridad principal)

| Recurso | Ruta real | Identidad comprobada | Estado |
|---|---|---|---|
| ZIP de fuente | `/home/<user>/dusklight/dusklight-2.0.3.zip` (copia idéntica en `/home/<user>/codex-cp00-inputs/`) | SHA-256 `9dbdc0b068df24c3fbb680c87be25e904978f04b315e2051e3c6203476516008` = valor esperado. El comentario del ZIP (`unzip -l`, línea 2) es `40457c6adb381928e4b5fef6ed459ed291edd5e2` | VERIFIED |
| Árbol extraído | `/home/<user>/dusklight_work/bars_203/ref/src/dusklight-2.0.3/` | 14 archivos clave (lista en `VERIFICATION.json`) idénticos byte a byte al ZIP (`unzip -p` frente a `sha256sum`) | VERIFIED |
| Distribución Windows | `/home/<user>/dusklight/Dusklight-v2.0.3-win32-x86_64.zip` | SHA-256 `ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf` = valor esperado | VERIFIED |
| `dusklight.exe` | `/home/<user>/dusklight_work/bars_203/ref/win/dusklight.exe` | SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`, igual a `unzip -p … dusklight.exe \| sha256sum`. PE `pei-x86-64`, ImageBase `0x140000000` | VERIFIED |
| Biblioteca de importación del SDK | `sdk/windows-amd64.lib`, dentro del ZIP de Windows | Exporta `?damage_check@daE_OC_c@@QEAAXXZ`, `?setActionMode@daE_OC_c@@QEAAXHH@Z`, `?offTgSph@daE_OC_c@@QEAAXXZ`, `?executeBigDamage@daE_OC_c@@QEAAXXZ` y `?setStabPos@daE_OC_c@@QEAAXXZ` (`grep -a`) | VERIFIED_TOOL |
| Repositorio público | https://github.com/TwilitRealm/dusklight/tree/40457c6adb381928e4b5fef6ed459ed291edd5e2 | No se consultó por red: se usó la copia local verificada | — |

Prefijo de URL para las citas: `https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/`.

## 2. DEVF / Bokoblin Expansion (repos privados, `gh` con permiso ADMIN)

| Recurso | Rama / SHA | Uso en POST00 |
|---|---|---|
| `iscoremusic26-maker/Mods-Duskligh`, rama por defecto | `checkpoint/devf-cp00-windows-20261011` | No se usó como base |
| Clon local `devf/Mods-Duskligh` | `feature/devf-cp10-multi-room` @ `42fc87455624bde8b898a26a0512f708f02a3b26`, limpio | Solo leído. Sin cambios |
| PR #81 CP21 (draft, OPEN) | `feature/devf-cp21-public-package` @ `fe47c8b828939829914d466a425cb1e2c0223cd9` | Leído con `git show`/`git grep` sobre el objeto, tras un `git fetch` de solo lectura. No se hizo checkout |
| PR #80 CP20 (draft, OPEN) | `feature/devf-cp20-explicit-blue-red-black` @ `d9f83eaabff549440a10a33c002bf8e2e37945a6` | Base del #81. Su contenido se consultó a través del árbol de `fe47c8b` |
| `iscoremusic26-maker/codex-cp00-inputs` | local `ci/devf-cp10-multi-room` @ `aff0b5d9f522a1944a15e5cd522a187a5f9b9a6b`, limpio | No modificado. Solo se usaron sus ZIP como comprobación de hash |
| Handoff | `DEVF/TRANSFER_01_HANDOFF_2026-10-17.md` (en `fe47c8b` y en `docs/devf-transfer-01` @ `b33309871da1…`) | Solo se localizó. La información de hooks se tomó del código CP21 |

Archivos CP21 leídos: `DEVF/CP21_PUBLIC_RELEASE/README.md`, `runtime/DEVF/CP19_FIX02_UNIVERSAL_AUDIO_BLACK_SHIELD_CHIP/expansion/mod.cpp` (L127–135 y L2000–2025), `.../expansion/cp19_policy.hpp` (L1–30), `.../CP10_5_DAMAGE_BLUE_RED_BLACK/expansion/damage_policy.hpp` (L1–30), `.../CP07_2B_BOKOBLIN_EXPANSION_PILOT/shared/devf_encounter_v11.h`, además de búsquedas `git grep` de `DEFINE_HOOK|add_pre|add_post|EXPORT_SERVICE` en `DEVF/CP21_PUBLIC_RELEASE` y `DEVF/CP20_EXPLICIT_BLUE_RED_BLACK`.

## 3. Enemy Health Multiplier y Enemy Health Bars (locales, sin remoto)

| Recurso | Ruta / commit local | Correspondencia con lo distribuido |
|---|---|---|
| HM 2.0.3, fuente `core8` | `/home/<user>/dusklight_work/hm_203` (git local `master` @ `cc9f1ed9c71aa69753ee1adccba361dfb2c0701d`, limpio). `core8/src/mod.cpp` SHA-256 `5c70f9cd…a6d6` | `core8/mod.json` declara la versión `2.0.3-cp11-arrow-route-test`, la misma que figura en `release/HM203_BARS203_WINDOWS_DX12_VALIDATED_PAIR_2026-10-13/RELEASE_MANIFEST.json`. **No se verificó que el .dusk se reconstruya byte a byte** desde esta fuente |
| Bars 2.0.3 con integración HM | `/home/<user>/dusklight_work/bars_203_hm` (git local `hm-integration` @ `e9b42a4dab2e7a4e0e69b2d634dedacaa7ce2102`; 4 archivos sin seguimiento ajenos, intactos) | `mod/mod.json` `2.0.3-cp06-armos-test`, la versión del par validado. Misma reserva sobre la reconstrucción |
| Evidencia de hooks de HM | `hm_203/evidence/cp01_hook_targets_verification.md` | Reutilizada. Ya había verificado que `daE_OC_c::damage_check` y `cc_at_check` no tienen el flag INLINE |
| Herramienta de manifiesto | `hm_203/tools/manifest_query.py` (existente, reutilizada; caché en el scratchpad) | Sin herramientas nuevas |

## 4. Recursos no encontrados o no usados

- `/workspace/...`: no existe en este entorno. No hace falta: los ZIP y el árbol locales están verificados.
- No se encontró documentación previa de Posture System, ni local ni en los repos. POST00 parte de cero en su ámbito.
- Las fuentes de Bars/HM tienen la reserva de reconstrucción del punto 3. Por eso la auditoría de dependencias es parcial (`INCOMPLETE_DEPENDENCY_AUDIT` para «byte-exact»).
- No se leyeron logs, partidas, ISO/CISO ni assets del juego.
