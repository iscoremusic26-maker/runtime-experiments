# Prueba humana de 0.13.6 (CHILFOS FIX06)

## Instalación
1. Cierra Dusklight.
2. Comprueba el SHA-256 del `.dusk` 0.13.6.
3. Guarda una copia del 0.13.5 y quítalo. Debe quedar un solo Light Fades Twice activo.
4. Para volver atrás, restaura el 0.13.5:
   - público: `7a0421b4…18e8`, run 43340220745;
   - o el privado que probaste: `d9b0ca80…a9aa`.

## Perfiles
- **A:** Light Fades Twice solo. Enemy Spawner se puede usar únicamente para colocar enemigos, y hay que indicarlo.
- **B:** tu conjunto habitual (Expansion 0.17.0, EVF 0.15.0, Enemy Spawner 0.1.1, HM203, barras, Zora Swim…).

## Qué probar (cinco minutos por punto)
1. **Jump Strike** contra el Chilfos, el Lizalfos y los Bokoblins Blue, Red y Black, con HP alto y con HP muy bajo.
   - Hace más daño y más postura que un tajo, pero nunca mata por sí solo. Un tajo normal después sí mata.
   - Con el enemigo roto tampoco remata. Helm Splitter y Mortal Draw siguen rematando.
   - En el log: `JUMP_STRIKE event=CONTACT … result=NON_LETHAL` y `JUMP_STRIKE_SUMMARY`.
2. **Spam de Jump Attack** de frente y de lado:
   - Bloqueos y parries sin pérdida de HP del enemigo en ese golpe.
   - Tras un parry en el aire, Link aterriza con su retroceso nativo y llega un contraataque.
   - Vídeo: el retroceso visible.
   - En el log: `LINK_JUMP_RECOIL event=LAND_RECOIL_NATIVE` y `event=RECEIPT result=PROC_CUT_REVERSE`.
3. **Parry de los ataques del enemigo**, para provocar su contraataque:
   - A veces le sigue enseguida un combo (más o menos el 65 %), y cada uno de los cuatro patrones aparece con frecuencia parecida.
   - En el log: `CHILFOS_CHAIN` y `LIZ_CHAIN` (`SCHEDULED`, `STARTED`, `NO_CHAIN`, `CANCELLED`).
4. **Back Slice repetido** contra el Chilfos:
   - Desde el segundo Back Slice gira y a veces hace parry. En ese parry Link sigue su giro sin interrumpirse, y aparecen chispa naranja y sonido agudo.
   - Desde la espalda real todavía hiere.
   - En el log: `PARRY_WITHOUT_LINK_RECOIL`.
5. **HUD:**
   - Con la barra visible, ningún destello de botón bajo ella.
   - Sin barra, los botones y sus destellos son los de siempre (Scoop, salto, Shield Attack, Helm Splitter).
   - Vídeo y `HUD_SPARK_SUMMARY`.
6. **Lanza pegada a Link:**
   - Cada choque contra el escudo muestra una chispa (azul en un bloqueo, naranja en un parry) y un solo sonido.
   - En el log: `PARRY_FX event=SPEAR_SPARK moved=…`. Vídeo.
7. **Que nada se haya roto:**
   - Lanzamiento C3 sin caída de FPS y lanza intacta.
   - Tambaleo FIX05 que termina erguido.
   - Helm Splitter alto y Mortal Draw sin inclinación.
   - Los cuatro patrones del Lizalfos y sus parries dobles.
   - Bokoblins con su furia.

## Comparte
Las líneas filtradas `JUMP_STRIKE`, `LINK_JUMP_RECOIL`, `CHILFOS_CHAIN`, `LIZ_CHAIN`, `CHILFOS_FIX06`, `PARRY_FX event=SPEAR_SPARK`, y los resúmenes:
- `CHILFOS_SUMMARY`, `CHILFOS_CONTACT_SUMMARY`, `CHILFOS_FIX05_SUMMARY`, `CHILFOS_FIX06_SUMMARY`;
- `LIZ_SUMMARY`, `LIZ_FIX06_SUMMARY`;
- `JUMP_STRIKE_SUMMARY`, `HUD_SPARK_SUMMARY`, `PARRY_FX_SUMMARY`.

Si puedes, añade también los vídeos de los puntos 2, 4, 5 y 6.

Estado: `HUMAN_RUNTIME_PENDING`, `VISUAL_RUNTIME_PENDING` y `PERF_RUNTIME_PENDING` hasta tu prueba.
