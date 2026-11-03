// J2D painter for normal bars: ported from Bars 1.1.1 normal_draw.cpp (same primitives, same recovered renderer).
#include <cstring>
#include "d/d_com_inf_game.h"
#include "m_Do/m_Do_ext.h"
#include "JSystem/J2DGraph/J2DOrthoGraph.h"
#include "JSystem/JUtility/JUTFont.h"
#include "normal_draw.h"
#include "reused/recovered/normal_renderer.h"

namespace ehz {
namespace {
struct DrawContext { JUTFont* font; J2DGrafContext* graph; bool fontGX = false; };
JUtility::TColor native(recovered::Color c) { return JUtility::TColor(c.r, c.g, c.b, c.a); }
void box(void*, float x, float y, float w, float h, recovered::Color a, recovered::Color, recovered::Color, recovered::Color) { J2DFillBox(x, y, w, h, native(a)); }
void frame(void*, float x, float y, float w, float h, recovered::Color c, uint8_t t) { J2DDrawFrame(x, y, w, h, native(c), t); }
void text(void* context, float x, float y, float w, float h, const char* s, recovered::Color a, recovered::Color b, bool flag) {
    auto& c = *static_cast<DrawContext*>(context);
    if (!c.font) return;
    if (!c.fontGX) { c.font->setGX(); c.fontGX = true; }
    if (recovered::pack(a) == recovered::pack(b)) c.font->setCharColor(native(a)); else c.font->setGradColor(native(a), native(b));
    c.font->drawString_size_scale(x, y, w, h, s, (u32)std::strlen(s), flag);
    if (recovered::pack(a) != recovered::pack(b)) { c.graph->setup2D(); c.fontGX = false; }
}
int width(void* p) { return static_cast<JUTFont*>(p)->getWidth(); }
uint8_t entry(void* p, signed char ch) { JUTFont::TWidth e{}; static_cast<JUTFont*>(p)->getWidthEntry(ch, &e); return e.field_0x1; }
}  // namespace

void normal_draw(J2DGrafContext& g, const NormalDrawState* states, unsigned count, bool showNumbers) {
    if (!count) return;
    DrawContext ctx{nullptr, &g};
    if (showNumbers) { ctx.font = mDoExt_getSubFont(); if (!ctx.font) ctx.font = mDoExt_getMesgFont(); }
    JUtility::TColor colors[4] = {g.mColorTL, g.mColorTR, g.mColorBR, g.mColorBL}, fontColors[4];
    if (ctx.font) { fontColors[0] = ctx.font->mColor1; fontColors[1] = ctx.font->mColor2; fontColors[2] = ctx.font->mColor3; fontColors[3] = ctx.font->mColor4; }
    NormalOutput out{{{&ctx, box, text}, {ctx.font, width, entry, ctx.font != nullptr}, {}, nullptr}, frame};
    for (unsigned n = 0; n < count && n < 256; ++n) normal_render(out, states[n], showNumbers);
    if (ctx.font) { ctx.font->mColor1 = fontColors[0]; ctx.font->mColor2 = fontColors[1]; ctx.font->mColor3 = fontColors[2]; ctx.font->mColor4 = fontColors[3]; }
    g.setColor(colors[0], colors[1], colors[2], colors[3]);
    g.setup2D();
}
}  // namespace ehz
