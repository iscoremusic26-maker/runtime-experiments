# HANDOFF MAESTRO — Dusklight Enemy Variant Framework (DEVF)

**Fecha de preparación:** 11 de octubre de 2026  
**Estado:** especificación revisada con los ZIP 2.0.3 exactos; **NO hay framework DEVF implementado ni probado**.  
**Destino:** Codex, preferentemente en un entorno Cloud con repositorio aislado.  
**Juego objetivo:** *The Legend of Zelda: Twilight Princess*, **Dusklight 2.0.3, Windows x64, DirectX 12 (DX12)**. **NO Vulkan**.  
**Política de arranque:** iniciar únicamente **DEVF_CP00** cuando el usuario lo solicite mediante un prompt posterior. No adelantar CP01 ni asumir autorización para instalar nada en el PC.

---

> **Revisión 2.0.3 (11-10-2026):** se comprobaron directamente los dos ZIP 2.0.3 aportados por el usuario, sus SHA256 y la existencia de los servicios y el ejemplo en el árbol fuente. El diseño sigue siendo provisional donde la reutilización de IA y recursos nativos requiere pruebas. No confundir comprobación de archivos con compilación o ejecución Windows.

## 0. Resumen ejecutivo y decisión de arquitectura

Construir **un mod principal `.dusk` independiente y modular** —nombre provisional **Dusklight Enemy Variant Framework (DEVF)**— que permita **crear múltiples variantes de enemigos existentes**, dotarlas de **comportamientos y apariencias diferenciados por instancia**, y **colocarlas donde el usuario elija dentro de lugares técnicamente válidos del juego**, con **apariciones reproducibles al recargar la zona**. Después habrá un **editor dentro del juego**, para no tener que editar posiciones manualmente.

Servicios nativos que se deben **aprovechar antes de inventar otros mecanismos**:

- **ActorService:** registrar perfiles de actores personalizados, crearlos/eliminarlos, gestionar creación/ejecución/dibujo/destrucción.
- **StageService:** insertar actores en registros de escenario/sala/capa; retirar registros o parches cuando corresponda.
- **ResourceService:** leer definiciones y recursos incluidos en el paquete `res/` del `.dusk`.
- **HostService / FileService / UiService y otros servicios**, solo si sus APIs exactas en 2.0.3 justifican persistencia y editor.
- Código del juego original, SDK y recursos nativos cuando convenga, **sin modificar el ejecutable**.

**Incertidumbre central y puerta de decisión CP02:** `ActorService` no proporciona por sí solo una forma demostrada de «heredar» la IA de un enemigo retail. Para construir una variante, evaluar con pruebas: **A)** instancia de enemigo nativo con personalización y control *por instancia*, usando técnicas limitadas y seguras; **B)** actor nuevo con comportamiento propio y componentes del juego reutilizados. Puede ser útil una combinación. Elegir tras prueba real del SDK, **no por preferencia teórica**. No asumir que copiar un objeto C++/perfil existente conserva correctamente su ciclo de vida.

**Plan aprobado como ruta de trabajo provisional, no como certeza inmutable:** CP00–CP08; las puertas GO/NO-GO de CP00, CP02 y CP04 pueden obligar a reducir alcance o reajustar etapas antes de continuar. El **MVP utilizable termina en CP06**, sin esperar al editor CP07. No construir un «framework de bosses», nuevas mazmorras ni un sistema de animaciones completo como parte de DEVF v1.

---

## 1. Requisitos funcionales — qué significa «poder crear y colocar variantes»

### 1.1 Variantes

- Definición con identificador estable, enemigo base/referencia y versión de esquema.
- Atributos configurables **solo donde exista mecanismo verificable**: vida, daño, defensa, velocidad, tamaño, distancias de visión/ataque, tiempos de reutilización, recompensas, etc. Un campo de configuración no convierte una capacidad en implementada: cada atributo debe mapearse a código probado.
- Comportamientos combinables: guardia, patrulla, persecución, retirada táctica, agresividad, rangos, prioridades, transiciones de estado, elección de ataques y condiciones especiales. **Ataques originales nuevos y animaciones inéditas requieren implementaciones de código/recursos específicas**.
- Apariencia **individual**: tinte, material, textura, equipo, escala, efectos y, a futuro, modelo/animación propios. Nunca recolorear globalmente todas las instancias de la especie por accidente.
- Variantes originales y enemigos vanilla coexistiendo en una misma habitación sin interferencias.
- Una variante declarada una vez se puede instanciar en múltiples lugares; una colocación puede usar ajustes puntuales permitidos (`overrides`) sin duplicar la definición.

