# Mapa de las chispas de un parry

Fuente: `src/d/d_cc_s.cpp`, `d_particle.cpp`, `d_kankyo.cpp`, `actor/d_a_e_dn.cpp`, `libs/JSystem/src/JParticle/*`, `src/dusk/interp/particle.cpp` del SDK `40457c6`. Inspección de código, salvo donde se indica.

## Quién crea cada parte

| Contacto | Función | Marca | Recursos | Cuándo |
|---|---|---|---|---|
| Link hace parry: arma del Lizalfos sobre el escudo de Link | `dCcS::ProcAtTgHitmark` → `setHitMark(6, Link)` | HITNG | `ID_ZI_J_HITNG_A` (0x117) y `_B` (0x118) | Pasada de colisión |
| Lizalfos hace parry: espada de Link sobre `tate_sph` | `ProcAtTgHitmark` → `setHitMark(2, Lizalfos)` (Tg mark 5) | HITNG | A y B | Pasada de colisión |
| Lizalfos hace parry: chispa propia del escudo | `daE_DN_Execute` → `setHitMark(2, NULL)` en el brazo | HITNG | A y B | Execute siguiente |
| Destello de cualquier marca HITNG | `dKy_SordFlush_set(pos, 0)` | luz | `flush_col`, verde azulado | Con la marca |

El sonido metálico del escudo de Link sale de `setGuardSe`, y el del Lizalfos de `def_se_set`, ambos en `Z2SoundObjBase::startCollisionSE`.

## Por qué quedaba azul

Log 230009: los parries de Link capturaron 2 emisores y los del Lizalfos 4. Todas las chispas nativas estaban capturadas, pero el usuario vio azul.

El color de un recurso con animación de color por partícula se escribe en `calc_p`, después de `executeAfter`. El port de PC guarda ese color al final de `calc_p` y, en cada frame de presentación, dibuja una copia hecha con el color guardado. El tinte en `draw` escribía en la partícula viva, que esa copia no lee. Los recursos con color de emisor sí quedaban naranjas.

Esa es la causa encontrada en el código y reproducida en el laboratorio. Qué recurso concreto usa cada ruta no se ha leído del archivo original: `PARRY_FX event=RESOURCE` lo registrará en la próxima prueba.

## Cómo se tiñe ahora

| Parte | Ruta | Tratamiento |
|---|---|---|
| Color de emisor | `JPARegistPrmEnv`, `JPACalcColorCopy` | `executeAfter` (ya existía) |
| Color por partícula | `JPACalcPrm/Env` en `calc_p` | `work->mpRes` apunta a una copia privada con tablas naranjas |
| Partícula hija nacida del recurso | `init_c` | La misma copia privada |
| Hija con color fijo | `JPARegistChildPrmEnv` | `GXSetTevColor` en el callback del pase hijo |
| Otra marca del mismo choque | `ProcAtTgHitmark` | Se captura si llega en la misma pasada o en 4 ticks |
| Destello | `eflight.mLightType` | Paleta cálida nativa (tipo 1), antes de aplicarse |

El recurso compartido nunca se escribe. `work->mpRes` se reescribe en el `calc` del siguiente emisor. No se añade ninguna partícula.

## Límites

- Si el azul está en los píxeles de una textura de color, el tinte no lo cambia. `RESOURCE` da `texfmt`: 0..3 son texturas de intensidad, sin color propio. Si aparece `TEXTURE_BLUE_UNRESOLVED` o `PARRY_SPARK_BLUE_RISK`, ese caso queda abierto.
- Los blancos puros siguen blancos.
- "Sin azul" solo lo puede confirmar quien mira la pantalla.
