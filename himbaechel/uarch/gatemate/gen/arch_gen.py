#
#  nextpnr -- Next Generation Place and Route
#
#  Copyright (C) 2024  The Project Peppercorn Authors.
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), "../../.."))
from himbaechel_dbgen.chip import *

PIP_EXTRA_SB_BIG_Y1_MUX = 1
PIP_EXTRA_SB_BIG_Y2_MUX = 2
PIP_EXTRA_SB_BIG_Y3_MUX = 3
PIP_EXTRA_SB_BIG_Y4_MUX = 4
PIP_EXTRA_SB_BIG_YDIAG_MUX = 5
PIP_EXTRA_SB_SML_Y1_MUX = 6
PIP_EXTRA_SB_SML_Y2_MUX = 7
PIP_EXTRA_SB_SML_Y3_MUX = 8
PIP_EXTRA_SB_SML_Y4_MUX = 9
PIP_EXTRA_SB_SML_YDIAG_MUX = 10
PIP_EXTRA_SB_DRIVE = 11
PIP_EXTRA_INMUX_1 = 12
PIP_EXTRA_INMUX_2 = 13
PIP_EXTRA_INMUX_3 = 14
PIP_EXTRA_INMUX_4 = 15
PIP_EXTRA_OUTMUX_1 = 16
PIP_EXTRA_OUTMUX_4 = 19

@dataclass
class PipExtraData(BBAStruct):
    data_type: int = 0
    plain: int = 0
    value: int = 0

    def serialise_lists(self, context: str, bba: BBAWriter):
        pass
    def serialise(self, context: str, bba: BBAWriter):
        bba.u8(self.data_type)
        bba.u8(self.plain)
        bba.u8(self.value)
        bba.u8(0) # dummy

# Grid size including IOBs at edges
X = 80 + 2
Y = 64 + 2

CPE_PINS = {
    "RAM_I1" : PinType.INPUT,
    "RAM_I2" : PinType.INPUT,
    "IN1" : PinType.INPUT,
    "IN2" : PinType.INPUT,
    "IN3" : PinType.INPUT,
    "IN4" : PinType.INPUT,
    "IN5" : PinType.INPUT,
    "IN6" : PinType.INPUT,
    "IN7" : PinType.INPUT,
    "IN8" : PinType.INPUT,
    "CLK" : PinType.INPUT,
    "EN" : PinType.INPUT,
    "SR" : PinType.INPUT,
    "CINX" : PinType.INPUT,
    "PINX" : PinType.INPUT,
    "CINY1" : PinType.INPUT,
    "PINY1" : PinType.INPUT,
    "CINY2" : PinType.INPUT,
    "PINY2" : PinType.INPUT,
    "OUT1" : PinType.OUTPUT,
    "OUT2" : PinType.OUTPUT,
    "RAM_O1" : PinType.OUTPUT,
    "RAM_O2" : PinType.OUTPUT,
    "COUTX" : PinType.OUTPUT,
    "POUTX" : PinType.OUTPUT,
    "COUTY1" : PinType.OUTPUT,
    "POUTY1" : PinType.OUTPUT,
    "COUTY2" : PinType.OUTPUT,
    "POUTY2" : PinType.OUTPUT
}

def create_cpe(tt, z):
    cpe = tt.create_bel(f"CPE{z}", "CPE", z)    
    for pin_name,pin_type in CPE_PINS.items():
        tt.create_wire(name=f"CPE_{z}.{pin_name}", type="BEL_PIN_WIRE")
        tt.add_bel_pin(cpe, pin_name, f"CPE_{z}.{pin_name}", pin_type)

def create_inmux(tt, z, p):
    for i in range(8):
        tt.create_wire(f"INMUX_{z}.P{p+1}.D{i}", type="INMUX_WIRE")
    tt.create_wire(f"INMUX_{z}.P{p+1}.Y", type="INMUX_WIRE")

    for i in range(8):
        pp = tt.create_pip(f"INMUX_{z}.P{p+1}.D{i}", f"INMUX_{z}.P{p+1}.Y")
        pp.extra_data = PipExtraData(PIP_EXTRA_INMUX_1 + z, p, i)

def create_outmux(tt, z, p):
    # TODO: Y is inverted
    for i in range(4):
        tt.create_wire(f"OUTMUX_{z}.P{p+1}.D{i}", type="OUTMUX_WIRE")
    tt.create_wire(f"OUTMUX_{z}.P{p+1}.Y", type="OUTMUX_WIRE")
    
    for i in range(4):
        pp = tt.create_pip(f"OUTMUX_{z}.P{p+1}.D{i}", f"OUTMUX_{z}.P{p+1}.Y")
        pp.extra_data = PipExtraData(PIP_EXTRA_OUTMUX_1 + z, p, i)