### 1.2 Colocación

- `stage`, `room`, `layer`, posición `x/y/z`, orientación, parámetros adicionales; validación de límites y datos.
- Añadir enemigos sin reemplazar ni borrar enemigos originales, salvo decisión futura explícita.
- Aparición reproducible al cargar una sala y limpieza segura al salir, morir, cambiar de capa o desactivar el mod.
- Evitar spawns duplicados y estados obsoletos; diferenciar ID de colocación, instancia activa, actor nativo, sala/capa y ciclo de escena.
- Puntos de aparición físicamente válidos (suelo, colisión, altura, recursos, scripts). **«Donde quiera» significa escenarios compatibles, no garantía de que cualquier coordenada/sala admita cualquier actor**.
- Regla inicial: los enemigos reaparecen cuando el escenario los recrea, como una aparición de escena. Persistencia permanente de derrotas asociada a partidas será **opcional y posterior**, no alterar saves de forma silenciosa.

### 1.3 Editor (etapa posterior)

- Seleccionar una variante de un catálogo, previsualizar cuando sea seguro, colocar cerca de Link o en su posición, ajustar coordenadas/rotación, listar, editar, eliminar, guardar.
- Guardar definiciones y colocaciones en almacenamiento **propio del mod**, no modificar `.dzs/.dzr` originales ni saves retail directamente.
- Mostrar con claridad si un cambio se aplica **en el acto** o solo tras recargar la habitación. `StageService::add_actor` modifica registros procesados durante carga, **no demuestra por sí mismo aparición instantánea**.
- Modo edición explícito; fuera del modo edición, sin teclas que interfieran con los controles del juego.

### 1.4 No objetivos iniciales

- Crear modelos 3D desde cero, rigging completo o un editor Blender integrado.
- Transformar automáticamente en variantes a **todas** las familias enemigas sin adaptadores específicos.
- Cambiar el motor de renderizado, recompilar el EXE retail o depender de Vulkan.
- Un sistema de jefes o mazmorras completo; estos serán consumidores futuros del framework, si se demuestra extensibilidad.
- Compatibilidad automática con mods de **Dusklight 1.3.1**, que usan otra plataforma/ABI.

---

## 2. Inventario de fuentes: disponible, comprobado y pendiente

### 2.1 Autoridades exactas y material histórico

**Fuentes primarias aportadas por el usuario en esta conversación y verificadas como ZIP legibles:**

1. `dusklight-2.0.3.zip` — **fuente principal única de implementación**. SHA256 `9dbdc0b068df24c3fbb680c87be25e904978f04b315e2051e3c6203476516008`. Contiene 19 861 entradas y, entre ellas, `sdk/include/mods/svc/actor.h`, `stage.h`, `resource.h`, y `mods/custom_actor_demo/`.
2. `Dusklight-v2.0.3-win32-x86_64.zip` — **distribución Windows x64 exacta de referencia**. SHA256 `ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf`. Contiene 63 entradas. Su presencia no demuestra por sí sola la compatibilidad de una DLL recién compilada.

**Material histórico opcional, NO fuente de implementación:** `dusklight-2.0.2.zip`, `Dusklight-v2.0.2-win32-x86_64.zip`, `Dusklight_2.0_CHECKPOINT_CODIGO_PREBUILD_2026-09-19.zip`, `Actor_Variant_Engine_Arquero_Escarlata_Handoff_Actualizado_LIGERO.zip` (o FULL). Consultar solo si surge una cuestión histórica concreta que no pueda resolverse en 2.0.3. AVE 1.3.1 es un diseño anterior no implementado: rescatar ideas de aislamiento por instancia, nunca offsets ni ABI antiguos. No mezclar con HM, Magic, Bars o Zora Swim.

