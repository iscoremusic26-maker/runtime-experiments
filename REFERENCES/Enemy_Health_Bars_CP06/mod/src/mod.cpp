// Enemy Health Bars 2.0.3 port -- CP03 TEST + OPTIONAL Enemy Health Multiplier vitals integration (HM-INTEGRATION TEST): normal-enemy bars + boss / mini-boss bars (J2D, queued in the 2D draw lists).
// The ONLY addition over BARS203_CP04 is the optional import of HmVitalsService (hm_bridge.*): without the provider every path is the original one. Bars never writes to the game, to HM or to any HP.
// Hooks (official HookService, typed helpers): dMeter2_c::_execute (post), _draw (post), _delete (pre) -- verified in CP01.
// Nothing is written to actors, HP, damage, saves or the HUD. No pointers to game objects survive a tick.
#include <cstdint>
#include <cstdio>

#include "d/d_meter2.h"
#include "mods/service.hpp"
#include "mods/svc/hook.hpp"
#include "mods/svc/interp.h"
#include "mods/svc/log.h"

#include "game_bars.h"
#include "hm_bridge.h"
#include "hm_vitals_api.h"
#include "tick_gate.h"

DEFINE_MOD();
IMPORT_SERVICE(LogService, svc_log);
IMPORT_SERVICE(HookService, svc_hook);
IMPORT_OPTIONAL_SERVICE(InterpService, svc_interp);  // presentation interpolation of the bar anchor; bars work without it
// Optional: effective health of Enemy Health Multiplier. Minor 0 is enough (v1.0 has a single function). NULL when HM is absent, disabled, failed or incompatible: bars then use the native health exactly as before.
// The loader initialises the provider BEFORE this mod (optional imports are dependency edges) and shuts this mod down first (reverse order), so the pointer is valid from mod_initialize to mod_shutdown.
IMPORT_OPTIONAL_SERVICE_VERSION(HmVitalsService, svc_hm_vitals, 0);

DEFINE_HOOK(&dMeter2_c::_execute, MeterExecute);
DEFINE_HOOK(&dMeter2_c::_draw, MeterDraw);
DEFINE_HOOK(&dMeter2_c::_delete, MeterDelete);

