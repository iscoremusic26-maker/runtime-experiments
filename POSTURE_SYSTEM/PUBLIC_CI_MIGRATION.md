# Migración a repositorios públicos (2026-11-12)

## Repositorios
| Uso | Público (activo) | Privado (respaldo, intacto) |
|---|---|---|
| Fuente | `iscoremusic26-maker/runtime-experiments` | `iscoremusic26-maker/Mods-Duskligh` |
| CI / builds Windows | `iscoremusic26-maker/windows-build-lab` | `iscoremusic26-maker/codex-cp00-inputs` |

Las copias públicas conservan todas las ramas (145 + 116), etiquetas (46 + 2), commits (559 + 303), mensajes, nombres y fechas. El historial se reescribió **solo en las copias públicas**, así que los SHA no coinciden con los privados. La tabla `old → new` está guardada en local, fuera de Git.

Se excluyó del historial público:
- ARC del juego: `E_oc.arc`, `E_ocb.arc`, `E_oc2.arc` y los ZIP LFS `DEVF_CP01_EVIDENCIA_F_SP121.zip` y `DEVF_CP01_EXTRA_COLLISIONS.zip`.
- Grabaciones de audio original: `*_AUDIOS_ORIGINALES.zip` y `*_AUDIO_ORIGINALES.zip`.
- Logs de Dusklight en tiempo de ejecución (`dusklight-AAAAMMDD-HHMMSS*.log`), que contienen rutas personales.
- El ZIP binario oficial `Dusklight-v2.0.3-win32-x86_64.zip`. Ahora se descarga en cada build desde la release de TwilitRealm, comprobando su SHA-256 `ac63514e…2caf`; es el mismo archivo byte a byte.

También se redactaron las rutas con el nombre de usuario local (`C:\Users\<user>`, `/home/<user>`) y los correos personales de autor, committer y tagger pasaron a ser `noreply` de GitHub. Las firmas de GitHub web-flow se pierden al reescribir.

## CI público
- El workflow `ci/windows-post05.yml` (copiado en `.github/workflows/light-fades-twice-chilfos-fix05-0-13-5.yml`) solo corre si se cumple todo esto:
  - `github.repository == 'iscoremusic26-maker/windows-build-lab'`;
  - `github.event.repository.private == false`;
  - `github.event_name == 'push'`;
  - la rama es `ci/light-fades-twice-chilfos-fix05-0-13-5`.
- Usa runners estándar `windows-latest`. Los perfiles, tests, mutantes, auditorías PE, el `.dusk` y la descarga independiente son los mismos que antes.
- No necesita secretos: los checkouts son de este repo, de `TwilitRealm/dusklight` y de `encounter/aurora`, con los mismos pins de antes.

## Lanzar FAST, INTEGRATION o FULL
1. Trabaja en `runtime-experiments` (rama de la fuente) y haz push allí.
2. En `windows-build-lab`, rama `ci/...`, copia `src/`, `tests/`, `ci/`, `CMakeLists.txt` y `mod.json` a `POSTURE_SYSTEM/POST05/`.
3. Regenera `POSTURE_SYSTEM/POST05_CI_SOURCE.json`: `source_repo` = `iscoremusic26-maker/runtime-experiments`, `source_commit` = HEAD de la fuente, más los hashes.
4. Escribe `fast`, `integration` o `full` en `POSTURE_SYSTEM/POST05_CI_PROFILE.txt` y haz push. El push lanza el run.
5. Descarga el resultado con `gh run download <run> --repo iscoremusic26-maker/windows-build-lab --name LIZ_TEST_<run>_<attempt>`.

## Volver a los privados
Los privados no se tocaron y siguen siendo válidos con sus SHA originales. Para volver a usarlos, trabaja en los clones y worktrees privados de siempre (`devf/…`), cuyo `origin` sigue apuntando a ellos. El CI privado consume minutos de pago, así que solo vale la pena para algo que no pueda ser público.
