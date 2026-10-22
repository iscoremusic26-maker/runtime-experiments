# Diagnóstico de disco: metadata,worker,resultado y cancelación

CP-R42,Q-13. Fuente TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2; interpretación Windows x64/DX12/GZ2E01 USA. PORT-018..021 STATIC_CROSSCHECKED de wrappers y UI. No se abrió ROM/ISO/configuración/log personal ni se ejecutó inspección,hash o tráfico de red. No confundir esta investigación con inventario R00 ni certificación de disco.

## Contrato interno y backend

iso_validate.hpp declara inspect/validate y DiscInfo/ValidationError; Platform/Progress vienen de Borealis. inspect llama disc::inspect; validate llama disc::verify con catálogo y Progress. PathNULL se convierte a string_view vacío. Catálogo contiene GZ2E01 y otras variantes; aquí solo se interpreta objetivoUSA,no se certifican otras plataformas por una tabla. update_info solo sustituye campos si result.metadata.gameId no está vacío; caller que reutiliza DiscInfo debe distinguir status de campos residuales. Task nuevo inicia info por defecto.

Status Success,IOError,InvalidImage,UnknownGame,UnsupportedVersion,Canceled,HashMismatch se mapean a enum host; failed/default→Unknown. Devolver Success del wrapper describe el resultado del backend,no una prueba de esta sesión. Comentario de startup diferencia inspección metadata de hash completo. Parsing/formato de imagen,bytes cubiertos por hash y atención a cancelación quedan BLOCKED por Borealis gitlink ausente; no instalar dependencia ni reconstruir binarios.

## Entrada,worker y publicación

file_dialog_callback solo acepta Selected con locations no vacío; toma primera ubicación y begin_disc_verification. No se abrió diálogo en esta investigación. begin con pathempty retorna; si hay tarea previa escribe cancelRequested y reset. Destructor de tarea pidecancel y join de std::thread si joinable: reemplazar no suelta this con worker vivo,pero puede esperar a backend. No garantía de cancelación inmediata ni latencia acotada.

Tarea posee stringpath,DiscInfo,Progress,ValidationError y thread. Worker captura this,llama iso::validate y convierte excepciones C++ std::exception/otras aUnknown; no captura universal de corrupción/fallos de memoria. Al final done.store(release); finished.load(acquire) es gate de lectura UI de info/validation no atómicos. take_finished copia resultado propio,join,reset y devuelveoptional. No prestado al panel ni callback de mod. Este join explícito no se atribuye al Task Borealis/HttpService de CP-R33.

## Resultado consumido y cancelación UI

try_push crea modal una vez mientras tarea globalexiste. Tarea pertenece al unique_ptr global,no al modal. update pide resultado; si disponible aplica y pop. Si tareaNULL cierra modal; otro caso refresca progreso. bytesRead/Total se cargan relaxed y UI clampa fracción;100% no es done ni Success. No se observó progreso real.

Botón Cancel/NavCancel solo escribe cancelRequested relaxed,cambia etiqueta y deshabilita botón. No espera worker ni asigna Canceled inmediatamente. Atención/retorno depende backend; modal sigue esperando resultado. Cierre de un documento no se equipara a destrucción de esta tarea global.

Success aplica selección,limpia error/pending. HashMismatch y Canceled guardan resultado en pendingDisc y muestran aviso con posibilidad Continue; otros errores—including Unknown de worker nuevo—no entran en ese pending. Aceptar aviso mueve/copía datos,pone estado configurado,refresca metadata y cierra modal. No se ejecutó esa acción. Un nombre acceptHashMismatch no restringe por sí solo la rama aHashMismatch,pues Canceled también llega ahí.

## Metadata,configuración y consumidor posterior

apply_valid_disc_result fija configuredCanLaunch=true y campos; activeDisc solo cambia si vacío o misma ubicación. persist_disc_choice escribe isoPath e isoVerification,config::save y log nominal si cambió. Success/HashMismatch conservan estado; Canceled/otros mapean aUnknown. No se consultó CVar real ni se demuestra durabilidad por voidsave/log. No es SaveService ni guardado de partida.

refresh_configured_disc_state exige primero inspectSuccess. Después puede recuperar verificación por igualdad de ubicación con CVar; permiteUnknown,Success,HashMismatch. Así Unknown cacheado tras metadata válida difiere de Unknown devuelto por tarea nueva. Startup también inspecciona solo metadata; si falla limpia elección y fuerza prelaunch. Prelaunch::update puede poner IsGameLaunched=true desde configuredCanLaunch: esa variable no demuestra escena ejecutando o GPUlista.

Inferencia condicionada de PORT-021: misma ubicación y metadata válida no prueban identidad de bytes con los previamente verificados; en esta ruta no hay verify completo cada refresh. No se declara vulnerabilidad ni fallo observado. Config,estado UI,resultado de verificación y apertura efectiva del motor son fronteras separadas.

## Integración y límites

No DiscVerificationService público localizado en registro SDK auditado; helpers internos POTENTIAL_REQUIRES_VERIFICATION,sin export/ABI/hook Windows. FileService/LogService conservan contratos propios,no acceso libre al disco personal ni ownership de este worker. Una investigación futura debe respetar thread/join,resultados por valor y tarea global antes de modificar UI; no se propone mod o integración.

Q-13 sigue READ parcial; cancelaciónbackend,timings,formatos y garantías de disco físico no comprobados. Cuatrogitlinks/Android,sin runtime Windows,build ni producción. No conectar servicios externos ni usar logs personales para completar esta ficha.

**PORT-018** — [src/dusk/iso_validate.hpp:17–49](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/iso_validate.hpp#L17-L49); [src/dusk/iso_validate.cpp:30–34](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/iso_validate.cpp#L30-L34); [src/dusk/iso_validate.cpp:63–89](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/iso_validate.cpp#L63-L89); [src/dusk/iso_validate.cpp:108–135](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/iso_validate.cpp#L108-L135)

**PORT-019** — [src/dusk/ui/prelaunch.cpp:92–138](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L92-L138); [src/dusk/ui/prelaunch.cpp:171–196](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L171-L196); [src/dusk/ui/prelaunch.cpp:471–480](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L471-L480)

**PORT-020** — [src/dusk/ui/prelaunch.cpp:313–339](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L313-L339); [src/dusk/ui/prelaunch.cpp:364–388](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L364-L388); [src/dusk/ui/prelaunch.cpp:405–460](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L405-L460); [src/dusk/ui/prelaunch.cpp:672–677](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L672-L677); [src/dusk/ui/prelaunch.cpp:693–726](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L693-L726)

**PORT-021** — [src/dusk/ui/prelaunch.cpp:143–168](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L143-L168); [src/dusk/ui/prelaunch.cpp:266–278](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L266-L278); [src/dusk/ui/prelaunch.cpp:298–311](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L298-L311); [src/dusk/ui/prelaunch.cpp:627–670](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L627-L670); [src/dusk/ui/prelaunch.cpp:1032–1041](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/ui/prelaunch.cpp#L1032-L1041); [src/m_Do/m_Do_main.cpp:777–788](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_main.cpp#L777-L788)
