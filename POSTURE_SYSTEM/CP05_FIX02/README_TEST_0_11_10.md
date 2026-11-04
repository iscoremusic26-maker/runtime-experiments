# Light Fades Twice 0.11.10 — CP05 FIX02 PRIVATE TEST

P0-A (tambaleo de espada ordinaria por debajo de 100) y P0-B (rebote repetido por contacto antiguo ante guardia sostenida): **SOURCE_IMPLEMENTED / SOURCE_AUDIT_PASS / LAB_PASS / WINDOWS_MSVC_PASS / PE_AUDIT_PASS / INDEPENDENT_DOWNLOAD_PASS / ARTIFACT_DOWNLOADED_VERIFIED**. Ambos siguen **HUMAN_RUNTIME_PENDING** en Windows/DX12. No es certificación visual ni de coexistencia real de ocho mods.

[Descargar artifact privado 13338164623](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41856406121/artifacts/13338164623) · [CI 41856406121](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41856406121)

`LIGHT_FADES_TWICE_CP05_FIX02_0_11_10_PRIVATE_TEST_windows-amd64_d6e4c2179c2c.dusk`

**169147 bytes** · ID `dev.posture.post05_selective_reactions` · **0.11.10** · Windows x64 / DX12 / PRIVATE TEST.

SHA-256 del `.dusk`: `9c8f0074962386d7f46984cab43c0cff8fb429911d731e846aa52bef44e4bb4f`.

SHA-256 DLL interna: `5d9fef1e46e9e18fb5c4a49acc4c26758078909bdb7343e1005a5b19cfc45049`.

Caducidad informada por GitHub: **2026-12-04 10:38:41 Panamá (UTC−5)** (`2026-12-04T15:38:41Z`). Guardar el `.dusk` antes de caducar.

Fuente compilada `d6e4c2179c2c42a7aa807ce862290de728abb396`, árbol `47562231f0dc9c05075ef784cb064a7dd233c6f9`; commit CI `6f7ef784cde3cd1ee17511af863eaf5614aca9b0`. Este informe pertenece a un commit documental posterior y separado: su SHA se consulta en el historial de la rama; no se atribuye al binario. Base compilada FIX01 `785f7044a09588ea9f570f09b4b74580e4f7ee93`, no su commit documental `cf1cf30eacf2bee7db37bd03bd49f82c6d6d57b7`.

Jobs **build SUCCESS** e **independent-download SUCCESS**, mismo run. Paquete descargado de nuevo en esta sesión: CRC, SHA, DLL, manifiesto, fuente y PE coinciden. No se ejecutó el juego ni se cargó la DLL.


## Qué cambia

La continuidad de POST05 admite finales nativos B/C y recoil detenido solo con BCK, límites, isStop, PRE/POST, identidad y lectura actual verificados. Conserva el daño HP y la postura; no restaura vida. Mantiene muerte, ruptura a 100, Finish y prioridades legítimas.

Al recibir contacto fresco auténtico de Link se solicita la limpieza mediante el lease existente de registro `cc_set`, también después de un bloqueo ordinario. El motor limpia el contacto anterior; los bits AT se restauran antes de su pasada de colisión. No fuerza ataques ni cambia R, parry, tiempos, IA ajena o animaciones. Incluye comprobación ABI aun si ese es el primer bloqueo antes de cualquier espadazo/parry.

## Instalar y probar en unos cinco minutos

