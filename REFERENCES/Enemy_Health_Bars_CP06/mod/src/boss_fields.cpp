#include <type_traits>
#include "d/d_com_inf_game.h"
#include "m_Do/m_Do_ext.h"
#include "d/actor/d_a_e_fm.h"
#include "d/actor/d_a_b_ob.h"
#include "d/actor/d_a_b_ds.h"
#include "d/actor/d_a_b_yo.h"
#include "d/actor/d_a_b_gm.h"
#include "d/actor/d_a_b_dr.h"
#include "d/actor/d_a_b_mgn.h"
#include "d/actor/d_a_b_gnd.h"
#include "d/actor/d_a_b_zant.h"
#include "d/actor/d_a_b_tn.h"
#include "d/actor/d_a_b_gg.h"
#include "d/actor/d_a_e_vt.h"
#include "d/actor/d_a_e_gob.h"
#include "d/actor/d_a_e_pz.h"
#include "d/actor/d_a_e_dt.h"
#include "d/actor/d_a_b_bq.h"
#include "boss_fields.h"
namespace ehz {
#include "generated/boss_fields_203.inc"
bool boss_read_203(Boss kind, const fopAc_ac_c* actor, PhaseInput& out) { return read_phase_input_203(kind, actor, out); }
}  // namespace ehz
