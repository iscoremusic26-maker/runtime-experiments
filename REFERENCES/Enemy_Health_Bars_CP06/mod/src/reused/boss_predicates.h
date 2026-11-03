#pragma once
#include "boss_phases.h"
namespace ehz {
inline bool has_visible_predicate(Boss k){
 switch(k){case Boss::Fyrus:case Boss::Stallord:case Boss::Armogohma:case Boss::BeastGanon:
 case Boss::DeathSword:case Boss::Ook:case Boss::PhantomZant:return true;default:return false;}
}
inline bool boss_visible_predicate(Boss k,const PhaseInput&i){
 const auto&x=i.sample;
 switch(k){
 case Boss::Fyrus:return x.health>0&&!i.demo&&uint16_t(x.action)<11;
 case Boss::Stallord:return !i.dead&&(x.phase||x.hits||(!i.demo&&!i.intro&&uint32_t(x.action)<=7&&((0xf4u>>x.action)&1)));
 case Boss::Armogohma:return x.hits>0||(!i.demo&&x.action!=0);
 case Boss::BeastGanon:return x.action!=0&&x.action!=9;
 case Boss::DeathSword:return x.action>=5&&x.action!=20;
 case Boss::Ook:return true;
 case Boss::PhantomZant:return x.health>=2&&(x.action&~4)!=1;
 default:return false;}
}
inline bool boss_dead_predicate(Boss k,const PhaseInput&i,int&gohmaTimer){
 switch(k){case Boss::Fyrus:return i.sample.action==12;
 case Boss::Armogohma:{int previous=gohmaTimer;gohmaTimer=i.sample.hits>=3?previous+1:0;return i.sample.hits>=3&&previous>=45;}
 case Boss::Dangoro:return i.dead;
 case Boss::PhantomZant:return i.detail>9||i.sample.action==5;
 default:return false;}
}
}
