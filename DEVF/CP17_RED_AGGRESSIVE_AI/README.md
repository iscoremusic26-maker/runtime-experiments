# CP17 — Red aggressive AI · Expansion0.14.0 TEST privado

Solo sustituye Expansion FIX01. Provider/editor CP13 0.13.0, APIs, JSON y recursos del usuario permanecen intactos. Windows x64, Dusklight2.0.3@40457c6, DX12. No instalar dos Expansion ni usar hot reload.

Red clasificado por CP10.4 obtiene B/C nativos x1.15; oportunidades x3 por carga válida (70% por episodio), pasividad (105 ejecuciones propias) o selección aleatoria (12% por golpe elegible). Ráfagas con cooldown120–210 y recuperación normal entre ellas; pasividad180–300. Grupo no modifica ninguna de estas tasas. ATP2, lockout20, HP/regen, lifesteal/gold CP14 permanecen en su código anterior. Blue FIX01 y Black byte-preservados.

Aproximación: se observa y utiliza FIND nativo, sin forzar modo, marcha, timer, home o posición. No hay boost1.5 de movimiento: no se encontró una escritura PRE segura respecto de las decisiones nativas posteriores; se conserva persecución nativa y la intención vence a90. La animación x3 sí es una tasa real por golpe fresco, no un multiplicador de daño ni una promesa de interrupción.

Una compensación acotada reproduce el SFX B12.5 que el else-if nativo omite cuando un salto3 cruza10 y12.5 juntos. No altera hitboxes ni fotogramas. Audio/escudo/contacto físico aún requieren QA humana.

Estado actual: revalidación de dos casos de continuidad (episodio de carga ante LOS/prioridad transitoria y pasividad acumulada ante recoil nativo seguro).66 casos locales ASan/UBSan PASS. El snapshot8fbaea77/run39184082946 pasó build/descarga y queda preservado como histórico; NO es el nuevo snapshot final. Build/descarga de la revisión actual PENDING. HUMAN_RUNTIME_PENDING. Solo el artifact que se indique tras la nueva verificación será la entrega final.

Provider/editor/API/JSON y Blue/Black/CP14 intactos. Ver HUMAN_TEST/RECOVERY; no instalar versiones simultáneas. El canario físico CP14 sigue pendiente e independiente.
