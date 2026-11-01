# POST05 — notas de investigación (WIP, NO compilado, NO probado)

Estado: **GATE 05-R en curso**. Ningún `.dusk` de POST05 existe. Nada de esto es [C] ni [R].

## Hallazgos [S] (d_a_e_oc.cpp @40457c6) y [B] (dusklight.exe ffa99203…0049)
- Enum: 3 FIND, 4 ATTACK, 5 DAMAGE, 6 BIG_DAMAGE, 7 WATCH, 9 DEATH (`:20-37`).
- `action()` llama a `damage_check()` primero (`:2418`) y después al `switch` que lanza `executeDamage` en el mismo cuadro (`:2475`). La animación y la voz de daño empiezan en `executeDamage` (estados 0–4 → `setBck`), no en `damage_check`.
- La ruta ordinaria termina con `setActionMode(DAMAGE, my_val)` (`:783`). [B] `call` en `0x140e067b9` seguido solo del epílogo; el salto con giro cancelado escribe `cooldown=3` justo después (`0x140e06785`).
- `setActionMode` [B] (`0x140e0d260`) escribe exactamente: `+0x8cc ← +0x8c8`; `+0x8c8 ← mode`; `+0x8d0 ← state`; `u32 +0x8e0 = 0` (field_0x6c0/6c2); `orl $1` en `+0xce8 +0xd08 +0xea0 +0xec0` (Tg/Co de mSphs_cc); `and $0xff7f` en `+0x69a` (HeadLock).
- `cc_at_check` (d_cc_uty.cpp:372+) resta HP, lanza el SE de impacto, el hit-stop y la marca, ANTES de `setActionMode`.
- `mOldActionMode` solo se escribe en E_OC (`:585`); nunca se lee.
- HM CP11 (`hm_203/core8`) solo toca E_OC vía `cc_at_check`. Bars solo el medidor. Expansion (fuente más cercana 0.16.2) engancha `daE_OC_c::execute` PRE+POST y escribe modos, `field_0x6c2` y la velocidad de ataque. **Las fuentes exactas de EVF 0.15.0 y Expansion 0.17.0 no están disponibles: [P].**

## Estrategia elegida (pendiente de laboratorio/CI)
B estrecha: en el POST de `damage_check`, tras POST03.1 y POST04, deshacer EXACTAMENTE la última llamada `setActionMode(DAMAGE)` restaurando `mActionMode/mOcState/mOldActionMode` a sus valores PRE. Solo cuando las otras escrituras de `setActionMode` fueron no-ops (timers 0, bits Tg/Co a 1, HeadLock a 0, leídos en PRE y POST). Whitelist PRE: ATTACK estados 0/1/2. Solo SWORD no letal, ponderado, sin cruzar el umbral, `cooldown 0→10`, sin admisión inestable.
A (hook en `setActionMode` con skip) se descarta: rompe la firma P2 de POST03 y exige `HOOK_SKIP_ORIGINAL`. C (`executeDamage`) llega tarde.
Las direcciones de `GetObjTg()/GetObjCo()` deben compararse en runtime con `+0xce8/+0xd08/+0xea0/+0xec0` antes de escribir (miembros `protected`: no hay `offsetof`).

## Hecho en este worktree (sin compilar en CI)
`src/reaction_core.hpp` (decisión pura + plan de restauración + contadores R1–R5); `NativeAux` transportado PRE/POST; `ConsumeOutcome` y `ever_frozen` en el núcleo de postura. Los labs heredados pasan en g++ (1660 / 29558 / 12826 / 556878).
## Falta
`mod.cpp` (lecturas aux, comprobación de layout, escritor restringido), `POST05_WRITE_EFFECTS_AUDIT.md`, `reaction_lab` con oráculo y T01–T26, mutaciones, reglas de auditoría (escrituras solo en `restore_reaction`), CI/PE, artefacto, README_TEST.
