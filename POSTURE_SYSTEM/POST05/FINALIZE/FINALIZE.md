# POST05-FINALIZE 0.5.3 — fases tempranas y finales de E_OC2

Etiquetas: **[R]** log real del usuario · **[S]** fuente exacta · **[B]** binario del juego · **[L]** laboratorio · **[C]** CI · **[P]** pendiente de prueba humana.

## Punto de partida
- **Base:** 0.5.2, fuente compilada `e554fd1b4201ac1b4b67790d4f1f3f99974cff20`, documentos `f345414836ff25aad3de6c289ec66e869e6f3f4e`. Rollback: `.dusk` `f39b8827…5021`, artefacto `13105797739`.
- **Rama nueva:** `feature/posture-post05-finalize`, creada desde `f345414`. Los archivos de build de `f345414` son idénticos a los de `e554fd1`.

## Causa demostrada [R]
Logs `dusklight-20261101-185034` (POST05 + Zora Swim, SHA-256 `f083dba9…a7594`) y `dusklight-20261101-184349` (8 mods, `6cc1f3b4…dfe8`). Evidencia saneada en `evidence/`; el extractor da 0 violaciones.

- **Único rechazo por fase E_OC2 en las dos sesiones:** sesión aislada, Red 163 gen 9, evento 2. ATTACK 2 (clip C), `frame=1.00`, `rate=1.00`, postura 25→50 → `ALLOW_VANILLA E_OC2_FRAME_EARLY`.
- **Origen del gate de `frame` 1:** protege el x2 pendiente de Expansion (A5-2). En esa sesión Expansion no estaba cargado, así que el gate interrumpió un ataque sin necesidad.
- **Resto de reacciones vanilla por debajo de 100:** en su mayoría FIND estado 4 (aproximación/retroceso, también la espera tras un ataque, con `speedF` 0 o -3) y letales.
  - [S]: FIND 4 solo pasa a ATTACK 0 a 200–400 de distancia y de cara a Link. No es un ataque en curso: sigue vanilla por diseño.
  - Todos los BIG_DAMAGE observados fueron con postura 100.

## Cambio (mínimo)
- **Señal de entorno `E2Env`** (`probe_variant_ai_env`, solo en `mod_update`, cada 30 ticks hasta detectar presencia):
  - consulta `get_service("dev.devf.encounter_placement.v11", 1, 0)`, solo de existencia; el puntero devuelto únicamente se compara con nulo;
  - fundamento [S]: Bokoblin Expansion 0.17.0 la importa como **obligatoria** (`IMPORT_SERVICE(DevfEncounterPlacementServiceV11, …)`, CP21 `mod.cpp` :131), y el SDK (`mods/api.h`) no carga un mod con un import obligatorio sin resolver. Si la consulta da `MOD_UNAVAILABLE`, Expansion no puede estar activo: **NATIVE_ONLY**;
  - cualquier otro resultado, una excepción o la falta de comprobación cuentan como **EXPANSION_POSSIBLE**, y la presencia queda fija para toda la sesión;
  - la presencia nunca identifica un actor: solo la **ausencia** se usa como prueba.
- **`e2_allowed()`** (`reaction_core.hpp`) decide qué fase se suprime. Lo demás sigue igual que en 0.5.2: identidad, generación, collider, efectos nulos, potencia, relectura, el único escritor de 3 campos y un solo hook.

| Fase PRE E_OC2 | NATIVE_ONLY (Red 2/2) | EXPANSION_POSSIBLE |
|---|---|---|
| B/C maduro, frenada de ATTACK 0 | suprime | suprime (igual que 0.5.2) |
| `frame` 1 con `rate` 1,15 | suprime | **suprime** (`X1_15_ALREADY_OWNED`: un x2 pendiente deja `rate` 1) |
| `frame` 1 de Black 3/3 | — (potencia 3/6 implica Expansion) | **suprime** (`BLACK_BASE_NO_X2_PENDING`: sin furia al decidir no hay x2 pendiente) |
| `frame` 1 con `rate` 1 (Red), Black 6/6 | **suprime** (Red) | vanilla `X2_PENDING_POSSIBLE` |
| tick de arranque (`speedF` ≤ 1,5) | **suprime** | vanilla `RATE_DECISION_THIS_TICK` |
| fin de clip (`isStop`) | **suprime** (como Blue) | vanilla `CLIP_END_EXPANSION_CHAIN` |
| animación no autenticada, ATTACK 3 | vanilla | vanilla |

