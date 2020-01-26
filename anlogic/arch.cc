/*
 *  nextpnr -- Next Generation Place and Route
 *
 *  Copyright (C) 2018  Clifford Wolf <clifford@symbioticeda.com>
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

#include <iostream>
#include <math.h>
#include "nextpnr.h"
#include "placer1.h"
#include "placer_heap.h"
#include "router1.h"
#include "util.h"

NEXTPNR_NAMESPACE_BEGIN

// ---------------------------------------------------------------

Arch::Arch(ArchArgs args) : chipName("generic"), args(args)
{
    // Dummy for empty decals
//    decal_graphics[IdString()];
}

void IdString::initialize_arch(const BaseCtx *ctx) {}

// ---------------------------------------------------------------

BelId Arch::getBelByName(IdString name) const
{
    return BelId();
}

IdString Arch::getBelName(BelId bel) const { return IdString(); }

Loc Arch::getBelLocation(BelId bel) const
{
    return Loc(0, 0, 0);
}

BelId Arch::getBelByLocation(Loc loc) const
{
    return BelId();
}

const std::vector<BelId> &Arch::getBelsByTile(int x, int y) const { return std::vector<BelId>(); }

bool Arch::getBelGlobalBuf(BelId bel) const { return false; }

uint32_t Arch::getBelChecksum(BelId bel) const
{
    // FIXME
    return 0;
}

void Arch::bindBel(BelId bel, CellInfo *cell, PlaceStrength strength)
{
}

void Arch::unbindBel(BelId bel)
{
}

bool Arch::checkBelAvail(BelId bel) const { return false; }

CellInfo *Arch::getBoundBelCell(BelId bel) const { return nullptr; }

CellInfo *Arch::getConflictingBelCell(BelId bel) const { return nullptr; }

const std::vector<BelId> &Arch::getBels() const { return std::vector<BelId>(); }

IdString Arch::getBelType(BelId bel) const { return IdString(); }

const std::map<IdString, std::string> &Arch::getBelAttrs(BelId bel) const { return std::map<IdString, std::string>(); }

WireId Arch::getBelPinWire(BelId bel, IdString pin) const
{
    return WireId();
}

PortType Arch::getBelPinType(BelId bel, IdString pin) const { return PortType(); }

std::vector<IdString> Arch::getBelPins(BelId bel) const
{
    std::vector<IdString> ret;
    return ret;
}

// ---------------------------------------------------------------

WireId Arch::getWireByName(IdString name) const
{
    return WireId();
}

IdString Arch::getWireName(WireId wire) const { return IdString(); }

IdString Arch::getWireType(WireId wire) const { return IdString(); }

const std::map<IdString, std::string> &Arch::getWireAttrs(WireId wire) const { return std::map<IdString, std::string>(); }

uint32_t Arch::getWireChecksum(WireId wire) const
{
    // FIXME
    return 0;
}

void Arch::bindWire(WireId wire, NetInfo *net, PlaceStrength strength)
{
}

void Arch::unbindWire(WireId wire)
{
}

bool Arch::checkWireAvail(WireId wire) const { return false; }

NetInfo *Arch::getBoundWireNet(WireId wire) const { return nullptr; }

NetInfo *Arch::getConflictingWireNet(WireId wire) const { return nullptr; }

const std::vector<BelPin> &Arch::getWireBelPins(WireId wire) const { return std::vector<BelPin>(); }

const std::vector<WireId> &Arch::getWires() const { return std::vector<WireId>(); }

// ---------------------------------------------------------------

PipId Arch::getPipByName(IdString name) const
{
    return PipId();
}

IdString Arch::getPipName(PipId pip) const { return IdString(); }

IdString Arch::getPipType(PipId pip) const { return IdString(); }

const std::map<IdString, std::string> &Arch::getPipAttrs(PipId pip) const { return std::map<IdString, std::string>(); }

uint32_t Arch::getPipChecksum(PipId wire) const
{
    // FIXME
    return 0;
}

void Arch::bindPip(PipId pip, NetInfo *net, PlaceStrength strength)
{
}

void Arch::unbindPip(PipId pip)
{
}

bool Arch::checkPipAvail(PipId pip) const { return false; }

NetInfo *Arch::getBoundPipNet(PipId pip) const { return nullptr; }

NetInfo *Arch::getConflictingPipNet(PipId pip) const { return nullptr; }

WireId Arch::getConflictingPipWire(PipId pip) const { return WireId(); }

const std::vector<PipId> &Arch::getPips() const { return std::vector<PipId>(); }

Loc Arch::getPipLocation(PipId pip) const { return Loc(); }

WireId Arch::getPipSrcWire(PipId pip) const { return WireId(); }

WireId Arch::getPipDstWire(PipId pip) const { return WireId(); }

DelayInfo Arch::getPipDelay(PipId pip) const { return DelayInfo(); }

const std::vector<PipId> &Arch::getPipsDownhill(WireId wire) const { return std::vector<PipId>(); }

const std::vector<PipId> &Arch::getPipsUphill(WireId wire) const { return std::vector<PipId>(); }

const std::vector<PipId> &Arch::getWireAliases(WireId wire) const { return std::vector<PipId>(); }

// ---------------------------------------------------------------

GroupId Arch::getGroupByName(IdString name) const { return GroupId(); }

IdString Arch::getGroupName(GroupId group) const { return IdString(); }

std::vector<GroupId> Arch::getGroups() const
{
    return std::vector<GroupId>();
}

const std::vector<BelId> &Arch::getGroupBels(GroupId group) const { return std::vector<BelId>(); }

const std::vector<WireId> &Arch::getGroupWires(GroupId group) const { return std::vector<WireId>(); }

const std::vector<PipId> &Arch::getGroupPips(GroupId group) const { return std::vector<PipId>(); }

const std::vector<GroupId> &Arch::getGroupGroups(GroupId group) const { return std::vector<GroupId>(); }

// ---------------------------------------------------------------

delay_t Arch::estimateDelay(WireId src, WireId dst) const
{
    return 0;
}

delay_t Arch::predictDelay(const NetInfo *net_info, const PortRef &sink) const
{
    return 0;
}

bool Arch::getBudgetOverride(const NetInfo *net_info, const PortRef &sink, delay_t &budget) const { return false; }

// ---------------------------------------------------------------

bool Arch::place()
{
    std::string placer = str_or_default(settings, id("placer"), defaultPlacer);
    if (placer == "heap") {
        bool have_iobuf_or_constr = false;
        for (auto cell : sorted(cells)) {
            CellInfo *ci = cell.second;
            if (ci->type == id("GENERIC_IOB") || ci->bel != BelId() || ci->attrs.count(id("BEL"))) {
                have_iobuf_or_constr = true;
                break;
            }
        }
        bool retVal;
        if (!have_iobuf_or_constr) {
            log_warning("Unable to use HeAP due to a lack of IO buffers or constrained cells as anchors; reverting to "
                        "SA.\n");
            retVal = placer1(getCtx(), Placer1Cfg(getCtx()));
        } else {
            PlacerHeapCfg cfg(getCtx());
            cfg.ioBufTypes.insert(id("GENERIC_IOB"));
            retVal = placer_heap(getCtx(), cfg);
        }
        getCtx()->settings[getCtx()->id("place")] = 1;
        archInfoToAttributes();
        return retVal;
    } else if (placer == "sa") {
        bool retVal = placer1(getCtx(), Placer1Cfg(getCtx()));
        getCtx()->settings[getCtx()->id("place")] = 1;
        archInfoToAttributes();
        return retVal;
    } else {
        log_error("Generic architecture does not support placer '%s'\n", placer.c_str());
    }
}

bool Arch::route()
{
    bool retVal = router1(getCtx(), Router1Cfg(getCtx()));
    getCtx()->settings[getCtx()->id("route")] = 1;
    archInfoToAttributes();
    return retVal;
}

// ---------------------------------------------------------------

const std::vector<GraphicElement> &Arch::getDecalGraphics(DecalId decal) const
{
    return std::vector<GraphicElement>();
}

DecalXY Arch::getBelDecal(BelId bel) const { return DecalXY(); }

DecalXY Arch::getWireDecal(WireId wire) const { return DecalXY(); }

DecalXY Arch::getPipDecal(PipId pip) const { return DecalXY(); }

DecalXY Arch::getGroupDecal(GroupId group) const { return DecalXY(); }

// ---------------------------------------------------------------

bool Arch::getCellDelay(const CellInfo *cell, IdString fromPort, IdString toPort, DelayInfo &delay) const
{
    return false;
}

// Get the port class, also setting clockPort if applicable
TimingPortClass Arch::getPortTimingClass(const CellInfo *cell, IdString port, int &clockInfoCount) const
{
    return TimingPortClass();
}

TimingClockingInfo Arch::getPortClockingInfo(const CellInfo *cell, IdString port, int index) const
{
    return TimingClockingInfo();
}

bool Arch::isValidBelForCell(CellInfo *cell, BelId bel) const
{
    return false;
}

bool Arch::isBelLocationValid(BelId bel) const
{
    return false;
}

#ifdef WITH_HEAP
const std::string Arch::defaultPlacer = "heap";
#else
const std::string Arch::defaultPlacer = "sa";
#endif

const std::vector<std::string> Arch::availablePlacers = {"sa",
#ifdef WITH_HEAP
                                                         "heap"
#endif
};
void Arch::assignArchInfo()
{
}

NEXTPNR_NAMESPACE_END
