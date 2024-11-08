/*
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_lif_network (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Assign unused outputs to 0
    assign uio_out[6:0] = 0;
    assign uio_oe = 8'hFF;  // Set all uio outputs as active high

    // Prevent warnings by marking unused inputs
    wire _unused = &{ena, uio_in, 1'b0};

    // Call the network module, which instantiates the neurons
    wire [4:0] spike_outputs;
    network lif_network (
        .clk(clk),
        .reset(~rst_n),             // Active-high reset
        .external_input(ui_in[4:0]), // Use the lower 5 bits of ui_in for inputs
        .spike_output(uio_out[7])    // Use uio_out[7] to output the final spike
    );

    // Assign the state of the output neuron to uo_out (for monitoring or testing)
    assign uo_out = {3'b000, spike_outputs};

endmodule
