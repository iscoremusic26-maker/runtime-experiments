# CP17 0.14.0 — Registro humano Windows/DX12 (18 octubre 2026)

**Archivo original**: `dusklight-20261018-202114.log`
**Tamaño original**: 1,422,419 bytes
**Líneas originales**: 6,755 (LF)
**SHA-256 original**: `186616faec5a1e159faa22a0cdf7600ae82f1e866eed15492a951a2a9650f9b8`

El registro se conservó SIN EDICIONES en **17 partes consecutivas de texto UTF-8**, cada una contiene líneas completas y un LF final. Se dividió exclusivamente para su carga por GitHub; **ninguna línea se omitió ni modificó**. La suma de los tamaños de las partes es exactamente 1,422,419 bytes. La rama de evidencia fue creada a partir del HEAD documental PR74 `7abc4ca0f461f5756312b0e8ce56edb095797b08`, sin modificar código ni abrir/mergear PR.

## Ruta
`DEVF/CP17_RED_AGGRESSIVE_AI/evidence/HUMAN_RUNTIME_FAIL_2026-10-18/parts/dusklight-20261018-202114.log.part001` hasta `.part017`, nombres de tres dígitos.

## Reconstrucción exacta con Python
Ejecutar desde la carpeta `HUMAN_RUNTIME_FAIL_2026-10-18` tras clonar esta rama:

```python
from pathlib import Path
import hashlib

parts = sorted(Path("parts").glob("dusklight-20261018-202114.log.part*"))
assert len(parts) == 17
assert [p.name[-3:] for p in parts] == [f"{n:03d}" for n in range(1, 18)]
data = b"".join(p.read_bytes() for p in parts)
assert len(data) == 1422419
assert data.count(b"\n") == 6755
assert hashlib.sha256(data).hexdigest() == "186616faec5a1e159faa22a0cdf7600ae82f1e866eed15492a951a2a9650f9b8"
Path("dusklight-20261018-202114.log").write_bytes(data)
print("CP17_LOG_ORIGINAL_SHA256_PASS")
```

## Observaciones humanas sobre 0.14.0
- Los ataques de animación x3 de Red fallaron con frecuencia en registrar contacto contra Link o el escudo; en al menos un caso sí hubo daño.
- La reacción a la carga de Spin Attack / Jump Strike fue inconsistente y no incluyó una aproximación realmente acelerada.
- El registro muestra contadores agregados pero su detalle se saturó con `LINK_REACTIVE_SAMPLE_OBSERVED`; corregir esa telemetría antes de usarla para atribuciones individuales.
- El prompt FIX01 actualizado limita la **intercepción aérea** a **Jump Strike** y **Jump Attack normal con espada**, excluyendo otros ataques aéreos.
- No afirmar que un contador de rate o de colisión sin target demuestra impacto/escudo/interrupción. La nueva versión deseada usa **x2**, no x3.

**Solo evidencia**: no modificar fuente, mods, SDK, ROM, saves o checkpoints existentes en esta rama. Opus trabajará en la nueva rama FIX01 especificada en el prompt del usuario.
