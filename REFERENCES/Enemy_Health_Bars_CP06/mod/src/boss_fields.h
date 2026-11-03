// BARS203 CP03 -- typed reader of the boss-specific fields (2.0.3 classes). Game side: includes the real actor headers.
#pragma once
#include "reused/boss_phases.h"
class fopAc_ac_c;
namespace ehz {
// `actor` must be a fopAc_ac_c* of a live actor of the kind's profile. Returns false when the actor is not what its profile claims
// (profile mismatch, instance smaller than the 2.0.3 class): nothing is read in that case.
bool boss_read_203(Boss kind, const fopAc_ac_c* actor, PhaseInput& out);
}