**Acceso a Codex Cloud:** los ZIP adjuntos a ChatGPT no aparecen automáticamente en el entorno Cloud de Codex. Antes de CP00, establecer un repositorio privado y/o adjuntar el código 2.0.3 por un medio accesible a Codex; confirmar acceso mediante listado y hashes. No subir material sensible, partidas, ROMs ni contenido sin permiso. No crear ZIP adicional para el handoff.

### 2.2 Hechos verificados directamente en el ZIP fuente 2.0.3

- Existen y se pudieron leer los encabezados `sdk/include/mods/svc/actor.h`, `stage.h`, `resource.h`.
- `actor.h` declara operaciones de registro y creación de actores; `stage.h` declara `add_actor`; `mods/custom_actor_demo/src/mod.cpp` utiliza **ambas** capacidades.
- El ejemplo prueba el patrón de registro de actores personalizados, **no** demuestra que una instancia personalizada herede IA, recursos o colisiones de cualquier enemigo original.
- Los nombres, tamaños, versiones de tablas, callbacks, estructuras, semántica de carga y compilación deben extraerse **de 2.0.3** en CP00. No trasladar cifras ni firmas de 2.0.2 por suposición.
- La existencia de un SDK y un ejemplo **no demuestra todavía** que el framework, la modificación por instancia ni el render DX12 funcionen en el juego real.

### 2.3 Incógnitas específicas de CP00

- Correspondencia entre el SDK del ZIP fuente y el ejecutable del ZIP Windows 2.0.3: versión, metadatos, API, símbolos y requisitos de compilación.
- Construcción reproducible de un `.dusk` para Windows x64 usando el proyecto y toolchain oficiales, sin reconstruir todo el juego salvo necesidad justificada.
- Posibilidad de adaptar IA, animaciones, proyectiles y colisiones nativos **sin afectar a otras instancias**; comparar adaptación nativa vs actor personalizado, sin decidir antes de CP02.
- Aislamiento real de materiales/texturas y tratamiento de recursos compartidos.
- Acceso y configuración de repositorio/compilador en Codex Cloud, más flujo de transferencia a Windows para pruebas DX12.

**Puerta CP00:** si falta acceso al código fuente o binario exacto **dentro del entorno de Codex**, detenerse e indicar únicamente cómo proporcionar el recurso faltante. No sustituir silenciosamente 2.0.3 por 2.0.2 ni declarar GO sin un build verificable cuando este sea exigible.

## 3. Arquitectura propuesta (interfaces internas sujetas a CP02)

```text
DEVF .dusk
  ModEntry / Dependencies / VersionGate / Diagnostics
  ServiceAdapter (ActorService, StageService, ResourceService, HostService, UiService)
  DefinitionCatalog
    VariantSpec + AppearanceSpec + BehaviorProfile + SchemaValidation
  SpawnRegistry
    PlacementSpec + StageRoomLayerIndex + StablePlacementID
  RuntimeInstanceRegistry
    ActorID + verified identity + scene epoch + lifecycle
  VariantRuntime
    ScopedActorAdapter OR CustomActorController (decidido en CP02)
    AttributeRules / BehaviorStateMachine / AnimationAndCollisionGuards
  AppearanceController
    instance-owned material/mesh/effects; no global mutation
  Persistence
    immutable bundled presets + user placements/config in mod data_dir
  Editor (CP07; opcional para MVP)
  QA / BoundedLogging / Rollback
```

- **Mismo `.dusk` principal** para el primer framework; módulos separados dentro del código. No crear submods, SDK propio público ni `ServiceRegistry` de terceros antes de demostrar necesidad.
- Identificador de variante persistente, identificador de colocación estable y ActorID efímero son **tres conceptos distintos**.
- Si se elige usar actor original nativo, cualquier interceptación debe estar acotada a instancias DEVF y tener evidencia de ownership, reentrancia, restauración de estados, ciclo de vida y posibles conflictos con otros mods.
- Si se elige actor personalizado, reutilizar recursos oficiales del juego (animación, sonido, colisión, daño, movimiento) con APIs y ciclos de vida verificados. No inventar clases compatibles ni copiar vtables arbitrariamente.
- No instalar hooks genéricos si un servicio nativo resuelve el requisito.
- No mantener punteros a actores destruidos ni confiar solo en reutilización de ID; validar identidad, sala/capa, epoch y estado, y usar los tokens reales que el motor proporcione.
- StageService registra apariciones para **cargas de escenario**; ActorService sirve para **spawns runtime**. Elegir una autoridad por situación y evitar doble spawn.

