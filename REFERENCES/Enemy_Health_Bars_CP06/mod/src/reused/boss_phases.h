#pragma once
#include "health_model.h"
namespace ehz {
// Separate presentation state from instantaneous damage metrics. The source
// routines produce two control flags, not just a percentage. Their caller's
// fade/selection policy is still a distinct layer.
struct PhaseState {
 uint32_t phase=0;int timer=0;bool healthReady=false;
 int previous=-1,damagePeak=0,lastPhase=0;float fill=1,lastHealth=-1;
};
struct PhaseResult { float fill=0;bool started=false,suppressed=false; };
struct PhaseInput { BossSample sample;int demo=0;bool event=false,dead=false,intro=false,lineOfSight=true;int detail=0; };

inline PhaseState initial_phase(Boss boss){
 PhaseState s{};if(boss==Boss::Argorok)s.previous=0;
 if(boss==Boss::Zant)s.lastPhase=-1;return s;
}

// Original ELF 0x7dbe0 aggregates the main body and its two independent heads.
// The intro predicate belongs to the encounter selection layer, not the actor.
struct DiababaState {
 int phase=0,lastMetric=0,cyclesMetric=0;bool bodyPhase=false,introSeen=false;
 int introTicks=0,readyTicks=0;bool started=false;
 int headlessTicks=0,eventTicks=0,cycles=0;int16_t lastHealth=0;
};
struct DiababaInput {
 bool hasBody=false,bodyVulnerable=false,event=false,introPredicate=false;
 int heads=0,health=0,action=0,mode=0;
};
inline PhaseResult diababa_phase(DiababaState& s,const DiababaInput& x){
 PhaseResult r{};
 if(x.hasBody&&s.started&&(x.action==4||(x.action==3&&x.mode>=40))){
  s.bodyPhase=true;s.phase=3;r.started=true;return r;
 }
 if(x.event&&s.introTicks++>=20)s.introSeen=true;
 if(x.introPredicate)s.introSeen=true;
 if(!x.event&&s.introSeen&&x.heads>0){if(s.readyTicks++>=10)s.started=true;}
 else if(!s.started)s.readyTicks=0;
 if(!s.started){r.fill=1;r.suppressed=true;return r;}
 r.started=true;
 s.eventTicks=x.event?s.eventTicks+1:0;
 s.headlessTicks=x.heads?0:s.headlessTicks+1;
 int hp=x.hasBody?x.health:0;
 if(!s.bodyPhase){
  if((x.hasBody&&x.bodyVulnerable)||(s.headlessTicks>=91&&!x.event)){
   s.bodyPhase=true;s.cycles=0;s.lastHealth=(int16_t)hp;
  }else{
   s.phase=1;s.lastMetric=x.heads;r.suppressed=x.heads<=0;
   r.fill=x.heads>0?clamp01(x.heads*0.5f):0.05f;return r;
  }
 }
 r.suppressed=s.eventTicks>=13;
 if(((s.lastHealth>0&&hp<=0)||(s.lastHealth>=1&&s.lastHealth<45&&hp>=45))&&s.cycles<=1)++s.cycles;
 s.lastHealth=(int16_t)hp;s.phase=2;s.cyclesMetric=s.cycles;s.lastMetric=hp;
 r.fill=clamp01(1-(s.cycles+(hp>0?1-clamp01(hp/50.0f):0))*0.5f);return r;
}

// Original ELF 0x7df40. Core encounter -> hidden transition -> fish cycles.
inline PhaseResult morpheel_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 bool fish=x.phase!=0||x.action>=100;
 if(!fish&&x.health>=20)st.healthReady=true;
 if(st.phase==0){
  if(fish){
   if(x.cycles<=0&&x.hits<=0&&in.demo){r.fill=1;r.suppressed=true;return r;}
   st.phase=3;
  }else if(x.action>=1&&x.action<=5&&!in.demo)st.phase=1;
  else{r.fill=1;r.suppressed=true;return r;}
 }
 if(st.phase==1){
  r.started=true;
  if(fish||x.action==5){st.phase=2;st.timer=0;}
  else if(st.healthReady&&x.health<=0){
   int previous=st.timer++;
   if(previous>=60){st.phase=2;st.timer=0;}
   return r;
  }else{
   st.timer=0;r.fill=clamp01(st.healthReady?(x.health<0?1.0f:float(x.health)/30):1.0f);return r;
  }
 }
 if(st.phase==2){
  r.started=true;r.suppressed=true;r.fill=1;
  if(fish&&!in.demo)st.phase=3;
  return r;
 }
 if(st.phase==3){
  r.started=true;r.suppressed=in.demo!=0;
  int hits=x.hits>0&&x.hits<4?x.hits:0;
  int cycles=minimum(3,maximum(0,x.cycles));
  r.fill=clamp01(1.0f-float(cycles*4+hits)/12.0f);
  if(r.fill<=0)st.phase=4;
 }
 return r;
}

