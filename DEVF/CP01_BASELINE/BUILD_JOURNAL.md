# Checkpoint intermedio — baseline configurado

Esta observación corresponde al 12 de octubre de 2026, 08:43 (Panamá). No es un PASS final de compilación.

- Source oficial limpio: raíz40457c6, tagv2.0.3 y los cuatro gitlinks exactos; relación con ZIP registrada.
- Intento1, run38256216502: vcpkg PASS en121.468s; preflight falló en hash raw por EOL nativo del checkout Windows. Configure/build no ejecutados. Artefacto recibido, SHA/CRC comprobados y datos propios guardados en evidence/attempt1.
- Corrección únicamente de infraestructura: core.eol=lf antes del nuevo checkout. Respeta excepción .batCRLF. No altera source ni aplica patch.
- Intento2, código CI65c9b8b47f38ea966f5cb69fbc2e5b2623a785ba: run [38256856294](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38256856294), job114837029572. vcpkg, preflight de source/tools y configure oficiales: PASS; build/install EN CURSO.
- Los ocho ports del intento1 son freetype2.14.3, zstd1.5.7, libpng1.6.58, zlib1.3.2#1, brotli1.2.0, bzip2 1.0.8#6, vcpkg-cmake2024-04-23 y vcpkg-cmake-config2026-07-21. Sin ports agregados por conveniencia.

Si se pierde el entorno, recuperar esta rama, inspeccionar primero el run actual y descargar su artefacto textual. No relanzar antes de conocer su resultado. No aplicar el parche, repetir auditorías ni cambiar DEVF. Solo concluir BASELINE_BUILD_PASS si termina build/install con EXEAMD64, root/gitlinks/hashes originales y source limpio; en otro caso BASELINE_BUILD_BLOCKED con causa real.

DISARMED_NO_REGISTRATION, CP02 NO-GO, sin ejecución del juego. La preparación install es staging del runner; nada se instala en la PC del usuario ni se distribuye binario.
