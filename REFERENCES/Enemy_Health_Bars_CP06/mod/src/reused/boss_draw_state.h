#pragma once
#include "boss_presenter.h"
namespace ehz {
// Rendering receives only value data; never an actor address, ID or process profile.
struct BossDrawState { bool active=false; char name[48]{}; float fill=1,trail=1,alpha=0; };
inline const char* boss_name(Boss b) {
 switch(b){
 case Boss::Diababa:return "Diababa";case Boss::Fyrus:return "Fyrus";
 case Boss::Morpheel:return "Morpheel";case Boss::Stallord:return "Stallord";
 case Boss::Blizzeta:return "Blizzeta";case Boss::Armogohma:return "Armogohma";
 case Boss::Argorok:return "Argorok";case Boss::BeastGanon:return "Dark Beast Ganon";
 case Boss::Ganondorf:return "Ganondorf";case Boss::PuppetZelda:return "Puppet Zelda";
 case Boss::Zant:return "Zant";case Boss::Darknut:return "Darknut";
 case Boss::Aeralfos:return "Aeralfos";case Boss::DeathSword:return "Death Sword";
 case Boss::KingBulblin:return "King Bulblin";case Boss::Darkhammer:return "Darkhammer";
 case Boss::Ook:return "Ook";case Boss::DekuToad:return "Deku Toad";
 case Boss::Dangoro:return "Dangoro";case Boss::PhantomZant:return "Phantom Zant";
 default:return "Boss";}
}
inline BossDrawState copy_boss_draw(const BossView& v) {
 BossDrawState d{};d.active=v.active&&v.kind!=Boss::None;
 const char*n=boss_name(v.kind);for(unsigned i=0;i+1<sizeof(d.name)&&n[i];++i)d.name[i]=n[i];
 d.fill=v.fill;d.trail=v.trail;d.alpha=v.alpha;return d;
}
void boss_publish(const BossView&);
const BossDrawState& boss_draw_snapshot();
// Internal options entry for later manifest/config wiring. Both styles are native.
bool boss_set_draw_options(int style,float offsetX,float offsetY);
}
