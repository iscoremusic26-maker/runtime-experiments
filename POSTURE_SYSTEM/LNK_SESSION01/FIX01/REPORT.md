# Informe final SESSION01 FIX01

## A. Causa raíz LNK02

`lnk_pre` buscaba tarde un Tg que Link ya había consumido y limpiado al armar invulnerabilidad. Los diez `NOT_BLOCKED/tg_match0` aportados se rechazaban en classify antes de confirm_direct. La fuente exacta prueba esa ruta y el laboratorio reproduce el rechazo 0.10.0, con ambos órdenes de actores. No se afirma haber leído el log completo no disponible. FIX01 captura el primer cilindro seleccionado en checkDamageAction PRE/POST y el resultado ambiental scoped de checkPolyDamage; une solo contacto fresco del mismo tick/actor/generación/token con daño efectivo y timer nuevo. Se excluyen escudo/chip/parry, suelo, electricidad, armadura sin pérdida, invulnerabilidad, fuente ajena, ambigüedad, duplicados, cambio de Link, pausa, muerte y reciclaje. Misma postura, pesos y recuperación; cero nuevas escrituras a Link. Detalles y offsets: [IMPLEMENTATION.md](IMPLEMENTATION.md).

## B. Causa raíz IA

POST06 puede sustituir ATTACK por stun cuando una espada cruza 100. action había apagado At; si executeAttack ya no registra esa esfera, el motor no limpia el viejo AtHit. Al volver a ATTACK, el contacto antiguo contra Link guardando fuerza un rebote antes del frame 14; no se rearma, por lo que el registro puede sobrevivir y repetirse. El FIX02 histórico ya señalaba esta interacción pendiente, fuera de su aplazamiento específico de parry. El Breaker real y un modelo de Set/Move/executeAttack reproducen los abortos antiguos y el armado corregido.

La reparación registra temporalmente para que **el motor** limpie, y restituye Off antes de comprobar colisiones. No genera golpe extra, no borra AtHit manualmente ni fuerza FIND/recoil por watchdog. El contacto legítimo sigue visible a Expansion hasta su execute POST. POST05/POST08 reciben además un contrato de continuación válido, conservando la reacción nativa si falla. No se cambia el código ni las políticas de Expansion. Los16inicios/7armados/9abortos, maxFrozen1 y contactos stale del222/gen4 son coherentes con esta clase de fallo; sin el log íntegro, su cadena individual exacta permanece **AI_CAUSALITY_UNVERIFIED**, no HUMAN_PASS.

## C. Prevención general

La limpieza y la seguridad se basan en identidad/frescura/intervención, no en actor 222 ni color. Blue/E_OC, E_OC2 Red/Black/furia y Blue legado usan la misma regla. El modelo cubre ritmos 0.75/1/1.15/1.3/2 y grupos 1/2/4/8, preserva bits previamente On y rechaza peticiones vencidas/ajenas/no ofensivas. Continúan las exclusiones nativas por muerte/evento/cadena física y las políticas de admisión. Furia sigue con peso45 y sin parry; no se alteran chip, robo de vida ni aceleración.

El monitor exige armado AtSet real más terminación nativa del ciclo. Inicios/frames por sí solos no son recuperación. Detecta abortos recientes aunque existan armados históricos; distingue cancelación legítima, bucle, transición congelada, muerte antes de recuperar y expiración inconclusa. Preserva totales aunque se agoten los presupuestos de mensajes. Solo observa identidades intervenidas y no escribe al juego.

## D. Regresiones y límites

Cada compilador ejecutó 14 laboratorios: g++ con ASAN+UBSAN y MSVC x64, 1045932 comprobaciones por compilador.

| Laboratorio | Comprobaciones | Resultado |
|---|---:|---|
| hit | 1660 | PASS |
| posture | 556878 | PASS |
| parry | 1570 | PASS |
| collider | 12826 | PASS |
| lnks1 | 178 | PASS |
| hud | 57742 | PASS |
| lnk | 528 | PASS |
| fix01 | 21570 | PASS |
| break | 243624 | PASS |
| compat | 55992 | PASS |
| general | 5560 | PASS |
| rb | 21313 | PASS |
| lifecycle | 29558 | PASS |
| reaction | 36933 | PASS |

