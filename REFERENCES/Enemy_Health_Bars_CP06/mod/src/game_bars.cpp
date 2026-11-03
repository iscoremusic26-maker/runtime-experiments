// BARS203 CP02 -- game side of the normal bars: GameApi (Dusklight 2.0.3 types) for BarsCore (bars_core.h).
//
// Frame model (verified in src/m_Do/m_Do_main.cpp, d_drawlist.cpp, f_pc_*.cpp, game_clock.cpp, frame_interpolation.cpp):
//  * simulation tick  = fapGm_Execute: ModLoader::tick, then fpcM_Management { dComIfGd_reset (BeforeOfDraw), execute handler,
//    draw handler (every process draw; 2D draw lists are filled with dDlst_list_c::set, which only accepts entries while
//    is_sim_frame()), AfterOfDraw }.  The interpolation recording window (begin_record/end_record) spans execute + draw.
//  * presentation     = fpcM_DrawIterater(fpcM_Draw) again (set() is a no-op), then cAPIGph_Painter, which runs the lists that
//    the LAST simulation tick filled (draw2DOpa, draw2DOpaTop, draw2DXlu) -- possibly several times (one per rendered frame).
//  => We sample actors and QUEUE a packet in the _draw post hook of a simulation tick; the packet's draw() executes inside the
//     painter's 2D pass (after the HUD) on every rendered frame and re-projects each bar with the interpolated anchor.
#include "d/d_com_inf_game.h"
#include "d/d_meter2.h"
#include "d/d_meter2_info.h"
#include "d/d_meter2_draw.h"
#include "d/d_camera.h"
#include "d/actor/d_a_alink.h"
#include "d/actor/d_a_e_db.h"
#include "d/actor/d_a_e_tt.h"
#include "d/actor/d_a_e_ai.h"
#include "f_op/f_op_actor_tag.h"
#include "f_pc/f_pc_manager.h"
#include "f_pc/f_pc_profile.h"
#include "JSystem/J2DGraph/J2DOrthoGraph.h"
#include "m_Do/m_Do_lib.h"
#include "m_Do/m_Do_graphic.h"

#include "bars_core.h"
#include "hm_bridge.h"
#include "interp_glue.h"
#include "normal_draw.h"
#include "boss_fields.h"
#include "boss_paint.h"
#include "d/d_bg_s_lin_chk.h"
#include "d/d_attention.h"
#include "reused/boss_catalog.h"

