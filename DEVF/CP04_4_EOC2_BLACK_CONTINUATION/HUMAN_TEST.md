# CP04.4 — Prueba humana privada Windows/DX12

**TEST offline verificado; HUMAN_RUNTIME_NOT_TESTED.** No lo ejecutó Codex. APPLIED sólo confirma la palabra privada del comando y el cierre lógico del scope.

1. Cerrar completamente Dusklight. Respaldar saves por el usuario. Comprobar EXE oficialSHA `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`, versión2.0.3, D3D12. No Vulkan/hot reload.
2. Apartar del directorio de mods los .dusk DEVF CP03/CP04.x anteriores y cualquier mod/reemplazo de modelo/material/texel que interfiera. El nuevo paquete ya incluye aparición/HP150/telemetría CP03: **no combinar ambos**, para evitar registros duplicados.
3. Descargar [ZIP privado TEST](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492/artifacts/11936739368), extraerlo fuera de la instalación y verificar `SHA256SUMS.txt`. Copiar **sólo** `DEVF_CP04_4_EOC2_BLACK_windows-amd64_ee42f62d2bd2bbbfae9e61affb10c066fd0588af.dusk` al mismo directorio oficial de mods utilizado para CP03. No instalar SOURCE_COMPILED.zip ni la DLL suelta; no editar archivos originales.
4. Entrar F_SP121/room3/layer6. Observar exactamente el E_OC2 adicional del home(-1250,-6304.00830078125,60750): cuerpo negro carbón con textura/volumen/luces, ojos originales y arma original. Registrar log y captura. Debe haber HP_APPLIED220→150 una vez, CP04_BLACK_PREFLIGHT→READY→APPLIED de ese ActorId/generación. No basta APPLIED para confirmar píxeles.
5. Comparar con un **E_OC2 ORIGINAL del mismo modelo**, preferentemente ambos en el mismo frame. E_OC normal40HP no es control válido. Si no hay original disponible/visible, dejar ese control PENDIENTE; no crear otro actor ni modificar flags para fabricarlo.
6. Ante rechazo/desactivación, contaminación, glitch o crash: detener, cerrar y conservar log/captura privados/anonimizados; no seguir combate. Si apariencia/control estables, probar golpes/150HP, animaciones/efectos, muerte, salir/reentrar, una generación nueva y sin residuos. Los RELEASED no son prueba de GPU por sí solos.
7. Rollback con cierre completo: quitar **sólo** el nuevo .dusk y reabrir. Comprobar ausencia del adicional y originales intactos; no editar saves/flags/escena. Los archivos antiguos apartados pueden restaurarse únicamente con el juego cerrado; no mezclar versiones.

```powershell
(Get-FileHash -LiteralPath '.\DEVF_CP04_4_EOC2_BLACK_windows-amd64_ee42f62d2bd2bbbfae9e61affb10c066fd0588af.dusk' -Algorithm SHA256).Hash
```

Esperado .dusk:15287 bytes/SHA `a1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9`.
Artifact vence 2026-11-13 18:59:41 (Panamá, UTC−05:00). Tras vencer, no reconstruir/sustituir el paquete histórico CP03; recuperar este código/tag y preparar sólo una entrega nueva CP04.4 con nueva evidencia si fuese necesario.

Aceptación final sólo con LOG + confirmación visual del usuario. Quedan pendientes estética/sRGB/fog, ojos/arma en esta instalación, original E_OC2 mismo frame, combate, muerte, reentrada y reversión. No se activa nada en la PC del usuario automáticamente. No avanzar CP05/06.
