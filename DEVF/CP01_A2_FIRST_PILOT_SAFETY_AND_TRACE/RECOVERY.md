# Recuperación del piloto offline

Base obligatoria `befd909fd8229ef106d2f520368f7841b22fd749`, tag DEVF_CP01_A2_FIRST_NATIVE_REQUEST_OFFLINE_VERIFIED. #16 permanece intacta. Rama nueva **preparation/devf-cp01-first-eoc-pilot-safety**; [PR17 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/17),sin merge. Tag nuevo de recuperación: **DEVF_CP01_A2_FIRST_PILOT_SAFETY_TRACE_VERIFIED**; resolver el commit final mediante ese tag. Fuente compilada definitiva639d4780aeb15c17d9723babb5ff4c8d64c19a9d, distinta del checkpoint final solo por textos/herramientas de verificación.

[PR11CI draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/11),base ci/devf-cp01-first-native-offline@7a33a26b084aed794108d281d5cad84de7d69d37,head ci/devf-cp01-first-pilot-safety@0b7b517ff2fdce5a0964cbc1dbd91d4a27525b28. Se revisaron diff/triggers antes de abrirla: solo carpeta nueva y workflow nuevo; cinco filtros históricos disjuntos. Dos runs del único job pilot-offline, fallido y corregido, ambos documentados. Nada se abrió contra main ni se fusionó.

```bash
git fetch origin refs/heads/preparation/devf-cp01-first-eoc-pilot-safety:refs/remotes/origin/preparation/devf-cp01-first-eoc-pilot-safety
git fetch origin refs/tags/DEVF_CP01_A2_FIRST_PILOT_SAFETY_TRACE_VERIFIED:refs/tags/DEVF_CP01_A2_FIRST_PILOT_SAFETY_TRACE_VERIFIED
git switch --detach DEVF_CP01_A2_FIRST_PILOT_SAFETY_TRACE_VERIFIED
```

Para reconstruir offline: checkout privado inputs0b7b517...,GitLFS original Windows ZIP,SDK40457c6...yAurora3227d76...; DeveloperShellMSVCx64/WindowsSDK, comando en TEST_RESULTS. ci/windows-offline.yml reproduce el workflow real. No instalar ni cargar la DLL. No repetir las suites previas o compilar el host.

ci/overlay-edits.json y build_overlay.py generan copias de nuestras fuentes antiguas solo en build; sustituciones únicas y hashes/diff verificables. NativeBackend y admission son byte-equivalentes; el reader recibe únicamente la extensión escalar del mismo visitor. Las carpetas originales permanecen sin cambios: historical-integrity.json registra277 archivos. SDK/Aurora/host se conservan; las referencias históricas no se sobrescriben. Fuentes compiladas19, reutilizadas21 y siete overlays verificados contra artefactos.

Evidencia textual de ambos runs, manifiesto SHA/CRC, PE/disasm/map, requestslot32 y hashes en evidence/. Artefactos Actions pueden expirar; Git conserva el texto completo. Sin DLL/EXE/LIB/.dusk/ROM/ARC/ZIP de entrada, saves ni log privado. Herramienta verify_checkpoint.py permite comprobar hashes de un fetch independiente. recovery-verification.json certifica el parent publicado y el protocolo para verificar el tag final después de publicarlo, sin afirmaciones circulares.

Para un paquete activo faltan revisión/autorización separadas, provider de sesión explícito y nuevo build/PE/package audit; para ejecutarlo falta autorización de la sesión cold-start G5. No generar prompts, ejecutar juego, alterar progreso ni CP02 en esta etapa.
