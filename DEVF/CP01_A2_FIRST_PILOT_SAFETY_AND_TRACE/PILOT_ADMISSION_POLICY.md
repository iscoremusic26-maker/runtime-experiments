# Política de admisión del piloto, implementada offline

Esta revisión implementa **LOCATION_CANDIDATE_CONDITIONAL**. Conserva **SESSION_NOT_AUTHORIZED** y **LOCATION_SAFE_UNVERIFIED**. Un resultado de `assess()` significa cumplir el guard artificial del piloto; no acepta las incertidumbres ni aprueba formalmente C.

C se conserva, con sus valores float32 reales promovidos a double para calcular distancias: (-4806.7343750, -6729.4809570, 65135.8281250). No se corrige ni desplaza el candidato.

## Decisión exacta

Link y los demás actores identificables requieren **distancia horizontal XZ >=1600**. Para Link es la propuesta de diseño ~1200 de búsqueda E_OC +400 de margen; ninguna fuente demuestra que ese umbral impida detección, persecución, daño o colisión. Para otros actores se aplica el mismo umbral como regla inicial conservadora de ocupación por centros, sin inventar bounds individuales. Una gran diferencia Y no concede separación horizontal.

Todos los actores de la cola observada deben tener ID/perfil identificable, room0–63, owner registrado, init2, actorINIT y XYZ finitos; únicamente se excluye el Link explícitamente identificado. Los actores de otra room también se consideran: si están cerca en coordenadas de mundo, se deniega. Room−1 o campos desconocidos de un actor incluso lejano deniegan: política deliberadamente estricta, cuya satisfacibilidad en la sesión real **no se ha observado**. No reinterpretar un actor global desconocido como inocuo.

Link necesita el perfil oficial verificado por el reader, ID/membresía/owner/room coherentes y velocidades públicas `speed` y `speedF` finitas y exactamente cero. Cualquier movimiento observable de Link o cambio de actores entre A/B/C también deniega. Esto no demuestra inmovilidad futura ni ausencia de cambios entre la última lectura y el enqueue.

Se exige captura coherente, secuencia nueva, mismo update/contexto, censo completo no truncado ni duplicado; GroundCross observado en bg0/poly2174/room3/ground0/special0/no moving y Y dentro de0.01; agua vertical NO_HIT_AT_PROBE; scan BG completo, no truncado y cero candidatos; recursos leídos y E_OC/E_ocb registrados. UNKNOWN o fallo de una comprobación necesaria deniega. Water volume, BG exacto/transform y overlap continúan sin verificación por las APIs seguras usadas.

## Admisión y autorización separadas

El proveedor nativo `current_admission()` se reutiliza **sin cambios**, devuelve `{}` y deniega sesión/ubicación. Se retorna antes de cualquier reader, setter o request. No hay config, tecla, export, UI o API pública de armado. La DLL experimental conserva una ruta de creación real y no se presenta como READ_ONLY ni se distribuye.

Los fakes conceden permisos sintéticos y piden `bind_context_live=true`. La Key se obtiene después del precheck A desde node/child/play/parent/room/logical **actuales**; no de los IDs102/6/60/5 del log. Una Key explícita también se sigue comparando, sin bypass. B y C vuelven a comprobar identidad, medio, recursos, separación y freshness.

Una revisión futura del proveedor necesitaría autorización del usuario y nueva build/auditoría/paquete. No puede sustituir los preflights por flags true. La sesión cold-start, el paquete y el spawn real aún no están autorizados; G4/G5/G6/CP02 no se elevan por esta política.
