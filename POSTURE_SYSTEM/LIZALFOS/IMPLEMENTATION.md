# Light Fades Twice 0.12.0: Lizalfos Duelist

Parte de 0.11.12 (fuente compilada `2a57ebeeafe6ec48ee5b63b5f614b6a0fff95b5e`). El mod ID no cambia: `dev.posture.post05_selective_reactions`. Estado de runtime: **HUMAN_RUNTIME_PENDING**. Lo aquí escrito procede de la fuente, del desensamblado, de laboratorios y del CI; nadie lo ha ejecutado aún en el juego.

## 1. Identidad del Lizalfos
Se usa una clasificación positiva en `liz::classify`. Se admite un `e_dn_class` con perfil `fpcNm_E_DN_e` (435), salvo estas exclusiones:

| Exclusión | Evidencia nativa |
|---|---|
| `arg1 == 1` | `useHeapInit` carga la calavera (recurso 40), y también dependen de `arg1 == 1` el tiempo de alma «fuerte», el salto de precipicio y la patada de bomba. Se interpreta como Dynalfos. |
| `skull_model != NULL` | la misma variante, comprobada aparte |
| `arg0` 13..16 o `ACTION_REG` | carrera guionizada de `create`, con `status = 1` |
| `status != 0` | Execute no corre |
| `D_MN07` sala 8 | sala especial anotada en la fuente nativa |

Lo no identificado conserva el comportamiento original y se registra (`LIZ_POSTURE event=EXCLUDED_VANILLA`). La línea `event=ADMITTED` imprime `arg0` y `arg1`.

**Limitación:** no se han leído los datos de escena. Que `arg1 == 1` sea exactamente el Dynalfos es una inferencia de la fuente nativa. La primera partida lo confirmará con esas dos líneas.

La vida se escribe una vez, de 100/100 a 370/370, en el primer Execute de la identidad. Si hay otro valor de vida, no se toca y se registra `LIZ_CRITICAL code=1`.

## 2. Hooks y ABI
Se añaden 12 objetivos nuevos, todos PRE/POST, sin `replace`.

- **Once funciones estáticas de `d_a_e_dn.cpp`** resueltas por nombre mediante el manifiesto de símbolos del EXE 2.0.3 (registros `HOOK_NAME`): `daE_DN_Execute`, `daE_DN_Delete`, `damage_check`, `small_damage`, `big_damage`, `e_dn_fight_run`, `e_dn_attack_0`, `e_dn_attack`, `e_dn_tail_attack`, `at_hit_check` y `anm_init`. Todas figuran en el manifiesto con `code, local, display` y sin `INLINE`, `MULTI` ni `DUP`.
- **`daAlink_c::setCutType`** (POST): la señal de inicio de cada tajo de Link. Es el único objetivo nuevo sobre Link.
- **Un POST más sobre el `checkDamageAction` existente:** recibo del golpe directo y rearme rápido del escudo.

Layout comprobado en compilación contra valores medidos en el EXE: `sizeof(e_dn_class) == 5872` (log `procSize`), `mode 0x6c8`, `at_sph 0x1318`, `anm_p 0x6f0`, `anm_no 0x6f8`, `action 0x8e2`, `invulnerability_timer 0x8fc`, `mHitDirection.y 0x16a2`. Imports nuevos del juego: `setCutType` y `cCcD_ObjTg::ClrHit` (69 en total).

`ci/liz_native_audit.py` falla el build si cambia cualquiera de las líneas nativas de las que depende la lógica.

Si falta cualquier hook, `lz.enabled = false`: el E_DN queda original y el resto del mod no se altera.

## 3. La cancelación del doble
`e_dn_attack` es la única función que cancela por escudo: `setPlaySpeed(0); action = FIGHT_RUN; mode = 0`, cuando `at_hit_check()` devuelve a Link y Link guarda. El desensamblado confirma que `at_hit_check` solo se llama desde `e_dn_attack` y `e_dn_attack_0`, y que `e_dn_tail_attack` no la llama. En `e_dn_attack_0` el resultado solo produce vibración.

El POST de `at_hit_check` devuelve NULL **solo con `action == ACTION_ATTACK`**. Así la rama de cancelación nunca corre y no hay nada que deshacer: ni estado, ni velocidad, ni repetición de golpe. Colisión, marca de escudo, sonido, chispa, reacción de Link y daño legítimo no se tocan.

Control negativo del laboratorio: sin este hook, la transcripción nativa pierde D2 en cada doble bloqueado, como observó el usuario.

