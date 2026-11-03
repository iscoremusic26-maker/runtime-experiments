// BARS203 CP02 -- orchestration of the normal bars, written against a small `Api` so the SAME code runs in the game
// (game_bars.cpp: GameApi over Dusklight 2.0.3 types) and in the Linux lab (fake world, modelled draw lists).
//
// Required Api (all static):
//   using Meter, Base;                                  // dMeter2_c, dDlst_base_c (lab: stand-ins)
//   using List;                                         // dDlst_list_c-like: mp2DOpaTop*/mp2DOpa*/mp2DXlu* + set2DXlu()
//   static List& list();                                // the game's draw lists
//   static Base* packet();                              // THE packet object (its draw() calls core.draw_packet())
//   static const Base* meter_hud(Meter*);               // the HUD dlst the meter queues (mpMeterDraw)
//   static bool player(uintptr_t*, uint32_t*);          // false = no player / life zero (everything is dropped)
//   static void stage(char (&name)[8], int8_t*, int8_t*);
//   static bool hud_allows(Meter*);                     // pause/event/menu/HUD-status conditions
//   static bool draw_allows();                          // same conditions re-checked inside the painter
//   static unsigned gather(ActorView*, unsigned cap, bool* senses);   // copy of the native actor queue (values only)
//   static bool project(const Vec3&, Vec3* ortho); static bool clear_line(const Vec3&); static float distance(const ActorView&);
//   static void record(uint64_t key, const Vec3&); static void forget(uint64_t key); static bool lookup(uint64_t key, Vec3*);
//   static float width(); static float height(); static float minX(); static float minY();   // logical viewport (ortho space)
//   static void paint(const NormalDrawState*, unsigned, bool numbers);   // J2D (lab: records)
//   -- bosses (CP03) --
//   static bool paused(); static bool event_running(); static Identity lock_target();
//   static unsigned gather_bosses(BossActor*, unsigned cap);              // actors whose profile is in boss_catalog (values + scan handle)
//   static bool boss_read(Boss, const void* handle, PhaseInput&); static bool boss_los(const void* handle); static bool dungeon_complete();
//   static void paint_boss(const BossDrawState&);                         // J2D (lab: records)
#pragma once
#include <stdint.h>
#include "drawlist_ops.h"
#include "game_bars.h"
#include "tracker.h"
#include "boss_tracker.h"

namespace ehz {
template <class Api>
class BarsCore {
public:
    using Base = typename Api::Base;
    BarsStats stats;
    NormalOptions options{};  // Bars 1.1.1 defaults: bars on, HP numbers off

    void set_active(bool a) { active = a; }
    bool is_active() const { return active; }
    unsigned tracked() const { return tracker.tracked(); }
    const BossTracker& bosses() const { return bossTracker; }

    // Once per simulation tick, from the _draw post hook.
    void sim_tick(typename Api::Meter* meter, uint32_t simTick) {
        if (!active || !meter) return;
        uintptr_t addr = 0; uint32_t id = 0;
        if (!Api::player(&addr, &id)) { visibleAtTick = false; clear_all(); return; }
        char name[8]{}; int8_t layer = 0, dark = 0;
        Api::stage(name, &layer, &dark);
        bool newStage = !haveStage || stageLayer != layer || stageDarkArea != dark;
        for (unsigned i = 0; i < 8; ++i) newStage |= stageName[i] != name[i];
        if (playerAddress != addr || playerId != id || newStage) {
            clear_all();
            playerAddress = addr; playerId = id;
            for (unsigned i = 0; i < 8; ++i) stageName[i] = name[i];
            stageLayer = layer; stageDarkArea = dark; haveStage = true;
        }
        visibleAtTick = Api::hud_allows(meter);
        ++stats.ticks;
        bool senses = false;
        const unsigned n = Api::gather(views, kTrackCapacity, &senses);
        tracker.tick(simTick, visibleAtTick, options.enabled, senses, views, n, env());
        boss_tick();
        const auto& ts = tracker.stats();
        if (ts.maxPublished > stats.maxPublished) stats.maxPublished = ts.maxPublished;
        if (ts.maxTracked > stats.maxTracked) stats.maxTracked = ts.maxTracked;
        unsigned published = 0;
        tracker.draw_entries(&published);
        // The lists are reset every simulation tick, so the packet is queued again each tick while there is a bar to show.
        const bool bossShown = bossTracker.showing();
        if (bossShown) ++stats.bossShownTicks;
        if (visibleAtTick && (published || bossShown)) {
            switch (queue_after_hud(Api::list(), Api::meter_hud(meter), Api::packet())) {
            case QueueResult::Queued: ++stats.queued; break;
            case QueueResult::Refused: ++stats.queueRefused; break;
            case QueueResult::HudNotQueued: ++stats.hudNotQueued; break;
            }
        }
    }

