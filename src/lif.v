`default_nettype none

module lif(
    input wire [4:0] current,      // 5-bit input current
    input wire clk,                // Clock signal
    input wire reset,              // Active-low reset signal
    output reg [4:0] state,        // 5-bit membrane potential state
    output reg spike               // Spike output
);

    // Internal signals
    wire [4:0] NS;                 // Next state (membrane potential)
    reg [4:0] threshold;           // Threshold for firing

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            state <= 5'd0;         // Reset state to 0
            threshold <= 5'd15;    // Set threshold (can be parameterized)
            spike <= 0;            // Reset spike output
        end else begin
            state <= NS;           // Update state to next state
            // Generate a single-cycle spike when NS crosses the threshold
            if (NS >= threshold) begin
                spike <= 1;
                state <= 5'd0;     // Reset state after firing
            end else begin
                spike <= 0;        // Clear spike after the pulse
            end
        end    
    end

    // Leaky integration: add current and decay state
    assign NS = current + (state >> 1); // Leak by shifting state right

endmodule
