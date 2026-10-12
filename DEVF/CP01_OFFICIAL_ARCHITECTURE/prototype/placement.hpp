#pragma once
#include <mods/svc/actor.h>
#include <mods/svc/stage.h>
#include <array>
#include <bit>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

namespace devf::official {
inline constexpr bool kRegistrationAllowed = false;
inline constexpr char kPolicy[] = "DISARMED_NO_REGISTRATION";
inline constexpr char kEnemy[] = "E_SB"; // Official canonical name, profile 0x1C1, argument -1.
enum class RecordKind { Actr, Tgsc };
struct Placement {
    std::string stage;
    std::uint8_t room{};
    std::int8_t layer{};
    std::array<float, 3> position{};
    std::array<std::int16_t, 3> angle{};
    RecordKind kind{RecordKind::Actr};
    std::array<std::uint8_t, 3> scale_tenths{10, 10, 10};
};
inline bool valid(const Placement& p) {
    // Deliberately narrower than StageService validation: no wildcard or guessed scene.
    if (p.stage.empty() || p.stage.size() > 8 || p.room >= 64 || p.layer < 0 || p.layer > 15)
        return false;
    for (unsigned char ch : p.stage)
        if (!((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z') ||
              (ch >= '0' && ch <= '9') || ch == '_')) return false;
    for (float value : p.position) if (!std::isfinite(value)) return false;
    if (p.kind != RecordKind::Actr && p.kind != RecordKind::Tgsc) return false;
    for (auto value : p.scale_tenths) if (!value) return false;
    if (p.kind == RecordKind::Actr && p.scale_tenths != std::array<std::uint8_t, 3>{10, 10, 10})
        return false;
    return true; // Encoding validity only; NOT placement safety or native resource readiness.
}
inline void put_be(std::vector<std::uint8_t>& out, std::size_t offset,
                   std::uint32_t value, std::size_t width) {
    for (std::size_t i = 0; i < width; ++i)
        out[offset + i] = static_cast<std::uint8_t>(value >> (8 * (width - i - 1)));
}
inline std::vector<std::uint8_t> encode(const Placement& p) {
    if (!valid(p)) return {};
    std::vector<std::uint8_t> out(p.kind == RecordKind::Actr ? 32 : 35, 0);
    for (std::size_t i = 0; i < sizeof(kEnemy) - 1; ++i) out[i] = kEnemy[i];
    // E_SB's u8 room-switch parameter is disabled with 0xFF. This is not a universal stat.
    put_be(out, 8, 0x000000FFu, 4);
    for (std::size_t i = 0; i < 3; ++i) {
        put_be(out, 12 + 4 * i, std::bit_cast<std::uint32_t>(p.position[i]), 4);
        put_be(out, 24 + 2 * i, static_cast<std::uint16_t>(p.angle[i]), 2);
    }
    put_be(out, 30, 0xFFFFu, 2);
    if (p.kind == RecordKind::Tgsc)
        for (std::size_t i = 0; i < 3; ++i) out[32 + i] = p.scale_tenths[i];
    return out;
}
inline ActorSpawnParams direct_request(const Placement& p) {
    ActorSpawnParams out{};
    out.parameters = 0xFF;
    out.argument = -1;
    out.room_num = static_cast<std::int8_t>(p.room);
    out.position = {p.position[0], p.position[1], p.position[2]};
    out.angle = {p.angle[0], p.angle[1], p.angle[2]};
    out.scale = {p.scale_tenths[0] * 0.1f, p.scale_tenths[1] * 0.1f, p.scale_tenths[2] * 0.1f};
    out.create_function = nullptr; // No DLL post-create callback may escape.
    return out; // A data definition; this function never requests creation.
}
inline ModResult define_disarmed(ModContext* ctx, const StageService& stage,
                                 const Placement& p, StageActorHandle* handle) {
    if (handle) *handle = 0;
    const auto wire = encode(p);
    if (wire.empty()) return MOD_INVALID_ARGUMENT;
    if constexpr (kRegistrationAllowed) {
        // Type checked against official StageService 1.0, unreachable in this checkpoint.
        return stage.add_actor(ctx, p.stage.c_str(), p.room, p.layer, wire.data(), wire.size(), handle);
    }
    return MOD_UNSUPPORTED;
}
static_assert(!kRegistrationAllowed);
static_assert(ACTOR_SERVICE_MAJOR == 1 && STAGE_SERVICE_MAJOR == 1);
} // namespace devf::official
