`default_nettype none

module lif(
    input wire [4:0] current,      // 5-bit input current
    input wire clk,                // Clock signal
    input wire reset,              // Reset signal
    output reg [4:0] state,        // 5-bit membrane potential state
    output reg spike               // Spike output
);

    // Internal signals
    wire [4:0] NS;                 // Next state (membrane potential)
    reg [4:0] threshold;           // Threshold for firing

    always @(posedge clk or posedge reset) begin
        if (!reset) begin
            state <= 5'd0;         // Reset state to 0
            threshold <= 5'd15;    // Set threshold (can be parameterized)
            spike <= 0;            // Reset spike output
        end else begin
            state <= NS;           // Update state to next state
            spike <= (NS >= threshold); // Set spike if threshold is crossed
            if (NS >= threshold) begin
                state <= 5'd0;     // Reset state after firing
            end
        end    
    end

    // Leaky integration: add current and decay state
    assign NS = current + (state >> 1); // Leak by shifting state right

endmodule
