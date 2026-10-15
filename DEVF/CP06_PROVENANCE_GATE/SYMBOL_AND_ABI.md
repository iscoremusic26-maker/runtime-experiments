# P1 — símbolo y ABI exactos medidos, no sólo source-only

**P1 PASS para la entrada opaca elegida, mediante evidencia estática del binario exacto. Instalación de hook/callback/game runtime NOT_TESTED. P2 sigue NO_GO.**
No se certifica layout interno de ActorEditRecord, LoadedMod o STL, ni acceso a su buffer.

## Procedencia real y reproducción
[Run38749877215](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38749877215), job116473164418 SUCCESS; fuente CI **9b4930b3bab0a6437b17ce99e3f232f724823a5f**. Checkout explícito de ese HEAD, GITHUB_SHA de evento era merge temporal6f6a462263e5562a13f2bc851cdf3dedb1b108ef y **no es la fuente ejecutada**.
Fuente del probe principal inicial9eee5b975d8d43df79693e98337b826b194a9ee9; versión final se refleja en el checkpoint de esta rama y coincide por blob con CI.
Comandos: `git lfs pull --include=Dusklight-v2.0.3-win32-x86_64.zip`; `python DEVF/CP06_PROVENANCE_GATE/ci/inspect_transfer_symbol.py`. Sólo binario aprobado leído desde ZIP privado, nunca ejecutado/cargado/parcheado. Sin ARC ni logs de usuario.

| Input/resultado | Identidad comprobada |
| --- | --- |
| ZIP Windows | 56037777bytes; SHA256 ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf |
| EXE | 52309504bytes; SHA256 ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049; CRC miembro696d62e4 |
| Formato | AMD64, PE32+, manifiesto SYMGEN v2/Zstd,499234 entradas |
| Build-id | 3e441e7c7f09432d9cfb111c22596cb601000000; coincide con RSDS GUID+age del mismo EXE |
| Decoder | Python3.12.10; zstandard0.25.0, wheel cp312 win_amd64 SHA256 ffef5a74088f1e09947aecf91011136665152e0b4b359c42be3373897fb39b01 verificado contra PyPI/TLS |
| Herramientas | MSVC dev-cmd x64, VCTools14.51.36231, WindowsSDK10.0.26100.0; undname y dumpbin reales |

El lector reproduce estructuras/Header72/Entry24, validación build-id y resolución FNV de [manifest.cpp42–60,113–157,290–297,362–398](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/manifest.cpp#L362-L398).
Es **resolución offline de datos reales bajo el algoritmo exacto**, no una llamada inventada a HookService dentro del juego. El proceso sólo ejecutó Python/herramientas MSVC y nuestro fixture.

## Símbolo escogido, único límite
Nombre resoluble literal: `src/dusk/mods/svc/stage.cpp#dusk::mods::svc::register_edit`; alias `dusk::mods::svc::\`anonymous namespace'::register_edit`.
RVA **0x4e49d0**, local/code; flags69 en alias fuente y5 en nombre canónico. Son dos representaciones de la misma función, no dos funciones. No dupname, multiname ni inline-sites en las entradas al mismo RVA. Los símbolos dtor$… encontrados por búsqueda textual son funclets de cleanup y **no** se consideran la entrada objetivo.
El manifiesto no conserva un mangling MSVC decorado de register_edit entre estas entradas: no se inventa. Se valida identidad mediante alias fuente/canónico, RSDS y el cuerpo puntual correlacionado con fuente. Para la alternativa stage_add_actor sí se leyó mangling/demangling completo, pero flagsMULTI_NAME aconsejan no convertirla en una segunda ruta sin revisión. No se presume que esa bandera pruebe alias peligroso entre funciones diferentes.

Firma real de fuente [stage.cpp158–165](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/stage.cpp#L158-L165):
`ModResult register_edit(LoadedMod&, const char*, ActorEditRecord&&, uint64_t&)`.
MSVC x64: RCX referencia opaca a owner; RDX puntero stage; R8 referencia/rvalue a record; R9 referencia outHandle; resultado enum4bytes en EAX. Rvalue reference no copia la estructura como argumento por valor; no hay hidden return-buffer para ModResult.

## Evidencia máquina acotada
Intervalo único .pdata **[0x4e49d0,0x4e4b36)**,358bytes; SHA256 **04e7373d123870fd4e70b68209c762f7a486337bfc2fb3e7d13b0bb57af65be8**.
`dumpbin /disasm:nobytes /range` se limitó a esa función. Flujo relevante: R8 se conserva en RDI; RDX en RBX; instrucción de escritura al out-argument `mov qword ptr [r9],r8`; retorno `xor eax,eax; ret`, coherentes con asignar handle y devolver MOD_OK. El resto del cuerpo confirma asignaciones previas al almacenamiento y movimiento; no se reproducen offsets de sus contenedores en código experimental.
[evidence/symbol-abi-result.json](evidence/symbol-abi-result.json) conserva selección de instrucciones ABI, hash/rango y resultado de símbolos. El output completo del único rango permanece en el job privado; no se sube EXE, .lib, PDB, DLL ni bytes originales.
[HookService431–436](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/hook.cpp#L431-L436) advierte que entry hooks no cubren copias inline. No se observó tal flag en este objetivo; es evidencia del manifiesto de esta build, no garantía universal de otras builds/optimización.

## Lifetime y qué no habilita el PASS
LoadedMod& se usa sólo como referencia opaca durante llamada, no se dereferencia ni conserva tras detach. Stage y outHandle tienen scope del caller. ActorEditRecord&& es un temporal: válido durante llamada, movido al almacén antes de POST y destruido al terminar el caller; su dirección **no es record.data()**. No se retiene ni se inspecciona su vector.
El handle se escribe ANTES de push_back; un valor observado antes del retorno MOD_OK no prueba commit si una asignación/allocación falla. Una excepción del original puede impedir POST: no se da por cerrado un scope sólo por imaginar un callback. Cancelación y cleanup siguen P2/P3, no pruebas realizadas.
P1 verifica que el límite existe y su ABI opaco es consistente en el artefacto, **no que provea el buffer ni que se instalase un hook seguro**.

## Fixture MSVC: alcance explícito
Se compiló y ejecutó sólo un EXE propio que incluye api.h oficial (blob3015130ae3ceb41468723741902c257fc7c7fc8f), comprueba pointer8/ModResult4/Header72/Entry24 y devuelve PASS. Fuente generada SHA2567a2aa23263cbba9cc1e10e16033830e6449eca5d73adc6b4c50adc332651524e (bytes escritos en Windows); generación/comandos constan en el script ejecutado.
No declara ni fabrica ActorEditRecord/LoadedMod, no llama register_edit, no simula callbacks, actores, ownership o GPU. **No es P2 ni P3 ni build de .dusk/host.**