def create_sb_big(tt, p):
    tt.create_wire(f"SB_BIG.P{p+1}.D0", type="SB_BIG_WIRE")
    for i in range(4):
        tt.create_wire(f"SB_BIG.P{p+1}.D2_{i+1}", type="SB_BIG_WIRE")
        tt.create_wire(f"SB_BIG.P{p+1}.D3_{i+1}", type="SB_BIG_WIRE")
        tt.create_wire(f"SB_BIG.P{p+1}.D4_{i+1}", type="SB_BIG_WIRE")
        tt.create_wire(f"SB_BIG.P{p+1}.D5_{i+1}", type="SB_BIG_WIRE")
        tt.create_wire(f"SB_BIG.P{p+1}.D6_{i+1}", type="SB_BIG_WIRE")
        tt.create_wire(f"SB_BIG.P{p+1}.D7_{i+1}", type="SB_BIG_WIRE")

        tt.create_wire(f"SB_BIG.P{p+1}.Y{i+1}", type="SB_BIG_WIRE")
        tt.create_wire(f"SB_BIG.P{p+1}.Y{i+1}int", type="SB_BIG_WIRE_INTERNAL")
    tt.create_wire(f"SB_BIG.P{p+1}.YDIAG", type="SB_BIG_WIRE")
    tt.create_wire(f"SB_BIG.P{p+1}.YDIAGint", type="SB_BIG_WIRE_INTERNAL")
    tt.create_wire(f"SB_BIG.P{p+1}.X34", type="SB_BIG_WIRE")
    tt.create_wire(f"SB_BIG.P{p+1}.X14", type="SB_BIG_WIRE")
    tt.create_wire(f"SB_BIG.P{p+1}.X12", type="SB_BIG_WIRE")
    tt.create_wire(f"SB_BIG.P{p+1}.X23", type="SB_BIG_WIRE")


    # internal Y wire to output Y wire
    tt.create_pip(f"SB_BIG.P{p+1}.YDIAGint", f"SB_BIG.P{p+1}.YDIAG")
    for i in range(4):
        tt.create_pip(f"SB_BIG.P{p+1}.Y{i+1}int", f"SB_BIG.P{p+1}.Y{i+1}")

    # Per Y output mux
    for i in range(4):
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D0", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 0)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.YDIAGint", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 1)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D2_{i+1}", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 2)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D3_{i+1}", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 3)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D4_{i+1}", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 4)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D5_{i+1}", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 5)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D6_{i+1}", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 6)
        pp = tt.create_pip(f"SB_BIG.P{p+1}.D7_{i+1}", f"SB_BIG.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_Y1_MUX + i, p, 7)

    # YDIAG output mux
    pp = tt.create_pip(f"SB_BIG.P{p+1}.Y1int", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 0)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.Y2int", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 1)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.Y3int", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 2)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.Y4int", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 3)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.X34", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 4)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.X14", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 5)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.X12", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 6)
    pp = tt.create_pip(f"SB_BIG.P{p+1}.X23", f"SB_BIG.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_BIG_YDIAG_MUX, p, 7)

def create_sb_sml(tt, p):
    tt.create_wire(f"SB_SML.P{p+1}.D0", type="SB_SML_WIRE")
    for i in range(4):
        tt.create_wire(f"SB_SML.P{p+1}.D2_{i+1}", type="SB_SML_WIRE")
        tt.create_wire(f"SB_SML.P{p+1}.D3_{i+1}", type="SB_SML_WIRE")

        tt.create_wire(f"SB_SML.P{p+1}.Y{i+1}", type="SB_SML_WIRE")
        tt.create_wire(f"SB_SML.P{p+1}.Y{i+1}int", type="SB_SML_WIRE_INTERNAL")
    tt.create_wire(f"SB_SML.P{p+1}.YDIAG", type="SB_SML_WIRE")
    tt.create_wire(f"SB_SML.P{p+1}.YDIAGint", type="SB_SML_WIRE_INTERNAL")
    tt.create_wire(f"SB_SML.P{p+1}.X34", type="SB_SML_WIRE")
    tt.create_wire(f"SB_SML.P{p+1}.X14", type="SB_SML_WIRE")
    tt.create_wire(f"SB_SML.P{p+1}.X12", type="SB_SML_WIRE")
    tt.create_wire(f"SB_SML.P{p+1}.X23", type="SB_SML_WIRE")

    # internal Y wire to output Y wire
    tt.create_pip(f"SB_SML.P{p+1}.YDIAGint", f"SB_SML.P{p+1}.YDIAG")
    for i in range(4):
        tt.create_pip(f"SB_SML.P{p+1}.Y{i+1}int", f"SB_SML.P{p+1}.Y{i+1}")

    # Per Y output mux
    for i in range(4):
        pp = tt.create_pip(f"SB_SML.P{p+1}.D0", f"SB_SML.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_Y1_MUX + i, p, 0)
        pp = tt.create_pip(f"SB_SML.P{p+1}.YDIAGint", f"SB_SML.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_Y1_MUX + i, p, 1)
        pp = tt.create_pip(f"SB_SML.P{p+1}.D2_{i+1}", f"SB_SML.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_Y1_MUX + i, p, 2)
        pp = tt.create_pip(f"SB_SML.P{p+1}.D3_{i+1}", f"SB_SML.P{p+1}.Y{i+1}int")
        pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_Y1_MUX + i, p, 3)

    # YDIAG output mux
    pp = tt.create_pip(f"SB_SML.P{p+1}.Y1int", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 0)
    pp = tt.create_pip(f"SB_SML.P{p+1}.Y2int", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 1)
    pp = tt.create_pip(f"SB_SML.P{p+1}.Y3int", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 2)
    pp = tt.create_pip(f"SB_SML.P{p+1}.Y4int", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 3)
    pp = tt.create_pip(f"SB_SML.P{p+1}.X34", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 4)
    pp = tt.create_pip(f"SB_SML.P{p+1}.X14", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 5)
    pp = tt.create_pip(f"SB_SML.P{p+1}.X12", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 6)
    pp = tt.create_pip(f"SB_SML.P{p+1}.X23", f"SB_SML.P{p+1}.YDIAGint")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_SML_YDIAG_MUX, p, 7)

def create_sb_drive(tt, p, d):
    tt.create_wire(f"SB_DRIVE.P{p+1}.D{d}.IN", type="SB_DRIVE_WIRE")
    tt.create_wire(f"SB_DRIVE.P{p+1}.D{d}.OUT", type="SB_DRIVE_WIRE")
    pp = tt.create_pip(f"SB_DRIVE.P{p+1}.D{d}.IN", f"SB_DRIVE.P{p+1}.D{d}.OUT")
    pp.extra_data = PipExtraData(PIP_EXTRA_SB_DRIVE, p, d)

def create_inmux_to_cpe(tt, z):
    tt.create_pip(f"INMUX_{z}.P1.Y", f"CPE_{z}.IN1")
    tt.create_pip(f"INMUX_{z}.P2.Y", f"CPE_{z}.IN2")
    tt.create_pip(f"INMUX_{z}.P3.Y", f"CPE_{z}.IN3")
    tt.create_pip(f"INMUX_{z}.P4.Y", f"CPE_{z}.IN4")
    tt.create_pip(f"INMUX_{z}.P5.Y", f"CPE_{z}.IN5")
    tt.create_pip(f"INMUX_{z}.P6.Y", f"CPE_{z}.IN6")
    tt.create_pip(f"INMUX_{z}.P7.Y", f"CPE_{z}.IN7")
    tt.create_pip(f"INMUX_{z}.P8.Y", f"CPE_{z}.IN8")
    tt.create_pip(f"INMUX_{z}.P9.Y", f"CPE_{z}.CLK")
    tt.create_pip(f"INMUX_{z}.P10.Y", f"CPE_{z}.EN")
    tt.create_pip(f"INMUX_{z}.P11.Y", f"CPE_{z}.SR")
    # TODO output from plain 12

def create_logic_tiletype(chip: Chip):
    tt = chip.create_tile_type("LOGIC")

    # create switch boxes
    for p in range(12):
        create_sb_big(tt, p)

    for p in range(12):
        create_sb_sml(tt, p)

    for d in range(4):
        for p in range(12):
            create_sb_drive(tt, p, d)

    # create logic cells
    for i in range(4):
        create_cpe(tt, i)
        for p in range(12):
            create_inmux(tt, i, p)
        create_inmux_to_cpe(tt, i)

    # 1st OUTMUX group
    for p in range(4):
        create_outmux(tt, 0, p + 8)

    tt.create_pip("CPE_0.OUT2", "OUTMUX_0.P9.D0") # x1y1
    tt.create_pip("CPE_1.OUT2", "OUTMUX_0.P9.D1") # x1y2
    tt.create_pip("CPE_2.OUT1", "OUTMUX_0.P9.D2") # x2y1
    tt.create_pip("CPE_3.OUT1", "OUTMUX_0.P9.D3") # x2y2

    tt.create_pip("CPE_0.OUT1", "OUTMUX_0.P10.D0") # x1y1
    tt.create_pip("CPE_1.OUT1", "OUTMUX_0.P10.D1") # x1y2
    tt.create_pip("CPE_2.OUT2", "OUTMUX_0.P10.D2") # x2y1
    tt.create_pip("CPE_3.OUT2", "OUTMUX_0.P10.D3") # x2y2

    tt.create_pip("CPE_0.OUT2", "OUTMUX_0.P11.D0") # x1y1
    tt.create_pip("CPE_1.OUT2", "OUTMUX_0.P11.D1") # x1y2
    tt.create_pip("CPE_2.OUT1", "OUTMUX_0.P11.D2") # x2y1
    tt.create_pip("CPE_3.OUT1", "OUTMUX_0.P11.D3") # x2y2

    tt.create_pip("CPE_0.OUT1", "OUTMUX_0.P12.D0") # x1y1
    tt.create_pip("CPE_1.OUT1", "OUTMUX_0.P12.D1") # x1y2
    tt.create_pip("CPE_2.OUT2", "OUTMUX_0.P12.D2") # x2y1
    tt.create_pip("CPE_3.OUT2", "OUTMUX_0.P12.D3") # x2y2

    # 2nd OUTMUX group
    for p in range(4):
        create_outmux(tt, 3, p + 8)

    tt.create_pip("CPE_0.OUT1", "OUTMUX_3.P9.D0") # x1y1
    tt.create_pip("CPE_1.OUT1", "OUTMUX_3.P9.D1") # x1y2
    tt.create_pip("CPE_2.OUT2", "OUTMUX_3.P9.D2") # x2y1
    tt.create_pip("CPE_3.OUT2", "OUTMUX_3.P9.D3") # x2y2

    tt.create_pip("CPE_0.OUT2", "OUTMUX_3.P10.D0") # x1y1
    tt.create_pip("CPE_1.OUT2", "OUTMUX_3.P10.D1") # x1y2
    tt.create_pip("CPE_2.OUT1", "OUTMUX_3.P10.D2") # x2y1
    tt.create_pip("CPE_3.OUT1", "OUTMUX_3.P10.D3") # x2y2

    tt.create_pip("CPE_0.OUT1", "OUTMUX_3.P11.D0") # x1y1
    tt.create_pip("CPE_1.OUT1", "OUTMUX_3.P11.D1") # x1y2
    tt.create_pip("CPE_2.OUT2", "OUTMUX_3.P11.D2") # x2y1
    tt.create_pip("CPE_3.OUT2", "OUTMUX_3.P11.D3") # x2y2

    tt.create_pip("CPE_0.OUT2", "OUTMUX_3.P12.D0") # x1y1
    tt.create_pip("CPE_1.OUT2", "OUTMUX_3.P12.D1") # x1y2
    tt.create_pip("CPE_2.OUT1", "OUTMUX_3.P12.D2") # x2y1
    tt.create_pip("CPE_3.OUT1", "OUTMUX_3.P12.D3") # x2y2

    # SB_BIG input D0
    tt.create_pip("CPE_0.OUT2", "SB_BIG.P1.D0") # x1y1
    tt.create_pip("CPE_1.OUT1", "SB_BIG.P2.D0") # x1y2
    tt.create_pip("CPE_2.OUT2", "SB_BIG.P3.D0") # x2y1
    tt.create_pip("CPE_3.OUT1", "SB_BIG.P4.D0") # x2y2
    tt.create_pip("CPE_0.OUT1", "SB_BIG.P5.D0") # x1y1
    tt.create_pip("CPE_1.OUT2", "SB_BIG.P6.D0") # x1y2
    tt.create_pip("CPE_2.OUT1", "SB_BIG.P7.D0") # x2y1
    tt.create_pip("CPE_3.OUT2", "SB_BIG.P8.D0") # x2y2    
    tt.create_pip("OUTMUX_0.P9.Y", "SB_BIG.P9.D0")
    tt.create_pip("OUTMUX_0.P10.Y", "SB_BIG.P10.D0")
    tt.create_pip("OUTMUX_0.P11.Y", "SB_BIG.P11.D0")
    tt.create_pip("OUTMUX_0.P12.Y", "SB_BIG.P12.D0")

    # SB_SML input D0
    tt.create_pip("CPE_0.OUT1", "SB_SML.P1.D0") # x1y1
    tt.create_pip("CPE_1.OUT2", "SB_SML.P2.D0") # x1y2
    tt.create_pip("CPE_2.OUT1", "SB_SML.P3.D0") # x2y1
    tt.create_pip("CPE_3.OUT2", "SB_SML.P4.D0") # x2y2
    tt.create_pip("CPE_0.OUT2", "SB_SML.P5.D0") # x1y1
    tt.create_pip("CPE_1.OUT1", "SB_SML.P6.D0") # x1y2
    tt.create_pip("CPE_2.OUT2", "SB_SML.P7.D0") # x2y1
    tt.create_pip("CPE_3.OUT1", "SB_SML.P8.D0") # x2y2    
    tt.create_pip("OUTMUX_3.P9.Y", "SB_SML.P9.D0")
    tt.create_pip("OUTMUX_3.P10.Y", "SB_SML.P10.D0")
    tt.create_pip("OUTMUX_3.P11.Y", "SB_SML.P11.D0")
    tt.create_pip("OUTMUX_3.P12.Y", "SB_SML.P12.D0")

    return tt

def create_edge_tiletype(ch, side):
    tt = ch.create_tile_type(f"EDGE_{side}")
    return tt

def is_corner(x, y):
    return ((x == 0) or (x == (X-1))) and ((y == 0) or (y == (Y-1)))

def set_timings(ch):
    speed = "DEFAULT"
    tmg = ch.set_speed_grades([speed])

def cpe_to_xy_name(x,y, port):
    x_tile = (x-1) // 2 + 1
    y_tile = (y-1) // 2 + 1
    index = (((x-1) & 1)* 2) + ((y-1) & 1)
    return NodeWire(x_tile, y_tile, f"CPE_{index}.{port}")

def create_nodes(ch):
    for x in range(1,161):
        for y in range(1,128):
            node = [cpe_to_xy_name(x,y,"COUTY1"), cpe_to_xy_name(x,y+1,"CINY1")]
            ch.add_node(node)
            node = [cpe_to_xy_name(x,y,"COUTY2"), cpe_to_xy_name(x,y+1,"CINY2")]
            ch.add_node(node)
            node = [cpe_to_xy_name(x,y,"POUTY1"), cpe_to_xy_name(x,y+1,"PINY1")]
            ch.add_node(node)
            node = [cpe_to_xy_name(x,y,"POUTY2"), cpe_to_xy_name(x,y+1,"PINY2")]
            ch.add_node(node)

    for x in range(1,160):
        for y in range(1,129):
            node = [cpe_to_xy_name(x,y,"COUTX"), cpe_to_xy_name(x+1,y,"CINX")]
            ch.add_node(node)
            node = [cpe_to_xy_name(x,y,"POUTX"), cpe_to_xy_name(x+1,y,"PINX")]
            ch.add_node(node)

def main():
    ch = Chip("gatemate", "CCGM1A1", X, Y)
    # Init constant ids
    ch.strs.read_constids(path.join(path.dirname(__file__), "..", "constids.inc"))
    ch.read_gfxids(path.join(path.dirname(__file__), "..", "gfxids.inc"))
    logic = create_logic_tiletype(ch)
    #io = create_io_tiletype(ch)
    #bram = create_bram_tiletype(ch)
    create_edge_tiletype(ch, "B")
    create_edge_tiletype(ch, "T")
    create_edge_tiletype(ch, "L")
    create_edge_tiletype(ch, "R")
    # Setup tile grid
    for x in range(X):
        for y in range(Y):
            if y == 0:
                ch.set_tile_type(x, y, "EDGE_B")
            elif x == 0:
                ch.set_tile_type(x, y, "EDGE_L")
            elif y == Y - 1:
                ch.set_tile_type(x, y, "EDGE_T")
            elif x == X - 1:
                ch.set_tile_type(x, y, "EDGE_R")
            else:
                ch.set_tile_type(x, y, "LOGIC")
    # Create nodes between tiles
    create_nodes(ch)
    set_timings(ch)
    ch.write_bba(sys.argv[1])

if __name__ == '__main__':
    main()
