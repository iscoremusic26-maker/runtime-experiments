# Light Fades Twice 0.11.9 — CP05 FIX01 PRIVATE TEST

Candidato acumulativo para Dusklight 2.0.3 Windows x64/DX12. ID `dev.posture.post05_selective_reactions`. Corrige la cancelación prematura ante contactos de escudo resueltos sin daño, la continuación nativa entre swings y el exceso de pausa CP05. Introduce velocidades por golpe limitadas a1/1.15 y conserva el RNG. Blue, parry, postura, Link y HUD previos permanecen congelados.

**No está aprobado jugablemente:** HUMAN_RUNTIME_PENDING. La 0.11.8 anterior fue rechazada por el log humano; sus pruebas técnicas no certificaron la partida. Consulte [diagnóstico y límites](IMPLEMENTATION.md) y [resultados verificables](RESULTS.json).

## Paquete verificado

[Descargar artifact privado 13302951716](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41787837430/artifacts/13302951716) · [CI 41787837430](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41787837430), build e independent-download SUCCESS.

`LIGHT_FADES_TWICE_CP05_FIX01_0_11_9_PRIVATE_TEST_windows-amd64_785f7044a095.dusk`

**163257 bytes**. SHA-256:

`875e049ebb76f2deee50e7d2c62d73f3fe762d1f936925b4d008648b11cad4e6`

Fuente compilada `785f7044a09588ea9f570f09b4b74580e4f7ee93`; CI `ef57ee342cecd0afee26cc6e35034e6459518320`. El commit documental posterior no se atribuye al binario. ID `dev.posture.post05_selective_reactions`, versión0.11.9.

Expiración informada por GitHub: **2026-12-04 02:06:00 Panamá (UTC−5)** (`2026-12-04T07:06:00Z`). Guardar el archivo antes de expirar.

MSVC x64: 21 laboratorios y 4,272,615 verificaciones; adaptador CP05 142,364; integración nativa de FIX01 36,222, control viejo 2656; geometría 21,660. **525/525 mutaciones** (502 conservadas+23 nuevas), cero TIMEOUT; nuevos negativos de fuente12/12, conservados CP05 16/16; PE/imports y descarga independiente PASS. Juego, animaciones visibles, chispa/sonido y rendimiento: **HUMAN_RUNTIME_PENDING**.


## Sustituir un solo archivo

1. Cierre el juego. Guarde fuera del directorio activo el `.dusk`0.11.8 y su respaldo0.11.7. No active dos versiones de Light Fades Twice a la vez.
2. Descargue el artifact privado enlazado arriba; extraiga su único `.dusk` y colóquelo en lugar del anterior. No instale DLLs sueltas ni cambie configuraciones, saves, SDK o EXE.
3. Para la prueba principal B, conserve los otros siete mods exactamente: Enemy Variant Framework 0.15.0; Bokoblin Expansion 0.17.0; Enemy Health Bars 2.0.3 CP06 Armos TEST; Enemy Health Multiplier 2.0.3 CP11 arrow route TEST; Zora Swim 1.3.0; Luau Support 1.0.0; Dusklight Randomizer 1.0.6. El Zora Swim 1.2.1 shadowed no era un noveno mod.
4. Verifique en el inicio del log una sola carga de Light Fades Twice0.11.9 y la fuente compilada indicada arriba. Los otros paquetes no se reemplazan.

## Prueba breve B — ocho mods

En un encuentro válido Red/Black **normal**, sin infligir daño ni romper postura al principio, deje terminar varias selecciones completas. La selección sigue siendo aleatoria: no cada ofensiva es combo. Busque estos patrones:

