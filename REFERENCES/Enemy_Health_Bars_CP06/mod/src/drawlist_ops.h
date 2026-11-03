// BARS203 CP02 -- generic 2D draw-list helpers (pure templates; tested in the lab with a modelled list).
#pragma once
namespace ehz {
// Remove every entry equal to `packet` from a draw list laid out as the game's `T* list[N]` + `T** end`, compacting the rest
// and nulling the freed tail. Leaves the list untouched when `end` is not a pointer into the list's own array (list not
// initialised). Returns the number of removed entries.
template <class T, unsigned N>
unsigned scrub_list(T* (&list)[N], T**& end, const T* packet) {
    if (end < list || end > list + N) return 0;
    T** out = list;
    unsigned removed = 0;
    for (T** p = list; p < end; ++p) { if (*p != packet) *out++ = *p; else ++removed; }
    for (T** p = out; p < end; ++p) *p = nullptr;
    end = out;
    return removed;
}
// True when `needle` is among the first `end - list` entries of a list, bounded to `N` (defensive against a bogus end pointer).
template <class T, unsigned N>
bool list_contains(T* const (&list)[N], T* const* end, const T* needle) {
    if (!needle || end < list || end > list + N) return false;
    for (T* const* i = list; i < end; ++i) if (*i == needle) return true;
    return false;
}
}  // namespace ehz

namespace ehz {
enum class QueueResult { HudNotQueued, Queued, Refused };
// Queue `packet` in the 2D XLU list, but only when the native HUD queued its own meter (honours recording mode, minimal HUD,
// fly camera, ...). `D` has the dDlst_list_c members mp2DOpaTop*/mp2DOpa*/mp2DXlu* and set2DXlu(); a refused set() (full list,
// or not a simulation frame) is detected through the list pointer not advancing.
template <class D, class B>
QueueResult queue_after_hud(D& d, const B* hud, B* packet) {
    const bool found = hud && (list_contains(d.mp2DOpaTopDrawLists, d.mp2DOpaTopStart, hud) || list_contains(d.mp2DOpaDrawLists, d.mp2DOpaStart, hud));
    if (!found) return QueueResult::HudNotQueued;
    auto** before = d.mp2DXluStart;
    d.set2DXlu(packet);
    return d.mp2DXluStart != before ? QueueResult::Queued : QueueResult::Refused;
}
// Remove the packet from every 2D list the game owns (OpaTop, Opa, Xlu). Used on meter deletion and on mod shutdown.
template <class D, class B>
unsigned scrub_all(D& d, const B* packet) {
    return scrub_list(d.mp2DOpaTopDrawLists, d.mp2DOpaTopStart, packet) + scrub_list(d.mp2DOpaDrawLists, d.mp2DOpaStart, packet) +
           scrub_list(d.mp2DXluDrawLists, d.mp2DXluStart, packet);
}
}  // namespace ehz