### Ejemplo conceptual de definición (NO esquema implementado)

```json
{
  "schema_version": 1,
  "id": "scarlet_archer",
  "base_enemy": "native_bow_bulblin",
  "attributes": {"health_multiplier": 1.0},
  "behavior": {"profile": "ranged_retreat", "attack_cadence_multiplier": 1.5},
  "appearance": {"preset": "scarlet_per_instance"}
}
```

Este ejemplo **no autoriza aún** los campos: deben implementarse y validarse antes de exponerlos. El «Arquero Escarlata» del handoff de 1.3.1 es una **variante candidata futura** útil para demostrar cadencia de arco, IA de retirada y color por instancia; no queda fijado como enemigo obligatorio de la primera prueba. Se puede utilizar un enemigo más sencillo si reduce riesgo y consumo.

### Ejemplo conceptual de colocación

```json
{
  "id": "test_placement_001",
  "variant_id": "scarlet_archer",
  "stage": "STAGE_ID",
  "room": 0,
  "layer": -1,
  "position": {"x": 0, "y": 0, "z": 0},
  "rotation_y": 0,
  "respawn": "on_room_load"
}
```

`STAGE_ID` y las coordenadas son marcadores ilustrativos: **no son un lugar de prueba confirmado**.

---

## 4. Etapas y puertas de aceptación

**Política:** una etapa por tarea; entregar checkpoint y detenerse. Numeración **DEVF_CP00...DEVF_CP08**. Cada checkpoint de código debe ser un **commit/tag Git** y un handoff textual; ZIP de recuperación **solo** para artefactos descargables, compilaciones TEST, handoff a otro entorno o cuando Git no garantice acceso.

| Etapa | Resultado concreto | Modelo/esfuerzo de Codex sugerido | Condición de salida |
|---|---|---|---|
| **CP00** Fuentes y viabilidad | Inventario de 2.0.3 exacto, hashes fuente/binario, ABI/SDK/services; build mínima y estrategia evaluable | **Modelo equilibrado — Medio** | GO/NO-GO sustentado; NO avanzar solo por lectura teórica |
| **CP01** Servicios y ciclo de vida | `.dusk` DEMO aislado con actor nuevo y StageService; spawn, tick, draw, delete, cleanup | **Modelo equilibrado — Medio** | Laboratorio PASS + TEST solo si seguro; Windows DX12 pendiente hasta prueba |
| **CP02** Variante de enemigo real | Demostrar original y variante simultáneos con IA operativa, separación por instancia y seguridad | **Modelo equilibrado — Alto**; **modelo superior Medio** solo si hay bloqueo técnico real | **Puerta arquitectónica principal:** decidir nativo/adaptador vs actor personalizado |
| **CP03** Catálogo y atributos | Schema versionado, parseo validado, instancia por ID, atributos y reglas realmente soportados | **Modelo equilibrado — Medio** | Cambiar datos sin recompilar; original intacto; fallos limpios de configuración |
| **CP04** Apariencias por instancia | Dos apariencias coexistentes sin cambio global ni fuga de materiales; tamaño/efectos limitados según evidencia | **Modelo equilibrado — Medio/Alto**; Astra Medio si render es bloqueo | **Puerta visual:** GO al aislamiento; NO-GO al tintado global compartido |
| **CP05** IA/behaviors | Primera conducta no trivial, medible y extensible (p.ej. patrullar o retirada táctica), conserva reacciones nativas | **Modelo equilibrado — Medio/Alto** | Estados, colisión, animación, muerte y regresiones PASS en alcance probado |
| **CP06** Colocación persistente | Definiciones y placements stage/room/layer; reaparición y limpieza; formatos de datos y guardas | **Modelo equilibrado — Medio** | **MVP utilizable:** variantes distintas ubicadas sin recompilar entre sitios válidos |
| **CP07** Editor dentro del juego | UI de catálogo y colocación/ajuste/borrado/guardado; modo edición reversible | **Modelo equilibrado — Medio** | Editar posiciones desde el juego; confirmar actualización instantánea o al reload |
| **CP08** Endurecimiento y release | Pruebas Windows/DX12 con usuario; compatibilidad; recursos; performance; documentación; instalador | **Modelo equilibrado — Medio**, subir solo ante defecto concreto | Release únicamente cuando los requisitos y pruebas reales están demostrados |

