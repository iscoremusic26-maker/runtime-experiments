# Light Fades Twice CP06 — 0.11.11 PRIVATE TEST

`LIGHT_FADES_TWICE_CP06_0_11_11_PRIVATE_TEST_windows-amd64_0ef0ad282483.dusk` · **174626 bytes** · ID `dev.posture.post05_selective_reactions` · **0.11.11** · Windows x64 / DX12.

- SHA-256 `.dusk`: `7bcebf6ff442147d6741daf65d9b1e2128b524af8219296272ab64f236d15be3`
- SHA-256 DLL interna: `8473d76c31bb12531e52c9b207723dcdabebca25a5112c35a6f2cb72730df221`
- Fuente compilada `0ef0ad2824832c9e03d899c298b5f9a8e860d590` (rama `feature/light-fades-twice-cp06-0-11-11`, base compilada 0.11.10 `d6e4c2179c2c42a7aa807ce862290de728abb396`). Commit CI `06c64426de52fc8268e5499e1780c2ce5d4f89f7`. Este documento está en un commit documental posterior y separado.
- CI [42298979283](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42298979283): build SUCCESS, independent-download SUCCESS. Artefacto [13543119520](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42298979283/artifacts/13543119520), caduca **2026-12-06T22:02:03Z**. Descargado de nuevo en esta sesión: SHA, tamaño, DLL, `mod.json` y manifiesto coinciden.

Estado: SOURCE_IMPLEMENTED / SOURCE_AUDIT_PASS / LAB_PASS (Linux g++ y Windows MSVC) / WINDOWS_MSVC_PASS / PE_AUDIT_PASS / INDEPENDENT_DOWNLOAD_PASS. **Todo lo jugable y visual: HUMAN_RUNTIME_PENDING.** No se ejecutó el juego ni la DLL.

## 1. Ritmos (solo animación de espadazo, con propiedad verificada)

Las tasas se escriben solo con los escritores ya auditados (CP04 `cp04_native_rate`, CP05 `cp05_native_rate`) sobre un clip B/C nativo fresco, después del handoff de Expansion (1.0/1.15/1.30 Blue; exactamente 1.15 Red/Black normal). No se cambia daño, hitbox, posición, IA global ni velocidad de movimiento; nunca se salta ni reinicia un clip.

| Patrón | Tasas 0.11.10 | Tasas 0.11.11 | AT objetivo 0.11.10 | AT objetivo 0.11.11 | AT medido (clip B / C) |
|---|---|---|---|---|---|
| Blue 2+2 | 1.00 1.00 1.50 1.50 | 1.10 1.10 1.50 1.50 | pausas 12/12/2 | pausas 8/8/2 | 54/50/31 → **47/44/31** · 59/55/34 → **51/48/34** |
| Red4 | 1.00 1.15 1.15 1.00 | 1.05 1.35 1.35 1.05 | 68/46/72 | 60/36/62 | **60/36/62** · 60/38/62 |
| Black8 | 1.00 1.00 1.15×5 1.00 | 1.05 1.05 1.30×5 1.05 | 65/67/46×4/70 | 62/62/38×4/64 | **62/62/38×4/64** · 62/62/39×4/64 |
| Black7 | 1.15 1.15 1.00×5 | 1.30 1.30 1.05 1.05 1.20×3 | 46/68/70/56×3 | 38/62/64/47×3 | **38/62/64/47×3** · 39/62/64/47×3 |

Medidos con los callbacks de producción, `executeAttack`/`executeFind` nativos sin cambios y las políticas reales de Expansion (golpes que no contactan; ambos órdenes de registro dan lo mismo). Las +1/+2 en clip C son extensiones del propio clip nativo (más largo), registradas, no truncadas. Duración primera→última apertura AT: Blue 135→122 (B), Red4 186→158 (−15 %), Black8 386→340 (−12 %), Black7 352→305 (−13 %). Con guardia sostenida el control FIX01 da 62 (Black8 1→2) y 38 (Black7 1→2), igual que el objetivo.

Muestreo de colisión (cálculo float32 con la semántica de `J3DFrameCtrl::update`, AT nativo en frames pre-play 14..22): 1.05→8 pasadas, 1.20/1.30→7, 1.35→6 (poses 15.85–22.60). Ninguna tasa nueva baja de las 6 pasadas del Blue 1.50 ya aprobado por el usuario con dos parries consecutivos. Los avisos SFX `checkFrame(10/12.5/19)` y `(7/11.5)` siguen disparándose (separación mayor que el paso). Black normal ≤1.30 < 1.5 (`static_assert`), por lo que nunca se confunde con la furia.

`post05::e2_rate_known` **no** se amplió: bajo la política activa GENERAL la fase E_OC2 solo etiqueta telemetría y no decide la supresión anti-tambaleo (verificado por los laboratorios de terminal FIX02 y FIX01 nativo a las nuevas tasas). `lnks1fix::continuation` solo exige rate>0. La prueba terminal FIX02 (rate0 al final de B/C/recoil) no depende de la tasa.

## 2. Parry en todos los espadazos

Sin cambios en la regla: ventana [−1,+7] frames, edad ≤9 ticks, nueva pulsación R+B, inicio nativo `procGuardAttackInit`, serial nuevo, contacto fresco (ArmTrack), marca nativa AtShieldHit. Laboratorio de combate (`test_cp06_combat.py`): por cada patrón, cada índice individual y cada par consecutivo (Red 2→3, Black8 3→4…7, Black7 1→2, 4→7, etc.), clips B y C, ambos órdenes de hooks: 152 combos, un parry confirmado por índice seleccionado, guardia nativa en el resto, serial distinto por parry, ruptura a 100 cancela legítimamente (5.º parry Black). Un mismo Shield Attack no sirve para dos golpes; pulsar 10 pasos antes da MISSED_EARLY; pulsar tarde da NORMAL_GUARD. Blue 2+2 a 1.10/1.50 con máscaras de parry cubierto por el adaptador CP04 heredado.

