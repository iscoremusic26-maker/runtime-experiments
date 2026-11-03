#include "boss_tracker.h"
namespace ehz {
void BossTracker::clear() {
    presenter.clear();
    drawState = copy_boss_draw(presenter.view);
    count = 0; retiredCount = 0; locked = {}; aggregate = {}; collecting = false; gohmaIdentity = {}; gohmaTimer = 0;
}
void BossTracker::begin(bool paused, bool event, Identity lockedTarget) {
    count = 0; aggregate = {}; locked = {};
    collecting = !paused;
    if (!collecting) return;
    aggregate.event = event;
    // Bars 1.1.1: the source's 0x82ad0 is Boss Rush room detection, outside the authorized port. Its default (false) is
    // preserved; ordinary intro events still count.
    aggregate.introPredicate = false;
    locked = lockedTarget;
}
void BossTracker::observe(const BossActor& a, const BossEnv& env) {
    if (!collecting) return;
    const BossDescriptor* d = boss_descriptor(a.profile);
    if (!d) return;
    const Identity who{a.address, a.id, int16_t(a.profile)};
    for (unsigned i = 0; i < retiredCount; ++i) if (same(who, retired[i])) return;
    if (a.profile == 523) { if (a.health > 0) ++aggregate.heads; return; }   // Diababa heads: aggregated, never an encounter of their own
    if (!d->primary) return;                                                 // subordinate parts never become independent bosses
    const Boss k = boss_kind_of_profile(a.profile);
    PhaseInput in{};
    if (!env.read || !env.read(env.user, k, a.handle, in)) return;
    in.event = aggregate.event;
    if (k == Boss::Diababa) {
        aggregate.hasBody = true; aggregate.bodyVulnerable = in.detail == 0;
        aggregate.health = in.sample.health; aggregate.action = in.sample.action; aggregate.mode = in.sample.mode;
    }
    if (k == Boss::Armogohma && !same(who, gohmaIdentity)) { gohmaIdentity = who; gohmaTimer = 0; }
    if (boss_dead_predicate(k, in, gohmaTimer)) return;
    if (k == Boss::DeathSword && env.dungeon_complete) in.sample.dungeonComplete = env.dungeon_complete(env.user);
    if ((k == Boss::Darknut || k == Boss::Aeralfos) && env.line_of_sight) in.lineOfSight = env.line_of_sight(env.user, a.handle);
    if (count == sizeof(candidates) / sizeof(*candidates)) return;
    auto& c = candidates[count++];
    c = {};
    c.identity = who; c.kind = k; c.primary = d->primary; c.miniboss = d->miniboss;
    c.input = in; c.customMetric = boss_uses_metric(k); c.metric = c.customMetric ? instantaneous(in.sample) : 1;
    c.hasVisibilityPredicate = has_visible_predicate(k); c.visiblePredicate = boss_visible_predicate(k, in);
}
void BossTracker::end() {
    if (!collecting) return;
    presenter.tick(choose_boss(candidates, count, presenter.view, locked), locked, aggregate);
    drawState = copy_boss_draw(presenter.view);
    if (presenter.retired.address && retiredCount < sizeof(retired) / sizeof(*retired)) retired[retiredCount++] = presenter.retired;
}
}  // namespace ehz
