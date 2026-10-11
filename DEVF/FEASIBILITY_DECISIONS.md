# Viabilidad — CP00
Objetivo preservado: un .dusk modular para variantes por instancia y colocación reproducible en Dusklight 2.0.3 Windows x64 DX12. Sin cambiar renderer, EXE, ROM, partidas ni actores retail.

Ruta A plausible: ActorService crea una instancia del perfil nativo; mantener identidad y estado externo por instancia, y evaluar un adaptador acotado. No hay setters de atributos ni herencia IA en ActorService. HookService es posible solo tras verificar símbolo, firma, ownership y autorización adecuada; ningún hook añadido en CP00.

Ruta B plausible: perfil único con callbacks propios como custom_actor_demo, usando recursos/animación/colisión del juego cuando su ownership se demuestre. No copiar objetos, vtables ni un perfil C++ para asumir herencia.

Comprobación focal, sin elegir enemigo definitivo: include/d/actor/d_a_e_bu.h identifica e_bu_class como Bubble, NO Bulblin arquero. Expone phase, modelMorf, action/mode, timers, colisiones; src/d/actor/d_a_e_bu.cpp contiene create/execute/delete, recurso E_BU y static l_HIO compartido (velocidad/escala/rangos). Hay estado individual y global: modificar l_HIO contaminaría instancias. No portar los offsets de comentarios ni adoptar Bubble automáticamente.

Experimento propuesto CP02: tras CP01 y autorización de etapa, seleccionar un enemigo con recursos y sala verificados; registrar una instancia retail y una DEVF; medir un cambio conductual individual, muerte/daño/cambio de sala y limpieza, observando la retail. Ruta A exige resolver identidad, fase de creación y adaptador sin estado global. Ruta B exige demostrar AI/animación/colisión reutilizable con ownership propio. Comparar resultados y elegir allí. Materiales/texturas individuales continúan pendientes CP04.

No resolver arquitectura por lectura; no prometer ataque nuevo, herencia IA ni apariencia aislada. El candidato Arquero Escarlata permanece opcional. No se investigó 2.0.2 ni proyectos HM/Bars/Magic.
