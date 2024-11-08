import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_individual_neuron_spikes(dut):
    # Initialize the clock
    clock = Clock(dut.clk, 10, units="us")  # 100 kHz clock
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.ena.value = 1
    dut.rst_n.value = 0  # Active-low reset
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1  # Release reset
    dut._log.info("Reset completed")

    # Define input currents for each neuron to test edge cases around the threshold
    test_cases = [
        (0, 0, 0),  # Below threshold for all neurons
        (0,0,0),
        (8, 8, 8),  # At threshold for all neurons
        (10, 10, 10),  # Above threshold for all neurons
        (6, 4, 9),  # Mixed case around thresholds (testing weights 5, 4, and 3 respectively)
    ]

    for neuron_input_1, neuron_input_2, neuron_input_3 in test_cases:
        # Apply test currents to each neuron
        dut.uio_in.value = neuron_input_1               # Input for Neuron 1
        dut.ui_in.value = (neuron_input_2 << 4) | neuron_input_3  # Neuron 2 in upper bits, Neuron 3 in lower bits
        await ClockCycles(dut.clk, 5)  # Wait a few cycles for the neuron to process inputs

        # Read and print spike outputs
        spike_1 = int(dut.uio_out[4].value)
        spike_2 = int(dut.uio_out[5].value)
        spike_3 = int(dut.uio_out[6].value)
        final_spike = int(dut.uio_out[7].value)

        # Log results
        dut._log.info(f"Test case - Neuron inputs: N1={neuron_input_1}, N2={neuron_input_2}, N3={neuron_input_3}")
        dut._log.info(f"Spike outputs: spike_1={spike_1}, spike_2={spike_2}, spike_3={spike_3}, final_spike={final_spike}")

    dut._log.info("Completed test for individual neuron spikes")
