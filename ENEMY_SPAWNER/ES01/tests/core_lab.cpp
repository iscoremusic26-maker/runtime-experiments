// Enemy Spawner (Standalone) 0.1.2: laboratory of the pure core (catalog, presses, scene and ground rules, tracking, Expansion observation).
// Also checks the spawner's reading of Bokoblin Expansion 0.17.0 against Expansion's own identity code (vendored, unmodified).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include "../src/spawner_core.hpp"
#include "vendor/bokoblin_expansion_0_17_0/variant_policy.hpp"

static unsigned long long g_checks = 0;
#define CHECK(x)                                              \
  do {                                                        \
    ++g_checks;                                               \
    if (!(x)) {                                               \
      std::printf("ES_LAB_FAIL line=%d %s\n", __LINE__, #x);   \
      std::exit(1);                                           \
    }                                                         \
  } while (0)

using namespace es;

static int index_of(const char* label) {
  for (std::size_t i = 0; i < kCatalogSize; ++i)
    if (!std::strcmp(kCatalog[i].label, label)) return int(i);
  return -1;
}
static Scene good_scene() {
  Scene s;
  s.link = s.link_layer = s.actor_service = true;
  return s;
}

static void lab_catalog() {
  CHECK(kCatalogSize == 50 && kOriginalCount == 45);
  unsigned black = 0, blue = 0, red = 0;
  for (std::size_t i = 0; i < kCatalogSize; ++i) {
    const Entry& e = kCatalog[i];
    CHECK(e.label && e.label[0]);
    CHECK(unsigned(e.profile) < unsigned(Profile::Count));
    for (std::size_t j = 0; j < i; ++j) CHECK(std::strcmp(kCatalog[j].label, e.label) != 0);  // a label names one entry
    CHECK(kLabels.v[i] == e.label);
    black += e.route == Route::BlackUnavailable, blue += e.route == Route::ExpansionBlue, red += e.route == Route::ExpansionRed;
    if (e.route != Route::Native) CHECK(e.profile == Profile::E_OC);
    // E_OC's subtype lives in the high byte of angle.x: 0 -> E_OC, else E_OC2.
    if (e.route == Route::ExpansionBlue) CHECK((e.angle_x >> 8) == 0);
    if (e.route == Route::ExpansionRed || e.route == Route::BlackUnavailable) CHECK((e.angle_x >> 8) != 0 && ((e.angle_x >> 8) & 0xff) != 0xff);
    if (e.adapt == Adapt::ToadpoliWater) CHECK(e.profile == Profile::E_TK);
    if (e.adapt == Adapt::ToadpoliLava) CHECK(e.profile == Profile::E_TK2);
  }
  CHECK(black == 1 && blue == 1 && red == 1);
  CHECK(std::strstr(kCatalog[index_of("Bokoblin Black (Expansion): integration unavailable")].label, "integration unavailable") != nullptr);
  CHECK(index_of("Goron") < 0 && index_of("Staltroop") < 0);
  CHECK(index_of("Lizalfos") == 6);  // the default of the persisted "enemy" index  // an NPC and an arena-owned enemy are not offered
  // Lizalfos / Dynalfos: low byte 0xFF (native patrol), never 0 (ACTION_STAY); the defeated switch byte stays the 0xFF sentinel.
  CHECK((kCatalog[index_of("Lizalfos")].parameters & 0xff) == 0xff && (kCatalog[index_of("Lizalfos")].parameters >> 24) == 0xff);
  CHECK((kCatalog[index_of("Dynalfos")].parameters & 0xff) == 0xff);
  CHECK(kCatalog[index_of("Helmasaurus")].argument == 1 && kCatalog[index_of("Helmasaur")].argument == -1);
  CHECK(kCatalog[index_of("Stalfos")].angle_z == 0xff && kCatalog[index_of("Kargarok")].angle_z == 0xff);
}

// 0.1.2: the appended native variants, decoded exactly as their native create() does (catalog.hpp decode_selector, d_a_e_sf.cpp / d_a_b_tn.cpp / d_a_e_rd.cpp).
static void lab_variants() {
  // The 0.1.1 entries keep their indices: the persisted chooser index still names the same enemy.
  CHECK(index_of("Darknut") == 0 && index_of("Bokoblin Black (Expansion): integration unavailable") == 5 && index_of("Lizalfos") == 6 && index_of("Stalfos") == 9 &&
        index_of("Bulblin") == 8 && index_of("Black Chu") == 44);
  CHECK(index_of("Stalfos (Alternate Attack)") == 45 && index_of("Darknut (Sword)") == 46 && index_of("Stalfos (Breakable Shield)") == 47 && index_of("Bulblin (Bow)") == 48 &&
        index_of("Bulblin (Fire Bow)") == 49);
  for (std::size_t i = kOriginalCount; i < kCatalogSize; ++i) CHECK(kCatalog[i].route == Route::Native && kCatalog[i].adapt == Adapt::None && kCatalog[i].argument == -1);
  // Stalfos: base mType 0 (ACTION_ATTACK, BCK_SF_ATTACK01) and the alternate mType 1 (ACTION_ATTACK_0, BCK_SF_ATTACK02). Same switch sentinel.
  const Entry& sf = kCatalog[index_of("Stalfos")];
  const Entry& sf1 = kCatalog[index_of("Stalfos (Alternate Attack)")];
  CHECK(sf.parameters == 0x0000ff00u && sf1.parameters == 0x0100ff00u && sf.profile == Profile::E_SF && sf1.profile == Profile::E_SF);
  CHECK(sf.angle_z == 0xff && sf1.angle_z == 0xff && sf1.angle_x == 0 && !sf1.flying);
  CHECK(decode_selector(Profile::E_SF, sf.parameters).a == 0 && decode_selector(Profile::E_SF, sf.parameters).b == 0);
  CHECK(decode_selector(Profile::E_SF, sf1.parameters).a == 1 && decode_selector(Profile::E_SF, sf1.parameters).b == 0);
  CHECK(stalfos::expected_action(0) == stalfos::kActionAttack && stalfos::expected_bck(stalfos::kActionAttack) == stalfos::kBckAttack01);
  CHECK(stalfos::expected_action(1) == stalfos::kActionAttack0 && stalfos::expected_bck(stalfos::kActionAttack0) == stalfos::kBckAttack02);
  CHECK(stalfos::kActionAttack0 == 4 && stalfos::kActionAttack == 5 && stalfos::kBckAttack01 == 4 && stalfos::kBckAttack02 == 5);
  // Low bytes as the base: mWaitType 0 (ACTION_NORMAL), arg1 0xFF (-> 3). Only the high nibble selects.
  CHECK((sf1.parameters & 0x00ffffffu) == (sf.parameters & 0x00ffffffu));
  // Native clamps: mType > 1 -> 0, arg3 > 1 -> 0.
  CHECK(decode_selector(Profile::E_SF, 0x0700ff00u).a == 0 && decode_selector(Profile::E_SF, 0x3000ff00u).b == 0);
  // Breakable shield: arg3 1 (BMDR_SF_SHIELDB, durability), mType 0.
  const Entry& sfs = kCatalog[index_of("Stalfos (Breakable Shield)")];
  CHECK(sfs.parameters == 0x1000ff00u && sfs.angle_z == 0xff && decode_selector(Profile::E_SF, sfs.parameters).a == 0 && decode_selector(Profile::E_SF, sfs.parameters).b == 1);
  // Darknut: the existing entry IS the mace Darknut (mType 1, mType2 0 -> BMDR_TN2_MACE). The sword one differs only by mType2.
  const Entry& dn = kCatalog[index_of("Darknut")];
  const Entry& dn2 = kCatalog[index_of("Darknut (Sword)")];
  CHECK(dn.parameters == 0x000001ffu && dn2.parameters == 0x010001ffu && dn2.profile == Profile::B_TN && dn2.angle_z == 0 && !dn2.flying);
  CHECK(decode_selector(Profile::B_TN, dn.parameters).a == 1 && decode_selector(Profile::B_TN, dn.parameters).b == 0);
  CHECK(decode_selector(Profile::B_TN, dn2.parameters).a == 1 && decode_selector(Profile::B_TN, dn2.parameters).b == 1);
  CHECK((dn2.parameters & 0xffu) == 0xffu);  // mSwitchNo 0xFF: no defeated-switch
  CHECK(std::uint8_t((dn2.parameters >> 16) & 0xffffu) == 0 && std::uint8_t((dn.parameters >> 16) & 0xffffu) == 0);  // mBrkAnmFrame (u8): the same armour colour frame
  unsigned maces = 0;
  for (std::size_t i = 0; i < kCatalogSize; ++i)
    if (kCatalog[i].profile == Profile::B_TN) {
      const Selector s = decode_selector(Profile::B_TN, kCatalog[i].parameters);
      CHECK(s.a == 1);  // never the Temple of Time Darknut (mType 0)
      maces += s.b == 0;
    }
  CHECK(maces == 1);  // the mace Darknut is offered once, not duplicated
  CHECK(no_temple_of_time_darknut());
  CHECK(decode_selector(Profile::B_TN, 0x000000ffu).a == 0 && decode_selector(Profile::B_TN, 0x000002ffu).a == 0);  // what would be the Temple of Time one
  // Bulblin: club 1 (base), bow 2, fire bow 3; 4 (bomb arrows) is refused by the native create and is not offered.
  CHECK(decode_selector(Profile::E_RD, kCatalog[index_of("Bulblin")].parameters).a == 1);
  CHECK(decode_selector(Profile::E_RD, kCatalog[index_of("Bulblin (Bow)")].parameters).a == 2 && kCatalog[index_of("Bulblin (Bow)")].parameters == 0xff000200u);
  CHECK(decode_selector(Profile::E_RD, kCatalog[index_of("Bulblin (Fire Bow)")].parameters).a == 3 && kCatalog[index_of("Bulblin (Fire Bow)")].parameters == 0xff000300u);
  CHECK(bulblin_weapons_creatable() && decode_selector(Profile::E_RD, 0xff000f00u).a == 0);
  for (const char* b : {"Bulblin (Bow)", "Bulblin (Fire Bow)"}) CHECK((kCatalog[index_of(b)].parameters & 0xff0000ffu) == (kCatalog[index_of("Bulblin")].parameters & 0xff0000ffu));
  CHECK(!decode_selector(Profile::E_DN, 0xff0000ffu).known);
  // Not offered in 0.1.2.
  CHECK(index_of("Darknut (Temple of Time)") < 0 && index_of("Darknut (Mace)") < 0 && index_of("Darknut (Greatsword)") < 0 && index_of("Bulblin (Bomb Arrows)") < 0);
  for (std::size_t i = 0; i < kCatalogSize; ++i) CHECK(std::strstr(kCatalog[i].label, "Aeralfos") == nullptr || std::strcmp(kCatalog[i].label, "Aeralfos") == 0);
}

// 0.1.2: read-only telemetry. What the actor decoded is compared with the catalog; a Stalfos attack is noted once per kind, with its expectation.
static void lab_telemetry() {
  Event ev[Spawner::kEvents];
  Spawner sp;
  CHECK(sp.press(index_of("Stalfos (Alternate Attack)"), 1) == Press::Accepted);
  sp.created(true, 300, 1);
  Probe p;
  p.found = true, p.creating = true;  // not yet: nothing is read while the create runs
  p.selector_read = false;
  sp.observe(0, p, 2);
  p.creating = false, p.selector_read = true, p.sel_a = 1, p.sel_b = 0, p.stalfos = true, p.sf_action = 0, p.sf_anm = stalfos::kBckAttack01;
  sp.observe(0, p, 3);
  unsigned n = sp.drain(ev, Spawner::kEvents);
  CHECK(n == 3 && ev[1].kind == Ev::Appeared && ev[2].kind == Ev::NativeSelector && ev[2].why == 1 && ev[2].a == 1 && ev[2].b == 0 && sp.c.selector_match == 1);
  sp.observe(0, p, 4);
  CHECK(sp.drain(ev, Spawner::kEvents) == 0);  // reported once
  p.sf_action = stalfos::kActionAttack0, p.sf_anm = stalfos::kBckAttack02;
  for (std::uint64_t t = 5; t < 15; ++t) sp.observe(0, p, t);
  n = sp.drain(ev, Spawner::kEvents);
  CHECK(n == 1 && ev[0].kind == Ev::NativeAttack && ev[0].why == 1 && ev[0].action == stalfos::kActionAttack0 && ev[0].anm == stalfos::kBckAttack02 && ev[0].a == 1);
  CHECK(sp.c.attack_alt == 1 && sp.c.attack_base == 0 && sp.c.attack_unexpected == 0);
  p.sf_action = stalfos::kActionAttack;  // the other attack running on an mType 1 Stalfos would be reported, never hidden
  sp.observe(0, p, 20);
  n = sp.drain(ev, Spawner::kEvents);
  CHECK(n == 1 && ev[0].kind == Ev::NativeAttack && ev[0].why == 0 && sp.c.attack_unexpected == 1);
  // The base Stalfos: ACTION_ATTACK expected.
  Spawner s2;
  CHECK(s2.press(index_of("Stalfos"), 1) == Press::Accepted);
  s2.created(true, 301, 1);
  Probe q = p;
  q.sel_a = 0, q.sf_action = stalfos::kActionAttack, q.sf_anm = stalfos::kBckAttack01;
  s2.observe(0, q, 2);
  n = s2.drain(ev, Spawner::kEvents);
  CHECK(n == 4 && ev[2].kind == Ev::NativeSelector && ev[2].why == 1 && ev[3].kind == Ev::NativeAttack && ev[3].why == 1 && s2.c.attack_base == 1);
  // A mismatch is reported as one.
  Spawner s3;
  CHECK(s3.press(index_of("Darknut (Sword)"), 1) == Press::Accepted);
  s3.created(true, 302, 1);
  Probe d;
  d.found = true, d.selector_read = true, d.sel_a = 1, d.sel_b = 0;
  s3.observe(0, d, 2);
  n = s3.drain(ev, Spawner::kEvents);
  CHECK(ev[n - 1].kind == Ev::NativeSelector && ev[n - 1].why == 0 && s3.c.selector_mismatch == 1 && s3.c.selector_match == 0);
  // The mace Darknut and the Bulblin bow: matches. No attack telemetry outside Stalfos.
  for (const char* label : {"Darknut", "Bulblin (Bow)", "Bulblin (Fire Bow)", "Stalfos (Breakable Shield)"}) {
    Spawner s4;
    CHECK(s4.press(index_of(label), 1) == Press::Accepted);
    s4.created(true, 303, 1);
    const Selector want = decode_selector(kCatalog[index_of(label)].profile, kCatalog[index_of(label)].parameters);
    Probe r;
    r.found = true, r.selector_read = true, r.sel_a = want.a, r.sel_b = want.b, r.sf_action = stalfos::kActionAttack0;
    s4.observe(0, r, 2);
    n = s4.drain(ev, Spawner::kEvents);
    CHECK(n == 3 && ev[2].kind == Ev::NativeSelector && ev[2].why == 1);
  }
  // Profiles without a decoded selector: no telemetry at all.
  Spawner s5;
  CHECK(s5.press(index_of("Lizalfos"), 1) == Press::Accepted);
  s5.created(true, 304, 1);
  Probe z;
  z.found = true, z.selector_read = true, z.stalfos = true, z.sf_action = stalfos::kActionAttack0;
  s5.observe(0, z, 2);
  n = s5.drain(ev, Spawner::kEvents);
  CHECK(n == 2 && s5.c.selector_match + s5.c.selector_mismatch + s5.c.attack_alt + s5.c.attack_unexpected == 0);
}

static void lab_scene_and_ground() {
  CHECK(judge_scene(good_scene()) == Wait::Ready);
  Scene s = good_scene();
  s.actor_service = false;
  CHECK(judge_scene(s) == Wait::NoService);
  s = good_scene(), s.link = false;
  CHECK(judge_scene(s) == Wait::NoLink);
  s = good_scene(), s.link_layer = false;
  CHECK(judge_scene(s) == Wait::BadLayer);
  s = good_scene(), s.next_stage = true;
  CHECK(judge_scene(s) == Wait::Transition);
  s = good_scene(), s.event = true;
  CHECK(judge_scene(s) == Wait::Event);
  s = good_scene(), s.paused = true;
  CHECK(judge_scene(s) == Wait::Paused);
  GroundSample g;
  CHECK(judge_ground(g) == Ground::NoGround);
  g.found = true, g.ground_y = 10, g.link_y = 0;
  CHECK(judge_ground(g) == Ground::Ok);
  g.ground_y = policy::kMaxStep + 1;
  CHECK(judge_ground(g) == Ground::TooHigh);
  g.ground_y = -policy::kMaxStep - 1;
  CHECK(judge_ground(g) == Ground::TooLow);
  g.ground_y = 0, g.normal_y = 0.5f;
  CHECK(judge_ground(g) == Ground::Slope);
  g.normal_y = 1, g.water = true, g.water_y = 30;
  CHECK(judge_ground(g) == Ground::Water);
  g.water_y = -5;
  CHECK(judge_ground(g) == Ground::Ok);
  g.blocked = true;
  CHECK(judge_ground(g) == Ground::Blocked);
}

static void lab_presses() {
  Spawner sp;
  CHECK(sp.press(-1, 1) == Press::InvalidIndex && sp.press(std::int64_t(kCatalogSize), 1) == Press::InvalidIndex && sp.press(1LL << 40, 1) == Press::InvalidIndex);
  // Black is never creatable, with or without Expansion, confirmed or not.
  const int b = index_of("Bokoblin Black (Expansion): integration unavailable");
  for (Expansion x : {Expansion::Absent, Expansion::Possible, Expansion::Confirmed, Expansion::Refuted}) {
    sp.expansion = x;
    CHECK(sp.press(b, 1) == Press::BlackUnavailable && !sp.pending());
  }
  // Expansion entries need the framework; a refutation closes them for the session.
  const int blue = index_of("Bokoblin Blue (Expansion)"), red = index_of("Bokoblin Red (Expansion)");
  sp.expansion = Expansion::Absent;
  CHECK(sp.press(blue, 1) == Press::ExpansionAbsent && sp.press(red, 1) == Press::ExpansionAbsent && !sp.pending());
  sp.expansion = Expansion::Refuted;
  CHECK(sp.press(blue, 1) == Press::ExpansionRefuted);
  sp.expansion = Expansion::Possible;
  CHECK(sp.press(blue, 1) == Press::Accepted && sp.pending());
  CHECK(sp.press(index_of("Lizalfos"), 1) == Press::Busy);  // double click: one request
  // A press waits for a safe frame, then expires.
  Scene paused = good_scene();
  paused.paused = true;
  CHECK(sp.ready(paused, 2) == Wait::Paused && sp.pending());
  CHECK(sp.ready(paused, 2 + policy::kPendingTicks) == Wait::Paused && !sp.pending());
  Event ev[Spawner::kEvents];
  unsigned n = sp.drain(ev, Spawner::kEvents);
  CHECK(n == 1 && ev[0].kind == Ev::Expired && ev[0].why == std::uint8_t(Wait::Paused));
  // No safe ground: nothing created, the press ends.
  CHECK(sp.press(index_of("Lizalfos"), 10) == Press::Accepted);
  CHECK(sp.ready(good_scene(), 11) == Wait::Ready);
  sp.reject(Ground::Water, 11);
  n = sp.drain(ev, Spawner::kEvents);
  CHECK(!sp.pending() && n == 1 && ev[0].kind == Ev::Rejected && sp.live() == 0);
  // A refused service call is not tracked.
  CHECK(sp.press(index_of("Lizalfos"), 12) == Press::Accepted);
  sp.created(false, 0xFFFFFFFFu, 12);
  n = sp.drain(ev, Spawner::kEvents);
  CHECK(sp.live() == 0 && n == 1 && ev[0].kind == Ev::CreateFailed);
  // The limit counts requests and live actors; it never frees capacity.
  for (unsigned i = 0; i < policy::kMaxLive; ++i) {
    CHECK(sp.press(index_of("Keese"), 20 + i) == Press::Accepted);
    sp.created(true, 1000 + i, 20 + i);
  }
  CHECK(sp.live() == policy::kMaxLive && sp.press(index_of("Keese"), 40) == Press::Full);
}

static void lab_lifecycle() {
  Spawner sp;
  Event ev[Spawner::kEvents];
  CHECK(sp.press(index_of("Lizalfos"), 1) == Press::Accepted);
  sp.created(true, 77, 1);
  CHECK(sp.t[0].life == Life::Creating && sp.t[0].id == 77);
  Probe p;
  p.creating = true;
  sp.observe(0, p, 2);
  CHECK(sp.t[0].life == Life::Creating);
  p.found = true;  // in the actor queue while its create still runs: not visible yet
  sp.observe(0, p, 3);
  CHECK(sp.t[0].life == Life::Creating);
  p.creating = false;
  sp.observe(0, p, 4);
  CHECK(sp.t[0].life == Life::Alive);
  p.found = false;  // death, deletion or scene teardown
  sp.observe(0, p, 5);
  CHECK(sp.t[0].life == Life::Free);
  unsigned n = sp.drain(ev, Spawner::kEvents);
  CHECK(n == 3 && ev[0].kind == Ev::Created && ev[1].kind == Ev::Appeared && ev[2].kind == Ev::Vanished);
  // A request that ends without an actor (its own create refused it, or its scene went away).
  CHECK(sp.press(index_of("Lizalfos"), 10) == Press::Accepted);
  sp.created(true, 78, 10);
  Probe none;
  sp.observe(0, none, 11);
  n = sp.drain(ev, Spawner::kEvents);
  CHECK(sp.t[0].life == Life::Free && ev[n - 1].kind == Ev::CreateFailed);
  // A creation that never ends is reported and forgotten.
  CHECK(sp.press(index_of("Lizalfos"), 20) == Press::Accepted);
  sp.created(true, 79, 20);
  Probe stuck;
  stuck.creating = true;
  sp.observe(0, stuck, 20 + policy::kCreateTicks + 1);
  n = sp.drain(ev, Spawner::kEvents);
  CHECK(sp.t[0].life == Life::Free && ev[n - 1].kind == Ev::CreateTimeout);
  // An id the engine hands out again is never two actors of ours.
  CHECK(sp.press(index_of("Lizalfos"), 30) == Press::Accepted);
  sp.created(true, 90, 30);
  CHECK(sp.press(index_of("Lizalfos"), 31) == Press::Accepted);
  sp.created(true, 90, 31);
  unsigned with90 = 0;
  for (const auto& x : sp.t) with90 += x.life != Life::Free && x.id == 90;
  CHECK(with90 == 1 && sp.c.id_reused == 1);
  sp.forget_all();
  CHECK(sp.live() == 0 && !sp.pending());
}

// What Expansion 0.17.0 itself decides for a fresh Bokoblin created by this mod: no DEVF registration matches it (Registration::None).
static void lab_expansion_contract() {
  namespace dv = devf_variant;
  const dv::Plan blue = dv::make_plan("E_OC", 40, 40, true, dv::Registration::None, 0);
  CHECK(blue.variant == dv::Variant::Blue && blue.initial_hp == 220 && blue.write_hp);
  const dv::Plan red = dv::make_plan("E_OC2", 220, 220, true, dv::Registration::None, 0);
  CHECK(red.variant == dv::Variant::Red && red.initial_hp == 330 && red.write_hp);
  // Black exists only through an exact registration that Expansion builds at its own initialization from its packaged encounters.
  for (int hp = 1; hp <= 999; hp += 37) CHECK(dv::make_plan("E_OC2", 220, 220, true, dv::Registration::None, hp).variant != dv::Variant::Black);
  CHECK(dv::make_plan("E_OC2", 220, 220, true, dv::Registration::Black, 440).variant == dv::Variant::Black);
  // What the spawner reads back, from the same numbers.
  CHECK(es::classify(false, 40, blue.initial_hp) == es::Variant::Blue && es::classify(true, 220, red.initial_hp) == es::Variant::Red);
  CHECK(es::classify(false, 40, 40) == es::Variant::Native && es::classify(true, 220, 220) == es::Variant::Native);
  CHECK(es::classify(true, 220, 440) == es::Variant::Unexpected);  // a 440 HP E_OC2 is not taken for anything the spawner can name
  CHECK(es::classify(false, 80, 220) == es::Variant::Unexpected);
  CHECK(es::classify(true, 300, 330) == es::Variant::Unexpected && es::classify(false, 40, 330) == es::Variant::Unexpected);  // the creation value is part of the signature  // another mod changed the creation value: not Expansion's signature

  // Observation through the tracker.
  Spawner sp;
  Event ev[Spawner::kEvents];
  sp.set_framework_present(true);
  CHECK(sp.expansion == Expansion::Possible);
  CHECK(sp.press(index_of("Bokoblin Red (Expansion)"), 1) == Press::Accepted);
  sp.created(true, 5, 1);
  Probe p;
  p.found = true, p.bokoblin = true, p.e_oc2 = true, p.field_0x560 = 220, p.health = 220;
  sp.observe(0, p, 2);
  p.health = 330;
  sp.observe(0, p, 3);
  CHECK(sp.expansion == Expansion::Confirmed && sp.c.classified == 1);
  unsigned n = sp.drain(ev, Spawner::kEvents);
  CHECK(ev[n - 1].kind == Ev::Classified && ev[n - 1].why == std::uint8_t(es::Variant::Red));
  // Without Expansion's write, the asked route is refuted, and closes.
  Spawner s2;
  s2.set_framework_present(true);
  CHECK(s2.press(index_of("Bokoblin Blue (Expansion)"), 1) == Press::Accepted);
  s2.created(true, 6, 1);
  Probe q;
  q.found = true, q.bokoblin = true, q.e_oc2 = false, q.field_0x560 = 40, q.health = 40;
  for (std::uint64_t t = 2; t < 2 + policy::kVerifyTicks + 2; ++t) s2.observe(0, q, t);
  CHECK(s2.expansion == Expansion::Refuted && s2.c.not_classified == 1);
  CHECK(s2.press(index_of("Bokoblin Blue (Expansion)"), 50) == Press::ExpansionRefuted);
  n = s2.drain(ev, Spawner::kEvents);
  CHECK(ev[n - 1].kind == Ev::NotClassified && ev[n - 1].why == std::uint8_t(es::Variant::Native));
  // A native entry spawned while Expansion is loaded: observed, never a refutation of the Expansion entries.
  Spawner s3;
  s3.set_framework_present(true);
  CHECK(s3.press(index_of("Bokoblin (E_OC, native)"), 1) == Press::Accepted);
  s3.created(true, 7, 1);
  for (std::uint64_t t = 2; t < 2 + policy::kVerifyTicks + 2; ++t) s3.observe(0, q, t);
  CHECK(s3.expansion == Expansion::Possible);
  // The framework disappearing makes the Expansion entries unavailable again.
  s3.set_framework_present(false);
  CHECK(s3.expansion == Expansion::Absent && s3.press(index_of("Bokoblin Red (Expansion)"), 99) == Press::ExpansionAbsent);
}

int main() {
  lab_catalog();
  lab_variants();
  lab_telemetry();
  lab_scene_and_ground();
  lab_presses();
  lab_lifecycle();
  lab_expansion_contract();
  std::printf("ES_CORE_LAB version=%s checks=%llu failures=0 RESULT=LAB_PASS scope=PURE_CORE_AND_EXPANSION_0_17_0_IDENTITY_SOURCE runtime=HUMAN_RUNTIME_PENDING\n", kVersion, g_checks);
  return 0;
}