// Original ELF 0x7e4a0. Ice shell uses /7 here, unlike the /6 instantaneous
// metric. The transition waits 41 calls in a shell-break action, then refills.
inline PhaseResult blizzeta_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 if(st.phase==0){
  if(x.phase>=7)st.phase=3;
  else if(in.event||x.action==0||x.action==2||x.action==7){r.fill=1;r.suppressed=true;return r;}
  else st.phase=1;
 }
 if(st.phase==1){
  r.started=true;
  if(x.phase>=7){st.phase=2;st.timer=0;}
  else if(x.action==2||x.action==7){
   int previous=st.timer++;
   if(previous>=40){st.phase=2;st.timer=0;}
   return r;
  }else{st.timer=0;r.fill=clamp01(1.0f-float(x.phase)/7.0f);return r;}
 }
 if(st.phase==2){
  r.started=true;r.suppressed=true;r.fill=1;
  if(x.phase>=7&&x.action!=2&&x.action!=7&&!in.event)st.phase=3;
  return r;
 }
 if(st.phase==3){
  r.started=true;r.suppressed=in.event;
  if(x.action==9||x.hits>=3)st.phase=4;
  else r.fill=1.0f-float(minimum(3,x.hits))/3.0f;
 }
 return r;
}

// Original ELF 0x7e170; includes the hit already in progress while action==3.
inline PhaseResult stallord_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 bool hide=in.demo||(x.phase?(x.action==0||x.action==5):(in.intro||x.action==1))||in.event;
 if(hide)st.healthReady=true;
 int hits=minimum(3,x.hits);
 if(st.phase==0){
  if(x.phase)st.phase=3;
  else if(hide){r.fill=1;r.suppressed=true;return r;}
  else if(st.healthReady||hits>0||(!in.dead&&(x.action==2||(x.action>=4&&x.action<=7))))st.phase=1;
  else{r.fill=1;r.suppressed=true;return r;}
 }
 if(st.phase==1){
  r.started=true;
  if(!x.phase&&x.action==3){if(st.previous<0)st.previous=hits;}else st.previous=-1;
  int applied=hits+(st.previous>=0&&hits<=st.previous?1:0);
  if(!x.phase&&applied<3){r.fill=1-float(applied)/3;return r;}
  if(!x.phase){if(st.timer++>=60){st.phase=2;st.timer=0;}return r;}
  st.phase=2;st.timer=0;
 }
 if(st.phase==2){r.started=true;r.suppressed=true;r.fill=1;if(x.phase&&!hide)st.phase=3;return r;}
 if(st.phase==3){r.started=true;r.suppressed=hide;if(in.dead||x.health<=0)st.phase=4;else r.fill=clamp01(float(x.health)/1080);}
 return r;
}

// Original ELF 0x7e690. Armor removal gets its own 90-tick refill; the final
// sword phase reserves one third of the bar for the last 60 damage units.
inline PhaseResult darknut_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 if(st.phase==0){
  if(x.action>=9&&x.action<=13)st.phase=3;
  else if(x.action==8){st.phase=2;st.timer=0;}
  else if(x.action>=2&&x.action<=7&&!in.event)st.phase=1;
  else{r.fill=1;r.suppressed=true;return r;}
 }
 if(st.phase==1){
  r.started=true;r.suppressed=!in.lineOfSight;
  if(x.hits<=11&&!(x.action>=8&&x.action<=13)){r.fill=clamp01(1-float(x.hits)/12);return r;}
  st.phase=2;st.timer=0;
 }
 if(st.phase==2){
  r.started=true;r.suppressed=!in.lineOfSight;
  if(st.timer<90)++st.timer;
  if(st.timer>=90&&x.action>=9){st.phase=3;r.fill=1;}
  else r.fill=float(st.timer)/90<1?float(st.timer)/90:1;
  return r;
 }
 if(st.phase==3){
  r.started=true;r.suppressed=in.event||!in.lineOfSight;
  int limit=x.damageLimit>0?x.damageLimit:360;
  if(x.action==14||x.damage>=limit){st.phase=4;return r;}
  st.damagePeak=maximum(st.damagePeak,x.damage);
  int first=limit-60;
  r.fill=clamp01(st.damagePeak<=first?1-float(st.damagePeak)/first*(2.0f/3):
    (1-float(st.damagePeak-first)/60)*(1.0f/3));
 }
 return r;
}

