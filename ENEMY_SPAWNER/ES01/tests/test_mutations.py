"""Enemy Spawner 0.1.2: executed mutants of the PRODUCTION core, adapter and Mods panel against tests/core_lab.cpp, tests/adapter_lab.cpp
and tests/panel_lab.cpp (the last one compiled against the real SDK UI header: env ES_SDK_INCLUDE = <dusklight>/sdk/include).
Core/adapter mutants run core_lab + adapter_lab; panel mutants run panel_lab. A mutant counts as detected only when a lab reports ES_LAB_FAIL.
Compile errors and timeouts are failures, never credited. The positive control runs all three labs first."""
from pathlib import Path
import concurrent.futures, json, os, shutil, subprocess, sys, tempfile
root = Path(__file__).resolve().parents[1]
C, A, K, U = 'src/spawner_core.hpp', 'src/spawner_adapter.inc', 'src/catalog.hpp', 'src/ui_panel.inc'
SDK = os.environ.get('ES_SDK_INCLUDE', '')
CORE, PANEL, ALL = ('core_lab', 'adapter_lab'), ('panel_lab',), ('core_lab', 'adapter_lab', 'panel_lab')
cases = [
 ('black_creatable', C, '    if (e.route == Route::BlackUnavailable) return Press::BlackUnavailable;  // never a Red with a black label\n', ''),
 ('black_as_red', K, 'Route::BlackUnavailable, Adapt::None},', 'Route::ExpansionRed, Adapt::None},'),
 ('expansion_absent_allowed', C, 'route == Route::ExpansionRed) && expansion == Expansion::Absent) return Press::ExpansionAbsent;', 'route == Route::ExpansionRed) && false) return Press::ExpansionAbsent;'),
 ('refutation_ignored', C, 'route == Route::ExpansionRed) && expansion == Expansion::Refuted) return Press::ExpansionRefuted;', 'route == Route::ExpansionRed) && false) return Press::ExpansionRefuted;'),
 ('double_click_twice', C, '    if (pending_) return Press::Busy;\n', ''),
 ('no_limit', C, '    if (live() >= policy::kMaxLive) return Press::Full;\n', ''),
 ('index_unchecked', C, 'if (index < 0 || static_cast<std::uint64_t>(index) >= kCatalogSize) return Press::InvalidIndex;', 'if (index < 0) return Press::InvalidIndex;'),
 ('pending_never_expires', C, 'if (w != Wait::Ready && now - pending_since_ > policy::kPendingTicks) {', 'if (false) {'),
 ('paused_is_ready', C, '  if (s.paused) return Wait::Paused;\n', ''),
 ('event_is_ready', C, '  if (s.event) return Wait::Event;\n', ''),
 ('transition_is_ready', C, '  if (s.next_stage) return Wait::Transition;\n', ''),
 ('water_accepted', C, '  if (s.water && s.water_y > s.ground_y) return Ground::Water;\n', ''),
 ('wall_ignored', C, '  if (s.blocked) return Ground::Blocked;\n', ''),
 ('edge_ignored', C, '  if (s.ground_y < s.link_y - policy::kMaxStep) return Ground::TooLow;\n', ''),
 ('visible_while_creating', C, '      if (p.found && !p.creating) {', '      if (p.found) {'),
 ('gone_never_forgotten', C, '      if (!p.found) {  // death', '      if (false) {  // death'),
 ('creation_never_times_out', C, '} else if (now - x.since > policy::kCreateTicks) {', '} else if (false) {'),
 ('reused_id_twice', C, '        ++c.id_reused;\n        emit(Ev::IdReused, x.entry, id, 0, now);\n        x = Tracked{};', '        ++c.id_reused;'),
 ('any_hp_is_red', C, 'return health == 330 ? Variant::Red :', 'return health >= 220 ? Variant::Red :'),
 ('creation_value_ignored', C, '  if (e_oc2 && field_0x560 == 220) return', '  if (e_oc2) return'),
 ('native_refutes', C, 'if ((wanted_blue || wanted_red) && expansion != Expansion::Confirmed) expansion = Expansion::Refuted;', 'if (expansion != Expansion::Confirmed) expansion = Expansion::Refuted;'),
 ('layer_not_restored', A, '      es_native_layer(previous);\n', ''),
 ('root_layer_accepted', A, ' || layer == fpcLy_RootLayer() || fpcLy_IsDeletingMesg(layer)) return MOD_UNAVAILABLE;\n  struct', ' || fpcLy_IsDeletingMesg(layer)) return MOD_UNAVAILABLE;\n  struct'),
 ('created_in_caller_layer', A, '  es_native_layer(layer);\n  return svc_actor', '  return svc_actor'),
 ('not_facing_link', A, 'p.angle.y = static_cast<s16>(facing + 0x8000)', 'p.angle.y = facing'),
 ('flying_not_lifted', A, '(e.flying ? es::policy::kFlyingLift : 0.0f)', '0.0f'),
 ('wrong_room', A, 'p.room_num = static_cast<std::int8_t>(fopAcM_GetRoomNo(link));', 'p.room_num = -1;'),
 ('e_oc2_misread', A, "n[3] == 'C' && n[4] == '2' && n[5] == 0;", "n[3] == 'C';"),
 ('adapt_foreign_profile', A, '  if (fopAcM_GetName(a) != want) return;', ''),
 ('adapt_lost', A, '  es_native_keep_ground(a, how);\n', ''),
 ('ui_creates_directly', A, '  const es::Press r = esr.sp.press(index, esr.tick);', '  const es::Press r = esr.sp.press(index, esr.tick);\n  if (r == es::Press::Accepted) es_spawn_now(esr.tick);'),
 ('appeared_announced_early', A, '    case es::Ev::Created: std::snprintf(body, sizeof(body), "Spawn request submitted: %s.", label);', '    case es::Ev::Created: std::snprintf(body, sizeof(body), "Enemy spawned: %s.", label);'),
 ('lizalfos_stay', K, '{"Lizalfos", Profile::E_DN, 0xff0000ffu', '{"Lizalfos", Profile::E_DN, 0xff000000u'),
 ('e_oc2_subtype_lost', K, '{"Bokoblin Red (Expansion)", Profile::E_OC, 0x00ff0000u, -1, 0x0100,', '{"Bokoblin Red (Expansion)", Profile::E_OC, 0x00ff0000u, -1, 0x0000,'),
 # 0.1.2: the appended variants, their decoding and the read-only telemetry
 ('stalfos_alt_as_base', K, '{"Stalfos (Alternate Attack)", Profile::E_SF, 0x0100ff00u', '{"Stalfos (Alternate Attack)", Profile::E_SF, 0x0000ff00u'),
 ('stalfos_alt_type_2', K, '{"Stalfos (Alternate Attack)", Profile::E_SF, 0x0100ff00u', '{"Stalfos (Alternate Attack)", Profile::E_SF, 0x0200ff00u'),
 ('stalfos_alt_sentinel_lost', K, '0x0100ff00u, -1, 0, 0xff,', '0x0100ff00u, -1, 0, 0,'),
 ('stalfos_alt_wait_type', K, '{"Stalfos (Alternate Attack)", Profile::E_SF, 0x0100ff00u', '{"Stalfos (Alternate Attack)", Profile::E_SF, 0x0100ff01u'),
 ('stalfos_base_changed', K, '{"Stalfos", Profile::E_SF, 0x0000ff00u', '{"Stalfos", Profile::E_SF, 0x0100ff00u'),
 ('darknut_sword_is_mace', K, '{"Darknut (Sword)", Profile::B_TN, 0x010001ffu', '{"Darknut (Sword)", Profile::B_TN, 0x000001ffu'),
 ('darknut_mace_changed', K, '{"Darknut", Profile::B_TN, 0x000001ffu', '{"Darknut", Profile::B_TN, 0x010001ffu'),
 ('darknut_sword_brk_frame', K, '{"Darknut (Sword)", Profile::B_TN, 0x010001ffu', '{"Darknut (Sword)", Profile::B_TN, 0x010101ffu'),
 ('shield_variant_lost', K, '{"Stalfos (Breakable Shield)", Profile::E_SF, 0x1000ff00u', '{"Stalfos (Breakable Shield)", Profile::E_SF, 0x0000ff00u'),
 ('bulblin_bow_as_club', K, '{"Bulblin (Bow)", Profile::E_RD, 0xff000200u', '{"Bulblin (Bow)", Profile::E_RD, 0xff000100u'),
 ('fire_bow_as_bow', K, '{"Bulblin (Fire Bow)", Profile::E_RD, 0xff000300u', '{"Bulblin (Fire Bow)", Profile::E_RD, 0xff000200u'),
 ('variant_tail_reordered', K, '    {"Bulblin (Bow)", Profile::E_RD, 0xff000200u, -1, 0, 0, false, Route::Native, Adapt::None},\n    {"Bulblin (Fire Bow)", Profile::E_RD, 0xff000300u, -1, 0, 0, false, Route::Native, Adapt::None},\n',
  '    {"Bulblin (Fire Bow)", Profile::E_RD, 0xff000300u, -1, 0, 0, false, Route::Native, Adapt::None},\n    {"Bulblin (Bow)", Profile::E_RD, 0xff000200u, -1, 0, 0, false, Route::Native, Adapt::None},\n'),
 ('sf_decode_no_clamp', K, '    if (s.a > 1) s.a = 0;\n', ''),
 ('sf_decode_shield_shift', K, '    s.b = static_cast<std::uint8_t>(p >> 28);', '    s.b = static_cast<std::uint8_t>((p >> 24) & 0xF);'),
 ('tn_decode_type2_shift', K, '    s.b = static_cast<std::uint8_t>((p >> 24) & 0xFFFFFF);', '    s.b = static_cast<std::uint8_t>((p >> 16) & 0xFFFF);'),
 ('rd_decode_shift', K, '    s.a = static_cast<std::uint8_t>((p & 0xF00) >> 8);', '    s.a = static_cast<std::uint8_t>((p & 0xF000) >> 12);'),
 ('selector_reported_every_frame', C, '    if (!x.selector_reported && p.selector_read) {', '    if (p.selector_read) {'),
 ('attack_logged_every_frame', C, '    if (bit == 0 || (x.attacks_seen & bit)) return;', '    if (bit == 0) return;'),
 ('selector_compare_a_only', C, '      const bool match = want.a == p.sel_a && want.b == p.sel_b;', '      const bool match = want.a == p.sel_a;'),
 ('attack_expectation_inverted', C, 'return type == 0 ? kActionAttack : kActionAttack0; }', 'return type == 0 ? kActionAttack0 : kActionAttack; }'),
 ('attack_unexpected_counted_as_alt', C, '    if (!expected) ++c.attack_unexpected;\n    else ++(bit == 1 ? c.attack_alt : c.attack_base);', '    ++(bit == 1 ? c.attack_alt : c.attack_base);'),
 ('telemetry_for_every_profile', C, '    if (!want.known) return;\n', ''),
 ('probe_shield_as_type', A, 'p.sel_a = s->mType, p.sel_b = s->arg3;', 'p.sel_a = s->arg3, p.sel_b = s->mType;'),
 ('probe_type2_not_read', A, 'p.sel_a = d->mType, p.sel_b = d->mType2;', 'p.sel_a = d->mType, p.sel_b = 0;'),
 ('probe_weapon_not_read', A, 'p.sel_a = reinterpret_cast<const e_rd_class*>(a)->weapon_type, p.sel_b = 0;', 'p.sel_a = 1, p.sel_b = 0;'),
 ('probe_action_not_read', A, 'p.stalfos = true, p.sf_action = s->mAction, p.sf_anm = s->mAnm;', 'p.stalfos = true, p.sf_action = 0, p.sf_anm = s->mAnm;'),
 ('native_line_toasts', A, '  es_log(line);\n}\n\nvoid es_report(', '  es_log(line);\n  es_toast("Enemy Spawner", line, false);\n}\n\nvoid es_report('),
 ('native_line_wrong_match_text', A, 'ev.why ? "YES" : "NO",\n                  static_cast<unsigned long long>(ev.tick));\n  } else {', '"YES",\n                  static_cast<unsigned long long>(ev.tick));\n  } else {'),
]
cases = [c + (CORE,) for c in cases] + [c + (PANEL,) for c in [
 ('panel_select_again', U, 'chooser.kind = UI_CONTROL_DROPDOWN;', 'chooser.kind = UI_CONTROL_SELECT;'),
 ('panel_select_help_rml', U, 'chooser.kind = UI_CONTROL_DROPDOWN;', 'chooser.kind = UI_CONTROL_SELECT;\n  chooser.help_rml = "Choose an enemy.";'),
 ('panel_options_removed', U, '  chooser.options = es::kLabels.v;  // static storage: valid for the life of the module\n', ''),
 ('panel_option_count_short', U, '  chooser.option_count = es::kCatalogSize;', '  chooser.option_count = es::kCatalogSize - 1;'),
 ('panel_binding_callbacks', U, '  chooser.binding = UI_BINDING_CONFIG_VAR;', '  chooser.binding = UI_BINDING_CALLBACKS;'),
 ('panel_var_unbound', U, '  chooser.config_var = esui.var;', '  chooser.config_var = 0;'),
 ('panel_wrong_label', U, '  chooser.label = kUiChooser;', '  chooser.label = kUiButton;'),
 ('panel_button_handler_removed', U, '  button.on_pressed = on_invoke;\n', ''),
 ('panel_section_unchecked', U, '  if (r != MOD_OK) return es_ui_failed(error, "section", r);\n', ''),
 ('panel_dropdown_unchecked', U, '  if (r != MOD_OK) return es_ui_failed(error, "enemy_dropdown", r);\n', ''),
 ('panel_button_unchecked', U, '  if (r != MOD_OK) return es_ui_failed(error, "spawn_button", r);\n', ''),
 ('panel_text_unchecked', U, '  if (r != MOD_OK) return es_ui_failed(error, "black_notice", r);\n', ''),
 ('panel_failure_misnamed', U, 'es_ui_failed(error, "spawn_button", r)', 'es_ui_failed(error, "button", r)'),
 ('panel_failure_not_logged', U, '  es_log(line);\n', ''),
 ('panel_error_not_set', U, '  if (error) (void)mods::set_error(', '  if (false) (void)mods::set_error('),
 ('panel_notice_dropped', U, '  r = svc_ui->pane_add_text(ctx, pane, kUiBlackNotice, nullptr);\n', ''),
 ('panel_press_fixed', U, '  es_press(index);\n}', '  es_press(6);\n}'),
 ('panel_get_int_ignored', U, '  if (esui.var == 0 || svc_config->get_int(mod_ctx, esui.var, &index) != MOD_OK) index = -1;', '  (void)svc_config->get_int(mod_ctx, esui.var, &index);'),
 ('panel_button_spanish', U, '"Spawn Enemy";', '"Invocar enemigo";'),
 ('panel_chooser_spanish', U, '"Enemy";', '"Enemigo";'),
 ('panel_notice_spanish', U, '"Bokoblin Black: integration unavailable. ', '"Bokoblin Black: integracion no disponible. '),
 ('catalog_label_spanish', K, '"Bokoblin (E_OC, native)"', '"Bokoblin (E_OC, nativo)"'),
 ('catalog_black_label_spanish', K, '"Bokoblin Black (Expansion): integration unavailable"', '"Bokoblin Black (Expansion): integracion no disponible"'),
 ('default_not_lizalfos', K, '    {"Lizalfos",', '    {"Lizalfos_",'),
 ('panel_variant_label_spanish', K, '"Stalfos (Alternate Attack)"', '"Stalfos (Ataque alternativo)"'),
 ('panel_variant_label_changed', K, '"Darknut (Sword)"', '"Darknut (Greatsword)"'),
]]
def build(p, lab):
    exe = p / (lab + ('.exe' if os.name == 'nt' else ''))
    src = p / 'tests' / (lab + '.cpp')
    inc = [('/I' if os.name == 'nt' else '-I') + SDK] if lab == 'panel_lab' else []
    cmd = ['cl', '/nologo', '/std:c++20', '/EHsc', '/utf-8', '/O1', *inc, str(src), '/Fe' + str(exe), '/Fo' + str(p / (lab + '.obj'))] if os.name == 'nt' else ['g++', '-std=c++20', '-O1', '-w', *inc, '-o', str(exe), str(src)]
    return exe, subprocess.run(cmd, capture_output=True, text=True, timeout=300)