### CP00 — Preparación y contraste (un solo turno)

**Realizar:** leer exclusivamente la fuente 2.0.3 como autoridad, hashes/revisiones de Git, SDK `actor.h`, `stage.h`, ejemplos oficiales, API de recursos y paquete nativo 2.0.3. Identificar dónde compilar un `.dusk` Windows x64 sin recompilar el juego entero; preparar repo aislado, comando de build y prueba mínima (si el entorno lo permite). Identificar rutas A/B plausibles para variantes con hechos concretos (sin repetir análisis del 2.0.2) y una propuesta de experimento de CP02. Registrar qué componentes de los archivos existentes son referencia vigente o solo historial. No usar grandes ZIP de archivos antiguos como fuente principal si existe código/SDK exacto más pequeño.

**Salida:** `DEVF_CP00_HANDOFF.md`, `SOURCES_AND_VERSIONS.md`, `SERVICE_CAPABILITIES.md`, `FEASIBILITY_DECISIONS.md`, `BUILD_ENV.md`, `GO_NO_GO.md`, commit/tag `DEVF_CP00`. **No implementar el framework completo ni adelantar CP01**.

### CP01 — Proof of life de ActorService/StageService

**Realizar:** partir de `custom_actor_demo` sin reescribir su ciclo de vida. Registrar nombre único corto, instanciar, inicializar/destruir recursos y colisión, dibujar, mover sala, quitar registros al desactivar. Probar fallo temprano y rollback; documentar si StageService no admite modificaciones inmediatas en una sala cargada. Usar solo un lugar de prueba seguro y verificado, y no sobrescribir enemigos existentes.

**Salida:** `.dusk` **TEST** solo si compila y pasa validaciones posibles; registros con IDs y operaciones acotadas; matriz PASS/FAIL/NOT_TESTED. Prueba real en Windows DX12 a cargo del usuario cuando se autorice.

### CP02 — Reutilizar un enemigo nativo

**Realizar:** evaluar rutas A/B mediante un único enemigo controlado; revisar código original del actor (constructores, perfil, recursos, AI callbacks, animación, hitboxes, proyectiles, muerte, room). Demostrar **dos instancias coexistentes**: una retail inalterada y otra DEVF con al menos un cambio real de comportamiento **por instancia**, sin contaminación y sin fallos de lifecycle. Evitar duplicar la IA completa si basta con adaptadores seguros. No registrar un reemplazo global con el nombre original. Si ninguna ruta es segura, NO-GO con evidencia y propuesta de alcance revisado.

**Salida:** decisión documentada de arquitectura, código reproducible, test de coexistencia; aprobación del usuario antes de adoptar cambios grandes.

### CP03 — Configuraciones

**Realizar:** esquema pequeño y validado, catálogo por ID, límites de tipos/rangos, logs de error claros, defaults, cambios del archivo de configuración sin recompilar mod. Verificar que el recurso empaquetado `res/` es **de solo lectura**; persistencia local por API verificada del host. Distinguir valores estéticos, atributos nativos soportados y opciones que requieren nuevos adaptadores. Control de colisiones, vida, muerte, drops y estado por instancia.

**Salida:** dos presets/configuraciones válidos, una inválida rechazada sin crash, pruebas de recarga con proceso nuevo.

### CP04 — Apariencias

**Realizar:** demostrar aislamiento en materiales/modelos en **dos variantes de la misma especie simultáneas**, una retail. Tinte global de textura compartida es insuficiente. Auditar recursos de J3D/material/render y restauración por instancia; comprobar compatibilidad con efectos nativos, efectos de iluminación, freeze y culling. Primero reutilizar recursos; importar modelos y animaciones únicos es capacidad **posterior y condicionada al pipeline**.

