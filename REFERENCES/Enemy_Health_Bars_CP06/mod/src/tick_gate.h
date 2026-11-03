// BARS203 CP02 -- decides when the per-tick bar pass runs. _execute is called only on simulation ticks; _draw is called on
// simulation ticks AND on presentation-only frames. The bar pass runs on the first _draw after each _execute.
#pragma once
#include <stdint.h>
namespace ehz {
struct TickGate {
    uint32_t simTick = 1, lastDrawTick = 0;
    void on_execute() { ++simTick; }
    // true => run the pass for `simTick` (once per simulation tick)
    bool on_draw() {
        if (lastDrawTick == simTick) return false;
        lastDrawTick = simTick;
        return true;
    }
};
}  // namespace ehz
