# Prechecks A/B/C y revisión incremental del scope

Se conservan el backend nativo, preset, import library, setter oficial, monitor por ID y latch del checkpoint #16. Solo nuestras copias de build reciben hooks de política/traza. No se cambia ActorService ni se registra perfil/actor/stage/hook alguno.

1. Sin sesión autorizada: return BLOCKED, traza deduplicada SESSION_GATE_DENIED, **cero capturas, setters y requests**.
2. A: captura nueva; owner/host/thread/F_SP121/room3/logical6/ROOM/PLAY/bindings/layers/previous/colas/eventos/medio/recursos; C exacto; política Link/actores. Después se vincula la Key dinámica o se contrasta la Key explícita.
3. B: nueva captura del mismo update; misma escena/root/child/parent/PLAY/previous y secuencia mayor; revalida toda la política, posiciones/identidades y datos completos. Fallo antes del latch: no setter ni request; los fallos de revalidación son STOP.
4. Latch irreversible **antes del primer setter**; resolver capa hija registrada en vivo; nunca root ni owner de Link como sustituto.
5. C: tras seleccionar hija, captura nueva con current=child y contexto vigente, guard/medio/recursos/freshness nuevamente aprobados. Fallo: ningún enqueue; restaura previous y STOP con latch consumido.
6. Una llamada a create_actor, ID escalar, restauración RAII exactamente a previous registrado; luego requested/monitor. Restaurar no garantiza lifetime de sala ni cancela la cola.

Cada A/B/C reutiliza los recorridos originales de su captura; la extensión no agrega scans paralelos independientes. Las tres capturas frescas corresponden a los tres puntos de revalidación ya existentes. No se usa una captura anterior para evitar el check C ni se afirma atomicidad perfecta.

## Defecto focalizado corregido

El reproducer compila el core original sin modificar y simula reentrada en preflight A o B. El intento interior hacía STOP, pero el exterior podía continuar y sobrescribirlo al consumir latch. La extensión comprueba estado terminal después de las lecturas externas y antes del latch/enqueue; los dos fixtures nuevos exigen cero setters/requests. El checkpoint histórico y su admission NONE no se alteran. La evidencia Windows distingue el reproducer esperado del resultado de la corrección; no es una auditoría general repetida.

La traza se almacena solo en memoria propia durante el scope. El logger externo se llama después; throw/retorno falso no afecta el control. Reentrada posterior sigue siendo STOP. No hay cancel/delete/rollback, forced room/load, escrituras de flags, saves o recursos. Si previous desaparece, RESTORE_FAILED sin fallback root; ante incertidumbre tras enqueue se instruye full exit humano futuro, sin prometer reversión de progreso.

Se preservan los límites anteriores: petición asincrónica, posible execute E_OC antes de nuestro READY, ausencia de lease/generation handle, timeout120 polls y presupuesto READY60, sin cleanup seguro ni hot reload. El bloqueo de descarga DLL custom sigue independiente.