**Salida:** evidencia visual Windows/DX12 y datos de que la apariencia no cambia a otras instancias; documentación de límites.

### CP05 — Conducta no trivial

**Realizar:** primera FSM con comportamiento verdaderamente diferente (por ejemplo, un arquero que modifica cadencia y se retira de Link, si CP02 confirma animación/AI compatibles). Estados interrumpibles por muerte, daño, stun, cinemáticas y habilidades externas. Validar suelo/obstáculos, persecución, disparos, cooldowns, ownership de proyectiles y retorno a vanilla. IA especial solo cuando el actor pertenece a DEVF.

**Salida:** pruebas de juego/mocks pertinentes, métricas simples de frecuencia de ataques y estados, sin teleport/deslizamientos.

### CP06 — Spawns y placements utilizables

**Realizar:** leer placements por stage/room/layer, aplicar `StageService::add_actor` al cargar cuando corresponda, y `ActorService::create_actor` para spawns manuales de QA, con política clara anti-duplicado. Validar separación por scene epoch, actorID, room, layer y placementID. Persistir colocaciones del usuario de manera externa y segura; fallar limpiamente ante escenas incompatibles. Incluir import/export legible de configuraciones.

**Salida:** colocar dos variantes distintas en dos zonas verificadas, reproducirlas tras cambio de zona y reinicio, quitar una colocación y no reaparecer; **MVP listo para uso experimental**.

### CP07 — Editor en el juego

**Realizar:** utilizar UiService/API 2.0.3 confirmadas; listar variaciones y escena actual; crear/editar/borrar placements, ajustar Y y rotación; control de recursos y validación; guardado atómico y reversión. No introducir hooks globales de input o HUD si UI ya permite hacerlo. Distinguir preview/no preview según seguridad del spawn en sala cargada.

**Salida:** flujo completo sin editar JSON, incluyendo reinicio y conservación de ubicaciones. Si UiService resulta insuficiente, ofrecer editor reducido; no bloquear CP06 por ello.

### CP08 — Estabilización

**Realizar:** matriz de niveles/salas, cambio de capa, entrada/salida, teletransporte, muerte, save/load, eventos y cinemáticas, >1 variante, fallbacks; FPS/frametimes/RAM/logs; seguridad al habilitar/deshabilitar según servicios, con reinicio de proceso si las dependencias/hook lifetimes lo requieren. Compatibilidad con mods 2.x presentes **solo cuando sus versiones y código estén realmente disponibles**. Reproducción limpia desde repo/tag. No certificar ejecución DX12 sin log/prueba del usuario.

**Salida:** `.dusk` estable y guía de rollback **solo si** todos los bloqueadores de seguridad resueltos. Si no, `DEVF_BLOCKED_HANDOFF.md` y última versión TEST recuperable.

---

## 5. Matriz de QA transversal (cada etapa ejecuta únicamente lo que le corresponde)

| Área | Caso de prueba/criterio |
|---|---|
| Compatibilidad | Versiones de host, SDK y servicios; rechazo claro si no compatibles |
| Identidad | Enemigo retail original no cambia cuando existe una variante |
| Instancias | Dos o más variantes simultáneas, parámetros distintos, sin fuga de estado |
| Creación | Solicitud vs creación concluida; recursos cargados, errores tratados |
| Combate | Hitboxes, invulnerabilidad, daño, muertes, drops, animaciones y proyectiles coherentes |
| AI | Patrulla, pausa, pursuit/retreat, daño, stun, pérdida de objetivo, muerte |
| Gráficos | Material/tinte/modelo por instancia sin contaminación, iluminación y culling |
| Escenarios | Stage/room/layer exactos, límites, rooms incompatibles, eventos originales |
| Persistencia | Recarga escena, reinicio de juego, borrar placement, identidades durables |
| Seguridad | Desregistro/rollback, scene unload, callbacks, punteros, reentrancia y conflictos |
| Rendimiento | Medir variación de frametime/FPS y RAM frente a baseline; límite razonable de enemigos simultáneos configurable; hardware Intel UHD/8 GB como referencia |
| Compatibilidad mods | No interferir con otros `.dusk`; no suponer que los mods 1.3.1 ya están portados |
| Plataforma | Construcción Win64; pruebas reales Dusklight 2.0.3 + DX12 **separadas** de laboratorio Linux |

