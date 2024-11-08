`default_nettype none

module lif(
    input wire [4:0] current,      // 5-bit input current
    input wire clk,                // Clock signal
    input wire reset,              // Active-low reset signal
    output reg [4:0] state,        // 5-bit membrane potential state
    output wire spike               // Spike output
);

    // Internal signals
    wire [4:0] NS;                 // Next state (membrane potential)
    // parameter [4:0] threshold = 5'd10;  // Threshold for firing, set as parameter

    // always @(posedge clk or negedge reset) begin
    //     if (!reset) begin
    //         state <= 5'd0;         // Reset state to 0
    //         spike <= 0;            // Reset spike output
    //     end else begin
    //         if (NS >= threshold) begin
    //             spike <= 1;        // Set spike when NS crosses threshold
    //             state <= 5'd0;     // Reset state after firing
    //         end else begin
    //             state <= NS;       // Update state to next state
    //         end
    //     end    
    // end
    assign spike = current[4] | current[3] | current[2] | current[1];

    // Leaky integration: add current and decay state
    assign NS = current + (state >> 1); // Leak by shifting state right

endmodule
