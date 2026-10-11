#include <mods/service.hpp>
#include <mods/svc/actor.h>
#include <mods/svc/stage.h>
#include <mods/svc/resource.h>
#include <mods/svc/host.h>
#include <mods/svc/log.h>
#include <cstring>
DEFINE_MOD();
IMPORT_SERVICE(ActorService, svc_actor);
IMPORT_SERVICE(StageService, svc_stage);
IMPORT_SERVICE(ResourceService, svc_resource);
IMPORT_SERVICE(HostService, svc_host);
IMPORT_SERVICE(LogService, svc_log);
// FEATURES game adds the official GameService 2.0 import; no copied actor/profile.
static_assert(sizeof(ActorId) == 4 && sizeof(ActorHandle) == 8);
static_assert(sizeof(ProfileName) == 2 && sizeof(StageActorHandle) == 8);
extern "C" {
MOD_EXPORT ModResult mod_initialize(ModError*) {
    if (!svc_host || !svc_host->version ||
        (std::strcmp(svc_host->version, "2.0.3") != 0 &&
         std::strcmp(svc_host->version, "2.0.3.0") != 0))
        return MOD_UNSUPPORTED;
    svc_log->info(mod_ctx, "DEVF CP00: service imports resolved; no actor or stage operations performed");
    return MOD_OK;
}
MOD_EXPORT ModResult mod_update(ModError*) { return MOD_OK; }
MOD_EXPORT ModResult mod_shutdown(ModError*) { return MOD_OK; }
}
