# Pantalla estática focal del norte — permiso sólo para QA experimental

**STATIC_SCREEN_SUPPORTS_CONTROLLED_NORTH_QA; SITE2/HUMAN_TERRAIN_PENDING.**
No se detectó una incompatibilidad estática concreta que impida razonablemente ensayar **un** E_oc nativo. Esto no acredita navegación, progresión universal ni geometría GPU/colliders runtime.

## Evidencia anterior reutilizada, no repetida
PR39/checkpointd9a7765…: suelo calculado(-1250,-6327.600450915229,61950), prisma2281/PLCroom3 ground0 special0 exit63 sin through; cobertura±100/±501 completa. Pendiente en normal de soporte aproximadamente4.395°. RangoY de la pantalla501 [-6374.855453,-6261.322710], terreno inclinado, no plataforma plana universal. Pared más cercana ENTRE celdas consultadas802.709, no mínimo mundial. Pantallas de volúmenes/cotas y AABB mmvbg/ClearB anteriores positivas en el centro norte. No se decodificó KCL, WRock/E_oc2.arc, ni repitió su integridad.
La pantalla501 es cota histórica de análisis, no un nuevo certificado de poses/arma/movimiento E_OC2. Para QA nativo se conserva gravedad/Acch/AI y se detiene ante anomalías; no hace falta suponer confinamiento para autorizar una prueba experimental acotada.

## NUEVA consulta incremental ejecutada
[Build/estudio38755215665](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755215665), job116491729506: north_context.py reutilizó los lectores publicados, leyó sólo DZR de R03 privado por SHA y CRC del miembro. No extraer/publicar assets ni repetir tres ARC. Fuente/resultado en evidence/build-result.json.

- Entrada Link PLYR[11], entry angle.z4: centro a939.4147XZ. No coincide con el home; no garantiza ubicación actual del jugador ni impide que el enemigo lo detecte al entrar.
- flwr7 ACT6[32]/[30] a940.6912/950.3289; Digpl ACT6[26] home a1025.9142. Son distancias a records, no garantía sobre su geometría/estado vivo. No se sustituyen ni borran.
- E_oc retail home más cercano ACT6[7] a1697.0563XZ. No excluye movimiento posterior; esperable coexistencia nativa, sin intervención per-actor.
- Polilínea ruta7 a922.9514XZ; ruta24 a2130.5969 y ruta20 a2607.5016. La ruta7 del consumidor ya verificado es **27 puntos discretos Digpl**, no un corredor barrido por un enemigo. Punto discreto más cercano[8] a4219.3009XZ; separación a cuadrado±501=3513.204, y deltaY=-387.6842. No transferir esos resultados a otros consumidores de puntos ni atribuir al E_oc activación Digpl del jugador.
- Se conservan las cotas anteriores de eventos/entrada/salida y recursos: ningún nuevo record toca DZS/DZR/switch/save. Mismo E_oc/preset/capa que CP06 native humano, pero carga efectiva en esta nueva posición y ramas de progreso aún necesitan observación humana.

## Altura y decisión
Usar Y matemático del KCL exactamente como spawn arriesga redondeo bajo suelo. Se aplica el **mismo margen inicial +5** documentado en sitio1: -6322.600450915229, redondeado float32 a **-6322.6005859375**. El motor debe asentar al nativo; no se afirma que esa sea la Y final observada. Sitio1 no cambia.
Se autoriza técnicamente entregar QA A para que el usuario observe terreno/visibilidad/colisión/asentamiento/eventos. Si A falla, no ejecutar B. B sólo después de A satisfactorio, máximo2ediciones en total; no coordenadas libres. No SITE2_ACREDITADO, GAMEPLAY_PASS ni SIMULTANEITY_PASS de CI.
