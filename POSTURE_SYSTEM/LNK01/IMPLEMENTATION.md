# LNK01 0.9.0: postura de Link, barra inferior y prompts de acción ocultos

| Campo | Valor |
|---|---|
| Base | POST08 FIX02 0.8.2, commit compilado `62533c27730de14abcf65bf8d6d3ed409db2503f` |
| Rama fuente | `feature/posture-lnk01-player-hud-block-posture` |
| Commit de código | `10dff331f2013965cee41e4890a8585489478a92` |
| Rama CI | `ci/posture-lnk01-player-hud-block-posture` (desde `4bd5553`, la base CI exacta de 0.8.2) |
| ID del mod | `dev.posture.post05_selective_reactions` (sin cambios) |
| Versión | 0.9.0 |

**Etiquetas de evidencia:**
- **[S]** fuente del host `40457c6`;
- **[B]** EXE oficial 2.0.3 (SHA-256 `ffa99203…0049`) o la DLL compilada;
- **[L]** laboratorio (`LAB_MODEL_ONLY`);
- **[H]** humano (pendiente).

## 1. Qué hay en el HUD inferior y qué se oculta

### 1.1 Las dos familias de iconos de botón del HUD de juego [S]

| Familia | Clase / objeto | Pantalla (BLO) | Anclaje | ¿En la franja inferior? |
|---|---|---|---|---|
| Clúster principal A/B/X/Y/Z/R con objetos | `dMeter2Draw_c` (`mpButtonParent` = `cont_n`, `mpButtonA/B/XY`, `mpTextA/B/XY`…) | `zelda_game_image.blo` | **arriba a la derecha**: `dAnchorHudScale(mpButtonParent, HudCorner::TopRight)` (`d_meter2_draw.cpp:652-706`) | No |
| **Prompts de acción con énfasis** | **`dMeterButton_c`** = `dMeter2_c::mpEmpButton` | `zelda_game_image_button_info.blo` (`info_n`…) | **centro inferior**: `mParentCenterX = FB_WIDTH_BASE/2 − centro` (`d_meter_button.cpp:1105`), `mEmpButtonPosY = 175` sobre 448 (`d_meter_HIO.cpp:739`), es decir, ~89 % de la altura | **Sí** |

**Por qué el centro inferior es `dMeterButton_c`:**
- Lo crea `dMeter2_c::check2DContents()` en `_execute → move2DContents` cuando una acción tiene énfasis o hay un mensaje flotante.
- Lo encola `dMeter2_c::_draw` con `set2DOpaTop`.
- Lo destruyen `check2DContents`, `emphasisButtonDelete` (menús y mensajes) y `_delete`.

El resto de esquinas tampoco está en la franja:
- abajo a la izquierda, la cruz de objetos (`mpButtonCrossParent`) y el minimapa;
- abajo a la derecha, rupias y llaves;
- arriba a la izquierda, corazones y magia.

### 1.2 Inventario de `dMeterButton_c::draw` [S] (`d_meter_button.cpp:273-487`) y offsets Win64 [B]

| Paso del draw nativo | Miembro (Win64) | Qué pinta | LNK01 |
|---|---|---|---|
| `mpButtonScreen->draw` | `+0x10` (`J2DScreen`, `zelda_game_image_button_info.blo`) | Iconos `abtn_n`, `bbtn_n`, `rbtn`, `zbtn`/`z_btnl`, 3D, C, S, X, Y, Nun/Remo/AR/3DB/NURE/Reel/AB/Tate/NunZ/NunC/Bin, textos de acción `info_ar0-9`/`fnfo_ar0-9`, flechas `yaji_*`, Midna, objeto de pesca, todo bajo `info_n` | **OCULTO**: `hide()` en la raíz (`mVisible=false`) |
| `field_0x00c->draw` | `+0x18` | Siempre `NULL` (solo se asigna `NULL`) | — |
| `mpScreen->draw` (si `isFloatingMessageWakuVisible`) | `+0x20` | Marco del mensaje flotante | **SE CONSERVA** |
| `mpTextScreen->draw` + `drawOutFont` | `+0x28` | Texto del mensaje flotante (con sus glifos en línea) | **SE CONSERVA** |
| `drawPikari(vtx…)` por slot `field_0x4be[i]` | `+0x5d2` (`u8[2]`) | Brillos de énfasis, parpadeo de A y repetición de A en la posición del icono | **SUPRIMIDO**: el slot pasa a `BUTTON_NONE` solo durante este draw y se restaura en el POST |