- **El log de decisión añade:**
  - `env=NATIVE_ONLY|EXPANSION_POSSIBLE|UNKNOWN`;
  - `compat=` con el motivo;
  - en el resumen: `e2_applied_phase`, `e2_env` y `env_now`;
  - `POST05_E2_ENV`, como máximo 4 líneas;
  - conservación `r8_e2_phases`.

## Por qué no hay una política común con Expansion [S][L]
- **Expansion recibe el golpe antes que el hook:** su `execute` PRE lee el bit de golpe (`f.hit`), hace `pre_valid = false` y, en su POST, omite la decisión de tasa del arranque (`red_ai_policy.hpp` :381) y el x2 pendiente de `frame` 2 (:374).
- **El hook llega tarde y no hay alternativa limpia:**
  - todo eso ocurre antes de `damage_check`, y la decisión es privada de Expansion;
  - conservar el x2 exigiría un segundo escritor de `rate` que imitase su decisión privada (prohibido y sin datos), o editar Expansion (fuera de alcance).
- **Contraprueba en `rb_lab`:** aplicar la regla NATIVE_ONLY a actores de Expansion rompería el x1,15 o el x2 en **120** gemelos. Por eso el entorno es necesario.

## Pruebas [L]
- **Fixture del evento real** (`rb_lab` a09): Red E_OC2 2/2; evento 1 en FIND 3 (0→25, vanilla) y evento 2 en ATTACK 2, `frame` 1,00, `rate` 1,00, `speedF` 0 (25→50).
  - NATIVE_ONLY: `ELIGIBLE` y `SUPPRESSION_APPLIED`, sigue en ATTACK 2. Contra el gemelo sin POST05, solo difieren los 3 campos.
  - EXPANSION_POSSIBLE o UNKNOWN: vanilla `E_OC2_FRAME_EARLY`.
- **Arranque y fin de clip:** cubiertos los límites ±1,5 y ±1,6, fin de clip, `rate` 2 en `frame` 1, potencia 3/6 con la regla nativa y la secuencia 0→25→50→75→100 con latch.
- **Gemelos con CP21 real:** 7280 gemelos; **6880 ticks elegibles idénticos** al gemelo con la misma vida perdida sin golpe.
  - 200 de ellos son nuevos en 0.5.3 (`frame` 1 a x1,15, Black base y Red nativo) y los 200 son idénticos.
  - 240 ticks no elegibles difieren: arranque y `frame` 1 con x2 pendiente.
- **Labs** (MSVC = g++ con ASAN y UBSAN): 1660 / 29558 / 12826 / 556878 / 36933 / 55987 / 21272, con 0 fallos.

## Fase IV: otras rutas (auditoría breve) [S][R]
- **Espadazos que van a BIG_DAMAGE en `damage_check`:**
  - 4.º corte seguido (`getCutCount() >= 4`);
  - giratorios (6/7), salto, Mortal Draw y Twirl (5);
  - `AtSpl == 1`.
- **Tratamiento:** esas rutas llaman a `offTgSph()` y entran en BIG_DAMAGE (derribo), así que restaurar 3 campos no las deshace con seguridad. Quedan vanilla.
- **Evidencia:** en los dos logs, todos los BIG_DAMAGE se produjeron con postura 100 [R]. No hay ningún caso por debajo de 100 que justifique tocarlas.
- **Fuera de alcance:** bombas, bola, flechas, bumerán, escudo, letal y Finish siguen vanilla.

## Límites que siguen
1. **Con Expansion cargado** se siguen tambaleando:
   - el tick exacto de arranque;
   - el `frame` 1 de un golpe que puede llevar x2 (Red de reacción o aleatorio, Black en furia);
   - el final del clip.
   Son 1–2 ticks por golpe.
2. **Fuera de ataque** (FIND, WALK…), **en latch 100**, con **BIG_DAMAGE** y con **golpe letal**: vanilla por diseño. POST06 no existe.
3. **Validez de la señal:** solo vale para Expansion 0.17.0, que exige el servicio de EVF. Una versión futura que no lo importe invalidaría NATIVE_ONLY; habría que revisarlo.
