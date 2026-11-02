# Candidata privada POST06 rework 0.6.1

**PARTIAL_CANDIDATE / HUMAN_RUNTIME_PENDING.** El código está implementado, compilado y auditado. La oportunidad sigue la duración del mareo nativo, con un máximo de 90 ejecuciones propias: puede terminar antes de tres segundos. Faltan las pruebas dentro del juego.

[Descargar ZIP privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41386845338/artifacts/13115359099) · [Run de compilación y descarga verificada](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41386845338)

| Dato | Valor |
|---|---|
| Archivo para instalar | `POSTURE_POST06_1_REWORK_PRIVATE_TEST_windows-amd64_5037d3f311c3.dusk` |
| Tamaño del .dusk | 44011 bytes |
| SHA-256 del .dusk | `408b0c32679b1b930658e79e5f72ae123a4cf49bd382d98d2c549bb0285c030a` |
| Fuente realmente compilada | `5037d3f311c31dfb6b57a98a0c754b9e2bfd5ba9` |
| Rama fuente | `feature/posture-post06-rework` |
| Base congelada | `a0a81535639459275702371324448e96a5d17575` |
| Commit CI | `3860ca54970ce4dcb3a3b995edc6f68eb44126a3` |
| Rama CI | `ci/posture-post06-rework` |
| Run / artifact | `41386845338` / `13115359099` |
| Nombre del artifact | `POST06_TEST_41386845338_1` |
| Caducidad del artifact | **1 de diciembre de 2026, 23:11:03, Panamá** / 2 de diciembre, 04:11:03 UTC |
| ZIP descargado por ID | 45394 bytes; SHA-256 `75aa6be2fc8d7062e373eddd21bd8e5d7d2f45cda1f41dd4513a4ea72039a2bd` |
| DLL extraída | 89088 bytes; SHA-256 `a5f1cc37e3f90af1fb145dc5845b3326957a9d9ff89b8f694475a9ef04ecfca2` |

La descarga requiere acceso al repositorio privado. Alternativa por CLI:

```sh
gh run download 41386845338 --repo iscoremusic26-maker/codex-cp00-inputs --name POST06_TEST_41386845338_1
```

Instalar solamente el `.dusk`, con el juego cerrado. Guardar y retirar 0.6.0/0.5.4 y cualquier otra versión del mismo ID antes de instalar. Este paquete conserva `dev.posture.post05_selective_reactions`.

[Rollback 0.6.0](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41376998495/artifacts/13111921457) · [Rollback 0.5.4](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41371589990/artifacts/13109308222). No se sobrescribieron paquetes ni ramas anteriores. Su disponibilidad depende de la retención de esos artifacts históricos.

## Comportamiento y verificación

- Bajo 100 se conserva la protección GENERAL anterior.
- Ruptura: mareo nativo de Shield Attack en pie, sin bonus ni caída automática.
- Escudo real: prepara Helm, sin bonus, derribo ni renovación del plazo.
- Espada futura válida o Helm preparado: un único x1.50 sobre daño efectivo; caída, suelo y Finish nativos.
- Oportunidad desaprovechada: recuperar en pie y postura 50. Tras caída y levantamiento completo: postura 0.
- Helm independiente: adaptación equivalente a Expansion para Ordon/Master; no restaura HP tras una muerte ni vuelve a descontar el bonus cuando Expansion interviene. Wood conserva la excepción nativa de CP21.

Nueve laboratorios MSVC pasan. Nuevo `break_lab`: **242681 comprobaciones**, sin fallos; **26/26 mutaciones** detectadas en g++ y MSVC. Las ocho suites heredadas conservan sus conteos. La base 0.6.0 pasó sus nueve suites y 240 mutaciones: estas 240 se registran por separado y no se atribuyen al código nuevo. Auditoría PE sin errores y diez negativas PE rechazadas. Se verificaron el ZIP publicado, el manifest, el `.dusk` y la DLL sin cargarlos. Los 44 archivos del ledger coinciden con la fuente local compilada.

El estado interno del job de build termina en `POST05_PACKAGE_PASS_DOWNLOAD_PENDING` porque precede a la descarga; el job posterior terminó en `ARTIFACT_DOWNLOADED_VERIFIED`. Este agente hizo además otra descarga por ID y calculó los hashes.

CI inicial 41383942846: referencia incorrecta del runner a una carpeta histórica; corregida. Segundo 41384232633: la auditoría rechazó dos imports no previstos; se verificaron contra fuente y EXE y se fijó la lista exacta. La candidata intermedia 41384941523 pasó. La final 41386845338 añade la validación de contacto fresco y el collider nativo de escudo; pasa sin relajar hashes ni admitir imports arbitrarios.

## Prueba humana y límites

Primero nueva candidata + Zora; después los ocho mods. Comprobar ruptura sin vuelo, espera, escudo sin Helm, Shield→Helm con contacto, espada directa, Finish y levantamiento; luego variantes, HM x2 y barras. Enviar por chat el log completo de cada fase y la secuencia observada. Ante crash, `VERIFY_FAILED`/`ok=0`, doble daño, caída sin contacto, Helm imposible, animación congelada, Finish ausente o rearme prematuro: detener y volver al paquete anterior con el juego cerrado.

No se ejecutó el juego. Faltan duración visual y pausa/FPS, disponibilidad y contacto de Helm, animación, dirección, audio, Finish, muerte y convivencia jugable con ocho mods. No afirmar ventana fija de tres segundos ni compatibilidad universal.

[Informe español de ocho apartados](REPORT.md) · [Matriz de 36 familias y compatibilidad](TEST_PLAN.md) · [Diseño, fuentes y ABI](IMPLEMENTATION.md) · [Resultados verificables](RESULTS.json).

El commit posterior que publica estos documentos no cambia la fuente compilada indicada arriba. La instantánea Git local tiene un ancestro distinto; la rama remota parte de la base upstream correcta.
