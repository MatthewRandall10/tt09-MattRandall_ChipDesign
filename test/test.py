import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    # Logging
    dut._log.info("Starting test for tt_um_lif")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Applying reset")
    dut.ena.value = 1        # Enable the design
    dut.ui_in.value = 0      # Initialize input to zero
    dut.uio_in.value = 0     # Set unused input to zero
    dut.rst_n.value = 0      # Apply reset (active-low)
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1      # Release reset

    dut._log.info("Beginning test sequence")

    # Define threshold for testing
    threshold = 10570  # Adjust based on your Verilog module threshold

    # Test inputs: Apply various values to ui_in and check the output on uo_out and uio_out[7]
    test_values = [10570, 12000, 14000, 15000, 16000]  # Extended test values

    for value in test_values:
        dut.ui_in.value = value            # Set input value
        await ClockCycles(dut.clk, 5)      # Wait a few cycles for output stabilization

        # Log the current output values and debug info for accumulation
        dut._log.info(f"ui_in: {value}, uo_out: {int(dut.uo_out.value)}, spike: {int(dut.uio_out[7].value)}")

        # Additional debugging logs for internal signal (if accessible)
        # dut._log.info(f"input_current_output: {int(dut.lif_net.input_current_output.value)}")

        # Assertion: Check spike behavior
        if value >= threshold:
            assert dut.uio_out[7].value == 1, f"Expected spike for input {value} (threshold: {threshold})"
        else:
            assert dut.uio_out[7].value == 0, f"Expected no spike for input {value} (threshold: {threshold})"

    dut._log.info("Test sequence completed successfully")
