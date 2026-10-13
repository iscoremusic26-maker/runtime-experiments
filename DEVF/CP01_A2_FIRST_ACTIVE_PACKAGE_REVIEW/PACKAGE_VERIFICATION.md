# Verificación del paquete real y descarga

**ACTIVE-CAPABLE / NOT INSTALLED / NOT RUN / SESSION NOT AUTHORIZED.**

Dusklight **2.0.3 Windows x64/DX12**; paquete ID`dev.devf.cp01_eoc_first_active_pilot` versión`0.0.1`; fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`.

Fuente`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`, workflow`245c9eec99f7ff0186aac4174f04811cb9918b76`, [run38435464736](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38435464736),job115428153522,success,attempt1. Solo jobactive-package. SDK oficial40457c6adb381928e4b5fef6ed459ed291edd5e2/Aurora3227d76c60e1e782ca576610bce61c9e7744d8be/importlib SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4,9400986bytes/CRC70c35731.

Tras build y auditoría PE/map/disasm PASS se ejecutó **devf_first_eoc_active_package**, regla real add_mod de cmake/ModSDK.cmake. No ZIP manual sustituto. Loose DLL SHA se registró antes; el package target no cambió sus bytes. Se comparó literalmente toda la DLL interna con la loose y se repitieron PE/exports/dumpbin internos. Nada se normalizó, reescribió o ejecutó.

Nombre`DEVF_CP01_E_OC_FIRST_ACTIVE_PILOT_windows-amd64_a67662bec0be8ac7982dd8685f9ac29cc1c0ebea.dusk`, id`dev.devf.cp01_eoc_first_active_pilot`, version0.0.1. mod.json byte-identical al fuente; descripción expresa creación nativa, ACTIVE-CAPABLE, experimental y sin permiso G5. No identidad G4B.

| Objeto | Bytes | SHA256 |
|---|---:|---|
| `.dusk` | 33897 | `f1475a82dc0d4783f2dcedd1d0748390733ff0f5006ddd54842691246397bd78` |
| DLL interna | 122368 | `26d07aae3f53151d105844f20f7be245f1dfcca120df51bcf239c8e3c449461b` |
| mod.json |330|`b14a16f582adf2dd3d8a1f38900345b83b8ab6747f23df2e11afd6ff9b8a8f67`|
| ZIP externo Actions |34520|`1f3956c2995e0243d9ad0f4280d8669ddc3c3958de0e8dba5439409dde796b53`|

Cuatro entradas SDK exactas: mod.json, lib/, lib/windows-amd64/, lib/windows-amd64/mod.dll. CRC manifest6377da46,DLL75cd5444,directorios00000000. Solo dos archivos funcionales. No originales/EXE/LIB/recursos/labs/logs privados/debug/instalador/otraDLL. Directorios/atributos, rutas, tamaños, CRC, SHA y unicidad/casealias auditados; symlink/encrypted/traversal/especial/extras rechazados.

[Entrega privada real11832392953](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38435464736/artifacts/11832392953),34520bytes, expira2026-11-12T17:03:55Z (**12:03:55 Panama UTC−5**). Artifact externo exactamente `.dusk` + DOWNLOAD_MANIFEST.json. `creation_capable=true`, `provider_armed_in_binary=true`, `installed=false`, `runtime_tested=false`, `execution_authorized=false`, `G5=NO_GO`, `CP02=NO_GO`. Copia externa versionada, no dentro del .dusk.

Descarga efectivamente recibida y leída: SHA ZIP coincidente con digest API; CRC exterior; SHA/bytes paquete y DLL; manifest byte-identical también al artefacto textual independiente; CRC/members exactos; PE/exports/imports repetidos sobre DLL extraída en scratch con permisos0600, sin cargarla. Whole DLL SHA coincide con la loose auditada y, por ello, con su mapa/disasm. `DOWNLOAD_VERIFIED` evidencia/evidence/download-verification.json; herramienta ci/verify_download.py. Tres negativos sobre ese download rechazan digest falso, workflowmanifest distinto y DLLhash esperado falso, sin extracción DLL en esos casos.

[Texto11832716912](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38435464736/artifacts/11832716912):255743bytes,SHA`c8f96624035ce0c8a3df2fcd0d02b469cf777cddfd5c8b1cb308c01ab54677ab`,23 archivos/22 hashes internos, CRC PASS. Todos preservados en evidence/windows-run-38435464736/; Actions puede expirar sin borrar esta evidencia textual. Archivos originales solo en privado y .lib en scratch del runner. No DLL/.dusk comprometidos en Git.

La verificación de descarga es análisis ZIP/hash/PE en Linux, no simulación del compilador ni prueba de juego. Windows build/link real ocurre en Actions. Ubicación/render/colisión/cleanup/DX12 siguen sin ensayo de esta DLL.
