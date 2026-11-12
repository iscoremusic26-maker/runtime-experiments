// Enemy Spawner (Standalone) 0.1.2: the part that touches the engine. Included once by mod.cpp, and by tests/adapter_lab.cpp over a model of
// the engine's layer and creation rules. The includer provides: the SDK names used below, es_profile(), es_sample_ground(), es_log(), es_toast().
//
// Scene ownership is Dawnlight's rule (BeZide93, CC0, b5e9046 src/enemy_spawner.cpp create_test_actor_in_player_layer, user-confirmed
// in Dawnlight): ActorService::create_actor -> fopAcM_create -> fpcM_Create records fpcLy_CurrentLayer() in the asynchronous request.
// room_num does not choose the owner. A request made on the root layer gives a root-owned enemy: drawn twice (actor queue + root traversal)
// and alive after its scene is deleted. So Link's own layer is current during the call and the caller's layer comes back on every exit.
//
// Native writes of this file (all on actors this mod created, all through the named writers below):
//  es_native_layer      fpcLy_SetCurrentLayer, set and restored around one create_actor call
//  es_native_keep_ground  e_tk mExecuteState / e_tk2 mActionTimer[3], each frame before the actor's Execute (catalog Adapt)
// Everything else is read only. 0.1.2 adds READS only (es_probe): e_sf_class mType/arg3/mAction/mAnm, daB_TN_c mType/mType2, e_rd_class weapon_type,
// each by name through the SDK headers and only after fopAcM_GetName says the actor is of that profile.
struct EsRuntime {
  es::Spawner sp;
  std::uint64_t tick = 0, framework_checked = ~0ull;
  bool ui = false;
  unsigned lines = 0;
  std::uint64_t dropped = 0, adapt_writes = 0, layer_restores = 0;
} esr;

ES_NOINLINE void es_native_layer(layer_class* layer) noexcept { fpcLy_SetCurrentLayer(layer); }

// Dawnlight's helper, adapted: same checks, same guarantee (the previous layer comes back on success, failure or exception).
ModResult es_create_in_link_layer(daAlink_c* link, s16 profile, const ActorSpawnParams& params, ActorId& id) {  // not noexcept: an exception still restores the layer
  if (link == nullptr || dComIfGp_isEnableNextStage()) return MOD_UNAVAILABLE;
  layer_class* layer = link->layer_tag.layer;
  if (layer == nullptr || layer == fpcLy_RootLayer() || fpcLy_IsDeletingMesg(layer)) return MOD_UNAVAILABLE;
  struct Restore {
    layer_class* previous;
    ~Restore() {
      es_native_layer(previous);
      ++esr.layer_restores;
    }
  } restore{fpcLy_CurrentLayer()};
  es_native_layer(layer);
  return svc_actor->create_actor(mod_ctx, profile, &params, &id);
}

ES_NOINLINE void es_native_keep_ground(fopAc_ac_c* a, es::Adapt how) noexcept {
  if (how == es::Adapt::ToadpoliWater) static_cast<e_tk_class*>(a)->mExecuteState = 2;
  else if (how == es::Adapt::ToadpoliLava) static_cast<e_tk2_class*>(a)->mActionTimer[3] = 2;
}

es::Scene es_scene() noexcept {
  es::Scene s;
  s.actor_service = svc_actor != nullptr && svc_actor->create_actor != nullptr;
  daAlink_c* link = daAlink_getAlinkActorClass();
  s.link = link != nullptr;
  if (link) {
    layer_class* layer = link->layer_tag.layer;
    s.link_layer = layer != nullptr && layer != fpcLy_RootLayer() && !fpcLy_IsDeletingMesg(layer);
  }
  s.next_stage = dComIfGp_isEnableNextStage() != 0;
  s.event = dComIfGp_event_runCheck() != 0;
  s.paused = dComIfGp_isPauseFlag() != 0;
  return s;
}

// The point in front of Link at distance d, with its ground. Flying enemies are lifted after the check.
cXyz es_point(daAlink_c* link, float d) noexcept {
  const s16 facing = link->shape_angle.y;
  return cXyz(link->current.pos.x + cM_ssin(facing) * d, link->current.pos.y, link->current.pos.z + cM_scos(facing) * d);
}

