// BARS203 CP03 -- encounter selection/presentation for bosses and mini-bosses. Pure logic (no game headers): the scan/aggregation
// of Bars 1.1.1 boss_runtime.cpp (boss_begin/boss_observe/boss_end/boss_clear) around the unchanged models in reused/.
// The game-dependent parts (typed field reader, line of sight, lock-on target, stage flag) arrive through BossEnv.
#pragma once
#include <stddef.h>
#include "reused/boss_catalog.h"
#include "reused/boss_draw_state.h"
#include "reused/boss_predicates.h"

namespace ehz {
// One native actor of the boss families seen in this tick. `handle` is only meaningful inside BossEnv callbacks during the scan.
struct BossActor { uintptr_t address; uint32_t id; int profile; int health; const void* handle; };
struct BossEnv {
    void* user;
    bool (*read)(void*, Boss kind, const void* handle, PhaseInput& out);  // typed reader: false = not what its profile claims
    bool (*line_of_sight)(void*, const void* handle);                     // Darknut / Aeralfos only
    bool (*dungeon_complete)(void*);                                      // Death Sword: dComIfGs_isStageMiddleBoss()
};
inline Boss boss_kind_of_profile(int p) {
    switch (p) {
    case 524: case 523: case 475: return Boss::Diababa;
    case 471: return Boss::Fyrus;
    case 243: case 210: case 528: return Boss::Morpheel;
    case 246: return Boss::Stallord;
    case 529: return Boss::Blizzeta;
    case 525: return Boss::Armogohma;
    case 247: case 533: return Boss::Argorok;
    case 534: return Boss::BeastGanon;
    case 526: return Boss::Ganondorf;
    case 459: return Boss::PuppetZelda;
    case 249: case 248: case 250: case 125: return Boss::Zant;
    case 531: return Boss::Darknut;
    case 532: return Boss::Aeralfos;
    case 520: return Boss::DeathSword;
    case 469: return Boss::KingBulblin;
    case 450: return Boss::Darkhammer;
    case 476: return Boss::Ook;
    case 512: return Boss::DekuToad;
    case 433: return Boss::Dangoro;
    case 484: return Boss::PhantomZant;
    default: return Boss::None;
    }
}
inline bool boss_uses_metric(Boss k) {
    switch (k) {
    case Boss::Fyrus: case Boss::Morpheel: case Boss::Stallord: case Boss::Blizzeta: case Boss::Armogohma: case Boss::Argorok:
    case Boss::BeastGanon: case Boss::Ganondorf: case Boss::Zant: case Boss::Darknut: case Boss::Aeralfos: case Boss::DeathSword:
    case Boss::Dangoro: return true;
    default: return false;
    }
}

class BossTracker {
public:
    // Start of a simulation tick. `paused` = the game's pause flag (nothing is collected, the presentation is frozen);
    // `event` = an event/cutscene is running; `locked` = identity of the current lock-on target.
    void begin(bool paused, bool event, Identity locked);
    void observe(const BossActor& a, const BossEnv& env);
    void end();                  // selects the encounter and advances the presenter (no-op when `begin` found the game paused)
    void clear();                // scene change / meter deleted / shutdown
    const BossDrawState& draw() const { return drawState; }
    const BossView& view() const { return presenter.view; }
    bool showing() const { return drawState.active && drawState.alpha >= 0.01f; }
    unsigned candidate_count() const { return unsigned(count); }
private:
    BossPresenter presenter{};
    BossCandidate candidates[64]{};
    size_t count = 0;
    Identity locked{}, retired[128]{};
    unsigned retiredCount = 0;
    DiababaInput aggregate{};
    bool collecting = false;
    Identity gohmaIdentity{};
    int gohmaTimer = 0;
    BossDrawState drawState{};
};
}  // namespace ehz