No inventar umbrales de FPS universales; tomar baseline y presupuesto acordado antes de calificar PASS de rendimiento. Registrar errores de forma acotada para no saturar logs. Ante crash, detener ejecución real y conservar log/checkpoint.

---

## 6. Selección de modelo y economía de usos de Codex

**Configuración inicial recomendada si está disponible en el selector de Codex:** **modelo equilibrado disponible en Codex, razonamiento MEDIO, modo estándar**. El esfuerzo `medium` es la preferencia operativa; **no se garantiza su disponibilidad en la cuenta/versión específica de Codex**. Leer el selector antes de fijar un nombre. Si no está, usar el modelo equilibrado disponible y conservar el mismo criterio de esfuerzo.

**Cambios de modo justificados:**

- **Modelo equilibrado MEDIO**: CP00, CP01, CP03, CP06, CP07, CP08, y la mayoría de cambios ordinarios.
- **Modelo equilibrado ALTO**: análisis de IA nativa específico CP02, render/materiales CP04 o FSM compleja CP05 cuando Medio deje un problema concreto sin resolver; no dejarlo en Alto por defecto para todo el proyecto.
- **Astra MEDIO**: excepcionalmente, bloqueo técnicamente demostrado en arquitectura de actores, lifecycle difícil, render de materiales o crash. Enviar a Astra **solo una pregunta delimitada con código, trazas y resultados**; devolver la implementación ordinaria a Sol después.
- **Luna BAJO/MEDIO**, si está disponible: documentación mecánica, schema/lint, empaquetado y resúmenes, **sin** delegarle decisiones de ABI o hooks riesgosos.
- No activar modos Pro/Max/Extra High/Ultrafast/varios agentes por rutina; no asumir que mayor velocidad equivale a menor coste.

**Reglas anti-desperdicio:**

1. **Una etapa = una tarea = un alcance finito**. No adelantar etapas, ni crear múltiples PR simultáneas sin permiso.
2. **Leer primero el repo existente, los checkpoints y el SDK**. Nunca recuperar/investigar lo ya resuelto.
3. Consultar fuentes precisas, no descomprimir o analizar repetidamente cientos de MB si solo cambió un header.
4. Usar tests dirigidos y build incremental; suites amplias **solo** tras cambios transversales o gates mayores.
5. Checkpoint Git por etapa y `RESUME_INSTRUCTIONS.md` corto; sin ZIP redundante de dependencias enormes.
6. No generar informes interminables repetidos ni modelos paralelos sin una pregunta precisa.
7. Registrar FAIL como FAIL, bloqueo como NO-GO, hipótesis como hipótesis; **nunca declarar prueba Windows ejecutada en Cloud/Linux**.
8. Para errores complejos: reproducir → minimizar → obtener log/traza → investigar → corregir → regresión → detenerse. No generar «soluciones» sucesivas a ciegas.
9. Limitar salida de consola/logs y evitar adjuntar binarios gigantes en cada turno.
10. Separar DEVF del proyecto HM/Bars/Magic en Dusklight 1.3.1; no consumir usos reabriendo esos proyectos.

**Cloud vs WSL:** preferir Cloud para análisis/compilación grandes, considerando que el usuario dispone de ~8 GB RAM y ya usa WSL con Claude/Codex; Windows local para pruebas DX12. Codex Cloud requiere **un entorno con repositorio y dependencias accesibles**, no hereda automáticamente la biblioteca de ChatGPT. Su consumo cuenta según plan/cuota: **Cloud no equivale a usos gratis**.

---

## 7. Reglas de integridad, checkpoints y reversión