void es_spawn_now(std::uint64_t now) noexcept {
  daAlink_c* link = daAlink_getAlinkActorClass();
  const std::uint16_t index = esr.sp.pending_entry();
  const es::Entry& e = es::kCatalog[index];
  es::Ground last = es::Ground::NoGround;
  for (float d : es::policy::kDistances) {
    cXyz pos = es_point(link, d);
    const es::GroundSample g = es_sample_ground(link, pos);
    last = es::judge_ground(g);
    if (last != es::Ground::Ok) continue;
    pos.y = g.ground_y + (e.flying ? es::policy::kFlyingLift : 0.0f);
    const s16 facing = link->shape_angle.y;
    ActorSpawnParams p{};
    p.parameters = e.parameters;
    p.argument = e.argument;
    p.room_num = static_cast<std::int8_t>(fopAcM_GetRoomNo(link));
    p.position.x = pos.x, p.position.y = pos.y, p.position.z = pos.z;
    p.angle.x = e.angle_x, p.angle.y = static_cast<s16>(facing + 0x8000), p.angle.z = e.angle_z;  // facing Link
    p.scale.x = p.scale.y = p.scale.z = 1.0f;
    p.create_function = nullptr;
    ActorId id = 0xFFFFFFFFu;
    const ModResult r = es_create_in_link_layer(link, es_profile(e.profile), p, id);
    esr.sp.created(r == MOD_OK, id, now);
    return;
  }
  esr.sp.reject(last, now);
}

es::Probe es_probe(std::uint32_t id) noexcept {
  es::Probe p;
  fopAc_ac_c* a = nullptr;
  p.found = fopAcM_SearchByID(id, &a) != 0 && a != nullptr;
  p.creating = fpcM_IsCreating(id) != 0;
  if (p.found && !p.creating && fopAcM_GetName(a) == fpcNm_E_OC_e) {
    const auto* b = static_cast<const daE_OC_c*>(a);
    const char* n = b->mName;
    p.bokoblin = n != nullptr;
    p.e_oc2 = n && n[0] == 'E' && n[1] == '_' && n[2] == 'O' && n[3] == 'C' && n[4] == '2' && n[5] == 0;
    p.field_0x560 = b->field_0x560, p.health = b->health;
  }
  // 0.1.2 telemetry: the selector the actor itself decoded in its create(), and the Stalfos action / animation running now. Read only.
  if (p.found && !p.creating) {
    const s16 profile = fopAcM_GetName(a);
    if (profile == fpcNm_E_SF_e) {  // e_sf_class has its fopEn_enemy_c first; the native code casts the same way ((e_sf_class*)a_this)
      const auto* s = reinterpret_cast<const e_sf_class*>(a);
      p.selector_read = true, p.sel_a = s->mType, p.sel_b = s->arg3;
      p.stalfos = true, p.sf_action = s->mAction, p.sf_anm = s->mAnm;
    } else if (profile == fpcNm_B_TN_e) {
      const auto* d = static_cast<const daB_TN_c*>(a);
      p.selector_read = true, p.sel_a = d->mType, p.sel_b = d->mType2;
    } else if (profile == fpcNm_E_RD_e) {  // e_rd_class has its fopEn_enemy_c first, like e_sf_class
      p.selector_read = true, p.sel_a = reinterpret_cast<const e_rd_class*>(a)->weapon_type, p.sel_b = 0;
    }
  }
  return p;
}

void es_adapt(const es::Tracked& x) noexcept {
  const es::Adapt how = es::kCatalog[x.entry].adapt;
  if (how == es::Adapt::None) return;
  fopAc_ac_c* a = nullptr;
  if (fopAcM_SearchByID(x.id, &a) == 0 || a == nullptr || fpcM_IsCreating(x.id)) return;
  const s16 want = how == es::Adapt::ToadpoliWater ? fpcNm_E_TK_e : fpcNm_E_TK2_e;
  if (fopAcM_GetName(a) != want) return;  // the id is ours and the actor is the one we asked for, or nothing is written
  es_native_keep_ground(a, how);
  ++esr.adapt_writes;
}

