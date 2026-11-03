cmake_minimum_required(VERSION 3.25)
project(enemy_health_bars_203 CXX)

# Dusklight 2.0.3 mod SDK, composed WITHOUT touching the original source tree: deps/dusk_root is a symlink farm
# (cmake/, sdk/, include/, libs/, assets/ -> the extracted 2.0.3 source; extern/aurora -> the pinned Aurora headers).
set(BARS203_DUSK_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../deps/dusk_root" CACHE PATH "Composed Dusklight 2.0.3 SDK root")
# Link against the import library shipped in the EXACT 2.0.3 distribution (no stub download).
set(DUSK_GAME_EXE "${CMAKE_CURRENT_SOURCE_DIR}/../ref/win/sdk/windows-amd64.lib" CACHE FILEPATH "2.0.3 host import library")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_subdirectory("${BARS203_DUSK_ROOT}/sdk" dusk-sdk EXCLUDE_FROM_ALL)

add_mod(enemy_health_bars_203_cp06_armos
    FEATURES game
    SOURCES  src/mod.cpp src/tracker.cpp src/boss_tracker.cpp src/boss_fields.cpp src/boss_paint.cpp src/game_bars.cpp src/normal_draw.cpp src/hm_bridge.cpp
    MOD_JSON mod.json
)
