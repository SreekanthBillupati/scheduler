// Use mask to identify the last grant
// Round robin arbiter

`timescale 1us/1us

module round_robin_arbiter (
  input     logic          clk  ,
  input     logic          rst_n,

  input     logic   [3:0]  req_i,
  output    logic   [3:0]  gnt_o
);

 //internal logic here
  assign gnt_o[0] = req_i[0];

  genvar i;
  for (i=1; i<NUM_PORTS; i=i+1) begin
    assign gnt_o[i] = req_i[i] & ~(|gnt_o[i-1:0]);
  end
endmodule
