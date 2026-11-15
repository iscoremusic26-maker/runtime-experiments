# Guía de prueba humana — LIGHT FADES TWICE 0.13.12 DKN01 FIX03 (prioridad de arriba abajo)

Estado: **HUMAN_RUNTIME_PENDING**. Instala solo este `.dusk`. Envía el `dusklight-*.log` de cada sesión.

1. **Lizalfos con Z-target:** fija a un Lizalfos y deja que te golpee (embestidas y coletazos), bloqueando y sin bloquear, de frente y de lado. Link no debe girarse bruscamente ni quedar de espaldas. Log: `LIZ_SUMMARY part=FIX02_DISTANCE version=0.13.12 ... atvec_inward_removed=`.
2. **Empuje al bloquear:** bloquea combos completos del Darknut en F1, F2 y F3. Link debe retroceder poco y cada vez menos en golpes seguidos. Log `LINK_SLIP_CAPPED ... chain=`.
3. **Tempo:** F1 debe sentirse igual que en 0.13.11. F2/F3 algo más lentos (×1,25), con el mismo ritmo entre golpes; estocada/doble sueltos ×1,2; patada ×1,12. Dinos si alguno queda raro (sobre todo patada → estocada de F2-C4).
4. **Defensa / parry del Darknut:** ataca con B varias veces seguidas en F1 (con escudo), F2 y F3. Bloqueo normal: tu espada NO rebota. A veces (más cuanto más encadenes golpes) tu espada rebota de verdad: ganas postura (+20 en F1, +25 en F2/F3) y él responde con UN contraataque (F1: escudo o maza; F2/F3: patada, estocada o doble). Logs `ADAPTIVE_GUARD verdict=PARRY_ATTEMPT streak=`, `ENEMY_PARRY_REAL link_gain=`, `COUNTER_START`.
5. **Helm Splitter:** rompe su postura en F2, Shield Attack → segundo tambaleo (debe verse **dañado, con la espada baja**, distinto del primero) → Helm Splitter → cae. No debe verse en pose de guardia. Repite con **Mortal Draw** en el primer tambaleo.
6. Finish en F2 (FIX02 → F3) y en F3 (muerte); sin Finish ~6 s → se levanta con FIX02.
7. **Ofensiva:** 0 `UNAUTHORIZED_NATIVE_ATTACK executed=1`; `NATIVE_ENTRY_SUPPRESSED executed=0` es normal. El doble completo ya no sale como golpe suelto (solo en combos o como contraataque).
8. Regresiones: Bokoblins, Chilfos, otros Darknut (Templo del Tiempo, "Darknut (Sword)"), barra de postura.