// 0.1.2: the two telemetry events are log lines only (no toast): evidence for the human test, never a claim that the game was observed by CI.
void es_report_native(const es::Event& ev, const char* label) noexcept {
  const es::Profile prof = ev.entry < es::kCatalogSize ? es::kCatalog[ev.entry].profile : es::Profile::Count;
  const es::Selector want = ev.entry < es::kCatalogSize ? es::decode_selector(prof, es::kCatalog[ev.entry].parameters) : es::Selector{};
  const char* fa = prof == es::Profile::E_SF ? "mType" : prof == es::Profile::B_TN ? "mType" : "weapon_type";
  const char* fb = prof == es::Profile::E_SF ? "arg3" : prof == es::Profile::B_TN ? "mType2" : "unused";
  char line[320];
  if (ev.kind == es::Ev::NativeSelector) {
    std::snprintf(line, sizeof(line), "ENEMY_SPAWNER event=NATIVE_SELECTOR version=%s entry=%u label=\"%s\" actor_id=%u expected=%s:%u,%s:%u observed=%s:%u,%s:%u match=%s tick=%llu", es::kVersion,
                  unsigned(ev.entry), label, ev.id, fa, unsigned(want.a), fb, unsigned(want.b), fa, unsigned(ev.a), fb, unsigned(ev.b), ev.why ? "YES" : "NO",
                  static_cast<unsigned long long>(ev.tick));
  } else {
    const char* action = ev.action == es::stalfos::kActionAttack0 ? "ACTION_ATTACK_0" : ev.action == es::stalfos::kActionAttack ? "ACTION_ATTACK" : "?";
    const char* anm = ev.anm == es::stalfos::kBckAttack02 ? "BCK_SF_ATTACK02" : ev.anm == es::stalfos::kBckAttack01 ? "BCK_SF_ATTACK01" : "OTHER";
    std::snprintf(line, sizeof(line), "ENEMY_SPAWNER event=NATIVE_ATTACK_OBSERVED version=%s entry=%u label=\"%s\" actor_id=%u action=%s(%d) anm=%s(%d) expected_bck=%d mType=%u match=%s tick=%llu",
                  es::kVersion, unsigned(ev.entry), label, ev.id, action, int(ev.action), anm, ev.anm, es::stalfos::expected_bck(ev.action), unsigned(ev.a), ev.why ? "YES" : "NO",
                  static_cast<unsigned long long>(ev.tick));
  }
  es_log(line);
}

