# Entrega más reciente — hotfix CISO +576 B
[Descargar ZIP privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38954973078/artifacts/12069682536) · [Run / Artifacts](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38954973078).
Artifact **DEVF_CP09_IMPORTER_TEST_38954973078**, ID12069682536; caduca **15-11-2026 14:27:58 America/Panama** (2026-11-15T19:27:58Z).

| Archivo | Bytes | SHA256 |
|---|---:|---|
| DEVF_CP09_IMPORTER_TEST.zip, ZIP interior | 65713914 | 61480beed1b28be932bbbf992c14c738827b4e152841bce0daabe80df1eab65a |
| DEVF Map Editor CP09.exe | 161844757 | 5a08548f038dcee8caf3e74be5d8369651e4484d9f6d516a9dcd0c484e25a9d3 |

Fuente compilada 3b45f2f50c65f98f0f9b880bc8d1ec7cc9829416; CI c6e20919e0f0d9ae3139879974c4e50220b1e429. Build e independent-download SUCCESS,113 casos de aplicación +2 negativos PE PASS. El cierre documental posterior no se recompila. Se conserva la versión CP09 0.9.0 TEST; identifique este hotfix por sourceSHA y hash del EXE. Extraiga en una carpeta nueva y cierre el editor anterior antes de abrirlo.

Incluye el EXE autónomo y fuentes/manifiestos/instrucciones; no contiene .dusk ni recursos del juego. El ZIP exterior de GitHub envuelve el ZIP TEST interior de la tabla. Evidencia adicional: evidence/ciso-tail-hotfix-verification.json. CISO_REAL_IMPORT_HUMAN_PENDING.

---

## Entrega CP09 anterior conservada
# Paquete CP09 0.9.0 TEST
[Descargar artifact privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38918182460/artifacts/12053167316) · [Página del run y sección Artifacts](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38918182460)
Nombre: DEVF_CP09_IMPORTER_TEST_38918182460; ID 12053167316. Se necesita acceso al repositorio privado.

| Contenido | Bytes | SHA256 |
|---|---:|---|
| DEVF_CP09_IMPORTER_TEST.zip (ZIP interior) | 65705384 | 24a65ebdd9b384d0aeeed166bf74592983a49aaf9edad3c44c4aec6542e56351 |
| DEVF Map Editor CP09.exe | 161840661 | d6aa54a97aa08dfa1c08eb2205ac6966ca49fade67ec490d1769e4909ea6cb90 |

Expiración API: 2026-11-15T14:46:03Z = 15 noviembre 2026, 09:46:03 Panamá.
El ZIP exterior descargado por GitHub envuelve el ZIP TEST interior; su tamaño/hash no es el de la fila anterior.

Fuente compilada: b9ea7518684126b733532cb0a99a0e3b98d4d74e; CI: 04e87f713f1d96301d7ede29cda9628ba8fa84f9. El cierre documental posterior no se recompiló.
Build net8.0-windows con SDK8.0.426, self-contained AMD64, archivo global.json y ledger de blobs exactos. Ninguna compilación MSVC necesaria: CP09 contiene C# y no modifica DLLs/mods/SDK del juego.

Contenido: ejecutable autónomo, README/HUMAN_TEST/RECOVERY/IMPLEMENTATION/CP10_HANDOFF, MANIFEST.json, SHA256SUMS.txt y SOURCE_COMPILED.zip. No se incluyen .dusk, binarios oficiales, geometría ni discos. El SourceZip contiene código propio y Config.cs histórico sin cambios; los fixtures de disco se generan sintéticamente en tests y no se distribuyen como discos.

El segundo runner descargó el artifact publicado y recalculó tamaño/SHA/CRC; comparó PE, manifiesto y cada fuente empaquetada contra el ledger. Evidencia resumida en evidence/verification.json.
