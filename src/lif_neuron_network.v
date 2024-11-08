`default_nettype none

module lif_neuron_network(
    input wire clk,                           // Clock signal
    input wire reset,                         // Active-low reset signal
    input wire [3:0] external_input_1,        // 5-bit input for Neuron 1
    input wire [3:0] external_input_2,        // 5-bit input for Neuron 2
    input wire [3:0] external_input_3,        // 5-bit input for Neuron 3
    output wire spike_1,                      // Spike output from Neuron 1
    output wire spike_2,                      // Spike output from Neuron 2
    output wire spike_3,                      // Spike output from Neuron 3
    output reg [3:0] state,
    output wire spike_output                  // Spike output from the output neuron
);

    // Internal signals for spikes and input current for the output neuron
    wire spike_out_1, spike_out_2, spike_out_3;
    reg [3:0] input_current_output;           // 5-bit input for the output neuron

    // Weights for synaptic connections from input neurons to the output neuron
    parameter [3:0] weight_1_to_output = 4'd5;  // Spike weight from Neuron 1 to Output Neuron
    parameter [3:0] weight_2_to_output = 4'd4;  // Spike weight from Neuron 2 to Output Neuron
    parameter [3:0] weight_3_to_output = 4'd3;  // Spike weight from Neuron 3 to Output Neuron

    // Instantiate the three input neurons with 5-bit width
    lif neuron1 (.current(external_input_1), .clk(clk), .reset(reset), .state(), .spike(spike_out_1));
    lif neuron2 (.current(external_input_2), .clk(clk), .reset(reset), .state(), .spike(spike_out_2));
    lif neuron3 (.current(external_input_3), .clk(clk), .reset(reset), .state(), .spike(spike_out_3));

    // Instantiate the output neuron with a 5-bit width
    lif output_neuron (.current(input_current_output), .clk(clk), .reset(reset), .state(), .spike(spike_output));

        // Generate the input current for the output neuron based on spikes from the input neurons
    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            input_current_output <= 4'd0;  // Ensure full reset on reset
        end else if (spike_out_1 || spike_out_2 || spike_out_3) begin
            // Accumulate contributions only when there is a spike from any input neuron
            input_current_output <= ({4{spike_out_1}} & weight_1_to_output) +
                                    ({4{spike_out_2}} & weight_2_to_output) +
                                    ({4{spike_out_3}} & weight_3_to_output);
             
        end else begin
            input_current_output <= 4'd0;  // Set to zero when there are no spikes
            
        end
    end

    always @(*) begin 
        state = input_current_output;
    end

    


    // Assign spike outputs for observation
    assign spike_1 = spike_out_1;
    assign spike_2 = spike_out_2;
    assign spike_3 = spike_out_3;

endmodule
