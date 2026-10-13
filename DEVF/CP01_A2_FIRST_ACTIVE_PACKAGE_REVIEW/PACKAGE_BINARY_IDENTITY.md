# Identidad binaria del paquete

**ACTIVE-CAPABLE / NOT INSTALLED / NOT RUN / SESSION NOT AUTHORIZED.**

Dusklight **2.0.3 Windows x64/DX12**; paquete ID`dev.devf.cp01_eoc_first_active_pilot` versión`0.0.1`; fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`.

Archivo`DEVF_CP01_E_OC_FIRST_ACTIVE_PILOT_windows-amd64_a67662bec0be8ac7982dd8685f9ac29cc1c0ebea.dusk`

ID`dev.devf.cp01_eoc_first_active_pilot` /version0.0.1

| Objeto | Bytes | SHA256 |
|---|---:|---|
| `.dusk` | 33897 | `f1475a82dc0d4783f2dcedd1d0748390733ff0f5006ddd54842691246397bd78` |
| DLL interna | 122368 | `26d07aae3f53151d105844f20f7be245f1dfcca120df51bcf239c8e3c449461b` |
| mod.json |330|`b14a16f582adf2dd3d8a1f38900345b83b8ab6747f23df2e11afd6ff9b8a8f67`|
| ZIP externo Actions |34520|`1f3956c2995e0243d9ad0f4280d8669ddc3c3958de0e8dba5439409dde796b53`|

Fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`; provider/core/test code también equivalente por hash a99b523c790ceecc747e385346e3419af4959e2f7 para reutilizar su laboratorio. CI`245c9eec99f7ff0186aac4174f04811cb9918b76`,run38435464736,job115428153522. SDK40457c6... oficial exacto; no modificación host/SDK/Aurora/lib. ABI1; Host2.2/Log1.0/Game2.0/Actor1.0; PE32+AMD64.

Cinco exports exactos: mod_ctx,mod_meta,mod_initialize,mod_update,mod_shutdown. Sin ordinal-only/forwarded/extra. Exactamente32 imports de juego decorados y conjuntos completos CRT/system idénticos al piloto previo; solo orden de tabla cambió por link graph de add_mod. Diferencia revisada en evidence/import-set-review.json; no permisividad por simple conteo. No StageService/HookService/delete/cancel/registro.

Map/disasm correlacionan NativeBackend::request [0x180003620,0x180003760), svc_actor0x18001f1f0 cargado en r10 y **único create slot32** `0x18000372F: call qword ptr [r10+20h]`. Dirección de nuestra DLL, no offset host. Provider current_admission rango[0x180003930,0x180003970): storeword101h=location/session true, storebyte[rcx+38h]=1=bindlive; Key inicialunknown, constantes del candidato. Cuerpo/link/callgraph reales conservados con /GL- y anchor.

DLL previaoffline`0afa4216...`,121856bytes, no es esta DLL122368bytes. No se fuerza igualdad ni se normalizan timestamps. La igualdad exigida es entre loose auditada, internaSDK y descarga del **mismo run**. Cualquier rebuild puede cambiar hashes por timestamps/tools; exige nueva verificación/manifiesto.

El ejecutable futuro sigue siendo el original52,309,504bytes/SHA`ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`; no se extrajo/cargó/parcheó ni compiló para esta etapa.
