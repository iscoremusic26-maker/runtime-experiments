# Prueba humana posterior — Windows x64, Dusklight 2.0.3, DX12

El paquete tiene BUILD_PASS, PACKAGE_VERIFIED y DOWNLOAD_VERIFIED. La ejecución requiere tu aprobación y se realiza manualmente en tu PC; Codex no instala ni ejecuta el juego.

1. Cierra completamente Dusklight y respalda saves/configuración. Verifica el EXE con `Get-FileHash -Algorithm SHA256`: debe dar `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`. Si difiere, detente: otra build puede cambiar ABI/inlining.
2. Retira temporalmente CP01, CP02, G5 y otros DEVF, además de mods de enemigos, stages, HP o hooks. Conserva sus archivos. Descarga el [TEST privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38513406897/artifacts/11870393231), extrae y verifica el `.dusk` de 8953 bytes, SHA256 `5754a47e84d56563cfb4143139aa0f4660b6852ce409e30b84fd398b0cfe3229`. Instala solo ese `.dusk`, no ZIP ni DLL suelta.
3. Inicia el ejecutable oficial intacto con DirectX12 y entra naturalmente a F_SP121, sala 3, capa 6, en el punto del puente hacia Kakariko ya probado en CP02. Sin teleport, flags, hot reload o edición de saves.
4. Conserva el log. Debe aparecer EDIT_REGISTERED y **una HP_APPLIED por instancia**: old_hp=220, new_hp=150, phase=PRE_FIRST_EXECUTE, evidence=FIELD_READBACK. Esa lectura acredita el campo propio en ese instante; no render, combate o HP máximo. Sin HP_APPLIED no hay PASS numérico.
5. Observa un único Bokoblin adicional con animaciones, recursos, efectos y combate normales. Tras daño no debe haber otra HP_APPLIED para ese ID ni reinicio de HP por frame. Comprueba un enemigo original como control negativo. No uses golpes o barra como medición directa de 150.
6. Detén ante HP_REJECTED, error de inicialización, target unresolved/inlined, warning del backend, modelo ausente, duplicado, curación, crash o alteración de otros enemigos. Cierra por completo y conserva evidencia privada; no intentes arreglarlo con hot reload.
7. Si la primera prueba es normal, una salida/entrada natural de sala puede generar nueva instancia/ID y una nueva HP_APPLIED. Nunca deben existir dos instancias coincidentes vivas sin rechazo. Sigue pendiente de prueba humana.
8. Reversión: cierra completamente, retira CP03, reinicia y vuelve naturalmente. Debe faltar el adicional. Desactivar en un proceso abierto no promete eliminar un actor vivo. Restaura mods previos solo en otra sesión sin CP03.

Una comparación opcional CP02/CP03 requiere procesos completos separados y la misma arma; no acredita daño multiplicado. Devuelve log anonimizado y observaciones de aparición, HP, daño sin reset, control original y retirada. No publiques logs personales. CP03 no será PASS_RUNTIME ni estable hasta revisar esa evidencia; no se inicia CP04.
