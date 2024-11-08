`default_nettype none

module lif_neuron_network(
    input wire clk,                           // Clock signal
    input wire reset,                         // Reset signal
    input wire [4:0] external_input_1,        // 5-bit input for Neuron 1
    input wire [4:0] external_input_2,        // 5-bit input for Neuron 2
    input wire [4:0] external_input_3,        // 5-bit input for Neuron 3
    output wire spike_1,                      // Spike output from Neuron 1
    output wire spike_2,                      // Spike output from Neuron 2
    output wire spike_3,                      // Spike output from Neuron 3
    output wire spike_output                  // Spike output from the output neuron
);

    // Internal signals for spikes and input current for the output neuron
    wire spike_out_1, spike_out_2, spike_out_3;
    reg [4:0] input_current_output;           // 5-bit input for the output neuron

    // Weights for synaptic connections from input neurons to the output neuron
    parameter [4:0] weight_1_to_output = 5'd2;  // Spike weight from Neuron 1 to Output Neuron
    parameter [4:0] weight_2_to_output = 5'd2;  // Spike weight from Neuron 2 to Output Neuron
    parameter [4:0] weight_3_to_output = 5'd2;  // Spike weight from Neuron 3 to Output Neuron

    // Instantiate the three input neurons with 5-bit width
    lif neuron1 (.current(external_input_1), .clk(clk), .reset(reset), .state(), .spike(spike_out_1));
    lif neuron2 (.current(external_input_2), .clk(clk), .reset(reset), .state(), .spike(spike_out_2));
    lif neuron3 (.current(external_input_3), .clk(clk), .reset(reset), .state(), .spike(spike_out_3));

    // Instantiate the output neuron with a 5-bit width
    lif output_neuron (.current(input_current_output), .clk(clk), .reset(reset), .state(), .spike(spike_output));

    // Generate the input current for the output neuron based on spikes from the input neurons
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            input_current_output <= 5'd0;
        end else begin
            // If an input neuron spikes, add its weighted contribution to the output neuron's input current
            input_current_output <= (spike_out_1 ? weight_1_to_output : 5'd0) +
                                    (spike_out_2 ? weight_2_to_output : 5'd0) +
                                    (spike_out_3 ? weight_3_to_output : 5'd0);
        end
    end

    // Assign spike outputs for observation
    assign spike_1 = spike_out_1;
    assign spike_2 = spike_out_2;
    assign spike_3 = spike_out_3;

endmodule
