# Continuidad — CP-R06

Continuar rama `research/dusklight-203-dusk-atlas` de `iscoremusic26-maker/Mods-Duskligh`, exclusivamente DUSKLIGHT_RESEARCH. Fuente fija `40457c6adb381928e4b5fef6ed459ed291edd5e2`; Windows x64 / DX12 / GZ2E01 USA. Padre remoto comprobado: CP-R05 `4dc156a5f4c1dcf70a536cf0298cf55774a8b0f0`; obtener el SHA de este checkpoint desde HEAD/historial.

CP-R06 añade CALLBACK-005..008 y tres símbolos: ruta ItemService resolver, clear/detach y consumidor cofre. PendingResolve copia fn/userData sin handle y revalida active, no el registro vivo. El contrato exige resolvers sin efectos secundarios: la copia defensiva no otorga permiso contractual para mutar registros desde callback. Userdata/info y nombre prestado deben respetar lifetime. Sin ejecución de reentrancia ni juego.

Acumulado: 188 evidencias, 205 símbolos, 19 fichas; las áreas READ/INVENTARIED se conservan. El inventario no se rehízo. Q-01/Q-02 quedan parcialmente resueltas para Item resolvers, no para todo Item ni Message.

Primera acción siguiente: alternar a Q-10, HUD/fonts. Leer systems/hud_ui_text.md y seguir una cadena representativa de adquisición → uso → liberación de fuente JUTResFont desde un consumidor, sin intentar todos los menús ni assets. Localizar contrato/tipo, recurso/heap, call site y destructor. Publicar CP-R07 antes de abrir otra familia. No repetir Save/Host/Camera/Item completos; Message puede retomarse después de ampliar presentación.

Comprobar HEAD remoto antes de escribir; recuperar solo archivos necesarios del atlas. La fuente certificada existe en work/source/dusklight-2.0.3 y el atlas de trabajo en work/atlas/DUSKLIGHT_RESEARCH, rutas efímeras. Revisar y ejecutar tools/validate_atlas.py; si falla no publicar. Solo commits bajo DUSKLIGHT_RESEARCH, sin PR nuevo, merge, tag, release ni force. Usar conector GitHub, padre/tree actuales y expected_sha; comprobar ref y archivo remoto. No tocar producción, SDK, upstream, PR80/81 ni CI65/66. No subir prompts o recursos originales.

Persistir bloques útiles aproximadamente cada 3–5 minutos activos; antes de nuevos análisis costosos. Máximo 2–3 lecturas paralelas tras checkpoint seguro. Cuatro submódulos siguen ausentes; disponibilidad binaria Windows y runtime no verificados. No hay ejecución de fondo.

NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED.
