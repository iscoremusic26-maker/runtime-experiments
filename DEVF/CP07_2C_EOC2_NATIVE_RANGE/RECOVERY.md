# Recuperación CP07.2C
Base inmutable 7c588d2a06d307b0288256fc2383186129430401, PR46 permanece draft/sin merge.
Nueva rama: feature/devf-cp07-2c-eoc2-native-range-5000. Fuente compilada 02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd; padre 7c588d2a06d307b0288256fc2383186129430401. El checkpoint pre-QA e2e937b060700801f04143624abd3217a3664db4 tiene ese source como padre. El encargo humano 684d027c1c73be5d083dfa6754e10fe3fc2ae066 es hijo del pre-QA y añadió sólo su Markdown; el cierre humano añade únicamente documentación sobre ese HEAD. Obtener su SHA exacto de PR47, sin confundirlo con el compilado. CI build 1c1a96cffbdf80199570423addec4c91ded46865; CI verificador 162e988157af120ee8f87fdc82dba6e90c33bb55.
No rebase/reset/amend/force/merge/retag. CP00–CP07.2B y siete tags históricos se preservan.
Rollback proveedor 0.7.3: .dusk 129906 bytes SHA256 398384e83b416aca0a791bac18d1a4e92b8a68d34aec9c278e5c8f343bed1358.
Consumidor 0.1.0 INALTERADO: .dusk 24439 bytes SHA256 104a6c0908f498b0a833b7ed31d12e75f224bc2f232633bd921446c217d2333f; ZIP SHA256 2fdbec7cdccf0bc9ececcfc7251cc2bb3fa8259deed95178310eec39de279ce8.
[Artefacto consumidor histórico](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38801130769/artifacts/12004087737); fecha histórica de caducidad 2026-11-14 15:23:17 Panamá, comprobar disponibilidad por API. No reempaquetar ni recompilar como requisito de este test.
Cloud falló aprovisionamiento; usar sólo conector GitHub/Actions autorizados. Ninguna shell ni ejecución de juego se presume.

## Estado recuperable
- [PR47 principal](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/47), rama feature/devf-cp07-2c-eoc2-native-range-5000; [PR33 CI](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/33), rama ci/devf-cp07-2c-eoc2-native-range-5000; ambas draft/sin merge.
- [Proveedor 0.7.4 verificado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812099184/artifacts/12009156482): 129925 bytes, SHA256 934a0a1a5127fa994b9325a5f94a493d0df53f3b5f9af9acfce3709006379fbb.
- ZIP 280547 bytes, SHA256 89258783b1d776d762f6b62c71d8bb1cefdd9086f8c3771ddec09ab137278464, vence 14-11-2026 16:45:50 Panamá según API.
- [Build](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812099184) y [descarga independiente](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812605127) SUCCESS.
- Intento de verificación fallido 38812467385 preservado: normalización de orden físico modmeta; no reconstruir proveedor por ello.
- 1599 de1603 archivos anteriores idénticos por path/blob/mode/type; sólo cuatro rutas previstas cambiaron. Consumidor entero y legacy native_records/registration idénticos; siete tags anotados leídos y conservados. [Auditoría](evidence/integrity.json).
El antiguo paso siguiente era QA A_ONLY/BOTH; ya se recibió la observación humana y se cerró como **CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12**, acotado. Ver [acta humana del 15-10-2026](HUMAN_RUNTIME_RESULTS_2026-10-15.md). No repetir QA ni iniciar nuevos ajustes, hooks, variantes o eliminación de executeWalk/home. Continuar con la próxima funcionalidad sólo cuando se autorice.
Este cierre no crea CI/paquete ni tags ni modifica PR33/46. Históricos y hashes anteriores permanecen; los originales de los logs siguen fuera del repositorio.