## 4. Combos
- **Selección:** cuando la decisión nativa de `e_dn_fight_run` elige atacar se hace un único sorteo sin sesgo (rechazo sobre generador propio; `cM_rnd` nunca se consume).
- **Composición:** P1 N-D-C (3/4), P2 N-N-N-D-N-C (6/7), P3 D-N-D-N-N-D (6/9), P4 C-C-N-D-C (5/6).
- **Velocidades por acción:** se escriben en el PRE de `anm_init`, así que el primer `play` ya va a la velocidad correcta: N 1,25; D 1,10; C lenta 1,10; C rápida 1,20.
- **Ritmo:** el intervalo se mide de apertura a apertura de AT. Tras cerrarse la última ventana de una acción, la siguiente arranca cuando corresponde, entrando en un frame nativo intermedio del clip. Nunca se salta una ventana AT y siempre quedan al menos 8 frames de preparación. La primera acción usa su preparación completa y la última su recuperación completa. Todos los intervalos entre acciones quedan a ±1 tick de la ficha (`LIZ_RHYTHM` en el log del laboratorio).

**Decisión de diseño a revisar en juego:** para llegar a intervalos como 0,58 s, las acciones intermedias recortan su preparación (se entra por el frame 4–19) y su recuperación. Son frames nativos sin assets nuevos, pero cambian cómo se telegrafía el golpe. Es la parte con más necesidad de validación visual.

**Desviación física registrada:** D1→D2 es 0,367 s de apertura a apertura (los 0,10–0,13 s grabados son imposibles con 12 frames de clip a x1,10). Ver `AUDIO_RHYTHM_ANALYSIS.md`.

**Otros detalles:**
- Sonidos: la velocidad fraccionaria saltaría comparaciones `frame == n` (por ejemplo, el frame 10 del doble a x1,10). Una fase subframe determinista garantiza que se alcanzan todos.
- Frame residual: en modo 0, `e_dn_attack` lee el frame del clip anterior antes de `anm_init`, lo que abriría una ventana AT falsa. El PRE lo pone a 0.
- Embestida: el paso nativo es por tick y con más velocidad hay menos ticks; cada tick añade `(r-1)*paso` para conservar el total.
- Durante los huecos entre acciones se omite `e_dn_fight_run`, de modo que ninguna decisión nativa rompe el combo.
- Tras cada episodio, `timer[2]` queda en 45..75 ticks: Link siempre tiene una apertura.

Causas de fin registradas: `COMPLETED`, `POSTURE_100_BREAK`, `DEATH`, `NATIVE_PRIORITY`, `ADAPTIVE_DEFENSE_AT_SAFE_BOUNDARY`, `SCENE_OR_DELETE`, `EVENT`, `WATCHDOG`.

## 5. Parry de Link
Cada ventana AT abre un serial de impacto propio, de modo que D1 y D2 son dos seriales. La verdad del contacto la da el motor: `AtHit` sobre un `mTgCyls` de Link + `AtShieldHit`.

El parry exige el `LinkTrack` de la pasada y la procedencia de CP04 (`cp04_guard_pass`), con la misma ventana `[-1,+7]` y 9 ticks que los Bokoblins. Un veredicto por impacto: +22 una vez; R mantenido es bloqueo; R+B fuera de ventana es bloqueo. Un parry que no rompe no cambia nada del combo.

**Rearme:** la cadena de CP04 solo admite otro R+B tras 12 ticks de deslizamiento y el clip da 6..11. Solo dentro de la pareja D1→D2 de ese mismo actor al que Link acaba de hacer parry, el rearme se admite a partir de 4 ticks con el mismo `procGuardAttackInit`. Sigue exigiendo una pulsación física nueva. Para el resto de enemigos, CP04 sigue igual.

La postura propia de Link al bloquear o recibir golpes del Lizalfos usa las filas existentes por AtAtp: ATP1 20/30 y ATP2 25/35. **Este valor no estaba en el encargo**; queda como `[BALANCE_PROVISIONAL]`.

## 6. Postura, ruptura y anti-tambaleo
- Capacidad 100; +15 espada que conecta con daño real; +22 parry de Link; +30 Iron Ball; +5 bloqueo real de su escudo. Las resoluciones son excluyentes.
- Regeneración 10/7/4/2/1 por franja exacta de vida; 60 ticks elegibles; acumulador entero sin deriva. **HP: 0 regeneración.**
- Espada con postura <100: se omite `small_damage` y `big_damage` y se repara el 1000 de invulnerabilidad. HP, marca de golpe e invulnerabilidad corta nativa se conservan.
- **Excepciones nativas sin suprimir:** muerte, Iron Ball, bombas, flechas, gancho, bumerán, patada y mordisco de lobo, a caballo, guion. Una Iron Ball no letal conserva su derribo nativo, así que puede abrir el remate antes de 100; lo mismo ocurre con otros derribos nativos.
- Shield Attack de Link sobre el cuerpo: se limpia su marca Tg en el PRE de `damage_check`, porque si no su ruta nativa (`DRAWBACK`) cortaría el combo.
- **Ruptura a 100:** se usa el `big_damage` original con `mHitDirection` hacia Link y se entra en `e_dn_damage` real: `onDownFlg` da el remate nativo; `checkCutDownHitFlg` mata de verdad; sin remate se levanta. La postura vuelve a 0 solo cuando el actor sale de `ACTION_DAMAGE`.
- Solo se rompe desde estados de combate: agua, caídas, mordisco o saltos nunca se sobrescriben; la ruptura queda pendiente hasta que terminan.

