#pragma once
// Enemy Spawner (Standalone) 0.1.2: the list of enemies this mod can create. PURE: no game header, no address.
//
// Adapted from the Enemy Spawner of Dawnlight by BeZide93 (https://github.com/BeZide93/dawnlight, CC0 1.0 Universal),
// commit b5e9046cd98bdd8593ab2cf219d72a0f61ef7213, src/enemy_spawner.{hpp,cpp}: kEnemySpawnerProfileLabels, kEnemySpawnerProfiles,
// kEnemySpawnerParameters, the Helmasaurus argument, the angle.z switch sentinel of Stalfos/Kargarok and the flying height list.
// Differences from Dawnlight (each one checked in the native source of Dusklight 2.0.3, TwilitRealm/dusklight@40457c6):
//  * Goron (an NPC) and Staltroop (retires itself without Stallord; Dawnlight replaces its idle AI) are not offered.
//  * Lizalfos and Dynalfos use low byte 0xFF instead of 0: with 0 the native create selects ACTION_STAY (d_a_e_dn.cpp L3482,
//    d_a_e_mf.cpp L3243), an idle that only reacts to noise; 0xFF is the ordinary patrol that finds Link and fights.
//  * Bokoblin is split by the native subtype byte of angle.x (d_a_e_oc.cpp create(): 0 -> resource E_OC, 1 -> E_OC2), and into
//    entries that ask Bokoblin Expansion for its classification. The Black entry is never creatable (see docs/BLACK_API_PROPOSAL.md).
//
// 0.1.2: entries 0..44 are the 0.1.1 FIX01 catalog, byte for byte, in the same order (ci/baseline_0_1_1.json, ci/baseline_check.py): the persisted
// index of the chooser keeps naming the same enemy. Five native variants are appended at 45..49, each selected by native parameter bits read in the
// create() of its actor (TwilitRealm/dusklight@40457c6). See docs/VARIANTS_0_1_2.md for the evidence and for the candidates that were NOT added.
//  * Stalfos (Alternate Attack)  E_SF 0x0100FF00: mType = (p >> 24) & 0xF = 1 (d_a_e_sf.cpp L1774). e_sf_fight_run picks ACTION_ATTACK_0 for mType 1
//    (L515-519), whose e_sf_attack_0 plays BCK_SF_ATTACK02 with its hit window on frames 15..22 (L556, L561); mType 0 plays BCK_SF_ATTACK01, frames 81..86.
//    Weapon model BMDR_SF_SWORDB instead of SWORDA (wepon_data, L1716). Same HP (200), defence, guard, crash and get-up as the base Stalfos.
//  * Darknut (Sword)  B_TN 0x010001FF: the 0.1.1 "Darknut" (0x000001FF, mType 1, archive B_tnp2, weapon BMDR_TN2_MACE) plus mType2 = (p >> 24) = 1
//    (d_a_b_tn.cpp L5062), whose only use is CreateHeap part 13: BMDR_TN2_SWORD_A instead of BMDR_TN2_MACE (L4967). AI, attacks, hitboxes (mSwordSphs on the
//    part-13 matrix), phases and HP are those of the mace Darknut. mBrkAnmFrame = (p >> 16) & 0xFFFF = 0x0100 stored in a u8 -> 0, as for 0x000001FF.
//  * Stalfos (Breakable Shield)  E_SF 0x1000FF00: arg3 = p >> 28 = 1 (L1775): BMDR_SF_SHIELDB, and only arg3 1 loses shield durability (field_0x5c0, 30)
//    on blocked hits until the shield breaks (arg3 = 0xFF, L1626-1637): no more guard (L1126). mType 0: the base attack.
//  * Bulblin (Bow) / Bulblin (Fire Bow)  E_RD 0xFF000200 / 0xFF000300: weapon_type = (p & 0xF00) >> 8 = 2 / 3 (d_a_e_rd.cpp L7375): a bow and E_ARROW
//    children (normal / fire, L6899-6910) instead of the club. Low byte 0 and switch byte 0xFF as the base Bulblin. Bomb arrows (4) are refused by the
//    native create (L7380) and are not offered.
// NEVER offered: the Temple of Time Darknut (B_TN mType 0). Its create runs its first Execute in ACT_ROOMDEMO (event order, camera stop, Link demo
// mode), its phase change and death are cutscenes, and its ending sets the stage middle-boss save bit and moves Link to fixed coordinates.
// static_assert below: no B_TN entry can decode to mType 0.
#include <cstddef>
#include <cstdint>

