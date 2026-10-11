# Fuentes y versiones — CP00
Autoridad: handoff maestro revisado adjunto, sección CP00. La petición actual autoriza retomar exclusivamente CP00; las instrucciones futuras del documento no autorizan CP01.

| Archivo original | Bytes | Entradas | SHA256 |
|---|---:|---:|---|
| dusklight-2.0.3.zip | 43245269 | 19861 | 9dbdc0b068df24c3fbb680c87be25e904978f04b315e2051e3c6203476516008 |
| Dusklight-v2.0.3-win32-x86_64.zip | 56037777 | 63 | ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf |

Ambos completos, CRC PASS, hashes coincidentes con handoff y OID LFS. Repositorio de insumos: https://github.com/iscoremusic26-maker/codex-cp00-inputs.git, revisión 72b61382d8518a9f727a974e18fae97ec44887fc. Copias locales en /workspace/codex-cp00-inputs.

Repositorio de trabajo detectado: /workspace/Mods-Duskligh, origin https://github.com/iscoremusic26-maker/Mods-Duskligh.git, rama work inicialmente sin commits. CP00 queda aislado en DEVF/; no se publica ni se modifica origin. No había checkpoints/análisis DEVF locales recuperables aparte del handoff; no se afirma acceso a conversaciones anteriores.

Árbol de fuente ya extraído: /workspace/setup-support/dusklight-2.0.3. Se cotejaron sus 19367 archivos con el ZIP: cero diferencias. Reutilizarlo sin modificar. El ZIP no contiene historial Git del upstream: no atribuirle un commit deducido de main.

EXE: PE32+ AMD64 0x8664, FileVersion/ProductVersion 2.0.3.0. Import library AMD64: 30042 short import objects apuntan a dusklight.exe; sus 30042 símbolos están exportados por el EXE, sin faltantes. Esto contrasta enlace, no demuestra ejecución ni layout runtime. Hashes de miembros y manifiestos nativos en evidence/input_verification.json. Paquetes oficiales usan lib/windows-amd64/mod.dll.

Referencias vigentes: sdk/, cmake/GameABIConfig.cmake, cmake/ModSDK.cmake, mods/custom_actor_demo/, include/, src/dusk/mods/svc/, src/d/actor/, libs/JSystem/. La distribución aporta el EXE y sdk/windows-amd64.lib exactos. 2.0.2 y AVE 1.3.1 son historial; no se consultaron. F_SP108 y coordenadas del demo son ejemplos oficiales, no una zona DEVF certificada.
