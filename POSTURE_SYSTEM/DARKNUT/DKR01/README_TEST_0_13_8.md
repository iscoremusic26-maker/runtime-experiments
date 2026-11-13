# Prueba humana de 0.13.8 (DARKNUT RESURRECTION DKR01)

## Instalación
1. Cierra Dusklight y comprueba el SHA-256 del `.dusk` 0.13.8.
2. Guarda una copia del 0.13.7 y quítalo. Debe quedar **un solo** Light Fades Twice.
3. Para volver atrás, restaura el 0.13.7: `482bed51…5cd7` (FULL 43384533943).

## Requisitos
- Ending Blow aprendido (primera técnica secreta) y Link en forma humana.
- Invoca el **"Darknut"** normal de Enemy Spawner, no "Darknut (Sword)".

## Perfiles (guarda un log por perfil)
- **A:** solo Light Fades Twice + Enemy Spawner (para invocar).
- **B:** tu conjunto habitual de 8 mods.

## Ruta A: Finish → una resurrección → muerte nativa
1. Rompe la armadura. La fase 1 y la transición deben ser nativas.
2. Derrótalo en la segunda fase.
   - Cae con la animación original, sin oscurecerse y con la espada en la mano.
   - Queda tumbado. Log: `DKR01 event=FIRST_DEFEAT_NATIVE_FALL` y luego `event=DOWN_FINISH_AVAILABLE`.
3. Fíjalo (Z/L) y comprueba que aparece **Finish** en A. Haz el Ending Blow.
   - No debe levantarse hasta que Link aterrice, saque la espada, haga el salto atrás y aterrice.
   - Log: `event=FINISH_HIT_NATIVE_RECEIPT` y `event=RESURRECTION_START ... path=FINISH`.
4. Se levanta con la animación nueva una sola vez y vuelve a pelear con su IA de segunda fase.
   - Log: `event=RESURRECTED_SECOND_PHASE_100PCT ... acc=0/360`.
5. Derrótalo otra vez. Muerte **nativa completa**: oscurece, la espada cae y desaparece, y el cuerpo se desvanece.
   - No hay Finish ni levantamiento.
   - Log: `event=SECOND_DEFEAT_NATIVE_DEATH` y `event=ACTOR_DELETED_SLOT_RETIRED`.

## Ruta B: sin Finish → temporizador → una resurrección → muerte nativa
1. Haz los pasos 1 y 2 de la ruta A.
2. No lo remates. Unos **10 s después de que acabe de caer**, se levanta.
   - Log: `path=TIMER`.
3. Haz el paso 5 de la ruta A.

## Extras (si hay tiempo)
- Golpéalo mientras cae, está tumbado o se levanta. No debe pasar nada.
- Pulsa Finish justo cuando van a cumplirse los 10 s. No debe levantarse a mitad del remate.
- Falla un Finish. El temporizador sigue y se levanta después.
- Prueba dos Darknuts a la vez y sal de la sala con uno tumbado. No debe haber crash, cuerpos congelados ni inmortales.
- Bokoblins, Lizalfos y Chilfos deben seguir como en 0.13.7.

## Logs que guardar
- El log de Dusklight de cada perfil.
- Líneas que interesan:
  - `DKR01 event=INSTALL ... enabled=1 resource=LOADED check=OK`
  - `DKR01 event=CLIP_BIND result=OK`
  - los eventos anteriores
  - `DKR01_SUMMARY why=SHUTDOWN`
