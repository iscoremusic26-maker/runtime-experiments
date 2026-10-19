# CP17 — Red aggressive AI · Expansion0.14.0 TEST privado

Solo sustituye Expansion FIX01. Provider/editor CP13 0.13.0, APIs, JSON y recursos del usuario permanecen intactos. Windows x64, Dusklight2.0.3@40457c6, DX12. No instalar dos Expansion ni usar hot reload.

Red clasificado por CP10.4 obtiene B/C nativos x1.15; oportunidades x3 por carga válida (70% por episodio), pasividad (105 ejecuciones propias) o selección aleatoria (12% por golpe elegible). Ráfagas con cooldown120–210 y recuperación normal entre ellas; pasividad180–300. Grupo no modifica ninguna de estas tasas. ATP2, lockout20, HP/regen, lifesteal/gold CP14 permanecen en su código anterior. Blue FIX01 y Black byte-preservados.

Aproximación: se observa y utiliza FIND nativo, sin forzar modo, marcha, timer, home o posición. No hay boost1.5 de movimiento: no se encontró una escritura PRE segura respecto de las decisiones nativas posteriores; se conserva persecución nativa y la intención vence a90. La animación x3 sí es una tasa real por golpe fresco, no un multiplicador de daño ni una promesa de interrupción.

Una compensación acotada reproduce el SFX B12.5 que el else-if nativo omite cuando un salto3 cruza10 y12.5 juntos. No altera hitboxes ni fotogramas. Audio/escudo/contacto físico aún requieren QA humana.

Estado verificado: SOURCE_IMPLEMENTED + LAB_PASS + WINDOWS_MSVC_PASS + INDEPENDENT_DOWNLOAD_PASS + HUMAN_RUNTIME_PENDING.64 CP17 MSVC y locales ASan/UBSan, regresiones,24 archivos runtime idénticos aFIX01 y462 blobs pinneados PASS. RED_LINK_CHARGE_DETECT_SOURCE_AND_MSVC_ABI_PASS_HUMAN_PENDING. No se ejecutó juego ni se leyó un objeto Link físico desde el laboratorio.

[Descargar TEST privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39184082946/artifacts/12157032798), artifact DEVF_CP17_RED_AGGRESSIVE_AI_TEST_39184082946; [run39184082946](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39184082946), build+independent-download SUCCESS. Caduca17-11-2026 20:13:35 America/Panama. Fuente REAL compilada8fbaea77df4fe547676ca2462a6db633f3788273; CIa14ca4e264d7b629bb6b02745510300f16bc08ae. El cierre posterior solo cambia documentación; hashes y límites en VERIFIED_PACKAGE.json.

Ver HUMAN_TEST y RECOVERY. CP14 LINK_LAYOUT_CANARY_FAILED_LIFESTEAL_DISABLED sigue pendiente; el lector CP17 no usa ni relaja ese canario.
