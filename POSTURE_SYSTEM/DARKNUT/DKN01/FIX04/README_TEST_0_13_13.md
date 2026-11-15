# Guía de prueba humana — LIGHT FADES TWICE 0.13.13 (DKN01 FIX04)

Instala solo el `.dusk` 0.13.13 (sustituye al 0.13.12; rollback: el `.dusk` 0.13.12 de `lft_0_13_12_dkn01_fix03_delivery`). Juega contra el Darknut normal de Enemy Spawner y, al terminar, entrégame el log completo (`%APPDATA%\TwilitRealm\Dusklight\logs\dusklight-*.log`).

## 1. F1 (armadura y maza)
- Aguanta claramente más: 600 de vida y postura 200. Golpear el escudo debe hacer progresar la barra (+4 por espadazo bloqueado).
- La armadura se desprende poco a poco; la transformación nativa solo al agotar la vida.
- Los cuatro combos de maza y los golpes sueltos deben sentirse **exactamente igual** que en 0.13.12.

## 2. Cadena de B (F1, F2 y F3)
- Encadena espadazos de frente: el Darknut debe **defender** (escudo en F1; en F2/F3 guardias de espada variadas según la dirección de tu corte) y **no** lanzar un combo encima de tu cadena.
- Los tres primeros espadazos de una cadena nunca reciben parry; a partir del 4.º puede intentarlo (25 %, 45 %, 60 %).
- Si dejas de atacar, te alejas o fallas al aire dos veces, recupera la iniciativa con su ritmo normal.

## 3. Parry del Darknut
- Debe verse el **rebote de tu espada** (también en F2/F3), sin daño ni chispa de daño del mismo golpe, con **chispa naranja y sonido agudo** (como el Lizalfos), +20/+25 de tu postura una vez.
- Después, **un** contraataque que te deja recuperar el control y responder (guardar o hacer parry). F1: escudo/lateral/vertical; F2/F3: patada/estocada/doble completo (dos cortes).

## 4. Tu parry
- Parry a cada golpe (incluidos los dos cortes del doble y la patada): chispa naranja y sonido agudo, sin rebote de tu espada por ese evento. Los bloqueos normales siguen azules y con su sonido normal.

## 5. Tempo F2/F3
- Más pausado (×1,40 frente a 0.13.11) pero continuo: no debería haber tramos en cámara lenta al principio de F2-C2 ni de F2-C4. Si aún notas uno, dime en qué combo y golpe (el log trae `rate_min`, `native_pause_ticks` y `error_ex_pause`).
- Los pequeños "tirones" de 2 ticks cuando golpeas al Darknut son el hitstop nativo del juego (afecta a toda la escena).

## 6. Retroceso
- Debe sentirse igual que en 0.13.12 (se corrigió un doble conteo interno conservando exactamente el mismo perfil).

## 7. Regresiones rápidas
- Lizalfos (Z-target, distancia, parries) igual. Levantamientos/remates/resurrección: no hace falta repetirlos si no quieres; **Mortal Draw** queda pendiente para cuando decidas probarlo.

Estado técnico: CI verde y laboratorios; estado humano: **HUMAN_RUNTIME_PENDING**.
