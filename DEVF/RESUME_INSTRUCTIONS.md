# Reanudar tras CP00 Windows
1. Recuperar rama checkpoint/devf-cp00-windows-20261011 o tag DEVF_CP00_WINDOWS del repo Mods-Duskligh. El tag DEVF_CP00 original sigue apuntando a 8a14628.
2. Leer handoff, GO_NO_GO, TEST_RESULTS y evidence/windows-verification.json. CP00 tiene GO técnico; Windows juego/DX12 permanecen NOT_TESTED. CP01 no autorizado por este checkpoint.
3. Para repetir build Windows, usar PR #1/rama cp00-ci/windows-msvc-20261011 en codex-cp00-inputs, workflow_dispatch o nueva actualización de PR. Mantener hashes ZIP, Aurora 3227d76..., MSVC/Windows SDK y target _package. No necesitar token entre repositorios. Confirmar que copia del probe coincide con su CP00_SOURCE.json.
4. Artifact final: run 38184306482 / artifact 11718469244, retención 14 días (vence 2026-10-25). Hashes propios y log durable también en repo principal. No instalar como TEST ni ejecutar el juego sin encargo.
5. Si se autoriza CP01, partir de custom_actor_demo según handoff y verificar loader/ciclo de vida seguro. No repetir smoke Linux, análisis 2.0.2 ni modificar originales.

> Nota de navegación (2026-10-17): documento histórico de CP00. El estado actual del proyecto (CP08–CP10) está en `DEVF/TRANSFER_01_HANDOFF_2026-10-17.md`.
