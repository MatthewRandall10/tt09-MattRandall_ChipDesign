// SPDX-License-Identifier: Apache-2.0

`default_nettype none

module tt_um_lif_network_MR (
    input  wire [7:0] ui_in,     // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path for neuron inputs
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,       // always 1 when the design is powered, so you can ignore it
    input  wire       clk,       // clock
    input  wire       rst_n      // reset_n - low to reset
);

    // Set `uio_oe` to 0 for inputs and 1 for outputs
    assign uio_oe = 8'b11110000;  // Lower 4 bits for inputs, upper 4 bits for outputs
    assign uio_out[3:0] = 0;
    // Prevent warnings by marking unused inputs
    wire _unused = &{ena, 1'b0, uio_in[7:4]};

    // Internal wires for spike outputs from neurons in the network
    wire spike_out_1, spike_out_2, spike_out_3, spike_out_final;

    // Instantiate the lif_neuron_network module with unique inputs for each neuron
    lif_neuron_network lif_net (
        .clk(clk),
        .reset(rst_n),                   
        .external_input_1(uio_in[3:0]),  // Unique input for Neuron 1
        .external_input_2(ui_in[7:4]),  // Unique input for Neuron 2
        .external_input_3(ui_in[3:0]),  // Unique input for Neuron 3
        .spike_1(spike_out_1),              
        .spike_2(spike_out_2),
        .spike_3(spike_out_3),
        .spike_output(spike_out_final)     
    );

    // Use the final spike output in uio_out[7] for observation
    assign uio_out[7] = spike_out_final;
    assign uio_out[6] = spike_out_3;
    assign uio_out[5] = spike_out_2;
    assign uio_out[4] = spike_out_1;

    // Combine individual neuron spike outputs into uo_out for monitoring
    assign uo_out = {4'b0, spike_out_3, spike_out_2, spike_out_1, spike_out_final};

endmodule
