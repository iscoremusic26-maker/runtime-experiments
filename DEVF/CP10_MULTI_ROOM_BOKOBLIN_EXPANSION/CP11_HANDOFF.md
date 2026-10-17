# Handoff limitado
CP10 es F_SP121, máximo8 global, schema1 compatibilidad y schema2 QA de recursos/layers explícitos. No habilita F_SP113/F_SP117.
Antes de CP11 se necesitan resultados humanos separados para sala/capa nuevas y revisión concreta de disponibilidad E_OC2, recursos, ciclo y coordenadas en cada escenario. La API mantiene ABI1.0; no ActorId ni gameplay inferido.
No implementar multistage, atlas, >8 o hot reload sin un encargo posterior. Mantener importador CP09 y rollback CP08.

## Actualización de estado — 2026-10-17
Resultados humanos CP10 (USER_TESTIMONY): F_SP121/R03/L6 y F_SP121/R01/L6 observados; sin multi-stage. Corrección: el host oficial (40457c6, `stage.cpp`) ya indexa las ediciones por nombre de escenario, de modo que la restricción a F_SP121 está en el código DEVF; no se asume que haya que modificar el host, y el multi-stage DEVF no está demostrado. CP11 sigue sin autorizar. Ver `DEVF/TRANSFER_01_HANDOFF_2026-10-17.md`.
