// SPDX-License-Identifier: Apache-2.0

`default_nettype none

module tt_um_lif_network_MR (
    input  wire [7:0] ui_in,     // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,       // always 1 when the design is powered, so you can ignore it
    input  wire       clk,       // clock
    input  wire       rst_n      // reset_n - low to reset
);

    // Assign unused outputs to 0
    assign uio_out[6:0] = 0;
    assign uio_oe = 8'hFF;       // Set all uio outputs as active high

    // Prevent warnings by marking unused inputs
    wire _unused = &{ena, uio_in, 1'b0};

    // Internal wires for spike outputs from neurons in the network
    wire spike_out_1, spike_out_2, spike_out_3, spike_out_final;

    // Instantiate the lif_neuron_network module
    lif_neuron_network lif_net (
        .clk(clk),
        .reset(!rst_n),                   // Correct for active-low reset
        .external_input_1(ui_in[4:0]),    // Use the lower 5 bits of ui_in for Neuron 1
        .external_input_2(ui_in[4:0]),    // For testing, input the same signal to all neurons
        .external_input_3(ui_in[4:0]),    // Adjust as needed for different signals
        .spike_1(spike_out_1),            // Connect spike outputs to internal signals
        .spike_2(spike_out_2),
        .spike_3(spike_out_3),
        .spike_output(spike_out_final)    // Final spike output
    );

    // Use the final spike output in uio_out[7] for observation
    assign uio_out[7] = spike_out_final;

    // Combine individual neuron spike outputs into uo_out for monitoring
    assign uo_out = {4'b0000, spike_out_3, spike_out_2, spike_out_1, spike_out_final};

endmodule
