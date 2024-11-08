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

    # Loop over all combinations of inputs from 0 to 10 for each neuron
    for neuron_input_1 in range(11):
        for neuron_input_2 in range(11):
            for neuron_input_3 in range(11):
                # Apply test currents to each neuron
                dut.uio_in.value = neuron_input_1               # Input for Neuron 1
                dut.ui_in.value = (neuron_input_2 << 4) | neuron_input_3  # Neuron 2 in upper bits, Neuron 3 in lower bits
                await ClockCycles(dut.clk, 5)  # Wait a few cycles for the neuron to process inputs

                # Read and print spike outputs
                spike_1 = int(dut.uio_out[4].value)
                spike_2 = int(dut.uio_out[5].value)
                spike_3 = int(dut.uio_out[6].value)
                final_spike = int(dut.uio_out[7].value)

                # Check for 'x' or 'z' in uo_out before converting to integer
                if "x" in dut.uo_out.value.binstr or "z" in dut.uo_out.value.binstr:
                    final_neuron_state = "undefined"
                else:
                    uo_out_value = int(dut.uo_out.value)
                    final_neuron_state = (uo_out_value >> 4) & 0xF  # Extract bits [7:4]

                # Log results
                dut._log.info(f"Test case - Neuron inputs: N1={neuron_input_1}, N2={neuron_input_2}, N3={neuron_input_3}")
                dut._log.info(f"Spike outputs: spike_1={spike_1}, spike_2={spike_2}, spike_3={spike_3}, final_spike={final_spike}")
                dut._log.info(f"Final neuron state (uo_out[7:4]): {final_neuron_state}")
    
    dut._log.info("Completed test for lif_neuron_network")
