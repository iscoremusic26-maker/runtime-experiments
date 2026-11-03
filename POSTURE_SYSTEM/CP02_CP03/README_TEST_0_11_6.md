# Enemy Posture System CP02+CP03 — 0.11.6 PRIVATE TEST

Un único `.dusk` acumulativo Windows x 64 / DirectX12 para Dusklight 2.0.3, mismo ID `dev.posture.post05_selective_reactions`. Base 0.11.5 probada y aprobada por el usuario; este binario nuevo sigue **HUMAN_RUNTIME_PENDING**. Solo cambian regeneración enemiga y precisión temporal del parry, según la tabla.

| Política | Antes 0.11.5 | Candidato 0.11.6 | Categoría |
|---|---|---|---|
| Regen enemiga por bandas >75/>50/>25/>10/>0% | 5/4/3/2/1 puntos/s | 10/7/4/2/1 puntos/s | IMPLEMENTADO |
| Demora desde último golpe/parry que suma postura | 120 ticks elegibles | 60 ticks elegibles | IMPLEMENTADO |
| Shield Attack: delta y edad simultáneos | −1/+9; edad≤11 | −1/+7; edad≤9 | IMPLEMENTADO |
| Pesos parry Blue/Red/Black | 40/27/20; Fury inseguro rechazado | Iguales | SIN CAMBIOS |
| Golpe decisivo | ×1,5 una sola vez, redondeo existente | Igual | SIN CAMBIOS; ×2 evaluado sin aplicar |
| Propuesta 5–8 puntos en Link | Sin regla aprobada; parry cuesta 0 | No aplicada | EVALUADO-SIN-APLICAR |
| HUD FIX03, Scoop, alineación EHB, Link y sus controles | Aprobados en 0.11.5 | Código conservado | SIN CAMBIOS |

## Paquete verificado

[Descargar PRIVATE TEST 13264179241](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41703645193/artifacts/13264179241) · [CI 41703645193](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41703645193).

`POSTURE_CP02_CP03_0_11_6_PRIVATE_TEST_windows-amd64_8c72aec291a7.dusk`

**137486 bytes**. SHA-256:

`0aa8e8d2941d644a33765fe288bc3f9867cc1e188506fed691caf069c63fb019`

ID `dev.posture.post05_selective_reactions`, versión `0.11.6`. Expiración según GitHub: **2026-12-03T14:44:30-05:00 (Panamá, UTC−5)**.

Fuente compilada `8c72aec291a7473f1752c702137229cc2224c998`; CI `505cd3fd053011e6dc7f78dfa73d7d039c57c23a`. Estos informes se añaden después en un commit documental separado.

MSVC x64, PE y ambas descargas verificados. 2,881,551 comprobaciones en 19 labs; 434/434 mutaciones (412 heredadas +22 nuevas), sin TIMEOUT; 126 negativos semánticos, 20 PE y dos de instrucciones. Prueba A/B Windows/DX12: **HUMAN_RUNTIME_PENDING**.



## Instalar y comparar

Descarga el artefacto y extrae del ZIP el único `.dusk`. Con el juego cerrado, conserva el `.dusk`0.11.5 fuera de mods y reemplaza **solo** el archivo de postura por 0.11.6. Nunca cargues ambas versiones del mismo ID. Arranca en frío con DX12; comprueba en el log la versión 0.11.6, tabla 10/7/4/2/1, demora 60 y ventana−1/+7 con edad 9.

Prueba A: Posture aislado, si procede y dispones de un perfil de prueba separado. Prueba B: conserva los otros siete mods y sus versiones: Enemy Variant Framework 0.15.0, Bokoblin Expansion 0.17.0, Enemy Health Bars CP06 Armos TEST, Enemy Health Multiplier CP11×1, Zora Swim 1.3.0, Luau Support 1.0.0 y Randomizer 1.0.6. No se ha ejecutado ninguna de estas partidas A/B en CI. No alteres saves ni otros mods para instalar este candidato.

Compara 0.11.5 y 0.11.6 con encuentros y contactos parecidos; cierra el juego entre sustituciones. El cambio intencional es una recuperación enemiga más rápida con mucha vida, y una ventana de parry dos frames/dos ticks más corta. Las recompensas permanecen iguales.

## Prueba humana compacta

1. Con Blue/Red/Black, suma postura sin romperla y deja de golpear. Prueba mucha y poca vida, en los límites 75/50/25/10% cuando puedas. A máxima tasa observada 10/s, la primera unidad cae tras 63 ticks elegibles desde el último contacto válido:60 de espera y 3 de fracción. Con 7/4/2/1, primera unidad en 65/68/75/90. Pausa durante la espera/recuperación y confirma que al regresar no hay avance acumulado por la pausa.
2. Haz parries de Shield Attack R+B en contactos tempranos, de borde y tardíos; repite dos ataques verdaderamente distintos y comprueba que dos esferas o llamadas repetidas del mismo golpe no dan dos créditos. Deben mantenerse 40/27/20 por variante. Black Fury con posible chip sigue rechazado. Los bordes exactos de frame/edad necesitan diagnósticos `POST08` y no se certifican solo a simple vista.
3. Cruza 100 y prueba la oportunidad de stun: espada/Helm, un único bonus decisivo, contactos no decisivos y oportunidad agotada. Comprueba rearme 25 de pie y 0 tras levantamiento completo; muerte y Finish nativos. Prueba bloqueo manual R, defensa L+R, rearme al soltar/pulsar R, guard-break y penalización 75 ticks de Link. Parry confirmado conserva coste 0.
4. En B, observa Red curándose y enemigos con máximos distintos. La tabla usa el máximo observado por generación: si el enemigo apareció ya herido, ese máximo puede ser inferior al verdadero. El log declara esa limitación; no interpretes el porcentaje observado como HP máximo infalible.
5. Repite Scoop con botella, Open/Talk/Pick Up, Shield attack/Jump/Helm Splitter y 10–20 golpes seguidos. Corazones, minimapa, rupias y HUD superior deben conservarse; supresión solo del prompt inferior invasor, reaparición nativa al desaparecer la barra, barras enemigas alineadas y sin parpadeo de Link. Pausa, menú, cambio de sala, lobo/humano y regreso no deben dejar residuos.
6. Si puedes, repite a 30/60 FPS. Compara tras igual número de ticks simulados; la interpolación de presentación no debe acelerar la recuperación. Son tasas medias con fracciones:7/s usa intervalos 4/5 ticks y 2/s un punto cada 15 ticks, no decrementos continuos por cada frame de render. Usa contadores de log para cuantificar lo que la barra no permite distinguir.

Conserva los logs completos para revisión privada; no publiques rutas o datos personales. Los presupuestos de diagnóstico son finitos: una ausencia de línea no demuestra ausencia de evento. Si el HUD, Scoop, alineación, parpadeo, controles, vida o Finish retroceden, es **regresión bloqueante**: detén la prueba y vuelve a 0.11.5.

## Rollback inmediato

Cierra el juego, retira únicamente 0.11.6 y restaura el backup 0.11.5. SHA-256 del `.dusk` aprobado:

`1dbf22a4c985e2ff334bd774faba86ac6bef717e55d135dbca7755103cd2f660`

[Artefacto 0.11.5, CI41687970224](https://github.com/iscoremusic 26-maker/codex-cp 00-inputs/actions/runs/41687970224/artifacts/13255667942). No se cambian partidas ni los otros siete mods.

[Implementación, límites y evaluación](IMPLEMENTATION.md) · [RESULTS.json](RESULTS.json) · [Evidencias](EVIDENCE/)