void es_report(const es::Event& ev) noexcept {
  const char* label = ev.entry < es::kCatalogSize ? es::kCatalog[ev.entry].label : "?";
  if (ev.kind == es::Ev::NativeSelector || ev.kind == es::Ev::NativeAttack) {
    es_report_native(ev, label);
    return;
  }
  const char* why = ev.kind == es::Ev::Expired ? es::name(es::Wait(ev.why)) : ev.kind == es::Ev::Rejected ? es::name(es::Ground(ev.why))
                    : ev.kind == es::Ev::Classified || ev.kind == es::Ev::NotClassified ? (ev.why == std::uint8_t(es::Variant::Blue) ? "BLUE" : ev.why == std::uint8_t(es::Variant::Red) ? "RED" : ev.why == std::uint8_t(es::Variant::Native) ? "NATIVE_HP_UNCHANGED" : "UNEXPECTED_VALUES")
                    : ev.kind == es::Ev::CreateFailed ? (ev.why ? "ENDED_WITHOUT_ACTOR" : "SERVICE_REFUSED") : "-";
  char line[256];
  std::snprintf(line, sizeof(line), "ENEMY_SPAWNER event=%s version=%s entry=%u label=\"%s\" actor_id=%u why=%s expansion=%s tick=%llu", es::name(ev.kind), es::kVersion, unsigned(ev.entry), label, ev.id, why,
                es::name(esr.sp.expansion), static_cast<unsigned long long>(ev.tick));
  es_log(line);
  char body[200];
  switch (ev.kind) {
    case es::Ev::Created: std::snprintf(body, sizeof(body), "Spawn request submitted: %s.", label); es_toast("Enemy Spawner", body, false); break;
    case es::Ev::Appeared: std::snprintf(body, sizeof(body), "Enemy spawned: %s.", label); es_toast("Enemy Spawner", body, false); break;
    case es::Ev::Expired: std::snprintf(body, sizeof(body), "%s was not spawned: the game was not in a safe state (%s).", label, why); es_toast("Enemy Spawner", body, true); break;
    case es::Ev::Rejected: std::snprintf(body, sizeof(body), "%s was not spawned: no safe spawn location in front of Link (%s).", label, why); es_toast("Enemy Spawner", body, true); break;
    case es::Ev::CreateFailed: std::snprintf(body, sizeof(body), "%s was not spawned: the game did not create the enemy.", label); es_toast("Enemy Spawner", body, true); break;
    case es::Ev::CreateTimeout: std::snprintf(body, sizeof(body), "%s was not spawned: creation did not finish in time.", label); es_toast("Enemy Spawner", body, true); break;
    case es::Ev::Classified: std::snprintf(body, sizeof(body), "Bokoblin Expansion classified the spawned enemy as %s.", why); es_toast("Enemy Spawner", body, false); break;
    case es::Ev::NotClassified: std::snprintf(body, sizeof(body), "Bokoblin Expansion did not classify the spawned enemy (%s): it is a native Bokoblin.", why); es_toast("Enemy Spawner", body, true); break;
    default: break;
  }
}

void es_update() noexcept {
  const std::uint64_t now = ++esr.tick;
  if (esr.framework_checked == ~0ull || now - esr.framework_checked >= 30) {  // presence of the framework Expansion requires; never a call into it
    esr.framework_checked = now;
    esr.sp.set_framework_present(es_framework_present());
  }
  if (esr.sp.pending() && esr.sp.ready(es_scene(), now) == es::Wait::Ready) es_spawn_now(now);
  for (unsigned i = 0; i < es::policy::kMaxLive; ++i) {
    if (esr.sp.t[i].life == es::Life::Free) continue;
    esr.sp.observe(i, es_probe(esr.sp.t[i].id), now);
    if (esr.sp.t[i].life == es::Life::Alive) es_adapt(esr.sp.t[i]);
  }
  es::Event ev[es::Spawner::kEvents];
  const unsigned n = esr.sp.drain(ev, es::Spawner::kEvents);
  for (unsigned i = 0; i < n; ++i) es_report(ev[i]);
}

void es_press(std::int64_t index) noexcept {
  const es::Press r = esr.sp.press(index, esr.tick);
  char line[200];
  std::snprintf(line, sizeof(line), "ENEMY_SPAWNER event=PRESS version=%s index=%lld result=%s expansion=%s tick=%llu", es::kVersion, static_cast<long long>(index), es::name(r), es::name(esr.sp.expansion),
                static_cast<unsigned long long>(esr.tick));
  es_log(line);
  switch (r) {
    case es::Press::Accepted: break;
    case es::Press::BlackUnavailable: es_toast("Enemy Spawner", "Bokoblin Black integration is unavailable: Bokoblin Expansion 0.17.0 has no API to register a Black at runtime.", true); break;
    case es::Press::ExpansionAbsent: es_toast("Enemy Spawner", "Bokoblin Expansion is not loaded. Use the native Bokoblin entries.", true); break;
    case es::Press::ExpansionRefuted: es_toast("Enemy Spawner", "Bokoblin Expansion did not classify the last spawned Bokoblin: Expansion entries are disabled for this session.", true); break;
    case es::Press::Busy: es_toast("Enemy Spawner", "A spawn request is already pending.", true); break;
    case es::Press::Full: {
      char full[96];
      std::snprintf(full, sizeof(full), "Maximum of %u active spawned enemies reached.", es::policy::kMaxLive);
      es_toast("Enemy Spawner", full, true);
      break;
    }
    default: es_toast("Enemy Spawner", "Invalid enemy selection.", true); break;
  }
}