**Ocultar la raíz basta para todo el subárbol** [S]:
- `J2DPane::draw` hace `param_4 = param_4 && mVisible` y pasa `param_4` a todos los hijos (`J2DPane.cpp:249-345`). Una raíz oculta no pinta ningún hijo.
- Ningún código nativo llama a `mpButtonScreen->show()`; solo muestra y oculta **subpaneles** (`d_meter_button.cpp:176-248, 1114-1170`).
- Una vez oculta, sigue oculta hasta que el objeto se destruye. El objeto nuevo se vuelve a ocultar en el POST de `_execute` del mismo tick en que se crea, antes de cualquier draw.

**Offsets medidos en el EXE oficial** [B], con `static_assert` en `mod.cpp`:

| Offset | Función del EXE | Instrucción |
|---|---|---|
| `dMeter2_c::mpMeterDraw` = `0x1e0`, `mpEmpButton` = `0x1f8` | `dMeter2_c::_draw` 0x140a25270 | `mov rcx,[rbx+0x1e0]` y `mov rcx,[rbx+0x1f8]` → `set2DOpaTop` |
| `dMeterButton_c::mpButtonScreen` = `0x10`, `mpScreen` = `0x20` | `draw` 0x140a01e60 y `_delete` 0x1409ff3c0 | `[rbx+0x10/0x18/0x20/0x28]` → `J2DScreen::draw` |
| `dMeterButton_c::field_0x4be` = `0x5d2` | `draw` | `cmp byte [rbx+rdi+0x5d2], 0/1` |
| `dMeter2Draw_c::mpScreen` = `0x80` | `draw` 0x140a12de0 | — |
| `J2DPane::mVisible` = `0xb0` | `draw` 0x141663180 | `cmp byte [rcx+0xb0],0` |

### 1.3 Tabla `TAG / FUNCIÓN / QUÉ SE OCULTA / QUÉ SE CONSERVA`

| Tag / pane | Función | Se oculta | Se conserva |
|---|---|---|---|
| raíz de `zelda_game_image_button_info.blo` (`info_n` y todo su árbol) | Prompt de acción inferior | Sí (raíz) | — |
| `abtn_n`, `bbtn_n`, `rbtn`, `zbtn`/`z_btnl`, 3D, `cbtn`, `sbtn`, `xbtn`, `ybtn`, Bin y las variantes Wii | Iconos de botón | Sí (hijos de la raíz) | Su lógica (alfas, temporizadores, sonidos de aparición) |
| `info_ar*` / `fnfo_ar*` | Textos de acción («Hablar», «Abrir», «Atacar»…) | Sí | `setString` y el estado de `mButtonText` |
| `yaji_*` | Flechas de stick/C | Sí | — |
| `midona`, objeto de pesca | Icono de Midna y de la caña | Sí | — |
| brillos `drawPikari` del prompt | Énfasis, parpadeo y repetición | Sí (máscara durante su draw) | Los slots (restaurados al valor exacto) |
| `zelda_message_window_new.blo` (`n_all`, `mg_null`) | Marco del mensaje flotante | No | Sí |
| `zelda_message_window_text.blo` (`mg_e4lin`…) | Texto del mensaje flotante | No | Sí |
| `zelda_game_image.blo` (corazones, magia, rupias, llaves, clúster arriba a la derecha, cruz) | HUD principal | No | Sí |
| `dMeterButton_c` de `d_a_skip_2D` (aviso de saltar cinemática) | Otro objeto de la misma clase | No (filtro `mpEmpButton == self`) | Sí |
| minimapa, barras EHB, barras POST07, diálogos, menús | — | No | Sí |

