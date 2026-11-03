#pragma once
#include "reused/normal_model.h"
class J2DGrafContext;
namespace ehz {
void normal_draw(J2DGrafContext& graph, const NormalDrawState* states, unsigned count, bool showNumbers);
}
