// BARS203 CP02 -- the three InterpService calls the bars use (shared by the game build and the lab build).
#pragma once
#include "mods/svc/interp.h"
#include "tracker.h"
extern ModContext* mod_ctx;
extern const InterpService* svc_interp;  // optional import (mod.cpp): null when the host does not provide it
namespace ehz {
// Record this tick's anchor of one instance (the recording window spans the simulation tick's execute + draw handlers).
inline void interp_record(uint64_t key, const Vec3& w) {
    if (!svc_interp) return;
    InterpMtx m = {{1, 0, 0, w.x}, {0, 1, 0, w.y}, {0, 0, 1, w.z}};  // pure translation: the lerp is a straight line
    svc_interp->record_mtx_keyed(mod_ctx, m, interp_key(key));
}
inline void interp_forget(uint64_t key) { if (svc_interp) svc_interp->forget_mtx(mod_ctx, interp_key(key)); }
// Interpolated anchor for the current presentation frame; false when unknown (not interpolating / new instance / sync frame).
inline bool interp_lookup(uint64_t key, Vec3* w) {
    if (!svc_interp) return false;
    InterpMtx m;
    if (!svc_interp->lookup_replacement_mtx(interp_key(key), m)) return false;
    *w = {m[0][3], m[1][3], m[2][3]};
    return true;
}
}  // namespace ehz
