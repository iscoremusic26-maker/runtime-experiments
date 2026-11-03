#pragma once
#include "boss_phases.h"
#include <stddef.h>
namespace ehz {
// Data-only encounter presentation. Native actor pointers never escape the
// sampling pass. This is independent from screen geometry and font ownership.
struct BossCandidate {
 Identity identity{};Boss kind=Boss::None;bool primary=true,miniboss=false;
 bool customMetric=false,hasVisibilityPredicate=false,visiblePredicate=false;
 PhaseInput input{};float metric=1;
};
struct BossView {
 bool active=false,started=false,missingHidden=false,customMetric=false,healthReady=false;
 Identity identity{};Boss kind=Boss::None;bool miniboss=false;
 int maximumHealth=0,currentHealth=0,previousHealth=0,lockTicks=0,deadTicks=0,missingTicks=0;
 float raw=1,fill=1,trail=1,alpha=0;bool suppressed=false;
};
inline bool lock_switch_boss(Boss b){return b==Boss::Darknut||b==Boss::Aeralfos;}
inline const BossCandidate* choose_boss(const BossCandidate* candidates,size_t n,
 const BossView& current,Identity locked){
 for(size_t i=0;i<n;++i){const auto&x=candidates[i];if(x.primary&&lock_switch_boss(x.kind)&&same(x.identity,locked))return &x;}
 const BossCandidate* best=nullptr;
 for(size_t i=0;i<n;++i){const auto&x=candidates[i];if(!x.primary)continue;
  if(current.active&&same(x.identity,current.identity))return &x;
  if(!best||x.input.sample.health>best->input.sample.health)best=&x;
 }
 return best;
}
inline bool has_phase_model(Boss b){
 switch(b){case Boss::Diababa:case Boss::Morpheel:case Boss::Stallord:case Boss::Blizzeta:
 case Boss::Darknut:case Boss::Zant:case Boss::Argorok:case Boss::BeastGanon:case Boss::Ganondorf:return true;
 default:return false;}
}
inline PhaseResult step_phase(Boss b,PhaseState& s,const PhaseInput& x){
 switch(b){case Boss::Morpheel:return morpheel_phase(s,x);case Boss::Stallord:return stallord_phase(s,x);
 case Boss::Blizzeta:return blizzeta_phase(s,x);case Boss::Darknut:return darknut_phase(s,x);
 case Boss::Zant:return zant_phase(s,x);case Boss::Argorok:return argorok_phase(s,x);
 case Boss::BeastGanon:return beast_ganon_phase(s,x);case Boss::Ganondorf:return ganondorf_phase(s,x);
 default:return {};}
}
inline bool intermediate_phase(Boss b,const PhaseState&s,const DiababaState&d,int beastAction){
 switch(b){case Boss::Diababa:return !d.bodyPhase;
 case Boss::Morpheel:case Boss::Stallord:case Boss::Blizzeta:case Boss::Darknut:case Boss::Argorok:return s.phase<4;
 case Boss::Zant:return s.phase!=4;case Boss::Ganondorf:return s.phase!=3;
 case Boss::BeastGanon:return beastAction!=9;default:return false;}
}
// Original 0x7d728..0x7d8a7: immediate fill, delayed 0.15 trail, 0.18/0.24
// asymmetric fade. A hidden transition primes both fills once alpha < .04.
inline bool advance_boss_visual(BossView&v){
 if(v.suppressed){if(v.alpha<0.04f)v.fill=v.trail=v.raw;}
 else{v.fill=v.raw;v.trail+=(v.raw-v.trail)*0.15f;}
 float target=v.started&&!v.missingHidden&&!v.suppressed&&v.deadTicks<19?1.0f:0.0f;
 v.alpha+=(target-v.alpha)*(v.alpha>target?0.24f:0.18f);
 return v.deadTicks>=19&&v.alpha<0.01f;
}
struct BossPresenter {
 BossView view{};PhaseState phase{};DiababaState diababa{};
 Boss recent=Boss::None;int recentTicks=0;bool fyrusFinal=false;
 // Caller stores the returned identity in its scene-local retired set.
 Identity retired{},phaseOwner{};
 void clear(){view={};phase={};diababa={};recent=Boss::None;recentTicks=0;fyrusFinal=false;retired={};phaseOwner={};}
 void tick(const BossCandidate*c,Identity locked,const DiababaInput& aggregate){
  retired={};if(recentTicks>0)--recentTicks;
  if(!c){
   if(!view.active)return;
   int absent=view.missingTicks++;
   if(!view.started){if(absent>=150){view={};return;}}
   else{
    bool eligible=!(view.kind==Boss::Diababa&&!diababa.bodyPhase)&&
     (!view.customMetric||view.kind==Boss::DeathSword||(view.kind==Boss::Fyrus&&fyrusFinal))&&view.raw<0.45f;
    if(eligible){view.raw+=(0-view.raw)*0.35f;if(view.raw<0.01f)view.raw=0;}
    if(absent>=(eligible?10:60))view.missingHidden=true;
    if(absent>=(eligible?24:240)){if(eligible)retired=view.identity;view={};return;}
   }
   if(advance_boss_visual(view)){retired=view.identity;view={};}return;
  }
  const auto&x=c->input.sample;bool switched=!view.active||!same(view.identity,c->identity);
  bool preserve=switched&&view.active&&view.started&&lock_switch_boss(view.kind)&&lock_switch_boss(c->kind);
  if(switched){
   view={};view.active=true;view.identity=c->identity;view.kind=c->kind;view.miniboss=c->miniboss;
   view.customMetric=c->customMetric||c->kind==Boss::Diababa;
   view.maximumHealth=maximum(0,x.health);view.currentHealth=view.previousHealth=x.health;view.healthReady=x.health>0;
   if(!same(phaseOwner,c->identity)){phase=initial_phase(c->kind);diababa={};phaseOwner=c->identity;}fyrusFinal=false;
   if(preserve){view.started=true;view.alpha=1;}
   else if(recent==c->kind&&recentTicks>0&&(!c->hasVisibilityPredicate||c->visiblePredicate))view.started=true;
  }
  bool wasStarted=view.started;view.missingTicks=0;view.missingHidden=false;view.suppressed=false;
  if(c->kind==Boss::Fyrus)fyrusFinal=x.cycles>=3;
  if(c->kind==Boss::Diababa){auto r=diababa_phase(diababa,aggregate);view.raw=r.fill;view.started|=r.started;view.suppressed=r.suppressed;}
  else if(has_phase_model(c->kind)){if(c->kind==Boss::Morpheel||c->kind==Boss::Stallord||c->kind==Boss::Zant||c->kind==Boss::Ganondorf||c->kind==Boss::BeastGanon)view.currentHealth=x.health;auto r=step_phase(c->kind,phase,c->input);view.raw=r.fill;if(c->kind==Boss::BeastGanon)view.currentHealth=int(r.fill*100);else view.started|=r.started;view.suppressed=r.suppressed;}
  else{
   if(view.customMetric){view.raw=c->metric;if(c->metric<0.997f&&c->kind!=Boss::DeathSword)view.started=true;}
   else{
    view.maximumHealth=maximum(view.maximumHealth,x.health);view.healthReady|=x.health>0;
    if(x.health<view.previousHealth&&x.health>=0&&view.previousHealth>0)view.started=true;
    view.previousHealth=view.currentHealth=x.health;
    view.raw=view.maximumHealth>0?float(x.health)/view.maximumHealth:1;
    if(!view.healthReady)view.raw=1;
    if(c->kind==Boss::DekuToad&&(x.action==9||c->input.dead)){view.started=true;view.raw=0;view.currentHealth=0;}
   }
   if(preserve)view.fill=view.trail=view.raw;
  }
  if(c->kind==Boss::Aeralfos)view.suppressed=!c->input.lineOfSight;
  view.raw=clamp01(view.raw);
  if(same(c->identity,locked)){
   if(view.lockTicks++>=7&&c->kind!=Boss::DeathSword)view.started=true;
  }else view.lockTicks=0;
  if(c->hasVisibilityPredicate&&!c->input.event&&c->visiblePredicate)view.started=true;
  if(!wasStarted&&view.started)recent=c->kind;
  if(view.started)recentTicks=150;
  if(!intermediate_phase(c->kind,phase,diababa,x.action)&&view.raw<=0.02f&&view.started)++view.deadTicks;
  else view.deadTicks=0;
  if(advance_boss_visual(view)){retired=view.identity;view={};}
 }
};
}
