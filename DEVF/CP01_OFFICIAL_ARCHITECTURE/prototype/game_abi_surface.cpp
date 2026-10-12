// Compile-only type evidence: no game calls, field mutations, actor profiles or executable patching.
#include <mods/svc/game.h>
#include <f_op/f_op_actor.h>
#include <d/d_stage.h>
#include <type_traits>
#include <utility>
static_assert(GAME_SERVICE_MAJOR == 2);
static_assert(sizeof(stage_actor_data_class) == 32);
static_assert(sizeof(stage_tgsc_data_class) == 36); // StageService wants 35 serialized bytes.
static_assert(std::is_same_v<decltype(std::declval<fopAc_ac_c>().health), s16>);
static_assert(std::is_same_v<decltype(std::declval<fopAc_ac_c>().speedF), f32>);
static_assert(std::is_same_v<decltype(std::declval<fopAc_ac_c>().scale), cXyz>);
static_assert(std::is_same_v<decltype(std::declval<fopAc_ac_c>().model), J3DModel*>);