| Patrón | Ritmo esperado | Qué observar | Estado |
| --- | --- | --- | --- |
| Red4 | 1—2-3—4 | Cuatro animaciones, pareja central más rápida y remate separado | HUMAN_PENDING |
| Black8 | 1—2—3-4-5-6-7—8 | Cinco swings en la parte central, ocho en total | HUMAN_PENDING |
| Black7 | 1-2—3—4–5–6–7 | Pareja inicial rápida y cuatro finales más cadenciosos | HUMAN_PENDING |
| Bloqueo por índice | R, rango y ángulo de contacto reales | Espada/escudo, chispa y sonido nativos; ningún golpe contado sin animación | HUMAN_PENDING |
| Parry por índice | Nueva pulsación R+B para cada intento | Movimiento físico nuevo del escudo y postura +27 Red/+20 Black normal | HUMAN_PENDING |
| Parejas de parry | Internos, penúltimo/último y parejas rápidas viables | Dos entradas y DOS acciones visibles; sin crédito duplicado por las dos esferas | HUMAN_PENDING |
| R sostenido/liberado | Mantener guardia durante y después; después soltarla | Continuidad sin espera fantasma de CP05; distinguir recuperación/aggro legítimos | HUMAN_PENDING |
| Interrupciones | Daño, postura100, muerte, agua, pausa/sala/evento | Cancelación segura, ningún swing adicional ni timer residual | HUMAN_PENDING |
| Fallos de contacto | Esquivar, alejarse, orientar el escudo fuera | Puede fallar legítimamente; no parry/chispa artificial por proximidad | HUMAN_PENDING |
| Blue CP04 | Blue2+2 y pareja final R+B | Misma cadencia y dos movimientos de escudo aprobados en0.11.7 | HUMAN_PENDING |
| Exclusiones | Furia Black y especial aleatorio Red | ×2/chip y exclusiones de parry previas intactas | HUMAN_PENDING |
| HUD/Link | Combate, Scoop/Open/Talk, pausa y cambio de sala | Barra Link, vida/postura enemiga y prompts como en HUD FIX03 | HUMAN_PENDING |
| Audio/rendimiento | Combos completos a simulación30Hz | Contraste rítmico reconocible; sin afirmar FPS desde CI | HUMAN_PENDING |

Pruebe los golpes intermedios y finales de forma aislada con postura suficiente. No es necesario conseguir ocho parries consecutivos: ruptura100 debe cancelar, y regeneración CP02 sigue activa. Mantener R no implica que el NPC deba atacar instantáneamente fuera de un combo. El especial aleatorio Red y Black en furia no forman parte de esta corrección de parry.

Cierre normalmente para guardar los resúmenes SHUTDOWN. Si persiste un problema, indique patrón/posición y si fue falta de animación, bloqueo, chispa/sonido, parry o continuidad. Un vídeo corto ayuda si se dispone de él; no es un requisito. No hace falta repetir ni demostrar las pruebas de CI.

## Entorno A — un solo mod

Con el juego cerrado, haga una prueba separada dejando activo solo este `.dusk`, sin eliminar sus siete paquetes de respaldo. Sirve para comprobar inicio, Link/HUD y degradación segura sin dependencias. Red/Black de Expansion y su clasificación/protocolo no existen de forma verificable sin ese mod: FIX01 no fuerza combos normales sobre perfiles desconocidos. A no certifica los tres patrones ni la convivencia de B. Restaure los siete paquetes intactos al terminar.

## Volver a 0.11.7 si falla

Cierre el juego, retire únicamente0.11.9 y reactive **un solo** `.dusk`0.11.7 CP04. Mantenga los otros siete mods intactos. La 0.11.8 se conserva como evidencia defectuosa, no como respaldo aprobado.

- [Artifact CP04 aprobado13283289812](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41746570392/artifacts/13283289812).
- `LIGHT_FADES_TWICE_CP04_0_11_7_PRIVATE_TEST_windows-amd64_2d103c5562f7.dusk`.
- Tamaño147.197 bytes; SHA-256 `e446ed3ee1111837a9feed628adf939942a006e60913fe66b00d48986b71826e`.
- Fuente `2d103c5562f7199b875d5c4c7de7f00a32922a61`. Expiración informada por GitHub: 2026-12-03 19:40:20 Panamá (2026-12-04T00:40:20Z). Guarde el respaldo antes de expirar.

La prueba humana de 0.11.7 reportó dos movimientos físicos diferenciados de escudo; eso no constituye una prueba humana de 0.11.9. No se ejecutó el juego ni su DLL en CI o en esta sesión.
