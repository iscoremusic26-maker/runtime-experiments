# Recuperación de la revisión estratégica

Base exacta y único padre previsto: `4276a0562eb156d04569be38b5cc2dc987cd074a`, tag `DEVF_CP01_G4_FINAL_STATIC_REVIEW`, rama histórica `review/devf-cp01-g4-final-static-review`, PR10 draft sin merge. Su tag es anotado: comparar `^{commit}`, no el hash del objeto tag.

Rama nueva: `review/devf-cp01-first-spawn-strategy`. Tag nuevo: `DEVF_CP01_FIRST_SPAWN_STRATEGY_REVIEW`. PR draft contra la rama base; sin merge, force-push ni cambios de referencias históricas. SHA de entrega reproducible mediante `git rev-parse DEVF_CP01_FIRST_SPAWN_STRATEGY_REVIEW^{commit}` y el enlace de commit de la entrega.

Solo cinco documentos propios en esta carpeta. Sin código activo, interfaces implementadas, pruebas ejecutadas, workflows, DLL/.dusk/EXE, recursos privados o raw logs. DISARMED_NO_REGISTRATION intacto. Publicación documental con `[skip ci]`; no ejecutar compilaciones o suites anteriores.

## Evidencia preservada y reutilizada

- Auditoría previa: los seis informes de [CP01_DAWNLIGHT_AUDIT](../CP01_DAWNLIGHT_AUDIT/RECOVERY.md), incluyendo semántica de capas, request y límites de sus pruebas. Su manifiesto de procedencia contiene hashes de fuentes; no se recalculó inventario/SDK.
- Fuente oficial limpia Dusklight2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Dawnlight `9bb214d47617c9bc295d22facf36c35d17661e5a` / v4.0.3; CMake default host2.0.0, resultados externos no asumidos2.0.3.
- G2: reader y seguridad de punteros/room node/capas, enlace y laboratorio históricos; sesión28 capturas, log privado2182 líneas y hash anonimizado conservados. No reconstruir ni publicar sus28 capturas/log. G2 limitado con otros mods activos, no sesión limpia.
- [G4 final](../CP01_G4_FINAL_STATIC_REVIEW/RECOVERY.md): recursos, cotas401/494/501,182 poses,31prismas, overlays0, movimiento y límites sociales, RTBL/SCLS,16+98 puntos. No recalculados ni promovidos a PASS nuevo.
- Baselines/arquitectura SDK anteriores e historia desde545b2d1 preservados. No parche de host ni integración del experimento lifetime.

## Hallazgos de esta revisión: alcance exacto

Lectura focalizada de los seis archivos Dawnlight solicitados, no reauditoría. Contraste únicamente decisivo de E_OC Create/searchPlayer2/perfil, ActorService/fopAcM_create/request, registro de capas, orden `fapGm_Execute` y resolver público ya existente en G2. Fuentes externas permanecen fuera del repo.

1. FFFFFFFF y00FF0000 dan modo0/búsquedaS/switch derrotaFF; difieren en switch secundarioFF/0. Modelo/rango los decide angle.x: DEVF FF14 conserva E_OC/rango2000 frente al X0 de Dawnlight. No hay ventaja acreditada para cambiar preset.
2. A2 con capa hija ROOM_SCENE ofrece solicitud identificada sin edición ni recarga natural. Scope oficial captura owner antes de fases, restaura caller sin rollback. Tick precede management en host original; sin hooks/callbacks propios el enqueue no ejecuta Create síncronamente. No se ha certificado ejecución de este nuevo consumidor.
3. G2 ya resuelve públicamente node y child layer; reaprovechar su validación sin IDs/pointers cacheados. Elegir Link owner o cualquier no-root por sí solo sería insuficiente.
4. Universalidad de navegación/progreso/censo y ciclo natural A1 no son gates universales para una sola sesión A2. Owner válido, rechazo de teardown, punto local admitido, binario revisado y cierre conservador sí continúan imprescindibles.

## Decisión y estado

| Elemento | Estado |
|---|---|
| Revisión y contrato estático | PASS_STATIC en alcance documental; recomendación **RECOMMEND_A2** |
| Consumidor A2 específico / link / lab / scope real | NOT_VERIFIED / NOT_TESTED |
| Punto de aparición | NO_SAFE_POSITION_VERIFIED; XYZ no asignado |
| G2 | PASS_RUNTIME_OBSERVED limitado, histórico |
| G4 | G4_RESOURCE_VERIFIED_POSITION_BLOCKED, histórico intacto |
| G5 | NO-GO; sin paquete ni prueba autorizada |
| G6 | NOT_VERIFIED / NOT_TESTED |
| CP02 | NO-GO |
| Perfiles personalizados/descarga DLL | BLOCKED independiente, no reauditar |

Próximo paso mínimo **solo después de aprobar estrategia y autorizar nueva tarea**: adaptar el resolver G2 a un controlador A2 desarmado, scope/latch/tracking propio y guards de node/escena/transición; revisión independiente, link MSVC/SDK y lab dirigido. No nuevos ARC, SDK completo, host build, geometría universal o ciclo natural obligatorio. Luego admitir un punto y condiciones locales antes de preparar activo; runtime requiere autorización expresa separada.

## Recuperar y verificar sin sobrescribir trabajo

```bash
git init work/devf-strategy-recovered
git -C work/devf-strategy-recovered remote add origin https://github.com/iscoremusic26-maker/Mods-Duskligh.git
git -C work/devf-strategy-recovered fetch origin refs/heads/review/devf-cp01-first-spawn-strategy:refs/remotes/origin/strategy refs/tags/DEVF_CP01_FIRST_SPAWN_STRATEGY_REVIEW:refs/tags/DEVF_CP01_FIRST_SPAWN_STRATEGY_REVIEW
git -C work/devf-strategy-recovered switch --detach DEVF_CP01_FIRST_SPAWN_STRATEGY_REVIEW
git -C work/devf-strategy-recovered rev-parse HEAD
git -C work/devf-strategy-recovered rev-parse HEAD^
git -C work/devf-strategy-recovered diff --name-only 4276a0562eb156d04569be38b5cc2dc987cd074a HEAD
git -C work/devf-strategy-recovered status --short
```

Padre debe ser4276a056…; diff solo los cinco Markdown de esta carpeta; árbol limpio. La entrega comprueba además recuperación por fetch a un bare independiente, igualdad de blobs, rama/tag y referencias históricas. Ninguna recuperación autoriza runtime. Reversión documental: seleccionar base detached en copia separada, sin reset/merge sobre historia compartida.

La tarea se detiene después de publicación y comprobación de recuperación. Aprobar RECOMMEND_A2 no aprueba G4/G5 ni instala/ejecuta nada.
