# Primer eslabón: observabilidad y pérdida de procedencia

Método único: observar el límite nativo **register_edit** en Dusklight40457c6…, sin inspeccionar contenedores internos ni modificar host. No se investigan cinco fábricas alternativas ni se repite sitio2.

## Cadena fijada por fuente
1. StageService.add_actor(ctx,…,out_handle) valida contexto y llama stage_add_actor con LoadedMod& (stage.cpp270–288).
2. stage_add_actor189–198 construye ActorEditRecord temporal y copia los bytes de entrada a su vector.
3. register_edit158–165 recibe **LoadedMod&, const char*, ActorEditRecord&&, uint64_t&**; fija handle/mod/seq, escribe outHandle y mueve al almacén.
4. stage_create_new_actors139–154 entrega sólo user, record.data(), size. El buffer del mod ya no es el buffer enumerado.
5. La ruta dStage de enemigo copia a objeto local/append; la ruta Link enumera sin crear. La solicitud nativa puede devolver ID, pero no recupera por sí misma owner/handle.

La existencia/ABI de la entrada se mide contra el EXE en SYMBOL_AND_ABI.md y evidence/. El paso3→4 es el gate de propiedad, no un problema de comparar dos XYZ.

## Qué puede observarse sin layout privado
- Una referencia LoadedMod& da una identidad opaca durante el scope, sin leer campos.
- La referencia outHandle permite leer el valor producido al regresar, validando retorno y contexto; no confundir handle con ActorId.
- La dirección del ActorEditRecord&& identifica el **objeto temporal**, no su buffer. En PRE aún no se asignaron handle/mod; en POST el objeto ya se movió al almacén.
- stage y el buffer externo pertenecen al caller: no son tokens del vector interno copiado.
- Ninguna de esas operaciones entrega por contrato record.data() del Add almacenado.

## Por qué no se implementa un hook de correlación
Para asociar el primer buffer enumerado con aquel handle haría falta (a) leer el vector privado del ActorEditRecord o el almacén s_edits, o (b) usar bytes/posición/orden/primera aparición como sustituto. Ambas opciones están excluidas para este método. Instalar un hook cuya salida no puede sustentar identidad sólo añade riesgo sin cerrar P2.

El movimiento de un vector puede conservar su allocation en condiciones estándar; **no proporciona un accessor seguro desde un objeto opaco**. Tampoco convierte la dirección del temporal en dirección de allocation. No se presupone layout MSVC STL, allocator, offset, memoria movida o contenido del objeto tras move. La dirección del caller-temporal no puede conservarse después de terminar stage_add_actor.
Aun si se lograse leer el buffer, remove/erase, fallo/cancelación y detach requerirían invalidaciones; append se libera al completar creación. No se almacenó ninguna referencia/puntero nativo en un nuevo core.

## Dos dueños y records idénticos: obligación no satisfecha
Desde las salidas públicas el mod conoce su handle; el callback de enumeración entrega direcciones de allocations internas sin etiqueta de owner/handle. Permutar el propietario de dos Add con el mismo record no cambia sus bytes/posición/perfil. Un ordinal de callback no resuelve esta equivalencia; una dirección de allocation distingue allocations, pero no demuestra cuál pertenece al handle.
Ésta es una prueba de insuficiencia de **estos observables**, no una ejecución de dos actores ni imposibilidad universal. No se inventa una traza A→ActorIdA/B→ActorIdB ni se ejecuta un fake para certificarla.

## Resultado por eslabón
owner/context→handle: conocido por la propia llamada de servicio, sin layout de LoadedMod.
handle→allocation interna: **NO_GO para el método de hook opaco elegido**.
allocation→scope enemigo→request→ActorId: NOT_RUN como implementación, condicionado al eslabón anterior.
epoch/generación/cancelación/reciclado: diseño y pruebas P3 NOT_RUN; admission_epoch previo no se eleva a scene epoch.
