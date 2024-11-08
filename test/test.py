import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_lif_neuron_network(dut):
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="us")  # 100 kHz clock
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.ena.value = 1
    dut.rst_n.value = 0  # Active-low reset
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1  # Release reset
    dut._log.info("Reset completed")

    # Loop over input values from 0 to 10 and apply them to ui_in
    for input_value in range(11):
        # Set the same input value for all neurons via ui_in
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 5)  # Wait a few cycles for processing

        # Read and print spike outputs
        spike_1 = int(dut.uio_out[4].value)
        spike_2 = int(dut.uio_out[5].value)
        spike_3 = int(dut.uio_out[6].value)
        final_spike = int(dut.uio_out[7].value)

        # Check for undefined bits in uo_out and handle them
        if "x" in dut.uo_out.value.binstr or "z" in dut.uo_out.value.binstr:
            final_neuron_state = "undefined"
        else:
            uo_out_value = int(dut.uo_out.value)
            final_neuron_state = (uo_out_value >> 4) & 0xF  # Extract bits [7:4]

        # Log results
        dut._log.info(f"Test case - ui_in: {input_value}")
        dut._log.info(f"Spike outputs: spike_1={spike_1}, spike_2={spike_2}, spike_3={spike_3}, final_spike={final_spike}")
        dut._log.info(f"Final neuron state (uo_out[7:4]): {final_neuron_state}")

    dut._log.info("Completed test for lif_neuron_network")
