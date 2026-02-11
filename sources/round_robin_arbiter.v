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

endmodule