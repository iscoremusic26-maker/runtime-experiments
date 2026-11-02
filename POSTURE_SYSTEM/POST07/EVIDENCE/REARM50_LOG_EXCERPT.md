# Rearme 50 del ID 161: extracto saneado [R]

| Campo | Valor |
|---|---|
| Fuente | log real de 0.6.1 `dusklight-20261101-231855` (8 mods, Windows DX12), aportado por el usuario |
| Acceso | lectura con permiso, copia temporal fuera de los repositorios, ya borrada |
| Contenido | solo líneas del juego relevantes, en orden de aparición. Sin marcas de tiempo, rutas, cuentas ni punteros. Las líneas de Expansion van recortadas a los campos útiles. |

```
POST05_E2_ENV env=EXPANSION_POSSIBLE queries=1 sticky=1 basis=REQUIRED_IMPORT_OF_VARIANT_AI_ABSENT_OR_NOT
POST06_EVENT id=161 generation=8 phase=STAGGER_OPEN>FALLING why=DECISIVE_SWORD_X1_50 act=2 ok=1 age=24 hp=184>169 base=10 bonus=5 rearm=0
POST06_EVENT id=161 generation=8 phase=FALLING>DOWN_FINISH why=NONE act=0 ok=1 age=66 hp=172>172 base=0 bonus=0 rearm=0
POST06_EVENT id=161 generation=8 phase=DOWN_FINISH>GETTING_UP why=GETTING_UP act=0 ok=1 age=118 hp=176>176 base=0 bonus=0 rearm=0
POST06_EVENT id=163 generation=10 phase=FALLING>DOWN_FINISH why=NONE act=0 ok=1 age=61 hp=290>290 base=0 bonus=0 rearm=0
POST06_EVENT id=163 generation=10 phase=DOWN_FINISH>GETTING_UP why=GETTING_UP act=0 ok=1 age=96 hp=293>293 base=0 bonus=0 rearm=0
POST06_EVENT id=161 generation=8 phase=GETTING_UP>TRACKING why=TECHNICAL_ABORT_ON_FEET_50 act=3 ok=1 age=167 hp=179>179 base=0 bonus=0 rearm=50
POST06_EVENT id=163 generation=10 phase=GETTING_UP>TRACKING why=REARM_AFTER_NATIVE_GET_UP_0 act=4 ok=1 age=145 hp=298>298 base=0 bonus=0 rearm=0
```

En la misma ventana del log (Expansion 0.17.0, campos recortados):

```
DEVF_CP10_3_REGEN event=REGEN_APPLIED actor_id=161 generation=8 kind=BLUE ... hp_before=174 hp_after=175
DEVF_CP16_RECRUIT event=BLUE_COMBAT_RESET blue_id=161 blue_gen=8 ... native_mode=6 native_state=6
DEVF_CP16_RECRUIT event=BLUE_LINK_DETECTED blue_id=161 blue_gen=8 ... native_mode=3 native_state=5
DEVF_CP16_RECRUIT event=BLUE_CALL_ISSUED blue_id=161 blue_gen=8 ... native_mode=3 native_state=5
DEVF_CP16_RECRUIT event=BLUE_SHOUT_REQUESTED_NATIVE_WATCH3 blue_id=161 blue_gen=8 ...
DEVF_CP16_RECRUIT event=BLUE_SHOUT_STARTED blue_id=161 blue_gen=8 ... native_mode=7 native_state=4
```

## Lectura

- **Duración del levantamiento.** El 161 tardó de `age=118` a `age=167`, 49 ticks. El 163 tardó de `age=96` a `age=145`, también 49 ticks: la duración nativa completa de BIG 6.
- **Sin golpes.** Entre esas dos líneas no hay ningún evento de golpe del 161. La vida 176 → 179 es la regeneración de Expansion.
- **Salida redirigida.** Expansion observa la salida nativa (`native_mode=3 native_state=5`, FIND 5). En su `execute` PRE la redirige a `setActionMode(Watch,3)` [S Expansion `mod.cpp:1049`] antes de que `damage_check` la vea. POST06 0.6.1 solo reconocía FIND 5, y por eso cayó en `TECHNICAL_ABORT_ON_FEET_50`.

**Clasificación:** caso (i). Es un levantamiento nativo completo que sale vivo, y se corrige con FIX_REARM50. No es una interrupción legítima (ii) ni un problema de observación o identidad (iii): mismo id y generación, actor vivo y de confianza.
