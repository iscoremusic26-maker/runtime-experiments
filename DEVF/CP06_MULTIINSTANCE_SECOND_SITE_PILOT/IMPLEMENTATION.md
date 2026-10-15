# Implementación real y alcance
**NO_GO_MULTIINSTANCE. Ninguna funcionalidad del mod fue modificada.** Parser/schema1, max_active=1, whitelist sitio1, mod_id/version, hooks de color/HP/AI y dos presets alternativos permanecen intactos. No nuevo owner multiinstancia, callback de creación, epoch general, factory hook, token setID/parent_id o uso de ActorService.create_actor.

Nuevas herramientas de sólo lectura en commit `a94eba477869a6a203949366945414a309e3902b`:
- ci/site_query.py adapta la consulta anterior a X/Z de entorno, reutilizando lectores inmutables.
- ci/review_sites.py lee sólo R03 del ZIP LFS privado, comprueba procedencia y consulta dos centros en cache RUNNER_TEMP fuera del código. Resultado éxito significa estudio completado, no sitio admitido.
- ci/previous-volume-bounds.json contiene metadata derivada anterior con origen, nunca assets.
- evidence/site-query-summary.json resume datos reales del job; external-bounds-reuse.json registra cálculo JavaScript de AABB autoradas previas, sin ARC nuevo.

Workflow principal nuevo `.github/workflows/devf-cp06-single-site-human-tag.yml`: fuente db254b9fa7d2714e4bb647b1880cac11b18fa5ba. Restricción repo privado/rama/base literales, checkout fijo3ab8ff2…, validación padre/cinco Markdown/seis tags y push no forzado del único tag humano. No ejecuta código del PR, build ni scripts del repo.
Workflow NUEVO de inputs de estudio: contents:read, PR25/base/rama restringidos, LFS selectivo; no permisos cross-repo supuestos, build ni artifacts. Ambos workflows históricos permanecen intactos.

CI de estudio ejecutado realmente: `98bbb027c91e4cabc9629f370971345c887a958c`. Helpers CP01 copiados al CI sin cambios y comparados por blob; no se alteran sus fuentes en principal. No nuevas pruebas fake de dos owners sobre una DLL que aún sólo admite uno. Fases4/5 de config doble/MSVC/PE/package no habilitadas al fallar procedencia. No juego/host/SDK/Aurora/ROM/saves modificados.