236/236 mutaciones detectadas, incluidos los194 casos heredados; 19/19 negativos PE rechazados; decodificador PMF estático5 válidos/10 rechazados; negativo adicional de metadatos de descarga rechazado. Fuente y PE PASS. El formateador MSVC produce la muestra exacta de g++; extractor y renders de referencia pasan, sin confundirlos con capturas del juego.

Frente al DLL 0.10.0 descargado:35→39imports del juego, seis→diez objetivos, ahora ocho HOOK_MEM y dos HOOK_MEM_EXT24paraLink. Se añaden checkDamageAction, checkPolyDamage, executeAttack y cc_set por razones concretas de captura/observación/limpieza. Servicios/exports/CRT/sistema sin cambios. El materializador PMF se inspecciona estáticamente, nunca se ejecuta durante la auditoría. Único escritor enemigo nuevo: AtSet bit0 del propio actor durante cc_set; no nuevos escritores de HP/Link/velocidad/animación.

O(64) de memoria y unión por actualización, O(1) por callback; sin asignaciones por frame, hilos ni búsqueda global por contacto. FPS/CPU y las ocho integraciones en juego: HUMAN_RUNTIME_PENDING. SDK/host/EXE fijados sin modificar; no se tocó otro mod, ROM/ISO/save o instalación. Solo ramas nuevas, sin PR/merge/tag/release. Hubo correcciones internas del auditor PMF y del manifiesto durante el desarrollo; la ejecución final vuelve a construir y comprobar todo. Véanse evidencias JSON y [TEST_PLAN.md](TEST_PLAN.md).

## E. Artefacto

[Descarga final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41524848968/artifacts/13179886722). Nombre `POSTURE_LNK_SESSION01_FIX01_0_10_1_DIRECT_HITS_AI_STABILITY_PRIVATE_TEST_windows-amd64_5454f32e0bb1.dusk`, **96454 bytes**, SHA-256 `e7b8d5dff337ae1274abc586278999527efe3c1f5c40623b051a8403a29c397d`. Fuente `feature/posture-lnks1-fix01-direct-hit-ai-liveness` @ `5454f32e0bb1fbdfde6ac866e94104e1b56df6be`; CI `ci/posture-lnks1-fix01-direct-hit-ai-liveness` @ `6e615ea4134d105566905ddd6911f4c8fdd2230a`; run `41524848968`, artifact `13179886722`. mod.json `dev.posture.post05_selective_reactions`/0.10.1; PE_AUDIT_PASS y ARTIFACT_DOWNLOADED_VERIFIED. Datos completos, expiración, DLL y rollback en [DELIVERY.md](DELIVERY.md) y [RESULTS.json](RESULTS.json).

## F. Prueba humana

Instalar solo el archivo final del mismo ID con el juego cerrado. Comprobar directos Blue/Red/Black y furia, invulnerabilidad sin crédito extra, bloqueos y parries, golpes sub100 contra Blue guardando, cruces 100 mientras golpea el escudo, Shield Attack, equivalentes Red/Black, furia y grupos mixtos, ruptura/Helm/Finish/rearme, recuperación/HUD/controles/pausa. Esperar ataques completos tras las intervenciones. Líneas: LNK_S1_FIX01_DIRECT, LNK_S1_DIRECT, LNK_S1_FIX01_AI, LNK_S1_FIX01_AI_CLEANUP, LNK_S1_FIX01_SUMMARY, POST05_DECISION, POST06_EVENT, POST08_EVENT y logs de Expansion. Muerte/expiración no son PASS. Conservar el log completo; ante crash, invariantes rotas, crédito doble, daño alterado o atasco, volver a 0.9.0. Pasos detallados: [TEST_PLAN.md](TEST_PLAN.md).