namespace es {

// Native profile of each entry. mod.cpp maps it to the fpcNm_* value of the SDK and checks the mapping at compile time.
enum class Profile : std::uint8_t { B_TN, E_OC, E_FZ, E_BA, E_TT, E_GI, B_GG, E_KK, E_FB, E_BS, E_BU, E_MS, E_WW, E_FS, E_CR, E_SH, E_TK, E_TK2, E_RD, E_DN, E_DD, E_MF, E_ST, E_HB, E_GB, E_DB, E_SF, E_MM, E_KR, E_GE, E_AI, E_SM2, Count };

// What a press of "Spawn Enemy" means for this entry.
enum class Route : std::uint8_t {
  Native,            // create the native actor, nothing else
  ExpansionBlue,     // native E_OC; Bokoblin Expansion must classify it BLUE (40 -> 220 HP) or the result is reported as native
  ExpansionRed,      // native E_OC2; Expansion must classify it RED (220 -> 330 HP)
  BlackUnavailable,  // Expansion 0.17.0 admits Black only for its exact packaged encounters: no public contract exists. Never creates.
};

// A minimal adaptation, applied only to actors this mod created, from mod_update (before the actor's own Execute).
enum class Adapt : std::uint8_t {
  None,
  ToadpoliWater,  // e_tk: mExecuteState kept above 0, so it stays on the chosen ground instead of searching water (Dawnlight's rule)
  ToadpoliLava,   // e_tk2: mActionTimer[3] kept above 0, so it stays on the chosen ground instead of searching lava (Dawnlight's rule)
};

struct Entry {
  const char* label;
  Profile profile;
  std::uint32_t parameters;
  std::int8_t argument;
  std::int16_t angle_x;  // E_OC: high byte = native subtype (0 -> E_OC, else E_OC2)
  std::int16_t angle_z;  // Stalfos/Kargarok: defeated-switch sentinel 0xFF
  bool flying;           // spawned 200 units above the ground
  Route route;
  Adapt adapt;
};

inline constexpr Entry kCatalog[] = {
    {"Darknut", Profile::B_TN, 0x000001ffu, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Bokoblin (E_OC, native)", Profile::E_OC, 0x00ff0000u, -1, 0x0000, 0, false, Route::Native, Adapt::None},
    {"Bokoblin (E_OC2, native)", Profile::E_OC, 0x00ff0000u, -1, 0x0100, 0, false, Route::Native, Adapt::None},
    {"Bokoblin Blue (Expansion)", Profile::E_OC, 0x00ff0000u, -1, 0x0000, 0, false, Route::ExpansionBlue, Adapt::None},
    {"Bokoblin Red (Expansion)", Profile::E_OC, 0x00ff0000u, -1, 0x0100, 0, false, Route::ExpansionRed, Adapt::None},
    {"Bokoblin Black (Expansion): integration unavailable", Profile::E_OC, 0x00ff0000u, -1, 0x0100, 0, false, Route::BlackUnavailable, Adapt::None},
    {"Lizalfos", Profile::E_DN, 0xff0000ffu, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Dynalfos", Profile::E_MF, 0xff0000ffu, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Bulblin", Profile::E_RD, 0xff000100u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Stalfos", Profile::E_SF, 0x0000ff00u, -1, 0, 0xff, false, Route::Native, Adapt::None},
    {"Stalchild", Profile::E_BS, 0x00ffff00u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Stalhound (night only)", Profile::E_SH, 0x00ffff00u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Gibdo", Profile::E_GI, 0x00ff01ffu, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Puppet", Profile::E_FS, 0x00000000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"White Wolfos", Profile::E_WW, 0x03000000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Chilfos", Profile::E_KK, 0x00ff0000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Freezard", Profile::E_FB, 0x00ffff00u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Mini Freezard", Profile::E_FZ, 0x00000000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Tektite", Profile::E_TT, 0x000000ffu, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Keese", Profile::E_BA, 0xffff0f01u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Fire Keese", Profile::E_BA, 0xffff1f01u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Ice Keese", Profile::E_BA, 0xffff2f01u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Bubble", Profile::E_BU, 0xffff0f00u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Fire Bubble", Profile::E_BU, 0xffff1f00u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Ice Bubble", Profile::E_BU, 0xffff2f00u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Aeralfos", Profile::B_GG, 0xffff0002u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Kargarok", Profile::E_KR, 0xffffff00u, -1, 0, 0xff, true, Route::Native, Adapt::None},
    {"Guay", Profile::E_GE, 0x00ffff01u, -1, 0, 0, true, Route::Native, Adapt::None},
    {"Rat", Profile::E_MS, 0xffff0000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Bomskit", Profile::E_CR, 0x00000000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Water Toadpoli", Profile::E_TK, 0x00ff0000u, -1, 0, 0, false, Route::Native, Adapt::ToadpoliWater},
    {"Fire Toadpoli", Profile::E_TK2, 0x00000000u, -1, 0, 0, false, Route::Native, Adapt::ToadpoliLava},
    {"Dodongo", Profile::E_DD, 0xffff0000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Skulltula", Profile::E_ST, 0xff000002u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Baba Serpent", Profile::E_HB, 0xff000000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Big Baba", Profile::E_GB, 0x00ffff00u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Deku Baba", Profile::E_DB, 0xff000000u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Helmasaur", Profile::E_MM, 0x0000ff00u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Helmasaurus", Profile::E_MM, 0x0000ff00u, 1, 0, 0, false, Route::Native, Adapt::None},
    {"Armos", Profile::E_AI, 0x00ff000au, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Red Chu", Profile::E_SM2, 0xffff0010u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Blue Chu", Profile::E_SM2, 0xffff0020u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Yellow Chu", Profile::E_SM2, 0xffff0030u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Purple Chu", Profile::E_SM2, 0xffff0040u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Black Chu", Profile::E_SM2, 0xffff0060u, -1, 0, 0, false, Route::Native, Adapt::None},
    // ---- 0.1.2: appended native variants (indices 45..49). Never insert above this line.
    {"Stalfos (Alternate Attack)", Profile::E_SF, 0x0100ff00u, -1, 0, 0xff, false, Route::Native, Adapt::None},
    {"Darknut (Sword)", Profile::B_TN, 0x010001ffu, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Stalfos (Breakable Shield)", Profile::E_SF, 0x1000ff00u, -1, 0, 0xff, false, Route::Native, Adapt::None},
    {"Bulblin (Bow)", Profile::E_RD, 0xff000200u, -1, 0, 0, false, Route::Native, Adapt::None},
    {"Bulblin (Fire Bow)", Profile::E_RD, 0xff000300u, -1, 0, 0, false, Route::Native, Adapt::None},
};
inline constexpr std::size_t kCatalogSize = sizeof(kCatalog) / sizeof(kCatalog[0]);
inline constexpr std::size_t kOriginalCount = 45;  // the 0.1.1 FIX01 entries, indices 0..44, frozen
static_assert(kCatalogSize == 50 && kCatalogSize > kOriginalCount, "0.1.2 = the 45 entries of 0.1.1 + 5 appended variants");

// ---------------------------------------------------------------- native selectors, decoded exactly as the native create() does
// What the actor will read from these parameters (TwilitRealm/dusklight@40457c6). Used by the guards below, by the labs, and by the read-only
// telemetry that compares this expectation with the fields of the created actor (spawner_adapter.inc es_selector_of).
struct Selector {
  bool known = false;  // a profile whose selector this mod decodes (E_SF, B_TN, E_RD)
  std::uint8_t a = 0;  // E_SF mType, B_TN mType, E_RD weapon_type
  std::uint8_t b = 0;  // E_SF arg3 (shield), B_TN mType2, E_RD unused
};
inline constexpr Selector decode_selector(Profile profile, std::uint32_t p) noexcept {
  Selector s;
  if (profile == Profile::E_SF) {  // d_a_e_sf.cpp daE_SF_Create L1774-1782 (u8 fields)
    s.known = true;
    s.a = static_cast<std::uint8_t>((p >> 24) & 0xF);
    s.b = static_cast<std::uint8_t>(p >> 28);
    if (s.a > 1) s.a = 0;
    if (s.b > 1) s.b = 0;
  } else if (profile == Profile::B_TN) {  // d_a_b_tn.cpp create() L5034-5066: fopAcM_GetParamBit(this, 8, 8) / (this, 24, 24), stored in u8
    s.known = true;
    s.a = static_cast<std::uint8_t>((p >> 8) & 0xFF);
    s.b = static_cast<std::uint8_t>((p >> 24) & 0xFFFFFF);
    if (s.a != 1) s.a = 0;
    if (s.b != 1) s.b = 0;
  } else if (profile == Profile::E_RD) {  // d_a_e_rd.cpp daE_RD_Create L7375-7378
    s.known = true;
    s.a = static_cast<std::uint8_t>((p & 0xF00) >> 8);
    if (s.a == 15) s.a = 0;
  }
  return s;
}
// The Temple of Time Darknut (mType 0) is never offered: see the top of this file and docs/VARIANTS_0_1_2.md.
inline constexpr bool no_temple_of_time_darknut() noexcept {
  for (const Entry& e : kCatalog)
    if (e.profile == Profile::B_TN && decode_selector(e.profile, e.parameters).a != 1) return false;
  return true;
}
static_assert(no_temple_of_time_darknut(), "a B_TN entry decodes to mType 0 (Temple of Time Darknut: ACT_ROOMDEMO, cutscenes, middle-boss save bit)");
// Bulblin weapon types >= 4 (bomb arrows) make the native create fail: never offered.
inline constexpr bool bulblin_weapons_creatable() noexcept {
  for (const Entry& e : kCatalog)
    if (e.profile == Profile::E_RD && decode_selector(e.profile, e.parameters).a >= 4) return false;
  return true;
}
static_assert(bulblin_weapons_creatable(), "an E_RD entry asks for a weapon type the native create refuses");

// Labels in catalog order, for the host's select control.
struct Labels {
  const char* v[kCatalogSize];
};
inline constexpr Labels make_labels() noexcept {
  Labels l{};
  for (std::size_t i = 0; i < kCatalogSize; ++i) l.v[i] = kCatalog[i].label;
  return l;
}
inline constexpr Labels kLabels = make_labels();

}  // namespace es
