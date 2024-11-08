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

    # Test each combination of inputs for neuron input currents (4-bit values from 0 to 15)
    # Set test thresholds and weights:
    threshold = 8
    weights = [5, 4, 3]

    for neuron_input_1 in range(16):  # Test all values for neuron 1
        for neuron_input_2 in range(16):  # Test all values for neuron 2
            for neuron_input_3 in range(16):  # Test all values for neuron 3
                # Set inputs
                dut.uio_in.value = neuron_input_1
                dut.ui_in.value = (neuron_input_2 << 4) | neuron_input_3
                await ClockCycles(dut.clk, 5)  # Wait a few cycles for the neuron to process inputs

                # Log the current state
                dut._log.info(f"Testing with inputs: neuron_input_1={neuron_input_1}, "
                              f"neuron_input_2={neuron_input_2}, neuron_input_3={neuron_input_3}")
                
                # Read spike and state outputs
                spike_1 = int(dut.uio_out[4].value)
                spike_2 = int(dut.uio_out[5].value)
                spike_3 = int(dut.uio_out[6].value)
                final_spike = int(dut.uio_out[7].value)
                final_neuron_state = int(dut.uo_out[7:4].value)

                # Calculate expected output for the neuron inputs based on weights and thresholds
                # Spike expected when each neuron's input >= weight (threshold check)
                expected_spike_1 = 1 if neuron_input_1 >= weights[0] else 0
                expected_spike_2 = 1 if neuron_input_2 >= weights[1] else 0
                expected_spike_3 = 1 if neuron_input_3 >= weights[2] else 0
                expected_final_spike = 1 if (expected_spike_1 + expected_spike_2 + expected_spike_3) >= threshold else 0

                # Assert that the observed spikes match expected behavior
                assert spike_1 == expected_spike_1, f"Neuron 1 spike mismatch: got {spike_1}, expected {expected_spike_1}"
                assert spike_2 == expected_spike_2, f"Neuron 2 spike mismatch: got {spike_2}, expected {expected_spike_2}"
                assert spike_3 == expected_spike_3, f"Neuron 3 spike mismatch: got {spike_3}, expected {expected_spike_3}"
                assert final_spike == expected_final_spike, f"Final neuron spike mismatch: got {final_spike}, expected {expected_final_spike}"

                # Log expected vs. actual results
                dut._log.info(f"Expected spikes: spike_1={expected_spike_1}, spike_2={expected_spike_2}, "
                              f"spike_3={expected_spike_3}, final_spike={expected_final_spike}")
                dut._log.info(f"Actual spikes: spike_1={spike_1}, spike_2={spike_2}, "
                              f"spike_3={spike_3}, final_spike={final_spike}")
                dut._log.info(f"Final neuron state: {final_neuron_state}")
    
    dut._log.info("Completed test for all input cases in lif_neuron_network")
