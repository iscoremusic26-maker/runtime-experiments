# Auditoría binaria del DLL 0.8.0 descargado [B]

## Archivos

| Versión | DLL SHA-256 | Origen |
|---|---|---|
| 0.8.0 | `0049e3fd…8429` | artefacto 13118929802 |
| 0.7.0 | `ca507493…09d9` | artefacto 13118435513 |

Ambos se descargaron por su ID de artefacto y se compararon con `objdump -d` y el mapa del enlazador del CI.

## Lecturas nuevas (`post08_judge`): coinciden con el EXE

- **Esferas At** (indexadas por esfera; base `0x1028`, paso `0x1b8`):
  - `movzbl 0x103c` = bit de golpe At (`+0x14`);
  - `mov 0x1040` = objeto golpeado (`+0x18`);
  - `movzbl 0x10bc` = `AtShieldHit` (`+0x94`).

  Son los mismos offsets que `dCcD_GObjInf::ChkAtHit`/`GetAtHitObj` del EXE (`0x140813030`/`0x140813900`).
- **Link:**
  - `cmpw $0x1e,0x4144` (`PROC_GUARD_ATTACK`);
  - `movss 0x2d4c` (frame de la animación);
  - `movss 0x45d8`/`0x45dc` (inicio y fin del Shield Attack);
  - `lea 0xb28`/`0xce8`/`0xea8` (`mTgCyls[0..2]`).

## Escrituras al actor (diferencia con 0.7.0)

- **Añadidas:** exactamente 10, en `post08_step` (el `restore_reaction` en línea del desvío): modo, estado, modo previo, `0x8e0`, `0x8e2`, `0x69a` y los bits Tg/Co de `0xce8`/`0xd08`/`0xea0`/`0xec0`.
- **Eliminadas:** ninguna.
- **Sin escrituras nuevas en:**
  - vida (`0x656`), atención (`0x650`) y cooldown (`0x8ec`);
  - `mCutType` de Link;
  - campos de Link (`0x4144`, `0x2d4c`).

## Imports

- El mismo conjunto que 0.7.0: `PE_AUDIT_PASS` con el pin de 0.7.0 sin tocar.
- 5 hooks; ninguno nuevo.
