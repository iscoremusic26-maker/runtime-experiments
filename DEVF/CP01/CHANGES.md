# Cambios exclusivos CP01
- Nuevo proyecto DEVF/CP01, actor Rock adaptado del demo oficial, nombre dvfrock y APIs/flags del SDK 2.0.3.
- Controller Actor/Stage y ResourceLifecycle con ownership, separación runtime/Stage y tratamiento de errores/cleanup.
- Module con imports versionados, guardas de host/política y diagnóstico acotado; ninguna aparición automática ni ubicación inventada.
- Laboratorio Windows de 16 casos, usando Controller/ResourceLifecycle reales y servicios/actor simulados; build CMake y workflow reutilizado de CP00.
- Verificación de paquete, imports/exports/PE y metadata, hashes y evidencia. .gitattributes de CP01 conserva LF; no cambia atributos/ZIP originales.
- Informes de etapa y guía futura de instalación/prueba/reversión, con NO-GO explícito. No TEST aprobado; build diagnóstica solamente.

CP00 y sus informes/tags/PR preservados; ramas nuevas CP01. No motor, EXE retail, ROM, save, .dzs/.dzr, otros mods, overrides de perfil retail, hooks, enemigos o CP02. No se ejecutó el juego, no se instaló en PC y no se repitió SDK Linux/CP00. No binarios originales en logs/artefactos. Licencia CC0 original se conserva como UPSTREAM_LICENSE.md y atribución de rutas en IMPLEMENTATION.md.
