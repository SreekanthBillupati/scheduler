from __future__ import annotations

import os
import random
from pathlib import Path
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb_tools.runner import get_runner


def is_onehot_or_zero(val):
    return val == 0 or (val & (val - 1)) == 0


def round_robin_model(req, last_grant, width=4):
    """
    Reference round-robin model
    """
    for offset in range(1, width + 1):
        idx = (last_grant + offset) % width
        if (req >> idx) & 1:
            return 1 << idx, idx
    return 0, last_grant


@cocotb.test()
async def round_robin_arbiter_test(dut):

    WIDTH = 4
    last_grant = -1  # before first grant

    # ----------------------------
    # Clock
    # ----------------------------
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start(start_high=True))

    # ----------------------------
    # Reset
    # ----------------------------
    dut.rst_n.value = 0
    dut.req_i.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    # ----------------------------
    # Main test loop
    # ----------------------------
    for cycle in range(32):
        req = random.randint(0, 0xF)
        dut.req_i.value = req

        await RisingEdge(dut.clk)

        gnt = int(dut.gnt_o.value)

        # ----------------------------
        # Check 1: one-hot or zero
        # ----------------------------
        assert is_onehot_or_zero(gnt), (
            f"[Cycle {cycle}] Grant not one-hot: gnt={gnt:04b}"
        )

        # ----------------------------
        # Check 2: grant must match request
        # ----------------------------
        assert (gnt & ~req) == 0, (
            f"[Cycle {cycle}] Grant without request: "
            f"req={req:04b} gnt={gnt:04b}"
        )

        # ----------------------------
        # Check 3: round-robin correctness
        # ----------------------------
        exp_gnt, new_last = round_robin_model(req, last_grant, WIDTH)

        assert gnt == exp_gnt, (
            f"[Cycle {cycle}] RR mismatch\n"
            f"  req = {req:04b}\n"
            f"  exp = {exp_gnt:04b}\n"
            f"  got = {gnt:04b}"
        )

        if gnt != 0:
            last_grant = new_last

        cocotb.log.info(
            f"Cycle {cycle:02d} | req={req:04b} | gnt={gnt:04b}"
        )

    cocotb.log.info("Round-robin scoreboard test PASSED ✅")


def test_scheduler_hidden_runner():
    """ 
    Pytest entry point:
    - Builds RTL
    - Runs Cocotb test
    """

    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path / "sources/priority_arbiter.v", proj_path / "sources/round_robin_arbiter.v"]
    #sources = [proj_path / "sources/priority_arbiter.v", proj_path / "sources/round_robin_arbiter.v"]
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="round_robin_arbiter",
        always=True,
    )

    runner.test(hdl_toplevel="round_robin_arbiter", test_module="test_scheduler_hidden")
