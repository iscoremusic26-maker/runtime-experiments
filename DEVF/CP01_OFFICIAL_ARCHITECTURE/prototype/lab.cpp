#include "placement.hpp"
#include <mods/svc/host.h>
#include <iostream>
#include <limits>
#include <cstdlib>
#include <cstring>
extern "C" ModResult mod_initialize(ModError*);
extern "C" ModResult mod_update(ModError*);
extern "C" ModResult mod_shutdown(ModError*);
extern "C" const HostService* svc_host;

namespace {
int checks = 0;
int add_calls = 0;
void check(bool ok, const char* label) {
    if (!ok) { std::cerr << "FAIL " << label << '\n'; std::exit(1); }
    ++checks; std::cout << "PASS " << label << '\n';
}
ModResult fake_add(ModContext*, const char*, std::uint8_t, std::int8_t,
                   const void*, std::size_t, StageActorHandle*) { ++add_calls; return MOD_OK; }
std::uint32_t be(const std::vector<std::uint8_t>& bytes, std::size_t offset, std::size_t size) {
    std::uint32_t result = 0;
    for (std::size_t i = 0; i < size; ++i) result = (result << 8) | bytes[offset + i];
    return result;
}
}
int main() {
    using namespace devf::official;
    // Synthetic encoding fixture: NOT a game location or an approved candidate.
    Placement p{"LAB_ONLY", 3, 6, {1.0f, -2.5f, 0.0f}, {0, -24697, 32767}};
    auto wire = encode(p);
    check(wire.size() == 32, "ACTR_exact_32_bytes");
    check(std::memcmp(wire.data(), "E_SB\0\0\0\0", 8) == 0, "canonical_native_name_and_padding");
    check(be(wire, 8, 4) == 255 && wire[8] == 0 && wire[11] == 255, "BE_actor_specific_switch_sentinel");
    check(be(wire, 12, 4) == 0x3F800000 && be(wire, 16, 4) == 0xC0200000, "BE_float_coordinates");
    check(be(wire, 26, 2) == static_cast<std::uint16_t>(-24697) && be(wire, 28, 2) == 32767, "BE_signed_angles");
    check(be(wire, 30, 2) == 65535, "setID_sentinel");
    auto copy = p; copy.kind = RecordKind::Tgsc; copy.scale_tenths = {10, 20, 30};
    auto scaled = encode(copy);
    check(scaled.size() == 35 && scaled.size() != 36 && scaled[32] == 10 && scaled[34] == 30,
          "TGSC_35_wire_bytes_not_cpp_padded_size");
    check(std::memcmp(scaled.data(), wire.data(), 32) == 0, "TGSC_preserves_ACTR_prefix");
    copy = p; copy.stage.clear(); check(encode(copy).empty(), "reject_empty_stage");
    copy = p; copy.stage = "TOO_LONG9"; check(encode(copy).empty(), "reject_long_stage");
    copy = p; copy.stage = "A/../B"; check(encode(copy).empty(), "reject_noncanonical_stage");
    copy = p; copy.room = 255; check(encode(copy).empty(), "reject_wildcard_room");
    copy = p; copy.room = 64; check(encode(copy).empty(), "reject_outside_room_table");
    copy = p; copy.layer = -1; check(encode(copy).empty(), "reject_wildcard_layer");
    copy = p; copy.layer = 16; check(encode(copy).empty(), "reject_outside_layer_nibble");
    copy = p; copy.position[0] = std::numeric_limits<float>::quiet_NaN();
    check(encode(copy).empty(), "reject_NaN");
    copy = p; copy.position[1] = std::numeric_limits<float>::infinity();
    check(encode(copy).empty(), "reject_infinity");
    copy = p; copy.scale_tenths[0] = 0; check(encode(copy).empty(), "reject_zero_scale");
    copy = p; copy.scale_tenths[0] = 20; check(encode(copy).empty(), "reject_ACTR_unencoded_scale");
    copy = p; copy.kind = static_cast<RecordKind>(9); check(encode(copy).empty(), "reject_unknown_record_kind");
    const auto direct = direct_request(p);
    check(direct.create_function == nullptr && direct.parameters == 255 && direct.argument == -1,
          "direct_definition_null_callback_no_creation");
    StageService mock{}; mock.add_actor = fake_add; StageActorHandle handle = 123;
    check(define_disarmed(nullptr, mock, p, &handle) == MOD_UNSUPPORTED && handle == 0 && add_calls == 0,
          "hard_disarm_no_Stage_registration");
    copy = p; copy.stage.clear(); handle = 456;
    check(define_disarmed(nullptr, mock, copy, &handle) == MOD_INVALID_ARGUMENT && handle == 0 && add_calls == 0,
          "invalid_plan_has_no_side_effects");
    ModError error = MOD_ERROR_INIT;
    svc_host = nullptr;
    check(mod_initialize(&error) == MOD_UNSUPPORTED, "module_rejects_missing_host");
    HostService host{}; host.version = "2.0.2"; svc_host = &host;
    check(mod_initialize(&error) == MOD_UNSUPPORTED, "module_rejects_other_version");
    host.version = "2.0.3";
    check(mod_initialize(&error) == MOD_OK && mod_update(&error) == MOD_OK &&
          mod_shutdown(&error) == MOD_OK && mod_shutdown(&error) == MOD_OK && add_calls == 0,
          "module_lifecycle_remains_disarmed");
    std::cout << "SUMMARY " << checks << " PASS; no host/game/runtime test\n";
}
