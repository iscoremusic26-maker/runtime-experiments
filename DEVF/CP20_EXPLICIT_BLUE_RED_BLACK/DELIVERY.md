# CP20 — entrega verificada

[Paquete privado de Windows](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39325015857/artifacts/12222186921) · [Fuente DRAFT #80](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/80) · [CI DRAFT #65](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/65)

Pareja obligatoria: **Provider 0.14.0 + Expansion 0.16.3**; editor **0.14.0**. Un solo paquete por mod ID, juego cerrado y arranque frío. Respaldar encounters.json y saves antes de probar. El ZIP incluye las guías HUMAN_TEST y RECOVERY.

Estados: `SOURCE_IMPLEMENTED` / `LAB_PASS` / `WINDOWS_MSVC_PASS` / `INDEPENDENT_DOWNLOAD_PASS` / **`HUMAN_RUNTIME_PENDING`**. No se ejecutó el juego.

Fuente compilada: `2ce550395ff69d2c9046a2d3e0b635024307ce1e`. CI: `d8b07d029c4f98ca62d4d2eaaf935d87eea290d2`. [Ejecución Windows exitosa](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39325015857).

Validación: 141 casos C++ CP20, 85 documentos compartidos entre parsers, 110 casos C# CP20, 9 casos contra el parser anterior, regresiones completas FIX02, ABI C/MSVC/COFF, GUI y mapa sintético, auditorías PE/.dusk y descarga independiente. Localmente también pasan 559 casos históricos y 35/35 controles de mutación FIX02.

El artifact privado caduca el **18 de noviembre de 2026, 16:12:05 (Panamá)**. La descarga de GitHub contiene un ZIP exterior y dentro `DEVF_CP20_EXPLICIT_BLUE_RED_BLACK_TEST.zip`; sus hashes son diferentes.

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| ZIP exterior de GitHub | 68491353 | `b294de1310806fe7afb03229aa4b42d0b011b7dc467f632b592eeb376bd88455` |
| ZIP de prueba interior | 68839714 | `96e3710fe62325c6527071b24eebf433d8470e7d510c01f8f39d8594c7abff79` |
| BokoblinExpansion_0.16.3_CP20_TEST.dusk | 154219 | `717e80a4c289fccd1f6b8004b5bdf83a74a23b21c6eb10449565c5d2753036b5` |
| DEVF_Provider_0.14.0_CP20_TEST.dusk | 130685 | `38a581161efb85d7e1ab7efc1382474892143676c936f5ebc3353d5cfdf13609` |
| DEVF Map Editor CP20.exe | 161984023 | `7c38b5fccd834bed8e4097f98aa0c5f04a1511e656ce0a185ab45be33d2d96c0` |

El Blue heredado sigue siendo E_OC2/Blue 220. Blue auténtico usa E_OC/220 y Red E_OC2/330; Black conserva HP configurables y FIX02. Las conversiones requieren confirmación, copia previa y nueva QA. Los JSON de ejemplo del ZIP son sintéticos y disabled; importar geometría local real antes de crear pruebas.

La captura incluida muestra únicamente el mapa sintético del laboratorio. La comprobación humana pendiente debe cubrir modelos, audio, IA, daño, escudo, transiciones, mezcla con nativos y coexistencia con Zora Swim; no hay afirmación de cobertura universal.
