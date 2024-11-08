import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_layered_neuron_network(dut):
    dut._log.info("Starting layered neuron network test")

    # Set up clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut._log.info("Reset completed")

    # Ramp-Up Test for ui_in
    for value in range(0, 2000, 10):  # Increment by 10 up to max 8-bit value
        dut.ui_in.value = value
        await ClockCycles(dut.clk, 5)

        # Print current input and output states, including each neuron's spike output
        dut._log.info(f"ui_in: {value}")
        dut._log.info(f"uo_out: {int(dut.uo_out.value)}")
        
        # Print individual spike outputs from uio_out bits
        dut._log.info(f"spike_1 (uio_out[4]): {int(dut.uio_out[4].value)}")
        dut._log.info(f"spike_2 (uio_out[5]): {int(dut.uio_out[5].value)}")
        dut._log.info(f"spike_3 (uio_out[6]): {int(dut.uio_out[6].value)}")
        dut._log.info(f"final spike (uio_out[7]): {int(dut.uio_out[7].value)}")

    # Threshold-Crossing Test
    threshold_values = [40, 50, 60]  # Adjust based on ramp-up test results
    for value in threshold_values:
        dut.ui_in.value = value
        await ClockCycles(dut.clk, 5)

        # Print current input and output states, including each neuron's spike output
        dut._log.info(f"Testing ui_in: {value}")
        dut._log.info(f"uo_out: {int(dut.uo_out.value)}")
        
        # Print individual spike outputs from uio_out bits
        dut._log.info(f"spike_1 (uio_out[4]): {int(dut.uio_out[4].value)}")
        dut._log.info(f"spike_2 (uio_out[5]): {int(dut.uio_out[5].value)}")
        dut._log.info(f"spike_3 (uio_out[6]): {int(dut.uio_out[6].value)}")
        dut._log.info(f"final spike (uio_out[7]): {int(dut.uio_out[7].value)}")
    
    dut._log.info("Layered neuron network test completed")
