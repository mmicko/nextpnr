/*
 *  nextpnr -- Next Generation Place and Route
 *
 *  Copyright (C) 2024  The Project Peppercorn Authors.
 *
 *  Permission to use, copy, modify, and/or distribute this software for any
 *  purpose with or without fee is hereby granted, provided that the above
 *  copyright notice and this permission notice appear in all copies.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 *  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 *  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 *  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 *  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 *  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 *  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */

#include "himbaechel_api.h"
#include "log.h"
#include "nextpnr.h"
#include "util.h"
#include "extra_data.h"

#include "himbaechel_helpers.h"

#include "gatemate.h"

#define GEN_INIT_CONSTIDS
#define HIMBAECHEL_CONSTIDS "uarch/gatemate/constids.inc"
#define HIMBAECHEL_GFXIDS "uarch/gatemate/gfxids.inc"
#define HIMBAECHEL_UARCH gatemate

#include "himbaechel_constids.h"
#include "himbaechel_gfxids.h"

NEXTPNR_NAMESPACE_BEGIN

GateMateImpl::~GateMateImpl(){};

void GateMateImpl::init_database(Arch *arch)
{
    const ArchArgs &args = arch->args;
    init_uarch_constids(arch);
    arch->load_chipdb(stringf("gatemate/chipdb-%s.bin", args.device.c_str()));
    arch->set_speed_grade("DEFAULT");
}

void GateMateImpl::init(Context *ctx)
{
    h.init(ctx);
    HimbaechelAPI::init(ctx);
}

void GateMateImpl::drawGroup(std::vector<GraphicElement> &g, GroupId group, Loc loc)
{
    IdString group_type = ctx->getGroupType(group);
    IdString group_name = ctx->getGroupName(group)[1];
    if (group_type == id_SB_BIG) {
        GraphicElement el;
        el.type = GraphicElement::TYPE_BOX;
        el.style = GraphicElement::STYLE_FRAME;

        el.x1 = loc.x + 0.05 + (group_name.index - id_SB_BIG_P01.index) * 0.04;
        el.x2 = el.x1 + 0.03;
        el.y1 = loc.y + 0.05 + (group_name.index - id_SB_BIG_P01.index) * 0.04;
        el.y2 = el.y1 - 0.03;
        g.push_back(el);
    }
    if (group_type == id_SB_SML) {
        GraphicElement el;
        el.type = GraphicElement::TYPE_BOX;
        el.style = GraphicElement::STYLE_FRAME;

        el.x1 = loc.x + 0.05 + (group_name.index - id_SB_SML_P01.index) * 0.03;
        el.x2 = el.x1 + 0.02;
        el.y1 = loc.y + 0.05 + (group_name.index - id_SB_SML_P01.index) * 0.03;
        el.y2 = el.y1 - 0.02;
        g.push_back(el);
    }
}
void GateMateImpl::drawBel(std::vector<GraphicElement> &g, GraphicElement::style_t style, IdString bel_type, Loc loc)
{
    GraphicElement el;
    el.type = GraphicElement::TYPE_BOX;
    el.style = style;
    switch (bel_type.index)
    {
        case id_CPE.index :
            el.x1 = loc.x + 0.70;
            el.x2 = el.x1 + 0.20;
            el.y1 = loc.y + 0.55;
            el.y2 = el.y1 + 0.40;
            g.push_back(el);
            break;
    }
}

void GateMateImpl::drawWire(std::vector<GraphicElement> &g, GraphicElement::style_t style, Loc loc, IdString wire_type,
                int32_t tilewire, IdString tile_type)
{
    GraphicElement el;
    el.type = GraphicElement::TYPE_LINE;
    el.style = style;
    switch (tile_type.index) {
        case id_CPE_BIG.index:
        case id_CPE_SML.index:
        case id_CPE.index:
            switch (wire_type.index) {
                case id_CPE_WIRE_L.index:
                    el.x1 = loc.x + 0.70 - 0.02;
                    el.x2 = el.x1 + 0.02;
                    el.y1 = loc.y + 0.90 - (tilewire - GFX_WIRE_CPE_IN1) * 0.02;
                    el.y2 = el.y1;
                    g.push_back(el);
                    break;
                case id_CPE_WIRE_R.index:
                    el.x1 = loc.x + 0.90;
                    el.x2 = el.x1 + 0.02;
                    el.y1 = loc.y + 0.90 - (tilewire - GFX_WIRE_CPE_OUT2 + 9) * 0.02;
                    el.y2 = el.y1;
                    g.push_back(el);
                    break;
                case id_CPE_WIRE_T.index:
                    el.x1 = loc.x + 0.75 + (tilewire - GFX_WIRE_CPE_COUTY1) * 0.02;
                    el.x2 = el.x1;
                    el.y1 = loc.y + 0.95;
                    el.y2 = el.y1 + 0.02;
                    g.push_back(el);
                    break;
                case id_CPE_WIRE_B.index:
                    el.x1 = loc.x + 0.75 + (tilewire - GFX_WIRE_CPE_CINY1) * 0.02;
                    el.x2 = el.x1;
                    el.y1 = loc.y + 0.55;
                    el.y2 = el.y1 - 0.02;
                    g.push_back(el);
                    break;    

            }
            break;
    }
}

struct GateMateArch : HimbaechelArch
{
    GateMateArch() : HimbaechelArch("gatemate"){};
    bool match_device(const std::string &device) override { return device.size() > 6 && device.substr(0, 6) == "CCGM1A"; }
    std::unique_ptr<HimbaechelAPI> create(const std::string &device, const dict<std::string, std::string> &args)
    {
        return std::make_unique<GateMateImpl>();
    }
} gateMateArch;

NEXTPNR_NAMESPACE_END
