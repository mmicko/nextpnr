/*
 *  nextpnr -- Next Generation Place and Route
 *
 *  Copyright (C) 2024  Miodrag Milanovic <micko@yosyshq.com>
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

#ifndef GATEMATE_EXTRA_DATA_H
#define GATEMATE_EXTRA_DATA_H

#include "nextpnr.h"

NEXTPNR_NAMESPACE_BEGIN

NPNR_PACKED_STRUCT(struct GateMatePipExtraDataPOD {
    uint8_t type;
    uint8_t plain;
    uint8_t value;
    uint16_t dummy;
});

enum PipExtra
{
    PIP_EXTRA_SB_BIG_Y1_MUX = 1,
    PIP_EXTRA_SB_BIG_Y2_MUX = 2,
    PIP_EXTRA_SB_BIG_Y3_MUX = 3,
    PIP_EXTRA_SB_BIG_Y4_MUX = 4,
    PIP_EXTRA_SB_BIG_YDIAG_MUX = 5,
    PIP_EXTRA_SB_SML_Y1_MUX = 6,
    PIP_EXTRA_SB_SML_Y2_MUX = 7,
    PIP_EXTRA_SB_SML_Y3_MUX = 8,
    PIP_EXTRA_SB_SML_Y4_MUX = 9,
    PIP_EXTRA_SB_SML_YDIAG_MUX = 10,
    PIP_EXTRA_SB_DRIVE = 11,
    PIP_EXTRA_INMUX_1 = 12,
    PIP_EXTRA_INMUX_2 = 13,
    PIP_EXTRA_INMUX_3 = 14,
    PIP_EXTRA_INMUX_4 = 15,
    PIP_EXTRA_OUTMUX_1 = 16,
    PIP_EXTRA_OUTMUX_4 = 19,
};

NEXTPNR_NAMESPACE_END

#endif
