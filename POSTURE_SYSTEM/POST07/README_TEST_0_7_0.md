# Enemy Posture System 0.7.0 (POST07): prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. Compila con MSVC y supera laboratorios, mutaciones y auditorías del CI, pero nadie lo ha cargado todavía en el juego.

**Alineación visual:** `LAYOUT_PARTIAL` hasta que haya capturas tuyas.

## Instalación (con el juego cerrado)

- **Descarga:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41392661597/artifacts/13118435513
- **Instala solo** `POSTURE_POST07_0_HUD_PRIVATE_TEST_windows-amd64_f0e92c9f1d74.dusk`:
  - 56686 bytes;
  - SHA-256 `070533d756f1329db3e48a47c00e0245deee08fff7fc0243a647bcd7ead23afd`;
  - el artefacto caduca el 2026-12-02 (05:14 UTC).
- **Mismo ID que 0.6.1** (`dev.posture.post05_selective_reactions`): retira el 0.6.1. **Nunca los dos a la vez.**
- **En el menú de mods** aparece como "Enemy Posture System PRIVATE TEST".
- **Rollback a 0.6.1:** cierra el juego, borra el 0.7.0 y copia `POSTURE_POST06_1_REWORK_PRIVATE_TEST_windows-amd64_5037d3f311c3.dusk`:
  - 44011 bytes;
  - SHA-256 `408b0c32679b1b930658e79e5f72ae123a4cf49bd382d98d2c549bb0285c030a`;
  - artefacto 13115359099 del run 41386845338.

  No hay que tocar las partidas.

## Qué deberías ver

1. **Debajo de la barra de vida** de Enemy Health Bars aparece una barra fina, oscura, con puntas afiladas y borde bronce. Es la postura de **ese** Bokoblin.
   - **Sin EHB:** aparece en el mismo sitio, justo encima de la cabeza.
2. **Con postura 0** no se ve. Al primer espadazo aparece.
3. **El relleno crece desde el centro hacia los dos extremos a la vez.** Cambia de color:
   - oro (poca postura);
   - ámbar;
   - naranja;
   - rojo (cerca de 100).
4. **Cada golpe** hace un pequeño destello en los extremos.
5. **Al recuperarse**, el relleno se retrae hacia el centro, con los extremos pálidos.
6. **Al llegar a 100 (ruptura):**
   - un único pulso de brasa sale de la barra;
   - la barra queda roja y respira mientras dura el castigo, la caída y el suelo;
   - en el suelo (ventana de Finish) respira más rápido; al levantarse se atenúa.
   - **No vuelve a pulsar** por el escudo ni por más golpes.
7. **Tras levantarse:** se vacía hacia el centro (rearme a 0) y desaparece.
   - Si el castigo acaba de pie (aturdimiento perdido), se retrae solo hasta la mitad (50).
8. **Al morir** el Bokoblin, su barra desaparece en el acto.
9. **Sin números ni texto.** Como mucho se pintan 16 barras a la vez (las más cercanas).
10. **Combate igual que en 0.6.1.** Una corrección: si Expansion hace gritar a un Blue justo al levantarse, la postura ahora vuelve a 0 (antes se quedaba en 50).

## Fase A: POST07 + Zora Swim (5 min)

1. **Log de arranque:**
   - `POST06_INIT version=0.7.0 … hud=POST07 rearm_redirected=FIX_REARM50`;
   - `POST07_INIT version=0.7.0 hud=ON hooks=…=MOD_OK … interp=PRESENT|ABSENT`;
   - `POST03_TARGET … inline_sites_flag=0`.
2. **Blue o Red nativo:** 3 espadazos. La barra crece desde el centro: oro, luego ámbar, luego naranja. No se tambalea.
   - **Captura 1:** barra al 75 %.
3. **4.º espadazo:** ruptura. Un pulso y la barra queda roja (`POST06_EVENT … phase=TRACKING>STAGGER_OPEN`).
   - **Captura 2:** justo tras el pulso.
4. **Escudo y luego Helm (o espadazo decisivo):** caída nativa. La barra sigue roja y no se vacía en el suelo.
   - **Captura 3:** en el suelo.
5. **Deja que se levante:** la barra se vacía hacia el centro y desaparece (`why=REARM_AFTER_NATIVE_GET_UP_0` o `…_REDIRECTED_0`).
6. **Muerte (Finish):** la barra desaparece en el acto.

## Fase B: los 8 mods (7 min)

- **EHB presente:** la barra queda justo debajo de la de vida, sin tocarla, y las dos se mueven juntas.
  - **Captura 4:** primer plano de un Bokoblin con las dos barras.
- **Varios Bokoblins a la vez:** cada uno con su barra; los valores no se mezclan.
- **Distancia y oclusión:** se desvanece a lo lejos y se oculta tras paredes, igual que la de vida.
- **Blue en grupo con Expansion:** ruptura, caída y levantamiento con grito. En el log debe aparecer `why=REARM_AFTER_NATIVE_GET_UP_REDIRECTED_0 … mode=7`, no `TECHNICAL_ABORT_ON_FEET_50`.
- **Pausa y menú:** la barra se oculta y al volver sigue donde estaba.
- **Rendimiento:** FPS similares a 0.6.1 con 6 u 8 Bokoblins en pantalla.

## STOP inmediato

Cierra el juego, vuelve a 0.6.1 y mándame el log y las capturas si ves algo de esto:

- **Estabilidad:** crash al entrar en una zona, al abrir el menú o al cambiar de sala.
- **Log de inicio:** `POST07_INIT hud=OFF_HOOK_FAILED` o `POST07_HUD_DISABLED`.
- **Barra mal pintada:**
  - barra que se queda en pantalla sin Bokoblin (fantasma);
  - barra en otro Bokoblin;
  - barra que pisa la de vida;
  - barra que parpadea fuerte.
- **Pulso:** pulsos repetidos en la misma ruptura.
- **Combate distinto de 0.6.1:** tambaleos, doble daño, Finish imposible o Bokoblin congelado.
- **Contadores de error:** `VERIFY_FAILED`, `RECHECK_FAILED` o `failed=` creciendo en `POST06_SUMMARY`.
- **Rendimiento:** caída fuerte de FPS.

## Qué mandar

- El log de cada fase.
- Las capturas 1 a 4.
- Para cada caso raro: qué variante era, en qué fase estaba y qué pasó.
