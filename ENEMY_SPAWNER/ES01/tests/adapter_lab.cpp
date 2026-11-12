// Enemy Spawner (Standalone) 0.1.2: the PRODUCTION adapter (src/spawner_adapter.inc, included verbatim) over a model of the engine rules it depends on.
// Model, from TwilitRealm/dusklight@40457c6 (inspection, not execution):
//  * ActorService::create_actor -> fopAcM_create -> fpcM_Create records fpcLy_CurrentLayer() in the asynchronous request (src/dusk/mods/svc/actor.cpp,
//    f_pc_manager). The actor is later owned by that layer.
//  * A layer's actors are deleted with it; a root-owned actor survives the play scene. The play scene draws its actors through the actor queue,
//    and the root traversal draws root-owned processes too: a root-owned enemy is drawn twice (Dawnlight docs/darknut-arena-spawner.md).
//  * fopAcM_SearchByID finds a process once it is in the actor queue (first create step); fpcM_IsCreating stays true until its create completes.
//  * 0.1.2: the native create() of E_SF, B_TN and E_RD decodes its selector from the parameters (d_a_e_sf.cpp L1774-1782, d_a_b_tn.cpp L5034-5066,
//    d_a_e_rd.cpp L7375-7378). The model decodes them with its OWN copy of those lines (below), not with the catalog's decode_selector.
// Declared limits: no renderer, no collision, no real actor, no AI: a model of the rules above, not a run of the game. Which attack a Stalfos runs
// is set by the scenario, not by the model: only the game shows it.
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <string>
#include <vector>
#include "../src/spawner_core.hpp"

