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

    # Test each possible combination for the lower 4 bits (Neuron 3) and upper 4 bits (Neuron 2) of `ui_in`
    for neuron_2_input in range(16):  # Upper 4 bits (Neuron 2)
        for neuron_3_input in range(16):  # Lower 4 bits (Neuron 3)
            # Combine upper 4 bits for Neuron 2 and lower 4 bits for Neuron 3
            dut.ui_in.value = (neuron_2_input << 4) | neuron_3_input
            dut.uio_in.value = neuron_3_input  # Assuming uio_in provides input for Neuron 1
            await ClockCycles(dut.clk, 1)  # Apply for one cycle
            
            # Reset inputs after one cycle
            dut.ui_in.value = 0
            dut.uio_in.value = 0
            await ClockCycles(dut.clk, 5)  # Allow time for effects to propagate


    dut._log.info("Completed exhaustive test for lif_neuron_network")
