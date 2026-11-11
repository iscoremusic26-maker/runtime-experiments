# Perfiles de CI

El perfil se elige con el archivo `POSTURE_SYSTEM/POST05_CI_PROFILE.txt` del repositorio de CI: `fast`, `integration` o `full`. Se commitea y se empuja, de modo que queda en el historial.

| Perfil | Trabajos | Qué ejecuta | Publica `.dusk` |
|---|---|---|---|
| `fast` | `gate`, `finalize` | Procedencia, auditorías de texto, anclas de mutantes, negativos críticos, compilación MSVC, auditoría PE, prólogos, escritores, laboratorios del código cambiado, empaquetado | No |
| `integration` | + `labs` | Además: todos los laboratorios, adaptadores, negativos restantes, benchmarks, renders | No |
| `full` | + `mutants`, `independent-download` | Además: todos los mutantes en 8 trabajos y la descarga independiente | Sí |

## Reglas

- Solo un `full` puede dar nombre al paquete. Los otros perfiles terminan en `PARTIAL_*_NOT_DELIVERABLE`.
- `finalize` comprueba que cada etapa pertenece a la misma ejecución y a la misma fuente, y que ejecutó exactamente su lista declarada. Suma los fragmentos de mutantes y los compara con el total.
- El binario lo construye y audita `gate`. `finalize` comprueba su hash antes de publicarlo: los mutantes no recompilan el producto.
- No se cachea ningún resultado de prueba o auditoría.
- Un cambio posterior a un `full` exige otro `full` del nuevo commit.
- `CI_INVENTORY.json` lista etapas, fases, duración, omisiones y sus motivos.

## Por qué es más rápido

Antes todo corría en serie en una máquina: unos 47 minutos en FIX04 y 62 en FIX03. Ahora los errores baratos salen en `gate`, y las suites independientes corren en paralelo en runners distintos, cada una con sus directorios temporales.