static unsigned long long g_checks = 0;
#define CHECK(x)                                              \
  do {                                                        \
    ++g_checks;                                               \
    if (!(x)) {                                               \
      std::printf("ES_LAB_FAIL line=%d %s\n", __LINE__, #x);   \
      std::exit(1);                                           \
    }                                                         \
  } while (0)

// ---------------------------------------------------------------- engine model
using s16 = std::int16_t;
using u32 = std::uint32_t;
using BOOL = int;
enum ModResult { MOD_OK = 0, MOD_ERROR = 1, MOD_UNAVAILABLE = 2, MOD_INVALID_ARGUMENT = 5 };
struct ModContext {};
static ModContext g_ctx;
static ModContext* mod_ctx = &g_ctx;
using ProfileName = std::int16_t;
using ActorId = std::uint32_t;
using ConfigVarHandle = std::uint64_t;
struct ActorSpawnParams {
  std::uint32_t parameters;
  std::int8_t argument, room_num;
  struct { float x, y, z; } position;
  struct { std::int16_t x, y, z; } angle;
  struct { float x, y, z; } scale;
  int (*create_function)(void*);
};
struct layer_class { bool deleting = false; int name = 0; };
static layer_class g_root{false, 0}, g_play{false, 1};
static layer_class* g_current = &g_root;
static layer_class* fpcLy_CurrentLayer() { return g_current; }
static layer_class* fpcLy_RootLayer() { return &g_root; }
static void fpcLy_SetCurrentLayer(layer_class* l) { g_current = l; }
static BOOL fpcLy_IsDeletingMesg(layer_class* l) { return l->deleting; }
struct cXyz {
  float x = 0, y = 0, z = 0;
  cXyz() = default;
  cXyz(float a, float b, float c) : x(a), y(b), z(c) {}
};
static float cM_ssin(s16 a) { return std::sin(a * 3.14159265f / 32768.0f); }
static float cM_scos(s16 a) { return std::cos(a * 3.14159265f / 32768.0f); }
struct csXyz { s16 x = 0, y = 0, z = 0; };
struct fopAc_ac_c {
  s16 name = 0;
  std::uint32_t id = 0;
  cXyz pos;
  struct { cXyz pos; } current;
  csXyz shape_angle;
  int room = 3;
  virtual ~fopAc_ac_c() = default;
};
struct layer_tag_t { layer_class* layer = &g_play; };
struct daAlink_c : fopAc_ac_c { layer_tag_t layer_tag; };
struct e_tk_class : fopAc_ac_c { s16 mExecuteState = 20; };
struct e_tk2_class : fopAc_ac_c { s16 mActionTimer[4] = {0, 0, 0, 20}; };
struct daE_OC_c : fopAc_ac_c { const char* mName = "E_OC"; s16 field_0x560 = 40, health = 40; };
// 0.1.2 telemetry targets. The production adapter reinterpret_casts to e_sf_class / e_rd_class like the native code; here they derive from the
// model actor so that the address is the same.
using u8 = std::uint8_t;
struct e_sf_class : fopAc_ac_c { u8 mWaitType = 0, arg1 = 0, mType = 0, arg3 = 0; int mAnm = 0xC; s16 mAction = 0; };
struct daB_TN_c : fopAc_ac_c { u8 mBrkAnmFrame = 0, mSwitchNo = 0, mType = 0, mType2 = 0; };
struct e_rd_class : fopAc_ac_c { u8 arg0 = 0, weapon_type = 0; };
constexpr s16 fpcNm_E_OC_e = 510, fpcNm_E_TK_e = 600, fpcNm_E_TK2_e = 601, fpcNm_E_DN_e = 435, fpcNm_E_SF_e = 520, fpcNm_B_TN_e = 300, fpcNm_E_RD_e = 515;
static daAlink_c g_link_obj;
static daAlink_c* g_link = &g_link_obj;
static daAlink_c* daAlink_getAlinkActorClass() { return g_link; }
static bool g_next_stage = false, g_event = false, g_pause = false;
static BOOL dComIfGp_isEnableNextStage() { return g_next_stage; }
static BOOL dComIfGp_event_runCheck() { return g_event; }
static std::uint8_t dComIfGp_isPauseFlag() { return g_pause; }
static int fopAcM_GetRoomNo(const fopAc_ac_c* a) { return a->room; }
static s16 fopAcM_GetName(const fopAc_ac_c* a) { return a->name; }
// Requests and actors
struct Request { ActorId id; ProfileName profile; ActorSpawnParams p; layer_class* owner; };
static std::vector<Request> g_requests;
struct Live { fopAc_ac_c* a; layer_class* owner; bool creating; };
static std::vector<Live> g_live;
static std::uint32_t g_next_id = 100;
static ModResult g_service_result = MOD_OK;
static bool g_service_throws = false;
static ModResult create_actor(ModContext*, ProfileName profile, const ActorSpawnParams* p, ActorId* id) {
  if (g_service_throws) throw std::runtime_error("service failure");
  if (g_service_result != MOD_OK) return g_service_result;
  *id = ++g_next_id;
  g_requests.push_back({*id, profile, *p, fpcLy_CurrentLayer()});  // fpcM_Create: the CURRENT layer, now
  return MOD_OK;
}
struct ActorService { ModResult (*create_actor)(ModContext*, ProfileName, const ActorSpawnParams*, ActorId*); };
static ActorService g_actor_service{&create_actor};
static const ActorService* svc_actor = &g_actor_service;
static int fopAcM_SearchByID(std::uint32_t id, fopAc_ac_c** out) {
  *out = nullptr;
  for (auto& l : g_live)
    if (l.a->id == id) *out = l.a;
  return *out != nullptr;
}
static BOOL fpcM_IsCreating(std::uint32_t id) {
  for (auto& l : g_live)
    if (l.a->id == id) return l.creating;
  for (auto& r : g_requests)
    if (r.id == id) return 1;
  return 0;
}
// The engine turns a request into an actor of the requested profile, in the owner layer.
static fopAc_ac_c* g_made = nullptr;
static fopAc_ac_c* materialize(const Request& r, bool creating) {
  fopAc_ac_c* a = nullptr;
  if (r.profile == fpcNm_E_OC_e) {
    auto* b = new daE_OC_c;
    const bool e_oc2 = ((r.p.angle.x >> 8) & 0xff) != 0 && ((r.p.angle.x >> 8) & 0xff) != 0xff;  // d_a_e_oc.cpp create()
    b->mName = e_oc2 ? "E_OC2" : "E_OC";
    b->field_0x560 = b->health = e_oc2 ? 220 : 40;
    a = b;
  } else if (r.profile == fpcNm_E_SF_e) {  // daE_SF_Create
    auto* s = new e_sf_class;
    const u32 prm = r.p.parameters;
    s->mWaitType = u8(prm), s->arg1 = u8(prm >> 8), s->mType = u8((prm >> 24) & 0xF), s->arg3 = u8(prm >> 28);
    if (s->mType > 1) s->mType = 0;
    if (s->arg3 > 1) s->arg3 = 0;
    a = s;
  } else if (r.profile == fpcNm_B_TN_e) {  // daB_TN_c::create
    auto* d = new daB_TN_c;
    const u32 prm = r.p.parameters;
    d->mSwitchNo = u8(prm), d->mType = u8((prm >> 8) & 0xFF), d->mBrkAnmFrame = u8((prm >> 16) & 0xFFFF), d->mType2 = u8((prm >> 24) & 0xFFFFFF);
    if (d->mType != 1) d->mType = 0;
    if (d->mBrkAnmFrame > 4) d->mBrkAnmFrame = 4;
    if (d->mType2 != 1) d->mType2 = 0;
    a = d;
  } else if (r.profile == fpcNm_E_RD_e) {  // daE_RD_Create
    auto* b = new e_rd_class;
    b->arg0 = u8(r.p.parameters), b->weapon_type = u8((r.p.parameters & 0xF00) >> 8);
    if (b->weapon_type == 15) b->weapon_type = 0;
    a = b;
  } else if (r.profile == fpcNm_E_TK_e) {
    a = new e_tk_class;
  } else if (r.profile == fpcNm_E_TK2_e) {
    a = new e_tk2_class;
  } else {
    a = new fopAc_ac_c;
  }
  a->name = r.profile, a->id = r.id;
  g_live.push_back({a, r.owner, creating});
  g_made = a;
  return a;
}
static void engine_create_all(bool finish = true) {
  for (auto& r : g_requests) materialize(r, !finish);
  g_requests.clear();
}
static void delete_layer(layer_class* l) {  // scene teardown: its actors and its pending requests go with it
  for (auto it = g_live.begin(); it != g_live.end();)
    if (it->owner == l) delete it->a, it = g_live.erase(it);
    else ++it;
  for (auto it = g_requests.begin(); it != g_requests.end();)
    if (it->owner == l) it = g_requests.erase(it);
    else ++it;
}
static unsigned draws_of(const fopAc_ac_c* a) {  // actor queue of the play scene + root traversal of root-owned processes
  for (auto& l : g_live)
    if (l.a == a) return (l.owner == &g_play ? 1u : 0u) + (l.owner == &g_root ? 2u : 0u);
  return 0;
}
// Includer-provided names of the production adapter
#define ES_NOINLINE
static s16 es_profile(es::Profile p) {
  return p == es::Profile::E_OC ? fpcNm_E_OC_e : p == es::Profile::E_TK ? fpcNm_E_TK_e : p == es::Profile::E_TK2 ? fpcNm_E_TK2_e : p == es::Profile::E_SF ? fpcNm_E_SF_e
       : p == es::Profile::B_TN ? fpcNm_B_TN_e : p == es::Profile::E_RD ? fpcNm_E_RD_e : fpcNm_E_DN_e;
}
static es::GroundSample g_ground;
static int g_ground_calls = 0;
static es::GroundSample es_sample_ground(daAlink_c* link, const cXyz&) {
  ++g_ground_calls;
  es::GroundSample g = g_ground;
  g.link_y = link->current.pos.y;
  return g;
}
static bool g_framework = false;
static bool es_framework_present() { return g_framework; }
static std::vector<std::string> g_log, g_toasts;
static void es_log(const char* l) { g_log.push_back(l); }
static void es_toast(const char*, const char* body, bool) { g_toasts.push_back(body); }

#include "../src/spawner_adapter.inc"

// ---------------------------------------------------------------- scenarios
static int index_of(const char* label) {
  for (std::size_t i = 0; i < es::kCatalogSize; ++i)
    if (!std::strcmp(es::kCatalog[i].label, label)) return int(i);
  return -1;
}
static void reset() {
  for (auto& l : g_live) delete l.a;
  g_live.clear(), g_requests.clear(), g_log.clear(), g_toasts.clear();
  esr.~EsRuntime();
  new (&esr) EsRuntime();
  g_current = &g_root;
  g_play.deleting = false;
  g_link = &g_link_obj;
  g_link->layer_tag.layer = &g_play;
  g_link->current.pos = cXyz(100, 50, -20);
  g_link->shape_angle.y = 0x4000;
  g_next_stage = g_event = g_pause = false;
  g_service_result = MOD_OK, g_service_throws = false;
  g_ground = es::GroundSample{};
  g_ground.found = true, g_ground.ground_y = 50, g_ground.normal_y = 1;
  g_framework = false;
}
static bool toasted(const char* part) {
  for (auto& t : g_toasts)
    if (t.find(part) != std::string::npos) return true;
  return false;
}
static bool logged(const char* part) {
  for (auto& t : g_log)
    if (t.find(part) != std::string::npos) return true;
  return false;
}

static void lab_ownership() {
  // What a request on the current (root) layer would do: the bug Dawnlight fixed. Shown with the engine model itself.
  reset();
  ActorId bad = 0;
  ActorSpawnParams p{};
  CHECK(create_actor(mod_ctx, fpcNm_E_DN_e, &p, &bad) == MOD_OK && g_requests.back().owner == &g_root);
  engine_create_all();
  fopAc_ac_c* root_owned = g_made;
  CHECK(draws_of(root_owned) == 2);  // drawn by the play queue AND the root traversal
  delete_layer(&g_play);
  CHECK(draws_of(root_owned) == 2);  // and it survives its scene
  // The production helper: Link's layer during the call, the caller's layer back afterwards.
  reset();
  ActorId id = 0;
  CHECK(es_create_in_link_layer(g_link, fpcNm_E_DN_e, p, id) == MOD_OK);
  CHECK(g_requests.size() == 1 && g_requests[0].owner == &g_play && g_current == &g_root && esr.layer_restores == 1);
  engine_create_all();
  CHECK(draws_of(g_made) == 1);
  delete_layer(&g_play);
  fopAc_ac_c* a = nullptr;
  CHECK(fopAcM_SearchByID(id, &a) == 0);  // gone with its scene
  // Restored on failure and on exception.
  reset();
  g_service_result = MOD_ERROR;
  CHECK(es_create_in_link_layer(g_link, fpcNm_E_DN_e, p, id) == MOD_ERROR && g_current == &g_root);
  reset();
  g_service_throws = true;
  bool thrown = false;
  try {
    (void)es_create_in_link_layer(g_link, fpcNm_E_DN_e, p, id);
  } catch (const std::exception&) {
    thrown = true;
  }
  CHECK(thrown && g_current == &g_root && g_requests.empty());
  // Never on a root, missing or dying layer, never during a stage change; nothing is requested and nothing is changed.
  for (int k = 0; k < 4; ++k) {
    reset();
    if (k == 0) g_link->layer_tag.layer = &g_root;
    if (k == 1) g_link->layer_tag.layer = nullptr;
    if (k == 2) g_play.deleting = true;
    if (k == 3) g_next_stage = true;
    CHECK(es_create_in_link_layer(g_link, fpcNm_E_DN_e, p, id) == MOD_UNAVAILABLE && g_requests.empty() && g_current == &g_root);
  }
  CHECK(es_create_in_link_layer(nullptr, fpcNm_E_DN_e, p, id) == MOD_UNAVAILABLE);
}

static void lab_press_to_actor() {
  reset();
  es_press(index_of("Lizalfos"));
  CHECK(g_requests.empty());  // the UI never touches the engine
  es_update();
  CHECK(g_requests.size() == 1 && g_requests[0].owner == &g_play && g_current == &g_root);
  const Request r = g_requests[0];
  CHECK(r.profile == fpcNm_E_DN_e && r.p.parameters == 0xff0000ffu && r.p.room_num == 3);
  CHECK(std::fabs(r.p.position.x - (100.0f + 300.0f)) < 0.5f && std::fabs(r.p.position.z - (-20.0f)) < 0.5f && r.p.position.y == 50.0f);  // 300 in front, on the ground
  CHECK(r.p.angle.y == static_cast<s16>(0x4000 + 0x8000));  // facing Link
  CHECK(toasted("Spawn request submitted") && !toasted("Enemy spawned"));
  engine_create_all(false);  // in the actor queue, still creating
  es_update();
  CHECK(!toasted("Enemy spawned"));
  for (auto& l : g_live) l.creating = false;
  es_update();
  CHECK(toasted("Enemy spawned: Lizalfos") && logged("event=ACTOR_APPEARED"));
  delete_layer(&g_play);
  es_update();
  CHECK(logged("event=ACTOR_GONE") && esr.sp.live() == 0);
  // Flying enemies are lifted; a fallback distance is used when the first point is refused.
  reset();
  es_press(index_of("Keese"));
  es_update();
  CHECK(g_requests.size() == 1 && g_requests[0].p.position.y == 250.0f && g_requests[0].p.parameters == 0xffff0f01u);
}

static void lab_refusals() {
  reset();
  g_ground.water = true, g_ground.water_y = 90;
  es_press(index_of("Lizalfos"));
  es_update();
  CHECK(g_requests.empty() && toasted("no safe spawn location") && g_ground_calls >= 3);
  reset();
  g_ground.found = false;
  es_press(index_of("Lizalfos"));
  es_update();
  CHECK(g_requests.empty() && logged("why=NO_GROUND"));
  // Unsafe moments: the press waits, then expires; nothing is created meanwhile.
  reset();
  g_event = true;
  es_press(index_of("Lizalfos"));
  for (std::uint32_t k = 0; k <= es::policy::kPendingTicks + 1; ++k) es_update();
  CHECK(g_requests.empty() && toasted("not in a safe state") && !esr.sp.pending());
  reset();
  g_pause = true;
  es_press(index_of("Lizalfos"));
  es_update();
  CHECK(g_requests.empty() && esr.sp.pending());
  g_pause = false;
  es_update();
  CHECK(g_requests.size() == 1);
  reset();
  g_link = nullptr;
  es_press(index_of("Lizalfos"));
  es_update();
  CHECK(g_requests.empty() && esr.sp.pending());
  // Black: a refusal with its reason, whatever is loaded. No request, ever.
  for (int fw = 0; fw <= 1; ++fw) {
    reset();
    g_framework = fw != 0;
    es_update();
    es_press(index_of("Bokoblin Black (Expansion): integration unavailable"));
    es_update();
    CHECK(g_requests.empty() && toasted("Bokoblin Black integration is unavailable"));
  }
  // Out of range selections from a damaged config value.
  reset();
  es_press(-3);
  es_press(9999);
  es_update();
  CHECK(g_requests.empty() && g_toasts.size() == 2);
}

static void lab_expansion_observation() {
  // Expansion loaded: the framework service is present, and Expansion's own classification writes 220 / 330 at the first Execute.
  for (int red = 1; red >= 0; --red) {
    for (int works = 1; works >= 0; --works) {
      reset();
      g_framework = true;
      es_update();
      CHECK(esr.sp.expansion == es::Expansion::Possible);
      es_press(index_of(red ? "Bokoblin Red (Expansion)" : "Bokoblin Blue (Expansion)"));
      es_update();
      CHECK(g_requests.size() == 1 && g_requests[0].profile == fpcNm_E_OC_e && ((g_requests[0].p.angle.x >> 8) & 0xff) == (red ? 1 : 0));
      engine_create_all();
      auto* b = static_cast<daE_OC_c*>(g_made);
      CHECK(!std::strcmp(b->mName, red ? "E_OC2" : "E_OC") && b->health == (red ? 220 : 40));
      if (works) b->health = red ? 330 : 220;  // what Expansion 0.17.0 writes for a native E_OC2 / E_OC (variant_policy.hpp)
      for (std::uint32_t k = 0; k < es::policy::kVerifyTicks + 3; ++k) es_update();
      if (works) {
        CHECK(esr.sp.expansion == es::Expansion::Confirmed && toasted(red ? "classified the spawned enemy as RED" : "classified the spawned enemy as BLUE") && b->health == (red ? 330 : 220));
      } else {
        CHECK(esr.sp.expansion == es::Expansion::Refuted && toasted("did not classify the spawned enemy") && b->health == (red ? 220 : 40));  // never written by the spawner
      }
    }
  }
  // Without the framework: refused, nothing created.
  reset();
  es_update();
  es_press(index_of("Bokoblin Blue (Expansion)"));
  es_update();
  CHECK(g_requests.empty() && toasted("Bokoblin Expansion is not loaded"));
  // Native Bokoblin entries stay available and honest.
  reset();
  es_press(index_of("Bokoblin (E_OC, native)"));
  es_update();
  CHECK(g_requests.size() == 1 && ((g_requests[0].p.angle.x >> 8) & 0xff) == 0);
}

static void lab_adaptations() {
  reset();
  es_press(index_of("Water Toadpoli"));
  es_update();
  engine_create_all();
  auto* tk = static_cast<e_tk_class*>(g_made);
  // An actor of the same profile that this mod did not create: never written.
  e_tk_class foreign;
  foreign.name = fpcNm_E_TK_e, foreign.id = 9999, foreign.mExecuteState = 1;
  g_live.push_back({&foreign, &g_play, false});
  for (int k = 0; k < 40; ++k) {
    if (foreign.mExecuteState > 0) --foreign.mExecuteState;
    if (tk->mExecuteState > 0) --tk->mExecuteState;  // the native countdown of its Execute
    es_update();
  }
  CHECK(tk->mExecuteState == 2 && foreign.mExecuteState == 0 && esr.adapt_writes > 0);
  g_live.pop_back();
  // An id of ours that now names another profile: nothing is written.
  reset();
  es_press(index_of("Fire Toadpoli"));
  es_update();
  g_requests[0].profile = fpcNm_E_DN_e;
  engine_create_all();
  es_update();
  CHECK(esr.adapt_writes == 0);
}

static unsigned count_logged(const char* part) {
  unsigned n = 0;
  for (auto& t : g_log) n += t.find(part) != std::string::npos;
  return n;
}
// 0.1.2: the appended variants reach the engine with their native parameters, and the telemetry reads back what the actor decoded.
static void lab_variants_and_telemetry() {
  struct V { const char* label; s16 profile; u32 parameters; s16 angle_z; const char* selector; } vs[] = {
      {"Stalfos", fpcNm_E_SF_e, 0x0000ff00u, 0xff, "observed=mType:0,arg3:0 match=YES"},
      {"Stalfos (Alternate Attack)", fpcNm_E_SF_e, 0x0100ff00u, 0xff, "observed=mType:1,arg3:0 match=YES"},
      {"Stalfos (Breakable Shield)", fpcNm_E_SF_e, 0x1000ff00u, 0xff, "observed=mType:0,arg3:1 match=YES"},
      {"Darknut", fpcNm_B_TN_e, 0x000001ffu, 0, "observed=mType:1,mType2:0 match=YES"},
      {"Darknut (Sword)", fpcNm_B_TN_e, 0x010001ffu, 0, "observed=mType:1,mType2:1 match=YES"},
      {"Bulblin", fpcNm_E_RD_e, 0xff000100u, 0, "observed=weapon_type:1,unused:0 match=YES"},
      {"Bulblin (Bow)", fpcNm_E_RD_e, 0xff000200u, 0, "observed=weapon_type:2,unused:0 match=YES"},
      {"Bulblin (Fire Bow)", fpcNm_E_RD_e, 0xff000300u, 0, "observed=weapon_type:3,unused:0 match=YES"},
  };
  for (const V& v : vs) {
    reset();
    es_press(index_of(v.label));
    es_update();
    CHECK(g_requests.size() == 1 && g_requests[0].profile == v.profile && g_requests[0].p.parameters == v.parameters && g_requests[0].p.angle.z == v.angle_z);
    CHECK(g_requests[0].p.angle.y == static_cast<s16>(0x4000 + 0x8000) && g_requests[0].owner == &g_play && g_current == &g_root);
    engine_create_all(false);
    es_update();
    CHECK(!logged("event=NATIVE_SELECTOR"));  // nothing is read while the create still runs
    for (auto& l : g_live) l.creating = false;
    es_update();
    CHECK(logged("event=ACTOR_APPEARED") && logged("event=NATIVE_SELECTOR") && logged(v.selector) && count_logged("event=NATIVE_SELECTOR") == 1);
    for (int k = 0; k < 5; ++k) es_update();
    CHECK(count_logged("event=NATIVE_SELECTOR") == 1 && !toasted("NATIVE") && !toasted("mType"));  // log only, once
    CHECK(esr.sp.c.selector_match == 1 && esr.sp.c.selector_mismatch == 0);
  }
  // Stalfos (Alternate Attack): when its native attack runs, the log names ACTION_ATTACK_0 and BCK_SF_ATTACK02. Never written by the spawner.
  reset();
  es_press(index_of("Stalfos (Alternate Attack)"));
  es_update();
  engine_create_all();
  auto* sf = static_cast<e_sf_class*>(g_made);
  es_update();
  CHECK(sf->mType == 1 && !logged("NATIVE_ATTACK_OBSERVED"));
  sf->mAction = 4, sf->mAnm = 5;  // e_sf_attack_0 running (set by the scenario: the model has no AI)
  for (int k = 0; k < 4; ++k) es_update();
  CHECK(count_logged("event=NATIVE_ATTACK_OBSERVED") == 1 && logged("action=ACTION_ATTACK_0(4) anm=BCK_SF_ATTACK02(5) expected_bck=5 mType=1 match=YES"));
  CHECK(sf->mAction == 4 && sf->mAnm == 5 && sf->mType == 1 && sf->arg3 == 0 && esr.sp.c.attack_alt == 1);
  sf->mAction = 3;  // back to fight_run, then the same attack again: still one line
  es_update();
  sf->mAction = 4;
  es_update();
  CHECK(count_logged("event=NATIVE_ATTACK_OBSERVED") == 1);
  // An actor that decoded something else than the catalog asked for (a host or another mod changed it): reported as a mismatch, with both values.
  reset();
  es_press(index_of("Stalfos (Alternate Attack)"));
  es_update();
  engine_create_all(false);
  static_cast<e_sf_class*>(g_made)->mType = 0;
  for (auto& l : g_live) l.creating = false;
  es_update();
  CHECK(logged("expected=mType:1,arg3:0 observed=mType:0,arg3:0 match=NO") && !logged("match=YES") && esr.sp.c.selector_mismatch == 1 && esr.sp.c.selector_match == 0);
  static_cast<e_sf_class*>(g_made)->mAction = 5, static_cast<e_sf_class*>(g_made)->mAnm = 4;  // the base attack running on an entry that asked for mType 1
  es_update();
  CHECK(logged("action=ACTION_ATTACK(5) anm=BCK_SF_ATTACK01(4) expected_bck=4 mType=1 match=NO") && esr.sp.c.attack_unexpected == 1);
  // A shield that breaks later (arg3 -> 0xFF) does not re-report the selector.
  reset();
  es_press(index_of("Stalfos (Breakable Shield)"));
  es_update();
  engine_create_all();
  es_update();
  static_cast<e_sf_class*>(g_made)->arg3 = 0xFF;
  for (int k = 0; k < 3; ++k) es_update();
  CHECK(count_logged("event=NATIVE_SELECTOR") == 1 && esr.sp.c.selector_mismatch == 0);
  // The base Stalfos: ACTION_ATTACK / BCK_SF_ATTACK01.
  reset();
  es_press(index_of("Stalfos"));
  es_update();
  engine_create_all();
  es_update();
  static_cast<e_sf_class*>(g_made)->mAction = 5, static_cast<e_sf_class*>(g_made)->mAnm = 4;
  es_update();
  CHECK(logged("action=ACTION_ATTACK(5) anm=BCK_SF_ATTACK01(4) expected_bck=4 mType=0 match=YES"));
  // An id of ours that names another profile: the fields of that other actor are never read as Stalfos fields.
  reset();
  es_press(index_of("Stalfos (Alternate Attack)"));
  es_update();
  g_requests[0].profile = fpcNm_E_DN_e;
  engine_create_all();
  for (int k = 0; k < 3; ++k) es_update();
  CHECK(logged("event=ACTOR_APPEARED") && !logged("event=NATIVE_SELECTOR") && !logged("NATIVE_ATTACK_OBSERVED"));
  // The 12 limit counts the new entries like any other.
  reset();
  for (unsigned i = 0; i < es::policy::kMaxLive; ++i) {
    es_press(index_of(i % 2 ? "Darknut (Sword)" : "Stalfos (Alternate Attack)"));
    es_update();
  }
  es_press(index_of("Bulblin (Bow)"));
  es_update();
  CHECK(g_requests.size() == es::policy::kMaxLive && toasted("Maximum of 12 active spawned enemies reached"));
}

static void lab_limit_and_shutdown() {
  reset();
  for (unsigned i = 0; i < es::policy::kMaxLive; ++i) {
    es_press(index_of("Rat"));
    es_update();
  }
  CHECK(g_requests.size() == es::policy::kMaxLive);
  es_press(index_of("Rat"));
  es_update();
  CHECK(g_requests.size() == es::policy::kMaxLive && toasted("Maximum of 12 active spawned enemies reached"));
  engine_create_all();
  es_update();
  const std::size_t live = g_live.size();
  esr.sp.forget_all();
  es_update();
  CHECK(g_live.size() == live && esr.sp.live() == 0);  // forgetting deletes nothing: the actors belong to their scene
}

int main() {
  lab_ownership();
  lab_press_to_actor();
  lab_refusals();
  lab_expansion_observation();
  lab_adaptations();
  lab_variants_and_telemetry();
  lab_limit_and_shutdown();
  reset();
  std::printf("ES_ADAPTER_LAB version=%s checks=%llu failures=0 RESULT=LAB_PASS scope=PRODUCTION_ADAPTER_OVER_ENGINE_LAYER_MODEL runtime=HUMAN_RUNTIME_PENDING\n", es::kVersion, g_checks);
  return 0;
}
