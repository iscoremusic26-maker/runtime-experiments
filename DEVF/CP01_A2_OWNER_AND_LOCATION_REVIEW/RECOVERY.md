# Recuperación de revisión focalizada owner/ubicación

Base exacta **b342a8dfdf47fa503f02cb91c470d66e646334c5**, tag `DEVF_CP01_A2_DISARMED_CONTROLLER_VERIFIED`, rama histórica `implementation/devf-cp01-a2-disarmed`, PR12 draft sin merge. Se comprobaron tag^{commit}, árbol limpio y ascendencia2911af6.

Rama nueva: **review/devf-cp01-a2-owner-location**. Tag nuevo: **DEVF_CP01_A2_OWNER_LOCATION_REVIEW**. SHA publicado de esta entrega mediante `git rev-parse DEVF_CP01_A2_OWNER_LOCATION_REVIEW^{commit}` y el enlace de commit de la entrega. PR draft contra la rama base. No mover tags, force-push, merge o modificar checkpoints anteriores.

## Qué se creó y qué no se repite

Solo cinco Markdown de esta carpeta: OWNER_RESOLVER_REVIEW, FIRST_TEST_LOCATION_REVIEW, EXACT_REMAINING_EVIDENCE, GATE_DECISION y RECOVERY. Sin código compilable modificado, scripts nuevos, DLL/.dusk, originales o logs privados. No defecto demostrado del resolver; no correcciones. No ejecutados99checks, mutantes, builds, binario ni juego. Las lecturas/comparaciones de documentos/fuentes existentes son comprobaciones offline, no PASS_LAB nuevo.

Tres PASS previos intactos; DLLfd9f04fdd52c87ac29ed491f6cdcb8f1b39187ac6086179a8b033412ce5b5ad1 sigue vinculada exclusivamente a código compilado0fa942f/CI38341931143. No se atribuye ese hash a un binario nuevo. Ledger previo de fuente se coteja con archivos actuales para asegurar que la nueva documentación no cambió el consumidor.

## Fuentes focalizadas

- Dusklight oficial limpio40457c6adb381928e4b5fef6ed459ed291edd5e2: scene lookup/append, node/layer/create/executor, dStage room/stay/next, dScnRoom status y dScnPly mProcID; dos setter sites de puertas para esclarecer next!=stay. Referencias exactas y matriz en OWNER_RESOLVER_REVIEW. No hostpatch ni auditoría general.
- Reader/Registry G2 y código/docs A2 actuales reutilizados, sin cambios. Tick→management y tipos/export/import anteriores conservados; no auditoría SDK nueva.
- G4 position-query/cotas/soporte/prismas/paredes/objetos y agregados históricos G2 reutilizados. No releer28capturas, KCL, ARC o models; no recomputar16+98 puntos.
- Consulta nueva acotada del source `d_a_obj_rgate.cpp`: condiciones de apertura/áreas/evento referidas a jugador/caballo/coach/switch/label. Esas rutas no cuentan E_OC. Create selecciona RIDER_GATE_OPEN00, distinto del registro R03_gate; no se prueba su correspondencia. No evento/cut universalmente certificado, ni ARC M_RGate00 obtenido o requerido automáticamente.
- Documentos de arquitectura y movimiento/progreso G4 sirven para límites, no nueva investigación. Dawnlight no se volvió a consultar.

## Decisiones y carencias

Owner **OWNER_STATIC_SUFFICIENT_FOR_TEST_DESIGN**, contrato preflight condicionado; runtime owner no verificado. Máscara0x2e/counts/next pueden rechazar contextos vivos correctamente por prudencia del primer ensayo, sin relajarlos. Pending monitor nativo no implementado y no sustituirlo por este preflight que rechaza creates.

Punto único C(-4806.7346,-6729.480961460304,65135.8281), F_SP121/R3/logical6: **FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE**. Faltan medio/BG efectivos y ocupación/contexto presentes. No motivo demostrado de rechazo, no punto alternativo/barrido y no admisión automática de C. Recursos/integridad/geometry cerrados; comportamiento de navegación universal ya no es prerrequisito del ensayo.

G4 POSITION_BLOCKED/NO_SAFE_POSITION_VERIFIED, G5/CP02 NO-GO, G6 NOT_VERIFIED, creación/render NOT_TESTED y DLL personalizada BLOCKED independiente. Sin actor/perfil/edición/hook/hostmod o instalación. DISARMED_NO_REGISTRATION intacto.

## Recuperar en copia independiente

```bash
git init work/devf-a2-owner-location-recovered
git -C work/devf-a2-owner-location-recovered remote add origin https://github.com/iscoremusic26-maker/Mods-Duskligh.git
git -C work/devf-a2-owner-location-recovered fetch origin refs/heads/review/devf-cp01-a2-owner-location:refs/remotes/origin/review refs/tags/DEVF_CP01_A2_OWNER_LOCATION_REVIEW:refs/tags/DEVF_CP01_A2_OWNER_LOCATION_REVIEW
git -C work/devf-a2-owner-location-recovered switch --detach DEVF_CP01_A2_OWNER_LOCATION_REVIEW
git -C work/devf-a2-owner-location-recovered rev-parse HEAD
git -C work/devf-a2-owner-location-recovered rev-parse HEAD^
git -C work/devf-a2-owner-location-recovered diff --name-only b342a8dfdf47fa503f02cb91c470d66e646334c5 HEAD
git -C work/devf-a2-owner-location-recovered status --short
```

Padre b342a8d…; diff únicamente los cinco informes. Publicación verificada por fetch GitHub a bare nuevo, igualdad rama/tag/commit/blobs y referencias históricas conservadas. Ninguna recuperación arma o ejecuta nada.

## Próxima operación mínima y parada

Una captura local **futura autorizada** de solo lectura del medio/ocupación/contexto de C, añadiendo Owner escalar en la misma muestra y usando el resolver/presupuesto existentes. Especificación en EXACT_REMAINING_EVIDENCE; ningún paquete o adaptador de captura se implementa aquí y no se pide al usuario ejecutarlo. Con esos datos, decidir admisión del mismo punto y después plantear adapter activo con autorización nueva, revisión/paquete propios.

No repetir CI por documentación. No producir otro prompt ni iniciar G5/G6/CP02. Se detiene al publicar y comprobar el checkpoint.
