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

    # Loop over all combinations for Neuron 1, Neuron 2, and Neuron 3 inputs
    for neuron_1_input in range(16):  # Neuron 1 (uio_in)
        for neuron_2_input in range(16):  # Neuron 2 (ui_in upper 4 bits)
            for neuron_3_input in range(16):  # Neuron 3 (ui_in lower 4 bits)
                # Set inputs for each neuron
                dut.uio_in.value = neuron_1_input  # Neuron 1 input
                dut.ui_in.value = (neuron_2_input << 4) | neuron_3_input  # Neuron 2 in upper 4 bits, Neuron 3 in lower 4 bits
                await ClockCycles(dut.clk, 1)  # Apply for one cycle
                
                # Reset inputs after one cycle
                dut.ui_in.value = 0
                dut.uio_in.value = 0
                await ClockCycles(dut.clk, 5)  # Allow time for effects to propagate

                

                

    dut._log.info("Completed exhaustive test for lif_neuron_network")
