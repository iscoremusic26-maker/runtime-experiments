# CP01 G5: diagnóstico desarmado verificado

**DISARMED_NO_REGISTRATION / READ_ONLY_DIAGNOSTIC. NEXT_G5_SESSION_AUTHORIZED=FALSE. CP02=NO_GO.**

Se recuperaron las mismas ramas y PR draft [principal #19](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/19) y [CI #13](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/13), sin merge, reset ni cambios históricos. Fuente compilada `29efb505a71014f9f8725846576485cdb91f77cd`; CI `f02cbd99bc280d6bbd54ab0f08b4ba241b7f0fe4`; checkpoint documental identificable por el tag anotado `DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED`. El commit documental final difiere deliberadamente del compilado.

El log recibido conserva 2.182 líneas y 27 eventos, resumidos sin publicar el original. No hubo solicitud E_OC de DEVF en esa sesión. Se acotó la clasificación de room=-1 a KYTAG04 con metadata/owner válidos; conserva la fila, frescura y distancia XZ>=1600. No prueba inocuidad de eventos. El criterio exacto speedXYZ==0/speedF==0 sigue intacto y sin calibración física. Temporal y trazas solo observan.

[Run Windows 38466822325](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325), job 115535637388: MSVC compile/link PASS, 20 negativos PE y 13 negativos ZIP PASS. Los 100 checks y ocho mutantes compilados/muertos de run 38445082050 se reutilizaron por hash, sin ejecutarlos nuevamente. El antiguo error de imports fue una diferencia real: solo se añade `VCRUNTIME140.dll!memcmp`, comparación readonly de ocho bytes de stage; los 30 imports de juego son idénticos. El auditor nuevo revisa identidad completa, ABI, servicios y cinco exports. Ver TEST_RESULTS, DIAGNOSTIC_IMPORT_REVIEW y BINARY_AND_PACKAGE_AUDIT.

Paquete **diagnóstico** `dev.devf.cp01_g5_rejection_diagnostic` v0.0.2: [artefacto privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325/artifacts/11847829866), descargado y verificado realmente, vence 2026-11-12 20:57:57 UTC (15:57:57 Panamá). No contiene provider activo, NativeBackend, Controller.attempt/poll, LayerScope, ActorService, registros ni mutadores. No instalar/cargar ni ejecutar el juego todavía; no autoriza primera aparición, render, colisión o limpieza runtime. No se reenvió el activo 0.0.1.

GATE_DECISION enumera los bloqueos; RECOVERY contiene reproducción y recuperación. Ubicación/G6 NOT_VERIFIED, reposo UNVERIFIED y descarga de DLL custom BLOCKED_INDEPENDENT. Siguiente paso mínimo: revisión humana del diagnóstico y autorización separada para captura observacional; no nueva solicitud de enemigo.