**Lógica intacta:**
- `dMeter2_c::_execute`, `dMeterButton_c::_execute` y `check2DContents` no se interceptan ni se cancelan;
- tampoco se tocan `setString`, Do/A status, flags, entradas, temporizadores ni sonidos.
- La máscara de slots solo existe entre el PRE y el POST del propio `draw`, de modo que `_execute` nunca ve el valor enmascarado.
- Efecto secundario conocido: el sonido de aviso de parpadeo (`Z2SE_SY_HINT_BUTTON_BLINK`, `d_meter_button.cpp:426`) va dentro de la rama del brillo y tampoco suena. Es audio de la indicación, no lógica.

## 2. Barra de Link

**Geometría** (unidades orto del pintor; `setOrtho(minX, minY, ancho, alto)` del viewport lógico actual):
- **Centro:** `(minX + 0,50·ancho, minY + 0,87·alto)`.
- **Ancho:** 32 % del ancho útil 16:9 (`min(ancho, alto·16/9)`); en ultrawide queda dentro del 16:9 centrado.
- **Alturas:** relleno de 11 px y marco de 16 px de referencia a 1080 (`u = alto/1080`).
- **A 1920×1080:** **614 × 16 px**, frente a ~67 px de una barra enemiga POST07 (unas 9 veces más ancha). Valores registrados en `LNK01_HUD_LAYOUT`.

**Diseño:** propio, sin assets de terceros.
- placa oscura translúcida con extremos difuminados;
- marco bronce con remates escalonados y muesca central;
- pista oscura;
- relleno simétrico del centro a ambos extremos, con la rampa de POST07: oro → ámbar → naranja → rojo;
- brillo superior y bordes de avance;
- un pulso de brasa al llegar a 100 (sin efecto de juego).

**Animación** (`lnk01::PlayerHud`, en ticks de simulación):
- subida rápida y retirada continua;
- a 0, la barra sigue visible **0,7 s** (21 ticks) y se funde en ~0,3 s;
- se oculta al instante si Link no es humano (lobo);
- se reinicia sin fantasma con una Link nueva.

**Dibujo:**
- Mismo paquete 2D XLU de POST07 (un solo `queue_after_hud` por pasada). Se encola si hay barras enemigas **o** la de Link es visible (`lnk01::packet_needed`).
- Se pinta **la última**, encima de las barras enemigas, a partir de la copia por valor `hg.player`.
- Orden de listas [S] (`m_Do_graphic.cpp:2814-2816`): `draw2DOpa` → `draw2DOpaTop` (HUD nativo y prompt) → `draw2DXlu` (este paquete). La ocultación de los prompts no depende de ese orden, porque se ocultan en origen.

**Cuándo se oculta:** las mismas condiciones del HUD nativo y de POST07.
- vida 0, pausa, evento o cinemática;
- `mStatus` del medidor oculto, ventana de menú abierta o vista ausente;
- *minimal HUD* (el medidor no se encola);
- además, Link no humana.

## 3. Postura de Link: fuente, deduplicación y parry

**Fuente:** el veredicto POST08 de la **misma** llamada de `damage_check`, ya calculado (`post08_judge`) y ya comprometido (`post08_step`).
- Sin hook nuevo sobre Link ni lectura nueva del colisionador.
- Solo cuenta con contacto **fresco** (`ArmTrack` de FIX02) de un E_OC/E_OC2 admitido.
- Estado de Link **durante la pasada** (`LinkTrack`, instantánea de `mod_update`).