def run(p, labs):
    out = ''
    for lab in labs:
        exe, c = build(p, lab)
        if c.returncode:
            return False, 'COMPILE_ERROR ' + c.stdout[-800:] + c.stderr[-800:]
        r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=120)
        out += r.stdout + r.stderr
        if r.returncode:
            return False, out
    return True, out
def copy(p):
    shutil.copytree(root / 'src', p / 'src')
    shutil.copytree(root / 'tests', p / 'tests', ignore=shutil.ignore_patterns('*.py', '__pycache__'))
with tempfile.TemporaryDirectory() as td:
    p = Path(td); copy(p)
    assert SDK and (Path(SDK) / 'mods/svc/ui.h').is_file(), 'ES_SDK_INCLUDE must point at the SDK include directory'
    ok, out = run(p, ALL)
    assert ok and out.count('RESULT=LAB_PASS') == 3, out[-2000:]
for name, rel, old, new, labs in cases:
    assert (root / rel).read_text(encoding='utf-8').count(old) == 1, (name, old)
def one(case):
    name, rel, old, new, labs = case
    with tempfile.TemporaryDirectory() as td:
        p = Path(td); copy(p)
        f = p / rel; f.write_text(f.read_text(encoding='utf-8').replace(old, new, 1), encoding='utf-8')
        try:
            ok, out = run(p, labs)
        except subprocess.TimeoutExpired:
            return {'mutation': name, 'detected': False, 'status': 'TIMEOUT', 'timeout': True}
        killed = not ok and 'ES_LAB_FAIL line=' in out
        return {'mutation': name, 'detected': killed, 'status': 'KILLED' if killed else 'FAIL', 'timeout': False, 'tail': None if killed else out[-300:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('ES_MUTATION_WORKERS', '4'))) as pool:
    result = list(pool.map(one, cases))
print(json.dumps({'positive_control': 'ALL_THREE_LABS_PASS', 'count': len(result), 'detected': sum(x['detected'] for x in result), 'timeouts': sum(x['timeout'] for x in result), 'mutations': result}, indent=1))
sys.exit(0 if all(x['detected'] for x in result) else 1)
