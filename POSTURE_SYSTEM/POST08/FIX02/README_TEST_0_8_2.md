# Enemy Posture System 0.8.2 (POST08 FIX02): prueba humana

**Estado:** `PARTIAL_CANDIDATE / HUMAN_RUNTIME_PENDING`.

## Qué se arregló

El juego guarda en el arma del Bokoblin la marca «choqué contra el escudo» y solo la borra cuando ese arma vuelve a estar activa en un golpe. 0.8.1, al desviar el golpe (o al romper la postura por parry), cortaba el golpe **antes** de que el juego pudiera borrarla. Con esa marca vieja:
- el Bokoblin «rebotaba» al empezar cada golpe nuevo mientras guardabas (se quedaba «pensando»);
- el mod a veces contaba un parry falso.

0.8.2 deja que el juego haga su rebote normal, ignora las marcas viejas y aplaza un tick el mareo de ruptura por parry.

## Instalación (con el juego cerrado; partidas intactas; DX12)

- **Descarga:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41458296635/artifacts/13147887858 (caduca el 2026-12-02, 14:07 UTC).
- **Instala solo** `POSTURE_POST08_2_FIX02_PRIVATE_TEST_windows-amd64_62533c27730d.dusk`:
  - 70 775 bytes;
  - SHA-256 `b0e245e687b313ce07b1efaf8ba3bc3e2cfe65205ed4dba5d909dc716c7166ba`.
- **Quita el 0.8.1** (`…d70f9674e3ba.dusk`). **Una sola versión de Posture a la vez.**
- **Rollback estable:** POST07 0.7.0
  - `POSTURE_POST07_0_HUD_PRIVATE_TEST_windows-amd64_f0e92c9f1d74.dusk`;
  - SHA-256 `070533d756f1329db3e48a47c00e0245deee08fff7fc0243a647bcd7ead23afd`.

  Ojo: 0.8.1 **no** es un rollback seguro, porque tiene el atasco de IA.

## Cómo saber si un Bokoblin «se queda pensando» (sin herramientas)

**Síntomas:**
- Está cerca de ti, de frente, sin mareo, y durante **más de ~5 segundos** no completa ningún golpe.
- Empieza a levantar el arma y la baja una y otra vez.
- Se queda quieto mirando.

**No cuentan como atasco:**
- el Blue que retrocede o esquiva;
- un Bokoblin lejos o detrás de algo;
- el mareo de una ruptura;
- estar en el suelo.

Si lo ves, anota más o menos el momento, cuántos había y qué hacías justo antes (parry, guardia, espadazo a otro).

## Fase A: Posture 0.8.2 + Zora Swim

1. **Arranque:** `POST08_INIT version=0.8.2 … fix02=FRESH_ARMED_CONTACT_ONLY+NATIVE_DEFLECT…`.
2. **Un Blue solo, cinco parries** (de uno en uno, dejando que vuelva a atacar entre ellos).
   - Tras cada parry debe volver a atacarte con normalidad, también si mantienes la guardia.
   - Log: `POST08_EVENT result=CONFIRMED stage=COMMITTED_NATIVE …` y, unos segundos después, `POST08_AI_TRACE event=END verdict=NORMAL_NEXT_ATTACK_OBSERVED cause=PARRY`.
3. **Parries hasta 100:** pulso al instante y mareo de pie un tick después (`POST06_EVENT … BREAK_BY_PARRY`). Castiga (espadazo o Escudo → Helm) y Finish. Tras levantarse debe atacar otra vez.
4. **Guardia normal** frente a varios golpes: sin postura y sin atasco.

## Fase B: los 8 mods

1. **Dos Bokoblins, A → B → A con espada, sin parry**, alternando cada 1–2 s durante un minuto. Ninguno debe quedarse quieto.
2. Repite con **parry a A** mientras B ataca, y al revés.
3. **Variantes:** Blue + Red, Blue + Black, Red + Black y grupos de 3–4 (y 6–8 si puedes).
4. **Black en furia:** sin parry (`FURY_CHIP_POSSIBLE`); su chip sigue igual.
5. **Barras y combate:**
   - barras de vida (HM ×2) y de postura correctas;
   - ×1,50, Helm y Finish;
   - rearme a 50/0;
   - FPS.

## Qué mandar

- El **log completo** de cada fase. Busca y, si quieres, copia:
  - `POST08_AI_TRACE` (sobre todo `event=SUSPECTED` y `verdict=AI_STALL_STILL_SUSPECTED`);
  - `POST08_SUMMARY tag=SHUTDOWN part=4/4` (`ai_stall_suspected`, `stale_contacts_ignored`, `deflect(…)`);
  - `part=3/4` (`invariant_ok=1`).
- Si un Bokoblin se atasca, el `POST08_AI_TRACE … recent={…}` de su `actor_id` muestra sus últimos estados.

## STOP (vuelve a 0.7.0 con el juego cerrado)

- **Estabilidad:** crash.
- **IA:** un Bokoblin atascado más de ~10 s que ni un espadazo libera.
- **Parry y vida:**
  - Link pierde vida en un golpe `CONFIRMED`;
  - un parry con guardia normal;
  - +80 en un golpe o dos pulsos;
  - pérdida de vida del Bokoblin por un parry.
- **Ruptura:** sin mareo, o mareo por debajo de 100.
- **Castigo y rearme:** Helm, Finish o rearme rotos.
- **Otros:** Black en furia alterado, barras fantasma o caída fuerte de FPS.
