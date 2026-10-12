# Análisis local de ubicación CP01

Herramientas propias de lectura: Python 3.9+ y biblioteca estándar. No son un mod ni ejecutan host. No activan ActorService/StageService.

ZIP/manifiesto íntegros privados; directorio de trabajo fuera del repositorio de código. Contendrá recursos y tablas completas privadas: no subirlo a Git, logs o artefactos públicos.

```bash
export DEVF_CP01_LOCATION_WORK=/workspace/work/cp01-location
python DEVF/CP01/analysis/analyze_location.py --inputs /workspace/codex-cp00-inputs
python DEVF/CP01/analysis/location_geometry.py
python DEVF/CP01/analysis/location_details.py
python DEVF/CP01/analysis/verify_footprint.py
python DEVF/CP01/analysis/location_spatial.py
```

SHA256/CRC/tamaños y límites se comprueban antes de decodificar. KCL: prismas stride 16/primer registro reservado. Rutas: puntos relativos a RPPN. GetTriPnt, semiplanos GroundCross con tolerancia 0.0075, árbol KCL, PLC, joint BMD y SAT se documentan en LOCATION_ANALYSIS.

Candidato en verify_footprint solo entrada de análisis yaw 0/escala 1, nunca configuración. geometry compara cuadrícula; suma de áreas no prueba unión. Cobertura definitiva: resta de semiplanos, 441 consultas por envolvente y contraste baricéntrico. Double estático no equivale a ejecución float del motor.

No certifican scripts/global callbacks ni geometría dinámica ausente. location_spatial cubre contratos identificados; no simula todos los actores.

No recompilar Windows por estos informes: módulo/política intactos. Evidencia MSVC/seguridad histórica conservada sin repetir suites.

## Solo pendiente incremental de consumidor de ruta7

Si inventory.json y footprint-verification.json siguen en el directorio privado, no ejecutar otra vez las cinco herramientas anteriores. Ejecutar únicamente:

```bash
python DEVF/CP01/analysis/location_digpoints.py
```

Usa los resultados conservados y room.dzr para confirmar ACTR[5]/Digpl y medir sus27 puntos. La distancia histórica a segmentos no equivale a trayectoria dinámica de este actor. Solo si se pierde el directorio temporal deben reconstruirse las entradas de análisis necesarias con los scripts iniciales y los mismos hashes privados.
