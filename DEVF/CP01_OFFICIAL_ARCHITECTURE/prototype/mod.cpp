#include <mods/service.hpp>
#include <mods/svc/host.h>
#include "placement.hpp"
#include <cstring>

DEFINE_MOD();
IMPORT_SERVICE(HostService, svc_host);
IMPORT_SERVICE(StageService, svc_stage);
// No ActorService import: this module does not request an actor or register a profile.
extern "C" {
MOD_EXPORT ModResult mod_initialize(ModError* error) {
    if (!svc_host || !svc_host->version ||
        (std::strcmp(svc_host->version, "2.0.3") && std::strcmp(svc_host->version, "2.0.3.0")))
        return mods::set_error(error, MOD_UNSUPPORTED, "Official Dusklight 2.0.3 required");
    static_assert(!devf::official::kRegistrationAllowed);
    // No placement supplied. No callbacks, records, resources, pointers, tasks or profiles retained.
    return MOD_OK;
}
MOD_EXPORT ModResult mod_update(ModError*) { return MOD_OK; }
MOD_EXPORT ModResult mod_shutdown(ModError*) { return MOD_OK; }
}
