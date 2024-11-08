import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_single_neuron(dut):
    dut._log.info("Starting single neuron test for tt_um_lif_network_MR")

    # Set up the clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0  # Active-low reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1  # Release reset
    dut._log.info("Reset completed")

    # Define test values for ui_in
    test_values = [5, 10, 15, 20, 25, 30]  # Modify this as needed to test spike thresholds

    # Apply test values to ui_in and monitor state and spike output
    for value in test_values:
        dut.ui_in.value = value
        await ClockCycles(dut.clk, 5)  # Wait a few cycles for the neuron to process the input

        # Print current input, neuron state, and spike output
        dut._log.info(f"ui_in: {value}")
        dut._log.info(f"Neuron state (uio_out[4:0]): {int(dut.uio_out.value & 0x1F)}")  # Extracting bits [4:0]
        dut._log.info(f"Spike output (uio_out[7]): {int(dut.uio_out[7].value)}")

    dut._log.info("Single neuron test completed")
