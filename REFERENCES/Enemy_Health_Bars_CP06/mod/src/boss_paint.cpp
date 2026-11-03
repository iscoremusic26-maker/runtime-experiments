// BARS203 CP03 -- boss / mini-boss J2D painter: ported from Bars 1.1.1 boss_draw.cpp. Same recovered renderer, same pane
// manipulation of the HUD's magic-meter frame ornaments (saved and restored around the draw), same fonts. Differences: no
// native.h access hack (the 2.0.3 headers expose these members), boss_set_draw_options dropped (no new options in CP03),
// the draw state is passed in (owned by BossTracker) instead of a file-static.
#include <cstring>
#include "d/d_com_inf_game.h"
#include "d/d_meter2_draw.h"
#include "m_Do/m_Do_graphic.h"
#include "m_Do/m_Do_ext.h"
#include "d/d_pane_class.h"
#include "JSystem/J2DGraph/J2DOrthoGraph.h"
#include "JSystem/JUtility/JUTFont.h"
#include "boss_paint.h"
#include "reused/recovered/renderer.h"
namespace ehz {
namespace {
recovered::BossStyle drawOptions{};   // style 0 (wide), no offset: the Bars 1.1.1 defaults
bool drawing=false;
bool finite(float x){return x==x&&x<=3.402823466e38f&&x>=-3.402823466e38f;}
JUtility::TColor native(recovered::Color c){return JUtility::TColor(c.r,c.g,c.b,c.a);}
struct Context { J2DGrafContext* graph;JUTFont* font;J2DScreen* screen;CPaneMgr* panes[5];bool fontGX=false;unsigned screenIndex=0; };
struct GraphicGuard {
 J2DGrafContext& g;JUTFont* font;JUtility::TColor colors[4],fontColors[4];
 GraphicGuard(J2DGrafContext&graph,JUTFont*f):g(graph),font(f),colors{g.mColorTL,g.mColorTR,g.mColorBR,g.mColorBL}{
  if(font){fontColors[0]=font->mColor1;fontColors[1]=font->mColor2;fontColors[2]=font->mColor3;fontColors[3]=font->mColor4;}
 }
 ~GraphicGuard(){
  g.setColor(colors[0],colors[1],colors[2],colors[3]);
  if(font){font->mColor1=fontColors[0];font->mColor2=fontColors[1];font->mColor3=fontColors[2];font->mColor4=fontColors[3];}
  g.setup2D();
 }
};
struct SavedPane {
 float alpha,sx,sy;JGeometry::TBox2<float> bounds,global,clip;Mtx positionMtx,globalMtx;u8 paneAlpha,colorAlpha;
 void save(CPaneMgr*p){
  auto*n=p->getPanePtr();alpha=p->getAlphaRate();sx=n->getScaleX();sy=n->getScaleY();
  bounds=n->mBounds;global=n->mGlobalBounds;clip=n->mClipRect;paneAlpha=n->mAlpha;colorAlpha=n->mColorAlpha;
  memcpy(positionMtx,n->mPositionMtx,sizeof(positionMtx));memcpy(globalMtx,n->mGlobalMtx,sizeof(globalMtx));
 }
 void restoreLocal(CPaneMgr*p)const{
  auto*n=p->getPanePtr();n->mBounds=bounds;n->mGlobalBounds=global;n->mClipRect=clip;
  n->mScaleX=sx;n->mScaleY=sy;n->mAlpha=paneAlpha;n->mColorAlpha=colorAlpha;
  memcpy(n->mPositionMtx,positionMtx,sizeof(positionMtx));memcpy(n->mGlobalMtx,globalMtx,sizeof(globalMtx));
 }
};
struct PaneGuard {
 Context& c;SavedPane saved[5];
 PaneGuard(Context&ctx):c(ctx){for(int j=0;j<5;++j)saved[j].save(c.panes[j]);}
 ~PaneGuard(){
  for(int j:{0,3,4})c.panes[j]->scale(saved[j].sx,saved[j].sy);
  for(int j=0;j<5;++j)c.panes[j]->setAlphaRate(saved[j].alpha);
  for(int j:{1,2})c.panes[j]->resize(saved[j].bounds.getWidth(),saved[j].bounds.getHeight());
  for(int j=0;j<5;++j)saved[j].restoreLocal(c.panes[j]);
 }
};
void box(void*context,float x,float y,float w,float h,recovered::Color a,recovered::Color b,recovered::Color c,recovered::Color d){
 auto&ctx=*(Context*)context;ctx.graph->setColor(native(a),native(b),native(c),native(d));
 ctx.graph->fillBox(JGeometry::TBox2<float>(x,y,x+w,y+h));
}
void text(void*context,float x,float y,float w,float h,const char*s,recovered::Color a,recovered::Color b,bool visible){
 auto&ctx=*(Context*)context;if(!ctx.font||!s)return;
 if(!ctx.fontGX){ctx.font->setGX();ctx.fontGX=true;}
 const bool uniform=recovered::pack(a)==recovered::pack(b);
 if(uniform)ctx.font->setCharColor(native(a));else ctx.font->setGradColor(native(a),native(b));
 ctx.font->drawString_size_scale(x,y,w,h,s,(u32)strlen(s),visible);
 if(!uniform){ctx.graph->setup2D();ctx.fontGX=false;}
}
int font_width(void*p){return ((JUTFont*)p)->getWidth();}
uint8_t font_entry(void*p,signed char ch){JUTFont::TWidth e{};((JUTFont*)p)->getWidthEntry(ch,&e);return e.field_0x1;}
void screen(void*context,float x,float y,const recovered::OrnamentState&s){
 auto&c=*(Context*)context;
 // The preparatory hidden draw already ran to produce actual global bounds.
 // Consume its plan command once; do not draw it a second time.
 if(c.screenIndex++==0)return;
 c.panes[3]->setAlphaRate(s.alpha[3]);c.panes[4]->setAlphaRate(s.alpha[4]);
 c.graph->setup2D();c.screen->draw(x,y,c.graph);
}
void snapshot_panes(recovered::OrnamentState&s,Context&c){
 s.available=true;
 for(int j=0;j<5;++j){auto*p=c.panes[j]->getPanePtr();s.alpha[j]=c.panes[j]->getAlphaRate();
  s.scales[j][0]=p->getScaleX();s.scales[j][1]=p->getScaleY();
  s.bounds[j][0]=p->mBounds.i.x;s.bounds[j][1]=p->mBounds.i.y;s.bounds[j][2]=p->mBounds.f.x;s.bounds[j][3]=p->mBounds.f.y;
 }
 auto l=c.panes[3]->getPanePtr()->getGlbBounds(),r=c.panes[4]->getPanePtr()->getGlbBounds();
 float a[4]={l.i.x,l.i.y,l.f.x,l.f.y},b[4]={r.i.x,r.i.y,r.f.x,r.f.y};
 for(int j=0;j<4;++j){s.globalLeft[j]=a[j];s.globalRight[j]=b[j];}
}
bool bind_panes(Context&c,dMeter2Draw_c*h){
 if(!h||!h->mpKanteraScreen)return false;
 c.screen=h->mpKanteraScreen;c.panes[0]=h->mpMagicParent;c.panes[1]=h->mpMagicMeter;
 c.panes[2]=h->mpMagicBase;c.panes[3]=h->mpMagicFrameL;c.panes[4]=h->mpMagicFrameR;
 for(int j=0;j<5;++j){if(!c.panes[j]||!c.panes[j]->getPanePtr())return false;
  for(int k=0;k<j;++k)if(c.panes[j]==c.panes[k]||c.panes[j]->getPanePtr()==c.panes[k]->getPanePtr())return false;
 }
 return true;
}
}
void boss_paint(J2DGrafContext&g,const BossDrawState& snapshot,dMeter2Draw_c*h){
 // Snapshot this frame's POD before any renderer/native callbacks run.
 const BossDrawState state=snapshot;const auto options=drawOptions;
 if(drawing||!state.active||!finite(state.alpha)||state.alpha<.01f||!finite(state.fill)||!finite(state.trail))return;
 recovered::Viewport v{mDoGph_gInf_c::m_minXF,mDoGph_gInf_c::m_minYF,mDoGph_gInf_c::m_maxXF,mDoGph_gInf_c::m_maxYF,
  mDoGph_gInf_c::m_safeMinXF,mDoGph_gInf_c::m_safeMaxXF,mDoGph_gInf_c::m_safeMaxYF};
 if(!finite(v.minX)||!finite(v.minY)||!finite(v.maxX)||!finite(v.maxY)||!finite(v.safeMinX)||!finite(v.safeMaxX)||!finite(v.safeMaxY))return;
 drawing=true;struct ReentryGuard{~ReentryGuard(){drawing=false;}} reentry;
 Context c{&g,mDoExt_getRubyFont(),nullptr,{}};
 if(!c.font)c.font=mDoExt_getSubFont();if(!c.font)c.font=mDoExt_getMesgFont();
 GraphicGuard graphics(g,c.font);
 recovered::Output o{{&c,box,text},{c.font,font_width,font_entry,c.font!=nullptr},{},screen};
 // Pure renderer emits rectangles and native-font text; adornments wait until
 // their actual bounds have been resolved by the native screen draw.
 recovered::render(o,v,options,state.name,state.fill,state.trail,state.alpha);
 if(!bind_panes(c,h))return;
 PaneGuard panes(c);auto layout=recovered::bossLayout(v,options);
 float alpha=recovered::clamp01(state.alpha),scale=layout.thin?.62f:1.15f;
 c.panes[0]->setAlphaRate(alpha);c.panes[0]->scale(1,1);
 for(int j:{1,2}){c.panes[j]->setAlphaRate(0);c.panes[j]->resize(0,0);}
 for(int j:{3,4}){c.panes[j]->scale(scale,scale);c.panes[j]->setAlphaRate(0);}
 g.setup2D();c.screen->draw(0,0,&g);
 snapshot_panes(o.ornaments,c);
 recovered::ornaments(o,layout.x,layout.w,layout.y,layout.thin?((layout.y+5.1f)+1.7f-layout.y):10,
  alpha,scale,layout.thin?-27.f:0,layout.thin?-34.f:0,layout.thin?-9.f:0);
}
}
