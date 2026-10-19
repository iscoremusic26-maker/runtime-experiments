# Recuperación CP17

Base: PR73 draft sourceccc40ce68f9143ac71af7809653ed1d913be4516; realmente compilado FIX01e6b85b123e0895c23dce6415c54b8a25773e4504. CI58 ec88e78fdd45da95203d068e0709c467403b48d5. Nuevas ramas fuente/CI CP17 apiladas; sin modificar PR73/58, tags, paquetes o defaults. Sin merge/release.

Rollback: cerrar completamente Dusklight; retirar SOLO Expansion0.14.0 y restaurar BokoblinExpansion_0.13.1_CP16_FIX01_TEST.dusk,103638 bytes,SHA256f5d601f5e9d7a7f8e141a59aa1b0ee811bcbf2dfac16c1add6a40033e2e729b6. Mantener Provider/editor0.13.0 y JSON/saves respaldados. No instalar ambas Expansion, no hot-unload, no borrar configuración ni assets.

El código/policy/lab, source gate24 runtimefiles, CMake y CI están segregados en CP17. SOURCE_CI_CP17.json fija el source real y blobs del mirror; documentos históricos conservan su origen compilado explícito. SourceZip/ledger y VERIFIED_PACKAGE.json distinguirán implementación compilada del cierre documental posterior. Si se corta antes de CI/descarga PASS, no declarar paquete listo.

Siguiente acción mínima tras entrega válida: HUMAN_TEST, no CP18. Contacto/audio/escudo/lectura física de Link y éxito del intento reactivo requieren observación real. El boost1.5 de marcha no está implementado por el riesgo de prioridad en action(); no es una función oculta que se deba activar. CP14 canary permanece independiente.

## Checkpoint recuperable de entrega

Ramas feature/devf-cp17-red-aggressive-ai y ci/devf-cp17-red-aggressive-ai, PR74/59 draft. Fuente REAL compilada8fbaea77df4fe547676ca2462a6db633f3788273; CIa14ca4e264d7b629bb6b02745510300f16bc08ae. Run39184082946 SUCCESS ambos jobs, artifact12157032798 y verificador12157457479. VERIFIED_PACKAGE.json contiene hashes/tamaños, expiración real, toolchain, ABI y límites. El commit posterior de esta acta solo cambia docs; el SHA compilado sigue siendo el anterior.

Histórico de fallos preservado en TEST_RESULTS:39182819992 encoding,39183207051 helper EXE/GXDestroyTexObj,39183741446 lector COFF off-by-one. El último run corrige los tres sin alterar la IA ni relajar gates. Próxima acción mínima: HUMAN_TEST de Red solo, luego cargas/pasividad/mixed variants. No CP18. Cualquier problema físico de x3/lectura Link requiere reporte del usuario y rollback frío, no un PASS deducido de logs.

## Revalidación final en curso

Desde cierre7abc4ca0f461f5756312b0e8ce56edb095797b08 se corrigen dos casos de continuidad de política Red y se añaden regresiones. Source/CI/artifact finales se fijarán tras nuevo build+download. El artifact113055B del run39184082946 permanece intacto como snapshot previo, no como entrega más reciente. No cambiar el rollback FIX01 original.