| Veredicto POST08 | LNK01 | Motivo |
|---|---|---|
| `NORMAL_GUARD`, `MISSED_EARLY`, `LATCHED`, `FURY_CHIP_POSSIBLE` | `CONFIRMED_NATIVE_BLOCK` (+20) si hay `AtShieldHit` nativo, Link humana y viva con el mismo id, sin evento, token válido, ataque no desviado y sin crédito previo de ese token | El motor bloqueó el golpe con el escudo y no fue un parry. Black en furia: el chip de Expansion sigue intacto; el bloqueo cuenta como ordinario |
| `CONFIRMED`, `DUPLICATE` | `REJECTED_PARRY` (+0; LNK03 decidirá el coste) | Parry POST08 (+40 para el enemigo) |
| `STALE_CONTACT` | `REJECTED_STALE` | Registro At de una pasada no armada |
| `NOT_BLOCKED`, `NOT_ATTACKING` | `REJECTED_NONBLOCK` | Daño directo (LNK02) o pasada de rebote |
| `MISSED_LATE` | `DUPLICATE` | El golpe ya se había resuelto |
| `EVENT_RUNNING` | `REJECTED_EVENT` | — |
| `UNTRACKED`, `LINK_INVALID`, `NO_PASS_SNAPSHOT` | `REJECTED_UNTRACKED` | Identidad no demostrada |

**Deduplicación:**
- Un registro por slot del ledger (64): `id`, `generación`, token acreditado y token desviado.
- Una identidad nueva no hereda nada.
- Dos esferas, callbacks repetidos, pasadas de rebote o un parry previo en el mismo ataque no suman.

**Regeneración** (`lnk01::Posture::tick`, una vez por `mod_update`):
- Retraso de 30 ticks tras el último bloqueo, luego 10 pts/s: 1 pt cada 3 ticks, en milésimas enteras con resto exacto.
- Se congela sin Link, con vida 0, en pausa, en evento o con menú. No hay ráfaga tras una pausa larga.
- Máximo 100 y mínimo exactamente 0.
- Link nueva o ausente (cambio de sala, muerte y continuación) ⇒ reinicio determinista a 0.

**Ruptura de guardia:**
- A 100 **no** hay ruptura propia, ni daño, ni penalización.
- El contador nativo `field_0x2fd5` (cada 4.º bloqueo consecutivo → `PROC_GUARD_BREAK`, `d_a_alink_guard.inc:244-246`) **no se lee ni se escribe**.
- Solo se miden las entradas de Link en `GUARD_SLIP` y `GUARD_BREAK` (`LNK01_GUARD`, `native_guard_*` en el resumen).
- **Limitación conocida:** la barra puede estar a 100 sin que el juego rompa la guardia, y el juego puede romperla con la barra por debajo de 100. La integración llegará en LNK05.

## 4. Escrituras, hooks e imports

| Escritura | Propiedad | Alcance |
|---|---|---|
| `J2DPane::mVisible = false` (inline `hide()`) en `mpEmpButton->mpButtonScreen` | `HUD_VISUAL_ONLY` | Solo el prompt vivo validado: vptr `J2DScreen` igual al de `mpMeterDraw->mpScreen` y al del marco del propio prompt, punteros alineados a 8. Si no, `LAYOUT_REFUSED` y no se escribe nada |
| `field_0x4be[0..1]` del mismo prompt | `HUD_VISUAL_ONLY`, transitoria | PRE del draw → `BUTTON_NONE`; POST → valor original. El POST se instala antes que el PRE |
| Contador privado `lg.posture` | Memoria del mod | — |

**Lo que no se escribe:** ningún actor, Link, vida, `mProcID`, `AttackInfo`, `at_spl`, `field_0x2fd5`, alfas globales, `g_drawHIO`, `mpScreen` del HUD principal ni flags de pantalla.

**Hooks:**
- Hook nuevo: `dMeterButton_c::draw`, **virtual** (PMF a un thunk vcall local de slot 0; el host lo resuelve por nombre, `src/dusk/mods/svc/hook.cpp`). PRE y POST siempre `HOOK_CONTINUE`.
- Total: 6 `HOOK_MEM`.

