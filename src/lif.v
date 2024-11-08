`default_nettype none
module lif(
    input wire [3:0] current,
    input wire clk,
    input wire reset,
    output reg [3:0] state,
    output wire spike
);

    wire [3:0] NS;
    reg [3:0] threshold;

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            state <= 0;
            threshold <= 8;
        end else if (spike) begin
            state <= 0;  // Reset state when spike occurs
        end else begin
            state <= NS;
        end    
    end

    // Leaky integration: add current and decay state
    assign NS = current + (state >> 1);

    // Generate spike when state reaches or exceeds the threshold
    assign spike = (state >= threshold); 

endmodule