namespace {
constexpr const char* kBuild = "2.0.3-tt-fix01-test";
constexpr uint64_t kHeartbeatUpdates = 1800;  // 60 s at the 30 Hz simulation tick
constexpr unsigned kMaxHeartbeats = 30;       // hard cap: the whole session writes at most ~45 lines

struct Counters {
    uint64_t update = 0, execute = 0, draw = 0, del = 0;
    ehz::TickGate gate;  // simTick advances in _execute (simulation only); one bar pass per tick in _draw
    unsigned heartbeats = 0;
    bool seenExecute = false, seenDraw = false, seenDelete = false;
    bool registered = false;  // true only between a successful mod_initialize and mod_shutdown
};
Counters g;  // fresh copy of the library on every enable/reload: no state survives a reload

void report(const char* tag) {
    const auto& s = ehz::bars_stats();
    char text[640];
    std::snprintf(text, sizeof text,
        "BARS203 CP03 %s: update=%llu execute=%llu draw=%llu delete=%llu | ticks=%llu tracked=%u/max %u published(max)=%u queued=%llu refused=%llu hudNotQueued=%llu "
        "packetDraws=%llu barsDrawn=%llu skipped=%llu interp(hit/miss)=%llu/%llu scrubbed=%llu | boss ticks=%llu shown=%llu draws=%llu maxCand=%u",
        tag, (unsigned long long)g.update, (unsigned long long)g.execute, (unsigned long long)g.draw, (unsigned long long)g.del,
        (unsigned long long)s.ticks, ehz::bars_tracked(), s.maxTracked, s.maxPublished, (unsigned long long)s.queued,
        (unsigned long long)s.queueRefused, (unsigned long long)s.hudNotQueued, (unsigned long long)s.packetDraws,
        (unsigned long long)s.barsDrawn, (unsigned long long)s.drawSkipped, (unsigned long long)s.interpHits,
        (unsigned long long)s.interpMisses, (unsigned long long)s.scrubbed, (unsigned long long)s.bossTicks,
        (unsigned long long)s.bossShownTicks, (unsigned long long)s.bossDraws, s.maxBossCandidates);
    svc_log->info(mod_ctx, text);
    const auto& h = ehz::hm_bridge_stats();
    if (h.ttSeen > 0) {
        std::snprintf(text, sizeof text,
            "BARS203 Tektite(%s): counter-based bars | instances=%u views=%llu alive=%llu defeated-hidden=%llu provider-effective=%llu provider-rejected=%llu",
            tag, h.ttIdCount, (unsigned long long)h.ttSeen, (unsigned long long)h.ttNativeViews, (unsigned long long)h.ttDead, (unsigned long long)h.ttEffectiveViews, (unsigned long long)h.ttRejected);
        svc_log->info(mod_ctx, text);
    }
    if (h.aiSeen > 0) {
        std::snprintf(text, sizeof text,
            "BARS203 ARMOS(%s): counter-based bars | instances=%u views=%llu alive=%llu defeated-hidden=%llu unreadable-counter=%llu provider-effective=%llu provider-rejected=%llu reflected-steps=%llu steady-repeats=%llu (shield hits leave the bar unchanged by construction: the view is built from the counter)",
            tag, h.aiIdCount, (unsigned long long)h.aiSeen, (unsigned long long)h.aiNativeViews, (unsigned long long)h.aiDead, (unsigned long long)h.aiUnreadable, (unsigned long long)h.aiEffectiveViews, (unsigned long long)h.aiRejected, (unsigned long long)h.aiSteps, (unsigned long long)h.aiSteadyRepeats);
        svc_log->info(mod_ctx, text);
    }
    if (h.attached || h.incompatible) {
        std::snprintf(text, sizeof text,
            "BARS203 HM bridge(%s): provider %s | queries=%llu ok=%llu (effective %llu, budget %llu) use-native=%llu [factor-one %llu breaker %llu profile-native %llu rule %llu not-living %llu no-budget %llu] unavailable=%llu invalid=%llu rejected=%llu chuchu-native=%llu scale-changes=%llu",
            tag, h.incompatible ? "INCOMPATIBLE (ignored)" : "present", (unsigned long long)h.queries, (unsigned long long)h.ok, (unsigned long long)h.okEffective, (unsigned long long)h.okBudget,
            (unsigned long long)h.useNative, (unsigned long long)h.nativeReason[HM_VR_FACTOR_ONE], (unsigned long long)h.nativeReason[HM_VR_BREAKER], (unsigned long long)h.nativeReason[HM_VR_PROFILE_NATIVE],
            (unsigned long long)h.nativeReason[HM_VR_PROFILE_RULE], (unsigned long long)h.nativeReason[HM_VR_NOT_LIVING], (unsigned long long)h.nativeReason[HM_VR_NO_BUDGET],
            (unsigned long long)h.unavailable, (unsigned long long)h.invalid, (unsigned long long)h.rejected, (unsigned long long)h.skippedChuchu, (unsigned long long)h.scaleChanges);
        svc_log->info(mod_ctx, text);
    }
}

// Post-hook of dMeter2_c::_execute: simulation ticks only (never called for presentation-only frames).
void on_execute_post(ModContext*, void*, void*, void*) {
    if (!g.registered) return;
    ++g.execute;
    g.gate.on_execute();
    if (!g.seenExecute) {
        g.seenExecute = true;
        svc_log->info(mod_ctx, "BARS203 CP03: first dMeter2_c::_execute post-hook call");
    }
}
// Post-hook of dMeter2_c::_draw: called on simulation ticks AND on presentation frames (the meter draws every rendered frame).
// Only the first call after a simulation tick does work: all actors have executed, the draw-list set() calls are accepted.
void on_draw_post(ModContext*, void* args, void*, void*) {
    if (!g.registered) return;
    ++g.draw;
    if (!g.seenDraw) {
        g.seenDraw = true;
        svc_log->info(mod_ctx, "BARS203 CP03: first dMeter2_c::_draw post-hook call");
    }
    if (!g.gate.on_draw()) return;
    ehz::bars_sim_tick(mods::arg<dMeter2_c*>(args, 0), g.gate.simTick);
    while (const char* w = ehz::hm_bridge_next_warning()) svc_log->warn(mod_ctx, w);   // bounded: each distinct unexpected provider answer once
}
// Pre-hook of dMeter2_c::_delete: runs BEFORE the original; never cancels it.
HookAction on_delete_pre(ModContext*, void*, void*, void*) {
    if (g.registered) {
        ++g.del;
        ehz::bars_meter_deleted();
        if (!g.seenDelete) {
            g.seenDelete = true;
            svc_log->info(mod_ctx, "BARS203 CP03: first dMeter2_c::_delete pre-hook call (original NOT cancelled; bars dropped)");
        }
    }
    return HOOK_CONTINUE;
}
}  // namespace

