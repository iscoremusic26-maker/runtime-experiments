// BARS203 CP02 -- game-facing side of the normal-bar renderer (hooks call these; see BARS203_CP02_REPORT.md).
#pragma once
#include <stdint.h>
class dMeter2_c;
namespace ehz {
struct BarsStats {
    uint64_t ticks = 0, queued = 0, queueRefused = 0, hudNotQueued = 0, packetDraws = 0, barsDrawn = 0, drawSkipped = 0, scrubbed = 0, interpHits = 0, interpMisses = 0;
    unsigned maxPublished = 0, maxTracked = 0, maxBossCandidates = 0;
    uint64_t bossTicks = 0, bossShownTicks = 0, bossDraws = 0;
};
// Runs once per simulation tick, from the _draw post hook (all actors have executed this tick).
void bars_sim_tick(dMeter2_c* meter, uint32_t simTick);
// dMeter2_c is being destroyed (pre hook): drop instances and any pending packet.
void bars_meter_deleted();
// mod_shutdown: remove the packet from every 2D draw list and drop all state (loader retires the hooks afterwards).
void bars_shutdown();
void bars_set_active(bool active);
const BarsStats& bars_stats();
unsigned bars_tracked();
}  // namespace ehz
