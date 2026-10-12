# Recuperación del checkpoint experimental CP01

Tag principal: `DEVF_CP01_HOST_LIFETIME_EXPERIMENT`. Rama: `experiment/devf-cp01-host-lifetime`. Base preservada: `5f3a7ef` / `DEVF_CP01_EXTRA_COLLISIONS_REVIEW`. Los anteriores commits/tags no se mueven. El commit final se obtiene resolviendo el tag anotado; evitar confundir su objeto tag con el commit.

En un checkout independiente, sin sobrescribir trabajo existente:

```sh
git clone https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-host-review
cd devf-host-review
git fetch origin tag DEVF_CP01_HOST_LIFETIME_EXPERIMENT
git switch --detach DEVF_CP01_HOST_LIFETIME_EXPERIMENT
git rev-parse DEVF_CP01_HOST_LIFETIME_EXPERIMENT^{commit}
git merge-base --is-ancestor 5f3a7ef HEAD
```

El source experimental no se aplica al mod ni al ejecutable. En la sesión de trabajo los 12 originales afectados se conservaron como baseline Git independiente en `/workspace/work/devf-host-lifetime`, rama `dusklight-2.0.3-original`. El ZIP fuente privado intacto y `SOURCE_MANIFEST.json` permiten reconstruir ese baseline si desaparece el entorno temporal. No se sube el árbol original a Mods-Duskligh.

La reproducción del **laboratorio**, separada de la integración, usa el repositorio privado de inputs. Resolver `DEVF_CP01_HOST_LIFETIME_LAB_MSVC` a `b9f03cbe10144c8ea240758dfae0f74917951891`, y ejecutar en Windows los comandos de TEST_RESULTS; ese snapshot mantiene también el workflow y la fixture propia. El artefacto de Actions expira; los logs resumidos/hashes están versionados aquí. Se necesita acceso privado al repo y LFS únicamente para el ZIP fuente. No usar el ZIP binario del juego ni exportar originales como artefactos.

Antes de **integrar el host**, conseguir el checkout 2.0.3 con gitlinks, Borealis/Aurora y dependencias transitivas exactas; comprobar `evidence/dependency-preflight.json`. No sustituirlos por HEAD sin acreditar correspondencia. Preparar una copia del source y guardar en Git el baseline original antes del patch. `ci/prepare_experiment.py --source <copia> --out <temporal>` rechaza originales o patch distintos de los hashes esperados. Sus archivos `.inc` contienen source extraído y deben permanecer privados/temporales; no son entregables públicos.

Reversión: conservar los checkouts originales y descartar solamente el checkout experimental independiente. No instalar nada, aplicar parches a EXE, modificar saves o usar reset/clean en un árbol con trabajo ajeno. DEVF permanece DISARMED_NO_REGISTRATION. No activar TEST ni avanzar CP02.

Siguiente paso mínimo: integrar/compilar el host experimental Windows con las dependencias exactas, y verificar el drenado real y el orden de teardown antes de considerar una prueba activa. La ubicación tiene condiciones pendientes independientes ya documentadas, sin nueva investigación en esta revisión.