1. Descargar el ZIP del artifact y extraer el único `.dusk`; el SHA indicado corresponde a ese `.dusk`, no al ZIP exterior. Cerrar el juego. Guardar el `.dusk` anterior fuera de la carpeta activa. Sustituir **solo Light Fades Twice**, mismo ID; dejar una única versión activa. No instalar la DLL interna por separado.
2. **Prueba B prioritaria:** conservar intactos los otros siete mods de los logs: Enemy Variant Framework 0.15.0; Bokoblin Expansion 0.17.0; Enemy Health Bars 2.0.3 CP06 Armos TEST; Enemy Health Multiplier 2.0.3 CP11 arrow-route TEST; Zora Swim 1.3.0; Luau Support 1.0.0; Dusklight Randomizer 1.0.6. No tocar sus archivos, opciones o partidas para atribuir un cambio al FIX02.
3. Dar varios espadazos ordinarios a Red con postura <100, especialmente durante recoil y final B/C. HP debe bajar y postura subir sin tambaleo prematuro. Repetir con Blue, Black normal y Black furia. Separar muerte, 100 y Finish de ese defecto.
4. A rango de ataque, mantener R frente a Blue y Red unos 20–30 segundos y comparar soltando R en situación equivalente. Repetir Black, uno y varios enemigos si están disponibles. Deben conservar pausas naturales y volver a atacar sin necesitar soltar R. Probar después de un espadazo y de un parry auténtico; no esperar persecución/ataque si no hay target o rango válido.
5. Comprobar Blue2+2, Red4, Black8 y Black7. Cada parry requiere R+B nuevo y un movimiento físico de Shield Attack, contacto, chispa y sonido nativos propios. Mantener R solo nunca cuenta como parry.
6. Permitir postura 100/remate, probar guard-break de Link/rearme y cambiar de sala/pausar. Verificar barra Link/enemigos y Scoop/Talk/Open como antes. Cerrar normalmente para conservar `SHUTDOWN`. Anotar variante, momento y síntoma si falla; vídeo opcional, no requisito.

**Prueba A aislada**, separada de B y con el juego cerrado al cambiar: solo FIX02. Sirve para arranque, degradación y rutas nativas compatibles. No valida patrones Red/Black de Expansion, cuya clasificación no existe sin esa dependencia. Ninguna de A/B se ejecutó en esta sesión.

## Verificación técnica

22 laboratorios MSVC y **4.486.668 comprobaciones**; se conservan los 21 laboratorios heredados y sus 4.272.615 comprobaciones. FIX02 aporta 214.053 del núcleo; además, integración nativa: 2.656, y guardia/colisión: 57.184, contadas por separado. **550/550 mutaciones**: 525 heredadas +25 nuevas, sin TIMEOUT. Negativos de fuente nuevos: 18/18; PE: 20/20; instrucciones: 6. Imports del juego: 63; targets: 24; contratos de servicio: 7. Sin nuevos targets ni escritores nativos. Detalle y límites en [VALIDATION.json](VALIDATION.json), [RESULTS.json](RESULTS.json) e [IMPLEMENTATION.md](IMPLEMENTATION.md).

Las pruebas ejecutan cuerpos auténticos del motor y callbacks de producción, con I/O, poses, contactos, control de animación y render modelados. No equivalen a una partida, medición FPS ni observación de escudo/chispa/sonido.

## Rollback

Con juego cerrado, retirar únicamente FIX02 e instalar una sola versión previa del mismo ID; conservar los siete mods. **CP04 0.11.7** es la última base jugable global aprobada: [artifact13283289812](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41746570392/artifacts/13283289812), 147197 bytes, SHA-256 `e446ed3ee1111837a9feed628adf939942a006e60913fe66b00d48986b71826e`. Su copia local verificada se conservó. Mantiene su fecha de expiración original de GitHub, 2026-12-03 19:40:20 Panamá.

FIX01 **0.11.9** es alternativa de diagnóstico con combos humanos confirmados pero los dos defectos reportados; no está globalmente aprobada: [artifact13302951716](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41787837430/artifacts/13302951716), 163257 bytes, SHA-256 `875e049ebb76f2deee50e7d2c62d73f3fe762d1f936925b4d008648b11cad4e6`. No volver a 0.11.8 defectuosa ni activar dos Light Fades Twice.

No se realizaron PR, merge, tag ni release. Los otros siete mods, host, SDK, EXE, ROM y saves permanecen intactos.