## 7. Defensa adaptativa
Un tajo cuenta para un actor solo si está dirigido a él (±45°) y a menos de 320 unidades. Cada tajo genera como máximo un sorteo.

| Nivel | Prob. de intentar parry | Condición |
|---|---|---|
| A | 12% | estado habitual |
| B | 35% | 3 tajos distintos en 75 ticks |
| C | 45% | 6 tajos en 150 ticks y al menos 2 impactos propios que Link no defendió desde su última defensa |

- Subida inmediata. Bajada de un nivel tras 45 ticks sin la condición.
- Un parry de Link baja un nivel y borra la memoria; alejarse a más de 600 durante 30 ticks también la borra.
- La vida del Lizalfos no entra en el cálculo.

Un intento entra en la guardia nativa con los mismos campos que su entrada original. El parry exige contacto real aceptado de `tate_sph` (`unk_timer_2` 0→10) con la espada de Link, de frente (±67,5°), dentro de 5 ticks desde la primera pasada físicamente posible. Si no se cumple, es un bloqueo normal: +5.

Un parry real da +25 a Link, sin +5 ni daño, y 120 ticks de enfriamiento. Link recibe la reacción nativa de espada desviada: `tate_sph` es Tg de escudo, así que el motor marca `AtShieldHit` y Link ejecuta `changeCutReverseProc`. No hay efectos nuevos.

**Iniciativa:** tras un parry, la guardia sale por su ruta nativa (modo 8) y se sortea: 40% golpe N corto, 40% uno de los cuatro combos, 20% reposicionarse. Esto solo adelanta `timer[2]`: la decisión nativa aún puede rechazar por distancia u orientación, y Link puede responder.

**Guardia voluntaria dentro de un combo:** solo en una frontera segura (AT cerrada, fuera de la pareja), con nivel ≥B y una vez por episodio. P1 nunca; P2 en cualquier frontera; P3 desde su mitad; P4 solo tras sus dos colas iniciales. La causa queda registrada.

Si la postura de Link llega a 100 durante su ataque: `lnk05_request` con la puerta nativa de orígenes seguros, reintentada durante 90 ticks mientras siga saturada. Nunca se fuerza un estado; si no aparece un origen seguro, la postura queda en 100 hasta su siguiente impacto.

## 8. Colisión y cobertura
No se añadió reconstrucción de poses. A x1,25 como máximo y con radios 55/88/77, la separación entre muestras queda por debajo del alcance combinado salvo trayectorias de más de unas 110 unidades por frame, algo que no se ha medido. Evita además otro escritor sobre J3D.

A cambio se mide cada tick armado: si la distancia entre centros supera `2*(r+30)`, se registra `LIZ_CRITICAL event=AT_SAMPLE_GAP`, y `LIZ_SWING` imprime el mayor salto por ventana. **Si la prueba humana muestra golpes atravesados, este es el primer dato a mirar.**

## 9. Coexistencia
- Estado por identidad en 16 slots; excluidos también ocupan slot. Con más de 16 E_DN, los sobrantes quedan originales y contados.
- Liberación en `daE_DN_Delete`, con cambio de escena y reciclado de dirección; ningún puntero sobrevive.
- HUD: misma barra 0..100, en los slots altos del HUD; un Bokoblin con ese slot tiene preferencia y el Lizalfos queda sin barra, con contador.
- Coste sintético de la lógica nueva (no son FPS): `run-lab`/`liz-bench` en la evidencia del CI.

Las rutas E_OC no llevan ningún hook de este módulo. `ci/liz_audit.py` exige que los 41 archivos de producción de 0.11.12 se reproduzcan byte a byte con un parche inverso contado de 10 bloques.

## 10. Otros mods de la partida (log de referencia de 0.11.12)
- Enemy Health Multiplier incluye el perfil 435 entre los que escala, con factor x1 en la configuración de la partida. **Con un factor superior no se ha probado la interacción con 370 HP.**
- Enemy Health Bars: mostrará el máximo de 370.
- Red 330 HP. El máximo de Black depende de la configuración y no se ha verificado que supere 370. Si un Black real tiene ≤370, la relación deseada no se cumple; no se ha tocado ningún valor para compensarlo.