#if defined(_WIN32)
// Tektite layout of the 2.0.3 headers == the shipped machine code of daE_TT_c::damage_check / setActionMode (HM evidence/cp04tt_exe_damage_check.txt): counter `addl %ecx,0x928`, health 0x656, action `movl %edx,0x8e8`.
static_assert(offsetof(daE_TT_c, field_0x6f0) == 0x928 && offsetof(daE_TT_c, mAction) == 0x8e8 && offsetof(fopAc_ac_c, health) == 0x656, "daE_TT_c layout != exe");
// Armos layout of the 2.0.3 headers == the shipped machine code of e_ai_class::damage_check (HM evidence/cp05_ai_exe_damage_check.txt): `movzbl 0x1211` / `incb 0x1211` / `cmpb $2,0x1211` [m_hitCount, signed byte].
static_assert(offsetof(e_ai_class, m_hitCount) == 0x1211 && sizeof(((e_ai_class*)nullptr)->m_hitCount) == 1 && static_cast<s8>(-1) < 0, "e_ai_class::m_hitCount layout != exe");
#endif
namespace ehz {
namespace {
bool allied(const fopAc_ac_c* actor) {
    if (actor->name == fpcNm_E_HB_e && fpcM_GetParam(actor) == 0xffff0040) return true;
    if (actor->name == fpcNm_E_HB_LEAF_e) {
        auto* parent = static_cast<fopAc_ac_c*>(fpcM_SearchByID(actor->parentActorID));
        return parent && parent->name == fpcNm_E_HB_e && fpcM_GetParam(parent) == 0xffff0040;
    }
    return false;
}
bool profile_ok(const fopAc_ac_c* a, size_t minSize) { return a->profile && a->profile->name == a->name && a->profile->process_size >= minSize; }
bool live_baba(const fopAc_ac_c* a) {
    if (a->name != fpcNm_E_DB_e || !profile_ok(a, sizeof(e_db_class))) return false;
    const auto* b = reinterpret_cast<const e_db_class*>(a);
    return b->action == 20 && b->mode < 50 && !b->field_0x852;
}
int displayed_health(const fopAc_ac_c* a) {
    if (a->name != fpcNm_E_DB_e || !profile_ok(a, sizeof(e_db_class))) return a->health;
    const auto* b = reinterpret_cast<const e_db_class*>(a);
    return baba_display_health(a->health, true, b->action, b->mode, b->field_0x852 != 0);
}

// Health view of one actor for the NORMAL bars: native by default; with the optional Enemy Health Multiplier provider attached, hm_normal_view() (hm_bridge.cpp) asks it only for actors
// the tracker would follow and returns its VALIDATED effective view. Pure read: nothing is written anywhere.
HealthView normal_view(fopAc_ac_c* a, bool boss, bool allied, bool senses) {
    if (a->name == fpcNm_E_TT_e && profile_ok(a, sizeof(daE_TT_c))) {   // Tektite: the defeat is its hit counter, not `health` (tektite_view.h): bar follows the counter, with or without Enemy Health Multiplier
        const auto* t = static_cast<const daE_TT_c*>(a);
        return hm_tektite_view(mod_ctx, a, a->id, t->field_0x6f0, a->health, t->mAction, a->group, a->actor_status, a->actor_condition, a->attention_info.flags, senses, boss, allied);
    }
    if (a->name == fpcNm_E_AI_e && profile_ok(a, sizeof(e_ai_class))) {   // Armos: the defeat is its hit counter, `health` is a 1000 decoy (armos_view.h): bar follows the counter, with or without Enemy Health Multiplier
        const auto* e = static_cast<const e_ai_class*>(a);
        return hm_armos_view(mod_ctx, a, a->id, (int)e->m_hitCount, a->group, a->actor_status, a->actor_condition, a->attention_info.flags, senses, boss, allied);
    }
    const int native = displayed_health(a);
    return hm_normal_view(mod_ctx, a, a->id, a->name, a->group, native, a->actor_status, a->actor_condition, a->attention_info.flags, senses, boss, allied);
}

struct GameApi {
    using Meter = dMeter2_c;
    using Base = dDlst_base_c;
    using List = dDlst_list_c;
    static List& list() { return g_dComIfG_gameInfo.drawlist; }
    static Base* packet();
    static const Base* meter_hud(Meter* m) { return m->mpMeterDraw; }
    static bool player(uintptr_t* addr, uint32_t* id) {
        auto* p = g_dComIfG_gameInfo.play.getPlayer(0);
        if (!p || g_dComIfG_gameInfo.info.getPlayer().getPlayerStatusA().getLife() == 0) return false;
        *addr = reinterpret_cast<uintptr_t>(p); *id = p->id;
        return true;
    }
    static void stage(char (&name)[8], int8_t* layer, int8_t* dark) {
        const char* s = g_dComIfG_gameInfo.play.getStartStageName();
        for (unsigned i = 0; i < 8; ++i) name[i] = s[i];
        *layer = g_dComIfG_gameInfo.play.getStartStageLayer(); *dark = g_dComIfG_gameInfo.play.getStartStageDarkArea();
    }
    static bool hud_allows(Meter* meter) {
        return !g_dComIfG_gameInfo.play.isPauseFlag() && !g_dComIfG_gameInfo.play.getEvent()->runCheck() &&
               !(meter->mStatus & (0x4000 | 0x40 | 0x100)) && dMeter2Info_getWindowStatus() == 0;
    }
    static bool draw_allows() {
        auto* meter = dMeter2Info_getMeterClass();
        return g_dComIfG_gameInfo.info.getPlayer().getPlayerStatusA().getLife() != 0 && !g_dComIfG_gameInfo.play.isPauseFlag() &&
               !g_dComIfG_gameInfo.play.getEvent()->runCheck() && dMeter2Info_getWindowStatus() == 0 &&
               !(meter && (meter->mStatus & (0x4000 | 0x40 | 0x100))) && dComIfGd_getView() != nullptr;
    }
    static unsigned gather(ActorView* out, unsigned cap, bool* senses) {
        auto* p = g_dComIfG_gameInfo.play.getPlayer(0);
        *senses = daPy_py_c::checkNowWolfEyeUp() || dComIfGs_wolfeye_effect_check();
        unsigned n = 0, scanned = 0;
        for (auto* node = g_fopAcTg_Queue.mpHead; node && scanned++ < cap; node = node->mpNextNode) {
            auto* a = static_cast<fopAc_ac_c*>(reinterpret_cast<create_tag_class*>(node)->mpTagData);
            if (!a || a == p || n >= cap) continue;
            bool targetable = (a->attention_info.flags & 7) != 0 || live_baba(a);
            if (a->name == fpcNm_E_ZS_e) targetable = profile_ok(a, sizeof(fopEn_enemy_c)) && !static_cast<fopEn_enemy_c*>(a)->checkWolfNoLock();
            const bool bossFlag = boss_descriptor(a->name) != nullptr, alliedFlag = allied(a);
            out[n++] = {reinterpret_cast<uintptr_t>(a), a->id, a->name, a->group, a->actor_status, a->actor_condition, a->attention_info.flags,
                        normal_view(a, bossFlag, alliedFlag, *senses),  // native HP, or the validated effective view of Enemy Health Multiplier when its optional service is present
                        bossFlag, alliedFlag, targetable,
                        {a->current.pos.x, a->current.pos.y, a->current.pos.z}, {a->eyePos.x, a->eyePos.y, a->eyePos.z},
                        {a->attention_info.position.x, a->attention_info.position.y, a->attention_info.position.z}, a};
        }
        return n;
    }
    static bool project(const Vec3& w, Vec3* ortho) {
        if (!dComIfGd_getView()) return false;
        Vec in{w.x, w.y, w.z}, out{};
        mDoLib_project(&in, &out);
        *ortho = {out.x, out.y, out.z};  // mDoLib_project already returns the painter's ortho-space coordinates (x offset by getMinXF)
        return true;
    }
    static bool clear_line(const Vec3& w) {
        // dCam_getBody itself assumes a live camera; check its native slot first.
        if (!g_dComIfG_gameInfo.play.getCamera(0)) return true;
        auto* c = dCam_getBody();
        if (!c) return true;
        cXyz eye = c->iEye(), delta(w.x - eye.x, w.y - eye.y, w.z - eye.z);
        const float distance = delta.abs();
        if (!(distance >= 1) || !normal_finite(distance)) return true;
        const float factor = (distance - 45) / distance;
        cXyz end(eye.x + delta.x * factor, eye.y + delta.y * factor, eye.z + delta.z * factor);
        return !c->lineBGCheck(&eye, &end, 0x40b7);
    }
    static float distance(const ActorView& v) {
        auto* p = g_dComIfG_gameInfo.play.getPlayer(0);
        return p ? fopAcM_searchActorDistance(p, static_cast<fopAc_ac_c*>(v.handle)) : 4500.0f;
    }
    static void record(uint64_t key, const Vec3& w) { interp_record(key, w); }
    static void forget(uint64_t key) { interp_forget(key); }
    static bool lookup(uint64_t key, Vec3* w) { return interp_lookup(key, w); }
    // ---- bosses and mini-bosses (CP03) ----
    static bool paused() { return g_dComIfG_gameInfo.play.isPauseFlag() != 0; }
    static bool event_running() { return g_dComIfG_gameInfo.play.getEvent()->runCheck() != 0; }
    static Identity lock_target() {
        auto* t = g_dComIfG_gameInfo.play.getAttention()->LockonTarget(0);
        return t ? Identity{reinterpret_cast<uintptr_t>(t), t->id, t->name} : Identity{};
    }
    static unsigned gather_bosses(BossActor* out, unsigned cap) {
        unsigned n = 0, scanned = 0;
        for (auto* node = g_fopAcTg_Queue.mpHead; node && scanned++ < kTrackCapacity && n < cap; node = node->mpNextNode) {
            auto* a = static_cast<fopAc_ac_c*>(reinterpret_cast<create_tag_class*>(node)->mpTagData);
            if (!a || !boss_descriptor(a->name)) continue;
            out[n++] = {reinterpret_cast<uintptr_t>(a), a->id, a->name, a->health, a};
        }
        return n;
    }
    static bool boss_read(Boss k, const void* h, PhaseInput& in) { return boss_read_203(k, static_cast<const fopAc_ac_c*>(h), in); }
    static bool boss_los(const void* h) {
        auto* a = static_cast<const fopAc_ac_c*>(h);
        auto* cam = g_dComIfG_gameInfo.play.getCamera(0);
        if (!cam) return false;
        cXyz target = a->current.pos; target.y += 100;
        dBgS_LinkLinChk ray; ray.Set(&cam->view.lookat.eye, &target, nullptr);
        return !dComIfG_Bgsp().LineCross(&ray);
    }
    static bool dungeon_complete() { return dComIfGs_isStageMiddleBoss() != 0; }
    static void paint_boss(const BossDrawState& st) {
        auto* meter = dMeter2Info_getMeterClass();
        dMeter2Draw_c* hud = meter ? meter->mpMeterDraw : nullptr;
        // Same sequence as Bars 1.1.1 health_draw: current graf port, set up, draw, restore.
        if (auto* current = dComIfGp_getCurrentGrafPort()) {
            current->setPort(); current->setup2D();
            boss_paint(*current, st, hud);
            current->setPort(); current->setup2D();
        } else {
            J2DOrthoGraph ortho(0, 0, FB_WIDTH, FB_HEIGHT, -1, 1);
            ortho.setOrtho(mDoGph_gInf_c::getMinXF(), mDoGph_gInf_c::getMinYF(), width(), height(), -1, 1);
            ortho.setPort();
            boss_paint(ortho, st, hud);
        }
    }
    static float width() { return mDoGph_gInf_c::getWidthF(); }
    static float height() { return mDoGph_gInf_c::getHeightF(); }
    static float minX() { return mDoGph_gInf_c::getMinXF(); }
    static float minY() { return mDoGph_gInf_c::getMinYF(); }
    static void paint(const NormalDrawState* states, unsigned n, bool numbers) {
        // Same set-up as the native painter: physical GC viewport, widescreen logical bounds.
        J2DOrthoGraph ortho(0, 0, FB_WIDTH, FB_HEIGHT, -1, 1);
        ortho.setOrtho(mDoGph_gInf_c::getMinXF(), mDoGph_gInf_c::getMinYF(), width(), height(), -1, 1);
        ortho.setPort();
        normal_draw(ortho, states, n, numbers);
        if (auto* current = dComIfGp_getCurrentGrafPort()) { current->setPort(); current->setup2D(); }
    }
};

BarsCore<GameApi> core;

// The packet object queued in the game's 2D lists. Its vtable lives in this library: it is scrubbed from every list on
// meter deletion and on mod shutdown, and its draw() is inert once the mod is inactive.
class GamePacket final : public dDlst_base_c {
public:
    void draw() override { core.draw_packet(); }
};
GamePacket gamePacket;
dDlst_base_c* GameApi::packet() { return &gamePacket; }
}  // namespace

void bars_set_active(bool active) { core.set_active(active); }
const BarsStats& bars_stats() { return core.stats; }
unsigned bars_tracked() { return core.tracked(); }
void bars_meter_deleted() { core.meter_deleted(); }
void bars_shutdown() { core.shutdown(); }
void bars_sim_tick(dMeter2_c* meter, uint32_t simTick) { core.sim_tick(meter, simTick); }
}  // namespace ehz