// Original ELF 0x7ec20. Phase changes drain before refill. Final cycles have
// native budgets 600/400/200 and cannot make the displayed bar increase.
inline PhaseResult zant_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 if(st.phase==4||x.action==22){st.phase=4;return r;}
 if(st.phase==0){
  if(!x.phase||x.action==4){r.fill=1;r.suppressed=true;return r;}
  st.phase=x.phase==6?3:1;st.lastPhase=x.phase;st.fill=1;
 }
 if(st.phase==1&&st.lastPhase!=x.phase&&x.action!=23){
  st.lastPhase=x.phase;st.fill=1;st.phase=x.phase==6?3:1;
 }
 if(st.phase==2){
  r.started=true;r.suppressed=true;
  constexpr unsigned blocked=8650768;
  if(!x.phase||(x.action>=0&&x.action<=23&&(blocked&(1u<<x.action)))||st.lastPhase==x.phase)return r;
  st.lastPhase=x.phase;st.fill=1;st.phase=x.phase==6?3:1;return r;
 }
 if(st.phase==1){
  r.started=true;
  if(x.action==23||x.action==18){
   int previous=st.timer++;
   if(previous<=7){st.fill+=(0-st.fill)*0.4f;if(st.fill<0.01f)st.fill=0;r.fill=st.fill;return r;}
   st.fill=0;if(previous>=21){st.phase=2;r.suppressed=true;}return r;
  }
  st.timer=0;
  float next=float(minimum(280,maximum(0,x.health)))/280;
  if(next<0.04f)next=0.04f;if(next<st.fill)st.fill=next;r.fill=st.fill;return r;
 }
 if(st.phase==3){
  r.started=true;r.suppressed=x.action==18;
  if(x.hits>=3){st.fill=0;return r;}
  constexpr float budgets[]={600,400,200};
  // Native field is u8, so a negative phase-cycle is not a valid actor sample.
  if(x.hits<0)return r;
  float next=(2-x.hits+clamp01(float(maximum(0,x.health))/budgets[x.hits]))/3;
  if(next<st.fill)st.fill=next;r.fill=st.fill;return r;
 }
 r.fill=st.fill;return r;
}

// Original ELF 0x7e8f0; completed weak-point cycles plus the active hit fraction.
inline PhaseResult argorok_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 if(x.phase==2){
  if(x.action==3)st.healthReady=true;
  else if(st.healthReady){st.healthReady=false;if(st.previous<=2)++st.previous;}
 }
 bool transition=in.demo==1||in.demo==254||x.action==12;
 if(st.phase==0){
  if(x.phase==2)st.phase=3;
  else if(transition){st.phase=2;st.timer=0;}
  else if(in.event||in.demo>1||x.action<=0){r.fill=1;r.suppressed=true;return r;}
  else st.phase=1;
 }
 if(st.phase==1){
  r.started=true;
  if(x.phase==2||transition){st.phase=2;st.timer=0;}
  else if(x.hits<2){st.timer=0;r.fill=1-float(x.hits)*0.5f;return r;}
  else if(x.mode>=0&&x.mode<=55&&(UINT64_C(0x80000080080000)&(UINT64_C(1)<<x.mode))){
   if(st.timer++>=45){st.phase=2;st.timer=0;}return r;
  }else{st.timer=0;r.fill=0.5f;return r;}
 }
 if(st.phase==2){
  r.started=true;r.suppressed=true;r.fill=1;
  if(x.phase==2&&!in.event&&in.demo<=1&&x.action!=12)st.phase=3;
  return r;
 }
 if(st.phase==3){
  r.started=true;r.suppressed=in.event||in.demo>1;
  if(x.action==13||x.health<=0){st.phase=4;return r;}
  float fraction=st.healthReady?float(minimum(4,in.detail))*0.25f:0;
  r.fill=clamp01(1-(st.previous+fraction)/3);
 }
 return r;
}

// Original ELF 0x7f180. Intro/event gating differs during charge/down actions.
inline PhaseResult beast_ganon_phase(PhaseState&,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 if(x.action==9||x.cycles>5)return r;
 bool eventSuppress=!(x.action>=4&&x.action<=6)&&!in.intro;
 if(!x.action||(in.event&&eventSuppress&&x.cycles==0&&!in.demo)){r.fill=1;r.suppressed=true;return r;}
 r.started=true;r.fill=clamp01(float(x.health)/700);return r;
}

// Original ELF 0x7ef10. Horse/duel transition and three final down cycles.
inline PhaseResult ganondorf_phase(PhaseState& st,const PhaseInput& in){
 const auto&x=in.sample;PhaseResult r{};
 bool hide=in.event||in.demo;
 if(st.phase==3||x.action==22){st.phase=3;st.lastHealth=float(x.health);return r;}
 if(st.phase<=1&&x.action==6){st.phase=1;st.lastHealth=float(x.health);r.started=r.suppressed=true;r.fill=1;return r;}
 bool duel=x.action>=10&&x.action<=22;
 if((st.phase==0&&duel&&!x.phase)||(st.phase==1&&duel&&!hide)){
  st.phase=hide?1:2;st.fill=1;
 }
 if((st.phase==0||st.phase==2)&&st.lastHealth>=0&&st.lastHealth-0.5f>x.health)r.started=true;
 st.lastHealth=float(x.health);
 if(st.phase==1){r.started=r.suppressed=true;r.fill=1;return r;}
 r.suppressed=hide;
 if(st.phase==2){
  if(!hide)r.started=true;
  float next=0;
  if(!(x.cycles>=3&&x.action==21&&x.mode<3))next=1-float(minimum(2,x.cycles))/3-clamp01(1-float(maximum(0,x.health))/100)/3;
  if(st.fill<next){st.fill+=0.013333333656191826f;if(st.fill<=next){r.fill=st.fill;return r;}}
  st.fill=next;r.fill=next;return r;
 }
 r.fill=clamp01(float(maximum(0,x.health))/24);return r;
}
}