**Imports:** sin imports nuevos ni eliminados del juego ni del CRT. El pin PE de 0.8.2 coincide con el link MSVC del run 41495366683; solo cambia `HOOK_MEM` de 5 a 6.

**Desensamblado de la DLL descargada:** las únicas escrituras nuevas en memoria del juego son `mov byte [rsi+0xb0],0` (`action_ui_step`), `mov word [rbx+0x5d2],0x1616` (PRE) y la restauración `[rdx+0x5d2]/[rdx+0x5d3]` (POST).

**Fallo seguro:**
- Si fallan los hooks del medidor: `button_hud=VISIBLE_HOOKS_FAILED` (los prompts siguen como en 0.8.2).
- Si falla el hook del draw: la raíz sigue oculta, pero puede verse algún brillo (`sparkle_mask=OFF` en `LNK01_INIT`).
- Una excepción en la parte UI la desactiva sin tocar POST08.

**Retirada:** el estado oculto solo vive en el objeto del HUD en RAM. No hay nada persistente. Quitar el `.dusk` y reiniciar Dusklight devuelve los iconos; no se promete descarga en caliente.

## 5. Telemetría (sin direcciones ni rutas)

- **Arranque:**
  - `LNK01_INIT`: política, geometría, resultado de los hooks y `resolve(dMeterButton_c::draw)`;
  - `LNK01_HUD_LAYOUT`: hasta 6 líneas, al cambiar el viewport.
- **Eventos:**
  - `LNK01_ACTION_UI event=PANE_RESOLVED|VISUAL_HIDDEN|LAYOUT_REFUSED|HUD_RECREATED`: hasta 40;
  - `LNK01_BLOCK`: hasta 200, con veredicto, `post08`, `attacker_id`, `generation`, token, tipo, tick, antes/después, `contact_fresh` y `link_state`;
  - `LNK01_REGEN event=START|ZERO|PAUSED`: hasta 60;
  - `LNK01_GUARD event=NATIVE_GUARD_SLIP|NATIVE_GUARD_BREAK`: hasta 40.
- **Resúmenes:** `LNK01_SUMMARY part=1/2` (postura, rechazos, rupturas nativas, `actor_writes=0`, `link_writes=0`, `invariants`) y `part=2/2` (prompts ocultos, máscaras, frames de la barra).
- POST03–POST08 conservan sus líneas y sus versiones de módulo (POST08 `v=0.8.2`, POST07 `v=0.7.0`), comparables con 0.8.2.

## 6. Laboratorio, mutaciones y auditorías

- **`lnk_lab`**: 528 comprobaciones, familias L01–L19, `LAB_MODEL_ONLY`.
  - Los bloqueos salen de una simulación por ticks con el `Parry`/`ArmTrack`/`LinkTrack` **reales** y la semántica de registro At del host.
  - Los prompts se prueban sobre un modelo de `dMeterButton_c` con 720 ticks, frames de presentación, recreaciones, brillos y mensajes flotantes.
  - Renders de referencia: `--render` a 1080p, 720p y 2560×1080.
- **Laboratorios heredados:** los 11 conservan los mismos conteos que 0.8.2.
- **Mutaciones:** 168/168 detectadas (130 heredadas + 38 de LNK01: 22 de lógica y 16 negativas de la auditoría de fuente).
- **Auditoría PE:**
  - 6 `HOOK_MEM`;
  - réplica de `vcall_slot_offset` del host (slot 0 exigido);
  - 3 negativos nuevos: N11 hook renombrado, N12 vtable alterada y N13 thunk alterado (14 en total).

**CI:** run 41495366683, MSVC 14.51. Compilación e `independent-download` correctas; 12 laboratorios sin fallos; 168/168 mutaciones; `PE_AUDIT_PASS` con el pin; 14/14 negativos rechazados. Evidencia en `EVIDENCE/ci_41495366683/` y datos en `RESULTS.json`.
