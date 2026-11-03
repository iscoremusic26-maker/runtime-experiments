#pragma once
#include "reused/boss_draw_state.h"
class J2DGrafContext;
class dMeter2Draw_c;
namespace ehz {
// Draws the boss bar for `state` (value data only) into `g`; `hud` supplies the HUD panes used for the ornaments (may be null).
void boss_paint(J2DGrafContext& g, const BossDrawState& state, dMeter2Draw_c* hud);
}