- Mantener repo separado: nombre sugerido `dusklight-enemy-variant-framework`; Git con historial y tags `DEVF_CP00`, `DEVF_CP01`, etc. No fijar rutas locales que no se hayan comprobado.
- Entregables mínimos por etapa: `HANDOFF_CPXX.md`, `CHANGES.md` o diff Git, `TEST_RESULTS.md` (PASS/FAIL/NOT_TESTED), `GO_NO_GO.md`, `RESUME_INSTRUCTIONS.md`, commit/tag, información de versiones/compilación y hashes para binarios producidos.
- Test `.dusk` nuevo solo después de pasar comprobaciones de compilación y compatibilidad; no instalar sin instrucciones y copia anterior.
- No modificar EXE, ROM, partidas, ni otros mods. No borrar archivos originales; solo crear y versionar archivos DEVF.
- Evitar dependencias de servicios que no estén realmente en el SDK/host; respetar versiones de API, imports y manejo de errores.
- No parchear código del motor si ActorService/StageService cumplen el objetivo. Hooks adicionales requieren evidencia y autorización según riesgo.
- No considerar una prueba sintética de actores como prueba del render, comportamiento ni la colisión real en Windows/DX12.
- Procesos nuevos para tests cuando estado/hook/unload no estén certificados como hot-reload safe.

---

## 8. Decisiones pospuestas conscientemente

1. **Primer enemigo de demostración:** no está fijado todavía. Probar el más simple que permita demostrar reutilización de IA y apariencia aislada; `Arquero Escarlata` (Bulblin arquero rojo, disparo más frecuente y retirada táctica) es candidato respaldado por el handoff histórico, no requisito impuesto.
2. **Nativo adaptado o actor totalmente personalizado:** **se decide al terminar CP02 con evidencia**.
3. **Qué comportamientos son presets de datos y cuáles requieren C++ adicional:** determinar con los adaptadores probados; no prometer «cualquier comportamiento» sin código.
4. **Modelos externos y animaciones originales:** extensibilidad futura; validar pipeline antes de garantizar compatibilidad.
5. **Respawn persistente por partida, drop especial, bosses, cuevas y mazmorras:** extensiones futuras, no bloquear MVP.
6. **Editor 3D avanzado:** CP07 entrega UI funcional mínima; manipulador gizmo 3D solo si se justifica.
7. **Publicación de API pública para otros mods:** después de tener un framework v1 realmente estable; no arquitectura prematura.

---

## 9. Instrucciones para el siguiente operador / Codex

Al recibir este handoff:

1. **No ejecutar todavía CP00** hasta que el usuario envíe el prompt específico de inicio.
2. Leer únicamente las referencias relevantes y confirmar acceso real a ellas. Si Codex Cloud no dispone de la fuente y distribución exactas 2.0.3, solicitar el repositorio/archivo mínimo necesario: **no inventar acceso a la biblioteca de ChatGPT**.
3. Tratar **únicamente** la fuente **2.0.3 exacta** como autoridad para compilar; la fuente **2.0.2** solo como referencia histórica excepcional; el AVE 1.3.1 como antecedente conceptual sin código portable.
4. Implementar **solo CP00** en el primer encargo; entregar estado honesto GO/NO-GO y detenerse.
5. Cuando el usuario apruebe CP01, continuar secuencialmente respetando gates y configuración de modelos económicos.
6. Preparar cada TEST de Windows para **Dusklight 2.0.3 DX12**, sin presumir capacidad de ejecutar DX12 en Codex Cloud.
7. Mantener prioridad máxima: **no romper el juego ni las instancias retail**. Progreso reproducible por encima de demos apresuradas.

### Fuentes públicas orientativas (revalidar en la versión exacta)

- Repositorio/SDK Dusklight: https://github.com/TwilitRealm/dusklight
- Guía de modding y servicios: https://github.com/TwilitRealm/dusklight/blob/main/docs/modding.md
- Ejemplo del código fuente **2.0.3**: `mods/custom_actor_demo/` dentro de `dusklight-2.0.3.zip`.
- Guía oficial de Codex Cloud: https://help.openai.com/es-es/articles/20001545-using-codex-cloud

---

**Fin del handoff.** Siguiente acción autorizable: el usuario pedirá el **prompt específico para CP00**. Ninguna otra etapa debe iniciarse automáticamente.