    // The packet's draw(): runs inside the painter's 2D pass, on EVERY rendered frame while the packet is in the list.
    void draw_packet() {
        ++stats.packetDraws;
        // Inert when the mod is not active (the library stays mapped for one more tick after shutdown).
        if (!active || !visibleAtTick || !Api::draw_allows()) { ++stats.drawSkipped; return; }
        const float width = Api::width(), height = Api::height();
        if (!(width > 0 && height > 0)) { ++stats.drawSkipped; return; }
        unsigned n = 0, count = 0;
        const DrawEntry* entries = tracker.draw_entries(&count);
        for (unsigned i = 0; i < count && n < kDrawCapacity; ++i) {
            Vec3 world = entries[i].anchor;
            if (Api::lookup(entries[i].key, &world)) ++stats.interpHits; else ++stats.interpMisses;
            Vec3 pt{};  // ortho-space point: what the painter's J2D context draws in (same space as the native HUD)
            if (!Api::project(world, &pt) || !normal_on_screen({pt.x - Api::minX(), pt.y - Api::minY(), pt.z}, width, height)) continue;
            states[n++] = {pt.x, pt.y, entries[i].fill, entries[i].trail, entries[i].alpha, entries[i].hp, entries[i].maximumHealth};
        }
        if (n) {
            Api::paint(states, n, options.showNumbers);
            stats.barsDrawn += n;
        }
        // Boss / mini-boss bar (HUD-fixed, no anchor): same pass, after the normal bars, as in Bars 1.1.1 health_draw.
        if (bossTracker.showing()) {
            Api::paint_boss(bossTracker.draw());
            ++stats.bossDraws;
        }
    }

    void meter_deleted() {
        visibleAtTick = false;
        clear_all();
        stats.scrubbed += scrub_all(Api::list(), static_cast<const Base*>(Api::packet()));
    }
    void shutdown() {
        active = false;
        meter_deleted();  // also scrubs the lists: the packet's vtable lives in this library
        tracker.clear(&envStorage());
        bossTracker.clear();
    }
    const Tracker& tr() const { return tracker; }

private:
    static bool e_project(void*, const Vec3& w, Vec3* h) { return Api::project(w, h); }
    static bool e_clear(void*, const Vec3& w) { return Api::clear_line(w); }
    static float e_dist(void*, const ActorView& v) { return Api::distance(v); }
    static void e_record(void*, uint64_t k, const Vec3& w) { Api::record(k, w); }
    static void e_forget(void*, uint64_t k) { Api::forget(k); }
    TickEnv& envStorage() { e = {nullptr, e_project, e_clear, e_dist, e_record, e_forget, Api::width(), Api::height(), Api::minX(), Api::minY()}; return e; }
    const TickEnv& env() { return envStorage(); }
    // Bars 1.1.1 boss_begin / boss_observe / boss_end around the native actor queue (values copied during this tick only).
    static bool b_read(void*, Boss k, const void* h, PhaseInput& in) { return Api::boss_read(k, h, in); }
    static bool b_los(void*, const void* h) { return Api::boss_los(h); }
    static bool b_done(void*) { return Api::dungeon_complete(); }
    void boss_tick() {
        const BossEnv benv{nullptr, b_read, b_los, b_done};
        bossTracker.begin(Api::paused(), Api::event_running(), Api::lock_target());
        const unsigned nb = Api::gather_bosses(bossActors, kBossScanCapacity);
        for (unsigned i = 0; i < nb; ++i) bossTracker.observe(bossActors[i], benv);
        bossTracker.end();
        ++stats.bossTicks;
        if (bossTracker.candidate_count() > stats.maxBossCandidates) stats.maxBossCandidates = bossTracker.candidate_count();
    }
    void clear_all() {
        tracker.clear(&envStorage());
        bossTracker.clear();
        haveStage = false; playerAddress = 0; playerId = ~0u;
    }

    static constexpr unsigned kBossScanCapacity = 128;
    Tracker tracker;
    BossTracker bossTracker;
    BossActor bossActors[kBossScanCapacity];
    TickEnv e{};
    bool active = false, visibleAtTick = false, haveStage = false;
    uint32_t playerId = ~0u;
    uintptr_t playerAddress = 0;
    char stageName[8]{};
    int8_t stageLayer = 0, stageDarkArea = 0;
    ActorView views[kTrackCapacity];
    NormalDrawState states[kDrawCapacity];
};
}  // namespace ehz