extern "C" {

MOD_EXPORT ModResult mod_initialize(ModError* error) {
    g = Counters{};
    ehz::hm_bridge_attach(svc_hm_vitals);   // may be null: bars use native health
    if (svc_log == nullptr || svc_hook == nullptr) {  // required imports are guaranteed non-null by the loader; belt and braces
        return mods::set_error(error, MOD_UNAVAILABLE, "BARS203 CP03: LogService/HookService unavailable");
    }
    // Each add_* installs the (shared) detour on first use. If any step fails the mod fails to load; the loader
    // detaches the mod and removes whatever was registered (HookService hook_remove_mod).
    ModResult r = mods::hook::add_post<MeterExecute>(on_execute_post);
    if (r != MOD_OK) return mods::set_error(error, r, "BARS203 CP03: could not hook dMeter2_c::_execute (post)");
    r = mods::hook::add_post<MeterDraw>(on_draw_post);
    if (r != MOD_OK) return mods::set_error(error, r, "BARS203 CP03: could not hook dMeter2_c::_draw (post)");
    r = mods::hook::add_pre<MeterDelete>(on_delete_pre);
    if (r != MOD_OK) return mods::set_error(error, r, "BARS203 CP03: could not hook dMeter2_c::_delete (pre)");
    g.registered = true;
    ehz::bars_set_active(true);
    char text[360];
    std::snprintf(text, sizeof text, "BARS203 CP03 + HM integration TEST %s loaded: 3/3 hooks registered; normal + boss bars via 2D draw-list packet; interpolation service %s; Enemy Health Multiplier vitals %s",
        kBuild, svc_interp ? "present" : "ABSENT (bars use the simulation anchor)",
        svc_hm_vitals == nullptr ? "ABSENT (native health)" : (ehz::hm_bridge_present() ? "PRESENT (effective health for the audited enemies)" : "INCOMPATIBLE (native health)"));
    svc_log->info(mod_ctx, text);
    return MOD_OK;
}

MOD_EXPORT ModResult mod_update(ModError*) {
    ++g.update;
    if (g.registered && g.update % kHeartbeatUpdates == 0 && g.heartbeats < kMaxHeartbeats) {
        ++g.heartbeats;
        report("heartbeat");
    }
    return MOD_OK;
}

MOD_EXPORT ModResult mod_shutdown(ModError*) {
    // The loader retires every hook of this mod (callbacks erased, detours removed) after this call and before the
    // library is unloaded (ModLoader::deactivate_mod -> modules_mod_detached -> hook_remove_mod; the native library is
    // dlclosed one tick later). Hooks are NOT uninstalled here. What the loader cannot know about is our packet inside the
    // game's 2D draw lists: its vtable lives in this library, so it is removed now (game thread, outside any painter run).
    g.registered = false;
    ehz::bars_shutdown();
    report("shutdown");
    ehz::hm_bridge_detach();   // the provider pointer is never used after this point
    return MOD_OK;
}

}  // extern "C"
