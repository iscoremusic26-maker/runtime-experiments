# Auditoría de escrituras del DLL descargado [B]

## Archivos comparados

| Versión | Paquete | DLL SHA-256 | Origen |
|---|---|---|---|
| 0.7.0 | `POSTURE_POST07_0_HUD_PRIVATE_TEST_windows-amd64_f0e92c9f1d74.dusk` | `ca507493…09d9` | artefacto 13118435513 |
| 0.6.1 (rollback) | `POSTURE_POST06_1_REWORK_PRIVATE_TEST_windows-amd64_5037d3f311c3.dusk` | — | artefacto 13115359099 |

Ambos paquetes se descargaron por su ID de artefacto.

## Método

1. `objdump -d` de los dos DLL.
2. Se cuentan las escrituras a memoria (`mov`/`or`/`and`… con destino en memoria) cuyo desplazamiento es un campo del actor:
   - modo, estado y modo previo: `0x8c8`, `0x8d0`, `0x8cc`;
   - timers: `0x8e0`, `0x8e2`;
   - flags: `0x69a`;
   - bits Tg/Co: `0xce8`, `0xd08`, `0xea0`, `0xec0`;
   - vida y atención: `0x656`, `0x650`;
   - tipo de corte de Link: `0x668`.
3. Cada escritura se asigna a su función mediante el mapa del enlazador del CI.

## Resultado

- **Mismas escrituras que en 0.6.1, campo por campo.** Solo cambia la selección de instrucciones: MSVC fusionó `old_mode=5` y `state=0` de `post06_recover` en un único `movq $0x5,0x8cc(%rbx)` (en `0x1800112e8`).
- **Dónde están:** todas en `restore_reaction`, `post06_step` (que incluye en línea bonus, aturdimiento y recuperación), `do_pre` y `do_post`.
- **Funciones del HUD:** **0** escrituras a campos del actor en `hud_sim_pass`, `hud_packet_paint`, `hud_drop_all`, `on_meter_execute_post`, `on_meter_draw_post` y `on_meter_delete_pre`.
- **Única escritura del HUD en memoria del juego:** nuestro puntero de paquete dentro de las listas 2D del juego. Se escribe con `dDlst_list_c::set` (EXE) y se retira con `scrub_all`, dentro de `hud_drop_all`. Lo impone la auditoría de fuente.
