# CP03 — revisión de viabilidad de HP150

**BLOCKED_WITH_EVIDENCE.** Este directorio contiene informes y una herramienta de lectura de procedencia. No contiene un mod funcional, manifest de mod, DLL, workflow nuevo ni `.dusk` CP03. No hay instrucciones de instalación de CP03.

Base inmutable: CP02 `0d2430262181bb2844f13bb8da0a628f71740998`, tag `DEVF_CP02_EOC2_ELITE_NATIVE_PACKAGE_VERIFIED`. Rama documental nueva: `feature/devf-cp03-hp150-feasibility`; los informes históricos CP01/CP02 y sus PR no se editan. CP02 sigue siendo el último checkpoint funcional.

Objetivo evaluado: una instancia adicional E_OC2, F_SP121 / room 3 / layer 6, XYZ `(-1250,-6304.0083,60750)`, yaw 0, setID FFFF; salud inicial efectiva 150, sin modificar originales ni host/SDK y sin hooks o escrituras directas no autorizadas.

La callback opcional de ActorService existe y alcanza la fase posterior a la creación nativa. No proporciona un setter de HP ni se conecta al registro añadido por StageService. Usarla para escribir `health` requeriría autorización nueva y resolver garantías de creación, identidad y cancelación; no se implementó ni se presenta como segura. El selector nativo sigue dando 40/220.

- [FEASIBILITY_GATE.md](FEASIBILITY_GATE.md): superficies, momento, identidad y decisión.
- [BLOCKER_REPORT.md](BLOCKER_REPORT.md): bloqueo preciso, campos de daño y alternativas condicionadas.
- [evidence/source-provenance.json](evidence/source-provenance.json): hashes y líneas de 21 archivos oficiales, 52 entradas del ledger CP02 y manifest histórico verificados.
- [evidence/preflight-and-results.json](evidence/preflight-and-results.json): GitHub, CI histórico y matriz de resultados.
- [RECOVERY.md](RECOVERY.md): recuperación y reproducción de la comprobación estática.

El usuario reporta PASS humano CP01 y CP02 para aparición/comportamiento y retirada tras cierre completo/reentrada. CP02: sesión `dusklight-20261013-214832.log`, solo CP02 v0.2.0 activo 1/1, registro result 0 / handle 1, sin ERROR/FATAL reportados. Este nuevo log no fue adjuntado ni leído aquí; no se publica. El usuario no midió 220 HP ni un multiplicador de daño. Se conserva esa distinción, sin retroeditar los informes anteriores.

CP03: revisión estática fundamentada; fake/lab y Windows build/package NO EJECUTADOS porque no hay implementación viable bajo el contrato. Runtime 150 HP **NOT_TESTED / NOT_VERIFIED**. No instalación, ejecución de juego, escrituras de actores, cambio de partidas ni CP04.