### 05-A Red especial ×2 — auditoría

No existe ninguna exclusión de POST08 para Red (el gate de furia excluye ATP2). En el log humano 0.11.10 de referencia, los 10 contactos a ×2 (Red ATP2 y Black furia ATP6) se juzgaron con Link **fuera** de `PROC_GUARD_ATTACK` en la pasada que resolvió el golpe; cuando hay una pulsación R+B cerca llega **0–2 ticks después** del tick de juicio (1–3 tras la pasada). Es decir, el golpe ya estaba bloqueado por la guardia normal. El ×2 de Expansion abre AT unos 7 ticks después de empezar (frente a 13–14 a ×1/×1.15). Con un Shield Attack a tiempo, el laboratorio confirma el parry contra la causa Random auténtica de Expansion (sin cambiar su selección, ×2 ni barrido); pulsación tardía = guardia nativa. No se amplió la ventana ni se crea contacto. Nuevo diagnóstico de solo lectura `CP06_PARRY_TIMING` registra cada R+B que llega después de la pasada resolutiva para que la prueba humana lo confirme.

### 05-B Black furia ×2 y chip

Parry de furia solo si coinciden: E_OC2, potencia 6 en ambas esferas, clase LNK07 BLACK_FURY de la generación y tasa exactamente 2.0 (×2 de Expansion). Si falla cualquiera, se conserva el gate antiguo (≥1.5 o desconocido ⇒ sin parry). Black normal a 1.30 sigue siendo Black.

El chip de Expansion CP19F2 (−1 unidad de vida pendiente) se carga en su POST (prioridad 0) del **mismo** `daE_OC_c::execute` en que POST08 confirma el parry. CP06 añade dos callbacks POST en el objetivo existente (90 antes, −250 después). Solo si el parry se comprometió, el par escudo nativo (esfera↔cilindro de Link, mismo predicado que Expansion) estaba presente, la vida de Link y el tipo de cuenta pendiente no cambiaron y la cuenta bajó **exactamente** 1, el escritor nuevo `cp06_native_chip_restore` devuelve +1 con lectura exacta, una vez por token de golpe. Cualquier otra diferencia (−2, curación, tipo, vida, sin captura) se rechaza y se registra; la guardia normal conserva su chip. Laboratorio: 8 casos × 2 órdenes con la lógica de chip de Expansion transcrita de fe47c8b y su `cp19f2_policy.hpp` real.

**Limitación honesta:** el destello rojo de Expansion se dibuja en su propio hook de render y no se controla: un parry perfecto de furia puede mostrar ese destello aunque no se pierda vida. La telemetría de Expansion puede informar `LIFE_NOT_LOWER`. Ambos quedan para observación humana.

## 3. Seguridad y auditoría

Nueva capa `ci/cp06_audit.py`: los 37 archivos de producción 0.11.10 deben reproducirse byte a byte tras el parche inverso exacto y contado (18 fragmentos en 6 archivos); los dos módulos nuevos y la referencia de chip están fijados por hash; un único escritor nuevo; prohibidos otros escritores nativos. La cadena antigua (FIX02→CP05→FIX01→CP04, barreras 0.11.2/CP02-03) se conserva y solo se compone con la nueva capa. `ci/cp06_pe_audit.py` inspecciona la DLL MSVC: exactamente un almacén float en `g_dComIfG_gameInfo+0x98f0` y uno de byte en `+0x99e6`, ningún otro almacén desplazado, con 3 negativos de instrucción rechazados.

Sin nuevos objetivos de hook (24) ni imports del juego (63, idénticos a 0.11.10; también idénticos en una compilación cruzada clang-cl local de base y candidata).

## 4. Rendimiento

Banco sintético (`tests/bench_cp06.py`, mismos callbacks/modelo/compilador g++ -O2, 3000 ticks × 15 repeticiones, mediana): coste de callbacks de combate por actor y tick 248–251 ns (base, 16 actores) frente a 262–264 ns (candidata); 64 actores 325–328 → 342–343 ns. La puerta O(1) de CP06 (sin barrido de 64 slots cuando no hay ventana de chip armada) bajó el coste de 396–401 a 347–358 ns con 64 actores (−12 %, ≈3 µs/tick). Neto: +5 %, ≤1 µs por tick con 64 actores (0,003 % de un tick de 33 ms). En el runner de CI la medición es ruidosa y no concluyente. No es FPS ni GPU; el FPS real queda HUMAN_RUNTIME_PENDING. El resto de rutas calientes (POST03/05/08, HUD, LNK) no cambian byte a byte, por lo que no se optimizó nada fuera de CP06 sin evidencia de ganancia segura.

## 5. Verificación

23 laboratorios / **4.899.024** comprobaciones en Linux y MSVC (4.486.668 heredadas − 18.816 por las pausas Blue 12→8 + 431.172 CP06). Combate CP06 58.692. **579/579** mutantes (550 heredados con anclas reorientadas a la semántica equivalente + 29 CP06), 0 TIMEOUT; un mutante CP06 descartado por equivalente (comprobación `tick<e.tick` redundante con aritmética sin signo). 34 negativos de fuente CP06 + todos los heredados. Expectativas heredadas cambiadas por diseño: tasas/pausas Blue, tablas Red/Black, intervalos 65→62 y 46→38 del control FIX01, envolvente geométrica 1.05–1.35, versión 0.11.11.

Las pruebas ejecutan cuerpos nativos auténticos y callbacks de producción; el movimiento de Link, los contactos de broadphase y el render están modelados.
