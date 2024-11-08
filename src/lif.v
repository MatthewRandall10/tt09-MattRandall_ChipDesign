module lif(
    input wire [4:0]    current,
    input wire  clk,
    input wire reset,
    output reg [4:0] state,
    output wire spike
);

    wire [4:0] NS;
    reg [4:0] threshold;

    always @(posedge clk) begin
        if (!reset) begin
            state <= 0;
            threshold <= 10;
        end else begin
            state <= NS;
        end    
    end


    assign NS = current + (state >> 1);
    assign spike = (state >= threshold); 
endmodule
